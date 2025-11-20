import dash
import pandas as pd
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import os 

app = dash.Dash(__name__)
app.title = "5G Fault Prediction Dashboard"

app.layout = html.Div(style={'backgroundColor': '#111111', 'color': '#FFFFFF'}, children=[
    html.H1("📊 AI-Powered 5G Fault Prediction Dashboard", style={'textAlign': 'center'}),
    dcc.Interval(id='interval-component', interval=5000, n_intervals=0),
    html.Div(id='active-alerts-card', style={'padding': '20px', 'fontSize': '24px', 'textAlign': 'center'}),
    dcc.Graph(id='signal-strength-graph'),
    dcc.Graph(id='fault-probability-graph')
])

@app.callback(
    [Output('active-alerts-card', 'children'),
     Output('signal-strength-graph', 'figure'),
     Output('fault-probability-graph', 'figure')],
    Input('interval-component', 'n_intervals')
)
def update_dashboard(n):
    try:
        alerts_df = pd.read_csv('alerts.csv') if os.path.exists('alerts.csv') else pd.DataFrame()
        predictions_df = pd.read_csv('predictions.csv').tail(100) if os.path.exists('predictions.csv') else pd.DataFrame()
        metrics_df = pd.read_csv('metrics.csv').tail(100) 
        
        alerts_card = f"🚨 Active Alerts: {len(alerts_df)}"
        template = 'plotly_dark'
        
        if not metrics_df.empty:
             fig_signal = px.line(metrics_df, x='timestamp', y='signal_strength', color='tower_id', title='Historical Signal Strength (dBm)', template=template)
        else:
             fig_signal = {}

        if not predictions_df.empty:
            fig_prob = px.bar(predictions_df, x='timestamp', y='predicted_fault_probability', color='tower_id', title='Live Predicted Fault Probability', template=template, range_y=[0, 1])
        else:
            fig_prob = {}

        return alerts_card, fig_signal, fig_prob
        
    except (FileNotFoundError, pd.errors.EmptyDataError):
        return "Waiting for data...", {}, {}

if __name__ == '__main__':
    print("📈 Starting Visualization Dashboard at http://127.0.0.1:8050")
    app.run(port=8050)
