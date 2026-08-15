import geopandas as gpd
import contextily as ctx
import matplotlib.pyplot as plt

from app.services import geo_service
from app.helpers.figure_converter_helper import figure_to_base64

def plot_talhao_satellite(talhao_row):
    geometry = geo_service.get_talhao_geometry_web_mercator(talhao_row)
    fig, ax = plt.subplots()

    gpd.GeoSeries([geometry]).plot(ax=ax, facecolor="none", edgecolor="red", linewidth=2)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    x_margin = (xlim[1] - xlim[0]) * 0.3
    y_margin = (ylim[1] - ylim[0]) * 0.3

    ax.set_xlim(xlim[0] - x_margin, xlim[1] + x_margin)
    ax.set_ylim(ylim[0] - y_margin, ylim[1] + y_margin)

    ctx.add_basemap(ax, source=ctx.providers.Esri.WorldImagery, zoom=15)

    ax.set_title("Croqui do Talhão")
    ax.set_axis_off()

    return figure_to_base64(fig)