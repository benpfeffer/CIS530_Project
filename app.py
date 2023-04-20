# App.py file for Cart-Based Pizza Recommendation System
# Ben Pfeffer, Andrew Anctil, Bradon Wetzel
# CIS 530 - Advanced Data Mining - Professor Thomas Gyeera

# Import necessary libraries
from flask import Flask, render_template, request, jsonify
import numpy as np
from matplotlib.figure import Figure
import io
import base64
from io import BytesIO
import os
from Pizza_recommendation_live import *
from Pizza_recommendation_plots import *
from plot_metrics import *

# Initialize application
app = Flask(__name__, static_folder='templates')

# Get and store the style for the renders
style = os.path.join('templates', 'style.css')

@app.route("/")
def index():
    # Send image and homepage ss to be rendered
    pizza_image = os.path.join('templates', 'images', 'pizza.jpg')
    home_css = os.path.join('templates', 'Home.css')
    return render_template("index.html", pizza_image = pizza_image, style = style, home_css = home_css)

@app.route("/cart")
def cart():
    # Send cart css to be rendered
    cart_css = os.path.join('templates', 'Cart.css')
    return render_template("Cart.html", style = style, cart_css = cart_css)

@app.route('/get_pizzas')
def get_pizzas():
    # Get pizza data (stores in a config file)
    with open('config.json', 'r') as file:
        return jsonify(file.read().replace('\n', ''))

@app.route('/reccomendations', methods=["POST"])
def reccomend():
    # Get and clean cart data
    cart = request.args.get('cart')
    cart_arr = cart.split(',')

    # Get the recommendations for the cart
    return get_recs(cart_arr)

@app.route("/plot1", methods=["POST"])
def plot1():
    # Get and clean cart data
    cart = request.args.get('cart')
    cart_arr = cart.split(',')

    # Plot the recommendations for plot 3
    fig, _fig2 = plot_recs(cart_arr)
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(image=f"data:image/png;base64,{data}")

@app.route("/plot2", methods=["POST"])
def plot2():
    # Get and clean cart data
    cart = request.args.get('cart')
    cart_arr = cart.split(',')

    # Plot the recommendations for plot 2
    _fig, fig2 = plot_recs(cart_arr)
    buf = BytesIO()
    fig2.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(image=f"data:image/png;base64,{data}")

@app.route("/plot3", methods=["post"])
def plot3():

    # Plot the recommendations for plot 3
    fig = plot_metrics()
    buf = BytesIO()
    fig.savefig(buf, format="png")
    # Embed the result in the html output.
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return jsonify(image=f"data:image/png;base64,{data}")

if __name__ == "__main__":
    # Run on port 8000
    app.run(port=8000, debug=True)

