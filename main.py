import os
import pyHook
import pythoncom
import threading
import time
import win32api
import win32con
from PIL import ImageGrab


class SkillCheckBot:
    def __init__(self):
        self._is_activated = False
        self._hm = pyHook.HookManager()
        self._cond = threading.Lock()
        self._thread = threading.Thread(target=self.find_image, args=(self._cond, ))

    def start(self):
        self._cond.acquire()
        self._thread.start()
        self._hm.KeyAll = self.read_pressed_key
        self._hm.HookKeyboard()
        pythoncom.PumpMessages()

    def read_pressed_key(self, event):
        if event.Key == 'e' or event.Key == 'E':
            if event.Message == 256 and not self._is_activated:
                self.activate_bot()
            elif event.Message == 257 and self._is_activated:
                self.deactivate_bot()
        elif event.Key == 'q' or event.Key == 'Q':
            os._exit(0)

        return True

    def activate_bot(self):
        print('activating')
        self._cond.release()
        self._is_activated = True
        return True

    def deactivate_bot(self):
        print('deactivating')
        self._cond.acquire()
        self._is_activated = False
        return True

    def find_image(self, evt):
        while True:
            with self._cond:
                # HD coords
                right_box = (640, 330, 655, 350)
                left_box = (625, 330, 640, 350)

                # FHD coords
                # right_box  = (960, 495, 985, 520)
                # left_box = (935, 495, 960, 520)

                right_ss = ImageGrab.grab(right_box)
                left_ss = ImageGrab.grab(left_box)

                right_ss = right_ss.convert('RGB').getcolors(maxcolors=9999)
                right_ss = sorted(right_ss, key=lambda x: -x[0])
                right_ss = right_ss[:3]

                left_ss = left_ss.convert('RGB').getcolors(maxcolors=9999)
                left_ss = sorted(left_ss, key=lambda x: -x[0])
                left_ss = left_ss[:3]

				#if R in RGB model is more than 200, then press button
                if right_ss[0][1][0] > 200:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif left_ss[0][1][0] > 200:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            time.sleep(0.055)
			

bot = SkillCheckBot()
bot.start()