from dash import dcc, html, Input, Output, dash_table
import pandas as pd
from components import unit_dropdown, bag_dropdown, hunt_code_dropdown, create_pie_chart, encoded_image, create_filtering_table
from data_handlers.query_odds import drop_success, filter_on_boolean_switches, get_df_for_pie_chart
from models import Residency, SuccessPercentages, SuccessTotals, Choice


# Layout for Page 1, including a Pie chart
filtering_table_layout = html.Div([
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
                                    dcc.Link('Go to Page find_top_10', href='/find_top_10')  # Link to Page 2
                                ])


# original callbacks to show draw result odds
def filtering_table_callbacks(app):

    # Callback to update merged data and pie charts based on selected unit
    @app.callback(
        [Output('pie-chart-container', 'children'),
        Output('result_info_table', 'children'),],
        Input('query_results', 'data'),
        Input('proclamation_results', 'data'),
        Input('hunt_dropdown', 'value'),
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
    )
    def update_dashboard(dataframe1, dataframe2, selected_hunt_code,
                        show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter,
                        show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals,
                        show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total,
                        show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage,
                        ):
        
        if dataframe1 is not None and dataframe1 != {"": ""} and dataframe2 is not None and dataframe2 != {"": ""}:
            # Merge the two dataframes on 'Hunt Code' and 'Licenses' (inner join)
            df1 = pd.DataFrame.from_dict(dataframe1, orient='index')
            df2 = pd.DataFrame(dataframe2)
            try:
                filtered_df = pd.merge(df1, df2, on=['Hunt Code', 'Licenses', 'Bag'], how='inner')

                # Calculate the percentage values before generating pie charts
                filtered_df = get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
                filtered_df = get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
                filtered_df = get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
                filtered_df = get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')

                if selected_hunt_code is not None and selected_hunt_code != "":
                    filtered_df = filtered_df[filtered_df['Hunt Code'] == selected_hunt_code]
                # Create a list to store pie chart components (dcc.Graph)
                pie_chart_components = []

                # Loop through each unique Hunt Code to generate pie charts for each row
                for hunt_code in filtered_df['Hunt Code'].unique():
                    # Filter rows with the current Hunt Code
                    hunt_code_df = filtered_df[filtered_df['Hunt Code'] == hunt_code]

                    # Create a row for the pie charts for each of the percentage columns
                    pie_charts_for_this_hunt_code = []
                    
                    for _, row in hunt_code_df.iterrows():
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_percent_success', 'Overall Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_1stDraw_percent_success', '1st Draw Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_2ndDraw_percent_success', '2nd Draw Success')))
                        pie_charts_for_this_hunt_code.append(dcc.Graph(figure=create_pie_chart(row, 'resident_3rdDraw_percent_success', '3rd Draw Success')))
                    
                    # Add pie charts for the current hunt code to the list
                    pie_chart_components.append(html.Div(
                        children=pie_charts_for_this_hunt_code,
                        style={'display': 'flex', 'justify-content': 'space-evenly', 'margin-bottom': '20px'}
                    ))    
                
                residency_choice = Residency(show_results_for_resident, show_results_for_nonresident, show_results_for_outfitter)
                choice_result = Choice(show_results_for_1stchoice, show_results_for_2ndchoice, show_results_for_3rdchoice, show_results_for_4thchoice, show_results_for_totals)
                success_total = SuccessTotals(show_resident_successfull_draw_total, show_nonresident_successfull_draw_total, show_outfitter_successfull_draw_total)
                success_percentage = SuccessPercentages(show_resident_successfull_draw_percentage, show_nonresident_successfull_draw_percentage, show_outfitter_successfull_draw_percentage)
                hunt_code_df = filter_on_boolean_switches(filtered_df, residency_choice, choice_result, success_total, success_percentage)
                hunt_code_df = drop_success(hunt_code_df)

                return pie_chart_components, dash_table.DataTable(data=hunt_code_df.to_dict('records'), page_size=10)
            except KeyError:
                return [None, None]
        else:
            return [None, None]
        