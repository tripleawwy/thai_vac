from dash import html

layout = html.Div([
    html.H2("Packliste & Notwendigkeiten", style={"font-family": "Raleway, sans-serif"}),
    html.Ul([
        html.Li("📄 Reisepass & Visa"),
        html.Li("💳 Kreditkarte & Bargeld"),
        html.Li("💊 Medikamente & Impfungen"),
        html.Li("🧴 Sonnenschutz & Insektenschutzmittel"),
        html.Li("📱 Handy, Ladegerät & Adapter"),
    ], style={"font-size": "1.2rem"})
])