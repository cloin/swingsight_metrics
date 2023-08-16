from datadog_checks.base import AgentCheck
import requests

class SwingSightCheck(AgentCheck):
    def check(self, instance):
        try:
            # Make a GET request to the Flask application's dashboard endpoint
            response = requests.get('http://localhost:5050/metrics')
            response.raise_for_status()
            
            # Extract metrics from the Flask application's response
            data = response.json()

            # Publish the metrics to Datadog
            self.gauge('swingsight.angle_of_departure', data['angle_of_departure'])
            self.gauge('swingsight.velocity_at_departure', data['velocity_at_departure'])
            self.gauge('swingsight.projected_yardage', data['projected_yardage'])
            self.gauge('swingsight.projected_zone', data['projected_zone'])
            self.gauge('swingsight.total_balls_hit', data['total_balls_hit'])
            self.gauge('swingsight.count_zone_1', data['count_zone_1'])
            self.gauge('swingsight.count_zone_2', data['count_zone_2'])
            self.gauge('swingsight.count_zone_3', data['count_zone_3'])
        except Exception as e:
            self.log.error(f"Unable to fetch metrics from the Flask application: {str(e)}")
