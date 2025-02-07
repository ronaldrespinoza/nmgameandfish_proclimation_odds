from dash import dcc, html, Input, Output, State, callback, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, available_weapon_dropdown, create_pie_chart, create_pie_chart_with_raw_value, encoded_image, create_choice_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart, parser_func, query_odds
from models import Residency, SuccessPercentages, PercentSuccess, SuccessTotals, Choice, Bag

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


    # @app.callback(
    #     Output("top_10_results", "data"), 
    #     Input('top_10_results_deer', 'data'),
    #     Input('top_10_results_elk', 'data'),
    #     Input('top_10_results_unit', 'data'),
    #     Input('top_10_results_hunt_type', 'data'),
    #     allow_duplicate=True)
    # def display_top_10_results(proclamation_results):
    #     return []
    
    @app.callback(
        [Output('top10-pie-chart-container', 'children'),
        Output('top10_result_info_table', 'children'),],
        [Input('proclamation_results', 'data'),
        Input(component_id='search_top_10_deer', component_property='n_clicks'),
        Input(component_id='top10_unit_numbers', component_property='value')],
        allow_duplicate=True)
    def find_top_10_deer(proclamation_results, search_top_10_deer, unit_number):
        if search_top_10_deer:
            csv_filename = '2024OddsSummary_Deer.csv'
            odds_summary = parser_func("input/{}".format(csv_filename))
            query_result_df = pd.DataFrame(odds_summary)
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
                            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart_with_raw_value(row, 'resident_percent_success', 'Overall Success')))
                            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart_with_raw_value(row, 'resident_1stDraw_percent_success', '1st Draw Success')))
                            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart_with_raw_value(row, 'resident_2ndDraw_percent_success', '2nd Draw Success')))
                            pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart_with_raw_value(row, 'resident_3rdDraw_percent_success', '3rd Draw Success')))
                        
                        # Add pie charts for the current hunt code to the list
                        pie_chart_components.append(html.Div(
                            children=pie_charts_for_this_hunt_code,
                            style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
                        ))

                    # making all of these classes default false becuse we want a more manageable dataframe
                    residency_choice = Residency(False, False, False)
                    choice_result = Choice(False, False, False, False, False)
                    success_total = SuccessTotals(False, False, False)
                    success_percentage = SuccessPercentages(False, False, False)
                    percent_success = PercentSuccess(True, False, False, False, False, False)

                    hunt_code_df = filter_on_boolean_switches(pd.concat(top10_resident_lists, ignore_index=True), residency_choice, choice_result, success_total, success_percentage, percent_success)
                    hunt_code_df = drop_success(hunt_code_df)
                    hunt_code_df = hunt_code_df.drop(columns=["Unit/Description"])
                return pie_chart_components, dash_table.DataTable(data=hunt_code_df.to_dict('records'), page_size=10)
            except KeyError:
                return [None, None]
        else:
            return [None, None]
    
    # @app.callback(
    #     Output("top_10_results_elk", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='unit_number', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_elk(proclamation_results):
    #     return []
    
    # @app.callback(
    #     Output("top_10_results_unit", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='unit_number', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_unit(proclamation_results, unit):
    #     return []

    # @app.callback(
    #     Output("top_10_results_hunt_type", "data"), 
    #     Input('proclamation_results', 'data'),
    #     Input(component_id='weapon_dropdown', component_property='value'),
    #     allow_duplicate=True)
    # def find_top_10_hunt_type(proclamation_results, hunt_type):
    #     return []

