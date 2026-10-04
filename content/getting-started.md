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
- `7000/TCP` — P2P control channel, used by the TunGuard client
- `7001/UDP` — P2P rendezvous and relay

`7000/TCP` and `7001/UDP` are only needed if you plan to build a [P2P
mesh](examples/tutorials/p2p.md). They are opened automatically; open them only when
you intend to use them.

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

/// warning | Important Security Step

Until you change them, a dedicated setup page at `http://YOUR_SERVER_IP:9000/login.html`
takes over and asks for new credentials. The dashboard only opens once they are set.

///

---

## Release Versions

TunGuard releases follow [Semantic Versioning](https://semver.org/).

The official release history and release notes are maintained in the [TunGuard binary repository](https://github.com/TunGuard/tanguard-binary).

The documentation site automatically uses release information from the binary repository, so release versions do not need to be manually added to this page.

---

## Follow the Guides

Once TunGuard is installed, continue with the relevant guide:

* [Dashboard](guides/setup.md)
* [Peers](guides/clients.md)
* [P2P Mesh](examples/tutorials/p2p.md)
* [TunGuard Client](guides/client.md)
* [Configuration](advanced/config/conf.md)
* [SSH Gateway](guides/admin.md)
* [API](guides/api.md)
* [Backups](guides/admin.md)

/// note | Updating TunGuard

To update an existing installation, run:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer replaces the binary, keeps your service configuration and your data
directory, and restarts the service.

///

## Install the Client

Devices that join a [P2P mesh](examples/tutorials/p2p.md) also run a small client.
Install it on each device with:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/client.sh | bash
```

Then enroll the device from the dashboard under **P2P → Enroll device** and run the
command it shows you:

```bash
tun YOUR_SERVER_IP YOUR_PSK
```

See [TunGuard Client](guides/client.md) for the full client reference.
