from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Initialize global variables to store the latest metric values
latest_metrics = {
    "angle_of_departure": None,
    "velocity_at_departure": None,
    "projected_yardage": None,
    "projected_zone": None,
    "total_balls_hit": 0,
    "count_zone_1": 0,
    "count_zone_2": 0,
    "count_zone_3": 0
}

@app.route('/golfball-hit', methods=['POST'])
def golfball_hit():
    try:
        # Extract JSON data from the request
        data = request.json
        
        # Extract values from the JSON data
        angle_of_departure = data['angle_of_departure']
        velocity_at_departure = data['velocity_at_departure']
        
        # Calculate projected yardage and zone
        projected_yardage = calculate_projected_yardage(angle_of_departure, velocity_at_departure)
        projected_zone = calculate_projected_zone(projected_yardage)
        
        # Update the latest metric values
        latest_metrics["angle_of_departure"] = angle_of_departure
        latest_metrics["velocity_at_departure"] = velocity_at_departure
        latest_metrics["projected_yardage"] = projected_yardage
        latest_metrics["projected_zone"] = projected_zone
        latest_metrics["total_balls_hit"] += 1  # Increment the total balls hit metric

        # Increment the count for the respective zone
        zone_metric_name = f"count_zone_{projected_zone}"
        latest_metrics[zone_metric_name] += 1
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/swingsight', methods=['GET'])
def dashboard():
    return render_template('swingsight_dashboard.html', **latest_metrics)

@app.route('/metrics', methods=['GET'])
def metrics():
    return jsonify(latest_metrics)

@app.route('/clear-data', methods=['GET'])
def clear_data():
    latest_metrics["angle_of_departure"] = None
    latest_metrics["velocity_at_departure"] = None
    latest_metrics["projected_yardage"] = None
    latest_metrics["projected_zone"] = None
    latest_metrics["total_balls_hit"] = 0
    latest_metrics["count_zone_1"] = 0
    latest_metrics["count_zone_2"] = 0
    latest_metrics["count_zone_3"] = 0
    return jsonify({"status": "success", "message": "All data has been cleared!"}), 200

def calculate_projected_yardage(angle, velocity):
    return velocity * (angle / 90)

def calculate_projected_zone(yardage):
    if yardage < 75:
        return 1
    elif 75 <= yardage < 200:
        return 2
    else:
        return 3

if __name__ == "__main__":
    app.run(debug=True, port=5050)
