# Python API Scripts Repository

This repository contains Python scripts designed to run various API calls. To set up and use these scripts correctly, follow the instructions below.

## Prerequisites

- Python 3.x
- Basic understanding of Python and API interactions

## Setup Instructions

### Certificate Folder

1. **Create a Cert Folder:**
    - In the root directory of this project, create a folder named `cert`.

2. **Add Certificate Files:**
    - Inside the `cert` folder, add the following files:
        - `transport.pem`: Your PEM certificate file.
        - `transport.key`: Your key file corresponding to the PEM certificate.

### Environment Variables

1. **Create .env File:**
    - In the root directory, create a file named `.env`.

2. **Add the Following Variables to .env File:**
   ACCESS_TOKEN=<Your Access Token>
   ORG=raidiam
   ENV=sb
   BASE_URL=https://matls-api.sandbox.raidiam.io
3. Replace `<Your Access Token>` with the access token which can be retrieved from Postman.

## Running the Scripts

To run the scripts, use the following command in your terminal:

```bash
python <script_name>.py

Replace <script_name> with the actual name of the Python script you want to execute.

## Additional Information

Security Note: Ensure that the .env file and the cert folder are secure and not publicly accessible, as they contain sensitive information.
Token Update: Regularly update the ACCESS_TOKEN as per your authentication policy requirements.

