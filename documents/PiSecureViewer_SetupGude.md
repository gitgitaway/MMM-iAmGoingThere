# PiSecureViewer Setup Guide: Secure Remote Access via Cloudflare Tunnel

This guide explains how to expose your MagicMirror module securely to your friends using a Cloudflare Tunnel, bypassing guest network restrictions and ensuring only authorized users can access the interface.

## 1. Install cloudflared on Raspberry Pi

Run the following commands to install the Cloudflare Tunnel client:

```bash
# Download the Cloudflare GPG key
sudo mkdir -p --mode=0755 /usr/share/keyrings
curl -fsSL https://pkg.cloudflare.com/cloudflare-main.gpg | sudo tee /usr/share/keyrings/cloudflare-main.gpg >/dev/null

# Add the Cloudflare repository
echo 'deb [signed-by=/usr/share/keyrings/cloudflare-main.gpg] https://pkg.cloudflare.com/cloudflared bullseye main' | sudo tee /etc/apt/sources.list.d/cloudflared.list

# Install cloudflared
sudo apt update
sudo apt install cloudflared
```

## 2. Authenticate and Create Tunnel

1.  **Login**: Run the following command and follow the URL displayed to authorize your Cloudflare account:
    ```bash
    cloudflared tunnel login
    ```
2.  **Create Tunnel**: Give your tunnel a name (e.g., `magicmirror-tunnel`):
    ```bash
    cloudflared tunnel create magicmirror-tunnel
    ```
    *Note: Take note of the Tunnel ID (UUID) generated.*

## 3. Point Tunnel to MagicMirror

Create a configuration file to tell Cloudflare where to send the traffic:

```bash
mkdir -p ~/.cloudflared
nano ~/.cloudflared/config.yml
```

Paste the following content (replace `<TUNNEL_ID>` with your UUID and `<USER>` with your pi username):

```yaml
tunnel: <TUNNEL_ID>
credentials-file: /home/<USER>/.cloudflared/<TUNNEL_ID>.json

ingress:
  - hostname: our-trip.yourdomain.com
    service: http://localhost:8080
  - service: http_status:404
```

## 4. Assign Domain and Route DNS

Route your domain/subdomain to the tunnel:
```bash
cloudflared tunnel route dns magicmirror-tunnel our-trip.yourdomain.com
```

## 5. Set Up Cloudflare Access (The "Security" Part)

To restrict access to only your 5 friends:
1.  Go to the [Cloudflare Zero Trust Dashboard](https://one.dash.cloudflare.com/).
2.  Navigate to **Access** -> **Applications**.
3.  Click **Add an Application** -> **Self-hosted**.
4.  **Application Name**: MagicMirror Mobile.
5.  **Domain**: `our-trip.yourdomain.com`.
6.  **Policies**: Create a policy named "Friends Access".
    *   **Action**: Allow.
    *   **Include**: Selector = **Emails**.
    *   **Value**: Enter the 5 email addresses of your friends.
7.  **Authentication**: Ensure "One-time PIN" is enabled.

## 6. Run as a Service

Ensure the tunnel starts automatically when the Pi boots:
```bash
sudo cloudflared --config /home/<USER>/.cloudflared/config.yml service install
sudo systemctl start cloudflared
sudo systemctl enable cloudflared
```

## 7. MagicMirror Configuration Change

For the tunnel to work, you **must** update your `config/config.js` to allow connections from the tunnel:

```javascript
address: "0.0.0.0",
ipWhitelist: [], 
```
*(Security is handled by Cloudflare, so whitelisting `0.0.0.0` is safe behind the tunnel).*
