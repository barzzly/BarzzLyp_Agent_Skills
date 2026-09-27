---
name: velocity-signed-auth-companion
description: Use when building Velocity signed auth companions.
---
# Velocity signed authentication

- Publish exact UTF-8 wire contract before parallel proxy/backend implementation; specify raw-payload HMAC, dedicated secret, challenge lifecycle, expiry, replay and negative semantics.
- Mark both request and response plugin-channel events handled before source checks; accept requests only from exact current ServerConnection targeting its Player and expected backend alias. Never trust payload UUID.
- Mint session UUID on ServerConnectedEvent, but do not assume getCurrentServer is installed in that event: official Velocity TransitionSessionHandler installs it afterward. Pin exact transport on first matching current-server request; reject replacement transport until new event.
- Use backend 2-second challenge polling to trigger live API reads in proxy event handling rather than caching login objects or running HTTP/scheduler profile polls. Velocity async=false does not guarantee one global thread; synchronize own session state and document upstream memory visibility limits.
- Reflect through public API interfaces, not obfuscated implementation classes; load API through required plugin instance classloader, refresh app/profile each request, and fail closed on absence/error/UUID mismatch.
- Test with real official Velocity event classes and JDK interface proxies at runtime boundary. Handwritten premium API fixtures belong only under test sources and must never enter distributable JAR.
- Build public Velocity API from official PaperMC repository and public transitive APIs from Maven Central; use javac --release 17 -proc:none plus explicit velocity-plugin.json when Maven absent. Verify classfile major version, descriptor, empty example secret, and absence of tests/vendor classes in JAR.
- Enforce strictly increasing per-session issuance without inventing future wall-clock timestamps: coalesce equal-millisecond requests into one delayed callback, re-read live login and revalidate exact session/transport/latest challenge before signing, and drop rollback responses without extending old grants. Test deterministic positive at 1000, logout at 1000, deferred negative at 1001 through actual backend verifier.
- Add optional interop test compiling against actual sibling backend verifier source. Exercise signed positive, negative, stale positive replay, new challenge, wrong carrier, expiry, tamper, connection pin and absent heartbeat. Unit/interop tests do not prove live server integration or network ACLs.
