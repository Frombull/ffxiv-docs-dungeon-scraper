from google.oauth2 import service_account

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SERVICE_ACCOUNT_FILE = 'top_secret_keys.json'
CREDS = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)

NONE_DICT = {
            "name": 'None',
            "type": 'None',
            "level": 'None',
            "ilevel": 'None',
            "expansion": 'None',
            "patch": 'None',
            "difficulty": 'None',
            "party_size": 'None',
            "url": 'None'
        }
