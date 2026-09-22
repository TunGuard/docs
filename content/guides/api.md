---
title: API Reference
---

TunGuard provides an HTTP API for managing the VPN server and its peers.

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
TUNGARD="http://localhost:9000"

curl \
  -H "X-API-Key: $API_KEY" \
  "$TUNGARD/api/peers"
```

## Example: Add a Peer

```shell
#!/bin/sh

API_KEY="REPLACE_WITH_YOUR_KEY"
TUNGARD="http://localhost:9000"

curl -X POST \
  -H "X-API-Key: $API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "public_key": "PEER_PUBKEY_HEX",
    "allowed_ip": "10.100.0.2/32",
    "device_name": "customer-device"
  }' \
  "$TUNGARD/api/peer/add"
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
