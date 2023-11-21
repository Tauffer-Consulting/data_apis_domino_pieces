from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import requests
import base64


accepted_extensions = ['jpg', 'jpeg', 'png', 'bmp', 'tiff', 'gif', 'svg']


class DogRandomPicturePiece(BasePiece):
    """
    This Piece uses the Dog API to get a random dog picture.
    - https://dog.ceo/dog-api/
    """
    def piece_function(self, input_data: InputModel):

        return_string = input_data.return_string
        return_file = input_data.return_file
        return_url = input_data.return_url

        endpoint = 'https://dog.ceo/api/breeds/image/random'
        try:
            # Get random picture url
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                dog_image_url = data['message']
                dog_image_extension = dog_image_url.split('.')[-1]
            else:
                raise Exception(f'Error: {response.status_code} - {response.text}')

            # Get picture from url
            response = requests.get(dog_image_url)
            if response.status_code == 200:
                dog_image_bytes = response.content
            else:
                raise Exception(f'Error: {response.status_code} - {response.text}')

            # Save picture to file
            image_file_path = ""
            if return_file:
                image_file_path = f"{self.results_path}/dog_image.{dog_image_extension}"
                with open(image_file_path, "wb") as f:
                    f.write(dog_image_bytes)

            # Convert picture to base64 string
            dog_image_base64_bytes = base64.b64encode(dog_image_bytes)
            dog_image_base64_string = dog_image_base64_bytes.decode('utf-8')

            # Save image to results
            if dog_image_extension in accepted_extensions:
                self.display_result = {
                    "file_type": dog_image_extension,
                    "base64_content": dog_image_base64_string,
                }

        except Exception as e:
            raise Exception(f'Error: {e}')

        return OutputModel(
            image_base64_string=dog_image_base64_string if return_string else "",
            image_file_path=image_file_path,
            image_url=dog_image_url if return_url else ""
        )



#         # Display to results
#         md_text = f"""## Dog Fact
# {dog_fact}\n
# """
#         with open(f"{self.results_path}/dog_fact.md", "w") as f:
#             f.write(md_text)
#         self.display_result = {
#             "file_type": "md",
#             "file_path": f"{self.results_path}/dog_fact.md",
#         }
