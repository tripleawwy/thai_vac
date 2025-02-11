import dash
import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.dependencies import Input, Output
from pages import survey, mandatory, flights  # Importing the modular pages

# Initialize Dash app with multi-page support
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.CYBORG, "https://fonts.googleapis.com/css2?family=Raleway:wght@300;400;700&display=swap"], suppress_callback_exceptions=True)
server = app.server  # For deployment

# Register callbacks from survey module
survey.register_callbacks(app)

# Define Navbar with better styling
navbar = dbc.Navbar(
    dbc.Container([
        dbc.NavbarBrand("📊 Umfrage Dashboard", className="ms-3", style={"fontSize": "1.5rem", "fontFamily": "Raleway, sans-serif"}),
        dbc.Nav([
            dbc.NavItem(dbc.NavLink("Umfrage", href="/", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Packliste", href="/mandatory", className="nav-link")),
            dbc.NavItem(dbc.NavLink("Flüge", href="/flights", className="nav-link")),
        ], className="ms-auto"),
    ], fluid=True),
    color="dark", dark=True, className="mb-4 shadow-lg p-2"
)

# Define App Layout with Navigation
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])

# Callback for Page Navigation
@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/mandatory':
        return mandatory.layout
    elif pathname == '/flights':
        return flights.layout
    return survey.layout

# Run the app
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8050, debug=True)
