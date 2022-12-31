from flask import Flask, render_template, Response, request, jsonify
import requests


app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')

# add a route to see the logs 
@app.route('/logger', methods=["GET"])
def logger():
    app.logger.info('testing info log in the console')
    script = """
    <script> console.log("Hello, just a little phrase in a console 😋")</script>"""
    print('hello there')
    return "Take a look at the console for a surprise 🎉" + script


@app.route('/print', methods=["GET"])
def print():
    # using a textbox, print the message in the browser console 
    script = """
    <script>
        function myFunction() {
        var message = document.getElementById("message").value;
        console.log(message);
        }
    </script>"""

    return """
    <input type="text" id="message" placeholder="Enter a message">
    <button onclick="myFunction()">Print</button>""" + script


# set up a cookies route
@app.route('/cookies', methods=["GET"])
def cookies():
    # add a get call to google req =requests.get("https://www.google.com/")
    req = requests.get("https://www.google.com/")
    return req.cookies.get_dict()






if __name__ == '__main__':
    app.run(debug=True)

