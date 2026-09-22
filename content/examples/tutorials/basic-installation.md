---
title: Public Access
---

TunGuard makes devices connected to the VPN reachable from the server.

This means you can run a service on a VPN-connected device and expose it publicly using the web server or reverse proxy of your choice.

TunGuard does not need to manage your web server, DNS, domains, or TLS.

## How It Works

Suppose a device connected to TunGuard has the VPN address:

```text
10.100.0.2
```

and runs a web application on port:

```text
8080
```

The service is reachable from the TunGuard server at:

```text
http://10.100.0.2:8080
```

You can then configure your web server to forward public requests to that address.

The traffic flow is:

```text
Internet
   |
   v
Your Domain
   |
   v
Web Server / Reverse Proxy
   |
   v
TunGuard VPN
   |
   v
10.100.0.2:8080
```

TunGuard provides the network connection between the server and the device. Your web server handles everything related to public HTTP/HTTPS access.

## Nginx

For example, if you use Nginx:

```nginx
server {
    listen 80;
    server_name app.example.com;

    location / {
        proxy_pass http://10.100.0.2:8080;
    }
}
```

Requests to:

```text
http://app.example.com
```

are forwarded through the TunGuard VPN to:

```text
10.100.0.2:8080
```

## HTTPS

HTTPS can be configured normally on your web server.

For example, your Nginx configuration can terminate TLS and proxy the traffic through TunGuard:

```nginx
server {
    listen 443 ssl;
    server_name app.example.com;

    ssl_certificate /etc/letsencrypt/live/app.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/app.example.com/privkey.pem;

    location / {
        proxy_pass http://10.100.0.2:8080;
    }
}
```

TunGuard does not need to handle the certificate or TLS connection.

## Caddy

Caddy can be configured in the same way.

```text
app.example.com {
    reverse_proxy 10.100.0.2:8080
}
```

Caddy handles the public HTTPS connection while TunGuard provides the private network path to the device.

## Any Web Server

You are not limited to Nginx or Caddy.

Any web server or reverse proxy that can connect to the TunGuard VPN address can be used, including:

- Nginx
- Caddy
- Apache
- Traefik
- HAProxy
- Other reverse proxies

No TunGuard-specific integration is required.

## Multiple Services

Multiple devices and services can be exposed using different domains or paths.

For example:

```text
app.example.com    → 10.100.0.2:8080
api.example.com    → 10.100.0.3:3000
camera.example.com → 10.100.0.4:80
```

Each service remains on its own VPN-connected device while the public web server controls how traffic reaches it.

## Requirements

The TunGuard server must be able to reach the peer's VPN address.

For example:

```text
10.100.0.2:8080
```

You do not need to expose the device's service port directly to the internet.

Only the public web server needs to be exposed.

## Security

Public access is controlled by your web server and the service itself.

Before exposing a service publicly:

- Use HTTPS for public web applications.
- Protect applications that require authentication.
- Do not expose administrative services unnecessarily.
- Keep the application and web server updated.
- Restrict access using your web server's firewall or authentication features where appropriate.
