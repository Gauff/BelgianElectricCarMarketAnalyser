import webbrowser

import plotly.express as px
from dash import Dash, callback_context, dcc, exceptions, html, no_update
from dash.dependencies import Input, Output

from src import graph_utils, visualization, data_preparation
from src.data_cleaning import clean_car_list
from src.data_preparation import (
    get_cars,
    filter_cars,
    prepare_dataset_for_display,
    save_dataframe,
)
from src.logging_config import setup_logging

# Set up logging
logger = setup_logging(__name__)


def generate_graph(df_cars):
    color_scale = graph_utils.generate_color_scale(df_cars["year"].unique().size)
    plot_height = len(df_cars["model"].unique()) * 25
    fig = px.box(
        df_cars,
        x="Price",
        y="model",
        points="all",
        custom_data=[
            "URL",
            "Image URL",
            "desc",
            "Brand Name",
            "Model Name",
            "year",
            "Kilometers",
            "Price",
        ],
        color="year",
        color_discrete_sequence=color_scale,
        height=plot_height,
    )
    fig.update_layout(yaxis={"categoryorder": "category descending"})
    fig.update_layout(
        legend=dict(
            title="Year",
            orientation="v",
            yanchor="top",
            y=1.0,
            xanchor="left",
            x=1.02,
            traceorder="normal",
        )
    )
    fig.update_layout(plot_bgcolor="white")
    fig.update_layout(yaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray"))
    fig.update_layout(xaxis=dict(showgrid=True, gridwidth=1, gridcolor="lightgray"))
    return fig


def scrap_ads():
    cars = get_cars("web")

    # Save the dataframe
    cars = clean_car_list(cars)
    cars = filter_cars(cars, min_price=500, max_price=300000)
    cars = sorted(
        cars,
        key=lambda car: (
            visualization.get_sort_key(car.brand_name, car.model_name),
            visualization.get_registration_year(car),
        ),
    )
    df_cars = prepare_dataset_for_display(cars)

    save_dataframe(df_cars)

    detect_price_drops()


def detect_price_drops():
    data_preparation.detect_price_drops()


def run_server():
    cars = get_cars("file")
    cars = clean_car_list(cars)
    cars = filter_cars(cars, min_price=500, max_price=300000)
    cars = sorted(
        cars,
        key=lambda car: (
            visualization.get_sort_key(car.brand_name, car.model_name),
            visualization.get_registration_year(car),
        ),
    )
    df_cars = prepare_dataset_for_display(cars)

    filtered_df_cars = df_cars

    min_price = df_cars["Price"].min()
    max_price = df_cars["Price"].max()

    app = Dash(__name__)
    url = "http://127.0.0.1:8050/"
    webbrowser.open(url)
    default_selected_min_price = 2000
    default_selected_max_price = 20000

    app.layout = html.Div(
        [
            html.Button("Refresh Data", id="refresh-button"),
            dcc.RangeSlider(
                id="range-slider",
                min=min_price,
                max=max_price,
                value=[default_selected_min_price, default_selected_max_price],
            ),
            dcc.Graph(
                id="graph-id",
                figure=generate_graph(filtered_df_cars),
                clear_on_unhover=True,
            ),
            dcc.Interval(
                id="interval-component",
                interval=1 * 1000,  # 1 second
                n_intervals=0,  # initial value
                disabled=False,  # initially enabled
            ),
            dcc.Tooltip(id="graph-tooltip"),
            html.Div(id="output-container-range-slider"),
        ]
    )

    @app.callback(
        [Output("graph-id", "figure"), Output("interval-component", "disabled")],
        [
            Input("refresh-button", "n_clicks"),
            Input("interval-component", "n_intervals"),
            Input("graph-id", "clickData"),
        ],
    )
    def update_graph(n_clicks, n_intervals, click_data):
        nonlocal filtered_df_cars

        ctx = callback_context

        if not ctx.triggered:
            raise exceptions.PreventUpdate

        trigger_id = ctx.triggered[0]["prop_id"].split(".")[0]

        if trigger_id == "graph-id" and click_data:
            url = click_data["points"][0]["customdata"][0]
            webbrowser.open_new_tab(url)
            raise exceptions.PreventUpdate

        if trigger_id == "refresh-button" or trigger_id == "interval-component":
            return generate_graph(filtered_df_cars), True

        return no_update, no_update

    @app.callback(
        Output("graph-tooltip", "show"),
        Output("graph-tooltip", "bbox"),
        Output("graph-tooltip", "children"),
        Input("graph-id", "hoverData"),
    )
    def display_hover(hover_data):
        if hover_data is None:
            return False, no_update, no_update

        hover_data = hover_data["points"][0]
        bbox = hover_data["bbox"]
        custom_data = hover_data["customdata"]
        url = custom_data[0]
        image_url = custom_data[1]
        desc = custom_data[2]
        make = custom_data[3]
        model = custom_data[4]
        year = custom_data[5] if custom_data[5] is not None else "-"
        km = f"{custom_data[6]}km" if custom_data[6] is not None else ""
        price = custom_data[7]

        children = [
            html.Div(
                [
                    dcc.Markdown(
                        f"**{make} {model}**<br>{year} | {km}<br>**{price}€**",
                        dangerously_allow_html=True,
                    ),
                    html.Img(
                        src=image_url,
                        style={"max-width": "300px", "max-height": "300px"},
                    ),
                    dcc.Markdown(desc, dangerously_allow_html=True),
                ],
                style={"width": "700px"},
            )
        ]

        return True, bbox, children

    @app.callback(
        Output("output-container-range-slider", "children"),
        [Input("range-slider", "value")],
    )
    def update_output(value):
        nonlocal filtered_df_cars
        lower_price = min(value)
        upper_price = max(value)
        filtered_df_cars = df_cars[
            (df_cars["Price"] >= lower_price) & (df_cars["Price"] <= upper_price)
        ]

    app.run(debug=True, use_reloader=False)


def scrap_adds_and_run_server():
    scrap_ads()
    run_server()


if __name__ == "__main__":
    try:
        # scrap_adds_and_run_server()
        # scrap_ads()
        run_server()
    except Exception as e:
        logger.error(f"An error occurred: {e!s}", exc_info=True)
