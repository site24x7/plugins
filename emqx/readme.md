# EMQX Plugin Setup

This project provides plugins for EMQX, an open-source, highly scalable, and cloud-native distributed MQTT broker. EMQX (Erlang MQTT Broker) supports millions of connections and provides real-time messaging, making it ideal for IoT, M2M, and edge computing scenarios. This repository includes plugins compatible with EMQX versions 4 and 5.

## EMQX Version Compatibility

To ensure compatibility, use the plugin corresponding to your version of EMQX:

- **For EMQX v4**: Use the plugin available in the [`v4`](./v4).
- **For EMQX v5**: Use the plugin available in the [`v5`](./v5).

## Checking Your EMQX Version

To identify your current version of EMQX, follow these steps:

1. Open your EMQX dashboard. This is usually accessible at your hosted EMQX URL, such as `http://localhost:18083`.
2. Log in using your account credentials.
3. Navigate to the **Monitor** tab.
4. Under the **Node** section, you will see the EMQX version currently in use.
