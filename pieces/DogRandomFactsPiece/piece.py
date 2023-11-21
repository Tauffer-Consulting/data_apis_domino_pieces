from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import requests


class DogRandomFactsPiece(BasePiece):
    """
    This Piece uses the Dog API to get a random dog fact.
    - https://dog-api.kinduff.com/api/facts
    """
    def piece_function(self, input_data: InputModel):

        endpoint = 'https://dog-api.kinduff.com/api/facts'
        try:
            response = requests.get(endpoint)
            if response.status_code == 200:
                data = response.json()
                dog_fact = data['facts'][0]
            else:
                raise Exception(f'Error: {response.status_code} - {response.text}')
        except Exception as e:
            raise Exception(f'Error: {e}')

        # Display to results
        md_text = f"""## Dog Fact
{dog_fact}\n
"""
        with open(f"{self.results_path}/dog_fact.md", "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": f"{self.results_path}/dog_fact.md",
        }

        return OutputModel(
            dog_fact=dog_fact
        )
