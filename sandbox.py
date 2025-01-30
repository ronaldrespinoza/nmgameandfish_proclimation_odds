import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.express as px
from dash.dependencies import Input, Output

# Updated Dataframe 1 (Hunt Code Unit data)
dataframe1 = pd.DataFrame({
    'Hunt Code': ['ELK-3-308', 'ELK-3-309', 'ELK-3-310'],
    'Unit/Description': ['Unit 17', 'Unit 17', 'Unit 17'],
    'Bag': ['MB', 'MB', 'MB'],
    'Licenses': [100, 100, 25],
    '1st_resident': [216, 51, 40],
    '2nd_resident': [278, 145, 46],
    '3rd_resident': [240, 170, 102],
    'Total_resident': [734, 366, 188],
    'resident_1st_success': [57, 32, 16],
    'resident_2nd_success': [47, 10, 6],
    'resident_3rd_success': [25, 11, 6],
    'Resident_successfull_draw_total': [84, 84, 21],
    'Total_drawn': [100.0, 100.0, 25.0],
    'total_allocation_of_available_tags': [100.0, 100.0, 100.0]
})

# Dataframe 2 (Hunt Details data)
dataframe2 = pd.DataFrame({
    'Unit': ['Unit 17', 'Unit 17', 'Unit 17', 'Unit 17', 'Unit 17', 'Unit 17', 'Unit 17', 'Unit 17', 'Unit 17'],
    'Hunt Type': ['Bow', 'Bow', 'Muzzle – Youth Only', 'Muzzle', 'Muzzle', 'Muzzle', 'Muzzle – NM', 'Muzzle – NM', 'Muzzle – NM'],
    'Hunt Dates': ['Sep . 1-14', 'Sep . 15-24', 'Oct . 11-15', 'Oct . 18-22', 'Oct . 25-29', 'Nov . 22-26', 'Nov . 22-26', 'Dec . 6-10', 'Dec . 13-17'],
    'Hunt Code': ['ELK-2-305', 'ELK-2-306', 'ELK-3-307', 'ELK-3-308', 'ELK-3-309', 'ELK-3-310', 'ELK-3-311', 'ELK-3-312', 'ELK-3-313'],
    'Fee Type': ['HD', 'Q/HD', 'HD', 'Q/HD', 'HD', 'HD', 'S', 'S', 'S'],
    'Licenses': [125, 75, 25, 100, 100, 25, 25, 100, 100],  # Same column name as in dataframe1
    'Bag Limit': ['ES', 'ES', 'ES', 'MB', 'MB', 'MB', 'A', 'A', 'A']
})

# Merge the two dataframes on 'Hunt Code' and 'Licenses' (inner join)
merged_df = pd.merge(dataframe1, dataframe2, on=['Hunt Code', 'Licenses'], how='inner')

# Function to calculate percentage for pie charts
def get_df_for_pie_chart(df, new_column, total_column, factored_column):
    df[new_column] = df[total_column] / df[factored_column] * 100
    return df

# Function to create pie charts
def create_pie_chart(row, column, label):
    fig = px.pie(
        names=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        title=f"{label} - {row['Hunt Code']}",
        hole=0.3
    )
    return fig

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the app
app.layout = html.Div([
    html.H1("Hunt Data Dashboard with Merged Data"),
    
    # Dropdown for selecting a unit
    html.Label("Select Hunt Unit:"),
    dcc.Dropdown(
        id='unit-dropdown',
        options=[{'label': unit, 'value': unit} for unit in merged_df['Unit/Description'].unique()],
        value='Unit 17'  # default value
    ),
    
    # Display merged Data
    html.Div([
        html.H2("Merged Hunt Data"),
        html.Div(id='merged-data')
    ]),
    
    # Pie chart for resident success rate
    html.Div([
        html.H2("Resident Success Rates by Hunt Code"),
        html.Div(id='pie-chart-container')  # This will hold the dynamically generated pie charts
    ])
])

# Callback to update merged data and pie charts based on selected unit
@app.callback(
    [Output('merged-data', 'children'),
     Output('pie-chart-container', 'children')],
    [Input('unit-dropdown', 'value')]
)
def update_dashboard(selected_unit):
    # Filter the merged DataFrame based on the selected unit
    filtered_df = merged_df[merged_df['Unit/Description'] == selected_unit]

    # Calculate the percentage values before generating pie charts
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_percent_success', 'Resident_successfull_draw_total', 'Total_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_1stDraw_percent_success', 'resident_1st_success', '1st_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_2ndDraw_percent_success', 'resident_2nd_success', '2nd_resident')
    filtered_df = get_df_for_pie_chart(filtered_df, 'resident_3rdDraw_percent_success', 'resident_3rd_success', '3rd_resident')

    # Generate the table of merged Data
    merged_table = html.Table(
        # Header
        [html.Tr([html.Th(col) for col in filtered_df.columns])] +
        # Rows
        [html.Tr([html.Td(filtered_df.iloc[i][col]) for col in filtered_df.columns]) for i in range(len(filtered_df))]
    )

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

    return merged_table, pie_chart_components

# Run the server
if __name__ == '__main__':
    app.run_server(debug=True)
