# SwingSight Metrics Datadog check

This Datadog check integrates with the SwingSight Flask application to fetch and monitor golf-related metrics.

## Overview

The SwingSight Datadog Check collects various golf metrics from the SwingSight Flask application and publishes them to Datadog for monitoring and visualization.

## Metrics Collected

- **swingsight.angle_of_departure**: The angle at which the golf ball departs.
- **swingsight.velocity_at_departure**: The speed of the golf ball upon departure.
- **swingsight.projected_yardage**: Estimated distance the golf ball will travel.
- **swingsight.projected_zone**: Categorized zone based on projected yardage.
- **swingsight.total_balls_hit**: A count of the total number of balls hit.
- **swingsight.count_zone_1**: Count of balls that land in zone 1.
- **swingsight.count_zone_2**: Count of balls that land in zone 2.
- **swingsight.count_zone_3**: Count of balls that land in zone 3.

## Setup

1. Ensure the Datadog Agent is installed on the host where the SwingSight Flask application runs.
   
2. Place the `SwingSightCheck` Python class in the Datadog Agent's `checks.d` directory.

3. Configure the check by creating a configuration YAML file in the Agent's `conf.d` directory.

4. Restart the Datadog Agent.

## Configuration

A sample configuration might look like:

```yaml
init_config:
instances:
  - min_collection_interval: 30 # seconds
```

This configuration specifies the interval between consecutive metric collection runs.

## Troubleshooting

### Verifying the Check

To verify that the `SwingSightCheck` is running correctly, you can use the following command:

```bash
datadog-agent status | grep SwingSightCheck
```

This command will show the status of the `SwingSightCheck`. If it's running correctly, you should see output indicating that the check has run without errors.

If you encounter issues with the Datadog check, inspect the Datadog Agent logs for error messages from the `SwingSightCheck`.
