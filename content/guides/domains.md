---
title: Domains & HTTPS Proxy
---

TunGuard can publish an internal service on a public domain with HTTPS handled
automatically. You point a domain at the server and choose the service behind
it; TunGuard terminates TLS with a Let's Encrypt certificate and proxies to
that service.

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
  "count": 2
}
```

### Console

```text
domain list                                     mappings: domain, backend, target, state
domain add app.example.com --trp 3              behind an existing TRP mapping
domain add api.example.com --wg 10.100.0.2 8080 behind a tunneled service
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