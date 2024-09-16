from dash import Input, Output, dash, dcc, html

from callbacks import register_callbacks
from layouts import landing_layout, main_app_layout

# Initialize the Dash app
app = dash.Dash(__name__, assets_folder="assets", suppress_callback_exceptions=True)
server = app.server
app.layout = html.Div(
    [dcc.Location(id="url", refresh=False), html.Div(id="page-content")]
)

@app.callback(Output("page-content", "children"), Input("url", "pathname"))
def display_page(pathname):
    if pathname == "/main":
        return main_app_layout
    else:
        return landing_layout


# Register callbacks
register_callbacks(app)