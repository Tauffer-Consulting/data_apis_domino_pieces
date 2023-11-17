from domino.testing import piece_dry_run


def test_dogfacts():
    input_data = dict()
    piece_output = piece_dry_run(
        piece_name="DogFactsPiece",
        input_data=input_data,
    )
    assert isinstance(piece_output["dog_fact"], str)
    assert len(piece_output["dog_fact"]) > 0
