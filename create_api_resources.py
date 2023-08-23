import os
from multiprocessing.pool import ThreadPool

import requests as requests
from dotenv import load_dotenv

ORG_ID = "e3bad9d5-c762-4d7b-87af-60be1be8c75b"
AS_ID = "1fdf72c8-116b-46b1-9352-f373734cfc9a"
BASE_URL = "https://matls-api.sandbox.raidiam.io"

RESOURCES = [
    {
        "family": "channels_phone-channels",
        "endpoint": "https://financiamentos.api.santander.com.br/open-banking/channels/v1/phone-channels",
    },
    {
        "family": "products-services_personal-loans",
        "endpoint": "https://financiamentos.api.santander.com.br/open-banking/products-services/v1/personal-loans",
    },
    {
        "family": "channels_electronic-channels",
        "endpoint": "https://financiamentos.api.santander.com.br/open-banking/channels/v1/electronic-channels",
    },

    {
        "family": "products-services_personal-financings",
        "endpoint": "https://hyundai.api.santander.com.br/open-banking/products-services/v1/personal-financings",
    },
    {
        "family": "products-services_business-financings",
        "endpoint": "https://hyundai.api.santander.com.br/open-banking/products-services/v1/business-financings",
    },
    {
        "family": "products-services_personal-accounts",
        "endpoint": "https://open.upp.com.br/open-banking/products-services/v1/personal-accounts",
    },
    {
        "family": "products-services_business-accounts",
        "endpoint": "https://open.upp.com.br/open-banking/products-services/v1/business-accounts",
    },
    {
        "family": "products-services_business-invoice-financings",
        "endpoint": "https://obbr.745.cipbanfico.com/open-banking/products-services/v1/business-invoice-financings",
    },
    {
        "family": "products-services_business-unarranged-account-overdraft",
        "endpoint": "https://obbr.745.cipbanfico.com/open-banking/products-services/v1/business-unarranged-account-overdraft",
    }
]

NUMBER_OF_AS = 4
FROM_AS = 0

load_dotenv()

ORG = os.getenv('ORG')
ENV = os.getenv('ENV')


def main():
    access_token = f'Bearer {os.getenv("ACCESS_TOKEN")}'

    executor = ThreadPool(2)
    futures = list()
    for i in range(FROM_AS, NUMBER_OF_AS):
        futures.append(executor.apply_async(func=create_as_server, args=(access_token, i)))
        print(f'applied {i}')

    for future in futures:
        future.get()


def create_as_server(access_token, i):
    print(f'Creating AS - {i}')
    body = {
        "Status": "Active",
        "OrganisationId": "e3bad9d5-c762-4d7b-87af-60be1be8c75b",
        "AutoRegistrationSupported": False,
        "CustomerFriendlyDescription": f'Test-{i}',
        "CustomerFriendlyLogoUri": "https://denis.podberiozkin.com/test.svg",
        "CustomerFriendlyName": f'Test-{i}',
        "PayloadSigningCertLocationUri": "https://denis.podberiozkin.com"
    }
    response = requests.post(f'{BASE_URL}/organisations/{ORG_ID}/authorisationservers',
                             json=body,
                             headers={'Authorization': access_token}, verify=False,
                             cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'), )

    if response.status_code == 201:
        as_id = response.json()['AuthorisationServerId']
        print(f'AS-{i} was created with ID - {as_id}')
        create_api_resources(as_id, access_token)
    else:
        print(f'Could not create AS-{i}')


def create_api_resources(as_id, access_token):
    print(f'Creating API resources for {as_id}')
    for resource in RESOURCES:
        body = {
            "ApiFamilyType": resource['family'],
            "ApiVersion": "1.0.0",
            "ApiCertificationUri": resource['endpoint'],
            "ApiEndpoint": resource['endpoint'],
            "CertificationStatus": "Awaiting Certification",
            "CertificationStartDate": "16/05/2023",
            "Status": "Active"
        }

        response = requests.post(f'{BASE_URL}/organisations/{ORG_ID}/authorisationservers/{as_id}/apiresources',
                                 json=body,
                                 headers={'Authorization': access_token}, verify=False,
                                 cert=(f'certs/{ORG}/{ENV}/transport.pem', f'certs/{ORG}/{ENV}/transport.key'))

        if response.status_code == 201:
            print(f'API Resource - {response.json()["ApiResourceId"]} was created for AS - {as_id}')
        else:
            print(f'Could not create APO Resource for AS - {as_id}')
            print(response.text)


if __name__ == '__main__':
    main()
