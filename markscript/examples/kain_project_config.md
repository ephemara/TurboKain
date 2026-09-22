# KainProject --- markscript config for Kain projects

@schema "schemas/kain_project_schema.md"

## Metadata
| Property | Value |
|----------|-------|
| Name | my-project |
| Version | 0.1.0 |
| Kind | kain_executable |
| Entry | src/main.kn |
| Target | llvm |
| Profile | debug |

## Dependencies
| Name | Version | Path |
|------|---------|------|
| std | * | -- |
| serde | 1.0 | - |
| blades.markscript | 1.0 | blades/markscript |

## Build
| ArtifactRoot | CacheRoot | SourceRoot |
|-------------|-----------|------------|
| .kain/out | .kain/cache | src |

## Platforms
| OS | Arch | Supported |
|----|------|-----------|
| windows | x86_64 | true |
| linux | x86_64 | true |
| macos | arm64 | true |
| wasm | wasm32 | false |

## Features
| Feature | Enabled | Description |
|---------|---------|-------------|
| networking | true | HTTP and WebSocket support |
| graphics | false | GPU rendering |
| telemetry | true | Metrics and tracing |
| encryption | true | TLS and crypto |
