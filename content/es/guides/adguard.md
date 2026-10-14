---
title: AdGuard DNS Filtering
---

<svg class="tg-figure" viewBox="0 0 720 190" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="Device DNS queries pass through the AdGuard filter before reaching the upstream resolver, and ad and tracker domains are blocked">
  <g class="tg-flow tg-accent" stroke-width="2.4">
    <path d="M180 95h92"/>
    <path d="M420 70h120"/>
  </g>
  <path class="tg-dash" opacity=".5" d="M420 120h90"/>
  <path stroke-width="2.6" d="M460 110l16 16M476 110l-16 16"/>
  <g class="tg-float">
    <circle cx="140" cy="95" r="44" fill="var(--md-default-bg-color)"/>
    <rect x="126" y="76" width="28" height="38" rx="4"/>
    <circle class="tg-blink" cx="140" cy="107" r="1.6" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d2">
    <circle cx="320" cy="95" r="56" fill="var(--md-default-bg-color)"/>
    <path d="M320 60l26 11v20c0 14-10 26-26 30-16-4-26-16-26-30V71l26-11z"/>
    <path class="tg-draw tg-accent" style="--tg-len:26" d="M308 90l8 8 18-20"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="560" cy="70" r="40" fill="var(--md-default-bg-color)"/>
    <path d="M548 76a9 9 0 0 1 1-16 11 11 0 0 1 20-1 7 7 0 0 1 1 14z"/>
  </g>
</svg>

<p class="tg-cap">Queries are filtered before they resolve. Ads and trackers never load.</p>

TunGuard can run a managed [AdGuard Home](https://github.com/AdguardTeam/AdGuardHome)
instance to filter DNS for the devices on your VPN. It is installed and tuned
for you, so a phone under full-tunnel WireGuard gets ad-blocking without any
client-side setup.

## How it works

AdGuard Home is **not embedded** in the TunGuard binary. It runs as a separate
child process that TunGuard manages:

- If the `adguardhome` binary is missing, TunGuard finds one next to its own
  executable, in `DATA_DIR`, in `cwd`, `/usr/local/bin`, or `/usr/bin`; if none
  is found it downloads the official AdGuard Home release (per architecture)
  and installs it.
- Its configuration lives in `AdGuardHome.yaml` inside `ADGUARD_DATA_DIR`
  (defaults to `DATA_DIR`). TunGuard re-applies the settings it owns on every
  start — the DNS bind address/port, the dashboard login, and defaults such as
  the upstream resolver — while leaving everything else in the file alone.
- The AdGuard web admin UI is bound to **loopback only** (`127.0.0.1:1116` by
  default). You reach it through the dashboard at `/adguard-ui/`, or straight
  from the server with:

  ```text
  http://127.0.0.1:1116
  ```

- The dashboard login is mirrored into AdGuard's own admin accounts (password
  stored as a bcrypt hash). Changing the dashboard password restarts AdGuard so
  the new login applies.

AdGuard is **enabled by default** (`ADGUARD_ENABLED=true`). It starts when
TunGuard starts and stays out of the way until you actually give a policy group
the AdGuard capability.

## DNS for clients

When a peer belongs to a group with the **AdGuard DNS filtering** capability
turned on, the WireGuard configuration that TunGuard generates for it points at
AdGuard:

```ini
DNS = 10.100.0.1
```

The value is the **server's tunnel address** (from `WG_ADDRESS`, port 53),
never loopback — a phone cannot reach `127.0.0.1` on your server.

For every other peer, the generated configuration keeps using the default
resolver (`1.1.1.1` by default, or whatever `dns` you pass to
`generate-config`/`peer config`).

## DNS interception on the server

Reading a filter address out of the client profile only works while a profile
is generated, so a device moved into an AdGuard group **after** it was set up
kept its old DNS and ads kept showing. Since `2.4.17` TunGuard enforces AdGuard
group membership on the server instead, with a dedicated iptables chain:

```text
# nat table, per AdGuard-group peer, both protocols:
-A TUNGARD_DNS -s <peer ip> -p udp --dport 53 -j DNAT --to-destination <adguard host>:53
-A TUNGARD_DNS -s <peer ip> -p tcp --dport 53 -j DNAT --to-destination <adguard host>:53
```

Every port-53 query from an AdGuard-group peer is redirected to the AdGuard
listener, **whatever DNS server its profile names**. The set of rules is rebuilt
whenever it could change:

- on every policy group change (create, update, delete, assign, unassign,
  apply);
- on every peer change (add, remove, config generation);
- when AdGuard is started or stopped;
- after a backup restore and at startup.

It is removed on shutdown. The rules only exist for peers with an IPv4 tunnel
address whose group allows AdGuard, and only while AdGuard is actually running,
so a stopped AdGuard leaves every peer's DNS untouched.

### Automatic protection

Practically this means:

1. Generate a phone's WireGuard profile once (any DNS — even `1.1.1.1`).
2. Import it, connect, browse — unfiltered.
3. On the **Policy** page, move the phone into the AdGuard group.
4. From the next query on, the phone's ad-related DNS is blocked — **no new
   profile, no re-import, no client change**.

Moving the phone back to Default turns interception off again.

/// warning | Android Private DNS bypasses the redirect

Android's **Private DNS** setting (DNS-over-HTTPS / DNS-over-TLS) encrypts
queries and does **not** use port 53. Port-53 interception cannot see those
queries.

To filter an Android device, set **Private DNS** to **Off** (or **Automatic**)
in its network settings so its queries actually go to the DNS server the VPN
profile configures. Keep it Off, and the moment the device is in an AdGuard
group its traffic is filtered, with no profile change.

///

## Public resolver (DoH and DoT)

The VPN path filters the devices on your tunnel. You can also expose the **same**
AdGuard filter to the wider internet as a public resolver, without any VPN
client, by mapping a domain to it as a `dns` backend:

```text
domain add dns.example.com --dns
```

That serves:

- **DNS-over-HTTPS** at `https://dns.example.com/dns-query`
- **DNS-over-TLS** at `dns.example.com:853`
- A landing page at the root explaining both endpoints

Only `/dns-query` is proxied to AdGuard: its admin UI and login are never
reachable through the mapped domain. This is covered in full in
[Domains & HTTPS Proxy](domains.md#serving-a-public-dns-resolver-doh-dot).

A few things worth knowing:

- It is the **same resolver**: the blocklists, custom rules and upstreams you
  configure in the AdGuard web UI apply to public and VPN queries alike.
- TLS is terminated by TunGuard, so AdGuard's DoH follows the tunnel-style
  setup internally; you do not configure DoT or the public certificate inside
  AdGuard.
- The `dns` backend needs AdGuard to be running. Stop AdGuard and the public
  resolver stops answering (the DoT listener goes down with it).
- It is an **open resolver**. AdGuard's rate limit bounds abuse, but anyone can
  query it. See the [security notes](domains.md#security-notes).

## Policy group integration

The AdGuard DNS filtering capability is a per-group switch, like the other four
policy rules:

| Capability | Effect |
|---|---|
| Allow AdGuard DNS filtering | Port-53 DNS of this group's devices is redirected to AdGuard |

Custom groups deny it by default; the built-in **Default Global Group** also
does **not** grant it, so nothing is filtered until you deliberately create or
turn on an AdGuard group. See [Policy Groups](admin.md#policy-groups).

/// tip | Combine with internet access

The redirect works even if the group blocks internet access, because a device
that only has tunnel access still needs (and gets) filtered DNS. For a normal
"filter everything" phone, turn on **Allow AdGuard DNS filtering** together
with **Allow standard WireGuard internet access**.

///

## Enabling and configuring AdGuard

All settings are environment variables:

| Variable | Default | Description |
|---|---|---|
| `ADGUARD_ENABLED` | `true` | Run the managed AdGuard Home instance |
| `ADGUARD_BINARY` | `adguardhome` | Path or name of the AdGuard Home binary |
| `ADGUARD_DATA_DIR` | `DATA_DIR` | Where `AdGuardHome.yaml` and data live |
| `ADGUARD_DNS_LISTEN` | `<tunnel IP>:53` | Address AdGuard's DNS service binds. Falls back to `127.0.0.1:5353` when `WG_ADDRESS` is unparsable |
| `ADGUARD_WEB_LISTEN` | `127.0.0.1:1116` | Loopback address of the AdGuard admin UI |
| `ADGUARD_UPSTREAM` | `1.1.1.1` | Upstream resolver AdGuard queries |
| `ADGUARD_UPSTREAM_FAMILY` | `1.1.1.2` | Upstream used while the adult-content filter is on |
| `ADGUARD_FILTER_ADULT` | `false` | Switch AdGuard to family-mode filtering |

`ADGUARD_DNS_LISTEN` normally comes from `WG_ADDRESS`, so AdGuard answers on
the tunnel address (for example `10.100.0.1:53`), which is also what generated
profiles hand to clients and where the redirect sends queries. If you move
WG subnets, the DNS listener moves with them automatically.

When AdGuard's DNS cannot bind the configured tunnel address — for example in
`-mesh-only` mode, where the tunnel does not exist — it falls back to loopback
so the filter still runs.

## Managing AdGuard

### Dashboard

- **AdGuard state** (`running`, `enabled`, UI address): Settings.
- **AdGuard web UI**: reach it in the browser at
  `http://YOUR_SERVER_IP:9000/adguard-ui/` (dashboard login required). From
  there you manage filter lists, blocking rules, and the query log just like a
  standalone AdGuard Home.

### API

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/adguard` | GET | `{enabled, running, web}` |
| `/api/adguard/start` | POST | Start AdGuard |
| `/api/adguard/stop` | POST | Stop AdGuard |
| `/api/adguard/config` | GET/POST | Read the effective `ADGUARD_*` settings |
| `/adguard-ui/` | GET | Reverse proxy to the AdGuard web UI (dashboard login only) |

```shell
curl -H "X-API-Key: $API_KEY" http://localhost:9000/api/adguard
```

### Console

```text
adguard status     state, DNS/Web listen addresses, upstream, adult filter
adguard start      launch the managed AdGuard Home instance
adguard stop       stop it
adguard config     binary, data dir and all ADGUARD_* settings
```

## Verifying that filtering works

With a phone connected and in an AdGuard group:

```text
# From the phone (or any peer in the group), you should see an answer of 0.0.0.0:
dig @10.100.0.1 doubleclick.net

# On the server, the redirect rules should list the phone's tunnel address:
iptables -t nat -S TUNGARD_DNS
```

Then open `/adguard-ui/` → Query Log to watch the blocked lookups arrive in
real time.