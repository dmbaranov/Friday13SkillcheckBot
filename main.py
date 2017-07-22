import os
import pyHook
import pythoncom
import threading
import time
import win32api
import win32con
from PIL import ImageGrab


# List of resolutions and coordinates for mouse icons
RESOLUTIONS = [
    ['1280x720', (620, 330, 640, 350), (640, 330, 660, 350)],
    # ['1280x768', (620, 350, 640, 370), (640, 350, 660, 370)],
    ['1280x768', (620, 355, 640, 375), (640, 355, 660, 375)],
    # ['1280x800', (620, 365, 640, 385), (640, 365, 660, 385)],
    ['1280x800', (620, 370, 640, 390), (640, 370, 660, 390)],
    # ['1280x960', (620, 445, 640, 465), (640, 445, 660, 465)],
    ['1280x960', (620, 450, 640, 470), (640, 450, 660, 470)],
    # ['1280x1024', (620, 480, 640, 500), (640, 480, 660, 500)],
    ['1280x1024', (620, 485, 640, 505), (640, 485, 660, 505)],
    # ['1360x768', (660, 350, 675, 370), (680, 350, 695, 370)],
    ['1360x768', (660, 355, 680, 375), (680, 355, 700, 375)],
    # ['1366x768', (665, 350, 680, 370), (685, 350, 700, 370)],
    ['1366x768', (665, 355, 685, 375), (685, 355, 705, 375)],
    # ['1400x1050', (680, 490, 700, 510), (700, 490, 720, 510)],
    ['1400x1050', (680, 495, 700, 515), (700, 495, 720, 515)],
    # ['1440x900', (700, 415, 715, 435), (720, 415, 740, 435)],
    ['1440x900', (700, 415, 720, 440), (720, 415, 740, 440)],
    # ['1600x900', (780, 415, 800, 435), (800, 415, 820, 435)],
    ['1600x900', (780, 415, 800, 440), (800, 415, 820, 440)],
    # ['1600x1200', (780, 560, 800, 580), (800, 560, 820, 580)],
    ['1600x1200', (780, 565, 800, 590), (800, 565, 820, 590)],
    # ['1680x1050', (815, 485, 840, 505), (840, 485, 865, 505)],
    ['1680x1050', (815, 485, 840, 515), (840, 485, 865, 515)],
    # ['1792x1344', (870, 625, 895, 650), (895, 625, 920, 650)],
    ['1792x1344', (870, 630, 895, 660), (895, 630, 920, 660)],
    # ['1856x1392', (900, 650, 925, 675), (925, 650, 950, 675)],
    ['1856x1392', (900, 655, 925, 680), (930, 655, 955, 680)],
    # ['1920x1080', (935, 495, 960, 520), (960, 495, 985, 520)],
    ['1920x1080', (935, 495, 960, 530), (960, 495, 985, 530)],
    # ['1920x1200', (935, 555, 960, 580), (960, 555, 985, 580)],
    ['1920x1200', (935, 555, 960, 585), (960, 555, 985, 585)],
    # ['1920x1440', (935, 675, 960, 700), (960, 675, 985, 700)],
    ['1920x1440', (935, 675, 960, 705), (960, 675, 985, 705)],
    # ['2048x1152', (995, 530, 1025, 555), (1025, 530, 1054, 555)],
    ['2048x1152', (995, 530, 1025, 560), (1025, 530, 1054, 560)],
    # ['2048x1536', (995, 720, 1025, 745), (1025, 720, 1054, 745)],
    ['2048x1536', (995, 720, 1025, 750), (1025, 720, 1054, 750)],
    # ['2560x1600', (1250, 755, 1280, 780), (1280, 755, 1310, 780)],
    ['2560x1600', (1245, 740, 1280, 780), (1280, 740, 1315, 780)],
    # ['2560x1920', (1250, 915, 1280, 940), (1280, 915, 1310, 940)],
    ['2560x1920', (1245, 905, 1280, 940), (1280, 905, 1315, 940)],
    # ['2560x2048', (1250, 975, 1280, 1000), (1280, 975, 1310, 1000)],
    ['2560x2048', (1240, 965, 1280, 1000), (1280, 965, 1315, 1000)],
    # ['3840x2160', (1890, 1030, 1920, 1060), (1920, 1030, 1950, 1060)]
    ['3840x2160', (1865, 990, 1915, 1050), (1920, 990, 1975, 1050)]
]


class SkillCheckBot:
    def __init__(self):
        self._left_box = None
        self._right_box = None
        self._is_activated = False
        self._hm = pyHook.HookManager()
        self._cond = threading.Lock()
        self._thread = threading.Thread(target=self.find_image)

    def start(self):
        self.pick_res()
        self._cond.acquire()
        self._thread.start()
        self._hm.KeyAll = self.read_pressed_key
        self._hm.HookKeyboard()
        pythoncom.PumpMessages()

    def pick_res(self):
        print('Choose a resolution of your screen: ')
        for i, res in enumerate(RESOLUTIONS):
            print('{0}. {1}'.format(i + 1, res[0]))

        try:
            chosen_index = int(input('\n\nEnter a number: '))
        except ValueError:
            print('That\'s not a number!')
            os._exit(1)


        try:
            self._left_box = RESOLUTIONS[chosen_index - 1][1]
            self._right_box = RESOLUTIONS[chosen_index - 1][2]
        except IndexError:
            print('Wrong number...')
            os._exit(1)

    def read_pressed_key(self, event):
        """
        Process all pressed buttons
        :param event: pressed key event
        :return: True
        """
        if event.Key == 'e' or event.Key == 'E':
            #  Button down
            if event.Message == 256 and not self._is_activated:
                self.activate_bot()
            #  Button up
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
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0, 0, 0)
                elif left_ss[1][0] > 200:
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)

            time.sleep(0.045)


bot = SkillCheckBot()
bot.start()
