---
title: Home
hide:
    - navigation
---

# Welcome to the Documentation for `TunGuard`

/// info | This Documentation is Versioned

**Make sure** to select the correct version of this documentation! It should match the version of the image you are using. The default version corresponds to [the most recent stable release][docs-tagging].

///

This documentation provides you not only with the basic setup and configuration of `TunGuard` but also with advanced configuration, elaborate usage scenarios, detailed examples, hints and more.

[docs-tagging]: ./getting-started.md

## About

`TunGuard` is a self-hosted networking platform for connecting remote devices and exposing internal services. One server gives you three things: a direct peer-to-peer mesh between devices, a TCP relay for publishing services that run on them, and a WireGuard-compatible VPN for ordinary client access.

The mesh and the relay are TunGuard's own protocols, not WireGuard. Devices sharing a group key discover each other automatically, punch a direct UDP path through NAT, and fall back to relaying through the server when no direct path can be opened — so traffic leaves the server path as soon as the peers can reach each other. The VPN half still produces standard WireGuard configurations and QR codes for any device that wants one.

Everything runs in userspace, so there are no kernel modules to install, no `apt install wireguard`, and no container runtime. A small client binary keeps unattended devices on the mesh with no local configuration, and a web dashboard and API drive all of it.

## What TunGuard Does

Pick the part that matches what you are building.

- **[P2P Mesh](examples/tutorials/p2p.md)** — devices sharing a group key discover each
  other, punch a direct UDP path through NAT, and relay through the server only when a
  direct path is not possible. TunGuard's own protocol; no VPN involved.
- **[TunGuard Client](guides/client.md)** — one small binary that puts an unattended
  device on the mesh. No config file, no routes, no local state beyond a device id.
- **[VPN Access](guides/clients.md)** — standard WireGuard configurations and QR codes,
  generated from the dashboard for phones, laptops, and routers.
- **[TCP Relay](guides/api.md#tcp-relay-trp)** — publish a service running on a mesh
  node to the internet on a port of your choosing.
- **[Dashboard and API](guides/api.md)** — everything above is drivable from a browser or
  from `curl`.

## Contents

### Getting Started

If you're new to TunGuard, make sure to read the [_Getting Started_ chapter][docs-getting-started] first. If you want to look at examples for a new VPS, we have an [_Examples_ page][docs-examples].

[docs-getting-started]: ./getting-started.md
[docs-examples]: ./examples/tutorials/basic-installation.md

### Contributing

We are always happy to welcome new contributors. For guidelines and entrypoints please have a look at the [Contributing section][docs-contributing].

[docs-contributing]: ./contributing/issues-and-pull-requests.md

### Migration

If you are upgrading from an older version of `TunGuard`, please read the [_Migration_ chapter][docs-migration].

[docs-migration]: ./advanced/migrate/
