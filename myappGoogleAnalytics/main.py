from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods=["GET"])
def hello_world():
    # display the home_page.html template
    return render_template('home_page.html')

# add a route to see the logs 
@app.route('/logger', methods=["GET"])
def logger():
    script = """
    <script> console.log("Hello, just a little phrase in a console 😋")</script>"""
    return "Take a look at the console for a surprise 🎉" + script




if __name__ == '__main__':
    app.run(debug=True)

