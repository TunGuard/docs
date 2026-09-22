---
title: Setup
---

## Install TunGuard

Install TunGuard on a fresh Linux server:

```shell
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer installs and starts TunGuard automatically.

After installation, open the dashboard:

```text
http://YOUR_SERVER_IP:9000
```

## First Login

On a fresh installation, use the default credentials:

- **Username**: `admin`
- **Password**: `tanguard`

You will be required to create new dashboard credentials after your first login.

## Dashboard Setup

After logging in, TunGuard is ready to manage your WireGuard server.

The default server configuration is:

- **WireGuard Address**: `10.100.0.1/24`
- **WireGuard Subnet**: `10.100.0.0/24`
- **WireGuard Port**: `13231`
- **Dashboard/API Port**: `9000`

## Create a Peer

Open **Peers** and create a new peer.

TunGuard generates the peer configuration automatically.

A generated configuration contains:

- **Private Key**: The peer's private WireGuard key.
- **Address**: The peer's assigned VPN address.
- **DNS**: The DNS server used by the peer.
- **Server Public Key**: The public key of the TunGuard server.
- **Endpoint**: The public address and WireGuard port of the TunGuard server.
- **Allowed IPs**: The networks that should be routed through the peer's connection.
- **Persistent Keepalive**: Keeps the connection active when the peer is behind NAT.

You can download the configuration, copy it, or scan its QR code using a WireGuard client.

## Peer Address

The first peer normally receives:

```text
10.100.0.2/32
```

Additional peers receive the next available address from the configured VPN subnet.

## Connect the Peer

Import the generated configuration into a WireGuard client on the device you want to connect.

The client connects to the TunGuard server using the configured WireGuard endpoint:

```text
YOUR_SERVER_IP:13231
```

Once connected, the peer appears in the **Peers** section of the TunGuard dashboard.

## Optional SSH Gateway

TunGuard can also provide SSH access to devices connected through the VPN.

Enable the SSH Gateway with:

```shell
./tanguard -ssh
```

The default SSH Gateway port is:

```text
2222
```

You can then connect to a VPN device through the TunGuard server:

```shell
ssh -J admin@YOUR_SERVER_IP:2222 root@10.100.0.2
```
