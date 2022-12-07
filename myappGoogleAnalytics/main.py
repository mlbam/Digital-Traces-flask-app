from flask import Flask, render_template
app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')

# add a route to see the logs 
@app.route('/logger', methods=["GET"])
def logs():
    # print a log on python 
    app.logger.info('This is a log')
    # display the logs on the front 
    return "This is a log"

