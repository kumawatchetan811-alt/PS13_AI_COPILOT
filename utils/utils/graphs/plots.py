import plotly.graph_objects as go

def create_graph(data_list, label):
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        y=data_list,
        mode='lines+markers'
    ))

    fig.update_layout(title=label)
    return fig