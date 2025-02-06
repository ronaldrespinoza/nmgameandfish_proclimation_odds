import dash
from dash import dcc, html, Input, Output
from layouts.filtering_table import filtering_table_callbacks, filtering_table_layout
from layouts.find_top_10 import find_top_10_callbacks, find_top_10_layout

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout of the app
app.layout = [
    dcc.Location(id='url', refresh=False),  # Used for URL routing
    html.Div(id='page-content')  # The content of the page changes here
]

# Register the callbacks for each page to the app instance
filtering_table_callbacks(app)
find_top_10_callbacks(app)

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
        return html.Div([
            html.H3('404 Page Not Found')
        ])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)