import os
import win32gui
import win32con
import subprocess


def set_auth_key():
    pass

def launch_transl():
    subprocess.popen('TransL.exe')


def set_foreground():
    hwnd = win32gui.FindWindow(None, 'TransL')
    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )


if __name__ == '__main__':
    if not os.path.exists('config.yaml'):
        set_auth_key()
    #launch_transl()
    set_foreground()
