import dash
from dash import dcc, html
import pandas as pd
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
from layouts.home import home_layout
from layouts.common_callbacks import common_callbacks
from layouts.filtering_table import filtering_table_callbacks, filtering_table_layout
from layouts.find_top_10 import find_top_10_callbacks, find_top_10_layout
from data_handlers import scrape_for_deer, scrape_for_elk

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP], suppress_callback_exceptions=True,)

# Define the layout of the app
app.layout = [
    # Navbar (using Dash Bootstrap Components)
    dbc.NavbarSimple(
        children=[
            dbc.NavItem(dbc.NavLink("Home", href="/Home")),
            dbc.NavItem(dbc.NavLink("filtering table", href="/filtering_table")),
            dbc.NavItem(dbc.NavLink("top 10", href="/find_top_10")),
            dbc.NavItem(dbc.NavLink("About", href="/about"))
        ],
        brand="NM Game and Fish Draw Odds and Potential Trip Success",
        brand_href="/",
        color="dark",
        dark=True
    ),
    dcc.Interval(
        id='interval-component', 
        interval=5 * 1000,  # in milliseconds (1ms means it runs right after load)
        n_intervals=0,  # Runs once when the page loads
        disabled=False  # Makes sure the interval is active right after page load
    ),
    dcc.Store(id="proclamation_results", storage_type='local', data={}),
    dcc.Location(id='url', refresh=True, pathname='/Home'),  # Used for URL routing
    html.Div(id='page-content')  # The content of the page changes here
    
]

# Callback that runs on application execution
@app.callback(
    Output("proclamation_results", "data"),
    Input('interval-component', 'n_intervals'),
    State('proclamation_results', 'data')  # Check if data is already in the store
)
def on_page_load(n, existing_data):
    # Debugging log
    # print(f"on_page_load triggered, n_intervals: {n}, existing_data: {existing_data}")

    if n == 1:  # The first interval (immediately after the page loads)
        if not existing_data:  # If no data is present in store
            deer_proclamation_df = scrape_for_deer()
            elk_proclamation_df = scrape_for_elk()
            return pd.concat([deer_proclamation_df, elk_proclamation_df], ignore_index=True, sort=False).to_dict("dict")
        return existing_data
    return existing_data  # Return existing data if n_intervals isn't 1


# Callback to disable the interval after it runs once
@app.callback(
    Output('interval-component', 'disabled'),
    Input('interval-component', 'n_intervals')
)
def disable_interval(n_intervals):
    if n_intervals > 0:
        return True  # Disable the interval after it runs once
    return False  # Keep it enabled initially


# Page layout for routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    common_callbacks(app)
    if pathname == '/filtering_table':
        # Register the callbacks for each page to the app instance
        return filtering_table_layout  # Return the filtering table layout
    elif pathname == '/find_top_10':
        return find_top_10_layout  # Return the "find top 10" layout
    elif pathname == "/Home":
        return home_layout
    else:
        return html.Div([
                            html.H1("404 Page Not Found", style={'color': 'red'}),
                            html.P("Sorry, the page you are looking for does not exist.")
                        ])

filtering_table_callbacks(app)
find_top_10_callbacks(app)

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
