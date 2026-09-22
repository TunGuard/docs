---
title: Admin Panel
---

The TunGuard Admin Panel provides access to server settings, authentication, API access, backups, and peer management.

## Dashboard Login

Change the username and password used to access the TunGuard Admin Panel.

Go to:

**Settings → Dashboard Login**

Changes take effect immediately.

## API Key

TunGuard provides an API key for authenticating API requests.

Go to:

**Settings → API Key**

From here you can:

- Generate an API key
- View the current API key
- Revoke the current API key
- Generate a new API key

Once an API key is revoked, applications using the old key can no longer authenticate.

API requests can authenticate using either:

```text
X-API-Key: YOUR_API_KEY
```

or:

```text
Authorization: Bearer YOUR_API_KEY
```

Keep your API key private. Anyone with the key can access the API according to the permissions provided by TunGuard.

## Backup & Restore

TunGuard can back up its persistent configuration so it can be restored later.

Go to:

**Settings → Backup & Restore**

### Download Backup

Download a backup containing the persistent TunGuard state.

Backups can be used to recover a server or move an existing TunGuard installation to another server.

### Restore Backup

A backup can be imported into a new TunGuard installation.

This is useful when moving from one server to another.

The restored state can include:

- Server configuration
- WireGuard server key
- Peer configuration
- Dashboard credentials
- API key
- Other persistent TunGuard data

/// warning | Server Key

If the restored backup contains a different WireGuard server private key, existing peers will need updated configurations.

///

### Moving TunGuard to a New Server

To move TunGuard to another server:

1. Download a backup from the old server.
2. Install TunGuard on the new server.
3. Open **Settings → Backup & Restore**.
4. Import the backup.
5. Restart TunGuard if required.
6. Update the server address in client configurations if the server's public address changed.

The backup does not replace the TunGuard binary or systemd service configuration.

## Peer Management

Peer management is available from the **Peers** section.

Administrators can:

- Create peers
- Edit peers
- Enable or disable peers
- Generate peer configurations
- Display peer QR codes
- Add existing WireGuard keys
- Remove peers

See [Edit Peer](./clients.md) for the available peer settings.

## Groups

Groups are planned for organizing peers into logical collections.

Groups will allow administrators to manage peers based on their role, location, network, or other requirements.

A peer will be able to move between groups without needing to recreate the peer.

Group functionality is currently under development.

## Server Settings

TunGuard provides settings for configuring the WireGuard server and its network.

Common settings include:

- WireGuard interface
- WireGuard listen port
- VPN address
- VPN subnet
- MTU
- External network interface
- Dashboard/API listener
- SSH Gateway

Changes to networking settings can affect connected peers. Make sure client configurations match the server configuration after making changes.

## SSH Gateway

The optional SSH Gateway allows administrators to reach devices connected through TunGuard.

The default port is:

```text
2222
```

For example:

```shell
ssh -J admin@YOUR_SERVER_IP:2222 root@10.100.0.2
```

See the [CLI](./cli.md) guide for SSH Gateway commands and configuration.

## Security

The Admin Panel controls access to sensitive TunGuard functionality.

Administrators should:

- Change the default dashboard credentials after installation.
- Protect API keys.
- Revoke API keys that are no longer trusted.
- Keep backups in a secure location.
- Use HTTPS when exposing the dashboard through a public network.
