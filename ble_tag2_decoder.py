#!/usr/bin/env python3
"""
BLE Tag2 advertisement decoder.

Supports:
- hex string input via arguments
- hex string input via stdin
- parsing log lines that contain an mfg=... field

Examples:
  python ble_tag2_decoder.py "05 64 01 0a 00 5f 00 00 00 01"
  echo "05 64 01 0a 00 5f 00 00 00 01" | python ble_tag2_decoder.py
  python ble_tag2_decoder.py --watch < live_scan.log
"""

from __future__ import annotations

import argparse
import re
import sys
from typing import Iterable, Optional


HEX_BYTE_RE = re.compile(r"(?i)\b(?:[0-9a-f]{2}\s+){2,9}[0-9a-f]{2}\b")
MFG_RE = re.compile(r"(?i)mfg=((?:[0-9a-f]{2}\s+){2,9}[0-9a-f]{2})")


def hex_to_bytes(hex_text: str) -> bytes:
    cleaned = hex_text.replace("-", " ").strip()
    if not cleaned:
        return b""
    return bytes(int(part, 16) for part in cleaned.split())


def decode_payload(payload: bytes) -> dict:
    if payload is None or len(payload) < 3:
        raise ValueError("payload too short")

    result = {
        "payload_hex": " ".join(f"{b:02x}" for b in payload),
        "buttonPressCounter": payload[0],
        "batteryPercent": payload[1],
        "fastPolling": payload[2],
        "upTimeFast": None,
        "upTimeSlow": None,
        "connectionCounter": None,
        "modeLatch": None,
        "active_window": None,
    }

    if len(payload) >= 5:
        result["upTimeFast"] = payload[3] | (payload[4] << 8)
    if len(payload) >= 7:
        result["upTimeSlow"] = payload[5] | (payload[6] << 8)
    if len(payload) >= 9:
        result["connectionCounter"] = payload[7] | (payload[8] << 8)
    if len(payload) >= 10:
        result["modeLatch"] = payload[9]
        result["active_window"] = payload[9] == 1

    return result


def format_decoded(parsed: dict) -> str:
    parts = [
        f"payload={parsed['payload_hex']}",
        f"b0={parsed['buttonPressCounter']}",
        f"b1={parsed['batteryPercent']}",
        f"b2={parsed['fastPolling']}",
        f"upTimeFast={parsed['upTimeFast']}",
        f"upTimeSlow={parsed['upTimeSlow']}",
        f"connectionCounter={parsed['connectionCounter']}",
        f"modeLatch={parsed['modeLatch']}",
    ]
    if parsed.get("active_window") is not None:
        parts.append(f"active_window={parsed['active_window']}")
    return " | ".join(parts)


def extract_payloads(text: str) -> list[str]:
    payloads: list[str] = []

    for match in MFG_RE.finditer(text):
        payloads.append(match.group(1).strip())

    if payloads:
        return payloads

    for match in HEX_BYTE_RE.finditer(text):
        payloads.append(match.group(0))

    return payloads


def decode_text(text: str) -> Iterable[str]:
    for payload_hex in extract_payloads(text):
        payload = hex_to_bytes(payload_hex)
        if len(payload) < 3:
            continue
        try:
            yield format_decoded(decode_payload(payload))
        except ValueError:
            continue


def main(argv: Optional[list[str]] = None) -> int:
    parser = argparse.ArgumentParser(description="Decode BLE Tag2 manufacturer payloads.")
    parser.add_argument("hex", nargs="*", help="Hex bytes, e.g. '05 64 01 0a 00 5f 00 00 00 01'")
    parser.add_argument("--watch", action="store_true", help="Read stdin line by line and decode any payloads found.")
    args = parser.parse_args(argv)

    if args.hex:
        payload = hex_to_bytes(" ".join(args.hex))
        print(format_decoded(decode_payload(payload)))
        return 0

    if args.watch:
        for line in sys.stdin:
            for decoded in decode_text(line):
                print(decoded)
        return 0

    stdin_text = sys.stdin.read().strip()
    if stdin_text:
        decoded_any = False
        for decoded in decode_text(stdin_text):
            print(decoded)
            decoded_any = True
        if decoded_any:
            return 0
        payload = hex_to_bytes(stdin_text)
        print(format_decoded(decode_payload(payload)))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
