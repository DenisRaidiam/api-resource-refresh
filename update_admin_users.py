import os
import requests
import json
from urllib.parse import quote
from dotenv import load_dotenv

ORG_ID = "3ffb8191-13c1-43e3-ac0e-5fbefacc6fc4"
BASE_URL = "https://matls-api.sandbox.raidiam.io"

load_dotenv()

ORG = os.getenv('ORG')
ENV = os.getenv('ENV')


def main():
    access_token = f'Bearer {os.getenv("ACCESS_TOKEN")}'
    get_orgadmin_user(access_token)

def get_orgadmin_user(access_token):
    response = requests.get(f'{BASE_URL}/organisations/{ORG_ID}/adminusers',
                            headers={'Authorization': access_token},
                            verify=False,
                            cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 200:
        users = json.loads(response.content.decode('utf-8'))
        print(f"Total users fetched: {len(users)}")
        return users
    else:
        print(f"Failed to retrieve users. Status code: {response.status_code}")
        return []

def filter_orgadmin_users(users, status_filter='Active'):
    qa_users = [user for user in users if user.get('UserEmail', '').startswith('qa_') and user.get('Status') == status_filter]
    print(f"Total 'qa_' users with status '{status_filter}': {len(qa_users)}")
    return qa_users

def update_orgadmin_user_status(access_token,orgadmin_user_email):
    url = f'{BASE_URL}/organisations/{ORG_ID}/adminusers/{orgadmin_user_email}'

    payload = {
        "Status": "Inactive"
    }

    response = requests.put(url,
                            json=payload,
                            headers={'Authorization': access_token},
                            verify=False,
                            cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 200:
        print(f"Successfully updated status for {orgadmin_user_email}")
    else:
        print(f"Failed to update status for {orgadmin_user_email}. Status code: {response.status_code}")


def main():
    access_token = f'Bearer {os.getenv("ACCESS_TOKEN")}'
    all_users = get_orgadmin_user(access_token)
    filtered_users = filter_orgadmin_users(all_users)

    for user in filtered_users:
        update_orgadmin_user_status(access_token, user['UserEmail'])

if __name__ == '__main__':
    main()
