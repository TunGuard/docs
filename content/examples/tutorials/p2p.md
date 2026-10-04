---
title: P2P Mesh
---

TunGuard can run a peer-to-peer mesh between remote devices. The server introduces
the devices and hands each one the address of the others; the devices then talk to
each other directly, and the server is only used again if a direct path cannot be
opened.

This is a different mechanism from the WireGuard VPN. Peers on the **Peers** page get
a WireGuard configuration and join the VPN subnet. Devices on the **P2P** page run
the TunGuard *client* and form a mesh of direct UDP paths between themselves. Both can
run on the same server at the same time.

/// note | Two different things

WireGuard peers and P2P mesh nodes are unrelated. A mesh node never receives a
`wg0` address, and a WireGuard peer never appears on the P2P page. What they share
is the TunGuard server that runs both subsystems.

///

## The two ports

The mesh control plane is two sockets, both opened by the server:

| Port | Protocol | Purpose |
|---|---|---|
| `7000/TCP` | `CONTROL_LISTEN` | The control channel every client dials out to. This is the port you put in the client command. |
| `7001/UDP` | `RELAY_LISTEN` | The rendezvous hub. Clients register their public endpoint here and ask who else is online. |

Both must be reachable from the internet. The client only ever makes *outbound*
connections, so it works from behind NAT — but the server has to be able to answer on
both ports.

/// warning | Open both ports

If `7001/UDP` is blocked, clients can still connect and appear online, but they can
never learn each other's addresses. Every link then stays relayed at best, and in
practice nothing gets discovered. See [When links stay
relayed](#when-links-stay-relayed).

///

## Install the client

Every device that joins the mesh needs the TunGuard client. The installer picks the
right binary for the machine, verifies its SHA-256 checksum, and links it as `tun`:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/client.sh | bash
```

This installs to `~/.local/bin/tun` on Linux and macOS, and to `$PREFIX/bin/tun` on
Termux. If that directory is not on your `PATH` the installer tells you what to add.

Supported platforms:

| Platform | Architectures |
|---|---|
| Linux | `x86_64`, `arm64` |
| macOS | `x86_64`, `arm64` |
| Windows | `x86_64`, `i686` |
| Android / Termux | `arm64-v8a`, `armeabi-v7a`, `x86_64` |

The client is a single static binary with no runtime dependencies. It is *not* a
`WireGuard` client and does not need a `tun` device, a kernel module, or `root` to
forward traffic — it only relays sockets.

For the full client reference — state files, boot hooks, troubleshooting, and building
from source — see [TunGuard Client](../../guides/client.md).

## Enroll a device

Enrolling gives a device its **PSK**, which is the only thing it needs to join.

1. Open the dashboard and go to **P2P**.
2. Click **Enroll device**.
3. Enter a name, such as `shop-router`.
4. Leave the **PSK** field blank to have one generated, or paste a key you already
   have.

The dialog then shows a ready-to-run command:

```bash
tun YOUR_SERVER_IP YOUR_PSK
```

Copy it and run it on the device. The client forks into the background immediately and
returns you to the shell.

/// tip | The PSK is the group

The PSK is not a per-device password. Devices that share a PSK are a *group*, and a
group auto-meshes: every online member is punched to every other member, with no
further action. Give a set of devices the same PSK to mesh them together, and a
different PSK to keep two sets of devices apart. The dashboard's **Groups** column is
exactly this grouping.

///

## What happens next

Nothing else is required. The mesh builds itself.

```text
 1.  tun <server> <psk>            client dials server:7000
 2.  "<psk>\n<device_id>\n"       identifies itself
 3.  0x07 hub target              server hands over the hub address:7001
 4.  TUN probe every 1s           server learns this device's public endpoint
 5.  P1H every 2s                 "who else is on my PSK?"
 6.  P1R reply                    every online peer with a fresh endpoint
 7.  peer punch                   both ends aim at each other, once a second
 8.  first packet received        link is direct; reported up to the dashboard
 9.  P1T every 3s                 each end tests the link and times the round trip
```

Steps 4 to 8 repeat for the life of the connection. A device that reboots, changes
network, or reconnects is picked up automatically — the server re-runs the group sweep
every five seconds, so a peer that comes online after you is linked without you doing
anything.

## How a direct path is opened

Most devices sit behind NAT, so neither can receive an unsolicited packet from the
other. TunGuard resolves this with a hole punch over UDP.

1. Each client keeps one UDP socket aimed at the hub and sends a small `TUN` probe once
   a second. That traffic is what makes the NAT allocate a public port for it, and the
   hub records the public address the datagrams arrive from.
2. Every other second a client sends a `P1H` rendezvous request to the hub. The server
   replies `P1R` with the id, IP, and port of every online node in the same PSK group
   that has a fresh endpoint.
3. Each client opens one UDP socket per discovered peer, aimed at that peer's recorded
   address, and sends a probe once a second. Both ends now send into each other's NAT
   mapping at the same time, and the packets that arrive open the hole.
4. A link is reported **direct** as soon as a peer socket receives anything at all.
   That is a sound test: hub-bound probes only ever land on the hub socket, so anything
   on a peer socket came straight from the peer.
5. Once the link is direct, each client sends it a `P1T` packet every three seconds and
   times the echo. That is the **link test**, and it is reported separately.

The hub socket is deliberately *not* `connect()`ed to the server. A connected UDP socket
only accepts datagrams from its single peer, so the kernel would silently drop the very
punch that completes the direct path. Using `sendto`/`recvfrom` keeps the NAT mapping
open while still letting a punch land. The hub socket echoes anything that is not a
`P1R` reply back to its sender, so a punch that arrives there instead of on a peer
socket still lets both ends reach the same conclusion.

## When the relay is used

Not every network can be punched. A symmetric NAT on both ends, or a firewall that only
permits traffic to a registered port, will keep a link from opening.

When that happens the server stays in the path. Every pair the server attempts to punch
also gets a relay circuit, and any datagram that arrives on the hub without a `TUN` or
`P1H` header is forwarded to the sender's linked peers. The mesh keeps carrying traffic;
it is just routed through the server instead of going direct.

Both paths exist at the same time. The direct one is preferred because it bypasses the
server, and the relay is the fallback that is always there behind it — there is no
switch to choose between them. A link turns direct the moment a packet genuinely
arrives from the peer, so the **Direct links** figure reflects what is really happening
rather than what was intended.

## Direct is not the same as working

A hole punch is one packet arriving, once. It can succeed against a peer that has since
moved, changed network, or started dropping what it receives — and `direct` stays set,
because it is a fact about the punch and nothing has contradicted it.

The link test is what answers the question you actually care about. Every three seconds
each client sends a 12-byte packet the peer echoes back:

```text
'P','1','T' | node_id(8) | seq(1)
```

The echo of the sequence that is outstanding is what counts, so a late reply to an older
test cannot be mistaken for the current one, and the reply to a punch probe cannot be
mistaken for a test at all. The round trip is timed on a monotonic clock, so an NTP
adjustment cannot invent latency. A test that gets no echo within two seconds drops the
result rather than leaving the old figure on screen.

In the links table this is its own column:

| State | Meaning |
|---|---|
| **direct**, with a time | The peer answers, and the time is the round trip it measured |
| **direct**, *no answer* | The punch completed, but the peer is no longer answering anything |
| **via hub**, not tested | No punch yet, so there is nothing to test |

```text
Direct (preferred)              Relayed (fallback)

  Peer A <========> Peer B        Peer A
     ^          ^                    |
     |          |                    v
     |   hole punch            TunGuard server
     |    + probes                    ^
     |          |                    |
     +----------+                    |
   no server in the path            Peer B
```

## Dashboard

The **P2P** page shows the whole mesh.

- **Devices** — total enrolled nodes, online or not.
- **Groups** — distinct PSKs. Each one is an independent mesh.
- **Direct links** — peer links that have completed a hole punch.
- **Control / hub** — the addresses the control plane is listening on.

Below that, devices are grouped by PSK, each showing its endpoint, the peers it holds,
and how many of those are direct. The links table at the bottom lists every punch
target with its state.

The server-side view of one row:

| Field | Meaning |
|---|---|
| `id` | The node handle every API call needs |
| `device_id` | The client's own stable 8-hex identity, reported on connect |
| `control_ip` | Address the control channel came from |
| `relay_ep` | Public UDP endpoint registered at the hub |
| `relay_seen` | When that endpoint was last refreshed |
| `peers` / `direct_peers` | Peers held, and how many are direct |

A node that shows a `relay_ep` but no direct links is the one to look at first — that
means discovery worked and the punch did not.

## Enrolling from the API

Everything on the P2P page is scriptable. The full reference is in the
[API Reference](../../guides/api.md#p2p-mesh); this is the whole onboarding flow:

```bash
API_KEY="REPLACE_WITH_YOUR_KEY"
API="http://localhost:9000"

# Enroll a device and keep the id and PSK it returns
ADDED="$(curl -sS -X POST \
  -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  "$API/api/mesh/node/add" -d '{"name":"edge-a"}')"

NODE_ID="$(printf '%s' "$ADDED" | python3 -c "import json,sys;print(json.load(sys.stdin)['id'])")"
PSK="$(printf '%s' "$ADDED" | python3 -c "import json,sys;print(json.load(sys.stdin)['psk'])")"

echo "run on the device:  tun YOUR_SERVER_IP $PSK"
```

Useful follow-ups:

```bash
# Watch the mesh come up
curl -H "X-API-Key: $API_KEY" "$API/api/mesh/groups"
curl -H "X-API-Key: $API_KEY" "$API/api/mesh/links"

# Force a re-punch of one pair (both nodes must be online)
curl -X POST -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  "$API/api/mesh/p2p/connect" -d "{\"a\":\"$NODE_ID\",\"b\":\"OTHER_NODE_ID\"}"

# Re-punch a whole group
curl -X POST -H "X-API-Key: $API_KEY" -H "Content-Type: application/json" \
  "$API/api/mesh/p2p/mesh" -d '{"group":"'"$PSK"'"}'
```

/// note | Unknown keys self-enroll

The server does not reject a PSK it has never seen — it registers a new node for it.
That is what makes "run the client with the shared PSK" the entire onboarding flow. It
also means a leaked PSK silently adds a node, so treat it as a credential.

///

## Limits

- **8 peers per node.** A node holds at most 8 simultaneous punches, and the server
  refuses to push a ninth. A group of 9+ devices meshes fine, but each node only
  tracks 8 of its peers.
- **Endpoints expire after 120 seconds.** A peer whose hub traffic stops is no longer
  offered as a punch target, so a stale entry cannot cause a client to probe a dead
  port.
- **Peers are addressed by node id**, not by a server-assigned slot, so both ends of a
  link agree on who they are talking to without extra bookkeeping.

## How it works on the wire

For anyone building tooling against it. Every control frame is exactly **17 bytes**:

```text
[0]      command
[1..8]   payload (8 bytes)
[9..16]  peer node id (8 ASCII hex chars, or '0' padding)
```

| Command | Name | Payload |
|---|---|---|
| `0x00` | Reset | none — drops every FRP, TRP, P2P, and hub session |
| `0x01` | FRP reverse proxy | `local_port` (2B BE) + `remote_port` (2B BE) |
| `0x02` | P2P, legacy single peer | `target_ip` (4 raw) + `target_port` (2B BE) |
| `0x03` | TRP pull reverse proxy | `target_ip` (4 raw) + `service_port` (2B BE) + `public_port` (2B BE) |
| `0x04` | P2P add peer | `target_ip` (4 raw) + `target_port` (2B BE); peer id in the id field |
| `0x05` | P2P drop peer | none; peer id in the id field |
| `0x06` | P2P clear all | none |
| `0x07` | P2P join hub | `hub_ip` (4 raw) + `hub_port` (2B BE); carries the node's **own** id |
| `0x08` | Stop hub | none — drops the rendezvous socket, node stays online |

Ports in a payload are big-endian. The four address bytes are already in network order
and are copied straight into `sin_addr.s_addr`; the client never reorders them.

Hub datagrams, all prefixed with the sender's own 8-character node id so the server
never has to guess who is talking — several devices behind one NAT share a public IP:

```text
'T','U','N' | id(8) | counter(1)     keepalive probe, once a second
'P','1','H' | id(8)                 rendezvous request, every other second
'P','1','R' | count(1) | count x { id(8) | ip(4) | port(2) }
```

Clients also report upward unprompted every five seconds:

```text
[0]      0xFE
[1]      peer count
then count x { node id (8 ASCII hex), flags (1 byte, bit 0 = direct path open) }
```

`0xFE` is never sent by the server, so a frame starting with it is unambiguously a
status report. This is how the dashboard knows which links are genuinely direct.

/// danger | Frame length is load-bearing

A control frame is 17 bytes. Sending only the 10 payload bytes desynchronizes the
stream, and the client reads your next command shifted by seven bytes — which looks
exactly like a client that is ignoring the dashboard.

///

## Running the mesh without WireGuard

The mesh does not need a `tun` device. To run only the control plane and the dashboard —
useful on a host that cannot create a tunnel interface, or when the VPN is not wanted:

```bash
sudo ./tanguard -mesh-only
```

`-mesh-only` implies the dashboard, since the dashboard is the only way to drive the
mesh by hand. The server's help output covers the other flags:

```bash
./tanguard --help
```

The relevant settings are environment variables, documented in
[Configuration](../../advanced/config/conf.md#p2p-control-plane):

| Variable | Default | Description |
|---|---|---|
| `MESH_ENABLED` | `true` | Set to `false` to disable the control plane entirely |
| `CONTROL_LISTEN` | `:7000` | TCP control listener |
| `RELAY_LISTEN` | `:7001` | UDP rendezvous/relay listener |
| `CONTROL_TIMEOUT_S` | `10` | Seconds allowed for the client handshake |
| `MESH_DATA_DIR` | `DATA_DIR` | Where the node registry is stored |

With `MESH_ENABLED=false` the hub never starts and every mesh endpoint returns
`503 tun control plane is disabled`. In `-mesh-only` mode the process refuses to start
at all.

## Verify a link

On the device, the client is silent by design — no logs, no pidfile. Check it this way:

```bash
# the process is alive (this is the reliable health check)
pgrep -laf tun

# the control connection to your server:7000 is established
ss -tnp | grep tun        # Linux
netstat -tnp | grep tun   # macOS
```

For a direct mesh link, you should see the client holding UDP sockets to its peers on
top of the hub socket.

Server-side, the same fact is visible in the log:

```text
[mesh] registered 3f2a1b04 (dev-6bb8a2) in psk group 9c1f… device="6bb8a291" from 203.0.113.10
[mesh] node 3f2a1b04 (dev-6bb8a2) online, control=203.0.113.10 device="6bb8a291"
[p2p]  node 3f2a1b04 reached 7d90ce35 directly (hole punch complete)
```

## Troubleshooting

**A device is online but has no `relay_ep`.**
The client never reached the hub on `7001/UDP`. Check the port is open in the VPS
firewall and security group, and that `ss -ulnp` on the server shows the socket bound.

**Devices are online but no peers are listed.**
They are not sharing a PSK. Peers only ever discover others in their own group, so two
different PSKs means two separate meshes. Compare them on the P2P page.

**A link is listed but never turns direct.**
The hole punch is not getting through. This is normal on symmetric NAT, and it is not a
misconfiguration — the relay is already carrying that link. Confirm `7001/UDP` is
bidirectional (some providers only allow outbound UDP), but otherwise there is nothing
to fix: direct and relayed paths are both maintained for every pair, and the direct one
takes over on its own if it ever opens.

Note that there is no switch to *force* a link onto the relay. `p2p/mesh` with
`"enable": false` clears the peer table, but each client re-learns the same peers from
the next `P1R` reply within a few seconds and starts punching again. Conversely,
`relay/unlink` removes the fallback, which leaves a stuck link with no path at all — use
it to isolate a node, not to pin traffic.

**A link keeps flipping back to relayed.**
The node's endpoint changed, so every direct path that depended on the old mapping was
dropped. This is expected when a device changes network. It re-punches on the next
sweep; a stable link on a stable network does not flip.

**A peer disappeared from the group after restarting it.**
The client lost its device id. It is generated once and stored in its state directory
(`~/.tun` by default), so deleting that directory makes the node reappear as a
stranger. Do not delete it — and see
[TunGuard Client](../../guides/client.md#state) for how to relocate it instead.

**`503 tun control plane is disabled` from every mesh endpoint.**
`MESH_ENABLED=false`, or the server was started without the mesh. `-mesh-only` and a
normal start both bring it up by default.

## Security

- **The PSK is a shared secret and it is sent in cleartext** on the control channel.
  On a hostile network, wrap the control link in a tunnel or encrypt above it. The
  connection is always outbound, so NAT and firewalls never block the handshake itself.
- **Mesh traffic between peers is not encrypted by TunGuard.** The client relays raw
  UDP datagrams. Use the P2P mesh to carry WireGuard — that is, mesh the nodes and run
  WireGuard over the result — if you need confidentiality on the direct path.
- **An unknown PSK self-enrolls.** Anyone holding the key becomes a node. Keep it out
  of shell history and off shared machines, and treat a node you did not enroll as
  suspicious.
- **A relayed link means the server sees the traffic.** Direct paths bypass it
  entirely, which is the main reason to prefer them.

## Next steps

- [TunGuard Client](../../guides/client.md) — installing, running, and verifying the
  client on every supported platform.
- [API Reference](../../guides/api.md#p2p-mesh) — the full mesh API.
- [Configuration](../../advanced/config/conf.md#p2p-control-plane) — every mesh
  environment variable.
