from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, available_weapon_dropdown, create_pie_chart, encoded_image, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag

find_top_10_layout = html.Div([
                                dcc.Store(id="top_10_results"),
                                html.Div([
                                    html.H2("Find the top 10 draw odd results by clicking the search buttons below"),
                                
                                html.Tr([html.Td(html.Div(create_choice_table()))], style={"width":"100%"}),
                                html.Tr([html.Td(html.Div(id='top10_result_info_table'))]),
                                # Pie chart for resident success rate
                                html.Div([
                                    html.H2("Top 10 Success Rates as pie charts"),
                                    html.Div(id='top10-pie-chart-container')  # This will hold the dynamically generated pie charts
                                ]),
                                ], style={"width":"100%"}),
                            ])


# Callbacks for finding the top 10 results of the draw
def find_top_10_callbacks(app):
    @app.callback(
        Output('top10_unit_numbers', component_property='options'),
        Input('proclamation_results', 'data')
    )
    def top10_unit_dropdown(proclamation_results):
        # print(Bag.get_unit_dropdown_from_bag('deer').append(Bag.get_unit_dropdown_from_bag('elk')))
        return Bag.get_unit_dropdown_from_bag(Bag, 'deer')
        # return Bag.get_unit_dropdown_from_bag('deer').append(Bag.get_unit_dropdown_from_bag('elk'))


    @app.callback(
        Output("top_10_results", "data"), 
        Input('top_10_results_deer', 'data'),
        Input('top_10_results_elk', 'data'),
        Input('top_10_results_unit', 'data'),
        Input('top_10_results_hunt_type', 'data'),
        allow_duplicate=True)
    def display_top_10_results(proclamation_results):
        return []
    
    @app.callback(
        Output("top_10_results_deer", "data"), 
        Input('proclamation_results', 'data'),
        Input(component_id='unit_number', component_property='value'),
        allow_duplicate=True)
    def find_top_10_deer(proclamation_results):
        return []
    
    @app.callback(
        Output("top_10_results_elk", "data"), 
        Input('proclamation_results', 'data'),
        Input(component_id='unit_number', component_property='value'),
        allow_duplicate=True)
    def find_top_10_elk(proclamation_results):
        return []
    
    @app.callback(
        Output("top_10_results_unit", "data"), 
        Input('proclamation_results', 'data'),
        Input(component_id='unit_number', component_property='value'),
        allow_duplicate=True)
    def find_top_10_unit(proclamation_results, unit):
        return []

    @app.callback(
        Output("top_10_results_hunt_type", "data"), 
        Input('proclamation_results', 'data'),
        Input(component_id='weapon_dropdown', component_property='value'),
        allow_duplicate=True)
    def find_top_10_hunt_type(proclamation_results, hunt_type):
        return []

