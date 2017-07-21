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

                if right_ss[0][1][0] > 200:
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif left_ss[0][1][0] > 200:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            time.sleep(0.055)



                # ss = ss.convert('RGB').getcolors(maxcolors=9999)
                # ss = ss[:3]
                # ss = sorted(ss, key=lambda x: -x[0])
                # print(ss)
                # ss.show()
                # ss = np.array(ss)

                # left_button = cv2.imread('f13_button_left.png')
                # right_button = cv2.imread('f13_button_right.png')

                # ss = cv2.resize(ss, (0, 0), fx=0.5, fy=0.5)
                # left_button = cv2.resize(left_button, (0, 0), fx=0.5, fy=0.5)
                # right_button = cv2.resize(right_button, (0, 0), fx=0.5, fy=0.5)


                # ss_gray = cv2.cvtColor(ss, cv2.COLOR_BGR2GRAY)
                # left_button_gray = cv2.cvtColor(left_button, cv2.COLOR_BGR2GRAY)
                # right_button_gray = cv2.cvtColor(right_button, cv2.COLOR_BGR2GRAY)

                # l_w, l_h = left_button_gray.shape
                # r_w, r_h = right_button_gray.shape

                # res_left = cv2.matchTemplate(ss_gray, left_button_gray, cv2.TM_CCOEFF)
                # res_right = cv2.matchTemplate(ss_gray, right_button_gray, cv2.TM_CCOEFF)

                # l_min_val, l_max_val, l_min_loc, l_max_loc = cv2.minMaxLoc(res_left)
                # r_min_val, r_max_val, r_min_loc, r_max_loc = cv2.minMaxLoc(res_right)

                # l_top_left = l_max_loc
                # l_bottom_right = (l_top_left[0] + l_w, l_top_left[1] + l_h)

                # r_top_left = r_max_loc
                # r_bottom_right = (r_top_left[0] + r_w, l_top_left[1] + r_h)


                # print('Left button result: ', l_top_left, l_bottom_right)
                # print('Right button result: ', r_top_left, r_bottom_right)

                # res = cv2.matchTemplate(ss_gray, google_gray, cv2.TM_SQDIFF_NORMED)
                # min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                # h, w = google_gray.shape
                # top_left = min_loc
                # bottom_right = (top_left[0] + w, top_left[1] + h)
                # print(top_left, bottom_right)
                # cv2.rectangle(ss, top_left, bottom_right, (0, 0, 255), 4)

                # cv2.imshow('Screenshot', ss)
                # cv2.imshow('Google', google)
                # cv2.waitKey(0)
                # cv2.destroyAllWindows()

            time.sleep(0.055)


        #     ss = ss.convert('RGB')
        #     ss = np.array(ss)
        #     ss = ss.astype(np.uint8)
        #     ss = cv2.cvtColor(ss, cv2.COLOR_RGB2GRAY)
        #     google = cv2.imread('google.png', 0)
        #     res = cv2.matchTemplate(google, ss, cv2.TM_SQDIFF_NORMED)
        #     min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        #     print('MIN_VAL', min_val)
        #     print('MAX_VAL', max_val)
        #     print('MIN_LOC', min_loc)
        #     print('MAX_LOC', max_loc)
        # time.sleep(1)


bot = SkillCheckBot()
bot.start()