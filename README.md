# Wikipedia Top Articles API Wrapper

This application is a wrapper for the Wikipedia API, fetching top articles and their respective views for given dates and durations.

## Features:

1. Fetch top articles for a specific date and duration (week or month).
2. Retrieve the total views for a specific article on a given date and duration.
3. Find out the day of the month when an article got the most page views.

## Requirements:
- Flask
- requests

## Setup:

1. Install the required libraries using pip:

```
pip install Flask requests
```

2. Run the application:

```
python app.py
```

The application will start and listen on the default Flask port (5000).

## API Endpoints:

### 1. `/top-articles/<int:year>/<int:month>/<int:day>`

Returns the top articles for a specific date and duration (week or month).

#### Test Cases:

- **Valid Request**:
  - Endpoint: `/top-articles/2015/10/10?duration=week`
  - Expected Response: List of top articles for the week starting from 10th October 2010.

- **Invalid Date**:
  - Endpoint: `/top-articles/2015/10/10?duration=week`
  - Expected Response: `{"error": "Invalid date provided."}` with 400 status.

- **Invalid Duration**:
  - Endpoint: `/top-articles/2015/10/10?duration=year`
  - Expected Response: `{"error": "Invalid duration. Please select either 'week' or 'month'."}` with 400 status.

### 2. `/article-views/<int:year>/<int:month>/<int:day>`

Returns the total views for a specific article on a given date and duration.

#### Test Cases:

- **Valid Request**:
  - Endpoint: `/article-views/2015/10/10?title=Python&duration=month`
  - Expected Response: Total views of the article "Python" for the month of October 2015.

- **No Article Title**:
  - Endpoint: `/article-views/2015/10/10?duration=month`
  - Expected Response: `{"error": "Article title is required."}` with 400 status.

### 3. `/max-views-day/<int:year>/<int:month>`

Find out the day of the month where a specific article got the most page views.

#### Test Cases:

- **Valid Request**:
  - Endpoint: `/max-views-day/2015/10?title=Python`
  - Expected Response: Day of October 2015 where the article "Python" got the most page views.

- **No Article Title**:
  - Endpoint: `/max-views-day/2015/10`
  - Expected Response: `{"error": "Article title is required."}` with 400 status.

## Notes:

- Ensure that the `User-Agent` header in the `headers` dictionary is modified to reflect your information or the application's user agent.
- Make sure not to send too many requests in a short span to avoid rate limits. Adjust `MAX_RETRIES` and `DELAY_BETWEEN_REQUESTS` accordingly.

## Future Enhancements:

- Implement caching to store frequently accessed data and reduce API calls.
- Add more detailed logging and error handling mechanisms.
- Implement more filters and sorts for the articles' data.

## Author
Jarod Florence
jarod.a.florence@gmail.com