---
title: API Reference
---

TunGuard provides an HTTP API for managing the VPN server, its peers, and the P2P mesh.

The API is available under:

```text
http://YOUR_SERVER_IP:9000/api
```

## Authentication

All `/api/*` endpoints require authentication except `/api/health`.

You can authenticate using either the dashboard credentials or an API key.

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
| `public_key` | Yes | WireGuard public key of the peer |
| `allowed_ip` | Yes | VPN address assigned to the peer |
| `device_name` | Yes | Name used to identify the peer |

## Generate Peer Configuration

### `POST /api/peer/generate-config`

Creates a new peer and generates its WireGuard client configuration.

TunGuard generates the client's WireGuard key pair.

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

| Parameter | Required | Description |
|---|---|---|
| `device_name` | Yes | Name used to identify the peer |
| `server_host` | Yes | Public hostname or IP address clients use to reach TunGuard |

The response contains the generated client configuration.

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

## API Key Management

### `POST /api/key/regenerate`

Creates a new API key and invalidates the previous key.

Dashboard authentication is required for this endpoint.

```shell
curl -X POST \
  -u admin:PASSWORD \
  http://localhost:9000/api/key/regenerate
```

After rotating the key, update any applications or automation using the previous key.

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
| `connected_for` | How long the node has been connected |

A node with a `relay_ep` but no `direct_peers` is the one to investigate: discovery
worked and the hole punch did not.

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
`400 node offline`.

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
| `400` | Bad request — `id required`, `node_id required`, `unknown group`, `node offline`, port out of range, or malformed JSON |
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
