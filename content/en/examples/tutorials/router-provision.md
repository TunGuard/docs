---
title: Router Provision
---

Provision a MikroTik RouterOS v7 router and connect it to your TunGuard server without manually configuring WireGuard.

## Open the Provision Generator

Use the [TunGuard Provision Generator](https://mikrotik-provision.vercel.app/) to generate the RouterOS bootstrap script.

The generator requires your TunGuard server address.

Enter either:

```text
vpn.example.com
```

or:

```text
203.0.113.10
```

If your domain is behind Cloudflare, use your server's public IP address instead.

## Generate the Script

1. Open the [TunGuard Provision Generator](https://mikrotik-provision.vercel.app/).
2. Enter your TunGuard server address.
3. Configure any optional settings.
4. Click **Generate Script**.
5. Download the `.rsc` file or copy the generated script.

The generated script handles the router-side provisioning automatically.

It will:

- Create a WireGuard interface
- Generate the router's keypair
- Register the router with TunGuard
- Apply the assigned VPN configuration
- Connect the WireGuard tunnel

## Import the Script

Upload the generated `.rsc` file to your MikroTik router.

Then open the RouterOS terminal and run:

```routeros
/import tunguard-bootstrap.rsc
```

You can also paste the generated script directly into the RouterOS terminal.

## Verify the WireGuard Connection

Check the WireGuard interface:

```routeros
/interface/wireguard/print
```

Check the WireGuard peer:

```routeros
/interface/wireguard/peers/print
```

You should see the router's WireGuard interface and its TunGuard peer.

## Access the Router Through TunGuard

After provisioning, the router receives an address from the TunGuard VPN network.

For example:

```text
TunGuard Server: 10.100.0.1
MikroTik Router: 10.100.0.2
```

You can then use the router's TunGuard address for management:

```text
10.100.0.2
```

For example, WinBox can connect to:

```text
10.100.0.2
```

You do not need the router to have a public IP for this.

## Firewall Rule Order

If the WireGuard tunnel connects but management access or traffic does not work, check the MikroTik firewall rules.

RouterOS processes firewall rules from top to bottom.

Check the rules:

```routeros
/ip firewall filter print
```

If the TunGuard allow rule is below a default drop rule, the traffic can be dropped before reaching the TunGuard rule.

Move the TunGuard rule above the relevant drop rule:

```routeros
/ip firewall filter move <TunGuard-rule-number> <drop-rule-number>
```

Replace the rule numbers with the actual numbers shown on your router.

TunGuard does not automatically reorder firewall rules because existing MikroTik firewall policies vary between installations.

## Multiple Routers

Repeat the provisioning process for each router.

Each router is registered as its own TunGuard peer and receives its own VPN address.

```text
                 TunGuard Server
                 10.100.0.1
                      |
          +-----------+-----------+
          |                       |
     MikroTik 1              MikroTik 2
     10.100.0.2              10.100.0.3
```

## Cloudflare

Do not use a Cloudflare-proxied hostname for the WireGuard server address.

WireGuard uses UDP traffic, while the normal Cloudflare proxy handles HTTP/HTTPS traffic.

Use the TunGuard server's public IP address instead:

```text
203.0.113.10
```

## Provisioning Tool

[Open TunGuard Provision Generator](https://mikrotik-provision.vercel.app/)
