# BLE Tag2 Reverse-Engineering Deliverables

This repository is the final documentation bundle for the BLE Tag2 analysis work.

It is meant for someone who did not follow the investigation from the beginning and wants a fast, reliable overview of what was learned, what was inferred from live traces, and what the payload structure means in practice.

## What This Work Covers

The project focused on the BLE Tag2 Android app and the manufacturer payload emitted by BLE Tag2 devices.

The main goal was to understand:

- how the app interprets BLE advertisements
- what the 10-byte manufacturer payload contains
- which fields are stable, which are inferred, and which remain unresolved
- how live sniffing evidence relates to the decompiled app behavior

## What You Will Find Here

- `ble_tag2_decoder_spec.md`: compact payload specification
- `BLE_TAG2_TECHNICAL_README.md`: shorter technical summary for quick orientation
- `ble_tag2_decoder_table.md`: readable field table with notes
- `ble_tag2_decoder_table.csv`: tabular export of the same structure
- `ble_tag2_decoder_schema.json`: schema for decoded payloads
- `ble_tag2_decoder.py`: executable decoder
- `ble_tag2_decoder_pseudocode.py`: simplified pseudocode version
- `cable_ble_tag2_reverse_notes.md`: extended analysis with evidence and trace notes
- `ble_tag2_payload_report.pdf`: polished report version
- `ble_tag2_white_paper.pdf`: cleaner white-paper style version
- `html/index.html`: navigation hub for the rendered HTML versions
- `html/*.html`: rendered HTML outputs for browser reading

## Core Finding

The recovered BLE Tag2 manufacturer payload is 10 bytes long.

Current working interpretation:

- `byte 0`: button press counter
- `byte 1`: battery percentage
- `byte 2`: fast polling flag
- `bytes 3..4`: `upTimeFast`, little-endian
- `bytes 5..6`: `upTimeSlow`, little-endian
- `bytes 7..8`: `connectionCounter`, little-endian
- `byte 9`: firmware-side mode/event latch

Multi-byte fields use little-endian encoding. Single-byte fields are endian-independent.

## How To Use This Repo

- Start with `html/index.html` if you want the browser-friendly version.
- Read `ble_tag2_decoder_spec.md` for the concise field map.
- Use `cable_ble_tag2_reverse_notes.md` if you want the full evidence trail and the live-sniff reasoning.
- Use `ble_tag2_decoder.py` when you want to decode raw payloads locally from the command line.

## Project Boundaries

This repository contains derived documentation and tooling only.

It does not include the original closed-source Android app source code or device firmware source.

## License

This repository is licensed under the GNU General Public License v3.0 or later.
See [`LICENSE`](./LICENSE) for the full text.
