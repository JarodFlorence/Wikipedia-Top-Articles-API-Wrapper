# Grow Therapy Wikipedia API Wrapper

This Flask-based web application provides a wrapper around the Wikipedia Pageviews API to retrieve article views data for specified durations.

## Requirements:
- Flask
- requests

## Installation & Running:

1. Clone the repository.
2. Install the required libraries:
    ```bash
    pip install Flask requests
    ```

3. Run the Flask application:
    ```bash
    python app.py
    ```

## API Endpoints:

### 1. Top Articles
Fetches the top articles for a given date and specified duration (`week` or `month`).

**Endpoint:** `/top-articles/<int:year>/<int:month>/<int:day>`

**Parameters:**
- `year`, `month`, `day`: The starting date from which the articles will be fetched.
- `duration`: Either `week` or `month` to specify the range.

**Usage:**
```
/top-articles/2015/10/10?duration=week
```

### 2. Article Views
Retrieves the view count for a specific article over a given duration (`week` or `month`).

**Endpoint:** `/article-views`

**Parameters:**
- `title`: The title of the article.
- `duration`: Either `week` or `month` to specify the range.

**Usage:**
```
/article-views?title=Napoleon&duration=week
```

### 3. Max Views Day
Finds the day within a given duration (`week` or `month`) when a specific article got the most page views.

**Endpoint:** `/max-views-day`

**Parameters:**
- `title`: The title of the article.
- `duration`: Either `week` or `month` to specify the range.

**Usage:**
```
/max-views-day?title=Napoleon&duration=week
```

## Notes:
- The application fetches data from the Wikipedia Pageviews API. There might be rate limits applied, so if you're fetching data for a longer duration, it might take some time.
- Ensure you're querying dates for which Wikipedia has relevant data.

## Future Improvements:
- Implement caching mechanisms to store data and avoid repeated requests to the Wikipedia API.
- Enhance error handling to address possible data-fetching issues.
- Extend the API to cater for more functionalities and possibly other Wikimedia data.

## Feedback:
For any feedback or issues, please raise a ticket or send an email. Contributions are also welcomed through pull requests.

To run this application:

```
flask --debug run
```
