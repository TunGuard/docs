---
title: Admin Panel
---

<svg class="tg-figure" viewBox="0 0 720 180" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="A browser drives the TunGuard dashboard, which manages server state, peers and settings">
  <g class="tg-flow tg-accent" stroke-width="2.4">
    <path d="M198 90h100"/>
    <path d="M422 90h120"/>
  </g>
  <g class="tg-float">
    <circle cx="140" cy="90" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="112" y="66" width="56" height="44" rx="6"/>
    <path d="M112 78h56"/>
    <circle class="tg-blink" cx="120" cy="72" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d1" cx="127" cy="72" r="1.6" fill="currentColor" stroke="none"/>
    <path class="tg-sweep" d="M126 92h30" opacity=".7"/>
  </g>
  <g class="tg-float tg-d2">
    <circle class="tg-pulse tg-accent" cx="362" cy="90" r="52" fill="var(--md-default-bg-color)"/>
    <rect x="336" y="70" width="24" height="40" rx="3"/>
    <rect x="364" y="70" width="24" height="18" rx="3"/>
    <rect x="364" y="92" width="24" height="18" rx="3"/>
    <circle class="tg-blink" cx="378" cy="88" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d1" cx="378" cy="110" r="1.6" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="600" cy="90" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="584" y="66" width="32" height="12" rx="3"/>
    <rect x="584" y="84" width="32" height="12" rx="3"/>
    <rect x="584" y="102" width="32" height="12" rx="3"/>
    <circle class="tg-blink" cx="590" cy="72" r="1.4" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d1" cx="590" cy="90" r="1.4" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d2" cx="590" cy="108" r="1.4" fill="currentColor" stroke="none"/>
  </g>
</svg>

<p class="tg-cap">Manage peers, settings, backups and the API from the browser.</p>

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

## Policy Groups

Policy groups are available from the **Policy** section. Each group holds a set of
devices and its own set of rules:

| Rule | Allows |
|---|---|
| Inter-device traffic | Devices in this group to reach each other |
| P2P mesh | Devices in this group to be punched together |
| TCP relay | Port mappings (TRP proxies) onto these devices |
| WireGuard access | Internet access out through the tunnel |
| AdGuard DNS filtering | Port-53 DNS of this group's devices is redirected to the embedded AdGuard Home |

See [AdGuard DNS Filtering](adguard.md) for what the AdGuard switch does.

Every rule starts **off**, and every device is in exactly one group. Devices in no
custom group are in **Default**, whose rules apply until you change them.

Administrators can:

- Create, rename, edit and delete groups
- Move devices between groups, including back to Default
- See how many packets the filter has dropped for inter-device and internet access

/// warning | Groups do not reach into each other

Inter-device traffic stays inside one group. Opening it on one group does not open
any other group, and a device in Default cannot reach a device in a custom group.
Devices that need to talk to each other belong in the same group.

///

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

The optional SSH Gateway turns TunGuard into a jump host so administrators can
reach devices connected through TunGuard without exposing SSH on them.

The full story — enabling it, jumping to a peer, the browser SSH terminal, and
the built-in `ssh` client — is in the [SSH Access](ssh.md) guide. As a quick
start, with the gateway enabled the default port is `2222` and you connect
with:

```shell
ssh -J admin@YOUR_SERVER_IP:2222 root@10.100.0.2
```

## Domains & HTTPS

TunGuard can publish an internal service on a public domain with automatic
Let's Encrypt HTTPS — in front of a TRP mapping or a tunneled WireGuard
service. Manage mappings from the **Domains** page, the API, or the console.
See [Domains & HTTPS Proxy](domains.md).

## AdGuard DNS Filtering

A managed AdGuard Home can filter DNS for devices in an
[AdGuard-enabled policy group](#policy-groups). It starts automatically, its
DNS service binds to the tunnel address, and protected devices are redirected
to it on the server — moving a device into the group takes effect immediately.
See [AdGuard DNS Filtering](adguard.md).

## Security

The Admin Panel controls access to sensitive TunGuard functionality.

Administrators should:

- Change the default dashboard credentials after installation.
- Protect API keys.
- Revoke API keys that are no longer trusted.
- Keep backups in a secure location.
- Use HTTPS when exposing the dashboard through a public network.
