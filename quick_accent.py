import time

import pynput
from pynput import keyboard


controller = keyboard.Controller()


class HotKeyTime:
    def __init__(self, activation_time: float):
        self.hotkeys = {}
        self.activation_time = activation_time
        self.start_time = None
        self.active_hotkey = None
        self.keys = []

    def new_hotkey(self, hotkey: list, key: str):
        if key in self.hotkeys:
            return
        self.hotkeys[str(hotkey)] = key

    def on_press(self, key):
        if key == keyboard.Key.backspace:
            return
        if not key in self.keys:
            self.keys.append(key)
        if str(self.keys) in self.hotkeys:
            if not self.start_time is None:
                return
            self.start_time = time.perf_counter()
            self.active_hotkey = str(self.keys)
        else:
            self.start_time = None
            self.active_hotkey = None


    def on_release(self, key):
        if key in self.keys:
            self.keys.remove(key)
        if str(key).lower() in self.keys:
            self.keys.remove(str(key).lower())
        if self.start_time is None:
            return
        end_time = time.perf_counter()
        if str(key) in self.active_hotkey:
            if end_time - self.start_time > (self.activation_time / 1000):
                char = self.hotkeys[self.active_hotkey]
                controller.press(keyboard.Key.backspace)
                controller.release(keyboard.Key.backspace)
                controller.press(keyboard.Key.backspace)
                controller.release(keyboard.Key.backspace)
                controller.type(char)
        self.start_time = None
        self.active_hotkey = None


hotkey_containter = HotKeyTime(100)
_hotkey = [keyboard.KeyCode.from_char("a"), keyboard.Key.space]
hotkey_containter.new_hotkey(_hotkey, u"á")
_hotkey = [keyboard.KeyCode.from_char("e"), keyboard.Key.space]
hotkey_containter.new_hotkey(_hotkey, u"é")
_hotkey = [keyboard.KeyCode.from_char("i"), keyboard.Key.space]
hotkey_containter.new_hotkey(_hotkey, u"í")
_hotkey = [keyboard.KeyCode.from_char("o"), keyboard.Key.space]
hotkey_containter.new_hotkey(_hotkey, u"ó")
_hotkey = [keyboard.KeyCode.from_char("u"), keyboard.Key.space]
hotkey_containter.new_hotkey(_hotkey, u"ú")
with keyboard.Listener(on_press=hotkey_containter.on_press, on_release=hotkey_containter.on_release ) as listener:
    listener.join()
