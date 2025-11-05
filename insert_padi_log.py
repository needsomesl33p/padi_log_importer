import json
import csv
import httpx
import time
from datetime import datetime as dt


url = "https://logbook.global-prod.padi.com/api/Logbook"
auth_token = "YOUR_JWT_AUTH_TOKEN_GOES_HERE"
headers = {
    "accept": "application/json, text/plain, */*",
    "accept-language": "en-GB,en;q=0.9",
    "affiliate-id": "31557437",
    "authorization": f"Bearer {auth_token}",
    "content-type": "application/json",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36",
    "x-platform": "web",
}


def read_json_file(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    return data


def fill_logbook(payload, dive_data, created_at):
    payload['variables']['general']['dive_title'] = dive_data['title']
    payload['variables']['general']['dive_location'] = dive_data['location']
    payload['variables']['general']['dive_date'] = dive_data['date']
    payload['variables']['general']['created_date'] = created_at
    payload['variables']['general']['update_date'] = created_at
    payload['variables']['general']['depth_times']['data']['bottom_time'] = dive_data['bottom_time']
    payload['variables']['general']['depth_times']['data']['max_depth'] = dive_data['max_depth']
    payload['variables']['general']['equipment']['data']['gas_mixture'] = dive_data['gas_mixture']
    payload['variables']['general']['equipment']['data']['oxygen'] = dive_data['oxygen']
    payload['variables']['general']['equipment']['data']['nitrogen'] = dive_data['nitrogen']
    payload['variables']['general']['experiences']['data']['notes'] = dive_data['notes']
    return payload


def get_iso_datetime_now():
    now = dt.now()
    return now.isoformat().split(".")[0]


def build_query(payload):
    variables = json.dumps(payload['variables'])
    query = '{"query":"mutation insert_logbook_logs($general: [logbook_logs_insert_input!]!) {\n  insert_logbook_logs(objects: $general) {\n    affected_rows\n    returning {\n      id\n      affiliate_id\n      dive_title\n      dive_type\n      dive_location\n      log_type\n      log_course\n      dive_date\n      created_date\n      status\n      adventure_dive\n    }\n  }\n}", "variables": ' + variables + '}'
    return query


def main():
    payload_prototype = read_json_file('payload_prototype.json')
    with open('dives.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        for dive in reader:
            log = fill_logbook(payload_prototype, dive, get_iso_datetime_now())
            payload = build_query(log)


            with httpx.Client() as client:
                print(f"[!] Sending dive log: {dive['title']}")
                response = client.post(url, headers=headers, data=payload)
                print(f"[!] Response status code: {response.status_code}")
                print(f"[!] Response text: {response.text[:150]}")
            time.sleep(1)


if __name__ == "__main__":
    main()