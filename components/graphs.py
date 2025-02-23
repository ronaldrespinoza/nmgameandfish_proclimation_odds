import plotly.graph_objects as go

# Define a function to create a more 3D pie chart with slice separation and shading
def create_pie_chart(row, column, label):
    # Create a Pie chart using Plotly Graph Objects
    fig = go.Figure(data=[go.Pie(
        labels=["Success", "Failure"],
        values=[row[column], 100 - row[column]],
        hole=0.3,  # Donut chart (optional)
        textinfo='label+percent',  # labels and percentages
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


def create_pie_chart_with_raw_value(row, percent_column, label):
    """
    Helper function to create a pie chart with raw percentage values (even if > 100%).
    """
    # Extract the raw percentage
    raw_value = row[percent_column]
    
    # Handle special cases where success is 0% or 100%
    if raw_value == 0:
        # If the success percentage is 0%, show only the 'Failure' slice
        fig = go.Figure(data=[go.Pie(
            labels=[label, 'Zero Submissions'],
            values=[0, 1],  # Success is 0%, Failure is 100%
            hole=0.3,  # Donut chart (optional)
            textinfo='label',  # labels and percentages
            hoverinfo='label',  # Hover info will still show label and percentage
            rotation=90,  # Optional rotation for aesthetics
            opacity=0.95,  # Optional opacity for smoothness
            marker=dict(
                colors=['#28a745', '#dc3545'],  # Green for Success, Red for Failure
                line=dict(color='white', width=2),  # Add a white border for better contrast
            ),
            pull=[0.1, 0],  # This pulls the "Success" slice out slightly for depth
            textfont=dict(color="black", size=25),
        )])
    elif raw_value == 100:
        # If the success percentage is 100%, show only the 'Success' slice
        fig = go.Figure(data=[go.Pie(
            labels=[label, 'Failure'],
            values=[1, 0],  # Success is 100%, Failure is 0%
            hole=0.3,  # Donut chart (optional)
            textinfo='label+percent',  # labels and percentages
            hoverinfo='label+percent',  # Hover info will still show label and percentage
            rotation=90,  # Optional rotation for aesthetics
            opacity=0.95,  # Optional opacity for smoothness
            marker=dict(
                colors=['#28a745', '#dc3545'],  # Green for Success, Red for Failure
                line=dict(color='white', width=2),  # Add a white border for better contrast
            ),
            pull=[0.1, 0],  # This pulls the "Success" slice out slightly for depth
            textfont=dict(color="black", size=25),
        )])
    else:
        # For all other cases, normalize the success percentage
        normalized_value = raw_value / max(100, raw_value)  # Normalize but let values over 100% still appear correctly
        
        fig = go.Figure(data=[go.Pie(
            labels=[label, 'Failure'],
            values=[normalized_value, 1 - normalized_value],  # Always sum to 100% visually
            hole=0.3,  # Donut chart (optional)
            textinfo='label+percent',  # labels and percentages
            hoverinfo='label+percent',  # Hover info will still show label and percentage
            rotation=90,  # Optional rotation for aesthetics
            opacity=0.95,  # Optional opacity for smoothness
            marker=dict(
                colors=['#28a745', '#dc3545'],  # Green for Success, Red for Failure
                line=dict(color='white', width=2),  # Add a white border for better contrast
            ),
            pull=[0.1, 0],  # This pulls the "Success" slice out slightly for depth
            textfont=dict(color="black", size=25),
        )])

        # Update layout for better visuals
    fig.update_layout(
        showlegend=False,
        title_text=f"{row['Unit']} {label} - {row['Hunt Code']} <br> {row['Hunt Dates']} - {row['Hunt Type']}",
        paper_bgcolor="#f5f5f5",  # Light gray background for the paper
        plot_bgcolor="#ffffff",  # White background for the plot
        margin=dict(t=40, b=40, l=40, r=40),  # Adjust margins for better spacing
        height=400,  # Adjust height to make it more compact
    )
    
    return fig