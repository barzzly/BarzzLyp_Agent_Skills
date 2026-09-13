# Secure service bridge

Use when a Discord bot or worker must write a vetted event into a website database.

1. Generate a separate high-entropy bridge secret locally; store it in both runtime `.env` files with mode `600`, never in source or chat.
2. Keep the bridge route outside browser/admin auth only when it has its own header secret; compare equal-length secrets with `crypto.timingSafeEqual`.
3. Validate event ID, username, product text, and positive integer amount with strict bounds. Reject HTML/control injection and malformed IDs.
4. Make writes idempotent with a unique transaction ID and `INSERT ... ON DUPLICATE KEY` behavior.
5. Store the event in the same transaction/history table used by public leaderboard/profile reads, with an explicit final status and payment method.
6. Return only success and ID; do not expose database or secret details in errors.
7. Build and restart the website process, then verify unauthenticated rejection and read back the exact inserted row through the real history/leaderboard path.
