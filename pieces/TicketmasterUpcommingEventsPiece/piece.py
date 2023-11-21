from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
from datetime import date, timedelta
import requests


class TicketmasterUpcommingEventsPiece(BasePiece):
    """
    This Piece uses the Ticketmaster API to get upcomming events based on a search options.
     -https://developer.ticketmaster.com/products-and-docs/apis/discovery-api/v2/
    """
    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):

        api_key = secrets_data.TICKETMASTER_API_KEY
        if not api_key:
            raise Exception("Ticketmaster API key is required.")

        endpoint = 'https://app.ticketmaster.com/discovery/v2/events.json'

        today = date.today().isoformat() + 'T00:00:00Z'
        params = {
            'apikey': api_key,
            'size': input_data.max_number_of_events,
            'startDateTime': today,
        }
        keyword = input_data.keyword
        if keyword:
            params['keyword'] = keyword
        end_date = input_data.end_date
        if end_date and end_date > date.today():
            params['endDateTime'] = end_date.isoformat() + 'T23:59:59Z'
        else:
            enddate = (date.today() + timedelta(days=7)).isoformat() + 'T23:59:59Z'
            self.logger.info(f"Invalid end date. Using default of 7 days from now: {enddate}.")
            params['endDateTime'] = enddate
        city = input_data.city
        if city:
            params['city'] = city
        country_code = input_data.country_code
        if country_code:
            params['countryCode'] = country_code

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                events = response.json().get('_embedded', {}).get('events', [])
                all_events = []
                if len(events) > 0:
                    for e in events:
                        event_object = dict(
                            name=e.get('name'),
                            event_date=e.get('dates', {}).get('start', {}).get('localDate'),
                            event_location=e.get('_embedded', {}).get('venues', [{}])[0].get('city', {}).get('name'),
                            classification=e.get('classifications', [{}])[0].get('segment', {}).get('name'),
                            url=e.get('url'),
                            image_url=e.get('images', [{}])[0].get('url')
                        )
                        all_events.append(event_object)
            else:
                raise Exception(f'Error: {response.status_code} - {response.text}')
        except Exception as e:
            raise Exception(f'Error: {e}')

        # Text with formatted results
        formatted_results = ''
        for e in all_events:
            formatted_results += f"{e['name']}\n"
            formatted_results += f"{e['event_date']} - {e['event_location']} - {e['classification']}\n"
            formatted_results += f"{e['url']}\n\n"

        formatted_file_path = f"{self.results_path}/results_formatted.txt"
        with open(formatted_file_path, "w") as file:
            file.write(formatted_results)

        # Display results
        self.format_display_result(input_data, all_events)

        return OutputModel(
            events=all_events,
            results_formatted=formatted_results
        )

    def format_display_result(self, input_data: InputModel, events: list):
        md_text = "## Upcomming Events:\n\n"
        for e in events:
            md_text += f"**{e['name']}**\n"
            md_text += f"{e['event_date']} - {e['event_location']} - {e['classification']}\n"
            md_text += f"{e['url']}\n\n"
            md_text += f"![{e['name']}]({e['image_url']})\n\n"
        file_path = f"{self.results_path}/display_result.md"
        with open(file_path, "w") as f:
            f.write(md_text)
        self.display_result = {
            "file_type": "md",
            "file_path": file_path
        }
