from pynput import mouse
import time
import threading

__DEBUG = False

def log(msg,debug=False):
    if __DEBUG or debug:
        print(msg)

class MouseMonitor():
    __press_time = 0
    __press_double_state = False
    __move = (0,0)

    def __init__(self,on_selected=None):
        if on_selected:
            self.on_selected = on_selected
        else:
            self.on_selected = self._on_selected

        self.listener = mouse.Listener(on_move=self.on_move,on_click=self.on_click)
        self.listener.start()
        self.listener.join()

    def _on_selected(self,msg):
        print('selected "%s" has been copied.' % (msg,))

    def on_move(self,x,y):
        if self.__press_time == 0:
            self.__move = (x,y)
        # log(self.__press_time,time.time())
        # log('Pointer moved to {0}'.format((x,y)))

    def on_click(self,x,y,button,pressed):
        if str(button) == 'Button.left':
            if pressed:
                self.on_pressed(x,y)
            else:
                self.on_released(x,y)

    def on_pressed(self,x,y):
        if self.__press_double_state:
            # double click
            # self.__press_double_state = False
            if not self.check_not_time_out(self.__press_time, time.time(),0.4): # miss double click
                log('double1 click timeout and reset then')
                self.reset()
                self.__press_time = time.time()
        else:
            # single click
            self.__press_time = time.time()
            # self.__press_double_state = False

    def on_released(self,x,y):
        if self.__press_double_state:
            # double click
            if self.check_not_time_out(self.__press_time, time.time(),0.8):
                log('double click: %s' % (self.get_copy()))
                self.on_selected(self.get_copy())
                self.__press_double_state = False
            else:
                log('double2 click timeout and reset then')
                self.reset()
        else:
            if self.check_not_time_out(self.__press_time, time.time()):
                log('double click maybe')
                self.__press_double_state = True
                threading.Timer(0.5, self.timeout_handler).start() # wait timeout to reset
            elif not self.check_not_time_out(self.__press_time, time.time(),1):
                if self.__move != (0,0):
                    self.on_selected(self.get_copy())
                    log('selected: %s' % (self.get_copy(),))
                    self.reset()
            else:
                log('reset state')
                self.reset()

    def get_copy(self):
        import win32clipboard as wc
        import win32con

        def trigger_copy():
            from pynput.keyboard import Key,Controller
            key = Controller()
            with key.pressed(Key.ctrl):
                key.press('c')
                key.release('c')
            time.sleep(0.1) # wait for ctrl+c valid

        trigger_copy()
        msg = ''
        try:
            wc.OpenClipboard()
            msg = wc.GetClipboardData(win32con.CF_UNICODETEXT)
            wc.CloseClipboard()
        except TypeError:
            log('Clipboard Content is TypeError.')
        return msg

    def reset(self):
        self.__press_time = 0
        self.__press_double_state = False
        self.__move = (0,0)

    def timeout_handler(self):
        self.reset()
        log('timeout reset state')

    def check_not_time_out(self,old,new,delta=0.2):
        if(new - old > delta): # time delta > 0.2s
            return False
        else:
            return True


def printf(msg):
    log('copy content:'+msg,True)
    # log('x = {0} , y = {1}'.format(x,y))


if __name__ == '__main__':
    mm = MouseMonitor(printf)