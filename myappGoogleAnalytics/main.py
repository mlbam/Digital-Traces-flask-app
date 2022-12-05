from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')