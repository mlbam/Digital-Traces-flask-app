from flask import Flask, render_template
import requests
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'digital-traces-373311-c607e60b6a4d.json'
VIEW_ID = '281216124' 





def initialize_analyticsreporting():
  credentials = ServiceAccountCredentials.from_json_keyfile_name(
      KEY_FILE_LOCATION, SCOPES)
  analytics = build('analyticsreporting', 'v4', credentials=credentials)

  return analytics


def get_report(analytics):
  return analytics.reports().batchGet(
      body={
        'reportRequests': [
        {
          'viewId': VIEW_ID,
          'dateRanges': [{'startDate': '30daysAgo', 'endDate': 'today'}],
          'metrics': [{'expression': 'ga:pageviews'}],
          'dimensions': []
        }]
      }
  ).execute()


def get_visitors(response):
  visitors = 0 # in case there are no analytics available yet
  for report in response.get('reports', []):
    columnHeader = report.get('columnHeader', {})
    metricHeaders = columnHeader.get('metricHeader', {}).get('metricHeaderEntries', [])

    for row in report.get('data', {}).get('rows', []):
      dateRangeValues = row.get('metrics', [])

      for i, values in enumerate(dateRangeValues):
        for metricHeader, value in zip(metricHeaders, values.get('values')):
          visitors = value

  return str(visitors)

@app.route('/visitors')
def visitors():
  analytics = initialize_analyticsreporting()
  response = get_report(analytics)
  visitors = get_visitors(response)

  return "Number of visitor fetched from Google Analytics using its API (GCP) : " + visitors






@app.route('/', methods=["GET"])
def hello_world():
        prefix_google = """
            <!-- Google tag (gtag.js) -->
            <script async
            src="https://www.googletagmanager.com/gtag/js?id=UA-251017585-1"></script>
            <script>
            window.dataLayer = window.dataLayer || [];
            function gtag(){dataLayer.push(arguments);}
            gtag('js', new Date());
            gtag('config', ' UA-251017585-1');
            </script>
            """
        return prefix_google + "Hello World"

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


# set up a cookies route
@app.route('/cookies_GA', methods=["GET"])
def cookies_GA():
    # add a get call to google req =requests.get("https://www.google.com/")
    req = requests.get("https://analytics.google.com/analytics/web/#/report-home/a251017585w345101616p281216124")
    return req.text











if __name__ == '__main__':
    app.run(debug=True)

