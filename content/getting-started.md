---
title: Getting Started
hide:
    - navigation
---

This page explains how to get started with `TunGuard`. The recommended installation method is the official installer, which installs TunGuard and starts the service automatically.

## Preliminary Steps

Before installing TunGuard, there are some requirements to be met:

1. You need a Linux VPS or server that you can manage
2. You need a public IP address or a hostname that points to your server
3. You need a supported architecture (`amd64` or `arm64`)
4. You need `root` or `sudo` access

### Host Setup

TunGuard runs directly on the host and does not require Docker or another container runtime.

The server should have:

- A supported Linux distribution
- Internet access
- `root` or `sudo` privileges
- UDP port `13231` available for WireGuard
- TCP port `9000` available for the dashboard and API

/// note | VPS Firewall

Make sure your VPS provider's firewall or security group allows the required TunGuard ports.

The default ports are:

- `13231/UDP` — WireGuard
- `9000/TCP` — Dashboard and API
- `2222/TCP` — SSH Gateway, when enabled

///

## Installing TunGuard

### Official Installer

Install the latest stable release with:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer automatically installs TunGuard and starts the service.
There is no need to manually start the web server after installation.

## Open the Dashboard

Once installation is complete, open:

`http://YOUR_SERVER_IP:9000`

For example:

`[http://203.0.113.10:9000](http://203.0.113.10:9000)`

The default login credentials are:

* **Username:** `admin`
* **Password:** `tanguard`

!!! note "Important Security Step"
    You will be required to change the default password after your first login.

---

## Release Versions

TunGuard releases follow [Semantic Versioning](https://semver.org/).

The official release history and release notes are maintained in the [TunGuard binary repository](https://github.com/TunGuard/tanguard-binary).

The documentation site automatically uses release information from the binary repository, so release versions do not need to be manually added to this page.

---

## Follow the Guides

Once TunGuard is installed, continue with the relevant guide:

* [Dashboard](dashboard.md)
* [Peers](peers.md)
* [Configuration](configuration.md)
* [SSH Gateway](ssh-gateway.md)
* [API](api.md)
* [Backups](backups.md)

!!! note "Updating TunGuard"
    To update an existing installation you can click the release button on top right to  update on the dashboard  then for latest stable release, run:

    ```bash
    curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
    ```

    The installer handles the update and restarts the TunGuard service.
