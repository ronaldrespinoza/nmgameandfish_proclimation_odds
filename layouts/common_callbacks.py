from dash import Input, Output, callback
from data_handlers.query_odds import parser_func, query_odds
from models import Residency, SuccessPercentages, SuccessTotals, Choice, Bag
import pandas as pd

# original callbacks to show draw result odds
def common_callbacks(app):

    @app.callback(
        Output("hunt_dropdown", "options"), 
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

    @app.callback(
        [Output('bag_choice', component_property='options'),
        Output('unit_number', component_property='options'),
        Output('deer_button', component_property='n_clicks'),
        Output('elk_button',  component_property='n_clicks'),
        Output(component_id='animal_choice_deer', component_property='on'),
        Output(component_id='animal_choice_elk', component_property='on')],
        [Input(component_id='animal_choice_deer', component_property='on'),
        Input(component_id='deer_button', component_property='n_clicks'),
        Input(component_id='animal_choice_elk', component_property='on'),
        Input(component_id='elk_button', component_property='n_clicks')]
    )
    def ensure_only_one_on(animal_choice_deer, n_clicks_deer, animal_choice_elk, n_clicks_elk):
        if animal_choice_deer and not(n_clicks_deer) and n_clicks_elk:
            return Bag.get_deer_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
        elif animal_choice_elk and not(n_clicks_elk) and n_clicks_deer:
            return Bag.get_elk_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1,False, True
        elif animal_choice_deer and not(n_clicks_deer) and not(n_clicks_elk):
            return Bag.get_deer_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'deer'), 1,0, True, False
        elif animal_choice_elk and not(n_clicks_elk) and not(n_clicks_deer):
            return Bag.get_elk_bag_drop_down(Bag), Bag.get_unit_dropdown_from_bag(Bag, 'elk'), 0,1, False, True
        else:
            return {},{},0,0,False,False
        

    @callback(
        Output('output', 'children'),
        Output("query_results", "data"),
        Input(component_id='animal_choice_deer', component_property='on'),
        Input(component_id='animal_choice_elk', component_property='on'),
        Input(component_id='add_private', component_property='on'),
        Input(component_id='add_youth', component_property='on'),
        Input(component_id='show_results_for_resident', component_property='on'),
        Input(component_id='show_results_for_nonresident', component_property='on'),
        Input(component_id='show_results_for_outfitter', component_property='on'),
        Input(component_id='show_results_for_1stchoice', component_property='on'),
        Input(component_id='show_results_for_2ndchoice', component_property='on'),
        Input(component_id='show_results_for_3rdchoice', component_property='on'),
        Input(component_id='show_results_for_4thchoice', component_property='on'),
        Input(component_id='show_results_for_totals', component_property='on'),
        Input(component_id='show_resident_successfull_draw_total', component_property='on'),
        Input(component_id='show_nonresident_successfull_draw_total', component_property='on'),
        Input(component_id='show_outfitter_successfull_draw_total', component_property='on'),
        Input(component_id='show_resident_successfull_draw_percentage', component_property='on'),
        Input(component_id='show_nonresident_successfull_draw_percentage', component_property='on'),
        Input(component_id='show_outfitter_successfull_draw_percentage', component_property='on'),
        Input(component_id='unit_number', component_property='value'),
        Input(component_id='bag_choice', component_property='value'),
    )
    def update_output_div(animal_choice_deer, animal_choice_elk,
                        add_private, add_youth,
                        show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter,
                        show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals,
                        show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total,
                        show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage,
                        unit_number, bag_choice):
        csv_filename = ""
        odds_summary = []
        query_result = None

        residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
        choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
        success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
        success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)

        if animal_choice_deer:
            csv_filename = '2024OddsSummary_Deer.csv'
        elif animal_choice_elk:
            csv_filename = '2024OddsSummary_Elk.csv'
        elif csv_filename == "":
            return "", {"": ""}

        odds_summary = parser_func("input/{}".format(csv_filename))
        if unit_number is None:
            return "you must choose a unit number", {"": ""}
        else:
            try:
                query_result = query_odds(odds_summary, unit_number, bag_choice, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth,)
            except TypeError as error:
                return "", {"": ""}

        return "", {index: value for index, value in enumerate(query_result)}


