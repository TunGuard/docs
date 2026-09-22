---
title: Edit Peer
---

## General

- **Name**: The name used to identify the peer.
- **Enabled**: Whether the peer is allowed to connect to the VPN.

## Address

- **IPv4**: The IPv4 address assigned to the peer.

TunGuard uses the configured VPN subnet to assign peer addresses.

The default VPN subnet is:

```text
10.100.0.0/24
```

The server uses:

```text
10.100.0.1
```

and peers are assigned addresses such as:

```text
10.100.0.2
10.100.0.3
10.100.0.4
```

## Allowed IPs

The networks that the peer will route through the VPN.

For example:

```text
0.0.0.0/0, ::/0
```

routes all IPv4 and IPv6 traffic through TunGuard.

A more specific configuration can be used when the peer should only route selected networks.

## DNS

The DNS server that will be configured for the peer.

For example:

```text
1.1.1.1
```

## Persistent Keepalive

The interval, in seconds, at which the peer sends keepalive packets to the TunGuard server.

This can help maintain connections when the peer is behind NAT or a restrictive firewall.

A common value is:

```text
25
```

## Keys

TunGuard uses WireGuard public and private keys for peer authentication.

When creating a peer, TunGuard can generate the required keys automatically.

Existing WireGuard keys can also be added when configuring an existing peer.

## Configuration

TunGuard generates a standard WireGuard client configuration for each peer.

A generated configuration contains:

```ini
[Interface]
PrivateKey = <client-private-key>
Address = 10.100.0.2/32
DNS = 1.1.1.1

[Peer]
PublicKey = <server-public-key>
Endpoint = yourserver:13231
AllowedIPs = 0.0.0.0/0, ::/0
PersistentKeepalive = 25
```

The configuration can be downloaded, copied, or displayed as a QR code from the dashboard.

## Actions

- **Save**: Save changes made to the peer.
- **Revert**: Discard unsaved changes.
- **Delete**: Remove the peer from TunGuard.
- **Generate Config**: Generate the peer's WireGuard configuration.
- **QR Code**: Display the peer configuration as a QR code.
