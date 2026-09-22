---
title: FAQ
hide:
    - navigation
---

Here are some frequently asked questions and common issues about `TunGuard`. If you have a question that is not answered here, feel free to open an issue or discussion on GitHub.

## Do I need to install WireGuard?

No. TunGuard runs WireGuard entirely in userspace. You do not need to install the WireGuard kernel module or run `apt install wireguard`.

## How do I install TunGuard?

On a fresh Linux server, run:

```shell
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer installs and starts TunGuard automatically.

After installation, open:

```text
http://YOUR_SERVER_IP:9000
```

## What are the default dashboard credentials?

On a fresh installation:

```text
Username: admin
Password: tanguard
```

You will be required to change the credentials after the first login.

## I cannot access the dashboard

TunGuard's dashboard and API use port `9000` by default.

Make sure the port is reachable from your network and that your server or cloud provider firewall allows TCP traffic on port `9000`.

You can also check the service status:

```shell
sudo systemctl status tanguard
```

## What ports does TunGuard use?

The default ports are:

| Service | Port | Protocol |
|---|---:|---|
| WireGuard | `13231` | UDP |
| Dashboard/API | `9000` | TCP |
| SSH Gateway | `2222` | TCP |

## How do I create a WireGuard peer?

Open **Peers** in the dashboard and create a new peer.

TunGuard can generate the client configuration and QR code.

The default VPN network is:

```text
10.100.0.0/24
```

## My peer cannot connect

Check that:

1. The WireGuard UDP port `13231` is reachable from the internet.
2. The client configuration uses the correct server address and port.
3. The server is running.
4. The peer exists in **Peers** in the dashboard.

You can check the service with:

```shell
sudo systemctl status tanguard
```

## My peer connects but cannot access the internet

Check that the server has internet connectivity and that the client's configuration routes the required traffic through TunGuard.

For full-tunnel routing, the peer configuration normally contains:

```text
AllowedIPs = 0.0.0.0/0, ::/0
```

Server-side routing and NAT must also be correctly configured for your environment.

## I forgot my dashboard password

Reset the dashboard credentials with:

```shell
sudo ./tanguard --reset
```

This removes the stored dashboard credentials and restores:

```text
Username: admin
Password: tanguard
```

You can then log in and set new credentials.

## How do I change the dashboard credentials?

Open **Settings → Dashboard Login** in the dashboard.

Changes take effect immediately.

## How do I update TunGuard?

Run the installer again:

```shell
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer updates the TunGuard binary while preserving the existing service configuration and persistent data.

## Will updating TunGuard delete my peers?

No. Peer data is stored in the persistent `DATA_DIR` and is preserved when updating the binary.

## How do I back up TunGuard?

From the dashboard, open:

**Settings → Backup & Restore → Download Backup**

You can also create a backup from the command line:

```shell
sudo tar -czf ~/tanguard-backup.tar.gz -C /var/lib/tanguard .
```

## How do I restore a backup?

Use **Settings → Backup & Restore** in the dashboard and upload a TunGuard backup.

The restored peer and server state is applied immediately.

If the restored server private key is different, existing clients will need updated configurations.

## Does TunGuard support existing WireGuard keys?

Yes. You can add an existing peer key through the **Peers** section instead of generating a new key.

## What is the SSH Gateway?

The optional SSH Gateway allows SSH access to WireGuard-connected devices through the TunGuard server.

It uses port `2222` by default and can be enabled with:

```shell
./tanguard -ssh
```

For example:

```shell
ssh -J admin@yourserver:2222 root@10.100.0.2
```

## How do I use the API?

TunGuard provides an API under `/api/*`.

Most API endpoints require dashboard authentication or an API key.

API keys can be generated from **Settings → API Key** and supplied using either:

```text
X-API-Key: YOUR_API_KEY
```

or:

```text
Authorization: Bearer YOUR_API_KEY
```

The `/api/health` endpoint does not require authentication.

## Where can I report a bug?

Open an issue in the TunGuard repository.

Include:

- TunGuard version
- Linux distribution
- Relevant logs
- Steps to reproduce the problem
