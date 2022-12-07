from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')

# add a route to see the logs 
@app.route('/logger', methods=["GET"])
def logs():
    # get the logs of the page 
    logs = app.logger.get_logs()
    # display the logs.html template
    return render_template('logs.html', logs=logs)

