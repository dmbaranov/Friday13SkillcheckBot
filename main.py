import os
import keyboard
import threading
import time
import math
import win32api
import win32con
from PIL import ImageGrab


# List of resolutions and coordinates for mouse icons
RESOLUTIONS = [
    [(1280, 720), (620, 330, 640, 350), (640, 330, 660, 350)],
    [(1280, 768), (620, 355, 640, 375), (640, 355, 660, 375)],
    [(1280, 800), (620, 370, 640, 390), (640, 370, 660, 390)],
    [(1280, 960), (620, 450, 640, 470), (640, 450, 660, 470)],
    [(1280, 1024), (620, 485, 640, 505), (640, 485, 660, 505)],
    [(1360, 768), (660, 355, 680, 375), (680, 355, 700, 375)],
    [(1366, 768), (665, 355, 685, 375), (685, 355, 705, 375)],
    [(1400, 1050), (680, 495, 700, 515), (700, 495, 720, 515)],
    [(1440, 900), (700, 415, 720, 440), (720, 415, 740, 440)],
    [(1600, 900), (780, 415, 800, 440), (800, 415, 820, 440)],
    [(1600, 1200), (780, 565, 800, 590), (800, 565, 820, 590)],
    [(1680, 1050), (815, 485, 840, 515), (840, 485, 865, 515)],
    [(1792, 1344), (870, 630, 895, 660), (895, 630, 920, 660)],
    [(1856, 1392), (900, 655, 925, 680), (930, 655, 955, 680)],
    [(1920, 1080), (935, 495, 960, 530), (960, 495, 985, 530)],
    [(1920, 1200), (935, 555, 960, 585), (960, 555, 985, 585)],
    [(1920, 1440), (935, 675, 960, 705), (960, 675, 985, 705)],
    [(2048, 1152), (995, 530, 1025, 560), (1025, 530, 1054, 560)],
    [(2048, 1536), (995, 720, 1025, 750), (1025, 720, 1054, 750)],
    [(2560, 1600), (1245, 740, 1280, 780), (1280, 740, 1315, 780)],
    [(2560, 1920), (1245, 905, 1280, 940), (1280, 905, 1315, 940)],
    [(2560, 2048), (1240, 965, 1280, 1000), (1280, 965, 1315, 1000)],
    [(3840, 2160), (1865, 990, 1915, 1050), (1920, 990, 1975, 1050)]
]


class SkillCheckBot:
    def __init__(self):
        self._left_box = None
        self._right_box = None
        self._exit_time = 0
        self._screenshot_time = 0.05
        self._is_activated = False
        self._cond = threading.Lock()
        self._thread = threading.Thread(target=self.find_image)

    def start(self):
        self.auto_pick_res()
        self._cond.acquire()
        self._thread.start()
        keyboard.hook_key('e', self.activate_bot, self.deactivate_bot)
        keyboard.hook_key('q', self.on_exit_key_down, self.on_exit_key_release)

    def auto_pick_res(self):
        # Getting a resolution as a tuple and looking for it in a list of resolutions
        resolution = win32api.GetSystemMetrics(0), win32api.GetSystemMetrics(1)

        for res in RESOLUTIONS:
            if res[0] == resolution:
                self._left_box = res[1]
                self._right_box = res[2]
                print('Mode has been set to: {0}x{1}. Have a nice game!'.format(res[0][0], res[0][1]))
                ss_time = input('Enter screenshot time or press enter (default is 50ms): ')

                if ss_time:
                    try:
                        self._screenshot_time = float(int(ss_time) / 1000)
                    except ValueError:
                        print('Enter a number in ms!')
                        input('Press enter to exit...')
                        os._exit(1)

                break
        else:
            print('Your resolution is not supported. Make sure that Windows interface scaling is set to 100%')
            input('Press enter to exit...')
            os._exit(1)

    def activate_bot(self):
        if not self._is_activated:
            self._cond.release()
            self._is_activated = True

    def deactivate_bot(self):
        if self._is_activated:
            self._cond.acquire()
            self._is_activated = False

    def on_exit_key_down(self):
        if self._exit_time == 0:
            # Initial time for pressing and holding a button
            self._exit_time = time.time()
        else:
            now = time.time()
            difference = math.ceil(now - self._exit_time)

            # If button was pressed for at least 2 seconds
            if difference >= 2:
                os._exit(0)

    def on_exit_key_release(self):
        # Reset the ext_time if user doesn't want to close the bot.
        self._exit_time = 0

    def find_image(self):
        while True:
            with self._cond:
                # Taking a screenshot
                right_ss = ImageGrab.grab(self._right_box)
                left_ss = ImageGrab.grab(self._left_box)

                # Gets list of colors, sorts and takes the first one (Dominant color)
                right_ss = right_ss.convert('RGB').getcolors(maxcolors=9999)
                right_ss = sorted(right_ss, key=lambda x: -x[0])
                right_ss = right_ss[0]

                left_ss = left_ss.convert('RGB').getcolors(maxcolors=9999)
                left_ss = sorted(left_ss, key=lambda x: -x[0])
                left_ss = left_ss[0]

                # if R in RGB model is more than 200, then press button
                if right_ss[1][0] > 200:
                    print('Right click')
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif left_ss[1][0] > 200:
                    print('Left click')
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            time.sleep(self._screenshot_time)


bot = SkillCheckBot()
bot.start()
