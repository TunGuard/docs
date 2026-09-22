---
title: Migrate
---

If you want to move an existing TunGuard installation to a new server, you can migrate the TunGuard data directory and restore it on the new server.

## Migrate to a New Server

A TunGuard backup contains the persistent state required to keep your existing server identity, peers, credentials, and configuration.

### 1. Create a Backup

On the existing server:

```bash
sudo tar -czf ~/tanguard-backup.tar.gz -C /var/lib/tanguard .
```

You can also create a backup from:

**Dashboard → Settings → Backup & Restore → Download Backup**

### 2. Install TunGuard on the New Server

Install TunGuard normally on the new server:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/installer.sh | bash
```

The installer creates and starts the TunGuard systemd service.

### 3. Stop TunGuard

On the new server:

```bash
sudo systemctl stop tanguard
```

### 4. Restore the Backup

Copy the backup to the new server and restore it into the TunGuard data directory:

```bash
sudo tar -xzf tanguard-backup.tar.gz -C /var/lib/tanguard
```

Make sure the restored files are owned by the account used to run TunGuard.

### 5. Start TunGuard

```bash
sudo systemctl start tanguard
```

Check the service:

```bash
sudo systemctl status tanguard
```

### What Is Migrated

The backup can contain:

- Server private key
- Peer data
- Dashboard credentials
- API key
- SSH host key
- TunGuard manifest and persistent state

Keeping the server private key means existing peers can continue using the same server identity.

### What Is Not Migrated

A backup does not replace:

- The TunGuard binary
- The systemd service
- The operating system
- Firewall rules
- Network configuration

Configure the new server's firewall and networking separately.

### If the Server Address Changes

If clients connect using the old server IP or hostname, update their endpoint.

For example:

```ini
[Peer]
PublicKey = <server-public-key>
Endpoint = vpn.example.com:13231
```

If the hostname remains the same and points to the new server, no client configuration change is required.

### If the Server Key Changes

If the migration does not preserve the original `server_private.key`, the server will have a different WireGuard identity.

In that case, generate new client configurations and replace the configurations on connected devices.

## Moving Back

The same process can be used to move TunGuard to another server again:

1. Back up the current data.
2. Install TunGuard on the destination server.
3. Stop the TunGuard service.
4. Restore the backup.
5. Start TunGuard.
6. Verify peers and connectivity.
