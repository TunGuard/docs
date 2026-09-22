---
title: Monitoring
---

TunGuard includes built-in monitoring in the web dashboard.

The monitoring system provides an overview of server resources, WireGuard activity, and peer connection status without requiring an external monitoring service.

## Dashboard Monitoring

Open the TunGuard dashboard and use the monitoring information shown on the dashboard.

The dashboard can display information such as:

- CPU usage
- Memory usage
- Disk usage
- Network activity
- WireGuard status
- Peer status
- Peer handshakes
- Peer transfer statistics
- Connection activity

Monitoring data is collected by TunGuard and displayed directly in the dashboard.

## System Monitoring

TunGuard monitors the server running the VPN service.

System information can include:

```text
CPU
Memory
Disk
Network
```

This allows you to quickly identify resource or capacity issues without installing additional monitoring software.

## Peer Monitoring

TunGuard also monitors WireGuard peers.

Peer information can include:

```text
Peer
Address
Endpoint
Latest Handshake
Transfer
Status
```

The latest handshake can be used to determine whether a peer is actively communicating with the server.

## Peer Status

TunGuard can identify peers that have not communicated recently.

For example, a peer may appear as stale when its latest handshake exceeds the configured monitoring threshold.

This helps identify devices that are offline, disconnected, or no longer communicating with the server.

## Graphs

TunGuard provides graphs for monitoring server and network activity over time.

Use the graphs to inspect changes in:

- CPU usage
- Memory usage
- Network traffic
- WireGuard traffic
- Peer activity

Graphs are useful for identifying traffic increases, resource usage patterns, and changes in peer activity.

## API Monitoring

Monitoring information can also be accessed programmatically through the TunGuard API.

The health endpoint can be used for simple availability checks:

```sh
curl http://127.0.0.1:9000/api/health
```

The server status endpoint provides authenticated server information:

```sh
curl \
  -u admin:PASSWORD \
  http://127.0.0.1:9000/api/status
```

API key authentication can also be used:

```sh
curl \
  -H "X-API-Key: YOUR_API_KEY" \
  http://127.0.0.1:9000/api/status
```

See the [API](../api.md) documentation for available endpoints and authentication.

## Service Logs

For detailed events that are not represented in the dashboard, use the systemd logs:

```sh
journalctl -u tanguard -f
```

View recent logs:

```sh
journalctl -u tanguard -n 100
```

## External Monitoring

External monitoring is optional.

You can use `/api/health` with an uptime monitoring service or load balancer when you need monitoring outside the TunGuard dashboard.

TunGuard's built-in monitoring does not require Prometheus or Grafana.
