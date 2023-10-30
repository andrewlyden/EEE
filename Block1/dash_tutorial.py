from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd

app = Dash(__name__)

app.layout = html.Div(
    [
        html.H4("Budget constraint"),
        dcc.Graph(id="graph"),
        html.P("Select budget:"),
        dcc.Slider(
            id="slider-budget",
            min=10,
            max=100,
            step=5,
            value=100,
            marks={i: str(i) for i in range(10, 101, 10)},
        ),
        html.P("Select fuel price:"),
        dcc.Slider(
            id="slider-fuel",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        ),
        html.P("Select food price:"),
        dcc.Slider(
            id="slider-food",
            min=1,
            max=5,
            step=1,
            value=1,
            marks={i: str(i) for i in range(1, 6, 1)},
        )
    ]
)


@app.callback(
    Output("graph", "figure"),
    Input("slider-budget", "value"),
    Input("slider-fuel", "value"),
    Input("slider-food", "value"),
)

def max(budget, fuel, food):
    df = pd.DataFrame({'Quantity of fuel': [0, budget / fuel], 'Quantity of food': [budget / food, 0]})
    fig = px.line(df, x='Quantity of fuel', y='Quantity of food', range_x=[0,100], range_y=[0,100])
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)