import requests
import json
import os
from dotenv import load_dotenv

def upload_pdf_to_pinata(pdf_path: str, document_type: str): # document_type is either CARD or LOAN
    """
    Uploads a PDF file to Pinata and returns the IPFS hash and Pinata URL.

    :param pdf_path: The local path to the PDF file.
    :return: A dictionary with 'IpfsHash' and 'PinataURL' if successful, else None.
    """
    # Load environment variables from .env file
    load_dotenv()
    PINATA_API_KEY = os.getenv('PINATA_API_KEY')
    PINATA_SECRET_API_KEY = os.getenv('PINATA_API_SECRET')

    if not PINATA_API_KEY or not PINATA_SECRET_API_KEY:
        print("Error: Pinata API credentials not found in environment variables.")
        return None

    # Define the Pinata API endpoint
    PINATA_URL = "https://api.pinata.cloud/pinning/pinFileToIPFS"

    # Define the headers
    headers = {
        "pinata_api_key": PINATA_API_KEY,
        "pinata_secret_api_key": PINATA_SECRET_API_KEY
    }

    # Check if the file exists
    if not os.path.isfile(pdf_path):
        print(f"Error: The file {pdf_path} does not exist.")
        return None

    try:
        with open(pdf_path, 'rb') as pdf_file:
            # Prepare the files dictionary
            files = {
                'file': (os.path.basename(pdf_path), pdf_file, 'application/pdf')
            }

            # Optional: Add metadata
            metadata = {
                "name": document_type + "_" + pdf_path.split('_')[-2] + "_" + pdf_path.split('_')[-1],
                "keyvalues": {
                    "description": "This is a sample PDF file."
                }
            }

            # Convert metadata to JSON string
            json_metadata = json.dumps(metadata)

            # Prepare the data payload
            data = {
                'pinataMetadata': json_metadata
            }

            # Send the POST request
            response = requests.post(PINATA_URL, files=files, data=data, headers=headers)

            # Check the response status
            if response.status_code == 200:
                response_json = response.json()
                print("Upload successful!")
                print("IPFS Hash:", response_json['IpfsHash'])
                print(response_json)
                return response_json
            else:
                print(f"Upload failed with status code {response.status_code}")
                print("Response:", response.text)
                return None

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# # Usage Example
# if __name__ == "__main__":
#     # Path to your local PDF file
#     pdf_file_path = './applications/loan_application_ACC123_20241117091458.pdf'

#     # Upload the PDF to Pinata
#     result = upload_pdf_to_pinata(pdf_file_path)

