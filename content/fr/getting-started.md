---
title: Getting Started
hide:
    - navigation
---

<svg class="tg-figure" viewBox="0 0 720 170" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="Install TunGuard with the installer, open the dashboard, and connect a device">
  <g class="tg-flow tg-accent" stroke-width="2.4">
    <path d="M190 85h108"/>
    <path d="M420 85h108"/>
  </g>
  <g class="tg-float">
    <circle cx="130" cy="85" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="106" y="70" width="48" height="32" rx="4"/>
    <path class="tg-nudge" d="M114 78l7 7-7 7"/>
    <path class="tg-blink" d="M126 92h20"/>
  </g>
  <g class="tg-float tg-d2">
    <circle class="tg-pulse tg-accent" cx="360" cy="85" r="52" fill="var(--md-default-bg-color)"/>
    <rect x="338" y="58" width="44" height="14" rx="3"/>
    <rect x="338" y="78" width="44" height="14" rx="3"/>
    <rect x="338" y="98" width="44" height="14" rx="3"/>
    <circle class="tg-blink" cx="346" cy="65" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d1" cx="346" cy="85" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d2" cx="346" cy="105" r="1.6" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="590" cy="85" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="576" y="64" width="28" height="42" rx="4"/>
    <circle class="tg-blink" cx="590" cy="97" r="1.6" fill="currentColor" stroke="none"/>
  </g>
</svg>

<p class="tg-cap">Install once, open the dashboard, connect a device.</p>

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
* [AdGuard DNS Filtering](guides/adguard.md)
* [Domains & HTTPS Proxy](guides/domains.md)
* [SSH Access](guides/ssh.md)
* [P2P Mesh](examples/tutorials/p2p.md)
* [TunGuard Client](guides/client.md)
* [Configuration](advanced/config/conf.md)
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
