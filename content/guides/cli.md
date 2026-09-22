---
title: CLI
---

TunGuard can be managed directly from the command line or through systemd when installed as a service.

## Install

Install TunGuard on a Linux server with:

```shell
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer installs TunGuard as a systemd service and starts it automatically.

## Service Management

Check the service status:

```shell
sudo systemctl status tanguard
```

Start TunGuard:

```shell
sudo systemctl start tanguard
```

Stop TunGuard:

```shell
sudo systemctl stop tanguard
```

Restart TunGuard:

```shell
sudo systemctl restart tanguard
```

Enable TunGuard to start automatically on boot:

```shell
sudo systemctl enable tanguard
```

## Logs

View the TunGuard service logs:

```shell
sudo journalctl -u tanguard
```

Follow the logs in real time:

```shell
sudo journalctl -u tanguard -f
```

Show logs from the current boot:

```shell
sudo journalctl -u tanguard -b
```

Show the most recent logs:

```shell
sudo journalctl -u tanguard -n 100
```

## Reset Dashboard Credentials

If you forget the dashboard username or password, stop TunGuard first:

```shell
sudo systemctl stop tanguard
```

Run the reset command:

```shell
sudo ./tanguard --reset
```

The reset restores:

```text
Username: admin
Password: tanguard
```

Start TunGuard again:

```shell
sudo systemctl start tanguard
```

The complete procedure is:

```shell
sudo systemctl stop tanguard
sudo ./tanguard --reset
sudo systemctl start tanguard
```

This resets the stored dashboard login without removing the configured peers or other persistent TunGuard data.

## Manual Run

TunGuard can also be started directly from the command line.

```shell
sudo ./tanguard
```

Enable the web dashboard when running manually:

```shell
sudo ./tanguard -web
```

Enable the SSH Gateway:

```shell
sudo ./tanguard -ssh
```

Enable both:

```shell
sudo ./tanguard -web -ssh
```

When using the systemd service installed by the installer, these options are configured through the service configuration rather than being required for normal operation.

## SSH Gateway

The optional SSH Gateway allows you to reach devices connected to TunGuard through the VPN.

The default SSH Gateway port is:

```text
2222
```

For example, to connect to a WireGuard peer at `10.100.0.2`:

```shell
ssh -J admin@YOUR_SERVER_IP:2222 root@10.100.0.2
```

The SSH Gateway uses the TunGuard dashboard credentials for authentication.

The jump host can be used without exposing SSH directly on the VPN device.

## SSH Gateway With a Custom Port

If the SSH Gateway is configured to use another port, specify that port in the jump host:

```shell
ssh -J admin@YOUR_SERVER_IP:CUSTOM_PORT root@10.100.0.2
```

## Check the SSH Gateway

Check whether TunGuard is running:

```shell
sudo systemctl status tanguard
```

Then check that the SSH Gateway is listening on port `2222`:

```shell
sudo ss -lntp | grep 2222
```

## Check the Dashboard/API

The default dashboard and API port is:

```text
9000
```

Check whether TunGuard is listening:

```shell
sudo ss -lntp | grep 9000
```

The health endpoint can be checked locally with:

```shell
curl http://127.0.0.1:9000/api/health
```

## Check the WireGuard Port

The default WireGuard port is:

```text
13231/udp
```

Check whether TunGuard is listening:

```shell
sudo ss -lunp | grep 13231
```

## Update TunGuard

Run the installer again to update an existing installation:

```shell
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer replaces the TunGuard binary while preserving the existing persistent data and service configuration.

## Backup

Create a backup of the TunGuard data directory:

```shell
sudo tar -czf ~/tanguard-backup.tar.gz -C /var/lib/tanguard .
```

The persistent data contains the server key, peer configuration, dashboard credentials, API key, and other TunGuard state.

## Useful Service Commands

A quick reference:

```shell
# Status
sudo systemctl status tanguard

# Start
sudo systemctl start tanguard

# Stop
sudo systemctl stop tanguard

# Restart
sudo systemctl restart tanguard

# Enable at boot
sudo systemctl enable tanguard

# Follow logs
sudo journalctl -u tanguard -f

# Last 100 log entries
sudo journalctl -u tanguard -n 100
```
