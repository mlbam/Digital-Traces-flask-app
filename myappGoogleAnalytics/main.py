from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')

# add a route to see the logs 
@app.route('/logger', methods=["GET"])
def logger():
    # print in the console a phrase with a smiley hand shaking
    app.logger.info('testing info log in the console')
    script = """
    <script> console.log("Hello, just a little phrase in a console 😋")</script>"""
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








if __name__ == '__main__':
    app.run(debug=True)

