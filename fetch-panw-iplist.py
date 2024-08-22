import csv
import requests

def retrieve_data(url, payload, headers):
    response = requests.get(url, params=payload, headers=headers)
    if response.status_code == 200:
        json_data = response.json()
        return json_data
    else:
        print(f"Failed to retrieve data from {url}. Status code: {response.status_code}")
        return None

def write_to_csv(json_data, csv_file):
    ip_addresses = [entry["ipaddr"] for entry in json_data["data"]]
    with open(csv_file, 'a', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for ip_address in ip_addresses:
            writer.writerow([ip_address])       

def fetch_data_and_write_to_csv(start_url, payload, headers, csv_file):
    url = start_url
    while url:
        data = retrieve_data(url, payload, headers)
        next_url = data["link"]["next"]
        print(next_url)
        if data:
            write_to_csv(data, csv_file)
            url = next_url
        else:
            break

# Usage
start_url = 'https://api.threatvault.paloaltonetworks.com/service/v1/edl?name=panw-highrisk-ip-list&version=latest'  # Replace with your actual URL
payload = {}  # Replace with your actual payload
headers = {
  'Accept': 'application/json',
  'X-API-KEY': 'API-KEY-CHANGE-ME'
}
csv_file = 'output.csv'  # Replace with your desired CSV file name

# Call the function to fetch data and write to CSV
fetch_data_and_write_to_csv(start_url, payload, headers, csv_file)
