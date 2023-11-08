from domino.testing import piece_dry_run
from datetime import date, timedelta
import os


def test_newsapi_articles():
    to_date = date.today().isoformat()
    from_date = (date.today() - timedelta(days=10)).isoformat()
    input_data = dict(
        query="economy",
        from_date=from_date,
        to_date=to_date,
        sort_by="relevancy",
        language="en",
        number_of_results=10
    )
    piece_output = piece_dry_run(
        piece_name="NewsApiArticlesPiece",
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
        assert 'publishedAt' in article
        assert 'url' in article
        assert 'content' in article
