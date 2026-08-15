import io
import base64
import matplotlib.pyplot as plt

def figure_to_base64(fig):
    buffer = io.BytesIO()
    fig.savefig(buffer, format="png")
    buffer.seek(0)
    
    image_base64 = base64.b64encode(buffer.read()).decode("utf-8")
    
    plt.close(fig)
    return image_base64