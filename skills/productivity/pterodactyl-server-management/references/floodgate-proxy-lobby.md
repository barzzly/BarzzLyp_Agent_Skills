# Floodgate proxy, lobby and model bridge

- Inspect every server on the actual connection route when send-floodgate-data:true prevents joining. A default Lobby without Floodgate rejects forwarded Bedrock data before a correctly configured ECO RPG backend can be reached. Verify plugin inventory rather than treating HTTP 500 contents errors as absence.
- Compare exact key.pem bytes across proxy and backend privately; do not regenerate matched keys or expose key contents. GeyserModelEngine floodgate hook requires backend recognition, so disabling forwarding is not a complete model fix.
- Download Floodgate Spigot from official Geyser metadata, pin version/build and verify SHA-256. Use official embedded config with explicit prefix, key filename and linking behavior. Upload proxy key to authorized Lobby, not sibling servers outside scope. Obtain restart approval before activation.
- For JARs rejected by files/contents with HTTP 400, use files/download signed URL to read back binary and verify hash; do not upload twice after a successful upload.
- Confirm fresh Floodgate load/enable and server Done plus unchanged key after restart. Separate unrelated startup errors from installation success. Real Bedrock login, server transfer and ModelEngine rendering still require end-to-end client verification.
