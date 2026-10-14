---
title: Home
hide:
    - navigation
---

/// note | Traduction en cours
Cette traduction est en cours. Certaines pages peuvent encore être en anglais.
///

# Welcome to the Documentation for `TunGuard`

<svg class="tg-figure" viewBox="0 0 720 300" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="TunGuard connects laptops, phones, cloud, edge and AI through one userspace control plane">
  <g class="tg-flow tg-accent" stroke-width="2.2" opacity=".9">
    <path d="M360 150 140 70"/>
    <path d="M360 150 120 230"/>
    <path d="M360 150 580 70"/>
    <path d="M360 150 600 230"/>
    <path d="M360 150 360 44"/>
    <path d="M360 150 360 256"/>
  </g>
  <circle class="tg-ripple tg-accent" cx="360" cy="150" r="52" stroke-width="2" opacity=".5"/>
  <circle class="tg-ripple tg-accent tg-d2" cx="360" cy="150" r="52" stroke-width="2" opacity=".5"/>
  <g class="tg-float">
    <rect x="318" y="108" width="84" height="84" rx="18" fill="var(--md-default-bg-color)"/>
    <path class="tg-draw tg-accent" style="--tg-len:40" d="M340 150l13 13 27-30"/>
  </g>
  <g class="tg-float tg-d2">
    <circle cx="140" cy="70" r="26" fill="var(--md-default-bg-color)"/>
    <path d="M128 64h24v13h-24z M124 81h32"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="120" cy="230" r="26" fill="var(--md-default-bg-color)"/>
    <rect x="111" y="217" width="18" height="26" rx="3"/>
    <circle class="tg-blink" cx="120" cy="237" r="1.7" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d1">
    <circle cx="580" cy="70" r="26" fill="var(--md-default-bg-color)"/>
    <path d="M567 76a8 8 0 0 1 1-15 10 10 0 0 1 18-2 6.5 6.5 0 0 1 1 13z"/>
  </g>
  <g class="tg-float tg-d4">
    <circle cx="600" cy="230" r="26" fill="var(--md-default-bg-color)"/>
    <rect x="590" y="220" width="20" height="20" rx="3"/>
    <path d="M594 220v-4M600 220v-4M606 220v-4M594 244v4M600 244v4M606 244v4"/>
  </g>
  <g class="tg-float tg-d1">
    <circle cx="360" cy="44" r="26" fill="var(--md-default-bg-color)"/>
    <path d="M348 44h8l4-8 4 16 4-8h8"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="360" cy="256" r="26" fill="var(--md-default-bg-color)"/>
    <path d="M350 250h20M350 256h20M350 262h20"/>
  </g>
</svg>

<p class="tg-cap">One userspace control plane connects people, cloud, edge devices and AI workloads.</p>

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

- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle class="tg-blink" cx="12" cy="5" r="2.4" fill="currentColor" stroke="none"/><circle class="tg-blink tg-d1" cx="5" cy="18" r="2.4" fill="currentColor" stroke="none"/><circle class="tg-blink tg-d2" cx="19" cy="18" r="2.4" fill="currentColor" stroke="none"/><path class="tg-flow" d="M12 7 6 16M12 7l6 9M7 18h10"/></svg> **[P2P Mesh](examples/tutorials/p2p.md)** — devices sharing a group key discover each
  other, punch a direct UDP path through NAT, and relay through the server only when a
  direct path is not possible. TunGuard's own protocol; no VPN involved.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="5" y="5" width="14" height="14" rx="2"/><path d="M9 2v3M15 2v3M9 19v3M15 19v3M2 9h3M2 15h3M19 9h3M19 15h3"/><circle class="tg-blink" cx="12" cy="12" r="2" fill="currentColor" stroke="none"/></svg> **[TunGuard Client](guides/client.md)** — one small binary that puts an unattended
  device on the mesh. No config file, no routes, no local state beyond a device id.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 3.5V12c0 4.6-3.4 8.5-8 10-4.6-1.5-8-5.4-8-10V5.5L12 2z"/><path class="tg-draw" style="--tg-len:14" d="M8.5 12l2.4 2.4 4.6-5"/></svg> **[VPN Access](guides/clients.md)** — standard WireGuard configurations and QR codes,
  generated from the dashboard for phones, laptops, and routers.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l8 3.5V12c0 4.6-3.4 8.5-8 10-4.6-1.5-8-5.4-8-10V5.5L12 2z"/><path d="M8 8h8l-3 4v4h-2v-4L8 8z"/></svg> **[AdGuard DNS Filtering](guides/adguard.md)** — a managed AdGuard Home instance that
  filters DNS for devices in an AdGuard-enabled policy group, enforced on the server,
  so moving a device into the group protects it immediately. The same filter can be
  published as a public DNS resolver.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><g class="tg-spin"><ellipse cx="12" cy="12" rx="3.6" ry="9"/></g><path d="M3 12h18"/></svg> **[Domains & HTTPS Proxy](guides/domains.md)** — put a public domain with automatic
  Let's Encrypt HTTPS in front of a TRP mapping or a tunneled service, or map it as a
  public DNS-over-HTTPS and DNS-over-TLS resolver.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="2.5" y="4" width="19" height="16" rx="2.5"/><path class="tg-nudge" d="M6 9l3 3-3 3"/><path class="tg-blink" d="M12 15h6"/></svg> **[SSH Access](guides/ssh.md)** — jump host, browser SSH terminals, and a built-in
  `ssh` client, all using your dashboard login.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><rect x="3" y="4" width="18" height="6" rx="2"/><rect x="3" y="14" width="18" height="6" rx="2"/><circle class="tg-blink" cx="6.5" cy="7" r="1.1" fill="currentColor" stroke="none"/><circle class="tg-blink tg-d1" cx="6.5" cy="17" r="1.1" fill="currentColor" stroke="none"/><path class="tg-flow" d="M14 7h4M14 17h4"/></svg> **[TCP Relay](guides/api.md#tcp-relay-trp)** — publish a service running on a mesh
  node to the internet on a port of your choosing.
- <svg class="tg-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M9 4C6 4 7 10 4 12c3 2 2 8 5 8"/><path d="M15 4c3 0 2 6 5 8-3 2-2 8-5 8"/><circle class="tg-blink" cx="12" cy="12" r="1.4" fill="currentColor" stroke="none"/></svg> **[Dashboard and API](guides/api.md)** — everything above is drivable from a browser or
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

### Privacy

`TunGuard` is self-hosted and collects nothing on your behalf. The [_Privacy Policy_][docs-privacy]
spells out exactly what the server stores, which two third-party CDNs the dashboard
loads assets from, and what this documentation site does.

[docs-privacy]: ./privacy.md
