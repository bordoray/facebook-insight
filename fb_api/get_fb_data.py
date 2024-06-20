import requests
import json

import download_image as img

# Get your token here (authorize users photo)
# https://developers.facebook.com/tools/explorer/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.11
# Paste here
token = "your token"

a = 0
inbounds = []


def get_fb_api_result(token):
    url = (
        "https://graph.facebook.com/v11.0/me?fields=albums%7Bphotos.limit(600)%7Bpicture%2Cplace%7D%7D&limit=800&access_token="
        + token
    )
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Assuming the API returns a JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


# TODO Adjust
def nextpage_album(url):
    try:
        print(url)
        response = requests.get(url)
        # response.raise_for_status()
        result = response.json()
        print(result.keys())
        albums = result["data"]
        process_album(albums)

        if "paging" in result and "next" in result["paging"]:
            nextpage_album(result["paging"]["next"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


def add_geojson(thumb, place_name, lon, lat):
    if lon and lat:
        feature = {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"name": place_name, "img": img.get_image_filename(thumb)},
        }
        inbounds.append(feature)
        # img.download_image(thumb)


def process_album(albums):
    for album in albums:
        # In one album, first page
        if album.get("id") == "1495671911263":
            a = 1

        if "photos" in album:
            photos = album["photos"]["data"]

            for photo in photos:
                thumb = photo["picture"]
                if "place" in photo and "location" in photo["place"]:
                    place_name = photo["place"]["name"]
                    if (
                        "longitude" in photo["place"]["location"]
                        and "latitude" in photo["place"]["location"]
                    ):
                        lon = photo["place"]["location"]["longitude"]
                        lat = photo["place"]["location"]["latitude"]
                        add_geojson(thumb, place_name, lon, lat)
                    else:
                        print("skip following photo due to no coordinates")
                        print(photo)
                else:
                    # Print or handle missing location information
                    pass

            if "paging" in album["photos"] and "next" in album["photos"]["paging"]:

                nextpage_photo(album["photos"]["paging"]["next"])


def nextpage_photo(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        photos = result["data"]
        for pic in photos:
            if "place" in pic and "location" in pic["place"]:
                thumb = pic["picture"]
                place_name = pic["place"]["name"]
                if (
                    "longitude" in pic["place"]["location"]
                    and "latitude" in pic["place"]["location"]
                ):
                    lon = pic["place"]["location"]["longitude"]
                    lat = pic["place"]["location"]["latitude"]
                    add_geojson(thumb, place_name, lon, lat)
                else:
                    print("skip following photo due to no coordinates")
                    print(pic)

        if "paging" in result["data"] and "next" in result["data"]["paging"]:
            nextpage_photo(result["data"]["paging"]["next"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


def main():
    result = get_fb_api_result(token)
    albums = result["albums"]["data"]
    process_album(albums)

    if "next" in result["albums"]["paging"]:
        nextpage_album(result["albums"]["paging"]["next"])
    else:
        print(inbounds[0])
    return


def save_json_to_js_file(json_data, file_path):
    try:
        # Convert the JSON data to a pretty-printed JSON string
        json_string = json.dumps(json_data, indent=4)

        # Create the JavaScript content
        js_content = f"const json_contents = {json_string};"

        # Write the JavaScript content to the file
        with open(file_path, "w") as file:
            file.write(js_content)

        print(f"JavaScript file successfully written to {file_path}")
    except IOError as e:
        print(f"Error writing JavaScript file: {e}")


main()
print(len(inbounds))

save_json_to_js_file(inbounds, "rlinsight_data.js")
