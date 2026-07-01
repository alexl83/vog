# caBLE 4.9 Reverse Notes

Source analyzed:
- `/Users/alex/Downloads/CaBLE_4.9_APKPure.xapk`
- Base APK: `com.zucchettiaxess.bletagtools.apk`

## High-level takeaways

- The app is organized around a custom BLE GATT stack, not a generic GATT client.
- The code clearly separates device families:
  - `ZTAG`
  - `TAG_R`
  - `ZTAG_SL`
  - `Proximity`
  - `XIO`
- OTA support is built in and references device-specific firmware blobs:
  - `otafileTag2.gbl`
  - `otafileTagP.gbl`
  - `otafileTagR.gbl`
  - `otafileTagX.gbl`
- The OTA format is Silicon Labs `.gbl`, which strongly suggests these tags are built on a Silicon Labs BLE platform.

## Main BLE classes

- `com.zucchettiaxess.bletagtools.Blecore.Ble_Scan`
  - handles scan start/stop
  - maps discovered devices to the supported product families
  - exposes family-specific connect entry points

- `com.zucchettiaxess.bletagtools.Blecore.Ble_Gatt`
  - generic GATT base layer
  - connect / disconnect / service discovery
  - characteristic read/write helpers
  - common helper methods like hex conversion and signed reads

- `com.zucchettiaxess.bletagtools.Blecore.Ble_Gatt_TAG_R`
  - TAG-R specific GATT wrapper

- `com.zucchettiaxess.bletagtools.Blecore.Ble_Gatt_ZTAG_SL`
  - ZTAG-SL specific GATT wrapper

- `com.zucchettiaxess.bletagtools.Blecore.Ble_Gatt_ProximityTAG`
  - proximity tag specific GATT wrapper

- `com.zucchettiaxess.bletagtools.Blecore.BLE_Gatt_XIO`
  - XIO-specific GATT wrapper

- `com.zucchettiaxess.bletagtools.Blecore.Ble_OTA_Update`
  - firmware update logic
  - packetized update flow
  - temp-file creation and OTA state tracking

## Concrete UUIDs recovered

### Generic ZTAG config

- `UUID_SERVICE_ZTAG_CONFIG` = `B9B5CA6F-5753-4870-9BFB-45376D217623`
- `UUID_CHARS_BVERS` = `FEDFBECE-C80B-473b-A718-48E284FAFBF9`
- `UUID_CHARS_FAST_ADV_MSEC` = `91345D99-7DE8-41a9-80EF-1172198382E5`
- `UUID_CHARS_SLOW_ADV_MSEC` = `0EF4B4A4-CA04-4d61-AB8D-1345D19A9C43`
- `UUID_CHARS_LED_CONTROL` = `4BAD317F-DB6C-4fdc-B1B4-106825E7836E`
- `UUID_CHARS_AUTO_DISC_COUNT` = `CF7759A7-8F26-4cc1-9395-19B8E4597CFB`
- `UUID_CHARS_MOTION_CONTROL` = `E69AF476-8F07-40a0-9E45-125CEC546B7D`
- `UUID_CHARS_CONNECT_CONTROL` = `78537281-3873-443a-B3CB-BAA8995C5521`
- `UUID_CHARS_TX_POWER` = `d990b4a1-ecd0-4300-a88c-cf828962d37f`
- `SERVICE_OTA` = `E4E37000-7A01-4507-8EFB-666B4EFC257F`
- `CHARACTERISTIC_CONTROL_NO_ACK` = `01737572-6573-686a-6f73-68692e636f6d`
- `CHARACTERISTIC_DATA_ACK` = `00737572-6573-686a-6f73-68692e636f6d`

### TAG_R

- `UUID_SERVICE_TAGR_CONFIG` = `e8df2b80-14d7-4e68-aaf4-66f6c31a2b95`
- `UUID_CHARS_FAST_ADV_MSEC` = `91345D99-7DE8-41a9-80EF-1172198382E5`
- `UUID_CHARS_SLOW_ADV_MSEC` = `0EF4B4A4-CA04-4d61-AB8D-1345D19A9C43`
- `UUID_CHARS_LED_CONTROL` = `4BAD317F-DB6C-4fdc-B1B4-106825E7836E`
- `UUID_CHARS_AUTO_DISC_COUNT` = `CF7759A7-8F26-4cc1-9395-19B8E4597CFB`
- `UUID_CHARS_MOTION_CONTROL` = `E69AF476-8F07-40a0-9E45-125CEC546B7D`
- `UUID_CHARS_CONNECT_CONTROL` = `78537281-3873-443a-B3CB-BAA8995C5521`
- `UUID_CHARS_TX_POWER` = `d990b4a1-ecd0-4300-a88c-cf828962d37f`
- `UUID_CHARS_BVERS` = `660c724a-ed3e-4748-9e6b-eeafe341ed80`
- `UUID_CHARS_FAST_BLINK_MSEC` = `3851a81e-13b5-4ecf-b98a-c278ffbb79af`
- `UUID_CHARS_SLOW_BLINK_MSEC` = `0adc95e2-5fcf-4ad0-ad84-a980aeb41827`
- `UUID_CHARS_DW_TX_POWER` = `57ca86da-955d-4264-b3df-49a4f14f9fc1`
- `UUID_CHARS_ALARM_THRESHOLD` = `6d76f866-8a14-45e6-8594-0d994629a33f`
- `UUID_CHARS_BUZZER_CONTROL` = `72EC0030-034E-4240-B4AB-3D6928C26B2F`
- `SERVICE_OTA` = `F7BF3564-FB6D-4E53-88A4-5E37E0326063`

### ZTAG_SL

- `UUID_SERVICE_ZTAG_CONFIG` = `B9B5CA6F-5753-4870-9BFB-45376D217623`
- `SERVICE_OTA` = `E4E37000-7A01-4507-8EFB-666B4EFC257F`

### Proximity

- The exact service UUID was not surfaced in the short excerpts I reviewed, but the class exposes:
  - alarm threshold
  - buzzer control
  - buzzer frequency
  - firmware version
  - RSSI filter
  - transmit power

### XIO

- `UUID_SERVICE_GATT_DEVICE_INFO` = `0000180A-0000-1000-8000-00805F9B34FB`
- `UUID_CHAR_GATT_FW_REV_STRING` = `00002A26-0000-1000-8000-00805F9B34FB`
- `UUID_SERVICE_XTAG_AUTH` = `591DABCC-7116-11E7-8CF7-A6006AD3DBA0`
- `UUID_SERVICE_XTAG_GENERICS_CMDS` = `4C39C376-711D-11E7-8CF7-A6006AD3DBA0`
- `UUID_SERVICE_XTAG_IP_PARAMS` = `50bcbc27-cbc5-4da3-8e12-703899d9220f`
- `UUID_CHAR_XTAG_AUTH_PSW` = `A4E48D8C-7116-11E7-8CF7-A6006AD3DBA0`
- `UUID_CHAR_XTAG_AUTH_RESULT` = `7221E968-711F-11E7-8CF7-A6006AD3DBA0`
- `UUID_CHAR_XTAG_IP_IP` = `9593d6a3-0482-456d-8c02-9791b4c5e645`
- `UUID_CHAR_XTAG_IP_SM` = `16156e4e-2e2c-473d-992b-f1fb8b7133c6`
- `UUID_CHAR_XTAG_IP_GW` = `b4ca3c71-16ae-481a-b37d-eb13e0b36589`
- `UUID_CHAR_XTAG_IP_MAC` = `411d22a0-b02e-4506-93dd-37db38bd5aa5`
- `UUID_CHAR_XTAG_IP_TID` = `70faad68-7156-11e7-8cf7-a6006ad3dba0`
- `UUID_CHAR_XTAG_IP_FW` = `3e3ab720-679d-416f-b302-396ba4b08782`
- `UUID_CHAR_XTAG_IP_DHCP` = `31f55af6-809e-4609-bbfa-a244faf5d3ad`
- `UUID_CHAR_XTAG_PARAM_SECTION` = `294bc082-3013-48a9-973c-b16db244af9b`
- `UUID_CHAR_XTAG_PARAM_KEY` = `2a705ddc-7126-11e7-8cf7-a6006ad3dba0`
- `UUID_CHAR_XTAG_PARAM_VALUE` = `5d81c800-7126-11e7-8cf7-a6006ad3dba0`
- `UUID_CHAR_XTAG_ACTION` = `2fc35d20-7121-11e7-8cf7-a6006ad3dba0`
- `UUID_CHAR_XTAG_PARAM_VALUE_DESCRIPTOR` = `00002902-0000-1000-8000-00805f9b34fb`

## Key methods seen in the dex

### `Ble_Scan`

- `ScanBLE_Scan(...)`
- `startScanLocal(...)`
- `stopScanner()`
- `connectToZTag()`
- `connectToZTagSL()`
- `connectToTagR()`
- `connectToZTagProximity()`
- `connectToXIO(...)`

### `Ble_Gatt`

- `connectToDevice(...)`
- `disconnectDevice()`
- `discoverServices()`
- `requestCharacteristics(...)`
- `writeAllChars(...)`
- `writeStringCharInAck(...)`
- `isTagConnected()`

### `Ble_OTA_Update`

- `startFirmwareUpdate()`
- `updateFirmware(File)`
- `sendNextPacket()`
- `createTempFile(BufferedSource)`

### `BLE_Gatt_XIO`

- `XIO_connectToDevice(...)`
- `XIO_disconnectDevice()`
- `XIO_WriteIPParams()`
- `setCharacteristicNotification2()`
- `delayedRead()`

## Protocol structure inferred from strings

The app contains named services/characteristics for:

- Services:
  - `UUID_SERVICE_GATT_DEVICE_INFO`
  - `UUID_SERVICE_ZTAG_CONFIG`
  - `UUID_SERVICE_TAGR_CONFIG`
  - `UUID_SERVICE_XTAG_AUTH`
  - `UUID_SERVICE_XTAG_GENERICS_CMDS`
  - `UUID_SERVICE_XTAG_IP_PARAMS`

- Characteristics:
  - `UUID_CHARS_CONNECT_CONTROL`
  - `UUID_CHARS_FW_VERSION`
  - `UUID_CHARS_TX_POWER`
  - `UUID_CHARS_LED_CONTROL`
  - `UUID_CHARS_BUZZER_CONTROL`
  - `UUID_CHARS_FAST_ADV_MSEC`
  - `UUID_CHARS_FAST_BLINK_MSEC`
  - `UUID_CHARS_SLOW_ADV_MSEC`
  - `UUID_CHARS_SLOW_BLINK_MSEC`
  - `UUID_CHARS_AUTO_DISC_COUNT`
  - `UUID_CHARS_ALARM_THRESHOLD`
  - `UUID_CHARS_RSSI_FILTER`
  - `UUID_CHARS_MOTION_CONTROL`
  - `UUID_CHAR_GATT_FW_REV_STRING`
  - `UUID_CHAR_XTAG_ACTION`
  - `UUID_CHAR_XTAG_AUTH_PSW`
  - `UUID_CHAR_XTAG_AUTH_RESULT`
  - `UUID_CHAR_XTAG_IP_DHCP`
  - `UUID_CHAR_XTAG_IP_FW`
  - `UUID_CHAR_XTAG_IP_GW`
  - `UUID_CHAR_XTAG_IP_IP`
  - `UUID_CHAR_XTAG_IP_MAC`
  - `UUID_CHAR_XTAG_IP_SM`
  - `UUID_CHAR_XTAG_IP_TID`
  - `UUID_CHAR_XTAG_PARAM_KEY`
  - `UUID_CHAR_XTAG_PARAM_SECTION`
  - `UUID_CHAR_XTAG_PARAM_VALUE`

## Reverse of the BLE flow

### Generic tags

- `Ble_Scan` selects a device family from the scan list, then dispatches to a family-specific connect method.
- `Ble_Gatt` and the family variants call `connectGatt(...)`, wait for `STATE_CONNECTED`, then call `discoverServices()`.
- `onServicesDiscovered` checks the target service UUID and either:
  - reads config characteristics, or
  - switches into OTA mode and starts packet upload.

### Read/write model

- The app reads all readable characteristics first, maps them into the corresponding `Class_*` object, then writes modified values back.
- `writeAllChars(...)` is used to push config values after readback.
- Writes are serialized one characteristic at a time and chained by the GATT callbacks.

### OTA model

- OTA is chunked into 16-byte packets.
- The app reads `R.raw.tag06`, copies it into a temp file, then streams it through `Ble_OTA_Update`.
- Each successful characteristic write triggers `sendNextPacket()`.
- End-of-file is signaled by sending a single control byte `{3}` to `CHARACTERISTIC_CONTROL_NO_ACK`.

### XIO model

- XIO uses a different workflow:
  - connect with a password
  - read firmware version
  - read IP, subnet, gateway, MAC, terminal ID, and DHCP
  - use a `GETPAR` action pattern against `UUID_CHAR_XTAG_PARAM_SECTION`, `UUID_CHAR_XTAG_PARAM_KEY`, and `UUID_CHAR_XTAG_PARAM_VALUE`
- The source explicitly handles `Wifi`, `Ethernet`, and `System` sections.

## What this suggests about BLE Tag 2

- The device is almost certainly managed through a proprietary GATT profile.
- The app seems to:
  - scan for nearby tags
  - classify them by family
  - connect with a family-specific GATT handler
  - discover services
  - read/write a set of config characteristics
  - optionally push firmware via OTA
- The presence of `connectControl`, `tx power`, `LED`, `buzzer`, `motion`, `RSSI filter`, `auto discovery`, and `alarm threshold` strongly suggests the tag exposes:
  - proximity/range tuning
  - beaconing/advertising control
  - alerting features
  - firmware revision reporting

## Practical parameter map

### ZTAG / ZTAG-SL

- `fastAdvMsec`
  - range seen in UI: `100..10000` ms, step `50`
  - default: `200`
- `slowAdvMsec`
  - range seen in UI: `1000..30000` ms, step `1000`
  - default: `2000`
- `autoDisconnectTimerCount`
  - UI shows minutes, values start at `1`
  - default: `3`
- `txPower`
  - UI uses 1-based values
  - default: `14`
- `ledControl`
  - small integer flag, default `0`
- `motionControl`
  - boolean-like flag, default `1`
- `connectControl`
  - boolean-like flag, default `1`

### TAG_R

- Shares the same base config service UUID as ZTAG/ZTAG-SL.
- Adds these fields:
  - `dw_txPower`
  - `dw_fast_blink`
  - `dw_slow_blink`
  - `alarmThreshold`
  - `buzzerControl`
- Default values seen in the UI:
  - `txPower = 7`
  - `dw_txPower = 9`
  - `dw_fast_blink = 500`
  - `dw_slow_blink = 10000`
  - `buzzerControl = 12`
- `alarmThreshold`
  - validated in UI to `30..800`
  - default used when invalid: `150`
- `buzzerControl`
  - treated as a bitmask
  - observed combinations:
    - `4`
    - `8`
    - `12`
  - the UI bit behavior implies separate enable flags for buzzer/vibration-style alerts

### Proximity

- The service UUID used by the client matches the TAG_R config service UUID, but the characteristic set is different.
- Fields exposed:
  - `alarmThreshold`
  - `trasmitPower`
  - `buzzerControl`
  - `buzzerFrequency`
  - `rssiFilter`
- UI mappings:
  - `alarmThreshold` uses `45..800` in steps of `5`
  - `trasmitPower` is a 1-based scale
  - `buzzerFrequency` is a stepped scale starting around `6 Hz`
  - `rssiFilter` is a direct integer
  - `buzzerControl` is a 4-bit mask
- Default values:
  - `alarmThreshold = 55`
  - `trasmitPower = 7`
  - `rssiFilter = 6`
  - `buzzerFrequency = 12`
  - `buzzerControl = 12`

## Scan / identification

- `Ble_Scan` keeps a 5-minute scan window.
- The decompiled scan callback is partially elided by JADX, but the surrounding code shows it builds `Class_Device` entries and later dispatches to the family-specific connect method.
- The scanner does not rely only on the MAC address:
  - it rebuilds the device object from scan results
  - it uses parsed advertisement data
  - it classifies the device into `BLE_TYPE`

## Emulation notes

- For a compatible client, the key behaviors to preserve are:
  - connect with GATT
  - discover services
  - read all readable config characteristics first
  - write them back one by one
  - if OTA is requested, switch to the OTA service and stream 16-byte chunks
- The OTA control flow is sensitive to write ordering:
  - the app sends the next packet only after the previous write callback succeeds
  - the end marker is a single byte `{3}`

## Payload structure

### Advertising payload

- The scan parser is a standard BLE AD-structure TLV parser.
- Supported AD types in the app:
  - flags (`0x01`)
  - short/complete local name (`0x08`, `0x09`)
  - 16/32/128-bit service UUID lists (`0x02`-`0x07`)
  - service data (`0x16`)
  - manufacturer specific data (`0xFF`)
  - TX power (`0x0A`)
- So the on-air advertising packet is not a custom flat blob; it is a normal BLE advertisement composed of standard length/type/value blocks.
- From `Ble_Scan.onScanResult(...)`, the app pulls:
  - device name from `ScanRecord`
  - manufacturer-specific data, first entry in the sparse array
  - RSSI from the scan result
- The manufacturer payload is interpreted like this:
  - `byte 0` = button press counter byte
  - `byte 1` = battery percentage byte
  - `byte 2` = fast polling indicator
  - for longer payloads on some families:
    - `bytes 3..4` = `upTimeFast` little-endian
    - `bytes 5..6` = `upTimeSlow` little-endian
    - `bytes 7..8` = connection counter little-endian
- Family-specific behavior:
  - `BLE Tag2` and related `ZTAG_SL` devices use the first 3 bytes for the common fields above, then may append timing/counter fields in longer manufacturer data
  - `BLE TagP` does not use the same long layout and is handled separately
  - `BLE TagR` uses the same first 3 bytes plus the extended timing/counter fields when present
- So the advertising packet is effectively:
  - standard BLE AD header fields
  - one manufacturer-specific record carrying status/state bytes
  - optional service UUIDs / service data / name strings

### GATT config payload

- Most writable characteristics are numeric scalars, sent through `BluetoothGattCharacteristic.setValue(...)`.
- The code clearly uses 1-byte and 2-byte GATT integer encodings.
- Fast/slow advertising periods are written as 16-bit values.
- Flags such as LED, motion, connect control, buzzer control, RSSI filter, and transmit power are generally treated as small integers.
- The proximity `alarmThreshold` looks like a wider numeric field because the UI allows values up to `800`; that is likely encoded as a 2-byte little-endian value even though the decompiler does not show the branch cleanly.
- OTA is separate from config and uses raw 16-byte chunks plus a final control byte `0x03`.

### Practical packet shape

- For a BLE Tag 2-style scan record, the app appears to expect at minimum:
  - `name` as the human-readable identifier
  - manufacturer data length `>= 3`
- When the manufacturer data length is `>= 8`, it reads:
  - `button press counter`
  - `battery percentage`
  - `fast polling`
  - `upTimeFast`
  - `upTimeSlow`
  - `connection counter`
- This is the most concrete payload structure recovered from the scan path.

### Manufacturer data table

| Offset | Size | Meaning | Notes |
| --- | --- | --- | --- |
| `0` | 1 byte | Button press counter | Read as an unsigned-ish button counter |
| `1` | 1 byte | Battery percentage | Commonly seen as `100` in the observed data |
| `2` | 1 byte | Fast polling | Copied into `fastPolling` |
| `3..4` | 2 bytes | `upTimeFast` | Little-endian |
| `5..6` | 2 bytes | `upTimeSlow` | Little-endian |
| `7..8` | 2 bytes | `connectionCounter` | Little-endian |

- The scanner code does **not** read offset `9`.
- The length guard in the decompiled code is slightly loose:
  - it checks `length < 8`
  - but later reads index `8`
  - so in practice the payload must be at least `9` bytes long for the extended fields to be safe
- For `BLE TagP`, the code does not use the same extended layout.
- If the full manufacturer payload is 10 bytes, that means:
  - bytes `0..8` are the decoded fields above
  - byte `9` exists on the air but is not used by the recovered scan code
  - that last byte is therefore likely reserved, a checksum, or a family-specific flag that this app version ignores

### Sample payloads

- Example 1:
  - `00 61 01 62 00 4b 03 00 00 00`
  - button press counter = `0`
  - battery = `0x61` = `97`
  - fast polling = `1`
  - `upTimeFast` = `0x0062` = `98`
  - `upTimeSlow` = `0x034b` = `843`
  - `connectionCounter` = `0`
  - byte `9` = `0`
- Example 2:
  - `01 64 01 00 00 00 00 00 00 01`
  - button press counter = `1`
  - battery = `0x64` = `100`
  - fast polling = `1`
  - `upTimeFast` = `0`
  - `upTimeSlow` = `0`
  - `connectionCounter` = `0`
  - byte `9` = `1`
- The examples fit the recovered layout well.
- Byte `9` looks more like a small state flag than a checksum, but the app version I decompiled does not decode it, so that remains an inference.
- Your sniffing observation refines that inference:
  - when the first-byte button counter increments, byte `9` often flips to `1`
  - but there are also cases with `buttonPressCounter > 0` and byte `9 = 0`
  - those cases happened while the tag was in slow mode
- The best current hypothesis is that byte `9` is a mode/state flag, not the press counter itself.
- A plausible interpretation is:
  - `0` = slow/inactive state
  - `1` = fast/active/event state
- That would fit the observation that button activity changes can force `1`, while slow mode can keep it at `0` even if the first-byte counter is already non-zero.
- This remains an inference from field behavior, not something explicitly decoded in the app sources.

### Working state matrix

| Observed mode | Button counter | Byte 9 | Working interpretation |
| --- | --- | --- | --- |
| Fast | 0 | 0 or 1 | Idle vs active fast-state may differ by moment of capture |
| Fast | > 0 | 1 | Press/event state appears asserted |
| Slow | 0 | 0 | Inactive / slow-state |
| Slow | > 0 | 0 | Counter can stay non-zero while the mode flag stays low |

- The table above is a working hypothesis, not a verified spec.
- The most likely meaning of byte `9` is therefore a **mode/event latch** rather than a pure history counter.
- This also matches the app-side behavior where `buttonPressed` is latched in the model when the first byte changes, but the scan code itself only stores the raw first-byte field.

### Evidence from the app

- The scan parser stores `byte 0` as the first status byte, `byte 1` as the second status byte, and `byte 2` as `fastPolling`.
- The model keeps a dedicated boolean latch:
  - `Class_Device.setButtonPression(int i)` sets `buttonPressed = true` when the first byte changes
  - `Class_Device.isButtonPressed()` returns `true` once and then clears the latch
- The list refresh logic uses that latch to highlight the item:
  - if `isButtonPressed()` is true, the UI colors the row
- That means the app distinguishes:
  - raw first-byte button counter
  - a transient event latch
  - fast/slow polling state
- Your observation that byte `9` can be `1` when the press counter changes, but remain `0` in slow mode, is consistent with byte `9` being a separate state flag rather than the counter itself.
- The app does not explicitly decode byte `9`, so this is still a field-behavior inference, but it is strongly supported by the separation of the first-byte button counter, `buttonPressed`, and `fastPolling` in the model.
- There is no app-side timer that clears byte `9`.
  - `MyListFragment` refreshes the UI on a 1-second countdown, but that only redraws the list
  - `Ble_Scan` updates model fields from advertisements, but never writes byte `9`
  - `Class_Device` only implements a UI latch for button changes, not an advertising reset timer
  - repository-wide searches for `18000`, `postDelayed`, `CountDownTimer`, and similar timeout logic did not surface any code path that clears or rewrites the advertiser payload
  - the only timer-like behavior tied to the scan UI is the 1-second `CountDownTimer` used to refresh the list view, not to alter radio state
  - the `Z_TAG_SL` profile does expose `slowAdvMsec`, `autoDisconnectTimerCount`, `dw_fast_blink`, and `dw_slow_blink`, but those are config fields for the tag, not a decoder for byte `9`
  - in the decompiled app, byte `9` is not mapped onto any named config characteristic or model field
- Live sniffing observed on a real `BLE Tag2`:
  - `00:38:18.877` -> `03 64 01 0a 00 5f 00 00 00 01`
  - `00:38:36.959` -> `03 64 01 0a 00 5f 00 00 00 00`
  - In that trace, byte `9` returned to `0` after roughly `18` seconds.
- A second filtered live trace confirmed the same behavior with a tighter window:
  - `00:43:19.183` -> `04 64 01 0a 00 5f 00 00 00 01`
  - `00:43:29.045` -> `04 64 01 0a 00 5f 00 00 00 00`
  - In that trace, byte `9` stayed high for about `9.862` seconds before clearing.
- A third filtered trace showed the same latch behavior while holding the middle fields steady:
  - `00:45:56.329` -> `05 64 01 0a 00 5f 00 00 00 01`
  - `00:46:04.127` -> `05 64 01 0a 00 5f 00 00 00 00`
  - In that trace, byte `9` cleared after about `7.799` seconds even though `b1=100`, `b2=1`, and `b3=10` stayed unchanged.
- In the button-correlation trace, the first observed active frame after the press was:
  - `00:47:21.340` -> `06 64 01 0a 00 5f 00 00 00 01`
  - Here `b0` incremented from `5` to `6` and `b9` flipped from `0` to `1` within `0.380` seconds of the previous frame.
- The same trace then showed `b9` returning to `0` after about `9.588` seconds while `b0=6`, `b1=100`, `b2=1`, and `b3=10` remained stable.
- So the reset is most likely firmware-side, not app-side, and the timing appears to be linked to the tag's own state machine/slow-mode transition.

### Final interpretation table

| Offset | Meaning | Confidence | Notes |
| --- | --- | --- | --- |
| `0` | Button press counter | High | Changes across traces and correlates with active/event transitions |
| `1` | Battery percentage | High | Commonly seen as `100` in the observed data |
| `2` | Fast polling flag | High | The app maps it to `fastPolling` |
| `3..4` | `upTimeFast` | High | Little-endian, only when extended payload is present |
| `5..6` | `upTimeSlow` | High | Little-endian, only when extended payload is present |
| `7..8` | `connectionCounter` | High | Little-endian, only when extended payload is present |
| `9` | Mode / event latch | Medium-high | Observed to flip `0 -> 1` on press-related transitions and return to `0` after about `8-10 s` in the traces captured here |

- Practical reading for `BLE Tag2`:
  - `byte 0` is the button press counter the app appears to expose in live traces
  - `byte 1` is the battery percentage the app appears to expose in live traces
  - `byte 2` is the fast/slow polling indicator the app exposes
  - `byte 9` is an additional firmware-side latch that the app ignores
- Current best hypothesis:
  - `byte 9 = 1` when the tag is in a transient active/event window
  - `byte 9 = 0` once the firmware settles back to its slow/inactive window
- Still open:
  - exact semantics of `byte 0`
  - whether the `8-10 s` decay window is fixed or depends on tag configuration / firmware build

## Notes

- This analysis is from the decompiled Java sources generated by `jadx`, plus a few earlier string-table passes.
- The reverse is already enough to map the BLE Tag 2 family into a proprietary GATT config protocol with OTA support.
- Remaining unknowns are mostly the exact per-characteristic payload formats and the advertisement parsing heuristics in the scanner.
