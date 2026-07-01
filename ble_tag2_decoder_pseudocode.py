def parse_ble_tag2_payload(payload: bytes) -> dict:
    """
    Parse the BLE Tag2 manufacturer payload observed in the CaBLE 4.9 app.

    Expected layout (10 bytes):
      0: buttonPressCounter
      1: batteryPercent
      2: fastPolling
      3..4: upTimeFast (little-endian)
      5..6: upTimeSlow (little-endian)
      7..8: connectionCounter (little-endian)
      9: modeLatch
    """

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
    }

    if len(payload) >= 5:
        result["upTimeFast"] = payload[3] | (payload[4] << 8)
    if len(payload) >= 7:
        result["upTimeSlow"] = payload[5] | (payload[6] << 8)
    if len(payload) >= 9:
        result["connectionCounter"] = payload[7] | (payload[8] << 8)
    if len(payload) >= 10:
        result["modeLatch"] = payload[9]

    return result


def is_active_window(parsed: dict) -> bool:
    """
    Heuristic: modeLatch=1 indicates a transient active/event window.
    """

    return parsed.get("modeLatch") == 1


def format_summary(parsed: dict) -> str:
    return (
        f"b0={parsed['buttonPressCounter']} "
        f"b1={parsed['batteryPercent']} "
        f"b2={parsed['fastPolling']} "
        f"b9={parsed['modeLatch']}"
    )
