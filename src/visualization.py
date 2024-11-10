import os

import matplotlib.pyplot as plt
import seaborn as sns
import sweetviz as sv
from data import dataframes
import file_management
from collections import Counter
from config import VISUALIZATIONS_DIR


visualization_file_path = os.path.join('visualizations')

def plot1(electric_cars):
    # Sort electric cars by the concatenation of brand name and model name
    electric_cars_sorted = sorted(electric_cars, key=lambda car: f'{car.brand_name} {car.model_name}')

    # Extracting prices and model names from the sorted list of ElectricCar objects
    prices = [car.price for car in electric_cars_sorted]
    model_names = [f'{car.brand_name} {car.model_name}' for car in electric_cars_sorted]

    # Creating a box plot
    plt.figure(figsize=(12, 8))
    sns.boxplot(x=model_names, y=prices, color='blue')
    plt.title('Prices of Electric Cars by Model (1)')
    plt.xlabel('Model Name')
    plt.ylabel('Price (in Euros)')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.subplots_adjust(left=0.076, bottom=0.33, right=0.96, top=0.96)

    save_plt(plt)

def _get_sort_key(brand_name, model_name):
    # Return a tuple of brand_name and model_name for sorting
    return f'{brand_name.upper()} {model_name.upper()}'

def _get_registration_year(car):
    # Return 0 if first_registration_year is None, otherwise return the integer value
    return int(car.first_registration_year) if car.first_registration_year is not None else 0

def plot2(electric_cars):
    electric_cars_sorted = sorted(electric_cars, key=lambda car: (_get_sort_key(car.brand_name, car.model_name), _get_registration_year(car)))

    prices = [car.price for car in electric_cars_sorted]
    model_names = [f'{car.brand_name.upper()} {car.model_name.upper()}' for car in electric_cars_sorted]
    registration_years = [_get_registration_year(car) for car in electric_cars_sorted]

    model_counts = Counter(model_names)
    model_names = [f'{model_name} ({model_counts[model_name]})' for model_name in model_names]

    palette = sns.color_palette("viridis", len(set(registration_years)))

    plt.figure(figsize=(12, 15))
    sns.boxplot(y=model_names, x=prices, hue=registration_years, dodge=False, palette=palette)

    plt.title('Prices of Electric Cars by Model and Registration Year (2)')
    plt.xlabel('Model Name')
    plt.ylabel('Price (in Euros)')
    plt.xticks(rotation=90)  # Rotate x-axis labels for better readability
    plt.legend(title='Registration Year')
    plt.subplots_adjust(left=0.238, bottom=0.079, right=0.99, top=0.971)
    plt.grid(True)
    #plt.show()
    save_plt(plt)

def save_plt(pplt):
    plt_png_file_path = file_management.generate_file_path(
        VISUALIZATIONS_DIR,
        str(pplt.gca().get_title()),
        '.png')
    pplt.savefig(plt_png_file_path, format='png')


def plot3(electric_cars):
    data = dataframes.create_dataframe(electric_cars)
    report = sv.analyze(data)
    report.show_notebook()

    html_file_path = file_management.generate_file_path(visualization_file_path, 'sweetvis_electric_cars', '.html')

    report.show_html(html_file_path)
    #webbrowser.open('file://' + html_file_path, new=2)

