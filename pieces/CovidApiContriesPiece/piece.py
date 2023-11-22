from domino.base_piece import BasePiece
from .models import InputModel, OutputModel
import requests
import plotly.express as px
from pathlib import Path


class CovidApiContriesPiece(BasePiece):
    """
    Piece to fetch COVID-19 data from https://disease.sh/ and display it on a world map.
    """

    def get_covid_data(self, countries: str = None):
        if countries is None:
            countries = ""
        url = f"https://disease.sh/v3/covid-19/countries/{countries}"
        response = requests.get(url)
        if response.status_code != 200:
            self.logger.info(response.json())
            raise Exception("Failed to fetch COVID-19 data.")
        return response.json()
    

    def piece_function(self, input_data: InputModel):
        countries = None
        if input_data.countries and "all" not in input_data.countries:
            countries = ','.join(input_data.countries).strip(',')

        covid_data = self.get_covid_data(countries=countries)
        if isinstance(covid_data, dict):
            covid_data = [covid_data]

        data = {
            'Country': [], 
            'Cases per One Million': []
        }
        for country_data in covid_data:
            country = country_data.get('country')
            cases_per_million = country_data.get('casesPerOneMillion', 0)

            # Use casesPerOneMillion as the risk score directly
            data['Country'].append(country)
            data['Cases per One Million'].append(cases_per_million)

        fig = px.choropleth(
            data, 
            locations='Country', 
            locationmode='country names',
            color='Cases per One Million', 
            range_color=(0, max(data['Cases per One Million'])),
            color_continuous_scale='viridis',
            title='COVID-19 Cases per One Million by Country'
        )
        fig.update_layout(geo=dict(showframe=False, showcoastlines=False, projection_type='equirectangular'))

        json_path = str(Path(self.results_path) / 'covid_cases_per_million.json')
    
        fig.write_json(json_path)
        self.display_results = {
            'file_type': 'plotly_json',
            'file_path': fig.to_json()
        }
        return OutputModel(data=data)