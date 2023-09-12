# Monitoring and Automation Stack with Podman Compose

This repository provides a Podman compose stack for setting up a monitoring and automation stack consisting of Prometheus, Alertmanager, Grafana, SwingSight Metrics and the Event-Driven Ansible CLI `ansible-rulebook`

## Table of Contents

- [Requirements](#requirements)
- [Quick Start](#quick-start)
- [Services](#services)
  - [Prometheus](#prometheus)
  - [Alertmanager](#alertmanager)
  - [Grafana](#grafana)
  - [Swingsight](#swingsight)
  - [Ansible-Rulebook](#ansible-rulebook)
- [Configuration](#configuration)
- [Respond to SSL certificate expiration](#respond-to-ssl-certificate-expiration)
- [Troubleshooting](#troubleshooting)

## Requirements

- Podman
- Podman Compose

## Quick Start

1. Clone the repository.
    ```bash
    git clone <repository_url>
    ```

2. Navigate to the directory containing the `podman-compose.yml` file.
    ```bash
    cd prometheus
    ```

3. Start the services.
    ```bash
    podman-compose -f podman-compose up -d
    ```


## Services

### Prometheus

- **Port**: 9090
- **Configuration**: `./prometheus.yml`
- **Alert Rules**: `./alert.rules`

Prometheus is configured to run as root and has access to custom configuration and alert rule files. The alert is configured to fire when total_balls_hit exceeds 10.

### Alertmanager

- **Port**: 9093
- **Configuration**: `./alertmanager/alertmanager.yml`

Alertmanager handles alerts sent by Prometheus.

### Grafana

- **Port**: 3000
- **Data Sources**: `./grafana/datasources`
- **Dashboards**: `./grafana/dashboards`

Grafana is configured to run in anonymous mode with Admin role. User/pass is admin/admin. Default dashboard has been created for SwingSight Metrics.

### Swingsight

- **Port**: 5050
- **Build Context**: `../app`
  
SwingSight Metrics application.

### Ansible-Rulebook

- **Container Name**: ansible-rulebook
- **Dependencies**: Depends on Alertmanager.
- **Volumes**: Rulebooks at `../rulebooks` and playbooks at `../playbooks`.

Runs Ansible rulebook against alertmanager using new alerts as events to execute automated response based on event payload.

## Configuration

- **Prometheus**: Edit `./prometheus.yml` and `./alert.rules` to customize Prometheus settings and alerting rules.
- **Alertmanager**: Edit `./alertmanager/alertmanager.yml` to customize webhook receiver.
- **Grafana**: Datasources and dashboards can be added in `./grafana/datasources` and `./grafana/dashboards` respectively.
- **Swingsight**: Modify the `ContainerFile` in the `../app` directory for custom settings.
- **ansible-rulebook**: Customize rulebooks in `../rulebooks` and playbooks in `../playbooks`.

## Respond to SSL certificate expiration

### Prometheus Configuration (`prometheus.yml`)

1. **Scrape Configuration for Swingsight App**: Prometheus is configured to scrape metrics directly from the Swingsight app at port 5050 using HTTPS. This is specified under `scrape_configs` with the job name `swingsight_app`.

    ```yaml
    scrape_configs:
      - job_name: 'swingsight_app'
        scheme: https
        ...
        static_configs:
          - targets: ['swingsight:5050']
    ```

2. **Scrape Configuration for Blackbox Exporter**: Another `scrape_configs` entry is set up to interact with Blackbox Exporter. Prometheus will request Blackbox Exporter to perform SSL certificate checks on the Swingsight app, and then scrape the metrics from Blackbox Exporter.

    ```yaml
    scrape_configs:
      - job_name: 'blackbox'
        ...
        static_configs:
          - targets:
            - 'swingsight:5050'
    ```

3. **Alerting**: Prometheus is configured to send alerts to Alertmanager. If any of the metrics cross a certain threshold (defined in `alert.rules`), an alert will be triggered.

### Blackbox Exporter Configuration (`blackbox.yml`)

1. **SSL Expiry Module**: In the Blackbox Exporter configuration, a module called `ssl_expiry` is defined to check SSL certificate expiration metrics.

    ```yaml
    modules:
      ssl_expiry:
        prober: tcp
        tcp:
          tls: true
          ...
    ```

### How They Work Together

1. **Metric Scraping**: When Prometheus executes its scrape based on the interval, it asks Blackbox Exporter to probe the Swingsight app using the `ssl_expiry` module, which checks SSL certificate expiration.
  
2. **Probing**: Blackbox Exporter performs the SSL expiry check on the Swingsight app and exposes the metrics at its own endpoint (`blackbox_exporter:9115`).

3. **Metric Collection**: Prometheus collects these metrics from Blackbox Exporter and stores them. If the SSL metrics cross certain thresholds defined in the alerting rules, Prometheus triggers an alert and sends it to Alertmanager, as specified in the configuration.

4. **Alerting**: If an alert is triggered, Prometheus sends it to Alertmanager (`alertmanager:9093`), which can then notify via the configured alerting channels.


## Troubleshooting

For any issues or troubleshooting, you can:

- Check the logs for each service:
    ```bash
    podman logs <container_name>
    ```
  