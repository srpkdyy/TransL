import yaml
import deepl
import pyperclip
import japanize_kivy
from unicodedata import category
from kivy.app import App
from kivy.core.window import Window
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock




class Translator:
    def __init__(self):
        self.source_lang = cfg['deepl']['source_lang']
        self.target_lang = cfg['deepl']['target_lang']
        self.deepl = deepl.Translator(cfg['deepl']['auth_key'])
        self.text = ''
        self.cache = dict()

    def __call__(self, text):
        if text == '':
            return '翻訳したい文章をコピーしてください'
        elif text == self.text:
            return self.translated_text
        
        self.translated_text = self.cache.get(text)

        if self.translated_text is None:
            self.translated_text = self.deepl.translate_text(
                text=self.remove_control_characters(text),
                source_lang=self.source_lang,
                target_lang=self.target_lang
            ).text
            self.text = text
            self.cache[text] = self.translated_text
        
        return self.translated_text

    def remove_control_characters(self, raw_text):
        return ''.join([t for t in raw_text if category(t) != 'Cc'])



class TextViewer(ScrollView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        pyperclip.copy('')
        self.translator = Translator()
        Clock.schedule_interval(self.update, 0.5)

    def update(self, deltatime):
        self.ids.translated.text = self.translator(pyperclip.paste())


class TransL(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.title = 'TransL'

    def build(self):
        return TextViewer()


if __name__ == '__main__':
    with open('config.yaml') as f:
        cfg = yaml.safe_load(f)

    Window.size = (cfg['window']['width'], cfg['window']['height'])
    Window.clearcolor = (1, 1, 1, 1)
    TransL().run()
