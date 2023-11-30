from domino.testing import piece_dry_run
from domino.testing.utils import skip_envs
from pathlib import Path
import os


@skip_envs("github")
def test_alphavantage():

    ALPHA_VANTAGE_API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", None)
    if not ALPHA_VANTAGE_API_KEY:
        raise Exception("ALPHA_VANTAGE_API_KEY environment variable is required.")
    input_data = dict(
        symbol="AAPL",
        output_size="compact",
        max_data_points=-1
    )
    piece_output = piece_dry_run(
        piece_name="AlphaVantageDailyPiece",
        input_data=input_data,
        secrets_data=dict(
            ALPHA_VANTAGE_API_KEY=ALPHA_VANTAGE_API_KEY
        ),
    )
    assert Path(piece_output["data_file_path"]).exists()
