from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
import random
import requests
import json
import base64


locations = {
    "America": -90.0,
    "Atlantic Ocean": -38.0,
    "Africa": 24.0,
    "Asia": 100.0,
    "Pacific Ocean": 178.0
}


def longitude_distance(lon1, lon2):
    return min(abs(lon1 - lon2), 360 - abs(lon1 - lon2))


def find_closest_locations(images_list: list, location_longitude: float):
    """Function to find closest location for each coordinate pair in a list."""
    min_distance = 100000.0
    for img_item in images_list:
        distance = longitude_distance(img_item['centroid_coordinates']['lon'], location_longitude)
        if distance < min_distance:
            closest_item = img_item
            min_distance = distance
    return closest_item


class NasaEarthImagePiece(BasePiece):
    """
    This Piece uses the NASA EPIC API to get satellite images of the Earth.
    References:
        - https://epic.gsfc.nasa.gov/about/api
        - https://api.nasa.gov/
    """
    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):

        if input_data.location == "random":
            center_location = random.choice(list(locations.keys()))
        else:
            center_location = input_data.location.value

        url = f"https://epic.gsfc.nasa.gov/api/natural?api_key={secrets_data.NASA_API_KEY}"
        response_content = requests.get(url).content
        response_json = json.loads(response_content)
        closest_image_item = find_closest_locations(response_json, locations[center_location])

        identifier = closest_image_item['identifier']
        year = identifier[:4]
        month = identifier[4:6]
        day = identifier[6:8]

        image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{closest_image_item['image']}.png"
        image_content = requests.get(image_url).content
        encoded_string = base64.b64encode(image_content).decode()

        # Save the image locally
        image_file_path = f"{self.results_path}/nasa_earth_image_{center_location}.png"
        with open(image_file_path, "wb") as image_file:
            image_file.write(image_content)

        # Save image to results
        self.display_result = {
            "file_type": "png",
            "base64_content": encoded_string,
        }

        return OutputModel(
            image_url=image_url,
            image_base64_string=encoded_string,
            image_file_path=image_file_path,
        )
