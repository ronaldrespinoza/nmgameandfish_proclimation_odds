from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, available_weapon_dropdown, create_pie_chart, encoded_image, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag

find_top_10_layout = html.Div([
                                dcc.Store(id="top_10_results"),
                                html.Div([
                                    html.H2("Find the top 10 draw odd results by clicking the search buttons below"),
                                ]),
                                html.Tr([html.Td(html.Br())]),
                                html.Tr([html.Td(html.Div(create_choice_table()))]),
                                html.Tr([html.Td(html.Div(id='top10_result_info_table'))]),
                                # Pie chart for resident success rate
                                html.Div([
                                    html.H2("Top 10 Success Rates as pie charts"),
                                    html.Div(id='top10-pie-chart-container')  # This will hold the dynamically generated pie charts
                                ]),
                            ])


# Callbacks for finding the top 10 results of the draw
def find_top_10_callbacks(app):
    @app.callback(
        Output("top_10_results", "data"), 
        Input('proclamation_results', 'data'),
        allow_duplicate=True)
    def find_top_10(proclamation_results):
        return []

