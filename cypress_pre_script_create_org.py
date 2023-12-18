import os
import requests
import uuid

import json
from urllib.parse import quote
from dotenv import load_dotenv

ORG_ID = "ORG0000001"
AUTH_DOMAIN = "Ergonomic Frozen Cheese"
BASE_URL = "https://matls-api.sandbox.raidiam.io"

load_dotenv()

ORG = os.getenv('ORG')
ENV = os.getenv('ENV')


def main():
    access_token = f'Bearer {os.getenv("ACCESS_TOKEN")}'

    create_org_response = create_organisation(access_token)
def create_organisation(access_token):
    unique_id = uuid.uuid4()  # Generate a unique UUID

    organisation_id = f"ORG{unique_id}"
    organisation_name = f"Organisation {unique_id}"

    url = f'{BASE_URL}/organisations/'

    url = f'{BASE_URL}/organisations/'

    payload = {
        "AddressLine1": "test line 1",
        "AddressLine2": "test line 2",
        "City": "London",
        "CompanyRegister": "  REG123",
        "Country": "United Kingdom",
        "CountryOfRegistration": "United Kingdom",
        "LegalEntityName": " LEG1234",
        "OrganisationId": organisation_id,
        "OrganisationName": organisation_name,
        "ParentOrganisationReference": "string",
        "Postcode": "ME19 5FG",
        "RegisteredName": " Registration Number 1",
        "RegistrationId": " Reg Id number 1",
        "RegistrationNumber": "REG123",
        "RequiresParticipantTermsAndConditionsSigning": True,
        "Size": "string",
        "Status": "Active",
        "Tags": ["string"]
    }

    response = requests.post(url,
                             json=payload,
                             headers={'Authorization': access_token},
                             verify=False,
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print(f"Successfully created organisation with ID {organisation_id} and Name '{organisation_name}'")
    else:
        print(f"Failed to create organisation. Status Code: {response.status_code}")

def create_auth_domain_role(organisation_id):
    {

    }

if __name__ == '__main__':
    main()
