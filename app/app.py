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
        data = request.json
        
        angle = data['angle_of_departure']
        velocity = data['velocity_at_departure']
        
        yardage = calculate_projected_yardage(angle, velocity)
        zone = calculate_projected_zone(yardage)
        
        latest_metrics["angle_of_departure"] = angle
        latest_metrics["velocity_at_departure"] = velocity
        latest_metrics["projected_yardage"] = yardage
        latest_metrics["projected_zone"] = zone
        latest_metrics["total_balls_hit"] += 1

        zone_metric_name = f"count_zone_{zone}"
        latest_metrics[zone_metric_name] += 1
        
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/', methods=['GET'])
def dashboard():
    return render_template('swingsight_dashboard.html', **latest_metrics)

@app.route('/metrics', methods=['GET'])
def metrics():
    output = []

    output.append("# TYPE angle_of_departure gauge")
    output.append("# TYPE velocity_at_departure gauge")
    output.append("# TYPE projected_yardage gauge")
    output.append("# TYPE projected_zone gauge")
    output.append("# TYPE total_balls_hit counter")
    output.append("# TYPE count_zone_1 counter")
    output.append("# TYPE count_zone_2 counter")
    output.append("# TYPE count_zone_3 counter")

    for key, value in latest_metrics.items():
        if value is not None:
            output.append(f"{key} {value}")

    return '\n'.join(output), 200, {"Content-Type": "text/plain"}



@app.route('/clear-data', methods=['GET'])
def clear_data():
    latest_metrics.update({
        "angle_of_departure": None,
        "velocity_at_departure": None,
        "projected_yardage": None,
        "projected_zone": None,
        "total_balls_hit": 0,
        "count_zone_1": 0,
        "count_zone_2": 0,
        "count_zone_3": 0
    })
    return jsonify({"status": "success", "message": "All data has been cleared!"}), 200

def calculate_projected_yardage(angle, velocity):
    return velocity * (angle / 90)

def calculate_projected_zone(yardage):
    if yardage < 75:
        return 1
    elif yardage >= 75 and yardage < 280:
        return 2
    else:
        return 3

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=5050)
