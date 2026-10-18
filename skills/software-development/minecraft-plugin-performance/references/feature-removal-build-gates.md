# Feature Removal Build Gates

Use when removing a performance-heavy feature from a Paper plugin.

1. Map every feature symbol and caller across hooks, API, config, layout state, tests, and descriptors before editing. Keep integrations that serve unrelated behavior, such as item lookup, and remove only feature-specific calls and state.
2. Make one small symbol-family patch at a time. Read exact Java method boundaries first; do not use broad regex or block deletion because adjacent helpers can disappear while signatures still look plausible.
3. After every signature change, search callers, implementations, tests, and API consumers, then run the narrowest compile target. This catches stale guards, duplicate arguments, and test doubles at the smallest diff.
4. Run `git diff --check`, compile with one Gradle worker, run focused tests, and hash the final JAR before deployment. Keep source and artifact undeployed until all gates pass.
5. Gradle Kotlin DSL can fail before Java compilation when the active JDK reports a vendor-specific version string that its embedded parser rejects. Read the full stacktrace and switch to an installed compatible JDK before diagnosing Java source; do not rewrite plugin code for a toolchain bootstrap error.
6. For this user's servers, upload only the verified artifact to `plugins/`, preserve the current JAR as backup, verify remote hash and running state, and never restart unless explicitly requested.
