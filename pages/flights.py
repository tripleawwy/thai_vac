from dash import html, dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    html.H2("Flugbuchungen & Pläne", style={"font-family": "Raleway, sans-serif"}),
    html.P("Hier kannst du geplante Flüge eintragen:"),
    dbc.Input(id="flight-input", type="text", placeholder="Flugnummer eingeben..."),
    html.Button("Hinzufügen", id="add-flight", n_clicks=0, className="btn btn-primary mt-2"),
    html.Ul(id="flight-list", style={"font-size": "1.2rem"})
])