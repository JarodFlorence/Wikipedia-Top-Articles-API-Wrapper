from flask import Flask, request, jsonify
import requests, time
from calendar import monthrange
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access"
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # in seconds
headers = {
    "User-Agent": "WikipediaApiWrapper/1.0 (john.doe@gmail.com)"
}


def fetch_data(date):
    url = f"{BASE_URL}/{date.strftime('%Y/%m/%d')}"
    print(url)

    retries = 0
    while retries < MAX_RETRIES:
        response = requests.get(url, headers=headers, timeout=3000, params={
            "action": "query",
            "format": "json"
            })

        if response.status_code == 403:  # Forbidden, probably due to rate limiting
            print("Rate limited. Waiting before retrying...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            retries += 1
        elif response.status_code == 200:  # Success
            try:
                json_response = response.json()
                # Check if the Wikipedia API returned an error
                if 'error' in json_response:
                    return (False, json_response['error'].get('info', 'An error occurred.'))

                return (True, json_response)
            except requests.exceptions.JSONDecodeError:
                print("JSON decode error occurred.")
                return (False, "JSON decode error occurred.")
        else:
            print(f"Unexpected status code: {response.status_code}. Breaking out.")
            return (False, f"Unexpected status code: {response.status_code}")

    return (False, "Max retries reached.")


@app.route('/top-articles/<int:year>/<int:month>/<int:day>')
def top_articles(year, month, day):
    # Parsing the provided date
    try:
        start_date = datetime(year, month, day).date()
    except ValueError:
        return jsonify(error="Invalid date provided."), 400

    # Getting the duration and verifying it
    duration = request.args.get('duration')
    if duration not in ["week", "month"]:
        return jsonify(error="Invalid duration. Please select either 'week' or 'month'."), 400

    # Calculate the end date based on the provided start date and duration
    if duration == "week":
        end_date = start_date + timedelta(weeks=1) - timedelta(days=1)  # Including the start date
    else:
        _, last_day_of_month = monthrange(year, month)
        end_date = datetime(year, month, last_day_of_month).date()  # Set to the last day of the month

    articles = {}
    current_date = start_date
    for current_date in [start_date + timedelta(days=i) for i in range((end_date-start_date).days + 1)]:
        success, result = fetch_data(current_date)
        if not success:
            # Handle the error (result contains the error message)
            return jsonify(error=result), 500
        else:
            # Process the data (result contains the actual data)
            articles_data = result.get('items', [])
            if articles_data:
                for article in articles_data[0].get('articles', []):
                    title = article['article']
                    views = article['views']
                    articles[title] = articles.get(title, 0) + views

    sorted_articles = sorted(articles.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_articles)


@app.route('/article-views/<int:year>/<int:month>/<int:day>')
def article_views(year, month, day):
    # Parsing the provided date
    try:
        start_date = datetime(year, month, day).date()
    except ValueError:
        return jsonify(error="Invalid date provided."), 400

    title = request.args.get('title')
    if not title:
        return jsonify(error="Article title is required."), 400

    duration = request.args.get('duration')
    if duration not in ["week", "month"]:
        return jsonify(error="Invalid duration. Please select either 'week' or 'month'."), 400

    # Calculate the end date based on the provided start date and duration
    if duration == "week":
        end_date = start_date + timedelta(days=6)  # Including the start date
    else:
        end_date = start_date + timedelta(days=29)  # Including the start date

    total_views = 0
    current_date = start_date
    while current_date <= end_date:
        success, result = fetch_data(current_date)
        if not success:
            # Handle the error (result contains the error message)
            return jsonify(error=result), 500
        else:
            # Process the data (result contains the actual data)
            for article in result.get('items', [{}])[0].get('articles', []):
                if article['article'] == title:
                    total_views += article['views']
                    break
            current_date += timedelta(days=1)

    return jsonify({"title": title, "total_views": total_views})


@app.route('/max-views-day/<int:year>/<int:month>')
def max_views_day(year, month):
    # Get the last day of the given month
    _, last_day = monthrange(year, month)
    
    # Define the start and end dates for the entire month
    start_date = datetime(year, month, 1).date()
    end_date = datetime(year, month, last_day).date()

    title = request.args.get('title')
    if not title:
        return jsonify(error="Article title is required."), 400

    max_views = 0
    max_views_date = None
    current_date = start_date
    while current_date <= end_date:
        success, result = fetch_data(current_date)
        if not success:
            # Handle the error (result contains the error message)
            return jsonify(error=result), 500
        else:
            # Process the data (result contains the actual data)
            for article in result.get('items', [{}])[0].get('articles', []):
                if article['article'] == title:
                    views = article['views']
                    if views > max_views:
                        max_views = views
                        max_views_date = current_date
                    break
            current_date += timedelta(days=1)

    return jsonify({
        "title": title,
        "max_views": max_views,
        "max_views_date": max_views_date.strftime('%Y-%m-%d') if max_views_date else None
    })

if __name__ == '__main__':
    app.run(debug=True)
