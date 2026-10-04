---
title: Privacy Policy
---

# Privacy Policy

**Last updated:** 2026-10-04

`TunGuard` is software you run yourself. There is no `TunGuard` account, no vendor
holding a copy of your configuration, and no service in the middle. This page
describes exactly what the software stores, what leaves your server, and what
this documentation site does.

/// info | Self-hosted means self-hosted

`TunGuard` collects nothing on your behalf. It has no telemetry, no analytics, no
crash reporting and no advertising identifier. The only server you ever talk to
is the one you installed.

///

## What This Covers

Two separate things, because they behave differently:

| Component | Operator | Who can read your data |
|---|---|---|
| The `TunGuard` server you install | You | You, plus anyone with filesystem or root access to your host |
| This documentation site | The `TunGuard` project | The public, and the search index of your browser |

## The TunGuard Server

### Data stored on your server

Everything lives in your data directory (`DATA_DIR`, `./` by default). Files that
hold secrets are written with `0600` permissions.

| File | Contents |
|---|---|
| `server_private.key` | The server's WireGuard private key. Anyone holding it can impersonate your server. |
| `server_wg_pubkey.txt` | The matching public key, for client configurations. |
| `web_credentials.json` | Dashboard username and a bcrypt password hash. The plaintext password is never written. |
| `api_key.json` | The single API key, with a creation timestamp. |
| `ssh_host_key` | Host key for the optional SSH gateway. |
| `peers.json` | WireGuard peers you add: public key, assigned address, and the device name and device id you supply. |
| `policy_groups.json` | Policy groups and their membership, keyed by public key or device id. |
| `nodes.json` | Mesh nodes: id, name, group key (`PSK`), reported device id, creation time. |
| `proxies.json` | TCP relay mappings: bind address and port, target device, target port. |
| `wg_status.json` | A small status snapshot with your public key, subnet and listen ports. |

No message contents, packet payloads or file contents are written to disk. The
mesh and the VPN carry encrypted traffic, and `TunGuard` does not decrypt or log
what flows through them.

### Log contents

The service log records operational events: which peers were added or removed,
node ids and device ids as they connect and disconnect, policy group names, and
dashboard actions. Three things log a network address: backup downloads and
restores, and SSH gateway connections.

Requests to the dashboard and API are logged with method, path and duration, not
with your IP address or the request body. Passwords, API keys and pre-shared keys
are never logged.

### Outbound requests the software makes

`TunGuard` makes exactly one outbound request of its own:

- **Update check.** When the API starts, and once an hour after that, the server
  performs a `GET` against
  `https://api.github.com/repos/TunGuard/tanguard-binary/releases/latest` to
  compare your build against the newest published release. It sends no data about
  your installation beyond the fact that the request arrived; the destination sees
  your server's IP address, as with any outbound connection. Refreshing the
  version on demand triggers the same request.

If even that is unwanted, keep the dashboard off and block `api.github.com` on
the host. The check is informational; nothing about the server depends on it.

/// note | Traffic between your own devices

Mesh traffic between devices, relay traffic, and VPN traffic go between the
devices and your server, and then peer-to-peer where possible. Your peers' IP
addresses are visible to each other by design — that is what a direct path is.
An operator whose servers sit between relaying peers will see the metadata of
the traffic they relay, but not its contents.

///

### Third-party assets in the dashboard

The dashboard is a page in your browser, and three of its assets are loaded from
third-party CDNs. Your browser connects to those hosts directly, so **they see
your IP address and the fact that you are running `TunGuard`**:

| Host | Used for |
|---|---|
| `fonts.googleapis.com` | Google Fonts (the stylesheet) |
| `cdn.jsdelivr.net` | Chart.js on the dashboard, xterm.js on the SSH page |

The rest of the dashboard, including all of your configuration and every API
response, is served by your own server and goes nowhere else.

To remove those requests, self-host the three assets: edit the stylesheet's
`@import` and the two `<script>` tags to point at local copies under
`webui/`. Nothing in `TunGuard` needs them to function.

### Authentication and browser storage

There are no cookies and no sessions. The dashboard uses HTTP Basic
authentication, and automation uses an API key in the `X-API-Key` or
`Authorization` header. The dashboard stores nothing in `localStorage` or
`sessionStorage`, so clearing your browser data erases it completely.

### Backups

A backup archive contains the files listed above, including
`server_private.key` and the API key. Treat it as a secret: whoever holds it can
reconstruct your server's identity. Restores are validated before anything is
written, and an archive that would break the default policy group is rejected.

### Retention and deletion

There is no data store behind a service that expires anything, because there is
no service. Deleting a peer, node, device or relay mapping removes it from the
server's state at the next save; stopping and deleting `TunGuard` leaves only the
files in your data directory, which you can remove yourself. Rotating the API key
invalidates the old one immediately.

## This Documentation Site

- This site is static HTML published on GitHub Pages. There is no comment system,
  no analytics, and no advertising.
- The version selector is plain client-side JavaScript; it does not report usage.
- The site contains a Google `site-verification` meta tag, which allows Google to
  confirm ownership for Search Console. Verifying ownership does not add
  tracking, cookies or profiling to the site.
- Fonts and any third-party code loaded by the site are subject to those
  providers' own policies, not `TunGuard`'s.
- Search queries you type into the site's search box are handled in your browser.
  Queries are never sent to `TunGuard` or to a search provider.

## Changes to This Policy

This policy is part of the documentation and changes with the software. It is
tracked in the repository alongside the code it describes, so its history is
public and each change is reviewable.

## Contact

Questions about this policy, or a correction to it, belong in the issue tracker
or discussions of the repository:

- Server: [github.com/TunGuard/tanguard-binary](https://github.com/TunGuard/tanguard-binary)
- Documentation: the repository that builds this site