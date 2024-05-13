import requests
from key import konbert_api_key
import os

# API key is obtained here after creating an account: https://konbert.com/account 
api_key = konbert_api_key
api_endpoint = "https://konbert.com/api/v1/convert"

headers = {
    "Authorization": f"Bearer {api_key}"
}

data = {
    "input[format]": "avro",
    "output[format]": "csv",
    "sync": "true"
}

# List of input file paths
input_file_paths = ["AVROS final/Primera/Meditador 1/1-1-MED1_1714159675.avro", "AVROS final/Primera/Meditador 1/1-1-MED1_1714161478.avro", "AVROS final/Primera/Meditador 11-1-MED1_1714163277.avro"]

for input_file_path in input_file_paths:
    output_file_path = os.path.splitext(input_file_path)[0] + ".csv"

    files = {
        "input[file]": open(input_file_path, 'rb')
    }

    response = requests.post(api_endpoint, headers=headers, data=data, files=files)

    if response.status_code != 200:
        print(f"Error: Failed to convert file {input_file_path}")
        print(f"Response: {response.text}")
        continue

    if response.text:
        with open(output_file_path, 'w') as f:
            f.write(response.text)
        print(f"File {input_file_path} converted successfully")