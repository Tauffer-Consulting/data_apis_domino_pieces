from domino.testing import piece_dry_run


def test_nasaearthimage_natural():
    input_data = dict(location="random")
    piece_output = piece_dry_run(
        piece_name="NasaEarthImagePiece",
        input_data=input_data,
        secrets_data=dict(
            NASA_API_KEY="DEMO_KEY"
        ),
    )

    assert "epic.gsfc.nasa.gov" in piece_output["image_url"]
