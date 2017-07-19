import pyHook
import pythoncom
import threading
import time
import cv2
import numpy
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
        # self._hm.SubscribeMouseLeftDown(self.activate_bot)
        # self._hm.SubscribeMouseLeftUp(self.deactivate_bot)
        # self._hm.HookMouse()
        self._hm.HookKeyboard()
        pythoncom.PumpMessages()

    def read_pressed_key(self, event):
        if event.Key == 'e' or event.Key == 'E':
            if event.Message == 256 and not self._is_activated:
                self.activate_bot()
            elif event.Message == 257 and self._is_activated:
                self.deactivate_bot()

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
                box = (0, 0, 300, 300)
                ss = ImageGrab.grab(box)
                ss = ss.convert('RGB')
                ss = numpy.array(ss)
                ss = ss.astype(numpy.uint8)
                ss = cv2.cvtColor(ss, cv2.COLOR_RGB2GRAY)
                google = cv2.imread('google.png', 0)
                res = cv2.matchTemplate(google, ss, cv2.TM_SQDIFF_NORMED)
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                print('MIN_VAL', min_val)
                print('MAX_VAL', max_val)
                print('MIN_LOC', min_loc)
                print('MAX_LOC', max_loc)
            time.sleep(1)


bot = SkillCheckBot()
bot.start()