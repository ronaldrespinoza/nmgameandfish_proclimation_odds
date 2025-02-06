from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, hunt_code_dropdown, create_pie_chart, encoded_image, create_filtering_table
from data_handlers import scrape_for_deer, scrape_for_elk
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag

find_top_10_layout = html.Div([
                                    dcc.Interval(
                                        id='interval-component', 
                                        interval=5 * 1000,  # in milliseconds (1ms means it runs right after load)
                                        n_intervals=0,  # Runs once when the page loads
                                        disabled=False  # Makes sure the interval is active right after page load
                                    ),
                                    dcc.Store(id="proclamation_results", storage_type='local', data={}),
                                    dcc.Store(id="query_results"),
                                    html.Tr([html.Td(html.Br())]),
                                    html.Tr([html.Td(html.Div(create_filtering_table()))]),
                                    html.Tr([html.Td(unit_dropdown())]),
                                    html.Tr([html.Td(bag_dropdown())]),
                                    html.Tr([html.Td(hunt_code_dropdown())]),
                                    html.Tr([html.Td(html.Br())]),
                                    html.Tr([html.Td(html.Div(id='result_info_table'))]),
                                    # Pie chart for resident success rate
                                    html.Div([
                                        html.H2("Resident Success Rates by Hunt Code"),
                                        html.Div(id='pie-chart-container')  # This will hold the dynamically generated pie charts
                                    ]),
                                        html.Td([html.Td("GMU Map"),
                                                    html.Td([html.Img(src=encoded_image, style={'width': '100%'})])
                                            ]),
                                    html.Div(id='output'),
                                    dcc.Link('Go to Page 2', href='/page-2')  # Link to Page 2
                                ])

# Callback for Page 2 to render the Pie chart
def find_top_10_callbacks(app):
    # Callback that runs once after the page loads
    @app.callback(
        Output("proclamation_results", "data"),
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
