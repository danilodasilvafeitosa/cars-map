import matplotlib.pyplot as plt
import io
import base64

def plot_rainfall_climatology(monthly_data):
    fig, ax = plt.subplots()
    ax.bar(monthly_data.index, monthly_data["precipitation_sum"])
    ax.set_title("Climatologia de chuva (30 anos)")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Precipitação (mm)")
    ax.set_xticks(monthly_data.index, labels=["Jan", "Fev", "Mar", "Abr", "Mai", "Jun", "Jul", "Ago", "Set", "Out", "Nov", "Dez"])

    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)

    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")

    plt.close(fig)
    return image_base64
