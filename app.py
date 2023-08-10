from flask import Flask, request, jsonify
import requests, time
from datetime import datetime, timedelta

app = Flask(__name__)

BASE_URL = "https://wikimedia.org/api/rest_v1/metrics/pageviews/top/en.wikipedia/all-access"
MAX_RETRIES = 3
DELAY_BETWEEN_REQUESTS = 2  # in seconds

def fetch_data(date):
    url = f"{BASE_URL}/{date.strftime('%Y/%m/%d')}"
    print(url)

    retries = 0
    while retries < MAX_RETRIES:
        response = requests.get(url)
        print(response)
        print(retries)
        
        if response.status_code == 403:  # Forbidden, probably due to rate limiting
            print("Rate limited. Waiting before retrying...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            retries += 1
        elif response.status_code == 200:  # Success
            try:
                return response.json()
            except requests.exceptions.JSONDecodeError:
                print("JSON decode error occurred.")
                return {}
        else:
            print(f"Unexpected status code: {response.status_code}. Breaking out.")
            break

    return {}

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
        end_date = start_date + timedelta(days=6)  # Including the start date
    else:
        end_date = start_date + timedelta(days=29)  # Including the start date

    articles = {}
    current_date = start_date
    while current_date <= end_date:
        data = fetch_data(current_date)
        print(jsonify(data))
        articles_data = data.get('items', [])
        if articles_data:
            for article in articles_data[0].get('articles', []):

                title = article['article']
                views = article['views']
                articles[title] = articles.get(title, 0) + views
            current_date += timedelta(days=1)

    sorted_articles = sorted(articles.items(), key=lambda x: x[1], reverse=True)
    return jsonify(sorted_articles)


@app.route('/article-views')
def article_views():
    title = request.args.get('title')
    if not title:
        return jsonify(error="Article title is required."), 400

    duration = request.args.get('duration')
    if duration not in ["week", "month"]:
        return jsonify(error="Invalid duration. Please select either 'week' or 'month'."), 400

    # Calculate the start and end dates based on the duration
    end_date = datetime.now().date()
    if duration == "week":
        start_date = end_date - timedelta(days=7)
    else:
        start_date = end_date - timedelta(days=30)

    total_views = 0
    current_date = start_date
    while current_date <= end_date:
        data = fetch_data(current_date)
        for article in data.get('items', [{}])[0].get('articles', []):
            if article['article'] == title:
                total_views += article['views']
                break
        current_date += timedelta(days=1)

    return jsonify({"title": title, "total_views": total_views})

@app.route('/max-views-day')
def max_views_day():
    title = request.args.get('title')
    if not title:
        return jsonify(error="Article title is required."), 400

    duration = request.args.get('duration')
    if duration not in ["week", "month"]:
        return jsonify(error="Invalid duration. Please select either 'week' or 'month'."), 400

    # Calculate the start and end dates based on the duration
    end_date = datetime.now().date()
    if duration == "week":
        start_date = end_date - timedelta(days=7)
    else:
        start_date = end_date - timedelta(days=30)

    max_views = 0
    max_views_date = None
    current_date = start_date
    while current_date <= end_date:
        data = fetch_data(current_date)
        for article in data.get('items', [{}])[0].get('articles', []):
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
