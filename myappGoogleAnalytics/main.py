import base64
from dotenv import load_dotenv
from flask import Flask, render_template
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials
from io import BytesIO
import matplotlib.pyplot as plt
import os
from pytrends.request import TrendReq
import requests





load_dotenv()
app = Flask(__name__)

SCOPES = ['https://www.googleapis.com/auth/analytics.readonly']
KEY_FILE_LOCATION = 'digital-traces-373311-c607e60b6a4d.json'
VIEW_ID = os.getenv("VIEW_ID")





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

  return "nb visitors" + visitors






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


# set up a route to display google trends intel using pytrends from the last 90 days in france 
@app.route('/trends', methods=["GET"])
def trends():

    pytrends = TrendReq(hl='fr-FR', tz=360)
    kw_list = ["Python"]
    pytrends.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='FR', gprop='')
    data = pytrends.interest_over_time()
    # return the data in a table format
    return data.to_html()




@app.route('/chart', methods = ["GET", "POST"])
def chartpytrend():
    #pytrends = TrendReq(hl='en-US', tz=360, timeout=(10,25), proxies=['https://34.203.233.13:80',], retries=2, backoff_factor=0.1, requests_args={'verify':False})

    pytrends = TrendReq()
    kw_list = ['vacances']
    pytrends.build_payload(kw_list=kw_list, timeframe='today 3-m', geo='FR', gprop='')
    trend_data = pytrends.interest_over_time()

    # Create a line chart using Matplotlib
    plt.plot(trend_data['vacances'])
    plt.xlabel('Date')
    plt.ylabel('Trend')

    # Save the chart to a PNG file
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)

    # Encode the chart in base64
    chart = base64.b64encode(buf.getvalue()).decode()
    plt.clf()

    # return the chart 
    return '<img src="data:image/png;base64,{}">'.format(chart)



if __name__ == '__main__':
    app.run(debug=True)

