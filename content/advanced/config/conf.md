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
| `TUNGARD_API_KEY` | — | API key for PHP or script integrations. Can also be supplied per request |

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

### `TUNGARD_API_KEY`

Sets an API key that can be used by applications and scripts.

Example:

```text
TUNGARD_API_KEY=your-api-key
```

The API key can also be supplied with individual API requests.

For example:

```sh
curl \
  -H "X-API-Key: YOUR_API_KEY" \
  http://127.0.0.1:9000/api/peers
```

See the [API](./api.md) documentation for authentication and available endpoints.

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
```

Not every variable needs to be configured. TunGuard uses the defaults when a variable is not provided.
