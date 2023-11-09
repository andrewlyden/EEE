# from jupyter_dash import JupyterDash
from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
import pandas as pd
import dash_bootstrap_components as dbc

app = Dash(external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div(
    [
        # html.H4("Budget constraint"),
        dcc.Graph(id="graph"),
        html.P("Select demand curve intercept:"),
        dcc.Slider(
            id="slider-intercept",
            min=0,
            max=100,
            step=1,
            value=100,
            marks={i: str(i) for i in range(0, 201, 25)},
        ),
        html.P("Select demand curve slope:"),
        dcc.Slider(
            id="slider-slope",
            min=-5,
            max=0.1,
            step=0.10,
            value=-3.,
            marks={i: str(i) for i in range(-5, 1, 1)},
        ),
        html.P("Select fuel price:"),
        dcc.Slider(
            id="slider-price",
            min=25,
            max=100,
            step=5,
            value=55,
            marks={i: str(i) for i in range(25, 101, 15)},
        )
    ]
)

@app.callback(
    Output("graph", "figure"),
    Input("slider-intercept", "value"),
    Input("slider-slope", "value"),
    Input("slider-price", "value")
)

def plot(intercept, slope, price):
    def demand_function(price):
        x_ = np.arange(0.1, 100., 0.1)
        y_ = []
        for x in x_:
            y = slope * x + intercept
            y_.append(y)
        df_plot = pd.DataFrame({'Quantity of fuel': x_, 'Price of fuel': y_})
        return df_plot

    df_plot = demand_function(price)
    # fig = df_plot.hvplot(kind='line', x='Quantity of fuel', y='Price of fuel', width=800, height=500, xlim=(0, 100), ylim=(0, 100))
    fig = px.line(df_plot, x='Quantity of fuel', y='Price of fuel', range_x=[0,50], range_y=[0,100])
    fig.update_traces(line_color='green', name='Demand curve', showlegend=True)
    quantity = (price - intercept) / slope
    consumer_surplus = (intercept - price) * quantity / 2

    fig_shape1 = go.Figure(go.Scatter(x=[0,0,quantity], y=[intercept,price,price], line=dict(color="LightGreen"), fill="toself"))
    consumer_surplus_text = "Consumer surplus = " + str(round(consumer_surplus, 2))
    fig_shape1.update_traces(name=consumer_surplus_text)

    fig = go.Figure(data=fig.data + fig_shape1.data, layout = fig.layout)

    fig.add_shape(type="line", x0=0, y0=price, x1=quantity, y1=price, line=dict(color="red", width=3, dash="dash"))
    fig.add_shape(type="line", x0=quantity, y0=0, x1=quantity, y1=price, line=dict(color="grey", width=3, dash="dash"))

    return fig

app.run(debug=True)