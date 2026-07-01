# BLE Tag2 Deliverables

This repository contains the final output of the BLE Tag2 reverse-engineering work.

## What Is Here

- `ble_tag2_decoder_spec.md`: compact payload specification
- `BLE_TAG2_TECHNICAL_README.md`: short technical summary
- `ble_tag2_decoder_table.md`: human-readable payload table
- `ble_tag2_decoder_table.csv`: tabular data export
- `ble_tag2_decoder_schema.json`: JSON schema for decoded payloads
- `ble_tag2_decoder.py`: executable Python decoder
- `ble_tag2_decoder_pseudocode.py`: simplified decoder pseudocode
- `cable_ble_tag2_reverse_notes.md`: extended reverse-engineering notes
- `ble_tag2_payload_report.pdf`: polished 2-page report
- `ble_tag2_white_paper.pdf`: matching white paper version
- `html/`: rendered HTML versions and navigation index

## Core Payload Interpretation

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

## Best Starting Points

- Open `html/index.html` for the HTML navigation hub.
- Read `ble_tag2_decoder_spec.md` for the compact field map.
- Read `cable_ble_tag2_reverse_notes.md` for the longer evidence trail and live-sniff observations.
- Use `ble_tag2_decoder.py` if you want to decode raw payloads from the command line.

## Notes

- The HTML files are rendered from the Markdown sources in this folder.
- The PDF deliverables are the polished report and white paper versions of the same findings.
- The repository root is this `outputs/` directory, so all paths are relative to here.
