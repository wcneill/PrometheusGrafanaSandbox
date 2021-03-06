# Prometheus - Grafana Sandbox

A sample `Python -> Prometheus -> Grafana` pipeline that includes integration of Slack alerts via webhooks. 

This repo contains a single, simple python module. This module contains a single function designed to imitate a stream of sensor data measuring tides and/or sea level with some gaussian latency. 

The metrics being exposed to the Prometheus server are:
- `current_sea_level`: A Prometheus `Gauge` style metric.
- `current_tide_direction`: Also a `Gauge` metric, but with 4 possible discrete values. `{Low: -2, Outgoing: -1, Incoming: 1, High: 2}`
- `latency_histogram`: A Prometheus `Histogram` style metric, that measures the latency of each tide measurement (simulated by `time.sleep(random.randomnormal(.3, .1))`).

## Instructions
Instructions to get started.

### Installation:
1. Install Prometheus AND Alertmanager following the directions at www.prometheus.io
2. Install Grafana (local version, not cloud), following the directions at www.grafana.com
### Configuration:
1. In the prometheus installation directory, replace the `prometheus.yml` file with the one found in this repo. Back the original up, if you'd like. 
2. Also add the `rules.yml` file to the prometheus install directory.
3. In the alertmanager installation directory, replace `alertmanager.yml` with the version found in this repo. Back the original up, if you'd like. 
### Startup
1. Run `main.py` to begin exposing "sea level" metrics on port 8000.
2. In the command line, `cd` to your prometheus install directory.
3. Start prometheus server: `./prometheus --config.file=prometheus.yml` 
4. In the command line, `cd` to your alertmanager install directory.
5. Start the alert manager server: `./alertmanager --config.file=alertmanager.yml`
6. Start Grafana. 
    a. On windows, navigate to localhost:3000 and follow the directions.
    b. On macOS, run `brew services start grafana` from anywhere.
## Queries and Visualization
A section on how to see the data being generated by `main.py` via the Prometheus database that is now recording that data.
### Prometheus UI: localhost:9090
The prometheus server that you started hosts a simple UI where you can query the database where the sea level data is being collected. You may also generate simple visualizations of these queries or view alerts. 
### Alertmanager: localhost:9093
In order to get alertmanager up and running, you will have to install the "Incoming WebHooks" plugin on Slack. You will need to provide the slack api URL for this plugin in the `alertmanager.yml` file, along with the channel you wish notifications to be pushed to. 

The alertmanager is currently only pushing the first extreme high tide alert for an unknown reason. 
### Grafana: localhost:3000
Sign into Grafana on your machine and login (initial username and password are "admin"). From here, you may query the prometheus database to make more advanced visualizations or entire dashboards. 






