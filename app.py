import dash
from dash import dcc, html, Input, Output, State
from layouts.common_callbacks import common_callbacks
from layouts.filtering_table import filtering_table_callbacks, filtering_table_layout
from layouts.find_top_10 import find_top_10_callbacks, find_top_10_layout
from data_handlers import scrape_for_deer, scrape_for_elk

# Initialize the Dash app
app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Define the layout of the app
app.layout = [
    dcc.Interval(
        id='interval-component', 
        interval=5 * 1000,  # in milliseconds (1ms means it runs right after load)
        n_intervals=0,  # Runs once when the page loads
        disabled=False  # Makes sure the interval is active right after page load
    ),
    dcc.Store(id="proclamation_results", storage_type='local', data={}),
    dcc.Store(id="query_results"),
    dcc.Location(id='url', refresh=False),  # Used for URL routing
    html.Div(id='page-content')  # The content of the page changes here
    
]

# Register the callbacks for each page to the app instance
common_callbacks(app)
filtering_table_callbacks(app)
find_top_10_callbacks(app)

# Callback that runs on application execution
@app.callback(
    Output("proclamation_results_filtering_table", "data"),
    Input('interval-component', 'n_intervals'),
    State('proclamation_results', 'data')  # Check if data is already in the store
)
def on_page_load(n, existing_data):

    if n == 1:  # The first interval (immediately after the page loads)
        if not existing_data:  # If no data is present in store
            deer_proclamation_df = scrape_for_deer()
            elk_proclamation_df = scrape_for_elk()
            return deer_proclamation_df.append(elk_proclamation_df, ignore_index=False, sort=False).to_dict("dict")
        return existing_data
    return existing_data  # Return existing data if n_intervals isn't 1


# Page layout for routing
@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/filtering_table':
        return filtering_table_layout  # Return the filtering table layout
    elif pathname == '/find_top_10':
        return find_top_10_layout  # Return the "find top 10" layout
    else:
        return filtering_table_layout  # Return the filtering table layout
        # return html.Div([
        #     html.H3('404 Page Not Found')
        # ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)