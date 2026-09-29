---
title: Configuration
---

TunGuard is configured through environment variables.

Most installations can use the default values. Change a setting when you need a different interface, port, network, data directory, or service configuration.

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `WG_INTERFACE` | `wg0` | WireGuard interface name |
| `WG_LISTEN_PORT` | `13231` | WireGuard UDP port used by clients |
| `WG_ADDRESS` | `10.100.0.1/24` | TunGuard server address on the VPN subnet |
| `WG_SUBNET` | `10.100.0.0/24` | VPN subnet assigned to clients |
| `WG_MTU` | `1420` | WireGuard MTU |
| `API_LISTEN` | `:9000` | Web dashboard and API listen address |
| `DATA_DIR` | `.` | Directory used to store keys and peer data |
| `EXTERNAL_NIC` | `auto` | External network interface used for NAT |
| `WEB_ENABLED` | `false` | Enables the web dashboard. Can also be enabled with `-web` |
| `WEB_USERNAME` | `admin` | Initial dashboard username. Only used until changed from the dashboard |
| `WEB_PASSWORD` | `tanguard` | Initial dashboard password. Only used until changed from the dashboard |
| `SSH_ENABLED` | `false` | Enables the SSH gateway. Can also be enabled with `-ssh` |
| `SSH_LISTEN` | `:2222` | SSH gateway listen address |
| `SSH_KEY_FILE` | `auto` | SSH host key path. Automatically generated when missing |
| `MESH_ENABLED` | `true` | Enables the P2P control plane. See [P2P Control Plane](#p2p-control-plane) |
| `CONTROL_LISTEN` | `:7000` | TCP control listener used by the P2P client |
| `RELAY_LISTEN` | `:7001` | UDP rendezvous and relay listener for the P2P mesh |
| `CONTROL_TIMEOUT_S` | `10` | Seconds allowed for a P2P client handshake |
| `MESH_DATA_DIR` | `DATA_DIR` | Where the P2P node registry is stored |

## WireGuard Settings

### `WG_INTERFACE`

Controls the name of the WireGuard interface created by TunGuard.

Default:

```text
wg0
```

Example:

```text
WG_INTERFACE=wg1
```

### `WG_LISTEN_PORT`

Controls the UDP port used by the WireGuard server.

Default:

```text
13231
```

Clients must connect to this port.

Example:

```text
WG_LISTEN_PORT=51820
```

If you change this value, make sure the new UDP port is allowed through your server firewall.

### `WG_ADDRESS`

Sets the server's address on the VPN network.

Default:

```text
10.100.0.1/24
```

Example:

```text
WG_ADDRESS=10.50.0.1/24
```

The address must belong to the subnet configured with `WG_SUBNET`.

### `WG_SUBNET`

Defines the VPN network used by TunGuard clients.

Default:

```text
10.100.0.0/24
```

Example:

```text
WG_SUBNET=10.50.0.0/24
```

The server address configured with `WG_ADDRESS` must belong to this subnet.

### `WG_MTU`

Sets the WireGuard interface MTU.

Default:

```text
1420
```

Example:

```text
WG_MTU=1380
```

Only change the MTU when required by your network.

## API and Dashboard

### `API_LISTEN`

Controls where the web dashboard and API listen.

Default:

```text
:9000
```

This listens on TCP port `9000` on all interfaces.

Example:

```text
API_LISTEN=:8080
```

### `WEB_ENABLED`

Enables the web dashboard.

Default:

```text
false
```

The dashboard can also be enabled with:

```sh
./tanguard -web
```

When using the normal installer, the installed service can be configured to enable the dashboard.

### `WEB_USERNAME`

Sets the initial dashboard username.

Default:

```text
admin
```

This value is only used until the dashboard credentials are changed.

### `WEB_PASSWORD`

Sets the initial dashboard password.

Default:

```text
tanguard
```

This value is only used until the dashboard credentials are changed.

Change the default credentials before exposing the dashboard publicly.

## Data Directory

### `DATA_DIR`

Controls where TunGuard stores persistent data.

Default:

```text
.
```

The directory contains data such as:

- Server private key
- Peer information
- Dashboard credentials
- API key
- SSH host key
- Other persistent TunGuard state

Example:

```text
DATA_DIR=/var/lib/tanguard
```

When changing this value, make sure the TunGuard process has permission to access the directory.

## Network Interface

### `EXTERNAL_NIC`

Specifies the external network interface used for NAT.

Default:

```text
auto
```

TunGuard automatically detects the external interface.

To specify an interface manually:

```text
EXTERNAL_NIC=eth0
```

This can be useful on servers with multiple network interfaces.

## SSH Gateway

### `SSH_ENABLED`

Enables the TunGuard SSH gateway.

Default:

```text
false
```

It can also be enabled with:

```sh
./tanguard -ssh
```

### `SSH_LISTEN`

Controls where the SSH gateway listens.

Default:

```text
:2222
```

Example:

```text
SSH_LISTEN=:2200
```

If you change the port, make sure the new TCP port is allowed through your firewall.

### `SSH_KEY_FILE`

Specifies the SSH host key file.

Default:

```text
auto
```

When set to `auto`, TunGuard generates a host key when one does not already exist.

Example:

```text
SSH_KEY_FILE=/var/lib/tanguard/ssh_host_key
```

## API Key

The API key is not set through an environment variable. It is generated from the
dashboard under **Settings → API Key**, or with:

```sh
curl -X POST \
  -u admin:PASSWORD \
  http://127.0.0.1:9000/api/key/regenerate
```

It is stored in `api_key.json` inside `DATA_DIR`, and can then be supplied with
individual API requests:

```sh
curl \
  -H "X-API-Key: YOUR_API_KEY" \
  http://127.0.0.1:9000/api/peers
```

Regenerating the key invalidates the previous one immediately.

See the [API](../../guides/api.md) documentation for authentication and available
endpoints.

## P2P Control Plane

The P2P mesh runs as a second subsystem alongside WireGuard. It is enabled by default
and needs no configuration, but these variables control it.

### `MESH_ENABLED`

Enables the P2P control plane.

Default:

```text
true
```

With `MESH_ENABLED=false` the control listener and the rendezvous hub are never
started, and every `/api/mesh/*` endpoint returns `503 tun control plane is disabled`.
Starting with `-mesh-only` while the mesh is disabled makes the process refuse to run.

### `CONTROL_LISTEN`

The TCP address that clients dial out to. This is the port that goes in the
`tun <server-ip> <psk>` command.

Default:

```text
:7000
```

### `RELAY_LISTEN`

The UDP address of the rendezvous hub, where clients register their public endpoint and
discover each other.

Default:

```text
:7001
```

Both ports must be reachable from the internet. If the hub port is unreachable, clients
still connect and appear online but never discover each other, so no link can go
direct.

### `CONTROL_TIMEOUT_S`

How long, in seconds, a client has to complete its handshake after connecting.

Default:

```text
10
```

### `MESH_DATA_DIR`

Where the mesh node registry is stored.

Default:

```text
(the value of DATA_DIR)
```

## Example Configuration

A typical server configuration could look like:

```text
WG_INTERFACE=wg0
WG_LISTEN_PORT=13231
WG_ADDRESS=10.100.0.1/24
WG_SUBNET=10.100.0.0/24
WG_MTU=1420

API_LISTEN=:9000
DATA_DIR=/var/lib/tanguard
EXTERNAL_NIC=auto

WEB_ENABLED=true

SSH_ENABLED=true
SSH_LISTEN=:2222
SSH_KEY_FILE=auto

MESH_ENABLED=true
CONTROL_LISTEN=:7000
RELAY_LISTEN=:7001
```

Not every variable needs to be configured. TunGuard uses the defaults when a variable is not provided.
