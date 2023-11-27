from domino.testing import piece_dry_run


def test_dogpicture():
    input_data = dict(
        return_string=True,
        return_file=True,
        return_url=True,
    )
    piece_output = piece_dry_run(
        piece_name="DogRandomPicturePiece",
        input_data=input_data,
    )
    assert len(piece_output["image_base64_string"]) > 0
    assert len(piece_output["image_file_path"]) > 0
    assert len(piece_output["image_url"]) > 0
