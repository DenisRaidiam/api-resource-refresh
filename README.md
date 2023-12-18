Python API Scripts Repository
This repository contains a collection of Python scripts designed to interact with various APIs. To ensure these scripts run correctly, please follow the setup instructions detailed below.

Prerequisites
Before running the scripts, ensure you have Python installed on your machine. These scripts are tested on Python 3.6 and above.

Setup Instructions

Step 1: Certificate Folder Creation
Create a folder named cert in the root directory of this repository.
Inside the cert folder, add the following files:
transport.pem: This is your PEM (Privacy Enhanced Mail) certificate file.
transport.key: This is your key file corresponding to the PEM certificate.

Step 2: Environment Variables Setup
Create a new file named .env in the root directory of the repository.

Add the following environment variables to the .env file:
makefile
Copy code
ACCESS_TOKEN=<Your Access Token>
ORG=raidiam
ENV=sb
BASE_URL=https://matls-api.sandbox.raidiam.io
ACCESS_TOKEN: This is the access token for API authentication. It can be retrieved using Postman or a similar API testing tool.
ORG, ENV, BASE_URL: These are pre-configured values for the Raidiam environment.
Step 3: Installing Dependencies
Run the following command to install necessary Python libraries:

Copy code
pip install -r requirements.txt
Running the Scripts
After completing the setup, you can run the Python scripts as follows:

php
Copy code
python <script_name>.py
Replace <script_name> with the name of the script you wish to run.

Additional Information
Ensure that the .env file and the cert folder are not shared publicly as they contain sensitive information.
Update the ACCESS_TOKEN regularly as per your authentication policy.
