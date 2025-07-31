import win32api

from config import CONFIG

def to_hex(buffer):
    return " ".join("{:02x}".format(x) for x in buffer)

def decodeu(data: bytes):
    return int.from_bytes(data, byteorder='little', signed=False)

def decodes(data: bytes):
    return int.from_bytes(data, byteorder='little', signed=True)

def convert_mac_string_to_value(mac: str):
    return int.from_bytes(bytes([int(b, 16) for b in mac.split(":")]), 'big')

def get_stick_xy(data: bytes):
    """Convert 3 bytes containing stick x y values into these values"""
    value = decodeu(data)
    x = value & 0xFFF
    y = value >> 12

    return x, y

def signed_looping_difference_16bit(a, b):
    diff = (b - a) % 65536
    return diff - 65536 if diff > 32768 else diff

def apply_calibration_to_axis(raw_value, center, max_abs, min_abs):
    signed_value = raw_value - center
    if signed_value > CONFIG.deadzone:
        return min(signed_value / max_abs, 1)
    if signed_value < -CONFIG.deadzone:
        return -min(-signed_value / min_abs, 1)
    return 0

def press_or_release_mouse_button(state: bool, prev_state: bool, button: int, mouse_x: int, mouse_y):
    if (state and not prev_state):
        win32api.mouse_event(button, mouse_x, mouse_y, 0, 0)
    if (not state and prev_state):
        win32api.mouse_event(button << 1, mouse_x, mouse_y, 0, 0)