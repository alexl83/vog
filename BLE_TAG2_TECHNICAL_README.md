# BLE Tag2 Reverse Engineering Summary

This document consolidates the recovered `BLE Tag2` advertisement format, the app-side evidence from `CaBLE 4.9`, and the practical decoder artifacts.

## What We Confirmed

- The app package is `com.zucchettiaxess.bletagtools` version `4.9`.
- `BLE Tag2` advertises a 10-byte manufacturer payload in the traces we captured.
- The app decodes bytes `0..8` but does not decode byte `9`.
- Live sniffing showed byte `9` behaving like a firmware-side latch:
  - it flips `0 -> 1` on press/event transitions
  - it returns `1 -> 0` after roughly `8-10 s` in the observed traces

## Payload Layout

| Offset | Size | Field | Meaning | Confidence |
| --- | --- | --- | --- | --- |
| `0` | `1` | `buttonPressCounter` | Observed button press counter | Medium-high |
| `1` | `1` | `batteryPercent` | Observed battery byte | Medium-high |
| `2` | `1` | `fastPolling` | Fast/slow polling flag | High |
| `3..4` | `2` | `upTimeFast` | Little-endian uptime/counter | High |
| `5..6` | `2` | `upTimeSlow` | Little-endian uptime/counter | High |
| `7..8` | `2` | `connectionCounter` | Little-endian connection/event counter | High |
| `9` | `1` | `modeLatch` | Firmware-side mode/event latch | Medium-high |

## App-Side Evidence

- `Ble_Scan` reads manufacturer data and maps:
  - byte `0` to the first status field
  - byte `1` to the second status field
  - byte `2` to fast polling
  - bytes `3..8` to timing/counter fields
- `Class_Device` keeps a separate `buttonPressed` boolean that is consumed by the UI and is not the same as the payload byte `9`.
- `MyListFragment` uses a 1-second UI refresh timer, but that does not touch the advertiser payload.
- No app-side code path was found that clears byte `9`.

## Live Trace Summary

Observed frames from live sniffing:

- `05 64 01 0a 00 5f 00 00 00 01`
- `05 64 01 0a 00 5f 00 00 00 00`
- `06 64 01 0a 00 5f 00 00 00 01`
- `06 64 01 0a 00 5f 00 00 00 00`

In the button-correlation trace:

- `b0` incremented from `5` to `6`
- `b9` flipped from `0` to `1` within `0.380 s`
- `b9` returned to `0` after about `9.588 s`

## Practical Interpretation

- For `BLE Tag2`, the live traces suggest:
  - byte `0` is the button press counter
  - byte `1` is the battery percentage
- `fastPolling` is the polling-state field the app exposes.
- `modeLatch` is extra firmware-side state that the app ignores.
- The best current hypothesis is:
  - `modeLatch = 1` means an active/event window
  - `modeLatch = 0` means the firmware has returned to a slow/inactive window

## Deliverables

- [Detailed reverse notes](./cable_ble_tag2_reverse_notes.md)
- [Decoder spec](./ble_tag2_decoder_spec.md)
- [JSON schema](./ble_tag2_decoder_schema.json)
- [Python pseudocode](./ble_tag2_decoder_pseudocode.py)
- [CSV table](./ble_tag2_decoder_table.csv)
- [Markdown table](./ble_tag2_decoder_table.md)
- [Executable parser](./ble_tag2_decoder.py)
