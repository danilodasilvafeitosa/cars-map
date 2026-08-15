import matplotlib.pyplot as plt
from datetime import date
import io
import base64

MONTHS=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"]

def _figure_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    
    plt.close(fig)
    return image_base64

def plot_rainfall_climatology(monthly_data):
    fig, ax = plt.subplots()
    ax.bar(monthly_data.index, monthly_data["precipitation_sum"])
    ax.set_title("Climatologia de chuva (30 anos)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Precipitação (mm)")
    ax.set_xticks(monthly_data.index, labels=MONTHS)

    return _figure_to_base64(fig)

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

    return _figure_to_base64(fig)


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

    return _figure_to_base64(fig)
