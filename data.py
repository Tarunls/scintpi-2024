import dash
from dash import dcc, html
import pandas as pd
import plotly.graph_objects as go
from dash.dependencies import Input, Output
from datetime import datetime, timedelta
from azure.storage.blob import BlobServiceClient
import io
import re

SATELLITE_SYSTEMS = {
    0: "GPS",
    1: "SBS",
    2: "GAL",
    3: "BDS",
    5: "QZS",
    6: "GLO"
}

AZURE_CONNECTION_STRING = 'ASKFORDOTENV'
BLOB_CONTAINER = "bulkfiles"

blob_service_client = BlobServiceClient.from_connection_string(AZURE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER)

# Global cache
cached_df = None
last_fetch_time = None

app = dash.Dash(__name__)
server = app.server

def fetch_txt_blobs():
    blobs = container_client.list_blobs(name_starts_with="log_")
    txt_streams = []
    for blob in blobs:
        if blob.name.endswith(".txt"):
            blob_client = container_client.get_blob_client(blob.name)
            stream = io.BytesIO()
            blob_client.download_blob().readinto(stream)
            stream.seek(0)
            txt_streams.append((blob.name, stream))
    return txt_streams

def parse_log_streams(streams):
    pattern = re.compile(r"(\w+):\s*([\d\.\-]+)")
    data_list = []
    for name, stream in streams:
        for line in stream.getvalue().decode().splitlines():
            matches = pattern.findall(line)
            if matches:
                data_list.append({key: float(value) if "." in value else int(value) for key, value in matches})

    df = pd.DataFrame(data_list) if data_list else pd.DataFrame()
    if not df.empty:
        offset = pd.Timedelta('3657 days 05:00:18')
        gps_epoch = pd.Timestamp("1980-01-06")
        leap_seconds = pd.Timedelta(seconds=18)
        df['datetime'] = pd.to_datetime(df['tow'], unit='s') - offset + leap_seconds
        df['datetime'] += gps_epoch - pd.Timestamp("1970-01-01")
        df['system'] = df['const'].map(lambda x: SATELLITE_SYSTEMS.get(x, "Unknown"))
        return df[['tow', 'datetime', 'PRN', 'const', 'system', 's4', 'elev', 'azim']]
    return df

def get_cached_df():
    global cached_df, last_fetch_time
    now = datetime.utcnow()
    if cached_df is None or last_fetch_time is None or (now - last_fetch_time).total_seconds() > 300:
        print("Refreshing cache...")
        streams = fetch_txt_blobs()
        cached_df = parse_log_streams(streams)
        last_fetch_time = now
    else:
        print("Using cached data...")
    return cached_df

CONTENT_STYLE = {
    "margin-left": "2rem",
    "margin-right": "2rem",
    "padding": "2rem",
    "backgroundColor": "#1e1e1e"
}

app.layout = html.Div([
    dcc.Interval(id='interval-component-24h', interval=15000, n_intervals=0),
    dcc.Interval(id='interval-component-sky', interval=15000, n_intervals=0),

    html.Div(id='last-update-time',
             style={'color': 'white', 'textAlign': 'right', 'paddingRight': '1rem', "font-family": "Ubuntu, sans-serif"}),

    html.H1("ScintPi Real-time Dashboard, Station: UTD (32.99°N, 96.76°W)",
            style={"textAlign": "center", "color": "white", "marginBottom": "2rem", "paddingTop": "1rem", "font-family": "Ubuntu, sans-serif"}),

    html.Div(id='main-graph-container'),
    html.Div(id='sky-plot-container'),
], style=CONTENT_STYLE)

@app.callback(
    Output('last-update-time', 'children'),
    [Input('interval-component-24h', 'n_intervals'),
     Input('interval-component-sky', 'n_intervals')]
)
def update_last_update_time(n1, n2):
    now = datetime.now()
    return f"Last checked for updates: {now.strftime('%Y-%m-%d %H:%M:%S')}"

@app.callback(
    Output('main-graph-container', 'children'),
    Input('interval-component-24h', 'n_intervals')
)
def update_main_graph(n):
    df = get_cached_df()

    if df.empty:
        return html.Div(
            html.H3("Waiting for data...", style={"color": "white", "textAlign": "center", "marginTop": "2rem", "font-family": "Ubuntu, sans-serif"})
        )

    filtered_df = df[df['elev'] >= 30].copy()
    max_time = filtered_df['datetime'].max()
    min_time = max_time - timedelta(hours=72)
    filtered_df = filtered_df[filtered_df['datetime'] > min_time]
    filtered_df = filtered_df[~((filtered_df['system'] == 'GLO') & (filtered_df['PRN'] == 255))]

    if filtered_df.empty:
        return html.Div(
            html.H3("No data available above 30° elevation", style={"color": "white", "textAlign": "center", "marginTop": "2rem", "font-family": "Ubuntu, sans-serif"})
        )

    scatter_fig = go.Figure()
    scatter_fig.add_trace(
        go.Scattergl(
            x=filtered_df['datetime'],
            y=filtered_df['s4'],
            mode='markers',
            marker=dict(color='#636EFA', size=5),
            hovertemplate=(
                "<b>PRN:</b> %{customdata[0]}<br>" +
                "<b>System:</b> %{customdata[1]}<br>" +
                "<b>Elevation:</b> %{customdata[2]:.1f}°<br>" +
                "<b>Azimuth:</b> %{customdata[3]:.1f}°<br>" +
                "<b>S4:</b> %{y:.4f}<br>" +
                "<b>Time:</b> %{x|%H:%M:%S}<extra></extra>"
            ),
            customdata=filtered_df[['PRN', 'system', 'elev', 'azim']].values
        )
    )

    scatter_fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="#1e1e1e",
        plot_bgcolor="#1e1e1e",
        font=dict(color="white", family="Ubuntu, sans-serif"),
        title="S4",
        title_x=0.5,
        xaxis_title="Central Daylight Time (UTC-5)",
        yaxis_title="S4 Index",
        showlegend=False,
        xaxis=dict(range=[min_time, max_time], tickformat='%H:%M \n %Y-%m-%d', gridcolor='rgba(255,255,255,0.1)'),
        yaxis=dict(range=[0, 1], gridcolor='rgba(255,255,255,0.1)')
    )

    return dcc.Graph(
        figure=scatter_fig,
        style={"marginBottom": "2rem", "backgroundColor": "#1e1e1e", "borderRadius": "5px", "padding": "1rem", "height": "70vh"},
        config={'displayModeBar': True, 'scrollZoom': True, 'doubleClick': 'reset'}
    )

@app.callback(
    Output('sky-plot-container', 'children'),
    Input('interval-component-sky', 'n_intervals')
)
def update_sky_plot(n):
    df = get_cached_df()

    if df.empty:
        return html.Div(
            html.H3("Waiting for data...", style={"color": "white", "textAlign": "center", "marginTop": "2rem", "font-family": "Ubuntu, sans-serif"})
        )

    filtered_df = df[df['elev'] >= 30].copy()
    if filtered_df.empty:
        return html.Div(
            html.H3("No data available above 30° elevation", style={"color": "white", "textAlign": "center", "marginTop": "2rem", "font-family": "Ubuntu, sans-serif"})
        )

    max_time = filtered_df['datetime'].max()
    last_30_min = max_time - timedelta(minutes=30)
    polar_df = filtered_df[filtered_df['datetime'] >= last_30_min].copy()

    if polar_df.empty:
        return html.Div(
            html.H3("No recent data (last 30 minutes)", style={"color": "white", "textAlign": "center", "marginTop": "2rem", "font-family": "Ubuntu, sans-serif"})
        )

    polar_df.loc[:, 'r_sky'] = 90 - polar_df['elev']

    polar_fig = go.Figure()
    polar_fig.add_trace(
        go.Scatterpolar(
            r=polar_df['r_sky'],
            theta=polar_df['azim'],
            mode='markers',
            marker=dict(
                size=8,
                color=polar_df['s4'],
                colorscale='Bluered',
                cmin=0,
                cmax=0.3,
                colorbar=dict(title="S4 Index")
            ),
            hovertemplate=(
                "<b>PRN:</b> %{customdata[0]}<br>" +
                "<b>System:</b> %{customdata[1]}<br>" +
                "<b>Elevation:</b> %{customdata[2]:.1f}°<br>" +
                "<b>Azimuth:</b> %{theta:.1f}°<br>" +
                "<b>S4:</b> %{marker.color:.4f}<br>" +
                "<b>Time:</b> %{customdata[3]}<extra></extra>"
            ),
            customdata=polar_df[['PRN', 'system', 'elev', 'datetime']].values
        )
    )

    polar_fig.update_layout(
        margin=dict(l=40, r=40, t=60, b=40),
        paper_bgcolor="#1e1e1e",
        font=dict(color="white", family="Ubuntu, sans-serif"),
        title="Sky Plot",
        title_x=0.5,
        polar=dict(
            bgcolor="#1e1e1e",
            angularaxis=dict(
                direction="clockwise",
                tickmode="array",
                tickvals=[0, 90, 180, 270],
                ticktext=["N", "E", "S", "W"]
            ),
            radialaxis=dict(
                range=[0, 70],
                tickvals=[0, 30, 60],
                ticktext=["90°", "60°", "30°"],
                gridcolor="rgba(255,255,255,0.1)",
                showline=True,
                linewidth=1
            )
        )
    )

    return dcc.Graph(
        figure=polar_fig,
        style={"marginBottom": "2rem", "backgroundColor": "#1e1e1e", "borderRadius": "5px", "padding": "1rem", "height": "70vh"},
        config={'displayModeBar': True, 'scrollZoom': True, 'doubleClick': 'reset'}
    )

if __name__ == "__main__":
    app.run_server(debug=True)
