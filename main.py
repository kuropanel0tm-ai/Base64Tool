from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.lang import Builder
from kivy.core.clipboard import Clipboard
import base64
import json
import os

KV = """
<LoginScreen>:
    BoxLayout:
        orientation: 'vertical'
        spacing: 20
        padding: [40, 80, 40, 40]
        canvas.before:
            Color:
                rgba: 0.12, 0.12, 0.14, 1
            Rectangle:
                pos: self.pos
                size: self.size

        Label:
            text: 'B'
            font_size: 48
            bold: True
            color: 0.3, 0.6, 0.95, 1
            size_hint_y: 0.15
            halign: 'center'

        Label:
            text: 'Base64 Tool'
            font_size: 32
            bold: True
            color: 0.95, 0.95, 0.97, 1
            size_hint_y: 0.08
            halign: 'center'

        Label:
            text: 'Lutfen giris yapin'
            font_size: 14
            color: 0.6, 0.6, 0.65, 1
            size_hint_y: 0.04
            halign: 'center'

        Widget:
            size_hint_y: 0.05

        TextInput:
            id: username
            hint_text: 'Kullanici Adi'
            multiline: False
            size_hint_y: 0.08
            background_color: 0.2, 0.2, 0.22, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.5, 0.5, 0.55, 1
            cursor_color: 1, 1, 1, 1
            padding: [15, 15]
            font_size: 16

        TextInput:
            id: password
            hint_text: 'Sifre'
            password: True
            multiline: False
            size_hint_y: 0.08
            background_color: 0.2, 0.2, 0.22, 1
            foreground_color: 1, 1, 1, 1
            hint_text_color: 0.5, 0.5, 0.55, 1
            cursor_color: 1, 1, 1, 1
            padding: [15, 15]
            font_size: 16

        Widget:
            size_hint_y: 0.03

        Button:
            text: 'GIRIS YAP'
            size_hint_y: 0.09
            background_color: 0.3, 0.6, 0.95, 1
            background_normal: ''
            color: 1, 1, 1, 1
            font_size: 18
            bold: True
            on_press: app.login(root)

        Label:
            id: error_label
            text: ''
            font_size: 14
            color: 1, 0.3, 0.3, 1
            size_hint_y: 0.05


<MainScreen>:
    BoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.12, 0.12, 0.14, 1
            Rectangle:
                pos: self.pos
                size: self.size

        BoxLayout:
            size_hint_y: 0.08
            padding: [15, 5]
            spacing: 10
            canvas.before:
                Color:
                    rgba: 0.18, 0.18, 0.2, 1
                Rectangle:
                    pos: self.pos
                    size: self.size

            Label:
                text: 'Base64 Tool'
                font_size: 20
                bold: True
                color: 0.95, 0.95, 0.97, 1

            Widget:

            Button:
                text: 'Cikis'
                size_hint_x: 0.2
                background_color: 0.8, 0.2, 0.2, 1
                background_normal: ''
                color: 1, 1, 1, 1
                on_press: app.logout()

        BoxLayout:
            orientation: 'vertical'
            spacing: 15
            padding: [20, 20, 20, 20]

            BoxLayout:
                size_hint_y: 0.08
                spacing: 10

                Button:
                    id: btn_encode
                    text: 'Sifrele'
                    background_normal: ''
                    color: 1, 1, 1, 1
                    on_press: root.set_mode('encode')

                Button:
                    id: btn_decode
                    text: 'Coz'
                    background_normal: ''
                    color: 1, 1, 1, 1
                    on_press: root.set_mode('decode')

            Label:
                id: mode_label
                text: 'Telefon numarasini girin:'
                font_size: 15
                color: 0.7, 0.7, 0.75, 1
                size_hint_y: 0.05

            TextInput:
                id: input_field
                multiline: True
                size_hint_y: 0.2
                background_color: 0.2, 0.2, 0.22, 1
                foreground_color: 1, 1, 1, 1
                hint_text_color: 0.5, 0.5, 0.55, 1
                cursor_color: 1, 1, 1, 1
                padding: [15, 15]
                font_size: 16

            Button:
                id: action_btn
                size_hint_y: 0.08
                background_color: 0.3, 0.6, 0.95, 1
                background_normal: ''
                color: 1, 1, 1, 1
                font_size: 16
                bold: True
                on_press: root.process()

            Label:
                text: 'Sonuc:'
                font_size: 14
                color: 0.6, 0.6, 0.65, 1
                size_hint_y: 0.04

            TextInput:
                id: output_field
                readonly: True
                multiline: True
                size_hint_y: 0.2
                background_color: 0.15, 0.15, 0.17, 1
                foreground_color: 0.3, 0.9, 0.5, 1
                padding: [15, 15]
                font_size: 16

            Widget:

            Button:
                text: 'SONUCU KOPYALA'
                size_hint_y: 0.08
                background_color: 0.2, 0.25, 0.3, 1
                background_normal: ''
                color: 0.8, 0.8, 0.85, 1
                font_size: 14
                on_press: root.copy_result()

            Label:
                id: copy_label
                text: ''
                font_size: 13
                color: 0.3, 0.9, 0.5, 1
                size_hint_y: 0.04
"""


class LoginScreen(Screen):
    pass


class MainScreen(Screen):
    mode = 'encode'

    def set_mode(self, mode):
        self.mode = mode
        if mode == 'encode':
            self.ids.mode_label.text = 'Telefon numarasini girin:'
            self.ids.input_field.hint_text = 'Ornek: 905551234567'
            self.ids.action_btn.text = 'SIFRELE'
            self.ids.btn_encode.background_color = (0.3, 0.6, 0.95, 1)
            self.ids.btn_decode.background_color = (0.2, 0.2, 0.22, 1)
        else:
            self.ids.mode_label.text = 'Base64 kodunu girin:'
            self.ids.input_field.hint_text = 'Base64 veriyi girin'
            self.ids.action_btn.text = 'COZ'
            self.ids.btn_decode.background_color = (0.3, 0.6, 0.95, 1)
            self.ids.btn_encode.background_color = (0.2, 0.2, 0.22, 1)

    def process(self):
        input_text = self.ids.input_field.text.strip()
        output = self.ids.output_field
        self.ids.copy_label.text = ''

        if not input_text:
            output.text = '[HATA] Lutfen veri girin!'
            return

        try:
            if self.mode == 'encode':
                output.text = base64.b64encode(input_text.encode()).decode()
            else:
                output.text = base64.b64decode(input_text.encode()).decode()
        except Exception as e:
            output.text = f'[HATA] {str(e)}'

    def copy_result(self):
        text = self.ids.output_field.text
        if text and not text.startswith('[HATA]'):
            Clipboard.copy(text)
            self.ids.copy_label.text = 'Kopyalandi!'
        else:
            self.ids.copy_label.text = 'Kopyalanacak veri yok'


class Base64App(App):
    def build(self):
        self.users = self.load_users()
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name='login'))
        sm.add_widget(MainScreen(name='main'))
        return sm

    def load_users(self):
        try:
            path = self.get_users_path()
            if os.path.exists(path):
                with open(path) as f:
                    data = json.load(f)
                    if isinstance(data, dict) and len(data) > 0:
                        return data
        except:
            pass
        return {'admin': '1234'}

    def get_users_path(self):
        return os.path.join(os.path.dirname(os.path.abspath(__file__)), 'users.json')

    def login(self, screen):
        username = screen.ids.username.text.strip()
        password = screen.ids.password.text.strip()
        error_label = screen.ids.error_label

        if not username or not password:
            error_label.text = 'Kullanici adi ve sifre girin!'
            return

        if username in self.users and self.users[username] == password:
            error_label.text = ''
            screen.ids.username.text = ''
            screen.ids.password.text = ''
            self.root.current = 'main'
        else:
            error_label.text = 'Hatali kullanici adi veya sifre!'

    def logout(self):
        self.root.current = 'login'


if __name__ == '__main__':
    Base64App().run()
