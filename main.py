import os
import json
import requests
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# 1. Setup Credentials from GitHub Secret
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
service_account_info = json.loads(os.environ["GCP_SERVICE_ACCOUNT_JSON"])
creds = Credentials.from_service_account_info(service_account_info, scopes=scopes)
gc = gspread.authorize(creds)

# 2. Config
SPREADSHEET_ID = 'YOUR_SPREADSHEET_ID_HERE'
STATIONS = {
    "Frankston Beach": "http://www.bom.gov.au/fwo/IDV60901/IDV60901.95866.json",
    "Fawkner Beacon": "http://www.bom.gov.au/fwo/IDV60801/IDV60801.95872.json",
    "South Channel": "http://www.bom.gov.au/fwo/IDV60901/IDV60901.94852.json"
}

def get_data():
    all_rows = []
    headers = {'User-Agent': 'Mozilla/5.0'}
    for name, url in STATIONS.items():
        try:
            res = requests.get(url, headers=headers).json()
            latest = res['observations']['data'][0]
            dt = datetime.strptime(latest['local_date_time_full'], '%Y%m%d%H%M%S')
            all_rows.append([
                dt.strftime('%d-%m-%Y'),
                dt.strftime('%H:%M'),
                name,
                latest['wind_spd_kt'],
                latest['wind_dir']
            ])
        except Exception as e:
            print(f"Error {name}: {e}")
    return all_rows

# 3. Run
sheet = gc.open_by_key(SPREADSHEET_ID).worksheet("WindData")
data = get_data()
if data:
    sheet.append_rows(data)
