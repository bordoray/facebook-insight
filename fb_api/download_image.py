from urllib.parse import urlparse
import requests
import os


def get_image_filename(url):
    parsed_url = urlparse(url)
    path = parsed_url.path
    filename = path.split("/")[-1]
    return filename


def download_image(url):
    try:
        file_path = os.path.join("./data", get_image_filename(url))
        if not os.path.isfile(file_path):
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful

            # Write the content to a file

            with open(file_path, "wb") as file:
                file.write(response.content)

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")
