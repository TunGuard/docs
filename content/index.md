---
title: Home
hide:
    - navigation
---

# Welcome to the Documentation for `Tunguard`

/// info | This Documentation is Versioned

**Make sure** to select the correct version of this documentation! It should match the version of the image you are using. The default version corresponds to [the most recent stable release][docs-tagging].

///

This documentation provides you not only with the basic setup and configuration of `Tunguard` but also with advanced configuration, elaborate usage scenarios, detailed examples, hints and more.

[docs-tagging]: ./getting-started.md

## About

`Tunguard` is a lightweight, zero-dependency userspace networking utility designed for high-performance peer-to-peer connectivity and public endpoint exposure. Built around WireGuard's core protocols, TunGuard operates entirely in userspace—eliminating the need to install kernel drivers, run elevated system daemons, or execute system-wide VPN configurations. It allows developers and sysadmins to create secure, instant network overlays and expose internal services across NATs and firewalls seamlessly.

## Contents

### Getting Started

If you're new to Tunguard, make sure to read the [_Getting Started_ chapter][docs-getting-started] first. If you want to look at examples for new vps, we have an [_Examples_ page][docs-examples].

[docs-getting-started]: ./getting-started.md
[docs-examples]: ./examples/tutorials/basic-installation.md

### Contributing

We are always happy to welcome new contributors. For guidelines and entrypoints please have a look at the [Contributing section][docs-contributing].

[docs-contributing]: ./contributing/issues-and-pull-requests.md

### Migration

If you are migrating from an older version of `wg-easy`, please read the [_Migration_ chapter][docs-migration].

[docs-migration]: ./advanced/migrate/
