from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from newsapi import NewsApiClient


class NewsApiHeadlinesPiece(BasePiece):
    """
    This Piece uses the News API to retrieve the top headlines from a given source or country.
    References:
        - https://newsapi.org/
        - https://newsapi.org/docs/endpoints/top-headlines
    """
    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):

        self.logger.info("Starting NEWS API client...")
        api_key = secrets_data.NEWSAPI_API_KEY
        newsapi_client = NewsApiClient(api_key=api_key)

        # Input arguments
        query = input_data.query
        category = input_data.category
        country = input_data.country
        if country == "all":
            country = None
        language = input_data.language
        number_of_results = input_data.number_of_results

        top_headlines = newsapi_client.get_top_headlines(
            q=query,
            category=category,
            language=language,
            country=country,
            page_size=number_of_results
        )

        articles = list()
        for article in top_headlines["articles"]:
            a = dict()
            a["source"] = str(article.get("source", {}).get("name"))
            a["title"] = str(article.get("title", ""))
            author = article.get("author", None)
            if isinstance(author, list):
                a["author"] = ", ".join(author)
            elif author is None:
                a["author"] = ""
            else:
                a["author"] = str(author)
            a["description"] = str(article.get("description", ""))
            a["publishedAt"] = str(article.get("publishedAt", ""))
            a["url"] = str(article.get("url", ""))
            a["url_to_image"] = str(article.get("urlToImage", ""))
            articles.append(a)

        self.logger.info(f"Query: {query}")
        self.logger.info(f"Number of results: {len(articles)}")
        message = f"Query: {query}\n"
        message += f"Number of results: {len(articles)}"

        # Display result in the Domino GUI
        self.format_display_result(input_data, articles=articles)

        return OutputModel(
            message=message,
            articles=articles
        )

    def format_display_result(self, input_data: InputModel, articles: list):
        md_text = "## Query:\n"
        md_text += f"{input_data.query}\n"
        for article in articles:
            md_text += f"\n### {article['title']}:\n"
            if article.get("url_to_image", None):
                md_text += f"![{article['title']}]({article['url_to_image']})\n\n"
            md_text += f"{article['author']}\n\n"
            md_text += f"{article['publishedAt']}\n\n"
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
