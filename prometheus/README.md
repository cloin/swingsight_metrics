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

## Troubleshooting

For any issues or troubleshooting, you can:

- Check the logs for each service:
    ```bash
    podman logs <container_name>
    ```
  