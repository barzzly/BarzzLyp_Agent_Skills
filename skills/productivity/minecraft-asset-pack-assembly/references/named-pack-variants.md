# Metadata-only pack variants

- For OPResourcePack and HDResourcePack, preserve identical assets and compatibility metadata; change only pack.description in pack.mcmeta and ZIP filenames. Exact descriptions: Optimize Resources Pack Noesantara; HighReso Resources Pack Noesantara. Names do not imply actual optimization or higher-resolution assets.
- Encode blue description gradient as vanilla JSON text components with per-character hex colors from #0038FF to #90E0F0, not MiniMessage tags; pack metadata does not parse plugin MiniMessage.
- When passing source ZipInfo to writestr, pass copy.copy(entry). writestr mutates offsets and sizes; reusing source entry objects corrupts in-memory source lookup and causes false overlapped-entry failures during verification.
- Verify CRC, identical archive member sets, unchanged bytes for every member except pack.mcmeta, exact description text and color endpoints, and all non-description metadata unchanged. Keep source untouched unless removal separately authorized.
