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

# making all of these classes default true becuse we want all the data
residency_choice = Residency(True, True, True)
choice_result = Choice(True, True, True, True, True)
success_total = SuccessTotals(True, True, True)
success_percentage = SuccessPercentages(True, True, True)
add_private = True
add_youth = True


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
    def find_top_10_deer(proclamation_results, unit_number):
        
        csv_filename = '2024OddsSummary_Deer.csv'
        odds_summary = parser_func("input/{}".format(csv_filename))
        query_result = query_odds(odds_summary, unit_number, residency_choice, choice_result, success_total, success_percentage, add_private, add_youth,)
        query_result_dict = {index: value for index, value in enumerate(query_result)}
        query_result_df = pd.DataFrame(query_result)
        proclamation_results_df = pd.DataFrame(proclamation_results)
        try:
            filtered_df = pd.merge(query_result_df, proclamation_results_df, on=['Hunt Code', 'Licenses', 'Bag'], how='inner')
            # Create a list to store pie chart components (dcc.Graph)
            pie_chart_components = []

            # Calculate the percentage values before generating pie charts
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
            filtered_df = get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')

            top10_resident_percent_success = filtered_df.nlargest(10, 'resident_percent_success')
            top10_resident_1stDraw_percent_success = filtered_df.nlargest(10, 'resident_1stDraw_percent_success')
            top10_resident_2ndDraw_percent_success = filtered_df.nlargest(10, 'resident_2ndDraw_percent_success')
            top10_resident_3rdDraw_percent_success = filtered_df.nlargest(10, 'resident_3rdDraw_percent_success')
            top10_resident_lists = [top10_resident_percent_success, top10_resident_1stDraw_percent_success, top10_resident_2ndDraw_percent_success, top10_resident_3rdDraw_percent_success]
            for top10_df in top10_resident_lists:
                # Loop through each unique Hunt Code to generate pie charts for each row
                for hunt_code in top10_df['Hunt Code'].unique():
                    # Filter rows with the current Hunt Code
                    top10_resident_df = top10_df[top10_df['Hunt Code'] == hunt_code]

                    # Create a row for the pie charts for each of the percentage columns
                    pie_charts_for_this_hunt_code = []
                    
                    for _, row in top10_resident_df.iterrows():
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_percent_success', 'Overall Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_1stDraw_percent_success', '1st Draw Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_2ndDraw_percent_success', '2nd Draw Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_3rdDraw_percent_success', '3rd Draw Success')))
                    
                    # Add pie charts for the current hunt code to the list
                    pie_chart_components.append(html.Div(
                        children=pie_charts_for_this_hunt_code,
                        style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
                    ))

        except KeyError:
            return []
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

