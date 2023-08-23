import json
import os
from datetime import datetime, timedelta

import requests as requests
from dotenv import load_dotenv

load_dotenv()

ORG = os.getenv('ORG')
ENV = os.getenv('ENV')
ACCESS_TOKEN = f'Bearer {os.getenv("ACCESS_TOKEN")}'
BASE_URL = os.getenv('BASE_URL')


def main():
    org_ids = get_org_ids()
    print(f'org ids {org_ids}')
    failed_api_resources = process_org_ids(org_ids)
    print(f'failed api resources - {failed_api_resources}')


def load_api_family_filter():
    with open(f'organisations/{ORG}/{ENV}/api_family_filter_list.json') as json_file:
        return json.load(json_file)


def process_org_ids(org_ids):
    failed_resources = list()
    for org_id in org_ids:
        print(f'processing {org_id} organisation')
        url = f'{BASE_URL}/organisations/{org_id}/authorisationservers'
        try:
            response = requests.get(url,
                                    headers={'Authorization': ACCESS_TOKEN},
                                    verify=False,
                                    cert=(f'organisations/{ORG}/{ENV}/certs/transport.pem',
                                          f'organisations/{ORG}/{ENV}/certs/transport.key'), )

            if response.status_code == 200:
                json_response = response.json()
                for server in json_response:
                    process_server(failed_resources, org_id, server)
            else:
                print(f'Could not get API Resource IDs | status_code {response.status_code} | message - {response.text}')
                failed_resources.append(url)

        except requests.exceptions.RequestException as e:
            print(f'Could not get API Resource IDs | reason - {e}')
            failed_resources.append(url)

    return failed_resources


def process_server(failed_resources, org_id, server):
    server_id = server['AuthorisationServerId']
    if 'ApiResources' in server:
        for resource in server['ApiResources']:
            family = resource['ApiFamilyType']
            if check_family(family) and check_endpoint(resource):
                failed_resource = update_resource(org_id, server_id, resource)
                if failed_resource is not None:
                    failed_resources.append(failed_resource)


def get_update_request_body_from_resource(resource):
    start_date = (datetime.now() - timedelta(7)).strftime('%d/%m/%Y')
    endpoint = resource['ApiDiscoveryEndpoints'][0]['ApiEndpoint']
    status = 'Self-Certified'
    if 'CertificationStatus' in resource:
        status = resource['CertificationStatus']

    return {
        "ApiVersion": resource['ApiVersion'],
        "ApiCertificationUri": endpoint,
        "CertificationStatus": status,
        "CertificationStartDate": start_date,
        "ApiFamilyType": resource['ApiFamilyType']
    }


def update_resource(org_id, server_id, resource):
    resource_id = resource['ApiResourceId']
    print(f'Updating API resource - {resource_id} in AS - {server_id} in org - {org_id}')
    url = f'{BASE_URL}/organisations/{org_id}/authorisationservers/{server_id}/apiresources/{resource_id}'
    try:
        response = requests.put(url,
                                headers={'Authorization': ACCESS_TOKEN},
                                json=get_update_request_body_from_resource(resource),
                                verify=False,
                                cert=(f'organisations/{ORG}/{ENV}/certs/transport.pem',
                                      f'organisations/{ORG}/{ENV}/certs/transport.key'), )

        if response.status_code == 200:
            print(f'Updated API resource - {resource_id} in AS - {server_id} in org - {org_id}')
            return None

        print(f'Could not update API resource - {resource_id} in AS - {server_id} in org - {org_id} | code - {response.status_code} | response - {response.text}')
    except requests.exceptions.RequestException as e:
        print(f'Could not update API resource - {resource_id} in AS - {server_id} in org - {org_id} | Reason - {e}')

    return url


def check_family(family):
    family_filter = load_api_family_filter()
    return family in family_filter


def check_endpoint(resource):
    if 'ApiDiscoveryEndpoints' not in resource:
        print(f'Could not find ApiDiscoveryEndpoints key in resource {resource}')
        return False

    endpoints = resource['ApiDiscoveryEndpoints']
    if len(endpoints) != 1:
        print(f'CS Enabled API resource has incorrect number of endpoints | resource - {resource}')
        return False
    return True


def get_org_ids():
    response = requests.get(f'{BASE_URL}/organisations',
                            headers={'Authorization': ACCESS_TOKEN}, verify=False,
                            cert=(f'organisations/{ORG}/{ENV}/certs/transport.pem',
                                  f'organisations/{ORG}/{ENV}/certs/transport.key'), )
    ids = list()

    if response.status_code == 200:
        json_response = response.json()
        for org in json_response['content']:
            ids.append(org['OrganisationId'])

        print(f'Returning {len(ids)} ORG IDs')
        return ids

    else:
        print(f'Could not get org IDs| status_code {response.status_code} | message - {response.text}')


if __name__ == '__main__':
    main()
