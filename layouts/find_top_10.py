from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, hunt_code_dropdown, create_pie_chart, encoded_image, create_filtering_table
from data_handlers import scrape_for_deer, scrape_for_elk
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag

find_top_10_layout = html.Div([
                                dcc.Store(id="top_10_results"),
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
                                dcc.Link('Go to Page filtering_table', href='/filtering_table')  # Link to Page 2
                            ])

# Callbacks for finding the top 10 results of the draw
def find_top_10_callbacks(app):
    @app.callback(
        Output("top_10_results", "data"), 
        Input('query_results', 'data'),
        allow_duplicate=True)
    def generate_hunt_dropdown(query_values):

        if query_values != None and query_values !=  {"": ""}:
            # Convert the data to a DataFrame
            df = pd.DataFrame.from_dict(query_values, orient='index')

            #create the hunt_code_dropdown list of available selections
            return [{'label': row['Hunt Code'], 'value': row['Hunt Code']} for _, row in df.iterrows()]
        else:
            return []
