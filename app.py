from flask import Flask, render_template, request, jsonify
import numpy as np
from matplotlib.figure import Figure
import io
import base64
from io import BytesIO

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/plot", methods=["POST"])
def plot():
    data = request.get_json()["data"]
    x = np.arange(len(data))
    y = np.array(data)
    # Generate the figure **without using pyplot**.
    fig = Figure()
    ax = fig.subplots()
    ax.plot(x, y)
    # Save it to a temporary buffer.
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(image=f"data:image/png;base64,{data}")

if __name__ == "__main__":
    app.run(port=8000, debug=True)

