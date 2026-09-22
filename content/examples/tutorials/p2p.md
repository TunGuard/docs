---
title: P2P Connections
---

TunGuard can be used as a discovery and relay point for peer-to-peer connections.

The TunGuard server is used to introduce the two peers and provide a relay path when a direct connection cannot be established.

Once a direct path is available, traffic can move directly between the peers.

## How It Works

```text
Peer A
  |
  | 1. Connect to TunGuard
  |
  v
TunGuard Server
  |
  | 2. Discover / exchange connection information
  |
  v
Peer B

Peer A <----------------------> Peer B
              Direct P2P
```

If the peers cannot establish a direct connection, TunGuard remains available as the relay path.

```text
Peer A
  |
  v
TunGuard Server
  |
  v
Peer B
```

## Install the TunGuard Client

Each device participating in the P2P network must have the TunGuard client installed.

Get the client from the [TunGuard/get](https://github.com/TunGuard/get) repository.

The client runs on the device that will participate in the P2P connection.

Install it on both devices:

```text
Peer A → TunGuard Client
Peer B → TunGuard Client
```

## Connect a Device

After installing the client, connect the device to your TunGuard server using the server address and the credentials or connection information provided by your TunGuard setup.

The client establishes the initial connection to TunGuard.

TunGuard then provides the discovery information required for the peers to find each other.

## Peer Discovery

When two devices need to communicate:

1. Peer A connects to TunGuard.
2. Peer B connects to TunGuard.
3. TunGuard identifies the two peers.
4. The peers exchange the information required to establish a connection.
5. The peers attempt a direct connection.
6. If the direct connection succeeds, traffic uses the P2P path.
7. If a direct connection cannot be established, TunGuard can relay the traffic.

## Direct Connection

The preferred path is:

```text
Peer A <====================> Peer B
             Direct
```

TunGuard is used for discovery and connection establishment rather than carrying the traffic when a direct path is available.

This allows peers to communicate without requiring every connection to pass through the server.

## Relay

Some networks may prevent a direct connection because of NAT, firewalls, or other network restrictions.

In that case, the connection can fall back to TunGuard:

```text
Peer A
  |
  | encrypted traffic
  v
TunGuard
  |
  | encrypted traffic
  v
Peer B
```

The relay provides a path between peers that cannot establish a direct connection.

## Server Role

TunGuard can provide three functions for P2P connections:

- **Discovery** — helps peers find each other.
- **Connection establishment** — helps peers exchange the information required to connect.
- **Relay** — provides a fallback path when direct connectivity is unavailable.

The server does not need to remain in the traffic path when the peers have established a direct connection.

## Network Example

Two devices can be located on completely different networks:

```text
Office Network
     |
  Peer A
     |
     | Internet
     |
     v
TunGuard Server
     ^
     | Internet
     |
  Peer B
     |
Home Network
```

After discovery:

```text
Office Network
     |
  Peer A
      \
       \
        ===== Direct P2P =====
                              \
                               Peer B
                                |
                           Home Network
```

If direct connectivity is not possible, the relay path remains available through the TunGuard server.

## Security

P2P connectivity should use encrypted connections between the participating peers.

Keep the TunGuard server protected and only allow authorized clients to join the network.

Do not share client credentials or connection information with unauthorized devices.

## Client Installation

The TunGuard client is distributed through the [TunGuard/get](https://github.com/TunGuard/get) repository.

Install the client on every device that needs to participate in P2P connections.
