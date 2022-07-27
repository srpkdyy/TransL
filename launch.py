import os
os.environ['KIVY_NO_CONSOLELOG'] = '1'

import time
import yaml
import win32gui
import win32con
import subprocess
import japanize_kivy
from kivy.app import App
from kivy.config import Config



class AuthKeyRegister(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = '認証キー登録'
        self.cfg = {
            'window': {
                'width': 320,
                'height': 240
            },
            'deepl': {
                'source_lang': 'EN',
                'target_lang': 'JA'
            }
        }

    def save_config(self):
        self.cfg['deepl']['auth_key'] = self.root.ids.auth_key.text

        with open('config.yaml', 'w') as f:
            yaml.dump(self.cfg, f)
        
        self.exit()
    
    def exit(self):
        self.root_window.close()
        self.stop()


def launch_transl():
    return subprocess.Popen(
        ['python', './transl.py'],
        creationflags=subprocess.CREATE_NEW_PROCESS_GROUP
    )


def set_foreground(proc):

    while proc.poll() is None:
        hwnd = win32gui.FindWindow('SDL_app', 'TransL')
        if hwnd != 0:
            break

    win32gui.SetWindowPos(
        hwnd,
        win32con.HWND_TOPMOST,
        0, 0, 0, 0,
        win32con.SWP_NOMOVE | win32con.SWP_NOSIZE
    )



if __name__ == '__main__':

    if not os.path.exists('config.yaml'):
        Config.set('graphics', 'width', '300')
        Config.set('graphics', 'height', '100')
        AuthKeyRegister().run()

    else:
        Config.set('graphics', 'multisamples', 0)

    if not os.path.exists('config.yaml'):
        os._exit()

    proc = launch_transl()
    set_foreground(proc)
