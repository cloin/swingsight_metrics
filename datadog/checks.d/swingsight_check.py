from datadog_checks.base import AgentCheck
import requests

class SwingSightCheck(AgentCheck):
    def check(self, instance):
        try:
            # Make a GET request to the Flask application's metrics endpoint
            response = requests.get('http://localhost:5050/metrics')
            response.raise_for_status()
            
            # Parse the plain-text Prometheus-formatted metrics
            metrics_data = self._parse_metrics(response.text)

            # Publish the metrics to Datadog
            for metric_name, value in metrics_data.items():
                # Use the metric name as part of the Datadog metric name
                datadog_metric_name = f'swingsight.{metric_name}'
                self.gauge(datadog_metric_name, value)
        except Exception as e:
            self.log.error(f"Unable to fetch or parse metrics from the Flask application: {str(e)}")

    def _parse_metrics(self, metrics_text):
        """
        Parse Prometheus-formatted metrics from plain-text to a dictionary.
        """
        metrics_data = {}
        lines = metrics_text.strip().split('\n')
        for line in lines:
            # Ignore comments and empty lines
            if line.startswith('#') or not line:
                continue
            parts = line.split(' ')
            if len(parts) == 2:
                metric_name, value = parts
                metrics_data[metric_name] = float(value)
        return metrics_data
