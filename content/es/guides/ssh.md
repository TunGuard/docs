---
title: SSH Access
---

<svg class="tg-figure" viewBox="0 0 720 180" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" role="img" aria-label="An SSH client reaches the server as a jump host, which forwards to the machines on the VPN">
  <g class="tg-flow tg-accent" stroke-width="2.4">
    <path d="M196 90h104"/>
  </g>
  <g class="tg-flow tg-accent tg-d1" stroke-width="2.4">
    <path d="M420 68h124"/>
    <path d="M420 112h124"/>
  </g>
  <g class="tg-float">
    <circle cx="140" cy="90" r="46" fill="var(--md-default-bg-color)"/>
    <rect x="122" y="76" width="36" height="24" rx="4"/>
    <path d="M114 104h52"/>
  </g>
  <g class="tg-float tg-d2">
    <circle class="tg-pulse tg-accent" cx="360" cy="90" r="52" fill="var(--md-default-bg-color)"/>
    <rect x="330" y="66" width="60" height="16" rx="3"/>
    <rect x="330" y="86" width="60" height="16" rx="3"/>
    <rect x="330" y="106" width="60" height="16" rx="3"/>
    <circle class="tg-blink" cx="340" cy="74" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d1" cx="340" cy="94" r="1.6" fill="currentColor" stroke="none"/>
    <circle class="tg-blink tg-d2" cx="340" cy="114" r="1.6" fill="currentColor" stroke="none"/>
  </g>
  <g class="tg-float tg-d3">
    <circle cx="592" cy="68" r="38" fill="var(--md-default-bg-color)"/>
    <rect x="580" y="58" width="24" height="20" rx="3"/>
    <path d="M576 84h32"/>
  </g>
  <g class="tg-float tg-d4">
    <circle cx="592" cy="112" r="38" fill="var(--md-default-bg-color)"/>
    <rect x="580" y="102" width="24" height="20" rx="3"/>
    <path d="M576 128h32"/>
  </g>
</svg>

<p class="tg-cap">One server becomes the jump host for every machine on your VPN.</p>

TunGuard can act as an SSH jump host and gives you three ways to reach the
machines on your VPN: SSH straight through the server with `ssh -J`, an SSH
terminal in the browser from the dashboard, and a built-in `ssh` client in the
dashboard's Terminal.

## The SSH Gateway

The SSH Gateway turns TunGuard into an SSH jump host. Enable it with:

```shell
sudo ./tanguard -web -ssh
```

or set `SSH_ENABLED=true` (the installer's systemd service can also enable it).
It listens on `SSH_LISTEN`, default port **2222**.

It authenticates with the **same login as the web dashboard** — there are no
separate SSH credentials. If you change the username or password under
**Settings → Dashboard Login**, SSH access uses the new login immediately.

The gateway's host key is auto-generated (ed25519) at
`DATA_DIR/ssh_host_key` when `SSH_KEY_FILE=auto`, and is included in backups.

## Reach a peer over the tunnel

Jump through the gateway to any connected peer:

```shell
ssh -J admin@YOUR_SERVER_IP:2222 root@10.100.0.2
```

- `admin@YOUR_SERVER_IP:2222` are your TunGuard **dashboard** credentials and
  the gateway port — this part authenticates to the gateway.
- `root@10.100.0.2` is the peer you are landing on — this part authenticates to
  the peer itself, exactly as if the peer's own SSH were public.

You never have to expose SSH on the device to the internet. You can also jump
to any other host the server can reach: the gateway forwards whatever TCP
`host:port` you ask it to.

/// note | What the gateway forwards

The gateway accepts `direct-tcpip` forwarding to any host and port the server
can reach. That is what makes `ssh -J` work, and it is intentionally broad —
keep the gateway and the dashboard behind a trustworthy network.

///

Use the console's `jump` command to print the exact `ssh -J` line for a peer:

```text
jump laptop
```

## Connect directly to a peer (no jump)

Any peer that runs its own `sshd` can be reached end to end from the server:

```shell
ssh root@10.100.0.2
```

If the peer has a **device label** configured you can use it instead of the IP:

```shell
ssh laptop
```

## SSH from the dashboard (Web SSH)

Next to any **online** peer on the Peers page there is an **SSH** button. It
opens a browser terminal and connects to the peer over a WebSocket
(`/api/ws/ssh`), prompting you for the **peer's own** username and password
(SSH password auth to the target). The browser session and the peer's SSH are
end-to-end encrypted; TunGuard only relays the terminal.

## The built-in SSH client

The dashboard **Terminal** and the SSH gateway's own prompt both include a small
`ssh` client, so you can reach peers (or any host the server can reach) without
a second terminal:

```text
ssh root@10.100.0.5                 interactive session to a peer
ssh laptop                          a peer by its device label
ssh -p 2222 -l alice jumpbox        alternate port / login
ssh -i ~/.ssh/id_ed25519 host       use a specific private key
ssh host uptime                     run one remote command and exit
ssh --password s3cret host          non-interactive password (scripts)
```

- `Ctrl-]` detaches an interactive session and returns to the TunGuard prompt.
- `ssh host command` streams the remote output and reports the remote exit
  status.
- Peers are matched by device label, tunnel address, or key.

## Security notes

- The gateway itself accepts **password authentication only**, using the
  dashboard login. There is no separate SSH user database.
- Anything able to reach the API can also request `/api/ws/ssh`, which opens an
  interactive shell to the target host — keep the dashboard and API off
  untrusted networks, and prefer key-based auth on the peers you manage this
  way.
- For extra hardening of the peers themselves, consider key-based SSH auth on
  the devices (the gateway is only one leg of the connection; the second leg
  authenticates to the peer normally).

## API

| Endpoint | Method | Purpose |
|---|---|---|
| `/api/ws/ssh` | GET (WebSocket) | Browser SSH session to a peer |
| `/api/ws/console` | GET (WebSocket) | The dashboard Terminal |

## See also

- [SSH Gateway configuration](../advanced/config/conf.md#ssh-gateway) —
  `SSH_ENABLED`, `SSH_LISTEN`, `SSH_KEY_FILE`.
- [Console reference](cli.md) for the full CLI, including the `ssh` client and
  `jump` command.