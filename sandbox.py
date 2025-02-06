import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

# Initialize the Dash app with a Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout with a navigation bar and page content area
app.layout = html.Div([
    # Navbar (using Dash Bootstrap Components)
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/")),
            dbc.NavItem(dbc.NavLink("Page 1", href="/page-1")),
            dbc.NavItem(dbc.NavLink("Page 2", href="/page-2")),
            dbc.NavItem(dbc.NavLink("About", href="/about"))
        ],
        brand="My Dash App",
        brand_href="/",
        color="dark",
        dark=True
    ),
    # Location component to track the URL
    dcc.Location(id='url', refresh=False),
    # Content will be dynamically updated based on the URL
    html.Div(id='page-content')
])

# Define the page content for different URLs
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/page-1':
        return html.Div([html.H3('Welcome to Page 1')])
    elif pathname == '/page-2':
        return html.Div([html.H3('Welcome to Page 2')])
    elif pathname == '/about':
        return html.Div([html.H3('About This App')])
    else:
        return html.Div([html.H3('Welcome to the Home Page')])

if __name__ == '__main__':
    app.run_server(debug=True)
