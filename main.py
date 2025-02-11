import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Load and process the survey data
CSV_FILE = "data/Thailand.csv"  # Update with actual path


def load_data():
    df = pd.read_csv(CSV_FILE)
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)  # Remove whitespace
    df = df.iloc[:, :-1]  # Remove the last column (individual answers question)
    return df


def extract_emoji(text):
    words = text.split()
    return words[-1] if words else text


def process_responses(column_name, df, split=True, is_timing_question=False):
    all_responses = []
    hover_texts = {}
    for response in df[column_name].dropna():
        responses = response.split(';') if split else [response]
        for full in responses:
            if is_timing_question:
                hover_texts[full.strip()] = full.strip()
                all_responses.append(full.strip())
            else:
                emoji = extract_emoji(full.strip())
                hover_texts[emoji] = full.strip()
                all_responses.append(emoji)
    response_counts = pd.Series(all_responses).value_counts()
    winner_text = response_counts.idxmax() if not response_counts.empty else None
    winner_full = hover_texts.get(winner_text, "Keine Antworten")
    return response_counts, hover_texts, winner_full


# Initialize Dash app with a theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG,
                                                "https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;700&display=swap"])
server = app.server  # For deployment with Flask

df = load_data()
options = ["Balkendiagramm", "Tortendiagramm"]

app.layout = dbc.Container([
    html.Div([
        dbc.Row([
            dbc.Col([
                html.Label("Diagrammtyp auswählen:", style={'color': 'white', 'font-family': 'Raleway, sans-serif'}),
                dcc.Dropdown(
                    id="chart-type",
                    options=[{"label": opt, "value": opt} for opt in options],
                    value="Balkendiagramm",
                    clearable=False,
                    style={'color': 'black', 'font-family': 'Raleway, sans-serif'}
                )
            ], width=4)
        ], className="mb-4"),
        html.Div(id="charts-container")
    ], className="container text-light", style={"font-family": "Raleway, sans-serif"})  # Ensures full dark mode styling
], fluid=True)


@app.callback(
    Output("charts-container", "children"),
    Input("chart-type", "value")
)
def update_charts(chart_type):
    charts = []
    for idx, column in enumerate(df.columns):
        is_timing_question = idx < 2  # Ensure first two questions are split but remain as full responses
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
                        style={"font-size": "1.2rem", "font-family": "Raleway, sans-serif"}),
                html.H4(winner_full, className="text-center text-warning",
                        style={"font-size": "1.5rem", "font-family": "Raleway, sans-serif"})
            ]),
            className="mb-4 shadow-lg text-dark bg-light"
        )

        charts.append(
            dbc.Card(
                dbc.CardBody([
                    html.H4(column, className="card-title", style={"font-family": "Raleway, sans-serif"}),
                    dcc.Graph(figure=fig),
                    winner_card
                ]),
                className="mb-4 shadow-lg"
            )
        )
    return charts


if __name__ == '__main__':
    app.run_server(debug=True)
