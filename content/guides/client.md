---
title: TunGuard Client
---

The TunGuard client is a small, fully remote-orchestated binary. It starts in the
background, opens one **outbound** connection to your TunGuard server, identifies itself
with a shared key, and then does nothing until the server sends a command.

It is a *dumb pipe*: no config file to edit, no routes to configure, no service to
manage, and no local state beyond two small files. Everything it should be doing is
decided by the server.

The client is what joins a [P2P mesh](../examples/tutorials/p2p.md).

/// note | Not a VPN client

`tun` does not implement WireGuard, does not create a `tun0` interface, and does not
give you a VPN. Devices on the **Peers** page of the dashboard join the VPN with an
ordinary WireGuard configuration. Devices on the **P2P** page run `tun` and form a
direct mesh. The two are independent.

///

## Install

On Linux, macOS, Windows, and Termux, run:

```bash
curl -fsSL https://raw.githubusercontent.com/TunGuard/get/main/client.sh | bash
```

The installer detects the platform and architecture, downloads the matching binary from
the [TunGuard/client](https://github.com/TunGuard/client) releases, verifies its
SHA-256 checksum, and links it as `tun`.

| Platform | Installs to |
|---|---|
| Linux, macOS | `~/.local/bin/tun` |
| Termux / Android | `$PREFIX/bin/tun` |
| Generic Android (adb) | you choose the path |

If the install directory is not on your `PATH`, the installer prints the line to add.
On Termux that is usually:

```bash
export PATH="$PREFIX/bin:$PATH"
```

/// warning | Download location on Android

Android's W^X and SELinux policies prevent a binary from being executed off the SD
card (`/sdcard`, `/storage/emulated`). It has to live in app-private storage or
somewhere like Termux's `$PREFIX/bin`. The installer already handles Termux; for other
Android setups, push it yourself:

```bash
adb push tun_android_arm64-v8a /data/local/tmp/tun
adb shell chmod +x /data/local/tmp/tun
adb shell /data/local/tmp/tun YOUR_SERVER_IP YOUR_PSK
```

///

## Run it

```bash
tun <control-server-ip> <psk>
```

For example:

```bash
tun 203.0.113.10 secretkey99
```

The `<psk>` is the group key from the **P2P → Enroll device** dialog. Anyone holding it
joins your group, so treat it as a credential.

The client double-forks into the background and returns you to the shell. On Windows it
stays in the foreground unless `TUN_FOREGROUND=1` is set, so run it from a scheduled
task or keep the window open.

Once it is running you never need to touch it again. It reconnects on its own if the
server goes away, and it re-establishes the mesh after a reboot.

## Check that it is running

The client is silent by design, so verify it three ways:

```bash
# 1. the process is alive — this is the reliable health check
pgrep -laf tun
# or
ps -ef | grep [t]un

# 2. the control connection to your server:7000 is established
ss -tnp | grep tun        # Linux
netstat -tnp | grep tun   # macOS

# 3. it is connected to the dashboard — check the P2P page on the server
```

The `ESTABLISHED` socket is the confirmation that the client is currently talking to
the server. Note that the process stays alive even when the control link is down — it
reconnects every ~2s, and every ~5s while the server is unreachable — so `pgrep` is the
check that actually tells you something.

To stop it:

```bash
pkill -x tun        # by exact process name
```

/// note | The process name is the binary name

If you renamed the binary, use the new name in `pgrep` and `pkill`.

///

## State

The client keeps everything it needs in one directory, `~/.tun` by default:

```ini
# connection  (mode 0600 — holds the shared secret)
server=203.0.113.10
psk=secretkey99

# device_id  (8 hex chars — this node's identity in the mesh)
6bb8a291
```

`device_id` is generated once and is what lets a reconnecting device reclaim its record
instead of appearing as a stranger. **Do not delete this directory** — if you do, the
node re-registers under a new identity and the server keeps the old record as a ghost
until you remove it.

Run the client with no arguments to reuse the saved server and key:

```bash
tun
```

To put the directory somewhere else — useful on a read-only install path — either set
the environment variable or pass a third argument:

```bash
TUN_STATE_DIR=/var/lib/tun tun
tun 203.0.113.10 secretkey99 /var/lib/tun
```

Missing directories, including nested ones, are created. Re-running `tun <ip> <psk>`
re-points the client at a new server and rewrites both the state files and the boot
hook.

## Survives a reboot

On its first successful run as `root` (or an elevated shell on Windows), the client
installs a boot hook for the platform it is on. Each one is best-effort and silently
skipped when it does not apply:

| Platform | Boot hook |
|---|---|
| Linux | `/etc/systemd/system/tun.service`, enabled with `systemctl` |
| Windows | `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\Run\tun` |
| Android | `/data/adb/service.d/tun.sh`, which Magisk runs as root at boot |

The hook records the absolute path of the binary *and* the state directory, because it
re-runs the client with no arguments and could not otherwise find a non-default state
directory.

```bash
# check what got installed
systemctl status tun     # Linux
ls -l /data/adb/service.d/tun.sh   # Android
```

Because boot hooks supervise the process directly, the client skips its double-fork
when `TUN_FOREGROUND=1` is set. That is what the systemd unit uses; a manual
`tun <ip> <psk>` still backgrounds as before.

## What the client does

The client only relays sockets. It never changes routing, never opens a tunnel device,
and never writes a config.

| Session | What the operator sees |
|---|---|
| Control link | One outbound TCP connection to `server:7000` |
| P2P hub | One UDP socket registered with `server:7001` |
| P2P peer | One UDP socket per peer, with constant keepalive traffic |
| FRP | A local listener whose connections are forwarded to the server |
| TRP | A TCP pair the server asks the client to pump |
| After reset | Every listener and socket is gone; the node is idle |

Toggling is seamless. A new command replaces the previous session for that type, and a
reset always stops everything.

/// note | The protocol

The wire format — command bytes, the 17-byte frame layout, and the status report the
client sends upward every five seconds — is documented in
[P2P Mesh](../examples/tutorials/p2p.md#how-it-works-on-the-wire).

///

## Build from source

The client is a single C file with no dependencies beyond libc.

```bash
git clone https://github.com/TunGuard/client.git
cd client
make          # builds ./tun for your host
```

Per-platform targets:

```bash
make linux      # static musl builds for x86_64 and arm64
make macos      # x86_64 and arm64
make windows    # MinGW-w64, x86_64 and i686
make android    # NDK, arm64-v8a / armeabi-v7a / x86_64
make release    # everything
```

Linux binaries are statically linked against musl, so they have no libc dependency at
all. macOS uses Apple clang, Windows uses MinGW-w64. Android is built through the NDK
and links against **bionic**, never glibc:

```bash
export ANDROID_NDK_HOME=$HOME/Android/Sdk/ndk/27.2.12479018
make android
```

Android binaries are PIE and dynamically linked against the device's own `libc.so`.
That is deliberate: bionic refuses to run statically linked executables on ARM/ARM64
below API 29, and every device already ships the loader and libc. All Android ABIs
target **minSdk 21** (Android 5.0+).

Releases for every platform are published on the
[TunGuard/client](https://github.com/TunGuard/client) releases page, which is what
`client.sh` downloads from.

## Limitations

- **The PSK is sent in cleartext** over the control channel and stored on disk in the
  state directory. On hostile networks, wrap the control link in a tunnel or encrypt
  above it. The handshake is always outbound, so NAT and firewalls never block it.
- **Routers are not a target.** Consumer router firmware (RouterOS, OpenWrt) is
  deliberately unsupported: this client relays sockets and never creates a `tun0`
  interface, so sideloading it onto locked-down firmware is not automatable. Point a
  supported host at the control server instead.
- **BSD is not in the release matrix.** Only Linux, macOS, Windows, and Android are
  built.
- **No state beyond the two files** in the state directory. The server stays the single
  source of truth for what every pipeline should be doing.

## Next steps

- [P2P Mesh](../examples/tutorials/p2p.md) — how the mesh is built, punched, and
  relayed, and how to drive it from the dashboard or the API.
- [Configuration](../advanced/config/conf.md#p2p-control-plane) — the server-side
  control-plane settings this client connects to.
