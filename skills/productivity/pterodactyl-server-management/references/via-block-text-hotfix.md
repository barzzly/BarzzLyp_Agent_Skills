# ViaBackwards legacy block text mitigation

- Diagnose exact `Protocol1_21_5To1_21_4` direction; this is ViaBackwards downgrading, not the unrelated forward-conversion issue.
- Test exact live ViaVersion/ViaBackwards JARs. An empty CompoundTag in sign `messages` or block `CustomName` reproduces `MergedCodecException` with `Expected StringTag`, `Expected ListTag/NumberArrayTag`, and `No codec could deserialize the given map`. This reproduction identifies a failure class, not proof of exact live packet input.
- Inspect actual region block entities read-only; valid stored signs do not exclude plugin-generated malformed packets.
- Compare upstream commits before updating. A newer snapshot without a relevant fix is not evidence that updating solves it.
- If authorized mitigation is needed, scope fallback to ViaBackwards `BlockPacketRewriter1_21_5` sign/front/back/filtered lines and CustomName. Catch only mcstructs CodecException, preserve valid components/unrelated tags and source world, warn once, replace invalid client-visible text with safely serialized literal or empty string. Do not swallow arbitrary protocol failures.
- Test real block rewriter with malformed compounds plus valid styled text, sign/hanging sign, front/back and filtered messages, CustomName and untouched unrelated tags. Verify original RED and patched GREEN against exact JARs. Guava may be provided by proxy and must be included in isolated test classpath.
- A JRE with `jdk.compiler` but no javac executable can compile via a tiny source launcher calling `ToolProvider.getSystemJavaCompiler().run(...)`; compile harness explicitly when source launcher misreports `IllegalArgumentException: 0 > -7`.
- Package only changed class and compare every other archive entry byte-for-byte. Repeat tests against final archive, stage outside `/plugins`, and read back SHA-256.
- Respect no-restart preference: staging is not activation. Ask before disconnecting proxy players, swap backed-up JAR only while proxy is stopped, verify new startup and native affected-client join before claiming live fix. Label fallback as mitigation until faulty producer/block is identified.
