---
title: API Reference
---

TunGuard provides an HTTP API for managing the VPN server, its peers, and the P2P mesh.

The API is available under:

```text
http://YOUR_SERVER_IP:9000/api
```

## Endpoint overview

| Endpoint | Method | Auth | Purpose |
|---|---|---|---|
| `/api/health` | GET | None | Liveness check |
| `/api/status` | GET | Either | Server and peer status |
| `/api/system` | GET | Either | Host metrics |
| `/api/server_key` | GET | Either | Server public key and port |
| `/api/configure` | POST | Either | Change key or listen port at runtime |
| `/api/peers` | GET | Either | List peers |
| `/api/peer/add` | POST | Either | Add an existing public key |
| `/api/peer/remove` | POST | Either | Remove a peer |
| `/api/peer/config` | POST | Either | Re-render a peer's configuration |
| `/api/peer/generate-config` | POST | Either | Create a peer with a new key pair |
| `/api/version` | GET | Either | Version and update check |
| `/api/update` | POST | Either | Replace the binary and restart |
| `/api/backup/download` | GET | Either | Download a data directory backup |
| `/api/backup/restore` | POST | Either | Restore a backup |
| `/api/peer-monitor/events` | GET | Either | Peer event history |
| `/api/peer-monitor/state` | GET | Either | Latest peer metrics |
| `/api/ws/ssh` | GET | Either | WebSocket SSH session |
| `/api/auth/status` | GET | Dashboard | Current user, default-credential warning |
| `/api/web/credentials` | POST | Dashboard | Change dashboard password |
| `/api/key` | GET | Dashboard | Read the current API key |
| `/api/key/regenerate` | POST | Dashboard | Issue a new API key |
| `/api/mesh/*` | Various | Either | [P2P mesh](#p2p-mesh) |
| `/api/trp/*` | Various | Either | [TCP relay proxies](#tcp-relay-trp) |
| `/api/policy/*` | Various | Either | [Policy groups](#policy-groups-api) |

"Either" means the dashboard login or an API key. "Dashboard" means the login is
required and an API key is rejected.

## Authentication

All `/api/*` endpoints require authentication except `/api/health`.

Most endpoints accept **either** the dashboard credentials or an API key. A small group
of credential and key management endpoints accept **only** the dashboard login — see
[Credential and key management](#credential-and-key-management).

| Endpoint group | Accepted credentials |
|---|---|
| Most `/api/*`, all `/api/mesh/*`, all `/api/trp/*` | Dashboard login **or** API key |
| `/api/auth/status`, `/api/web/credentials`, `/api/key`, `/api/key/regenerate` | Dashboard login only |
| `/api/health` | None |

### Dashboard Authentication

Use HTTP Basic Authentication:

```shell
curl -u admin:PASSWORD http://localhost:9000/api/status
```

### API Key

Generate or rotate the API key from:

**Settings → API Key**

You can also generate one from the terminal using dashboard authentication:

```shell
curl -X POST \
  -u admin:PASSWORD \
  http://localhost:9000/api/key/regenerate
```

The response contains the new API key.

Store it securely:

```shell
API_KEY="REPLACE_WITH_YOUR_KEY"
```

Use the key with the `X-API-Key` header:

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  http://localhost:9000/api/status
```

The API key can also be sent using:

```text
Authorization: Bearer YOUR_API_KEY
```

/// note | Why the API key cannot manage itself

An API key is deliberately rejected by `/api/key` and `/api/key/regenerate`. A leaked
key can therefore be rotated, but only by someone who also has the dashboard password.
This is the difference between a key that can be neutralised and one that cannot.

///

## Health

### `GET /api/health`

Returns the health status of the TunGuard server.

This endpoint does not require authentication and exposes no sensitive information.

```shell
curl http://localhost:9000/api/health
```

This endpoint is suitable for uptime checks and load balancers.

## Server Status

### `GET /api/status`

Returns information about the TunGuard server and WireGuard status.

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  http://localhost:9000/api/status
```

## Server Public Key

### `GET /api/server_key`

Returns the WireGuard server public key.

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  http://localhost:9000/api/server_key
```

## System Information

### `GET /api/system`

Returns host metrics: hostname, OS, kernel, CPU model and core count, CPU utilisation,
load averages, process counts, uptime, memory, disk usage for the data directory, and
per-interface network counters.

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  http://localhost:9000/api/system
```

Response:

```json
{
  "hostname": "vpn-01",
  "os": "Debian GNU/Linux 12 (bookworm)",
  "kernel": "6.1.0-18-amd64",
  "cpu_model": "Intel(R) Xeon(R) Platinum 8375C CPU @ 2.90GHz",
  "cpu_cores": 4,
  "cpu_percent": 7.4,
  "load": [0.11, 0.08, 0.02],
  "uptime": 841203,
  "processes": { "total": 214, "running": 3 },
  "memory": { "total": 8123456, "used": 3910553, "percent": 48.1 },
  "disk": { "total": 41153856, "used": 12451840, "percent": 30.2 },
  "network": []
}
```

`disk` reflects the partition holding `DATA_DIR`, not the whole filesystem.

## Runtime Configuration

### `POST /api/configure`

Applies runtime changes without a restart. Both parameters are optional; send whichever
you need.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "private_key": "REPLACE_WITH_64_CHAR_HEX_PRIVATE_KEY",
    "listen_port": 51820
  }' \
  http://localhost:9000/api/configure
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `private_key` | No | New WireGuard server private key. Must be valid hex |
| `listen_port` | No | New WireGuard listen port. Recorded, but **a restart is required to apply it** |

If a new `private_key` is accepted, it is written to `DATA_DIR/server_private.key` with
mode `0600`, and the response includes the resulting `server_public_key`.

/// warning | Rotating the server key invalidates every peer config

    Peer configurations embed the server public key. After rotating, previously issued
    client configurations stop working and must be regenerated with `/api/peer/config`.

/// warning | Not available in mesh-only mode

With `-mesh-only` there is no WireGuard interface to reconfigure, so this endpoint must
not be used. Use the mesh and configuration file endpoints instead.

///

## List Peers

### `GET /api/peers`

Returns the peers currently configured on the TunGuard server.

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  http://localhost:9000/api/peers
```

## Add Peer

### `POST /api/peer/add`

Adds a peer using an existing WireGuard public key.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key": "PEER_PUBKEY_HEX",
    "allowed_ip": "10.100.0.2/32",
    "device_name": "my-device"
  }' \
  http://localhost:9000/api/peer/add
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `public_key` | Yes | WireGuard public key of the peer. Must be valid hex |
| `allowed_ip` | Yes | VPN address assigned to the peer, in CIDR form. Must not already be assigned |
| `device_name` | No | Label used to identify the peer in the dashboard |

Returns `409` if the public key is already registered, or if `allowed_ip` is already
assigned to another peer.

## Generate Peer Configuration

### `POST /api/peer/generate-config`

Creates a new peer and generates its WireGuard client configuration.

TunGuard generates the client's WireGuard key pair. Nothing is required — every
parameter has a default:

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "device_name": "my-phone",
    "server_host": "vpn.example.com"
  }' \
  http://localhost:9000/api/peer/generate-config
```

### Parameters

| Parameter | Required | Default | Description |
|---|---|---|---|
| `device_name` | No | — | Label used to identify the peer |
| `device_id` | No | — | Identifier stored with the peer record |
| `server_host` | No | Host of the request | Public hostname or IP clients use to reach TunGuard |
| `allowed_ip` | No | Next free address | VPN address to assign. Must not already be assigned |
| `dns` | No | `1.1.1.1` | DNS server written into the generated configuration |

Leaving `server_host` out uses the `Host` header of the request, so the generated
endpoint matches however you reached the server — but set it explicitly if you want a
different public hostname in the output.

The response contains the generated client configuration, including the peer's private
key. Treat it as a secret.

## Get Peer Configuration

### `POST /api/peer/config`

Generates the complete WireGuard configuration for an existing peer.

This is useful for re-downloading or re-rendering a configuration for a peer created using `/api/peer/generate-config`.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key": "PEER_PUBKEY_HEX",
    "server_host": "vpn.example.com"
  }' \
  http://localhost:9000/api/peer/config
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `public_key` | Yes | WireGuard public key of the peer |
| `server_host` | Yes | Public hostname or IP address clients use to reach TunGuard |

For peers created using `generate-config`, the returned configuration can include the client's private key.

Treat generated configurations as sensitive.

## Remove Peer

### `POST /api/peer/remove`

Removes a peer from TunGuard.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key": "PEER_PUBKEY_HEX"
  }' \
  http://localhost:9000/api/peer/remove
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `public_key` | Yes | WireGuard public key of the peer to remove |

## Credential and key management

These four endpoints all require the **dashboard login**. An API key is rejected, so a
leaked key can always be rotated by someone who holds the password.

### `GET /api/auth/status`

Returns the authenticated username and whether the server is still on default
credentials. Used by the dashboard to decide whether to force a password change.

```shell
curl -u admin:PASSWORD http://localhost:9000/api/auth/status
```

```json
{
  "authenticated": true,
  "username": "admin",
  "must_change": true
}
```

`must_change` is `true` only when no credentials have been stored yet and the configured
username and password are still `admin` / `tanguard`.

### `POST /api/web/credentials`

Changes the dashboard username and password.

```shell
curl -X POST \
  -u admin:tanguard \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "password": "a-long-passphrase",
    "confirm_password": "a-long-passphrase"
  }' \
  http://localhost:9000/api/web/credentials
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `username` | Yes | New dashboard username. Whitespace is trimmed; cannot be empty |
| `password` | Yes | New password. Minimum 8 characters |
| `confirm_password` | Yes | Must match `password` exactly |

Changing the password invalidates every existing session and API key, so update your
clients at the same time.

### `GET /api/key`

Returns the current API key, if one exists.

```shell
curl -u admin:PASSWORD http://localhost:9000/api/key
```

```json
{
  "exists": true,
  "key": "REPLACE_WITH_YOUR_KEY",
  "created_at": "2026-01-14T09:31:07Z"
}
```

When no key has been generated yet, `exists` is `false` and `key` is an empty string.
`created_at` is only present when a key exists.

### `POST /api/key/regenerate`

Creates a new API key and invalidates the previous key.

Dashboard authentication is required for this endpoint.

```shell
curl -X POST \
  -u admin:PASSWORD \
  http://localhost:9000/api/key/regenerate
```

The response contains the new key and its creation timestamp. The previous key stops
working immediately, so update any applications or automation that relied on it.

## Version and updates

### `GET /api/version`

Returns the running version, the latest published release, and update metadata. The
version check runs in the background; results are cached.

```shell
curl -H "X-API-Key: $API_KEY" http://localhost:9000/api/version
```

```json
{
  "current_version": "v1.2.0",
  "latest_version": "v1.3.0",
  "update_available": true,
  "download_url": "https://github.com/TunGuard/tanguard-binary/releases/download/v1.3.0/tanguard-linux-amd64",
  "release_notes": "https://api.github.com/repos/TunGuard/tanguard-binary/releases/latest",
  "release_url": "https://github.com/TunGuard/tanguard-binary/releases/tag/v1.3.0",
  "arch": "amd64",
  "last_checked": "2026-01-14T09:00:00Z"
}
```

Add `?refresh=1` to query GitHub immediately instead of returning the cached result:

```shell
curl -H "X-API-Key: $API_KEY" "http://localhost:9000/api/version?refresh=1"
```

### `POST /api/update`

Downloads a new binary, replaces the running executable, and restarts the process with
the same arguments.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"download_url": "https://github.com/TunGuard/tanguard-binary/releases/download/v1.3.0/tanguard-linux-amd64"}' \
  http://localhost:9000/api/update
```

### Parameters

| Parameter | Required | Description |
|---|---|---|
| `download_url` | Yes | URL of the replacement binary |

/// danger | This endpoint replaces the running binary

`/api/update` fetches `download_url` with no checksum or signature check, writes it over
the running executable, and re-execs it. Anything able to call this endpoint can install
arbitrary code as your server user.

Prefer downloading the release yourself, verifying it, and restarting through your
process supervisor. If you do use this endpoint, only ever pass a `download_url` you
obtained directly from the project's own releases, and never from a redirecting
shortener or mirror.

The download is capped at 256 MB, and a payload under 100 KB is rejected. A second
concurrent call returns `409` while an update is already in progress.

///

## Backup and restore

### `GET /api/backup/download`

Streams a `.tar.gz` backup of the data directory. The archive contains a `manifest.json`
recording the tool, version, creation time, and data directory path.

```shell
curl \
  -H "X-API-Key: $API_KEY" \
  -o tanguard-backup.tar.gz \
  http://localhost:9000/api/backup/download
```

### `POST /api/backup/restore`

Restores a backup produced by `/api/backup/download`. Send the archive as a multipart
form field named `backup`.

```shell
curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -F "backup=@tanguard-backup.tar.gz" \
  http://localhost:9000/api/backup/restore
```

/// warning | Back up before you restore

    Restore overwrites the current data directory. Take a fresh download first, and do
    not restore while peers are connected.

    A backup contains peer private keys and the stored API key. Anyone holding the file
    can impersonate your peers and read server credentials. Keep it encrypted at rest.

///

## Peer monitoring

These endpoints expose the peer handshakes the dashboard charts. They are registered
only when the peer monitor is running, and are absent in `-mesh-only` mode, where the
responses are `404`.

### `GET /api/peer-monitor/events`

Returns recorded peer events as a JSON array.

```shell
curl -H "X-API-Key: $API_KEY" http://localhost:9000/api/peer-monitor/events
```

```json
[
  { "t": "2026-01-14T09:31:07Z", "peer": "a1b2c3d4", "event": "handshake", "detail": "" },
  { "t": "2026-01-14T09:34:12Z", "peer": "e5f6a7b8", "event": "deferred", "detail": "handshake timeout" }
]
```

### Query parameters

| Parameter | Description |
|---|---|
| `since` | RFC 3339 timestamp. Returns only events strictly after it. Invalid values are ignored |
| `peer` | Public key prefix. Returns only events for that peer |

```shell
curl -H "X-API-Key: $API_KEY" \
  "http://localhost:9000/api/peer-monitor/events?peer=a1b2c3d4&since=2026-01-14T09:00:00Z"
```

This is a polling endpoint, not a stream — it returns the current buffer and closes.

### `GET /api/peer-monitor/state`

Returns a snapshot of the most recent metrics per peer, keyed by shortened public key.

```shell
curl -H "X-API-Key: $API_KEY" http://localhost:9000/api/peer-monitor/state
```

```json
{
  "a1b2c3d4": {
    "handshake": 1768382345,
    "endpoint": "198.51.100.24:4711",
    "txBytes": 184432,
    "rxBytes": 229104
  }
}
```

`handshake` is a Unix timestamp of the last completed handshake, or `0` if none has
happened yet.

## Web SSH

### `GET /api/ws/ssh`

Upgrades the connection to a WebSocket and opens a pseudo-terminal onto the host, which
is how the dashboard's **SSH Gateway** works. In a browser this must be requested as a
WebSocket; it cannot be called with a plain `curl` request.

Credentials are taken from the `Host` header in the form `user:password@host:port`, and
forwarded to the target host. A failure to connect is reported in-band over the socket
rather than as an HTTP status.

## Example: Automation

A simple script can use an API key to retrieve peer information:

```shell
#!/bin/sh

API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"

curl \
  -H "X-API-Key: $API_KEY" \
  "$API/api/peers"
```

## Example: Add a Peer

```shell
#!/bin/sh

API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"

curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key": "PEER_PUBKEY_HEX",
    "allowed_ip": "10.100.0.2/32",
    "device_name": "customer-device"
  }' \
  "$API/api/peer/add"
```

## P2P Mesh

The [P2P mesh](../examples/tutorials/p2p.md) is driven by endpoints under `/api/mesh/*`.
They use the same authentication as the rest of `/api/*`, and they answer whenever the
control plane is running — in a normal server start and under `-mesh-only` alike.

Mutating calls are `POST` with a JSON body. A `GET` on one of those returns `405`.

```shell
API_KEY="REPLACE_WITH_YOUR_KEY"
H="X-API-Key: $API_KEY"
JSON="Content-Type: application/json"
API="http://localhost:9000"
```

/// note | When the mesh is disabled

With `MESH_ENABLED=false` the control plane is never started and every endpoint below
returns `503 tun control plane is disabled`. Under `-mesh-only` the process refuses to
start at all. See [P2P Control Plane](../advanced/config/conf.md#p2p-control-plane).

///

### Nodes and Groups

A **node** is a client allowed onto the mesh. Nodes that share a **PSK** form a group,
and a group auto-meshes: every online member is punched to every other member. A node
added without a PSK gets a unique one. Every `node/add` response returns the generated
`psk` — save it, it is the device's join credential.

```shell
# Mesh state: enabled, node/group counts, listen addresses
curl -H "$H" "$API/api/mesh/status"

# List nodes. PSKs are masked; add ?show_psk=1 to reveal them
curl -H "$H" "$API/api/mesh/nodes"
curl -H "$H" "$API/api/mesh/nodes?show_psk=1"

# Devices bucketed by shared PSK, with per-group link counts
curl -H "$H" "$API/api/mesh/groups"

# Every direct and relayed link between nodes
curl -H "$H" "$API/api/mesh/links"
```

`GET /api/mesh/nodes` returns one object per node:

| Field | Description |
|---|---|
| `id` | The node handle every other call needs |
| `name` | Label you chose at enrollment |
| `psk` | The group key (masked unless `show_psk=1`) |
| `device_id` | The client's own stable identity, reported on connect |
| `online` | Whether the control channel is currently up |
| `control_ip` | Address the control channel came from |
| `relay_ep` | Public UDP endpoint registered at the hub |
| `relay_seen` | When that endpoint was last refreshed |
| `peers` | Number of peers this node holds |
| `direct_peers` | How many of those are direct |
| `tested_peers` | How many of those answered a link test |
| `connected_for` | How long the node has been connected |

A node with a `relay_ep` but no `direct_peers` is the one to investigate: discovery
worked and the hole punch did not.

`GET /api/mesh/links` returns one object per link:

| Field | Description |
|---|---|
| `from` / `to` | Node ids of the two ends |
| `online` | Whether the far node is connected |
| `endpoint` | Public endpoint the punch is aimed at |
| `direct` | A punch landed and the peer answered |
| `tested` | A link test completed on this link |
| `rtt_ms` | Round trip the client measured, in milliseconds |
| `direct_since` | When the link first went direct |

`direct` and `tested` answer different questions. `direct` is the punch: one packet
arrived, once. `tested` is the client's own round trip to the peer — a small packet it
sent that the peer echoed back — so `direct` with `tested` false is a link that punched
and then went quiet, which is what the dashboard shows as **no answer**.

```shell
# Add a node. Omit "psk" to have one generated.
# A "name" is only a label - it is NOT a unique key, and duplicates are allowed.
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/node/add" \
  -d '{"name":"edge-a"}'

# Add a node into an existing group
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/node/add" \
  -d '{"name":"edge-b","psk":"shared-group-key"}'

# Remove a node entirely, or just reset it (clears its link state, keeps the record)
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/node/remove" \
  -d '{"id":"NODE_ID"}'
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/node/reset" \
  -d '{"id":"NODE_ID"}'
```

/// warning | Removing a node leaves its proxies behind

`node/remove` does not clean up the node's TCP relays. Remove those with
`/api/trp/proxy/remove` first, or they keep holding their listeners.

///

### Direct Paths

Nodes in the same group are punched to each other automatically, so these calls are for
forcing a re-punch, forcing a group back onto the relay, or taking nodes off the mesh.

`p2p/connect` needs both nodes online — an offline or unknown id returns
`400 node offline`. Two nodes whose devices sit in **different policy groups**
cannot be punched together and the call is refused with
`400 policy groups are isolated`: a direct path never passes through the
server, so it is enforced at the point the link is created. Put both devices in
one group with `allow_inter_device` on to link them.

```shell
# Force an immediate direct path between two nodes
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/p2p/connect" \
  -d '{"a":"NODE_ID_A","b":"NODE_ID_B"}'

# Re-punch a whole group. "group" is the PSK.
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/p2p/mesh" \
  -d '{"group":"shared-group-key"}'

# Clear a group's peer table and punch targets
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/p2p/mesh" \
  -d '{"group":"shared-group-key","enable":false}'
```

`"enable": false` clears the server-side peer table and tells every member to drop its
punch targets. It is not a persistent "relay only" mode: each client re-learns the same
peers from the next rendezvous reply within a few seconds and resumes punching.

### Rendezvous Hub

Attach a node to the relay hub, or detach it. Both need the node connected; an offline
or unknown id returns `400 node offline`.

```shell
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/relay/join" \
  -d '{"id":"NODE_ID"}'
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/relay/leave" \
  -d '{"id":"NODE_ID"}'
```

Leaving drops only that node's P2P work. A full reset would also tear down its TCP
relay sessions, which is not what leaving the mesh should do.

To manage the relay circuits by hand — pin a relayed path, or drop every link leaving a
node:

```shell
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/relay/link" \
  -d '{"src":"NODE_ID_A","dst":"NODE_ID_B"}'
curl -X POST -H "$H" -H "$JSON" "$API/api/mesh/relay/unlink" \
  -d '{"src":"NODE_ID_A"}'
```

These are for overriding the automatic behaviour. Left alone, the server keeps a relay
circuit for every pair it attempts to punch, so a link that cannot go direct still
carries traffic.

/// warning | `relay/unlink` removes the fallback

Dropping a node's relay circuits leaves it with no path for any link that fails to go
direct. Use it to isolate a node while debugging, not to pin traffic onto the relay —
direct and relayed paths are maintained together, and there is no switch between them.

///

### TCP Relay (TRP)

A TRP proxy listens on the server and forwards each connection to `target_ip:target_port`
on the target node over its mesh path.

Leave `bind_port` as an **empty string** to let the OS pick a free port — the chosen port
comes back as `bind_port` and in `public_url`. `"0"` is rejected; only an empty string
means auto-assign. `target_port` is always required and always numeric.

```shell
# List proxies, with live connection counts
curl -H "$H" "$API/api/trp/proxies"

# Auto-assigned listen port, forwarding to port 8022 on the node
curl -X POST -H "$H" -H "$JSON" "$API/api/trp/proxy/add" \
  -d '{"node_id":"NODE_ID","bind_port":"","target_port":"8022"}'

# Fixed listen port and an explicit target address
curl -X POST -H "$H" -H "$JSON" "$API/api/trp/proxy/add" \
  -d '{"node_id":"NODE_ID","bind_ip":"0.0.0.0","bind_port":"18022","target_ip":"127.0.0.1","target_port":"8022"}'

# Remove a proxy
curl -X POST -H "$H" -H "$JSON" "$API/api/trp/proxy/remove" \
  -d '{"id":"PROXY_ID"}'
```

### Mesh Errors

Failures are JSON with an `error` field, so scripts can branch on them:

| Status | Meaning |
|---|---|
| `400` | Bad request — `id required`, `node_id required`, `unknown group`, `node offline`, `policy groups are isolated`, port out of range, or malformed JSON |
| `401` | Missing or invalid dashboard login / API key |
| `404` | No such node, proxy, or binding |
| `405` | `GET` used on a `POST`-only route |
| `503` | Mesh control plane not running — set `MESH_ENABLED=true` (the default) |

### Mesh End to End

```shell
#!/usr/bin/env bash
set -euo pipefail
API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"
field() { python3 -c "import json,sys;print(json.load(sys.stdin)['$1'])"; }

# Enroll a device and keep the id and PSK it returns
ADDED="$(curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/mesh/node/add" \
  -d '{"name":"edge-a"}')"
NODE_ID="$(printf '%s' "$ADDED" | field id)"
PSK="$(printf '%s' "$ADDED" | field psk)"
echo "run on the device:  tun YOUR_SERVER_IP $PSK"

# Expose a service running on that node
PROXY="$(curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/trp/proxy/add" \
  -d "{\"node_id\":\"$NODE_ID\",\"bind_port\":\"\",\"target_port\":\"8022\"}")"
echo "reachable at $(printf '%s' "$PROXY" | field public_url)"

# Tear down
curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/trp/proxy/remove" \
  -d "{\"id\":\"$(printf '%s' "$PROXY" | field id)\"}"
curl -sS -X POST -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" "$API/api/mesh/node/remove" \
  -d "{\"id\":\"$NODE_ID\"}"
```

## Policy Groups API

A policy group is a set of devices with its own rules. Every device the server
knows about is in exactly one group, and a device in no custom group is in
`default`. The group decides what a device may reach:

| Rule | Allows |
|---|---|
| `allow_inter_device` | Traffic to the other devices **of the same group** |
| `allow_p2p_mesh` | P2P mesh participation |
| `allow_trp` | TCP relay proxies onto the group |
| `allow_wg_access` | Internet access out through the tunnel |

```shell
API="http://localhost:9000"
H="X-API-Key: $API_KEY"
JSON="Content-Type: application/json"

# Every group with its members, every known device, and the packet-filter
# drop counters for inter-device and internet traffic
curl -H "$H" "$API/api/policy/groups"

# Create a group. Every omitted rule is OFF, so a new group denies by default
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/create" \
  -d '{"name":"office","allow_inter_device":true,"allow_wg_access":true}'

# Change a group. Omitted rules and an empty name keep their current value,
# so this turns on inter-device traffic without touching the other rules
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/update" \
  -d '{"id":"GROUP_ID","allow_inter_device":true}'

# Delete a group. Its devices fall back to the default group
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/delete" \
  -d '{"id":"GROUP_ID"}'

# Move WireGuard peers into a group, by public key
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/assign" \
  -d '{"id":"GROUP_ID","devices":["PEER_PUBKEY_HEX"]}'

# Move tun-client devices into a group, by device id
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/assign-device" \
  -d '{"id":"GROUP_ID","devices":["DEVICE_ID"]}'

# Send devices back to the default group
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/unassign" \
  -d '{"devices":["PEER_PUBKEY_HEX"]}'
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/group/unassign-device" \
  -d '{"devices":["DEVICE_ID"]}'

# Replace the whole policy in one call: groups, peer membership, and device
# membership. Rejected outright if any name names a device the server has
# never seen
curl -X POST -H "$H" -H "$JSON" "$API/api/policy/apply" \
  -d '{"groups":[{"id":"office","name":"Office","allow_inter_device":true,"allow_wg_access":true}],
       "assign":{"PEER_PUBKEY_HEX":"office"},
       "device_assign":{"DEVICE_ID":"office"}}'
```

A device is named by **public key** when it is a WireGuard peer, and by **device
id** when it is a tun-client device with no peer of its own. Sending the wrong
identity returns `400 unknown device`. `group/unassign` and
`group/unassign-device` do not need an `id` — the group id in their response is
always `default`.

/// warning | Groups are sealed from each other

`allow_inter_device` opens traffic to the other devices of **that group only**.
It never grants reach into or out of another group, and it does not depend on the
other group's own setting: one open side is enough, but only within one group.
Before `2.4.2`, an open group could reach into a closed one; that leak is fixed,
so cross-group traffic now needs the devices to be in the same group — and
`/api/mesh/p2p/connect` refuses such a pair with
`400 policy groups are isolated`.

///

## API Security

API keys provide access to protected TunGuard API endpoints. Keep them private and do not commit them to source control.

If a key is exposed, rotate it immediately from:

**Settings → API Key**

or:

```shell
curl -X POST \
  -u admin:PASSWORD \
  http://localhost:9000/api/key/regenerate
```

For production deployments, protect the dashboard and API with HTTPS when they are exposed over an untrusted network.

An API key is a broad credential: it can add and remove peers, read and restore
backups, and replace the server binary via `/api/update`. Scope it like a password, and
prefer issuing short-lived credentials from a provisioning job over a long-lived shared
key.

Two endpoints deserve particular attention:

- `/api/update` fetches an arbitrary URL and overwrites the running executable. Only
  point it at releases you obtained directly from the project's own release page.
- `/api/ws/ssh` opens an interactive shell to the host. Anyone who can reach the API can
  reach the machine's SSH credentials, so keep the API off untrusted networks.

Both are reasons to terminate TLS in front of the API and to keep the default dashboard
credentials from surviving first boot.

