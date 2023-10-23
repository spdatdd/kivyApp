from kivymd.app import MDApp
from kivy.lang import Builder
from kivy.metrics import dp
# register our custom font for application
from kivy.core.text import LabelBase
from kivymd.uix.menu import MDDropdownMenu
import requests
import json


KV = """

MDRelativeLayout:
    md_bg_color: app.theme_cls.primary_color
    MDBoxLayout:
        adaptive_height: True
        pos_hint: {"center_x": .5, "center_y": .5}
        orientation: 'vertical'
        padding: '10dp'
        spacing: '15dp'

        MDLabel:
            text: 'Nội dung bài báo'
            font_name: 'Playpen_Sans'

        MDTextFieldRect:
            id: NoiDung
            size_hint: 1, None
            height: '200dp'
            multiline: True
            hint_text: 'Nội dung'
            line_anim: False

        MDLabel:
            text: 'Loại mô hình dùng cho phân loại'
            font_name: 'Playpen_Sans'

        MDRectangleFlatIconButton:
            id: LoaiMoHinh
            icon: 'chevron-down'
            text: "Naive Bayes"
            theme_text_color: "Custom"
            text_color: "black"
            theme_icon: "Custom"
            icon: "black"
            elevation: 4
            font_name: 'Playpen_Sans'
            line_color: 1,1,1,1
            md_bg_color: 1,1,1,1
            on_release: app.loai_mo_hinh(root)
        
        
        MDGridLayout: 
            cols:2
            adaptive_height: True
            spacing: '15dp'
            
            MDFlatButton:
                text: "Phân loại"
                theme_text_color: "Custom"
                text_color: "black"
                elevation: 4
                font_name: 'Playpen_Sans'
                line_color: '#e6ffff'
                md_bg_color: '#e6ffff'
                on_press: app.phan_loai(root.ids.NoiDung.text, root.ids.LoaiMoHinh.text, root.ids.KetQua)

            MDFlatButton:
                text: "Xóa nội dung"
                theme_text_color: "Custom"
                text_color: "black"
                elevation: 4
                font_name: 'Playpen_Sans'
                line_color: '#e6ffff'
                md_bg_color: '#e6ffff'
                on_press: 
                    root.ids.NoiDung.text = ''
                    root.ids.KetQua.text = ''

        MDLabel:
            id: KetQua
            font_name: 'Playpen_Sans'
            theme_text_color: "Custom"
            text_color: "orange"
            adaptive_height: True       
"""

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.theme_cls.primary_palette = 'DeepPurple'
        # registering our new custom fontstyle
        LabelBase.register(name='Playpen_Sans', fn_regular='assets/fonts/Playpen_Sans/PlaypenSans-Regular.ttf')
        screen = Builder.load_string(KV)
        return screen
 
    def loai_mo_hinh(self, root):
        def dat_mo_hinh(text__item, root):
            root.ids.LoaiMoHinh.text = text__item
            self.menu.dismiss()
        menu_items = [
            {
                "height": dp(56),
                "text": f"{item}",
                "on_release": lambda x=f"{item}": dat_mo_hinh(x, root),
            } for i, item in enumerate(['Naive Bayes', 'SVM', 'Logistic Regression'])]
        self.menu = MDDropdownMenu(
            caller=root.ids.LoaiMoHinh,
            items=menu_items,
            width_mult=4       
        )
        self.menu.check_position_caller = (None, None, None)
        self.menu.open()

    def phan_loai(self, noi_dung, mo_hinh, ket_qua):
        if mo_hinh == 'Naive Bayes':
            mo_hinh = 'naive_bayes'
        elif mo_hinh == 'SVM':
            mo_hinh = 'svm'
        else:
            mo_hinh = 'logistic_regression'

        du_lieu = {"content": noi_dung, "type_model": mo_hinh}
        print(du_lieu)
        response = requests.post(
            "http://13.236.68.213:8000/classifier_news",
            data=json.dumps(du_lieu),
            headers={'Content-Type': 'application/json',
        })
        # Kiểm tra mã trạng thái của yêu cầu
        if response.status_code == 200:
            res = response.json()
            ket_qua.text = f"Kết quả trên {res['type_model']}: {res['result']}"
        else:
            ket_qua.text = f"Lỗi trong quá trình gửi yêu cầu: {response.status_code}"
            
MainApp().run()