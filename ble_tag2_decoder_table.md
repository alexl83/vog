# BLE Tag2 Payload Table

| Offset | Size | Field | Meaning | Confidence | Notes |
| --- | --- | --- | --- | --- | --- |
| `0` | `1` | `buttonPressCounter` | Observed button press counter | Medium-high | Decompiled app names this generically but live traces suggest click counter behavior |
| `1` | `1` | `batteryPercent` | Observed battery percentage | Medium-high | Commonly seen as `100` in the traces |
| `2` | `1` | `fastPolling` | Fast/slow polling flag | High | App exposes this field directly |
| `3..4` | `2` | `upTimeFast` | Little-endian uptime/counter | High | Observed in extended payloads |
| `5..6` | `2` | `upTimeSlow` | Little-endian uptime/counter | High | Observed in extended payloads |
| `7..8` | `2` | `connectionCounter` | Little-endian connection/event counter | High | Observed in extended payloads |
| `9` | `1` | `modeLatch` | Firmware-side mode/event latch | Medium-high | Flips to `1` on active transitions and decays back to `0` in about `8-10 s` |

## Practical Read

- `buttonPressCounter` is the byte that appears to move with button/click transitions.
- `batteryPercent` is the byte that looks like battery level in the live traces.
- `fastPolling` is the field the app surfaces.
- `modeLatch` is extra firmware-side state that the app does not decode.
- In live traces, `modeLatch` often flips `0 -> 1` with a press-related transition and returns to `0` after roughly `8-10 s`.

## Example

Payload:

`05 64 01 0a 00 5f 00 00 00 01`

Decoded:

- `buttonPressCounter = 0x05`
- `batteryPercent = 0x64`
- `fastPolling = 0x01`
- `upTimeFast = 0x000a`
- `upTimeSlow = 0x005f`
- `connectionCounter = 0x0000`
- `modeLatch = 0x01`
