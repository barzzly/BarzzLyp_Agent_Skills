---
name: paper-plugin-artifact-verification
description: "Use when verifying Paper plugin JAR builds."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux]
metadata:
  hermes:
    tags: [paper, minecraft, gradle, jar, verification]
    category: software-development
---

# Paper Plugin Artifact Verification

## Procedure

1. Inspect source diff before trusting artifact size.
   - Run `git diff --stat`, `git diff --name-status`, and `git diff --check`.
   - Classify deleted files by feature family. A smaller JAR can reflect intentional removal, changed shading, or missing packaged classes; size alone proves none.

2. Build from clean state.
   - Prefer `./gradlew clean build --no-daemon` with one worker.
   - If Gradle fails before source compilation on JDK 25 patch metadata, retry launcher with JDK 21: `JAVA_HOME=/usr/lib/jvm/java-21-openjdk-amd64 PATH=/usr/lib/jvm/java-21-openjdk-amd64/bin:$PATH ./gradlew clean build --no-daemon`.
   - Treat launcher/toolchain failure separately from source compile failure.

3. Inspect final JAR.
   - Record `stat`, `sha256sum`, `jar tf`, entry count, and packaged `plugin.yml`.
   - Search the JAR for intentionally removed classes and retained integration markers. Inspect source and packaged class lists; source compile alone does not prove final packaging.

4. Run tests and state evidence boundaries.
   - Require successful `check`/tests and `git diff --check`.
   - Report compiled, packaged, headless-tested, live-tested, and deployed as separate states. A successful build does not prove removed optional integrations still work.
   - Do not deploy or restart without explicit authorization. When sending a local artifact, use exact plugin filename and provide verified absolute path plus checksum.

## Emergency Class-Level Hotfixing (`jar uf`)

1. Compile class with complete transitive classpath.
   - When compiling a single class patch against a prebuilt plugin JAR without its build repository, include the server's Paper libraries directory (`find <libraries_dir> -name '*.jar' | tr '\n' ':'`). Omission causes `javac` failures for Adventure text types (`Audience`, `HoverEventSource`) referenced in Bukkit interfaces.

2. Run zero-dependency assert test before packaging.
   - Validate edge cases and recursive replacement limits using `java -ea <TestRunner>.java` against the compiled bytecode before JAR modification.

3. Inject and verify bytecode in final JAR.
   - Inject the class into the archive: `jar uf <plugin>.jar <package/path/Class.class>`.
   - Disassemble with `javap -c -cp <plugin>.jar <fully.qualified.Class>` to verify that intended bytecode instructions replaced the original.
   - Back up the remote JAR (`.bak`), upload the patched JAR via panel API, and compare remote SHA-256 against local before authorizing startup.

## Pitfalls

- Do not call a 200 KB or 800 KB size safe without identifying which artifact was measured; build outputs can live in multiple directories.
- Do not restore deleted hooks merely because the JAR shrank; first map deletions to requested scope and confirm retained APIs and tests.
- Do not claim live compatibility from compile output; optional provider behavior needs a runtime test on the authorized Paper server.
