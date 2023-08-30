#!/usr/bin/python

DOCUMENTATION = r'''
---
module: prometheus_query
short_description: Fetches latest metric values from Prometheus
description:
    - This module fetches the latest metric values from Prometheus for a given query and time range.
options:
    prometheus_url:
        description:
            - The Prometheus API endpoint URL to fetch metrics.
        required: true
        type: str
    duration_seconds:
        description:
            - The time duration in seconds for which to fetch metrics.
            - Default is 600 seconds (10 minutes).
        default: 600
        type: int
    queries:
        description:
            - List of Prometheus metric queries to fetch.
        required: true
        type: list
        elements: str
requirements:
    - python >= 3.x
    - requests
author:
    - Your Name @your_handle
examples:
    - name: Fetch metrics from Prometheus
      prometheus_query:
        prometheus_url: 'http://prometheus-server:9090'
        queries:
          - 'rate(http_requests_total[5m])'
          - 'up'
return:
    metrics_data:
        description: A dictionary containing the latest values for the queried metrics.
        returned: always
        type: dict
'''

from ansible.module_utils.basic import AnsibleModule
import time
import requests

def fetch_latest_metric_value(query, duration_seconds, prometheus_url):
    """Fetch the latest metric value for a given query."""
    current_time = int(time.time())
    end_time = current_time
    start_time = current_time - duration_seconds
    params = {
        'query': query,
        'time': end_time
    }
    try:
        response = requests.get(f"{prometheus_url}/api/v1/query", params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and 'result' in data['data']:
            metric_data = data['data']['result']
            if metric_data:
                # Explicitly convert to float
                return float(metric_data[0]['value'][1]) if metric_data else None
        else:
            return None
    except Exception as e:
        raise e

def main():
    argument_spec = {
        'prometheus_url': dict(type='str', required=True),
        'duration_seconds': dict(type='int', default=600),
        'queries': dict(type='list', required=True)
    }

    module = AnsibleModule(
        argument_spec=argument_spec,
        supports_check_mode=True
    )

    prometheus_url = module.params['prometheus_url']
    duration_seconds = module.params['duration_seconds']
    queries = module.params['queries']

    metrics_data = {}

    for query in queries:
        try:
            latest_value = fetch_latest_metric_value(query, duration_seconds, prometheus_url)
            if latest_value is not None:
                sanitized_query = query.replace(":", "_").replace(".", "_")
                metrics_data[sanitized_query] = latest_value
            else:
                metrics_data[query] = "No data available for the specified time range."
        except Exception as e:
            module.fail_json(msg=str(e))

    module.exit_json(changed=False, metrics_data=metrics_data)

if __name__ == '__main__':
    main()
