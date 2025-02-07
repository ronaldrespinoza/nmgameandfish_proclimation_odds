from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, available_weapon_dropdown, create_pie_chart, encoded_image, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag

home_layout = html.Div([
                        html.Div([
                            html.H2("Find your draw odd results by clicking the map unit or using the applications from the navigation bar"),
                        ]),
                        html.Td([html.Td([html.Img(src=encoded_image, style={'width': '100%'})])]),
                    ])