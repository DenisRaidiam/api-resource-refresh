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
    if create_org_response:
        organisation_id = create_org_response.get('OrganisationId', ORG_ID)

        # Define the different payloads
        payloads = [
            {
                "AuthorisationDomainName": "1",
                "AuthorityId": "a80c2e9c-d491-4135-9e82-126fa18b98d5",
                "AuthorityName": "5bbb2556-cf82-4930-8812-c7a6dc1236ad"
            },
            {
                "AuthorisationDomainName": "Itaú APIs 2",
                "AuthorityId": "eb511ce9-951b-4bd1-8206-969281699401",
                "AuthorityName": "b75c4798-9923-42d6-b6be-33d354002558"
            },
            {
                "AuthorisationDomainName": "Sleek Fresh Shirt",
                "AuthorityId": "c4305896-2162-4f2f-992a-02202d9ac66f",
                "AuthorityName": "f3208de0-05ba-461b-81ae-a60fc368a539"
            }
        ]
        for payload in payloads:
            create_auth_domain_claim_response = create_authority_domain_claim(organisation_id, access_token, payload)

    create_auth_domain_role_claim_response = create_authority_domain_role(organisation_id, access_token)
    create_software_statement_response = create_software_statement(organisation_id, access_token)
    server_payloads = [
            {
                "AuthorisationServerId": str(uuid.uuid4()),
                "OrganisationId": organisation_id,
                "AutoRegistrationSupported": True,
                "SupportsCiba": True,
                "SupportsDCR": True,
                "SupportsRedirect": True,
                "CustomerFriendlyDescription": "First Authorisation Server",
                "CustomerFriendlyLogoUri": "https://example.com/logo1.svg",
                "CustomerFriendlyName": "Server One",
                "PayloadSigningCertLocationUri": "https://example.com/cert1"
            },
            {
                "AuthorisationServerId": str(uuid.uuid4()),
                "OrganisationId": organisation_id,
                "AutoRegistrationSupported": False,
                "SupportsCiba": False,
                "SupportsDCR": True,
                "SupportsRedirect": True,
                "CustomerFriendlyDescription": "Second Authorisation Server",
                "CustomerFriendlyLogoUri": "https://example.com/logo2.svg",
                "CustomerFriendlyName": "Server Two",
                "PayloadSigningCertLocationUri": "https://example.com/cert2"
            },
            {
                "AuthorisationServerId": str(uuid.uuid4()),
                "OrganisationId": organisation_id,
                "AutoRegistrationSupported": True,
                "SupportsCiba": True,
                "SupportsDCR": False,
                "SupportsRedirect": False,
                "CustomerFriendlyDescription": "Third Authorisation Server",
                "CustomerFriendlyLogoUri": "https://example.com/logo3.svg",
                "CustomerFriendlyName": "Server Three",
                "PayloadSigningCertLocationUri": "https://example.com/cert3"
            }
        ]

    # Create each authorisation server
    for server_payload in server_payloads:
            create_authorisation_server_response = create_authorisation_server(organisation_id, access_token, server_payload)

    else:
        print("Organisation creation failed, cannot proceed to create authorisation servers.")
        # Loop through each payload and create the claims



def create_organisation(access_token):
    unique_id = uuid.uuid4()  # Generate a unique UUID

    organisation_id = f"ORG{unique_id}"

    organisation_name = f"Organisation {unique_id}"
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
        return {"OrganisationId": organisation_id}  # Return necessary data
    else:
        print(f"Failed to create organisation. Status Code: {response.status_code}")
        return None


def create_authority_domain_claim(organisation_id, access_token, payload):
    url = f'{BASE_URL}/organisations/{organisation_id}/authoritydomainclaims'

    response = requests.post(url,
                             json=payload,
                             headers={'Authorization': access_token},
                             verify=False,
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print("Successfully created authority domain claim")
        return response.json()
    else:
        print(f"Failed to create authority domain claim. Status Code: {response.status_code}")
        return None


def create_authority_domain_role(organisation_id, access_token):
    url = f'{BASE_URL}/organisations/{organisation_id}/authorityclaims'

    payload = {
        "AuthorityId": "a80c2e9c-d491-4135-9e82-126fa18b98d5",
        "Status": "Active",
        "AuthorisationDomain": "1",
        "Role": "1 test advance config",
        "RegistrationId": "REG123"
    }

    response = requests.post(url,
                             json=payload,
                             headers={'Authorization': access_token},
                             verify=False,  # Consider security implications
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print("Successfully created authority domain role")
        return response.json()
    else:
        print(f"Failed to create authority domain role. Status Code: {response.status_code}")
        return None


def create_software_statement(organisation_id, access_token):
    url = f'{BASE_URL}/organisations/{organisation_id}/softwarestatements'

    unique_id = uuid.uuid4()  # Generate a unique identifier
    client_name = f"Test_Client_{unique_id}"
    description = f"Test Description {unique_id}"

    payload = {
        "ClientName": client_name,
        "Description": description,
        "LogoUri": "https://www.example.com/file.svg",
        "RedirectUri": [
            "https://www.example.com/file.svg"
        ],
        "Version": 40,
        "ClientUri": "https://www.example.com",
        "Roles": [
            {
                "Status": "Active",
                "AuthorisationDomain": "1",
                "Role": "1 test advance config"
            }
        ]
    }

    response = requests.post(url,
                             json=payload,
                             headers={'Authorization': access_token},
                             verify=False,  # Consider security implications
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print(f"Successfully created software statement with Client Name: {client_name}")
        return response.json()
    else:
        print(f"Failed to create software statement. Status Code: {response.status_code}")
        return None

def create_authorisation_server(organisation_id, access_token, server_payload):
    url = f'{BASE_URL}/organisations/{organisation_id}/authorisationservers'

    response = requests.post(url,
                             json=server_payload,
                             headers={'Authorization': access_token, 'Content-Type': 'application/json'},
                             verify=False,
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print(f"Successfully created authorisation server: {server_payload['CustomerFriendlyName']}")
        return response.json()
    else:
        print(f"Failed to create authorisation server {server_payload['CustomerFriendlyName']}. Status Code: {response.status_code}")
        return None

    response = requests.post(url,
                             json=payload,
                             headers={'Authorization': access_token, 'Content-Type': 'application/json'},
                             verify=False,
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

    if response.status_code == 201:
        print("Successfully created authorisation server")
        return response.json()
    else:
        print(f"Failed to create authorisation server. Status Code: {response.status_code}")
        return None


if __name__ == '__main__':
    main()
