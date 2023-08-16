# SwingSight Metrics

SwingSight is a Flask-based application that calculates and tracks various golf-related metrics, such as the angle of departure, velocity at departure, and projected yardage.

## Features

- Capture metrics related to golf swings.
- Dynamically update and display metrics on a dashboard.
- Offer a metrics endpoint for easy integration with monitoring tools.
- Clear all recorded data with a single endpoint.

## Metrics Tracked

- **Angle of Departure**: The angle at which the golf ball departs.
- **Velocity at Departure**: The speed of the golf ball upon departure.
- **Projected Yardage**: Estimated distance the golf ball will travel.
- **Projected Zone**: Categorized zone based on projected yardage.
- **Total Balls Hit**: A count of the total number of balls hit.
- **Zone Counts**: Count of balls that land in each of the zones (1, 2, and 3).

## Endpoints

- `POST /golfball-hit`: Accepts metrics related to a golf swing and updates the internal metrics.
- `GET /swingsight`: Returns a dashboard displaying the latest metrics.
- `GET /metrics`: Provides a JSON response with all the latest metrics.
- `GET /clear-data`: Resets all metrics to their initial state.

## Setup

1. Ensure you have Flask installed. If not, you can install it using:

   ```bash
   pip install Flask
   ```

2. Clone this repository and navigate to the project directory.

3. Run the application:

   ```bash
   python app.py
   ```

4. The application will be accessible at `http://localhost:5050`.
