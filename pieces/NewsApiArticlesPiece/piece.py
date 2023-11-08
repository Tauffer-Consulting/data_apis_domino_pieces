from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from newsapi import NewsApiClient
import requests
from bs4 import BeautifulSoup
import re
from html import unescape


def clean_text(text):
    # Replace HTML entities with their corresponding characters, e.g., '&amp;' becomes '&'
    text = unescape(text)
    # Remove HTML tags
    text = re.sub(r'<[^>]+>', '', text)
    # Replace sequences of whitespace characters with a single space
    text = re.sub(r'\s+', ' ', text)
    # Remove leading and trailing whitespace
    text = text.strip()
    # Remove other unwanted characters
    text = text.replace(u'\xa0', ' ').replace('\r', '').replace('\n', '').replace('\t', '')
    return text


def extract_article_content(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        # Use a tag that is common for main content, like 'article' or 'main'
        main_content = soup.find('article') or soup.find('main')
        if main_content:
            paragraphs = main_content.find_all('p')
            return clean_text('\n'.join(paragraph.text for paragraph in paragraphs))
    return ""


class NewsApiArticlesPiece(BasePiece):
    """
    This Piece uses the News API to retrieve full articles.
    References:
        - https://newsapi.org/
        - https://newsapi.org/docs/endpoints/everything
    """
    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):

        self.logger.info("Starting NEWS API client...")
        api_key = secrets_data.NEWSAPI_API_KEY
        newsapi_client = NewsApiClient(api_key=api_key)

        # Input arguments
        query = input_data.query
        from_date = input_data.from_date
        to_date = input_data.to_date
        sort_by = input_data.sort_by
        language = input_data.language
        number_of_results = input_data.number_of_results

        # Execute query
        all_articles = newsapi_client.get_everything(
            q=query,
            from_param=from_date,
            to=to_date,
            language=language,
            sort_by=sort_by,
            page_size=number_of_results
        )

        # Extract article content from URLs
        articles = list()
        for article in all_articles["articles"]:
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
            a["content"] = extract_article_content(article.get("url", ""))
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
            md_text += f"{article['content']}\n"
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
