import plotly.express as px

# Function to create pie charts
def create_pie_chart(row, column, label):
    fig = px.pie(
        names=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        title=f"{label} - {row['Hunt Code']} <br> {row['Hunt Dates']} - {row['Hunt Type']}",
        hole=0.3
    )
    return fig