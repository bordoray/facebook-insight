import requests
import json

import download_image as img

# Get your token here (authorize users photo)
# https://developers.facebook.com/tools/explorer/?method=GET&path=me%3Ffields%3Did%2Cname&version=v2.11

token = "paste your token here"
token = "EAAbZBxNmEZCMABO450FZCy8PbWENpej4r4QaZCTMwVeVKi7cifKdNk8Ibe9qIWfSjYrItz7oHogl3bieWqYeGZCGqzMzqZBwupbagDw8SjlZAZCMhGEYMdGMfkBQOD6x7Sx6d0A4DMu67C0MJt0k6tvkCJpn2JmX5kQvJVFBrwoSnhpMMIPIYLIs2iBLBlDZA14274h1y2JcsDhymn7x6Hwtf55RlDXtlZCOTOPnz54S1IukzTj3gn6zs2cjgw6ZAiccfZBATqkgBRgO"

inbounds = []


def get_fb_api_result(url):

    # url = (
    #     "https://graph.facebook.com/v20.0/me?fields=photos{place,name,picture}&access_token="
    #     + token
    # )
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
        return response.json()  # Assuming the API returns a JSON response
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


def nextpage_album(url):
    try:
        print(f"next page : {url}")
        response = requests.get(url)
        result = response.json()

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
        img.download_image(thumb)


def process_album(albums):
    for album in albums:
        # In one album, first page
        if album.get("id") == "1495671911263":
            pass

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
        else:
            print(result["data"])

    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as err:
        print(f"Error occurred: {err}")


def check_attributes(json_data):
    if "place" in json_data and isinstance(json_data["place"], dict):
        place = json_data["place"]

        # Check if 'name' key exists in 'place'
        if "name" not in place:
            return False

        # Check if 'location' key exists and is a dictionary in 'place'
        if "location" in place and isinstance(place["location"], dict):
            location = place["location"]

            # Check if 'latitude' and 'longitude' keys exist in 'location'
            if "latitude" in location and "longitude" in location:
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def process_photos(response_data):
    for data in response_data["photos"]["data"]:
        having_place = check_attributes(data)
        if having_place:
            thumb = data["picture"]
            place_name = data["place"]["name"]
            lon = data["place"]["location"]["longitude"]
            lat = data["place"]["location"]["latitude"]
            add_geojson(thumb, place_name, lon, lat)
            # print(data)
    if "paging" in response_data["photos"]:
        if "next" in response_data["photos"]["paging"]:
            response = get_fb_api_result(response_data["photos"]["paging"]["next"])
            process_photos(response)


def main():
    url = (
        "https://graph.facebook.com/v20.0/me?fields=photos{place,name,picture}&access_token="
        + token
    )
    result = get_fb_api_result(url)
    # print(result)
    # file_path = "/Users/rlay/Documents/github/facebook-insight/fb_sample.json"
    # # Write the JSON data to a file
    # with open(file_path, "r") as file:
    #     result = json.load(file)
    process_photos(result)
    # albums = result["albums"]["data"]
    # process_album(albums)
    # print(inbounds)

    # if "next" in result["albums"]["paging"]:
    #     nextpage_album(result["albums"]["paging"]["next"])

    return


def save_json_to_js_file(json_data, file_path):
    try:
        # Convert the JSON data to a pretty-printed JSON string
        json_string = json.dumps(json_data, indent=4)

        # Create the JavaScript content
        js_content = 'const inbjson = {"type": "FeatureCollection","features": '
        js_content += json_string
        js_content += "};"

        # Write the JavaScript content to the file
        with open(file_path, "w") as file:
            file.write(js_content)

        print(f"JavaScript file successfully written to {file_path}")
    except IOError as e:
        print(f"Error writing JavaScript file: {e}")


main()
print(f"{len(inbounds)} pics processed")

save_json_to_js_file(inbounds, "rlinsight_data.js")
