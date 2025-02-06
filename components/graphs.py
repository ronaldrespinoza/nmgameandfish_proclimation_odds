import plotly.graph_objects as go

# Define a function to create a more 3D pie chart with slice separation and shading
def create_pie_chart(row, column, label):
    # Create a Pie chart using Plotly Graph Objects
    fig = go.Figure(data=[go.Pie(
        labels=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        hole=0.3,  # Donut chart (optional)
        textinfo='label+percent',  # Remove text info (no labels or percentages)
        hoverinfo='label+percent',  # Hover info will still show label and percentage
        rotation=90,  # Optional rotation for aesthetics
        opacity=0.95,  # Optional opacity for smoothness
        marker=dict(
            colors=['#28a745', '#dc3545'],  # Green for Success, Red for Failure
            line=dict(color='white', width=2),  # Add a white border for better contrast
        ),
        pull=[0.1, 0],  # This pulls the "Success" slice out slightly for depth
    )])

    # Update layout for better visuals
    fig.update_layout(
        showlegend=True,
        title_text=f"{label} - {row['Hunt Code']} <br> {row['Hunt Dates']} - {row['Hunt Type']}",
        paper_bgcolor="#f5f5f5",  # Light gray background for the paper
        plot_bgcolor="#ffffff",  # White background for the plot
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better spacing
        height=400,  # Adjust height to make it more compact
    )
    
    return fig
