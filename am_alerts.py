DOCUMENTATION = r'''
module: am_alerts
short_description: Event-Driven Ansible source plugin for Alertmanager alerts
description:
    - Poll Alertmanager API for new alerts
    - Only retrieves alerts that have changed status after the script began executing
    - This script can be tested outside of ansible-rulebook by specifying environment variables for ALERTMANAGER_HOST, ALERTMANAGER_PORT, and INTERVAL
author: "Colin McNaughton @cloin"
options:
    alertmanager_host:
        description:
            - Your Alertmanager host address
        required: true
    alertmanager_port:
        description:
            - Your Alertmanager port number
        required: true
    interval:
        description:
            - The interval, in seconds, at which the script polls the API
        required: false
        default: 10
notes:
    - The script will run indefinitely until manually stopped. To stop the script, use Control-C or any other method of sending an interrupt signal to the process
    - The script uses the aiohttp and asyncio libraries for making HTTP requests and handling asynchronous tasks, respectively. Make sure these libraries are installed in your Python environment before running the script
    - This script is designed for Python 3.7 and above due to the usage of the asyncio library. Please ensure you are using an appropriate version of Python
'''

EXAMPLES = r'''
- name: Respond to Alertmanager alerts
  hosts: all
  sources:
    - your_namespace.alertmanager.am_alerts:
        alertmanager_host: 'localhost'
        alertmanager_port: '9093'
        interval: 10
  rules:
    - name: Catch all Alertmanager alerts
      condition: event.labels.alertname is defined
      action:
        debug:
'''

import aiohttp
import asyncio
import os

async def fetch_alertmanager_alerts(session, am_url):
    async with session.get(am_url) as response:
        return await response.json()

async def main(queue: asyncio.Queue, args: dict):
    interval = int(args.get("interval", 10))
    am_host = args.get("alertmanager_host")
    am_port = args.get("alertmanager_port")
    am_url = f"http://{am_host}:{am_port}/api/v2/alerts"

    async with aiohttp.ClientSession() as session:
        known_alerts = set()  # keep track of known alerts

        while True:
            alerts = await fetch_alertmanager_alerts(session, am_url)
            
            for alert in alerts:
                alert_id = (alert['labels']['alertname'], alert['status']['state'])
                if alert_id not in known_alerts:
                    await queue.put(alert)  # put the alert in the queue
                    known_alerts.add(alert_id)

            await asyncio.sleep(interval)  # wait for interval seconds

if __name__ == "__main__":
    ALERTMANAGER_HOST = os.getenv("ALERTMANAGER_HOST", "localhost")
    ALERTMANAGER_PORT = os.getenv("ALERTMANAGER_PORT", "9093")
    INTERVAL = os.getenv("INTERVAL", "10")

    class MockQueue:
        async def put(self, event):
            print(event)

    args = {
        "alertmanager_host": ALERTMANAGER_HOST,
        "alertmanager_port": ALERTMANAGER_PORT,
        "interval": INTERVAL,
    }
    asyncio.run(main(MockQueue(), args))
