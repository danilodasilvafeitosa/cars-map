import matplotlib.pyplot as plt

from datetime import date
from app.helpers.figure_converter_helper import figure_to_base64

MONTHS=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

def plot_rainfall_climatology(monthly_data):
    fig, ax = plt.subplots()
    ax.bar(monthly_data.index, monthly_data["precipitation_sum"])
    ax.set_title("Climatologia de chuva (30 anos)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Precipitação (mm)")
    ax.set_xticks(monthly_data.index, labels=MONTHS)

    return figure_to_base64(fig)

def plot_temperature_climatology(monthly_data):
    fig, ax = plt.subplots()
    ax.plot(monthly_data.index, monthly_data["temperature_2m_max"], label="Máxima")
    ax.plot(monthly_data.index, monthly_data["temperature_2m_mean"], label="Média")
    ax.plot(monthly_data.index, monthly_data["temperature_2m_min"], label="Mínima")
    ax.legend()
    ax.set_title("Climatologia de Temperatura (30 anos)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Temperatura (C°)")
    ax.set_xticks(monthly_data.index, labels=MONTHS)

    return figure_to_base64(fig)


def plot_rainfall_comparison(climatology_data, current_year_data):
    matching_months = climatology_data.loc[current_year_data.index]
    current_year = date.today().year
    fig, ax = plt.subplots()

    ax.plot(matching_months.index, matching_months["precipitation_sum"], label="Média histórica")
    ax.plot(current_year_data.index, current_year_data["precipitation_sum"], label=f'{current_year}')

    ax.legend()
    ax.set_title("Comparativo climatologia de chuva")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Precipitação (mm)")
    ax.set_xticks(current_year_data.index, labels=MONTHS[:len(current_year_data)])

    return figure_to_base64(fig)

def plot_temperature_comparison(climatology_data, current_year_data):
    matching_months = climatology_data.loc[current_year_data.index]
    current_year = date.today().year
    fig, ax = plt.subplots()

    ax.plot(matching_months.index, matching_months["temperature_2m_max"], label="Máxima histórica", color="C0")
    ax.plot(matching_months.index, matching_months["temperature_2m_mean"], label="Média histórica", color="C1")
    ax.plot(matching_months.index, matching_months["temperature_2m_min"], label="Mínima histórica", color="C2")

    ax.plot(current_year_data.index, current_year_data["temperature_2m_max"], label=f'Máxima de {current_year}', linestyle="--", color="C0")
    ax.plot(current_year_data.index, current_year_data["temperature_2m_mean"], label=f'Média de {current_year}', linestyle="--", color="C1")
    ax.plot(current_year_data.index, current_year_data["temperature_2m_min"], label=f'Mínima de {current_year}', linestyle="--", color="C2")

    ax.legend()
    ax.set_title("Comparativo climatologia de temperatura")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Temperatura (C°)")
    ax.set_xticks(current_year_data.index, labels=MONTHS[:len(current_year_data)])

    return figure_to_base64(fig)
