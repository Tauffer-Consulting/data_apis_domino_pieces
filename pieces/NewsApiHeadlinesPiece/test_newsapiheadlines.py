from domino.testing import piece_dry_run
import os


def test_newsapi_headlines():
    input_data = dict(
        query="dollar",
        category="business",
        country="all",
        language="en",
        number_of_results=10
    )
    piece_output = piece_dry_run(
        piece_name="NewsApiHeadlinesPiece",
        input_data=input_data,
        secrets_data=dict(
            NEWSAPI_API_KEY=os.environ["NEWSAPI_API_KEY"]
        ),
    )

    assert 'message' in piece_output
    assert 'articles' in piece_output
    assert len(piece_output["articles"]) <= 10
    for article in piece_output["articles"]:
        assert 'title' in article
        assert 'author' in article
        assert 'source' in article
