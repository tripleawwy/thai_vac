import dash
from dash import dcc, html
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from utils import process_responses, load_data

df = load_data()
options = ["Balkendiagramm", "Tortendiagramm"]

layout = html.Div([
    html.Div([
        html.Label("Diagrammtyp auswählen:", style={'color': 'white', 'fontFamily': 'Raleway, sans-serif'}),
        dcc.Dropdown(
            id="chart-type",
            options=[{"label": opt, "value": opt} for opt in options],
            value="Balkendiagramm",
            clearable=False,
            style={'color': 'black', 'fontFamily': 'Raleway, sans-serif'}
        ),
        html.Div(id="charts-container")
    ], className="container text-light")
])


# Callback for generating survey charts
def register_callbacks(app):
    @app.callback(
        Output("charts-container", "children"),
        [Input("chart-type", "value")]
    )
    def update_charts(chart_type):
        df = load_data()  # Ensure data is loaded fresh each time
        charts = []
        for idx, column in enumerate(df.columns):
            is_timing_question = idx < 2  # First two questions should remain full text
            response_counts, hover_texts, winner_full = process_responses(column, df, split=True,
                                                                          is_timing_question=is_timing_question)
            hover_data = {"x": list(response_counts.index),
                          "customdata": [hover_texts.get(k, k) for k in response_counts.index]}

            if chart_type == "Balkendiagramm":
                fig = px.bar(response_counts, x=response_counts.index, y=response_counts.values, template='plotly_dark',
                             hover_data=hover_data)
                fig.update_layout(xaxis_title="", title="")
            else:
                fig = px.pie(response_counts, names=response_counts.index, values=response_counts.values,
                             template='plotly_dark', hover_data=hover_data)
                fig.update_layout(title="")

            winner_card = dbc.Card(
                dbc.CardBody([
                    html.H5("Beliebteste Antwort", className="card-title text-center",
                            style={"fontSize": "1.2rem", "fontFamily": "Raleway, sans-serif"}),
                    html.H4(winner_full, className="text-center text-warning",
                            style={"fontSize": "1.5rem", "fontFamily": "Raleway, sans-serif"})
                ]),
                className="mb-4 shadow-lg text-dark bg-light"
            )

            charts.append(
                dbc.Card(
                    dbc.CardBody([
                        html.H4(column, className="card-title", style={"fontFamily": "Raleway, sans-serif"}),
                        dcc.Graph(figure=fig),
                        winner_card
                    ]),
                    className="mb-4 shadow-lg"
                )
            )
        return charts
