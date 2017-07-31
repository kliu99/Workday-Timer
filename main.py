import pyautogui
import time

############################################
# Go to Workday -> Time -> View -> Day
# Go to the day you want to check-in
# DEFAULT STARTING AND ENDING TIME
AM_IN_DEFAULT = "0830"
AM_OUT_DEFAULT = "1200"
PM_IN_DEFAULT = "1300"
PM_OUT_DEFAULT = "1730"
N_RUN_DEFAULT = "5"
############################################


# Turn on Fail Safe:
# moving the mouse to the upper-left will raise a pyautogui.FailSafeException that can abort the program
pyautogui.FAILSAFE = True
screenWidth, screenHeight = pyautogui.size()


class Clicker:

    def __init__(self, AM_IN, AM_OUT, PM_IN, PM_OUT):
        self.AM_IN = AM_IN
        self.AM_OUT = AM_OUT
        self.PM_IN = PM_IN
        self.PM_OUT = PM_OUT
        self.stars = None
        self.okay = None

    def fillPopUp(self, x, y, type, IN, OUT, pause=0):
        time.sleep(pause)

        pyautogui.click(x, y, pause=2)

        if self.stars is None:
            self.stars = list(pyautogui.locateAllOnScreen("src/star.png"))

        # Time Type
        left, top, width, height = self.stars[0]
        x = left + width + 50
        y = top + height // 2
        pyautogui.click(x, y, pause=0.5, clicks=2, interval=0.5)
        pyautogui.typewrite(type, interval=0.1)

        # In
        left, top, width, height = self.stars[1]
        x = left + width + 50
        y = top + height // 2
        pyautogui.click(x, y, pause=0.5, clicks=2, interval=0.5)
        pyautogui.typewrite(IN, interval=0.1)

        # Out
        left, top, width, height = self.stars[2]
        x = left + width + 50
        y = top + height // 2
        pyautogui.click(x, y, pause=0.5, clicks=2, interval=0.5)
        pyautogui.typewrite(OUT, interval=0.1)

        # Move to somewhere else
        left, top, width, height = self.stars[-1]
        x = left + width + 50
        y = top + height // 2
        pyautogui.click(x, y, pause=0.5)

        # Click Okay
        if self.okay is None:
            self.okay = pyautogui.locateCenterOnScreen('src/okBtn.png')

        pyautogui.click(self.okay[0], self.okay[1])

    def fillADay(self, nextX, nextY, pause=0):
        # Find the 7AM to 8AM mark
        left, top, width, height = pyautogui.locateOnScreen('src/7AM_8AM.png')
        x = left + width + 10
        y = top + height // 2

        # AM
        self.fillPopUp(x, y, "work", self.AM_IN, self.AM_OUT)

        ## Meal
        self.fillPopUp(x, y, "meal", self.AM_OUT, self.PM_IN, pause=5)

        ## PM
        self.fillPopUp(x, y, "work", self.PM_IN, self.PM_OUT, pause=5)

        # Go to next day
        time.sleep(5)
        pyautogui.click(x=nextX, y=nextY, interval=0.25, pause=pause)

    def click(self):
        # Locate the arrow
        nextX, nextY = pyautogui.locateCenterOnScreen('src/nextArrow.png')

        # Bring the browser to front
        pyautogui.click(nextX, nextY-50)

        for i in range(0, self.N_RUN):
            pause = 5 if i > 0 else 0
            self.fillADay(nextX, nextY, pause=pause)

    def setRuns(self, N_RUN):
        self.N_RUN = int(N_RUN)
        if self.N_RUN is None:
            self.N_RUN = N_RUN_DEFAULT


if __name__ == "__main__":

    pyautogui.alert(text='Please change to Day view and change to the day you want to check-in before proceed',
                    title='', button='OK')

    response = pyautogui.confirm("Using default time?\nAM_IN=%s\nAM_OUT=%s\nPM_IN=%s\nPM_OUT=%s\nN_RUN=%s" %
                                 (AM_IN_DEFAULT, AM_OUT_DEFAULT, PM_IN_DEFAULT, PM_OUT_DEFAULT, N_RUN_DEFAULT),
                      "", buttons=["Yes", "No"])

    if response == "No":
        AM_IN = pyautogui.prompt('Please enter AM_IN. Format: 0830, 08:30, 08:30 AM', '', '08:30 AM')
        if AM_IN is None:
            AM_IN = AM_IN_DEFAULT

        AM_OUT = pyautogui.prompt('Please enter AM_OUT. Format: 1200, 12:00, 12:00 PM', '', '12:00 PM')
        if AM_OUT is None:
            AM_OUT = AM_OUT_DEFAULT

        PM_IN = pyautogui.prompt('Please enter PM_IN. Format: 1300, 13:00, 01:00 PM', '', '01:00 PM')
        if PM_IN is None:
            PM_IN = PM_IN_DEFAULT

        PM_OUT = pyautogui.prompt('Please enter PM_OUT. Format: 1730, 17:30, 05:30 PM', '', '05:30 PM')
        if PM_OUT is None:
            PM_OUT = PM_OUT_DEFAULT

        N_RUN = pyautogui.prompt('Please enter number of time to run', '', "5")
        if N_RUN is None:
            N_RUN = N_RUN_DEFAULT

        clicker = Clicker(AM_IN, AM_OUT, PM_IN, PM_OUT)
        clicker.setRuns(N_RUN)
    else:
        clicker = Clicker(AM_IN_DEFAULT, AM_OUT_DEFAULT, PM_IN_DEFAULT, PM_OUT_DEFAULT)
        clicker.setRuns(N_RUN_DEFAULT)

    clicker.click()