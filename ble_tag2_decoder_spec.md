# BLE Tag2 Decoder Spec

## Scope

This spec describes the manufacturer payload observed on `BLE Tag2` advertisements from the decompiled `CaBLE 4.9` app and live sniffing.

## Payload Shape

- Length observed: 10 bytes
- Endianness for multi-byte fields: little-endian

## Field Map

| Offset | Size | Name | Meaning |
| --- | --- | --- | --- |
| `0` | 1 byte | `buttonPressCounter` | Observed as the byte that increments across button/click traces |
| `1` | 1 byte | `batteryPercent` | Observed as `0x64` in traces that look like 100 percent battery |
| `2` | 1 byte | `fastPolling` | Fast/slow polling flag |
| `3..4` | 2 bytes | `upTimeFast` | Fast-mode uptime/counter |
| `5..6` | 2 bytes | `upTimeSlow` | Slow-mode uptime/counter |
| `7..8` | 2 bytes | `connectionCounter` | Connection/event counter |
| `9` | 1 byte | `modeLatch` | Transient firmware-side state latch |

## Parsing Rules

1. Require at least 3 bytes to accept a manufacturer payload.
2. If payload length is at least 9 bytes, decode bytes `3..8` as little-endian counters.
3. If payload length is exactly 10 bytes, treat byte `9` as an extra state flag.
4. Do not assume byte `9` is a counter. It behaves like a latch:
   - `0 -> 1` around press/event transitions
   - `1 -> 0` after roughly `8-10 s` in the observed traces

## Practical Semantics

- The decompiled app uses generic names, but for `BLE Tag2` the live traces suggest:
  - byte `0` = button press counter
  - byte `1` = battery percentage
- `fastPolling` is the field exposed by the app.
- `modeLatch` is not decoded by the app, but live sniffing shows it tracks an active window and decays back to zero.
- The app does not contain a timer that resets the advertiser payload.

## Example Frames

### Example A

`05 64 01 0a 00 5f 00 00 00 01`

- `buttonPressCounter = 0x05`
- `batteryPercent = 0x64`
- `fastPolling = 0x01`
- `upTimeFast = 0x000a`
- `upTimeSlow = 0x005f`
- `connectionCounter = 0x0000`
- `modeLatch = 0x01`

### Example B

`05 64 01 0a 00 5f 00 00 00 00`

- Same as above, but `modeLatch = 0x00`

## Current Hypothesis

- Byte `9` is a firmware-side mode/event latch, not the press counter itself.
- The decay to zero appears to be driven by the tag state machine, not by the mobile app.
