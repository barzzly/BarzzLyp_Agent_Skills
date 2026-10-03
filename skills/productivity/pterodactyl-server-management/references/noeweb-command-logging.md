# NoeWebApi command-logging guard

Keep fail-closed guard intact: backend native command logs can capture /webconnect passwords before preprocess sanitization. Set spigot.yml commands.log=false after checking proxy velocity.toml advanced.log-command-executions=false and Essentials socialspy-commands excludes wildcard/webconnect/namespaced alias. Do not bypass guard in JAR or claim no possible third-party logs from these checks alone.

Back up config, edit only commands.log, read back, coordinate restart with online players, verify offline then start and fresh NoeWebApi enabled; requires existing NoeWebAuth signed grants log. Startup proves initialization, not end-to-end web pairing/transfer. Never use real passwords for logging tests or print secrets from bridge config. Preserve authentication secrets and signed grants.
