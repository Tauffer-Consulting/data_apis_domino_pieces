from domino.base_piece import BasePiece
from .models import InputModel, OutputModel, SecretsModel
import pandas as pd
import requests
import json
import plotly
import plotly.graph_objects as go


def make_plotly_fig(df: pd.DataFrame, symbol: str):
    fig = go.Figure()
    trace_candlestick = go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'],
        name='Candlestick'
    )
    fig.add_trace(trace_candlestick)
    fig.update_layout(
        xaxis=dict(
            rangeslider=dict(visible=True),
            showgrid=True,  # Show gridlines for the x-axis
            gridcolor='lightgray'  # Set the grid color to gray
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor='lightgray',
            fixedrange=False
        ),
        title=f'{symbol} Daily Stock Data',
        xaxis_title='Date',
        yaxis_title='Price',
        height=600,
        width=800,
        plot_bgcolor='white',
    )
    return fig


class AlphaVantageDailyPiece(BasePiece):
    """
    This Piece uses the AlphaVantage API to get daily stock data.
    - https://www.alphavantage.co/
    """
    def piece_function(self, input_data: InputModel, secrets_data: SecretsModel):

        api_key = secrets_data.ALPHA_VANTAGE_API_KEY
        if not api_key:
            raise Exception("Alpha Vantage API key is required.")

        symbol = input_data.symbol
        output_size = input_data.output_size.value
        number_of_points = input_data.max_data_points

        endpoint = 'https://www.alphavantage.co/query'
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': output_size,
            'apikey': api_key
        }

        data_file_path = f"{self.results_path}/results_daily_data.csv"

        try:
            response = requests.get(endpoint, params=params)
            if response.status_code == 200:
                data = response.json()
                daily_data = data['Time Series (Daily)']
                df = pd.DataFrame(daily_data).T
                if number_of_points > 0 and number_of_points < len(df):
                    df = df[:number_of_points]
                df.columns = ['Open', 'High', 'Low', 'Close', 'Volume']
                df.index = pd.to_datetime(df.index)
                df.reset_index(inplace=True)
                df.rename(columns={'index': 'Date'}, inplace=True)
                df.to_csv(data_file_path, index=False)
            else:
                raise Exception(f'Error: {response.status_code} - {response.text}')
        except Exception as e:
            raise Exception(f'Error: {e}')

        # Save image to results
        fig = make_plotly_fig(df, symbol)
        fig_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
        with open(f"{self.results_path}/results_plotly.json", "w") as f:
            f.write(fig_json)
        self.display_result = {
            "file_type": "plotly_json",
            "file_path": f"{self.results_path}/results_plotly.json",
        }

        return OutputModel(
            data_file_path=data_file_path
        )
