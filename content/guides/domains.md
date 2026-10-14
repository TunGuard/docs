---
title: Domains & HTTPS Proxy
---

<svg class="tg-figure" viewBox="0 0 720 190" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="A domain is secured with automatic HTTPS and can serve a public DoH endpoint on 443 and a DoT endpoint on 853">
  <g class="tg-flow tg-accent" stroke-width="2.4">
    <path d="M446 80h54"/>
    <path d="M446 110h54"/>
    <path d="M220 95h120"/>
  </g>
  <g class="tg-float">
    <circle cx="140" cy="95" r="46" fill="var(--md-default-bg-color)"/>
    <circle cx="140" cy="95" r="26"/>
    <g class="tg-spin"><ellipse cx="140" cy="95" rx="11" ry="26"/></g>
    <path d="M114 95h52"/>
    <path d="M120 79h40M120 111h40" opacity=".55"/>
  </g>
  <g class="tg-float tg-d2">
    <circle cx="390" cy="95" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="372" y="88" width="36" height="28" rx="5"/>
    <path d="M380 88v-7a10 10 0 0 1 20 0v7"/>
    <circle class="tg-blink" cx="390" cy="101" r="2" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d3">
    <rect x="500" y="52" width="170" height="40" rx="10" fill="var(--md-default-bg-color)"/>
    <text x="585" y="77" text-anchor="middle" font-size="15" fill="currentColor" stroke="none" font-family="ui-monospace,monospace">DoH :443</text>
  </g>
  <g class="tg-float tg-d4">
    <rect x="500" y="104" width="170" height="40" rx="10" fill="var(--md-default-bg-color)"/>
    <text x="585" y="129" text-anchor="middle" font-size="15" fill="currentColor" stroke="none" font-family="ui-monospace,monospace">DoT :853</text>
  </g>
</svg>

<p class="tg-cap">Automatic HTTPS on your domain, plus an optional public DoH + DoT resolver.</p>

TunGuard can publish an internal service on a public domain with HTTPS handled
automatically. You point a domain at the server and choose the service behind
it; TunGuard terminates TLS with a Let's Encrypt certificate and proxies to
that service.

The same mapping can also turn a domain into a **public DNS resolver** that
serves DNS-over-HTTPS (DoH) and DNS-over-TLS (DoT) backed by the managed
[AdGuard Home](adguard.md) filter. See
[Serving a public DNS resolver](#serving-a-public-dns-resolver-doh-dot).

The domain proxy is **on by default** but does nothing until you add a mapping
— it binds no ports and makes no certificate request until the first domain is
configured. Disable it entirely with `DOMAIN_ENABLED=false`.

## What a mapping is

A domain mapping connects one public hostname to a backend reachable **from the
server**:

| Backend | Target | Typical use |
|---|---|---|
| **TRP** (`trp`) | An existing [TCP relay (TRP)](../guides/api.md#tcp-relay-trp) port mapping | A service running on a P2P mesh node, exposed through a TRP mapping |
| **WireGuard** (`wg`) | `IP:port` of a tunneled service | An app running on a WireGuard peer (or any address the server can reach) |
| **DNS** (`dns`) | The managed AdGuard Home resolver | A public, filtered DoH + DoT resolver (like `dns.adguard.com`) |

Example TRP mapping — publish a node's SSH:

```text
trp add edge-a 18022 127.0.0.1 8022
# returns a mapping id, e.g. "3"
```

then:

```text
domain add shell.example.com --trp 3
```

Example WireGuard backend — publish an app on the peer `10.100.0.2`:

```text
domain add app.example.com --wg 10.100.0.2 8080
```

The backend is always spoken to over **plain HTTP** — TLS is terminated at
TunGuard (or the webserver it manages). There is no TLS passthrough. The
original `Host` header is preserved to the backend, and
`X-Forwarded-For`/`X-Forwarded-Proto: https` are added, so an app that cares
about the incoming hostname sees `app.example.com`.

## HTTPS with Let's Encrypt

Certificates come from **Let's Encrypt** automatically using the **HTTP-01**
challenge. There is no self-signed mode and no manual certificate files for
domains.

For that to work:

1. Your domain's **A** (and AAAA, if used) record must point at the server.
2. Ports **80** and **443** must be reachable on the server.

TunGuard stores certificates under
`DATA_DIR/domains/certs/<domain>/` and renews them automatically when a
certificate is missing or expires within 30 days. It will never request a
certificate for a domain that has no mapping, and the built-in proxy returns
`404 domain not configured on this server` for any other host.

## How traffic is served

On the first mapping TunGuard decides how to serve it by looking at the web
stack already on the machine:

- **nginx / Apache / Caddy / Traefik** — the mapping is written into that
  server's configuration and reloaded. The config is introspected, never
  rewritten blindly: stale mappings are cleaned up, and when nginx or Apache is
  used, the TLS `443` block is only written once the certificate actually
  exists (a missing cert file would make `nginx -t` fail).
- **otherwise** — the built-in reverse proxy binds `DOMAIN_HTTP_PORT: 80` and
  `DOMAIN_HTTPS_PORT: 443` itself, using Go's `autocert` for HTTPS and a
  loopback HTTP-01 challenge listener on `DOMAIN_CHALLENGE_PORT` (default
  `8100`).
- **idle** — no mappings configured, nothing is bound.
- **blocked** — if an untracked process already holds ports 80/443, the proxy
  refuses to start rather than fight for them.

With a managed webserver, the ACME challenge for the domain is proxied to the
loopback challenge port, so certificate issuance works through the existing web
server. After any mapping change or issuance the server configuration is
re-written and reloaded.

## Serving a public DNS resolver (DoH + DoT)

A `dns` mapping turns a domain into a standalone, unauthenticated resolver that
serves the [managed AdGuard Home](adguard.md) filter to anyone. This is the
self-hosted equivalent of a public resolver such as `dns.adguard.com`: no
TunGuard login, no VPN required, just point a device at your endpoints.

```text
domain add dns.example.com --dns
```

The mapping exposes exactly two things:

| Endpoint | Address | Purpose |
|---|---|---|
| **DNS-over-HTTPS** | `https://dns.example.com/dns-query` | DoH, over the standard HTTPS port (`DOMAIN_HTTPS_PORT`, 443) |
| **DNS-over-TLS** | `dns.example.com:853` | DoT, on `DOMAIN_DOT_PORT` (default 853) |

The root `https://dns.example.com/` serves a TunGuard landing page that shows
these two endpoints, so the domain is self-explanatory to anyone who opens it.
Only `/dns-query` is proxied to AdGuard: every other path is a `404`, and
AdGuard's admin UI and login are never exposed through a DNS mapping.

/// note | Requires AdGuard Home

The `dns` backend needs the managed AdGuard Home instance. It is enabled by
default (`ADGUARD_ENABLED=true`); if it is disabled, `domain add ... --dns`
is rejected and `domain status` reports `AdGuard Home is not running`.

///

### How the endpoints are served

DoH reuses the same HTTPS machinery as any other mapping, so it works whether
TunGuard terminates TLS itself or an existing webserver does:

- **built-in proxy** — the mapping is served directly on `DOMAIN_HTTPS_PORT`.
- **nginx / Apache / Caddy / Traefik** — the generated vhost splits by path:
  `/dns-query` is proxied to AdGuard, everything else falls through to the
  TunGuard landing page on the loopback challenge listener.

DoT is a dedicated listener that TunGuard always binds itself on
`DOMAIN_DOT_PORT`, independent of the webserver:

- One listener serves **every** enabled `dns` mapping, selecting the certificate
  per-connection by SNI. An unknown or non-DNS hostname is refused.
- Each accepted TLS connection is tunnelled verbatim to AdGuard's plain DNS
  listener, so the DNS framing is the client's and AdGuard's, not TunGuard's.
- The listener starts when the first `dns` mapping becomes live and stops when
  the last one is removed or disabled.

Make sure `DOMAIN_DOT_PORT` (853) is reachable from the internet alongside
80/443, or DoT clients will fail.

/// warning | One resolver, many domains

Because the DNS backend always points at the single AdGuard Home instance, every
`dns` mapping on a server answers with the same filter and the same blocklists.
Multiple domains are useful for branding or redundancy, not for different
filtering per-domain.

///

## Managing domain mappings

### Dashboard

The **Domains** page lists every mapping with its state, and lets you add,
update (including pausing with *disable*), or remove entries.

### API

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/domains` | GET | List mappings plus proxy status |
| `/api/domains/status` | GET | Proxy mode, webserver, ports, owner of 80/443 |
| `/api/domain/add` | POST | Create a mapping |
| `/api/domain/update` | POST | Update a mapping |
| `/api/domain/remove` | POST | Delete a mapping |
| `/api` | — | All of the above return `409` when the proxy is disabled |

```shell
# Behind an existing TRP mapping (referenced by id or unique id prefix)
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain":"app.example.com","backend":"trp","proxy_ref":"3"}' \
  http://localhost:9000/api/domain/add

# Behind a tunneled service
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain":"api.example.com","backend":"wg","target_ip":"10.100.0.2","target_port":8080}' \
  http://localhost:9000/api/domain/add

# A public DoH + DoT resolver
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"domain":"dns.example.com","backend":"dns"}' \
  http://localhost:9000/api/domain/add

# Pause without deleting
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"DOMAIN_ID","enabled":false}' \
  http://localhost:9000/api/domain/update

# Remove
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"id":"DOMAIN_ID"}' \
  http://localhost:9000/api/domain/remove
```

`GET /api/domains/status` reports the serving mode so you can tell whether the
built-in proxy or an external webserver is active:

```json
{
  "enabled": true,
  "mode": "external",
  "webserver": "nginx",
  "owner_80": "nginx",
  "owner_443": "nginx",
  "http_port": 80,
  "https_port": 443,
  "challenge_port": 8100,
  "dot_port": 853,
  "dot": true,
  "count": 2
}
```

`dot` is `true` while the DoT listener is up (that is, while at least one `dns`
mapping is live), and `dot_port` is where it listens.

### Console

```text
domain list                                     mappings: domain, backend, target, state
domain add app.example.com --trp 3              behind an existing TRP mapping
domain add api.example.com --wg 10.100.0.2 8080 behind a tunneled service
domain add dns.example.com --dns                a public DoH + DoT resolver
domain update app.example.com --disable         pause without deleting
domain remove app.example.com                   by id or domain name
```

## Configuration

| Variable | Default | Description |
|---|---|---|
| `DOMAIN_ENABLED` | `true` | HTTPS domain proxy. `false` disables it |
| `DOMAIN_HTTP_PORT` | `80` | Public HTTP port for the ACME challenge and redirects |
| `DOMAIN_HTTPS_PORT` | `443` | Public HTTPS port of the domain proxy |
| `DOMAIN_CHALLENGE_PORT` | `8100` | Loopback port the HTTP-01 challenge answers on |
| `DOMAIN_DOT_PORT` | `853` | Public DNS-over-TLS port for `dns` mappings. `0` disables DoT |

Mappings persist in `DATA_DIR/domains/domains.json` (mode 0600), and
certificates plus the ACME account key under `DATA_DIR/domains/`, which are
covered by the usual backup and restore flow.

## Security notes

- A public mapping reaches its backend **without any added authentication**. The
  services you publish this way are exposed to the internet — protect them in
  the app, or only map domains you want public.
- The proxy forwards the request path as-is and preserves the `Host` header;
  `X-Forwarded-*` is set by TunGuard.
- Certificates are only requested for domains that have a mapping, and unknown
  `Host` headers get a `404`.
- A backend that cannot be reached responds `502 bad gateway`.
- A `dns` mapping is an **open resolver** by design. Only `/dns-query` is
  proxied to AdGuard and AdGuard's admin UI is never reachable through the
  domain, but anyone who knows the endpoint can query it. The filter applies,
  and AdGuard's own rate limit does too, so abuse is bounded rather than
  blocked. Remove the mapping (or disable it) if you no longer want it public.

## End to end: publish a service on a mesh node

```shell
#!/usr/bin/env bash
set -euo pipefail
API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"
field() { python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }

# Enroll a node running the service
ADDED="$(curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/mesh/node/add" \
  -d '{"name":"edge-a"}')"
NODE_ID="$(printf '%s' "$ADDED" | field id)"
echo "run on the device:  tun YOUR_SERVER_IP $(printf '%s' "$ADDED" | field psk)"

# Expose the service on the server through a TRP mapping
PROXY="$(curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/trp/proxy/add" \
  -d "{\"node_id\":\"$NODE_ID\",\"bind_port\":\"\",\"target_port\":\"8022\"}")"
PROXY_ID="$(printf '%s' "$PROXY" | field id)"
echo "tunnel listener:   $(printf '%s' "$PROXY" | field public_url)"

# Put a public HTTPS domain in front of it
curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/domain/add" \
  -d "{\"domain\":\"dashboard.example.com\",\"backend\":\"trp\",\"proxy_ref\":\"$PROXY_ID\"}"

echo "open:  https://dashboard.example.com"
```

## End to end: publish a public resolver

A DNS front is a single mapping. Point the domain's **A** record at the server,
open ports **443** and **853**, and add it:

```shell
API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"

curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/domain/add" \
  -d '{"domain":"dns.example.com","backend":"dns"}'

echo "DoH:  https://dns.example.com/dns-query"
echo "DoT:  dns.example.com:853"
```

Verify it resolves and filters:

```shell
# DoH (expect 0.0.0.0 for a blocked ad domain)
curl -s "https://dns.example.com/dns-query?name=doubleclick.net&type=A" \
  -H "accept: application/dns-json"

# DoT
kdig +tls +tls-host=dns.example.com @dns.example.com doubleclick.net
```