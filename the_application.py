from dash import Input, Output, dash, dcc, html

from callbacks import register_callbacks
from layouts import landing_layout, main_app_layout

# Initialize the Dash app
app = dash.Dash(__name__, assets_folder="assets", suppress_callback_exceptions=True)

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

if __name__ == "__main__":
    app.run_server(debug=True)
    # app.run_server(debug=False, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
