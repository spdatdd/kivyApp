from random import sample, randint
from string import ascii_lowercase
from time import asctime

from kivymd.app import MDApp
from kivy.factory import Factory
from kivy.lang import Builder
from kivy.properties import NumericProperty, ListProperty, StringProperty, BooleanProperty
from kivy.clock import Clock
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.boxlayout import MDBoxLayout

from kivy.clock import mainthread
import random
from threading import Thread
from time import sleep
from kivy.metrics import dp


KV = """
<HomeCard>:
    orientation: "vertical"
    radius: 16

    MDBoxLayout:
        padding: '10dp'

        MDLabel:
            id: label
            text: root.text
            markup: True
            color: "grey"
            bold: True
            halign: 'left'
            valign: 'top'
            text_size: None, None

    MDRelativeLayout:
        adaptive_height: True
        MDRelativeLayout:
            size_hint: .2, None

            FitImage:
                id: img
                source: 'assets/images/image.jpeg'
                radius: self.width/2, self.width/2, self.width/2, self.width/2
                size_hint: .75, .75
                pos_hint: {'center_x': .5, 'center_y': .5}
                canvas.before:
                    Color:
                        rgba: 0,0,0,.5
                    Ellipse:
                        pos: self.pos
                        size: self.size
        MDIconButton:
            icon: "arrow-up-bold"
            pos_hint: {"right": .9}

        MDIconButton:
            icon: "arrow-down-bold"
            pos_hint: {"right": 1}

MDRelativeLayout:

    FixedRecycleView:
        id: rv
        data: app.data
        viewclass: 'HomeCard'
        scrollable_distance: box.height - self.height
        do_scroll_x: False
        do_scroll_y: True
        on_scroll_y: app.check_pull_refresh(self, box)


        RecycleBoxLayout:
            id: box
            orientation: 'vertical'
            spacing: '5dp'
            size_hint_y: None
            height: self.minimum_height
            default_size_hint: 1, None
            default_size: None, dp(150)
    
    Label:
        opacity: 1 if app.refreshing or rv.scroll_y < 0 else 0
        size_hint_y: None
        pos_hint: {'top': 1}
        text: 'Refreshing…' if app.refreshing else 'Pull up to refresh'
"""


class HomeCard(RecycleDataViewBehavior, MDBoxLayout):
    text = StringProperty()
    chu_de = StringProperty()
    index = None

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super().refresh_view_attrs(rv, index, data)


class FixedRecycleView(Factory.RecycleView):
    distance_to_top = NumericProperty()
    scrollable_distance = NumericProperty()

    def on_scrollable_distance(self, *args):
        if self.scroll_y > 0:
            self.scroll_y = (self.scrollable_distance - self.distance_to_top) / self.scrollable_distance


class Application(MDApp):
    data = ListProperty([])
    refreshing = BooleanProperty()


    def build(self):
        self.theme_cls.theme_style = 'Dark'
        self.refresh_data()
        return Builder.load_string(KV)
            

    def add_data(self):
        for i in range(10):
            self.data.append({
                    "text": f'{random.random()}',
                    "chu_de": "dt['chu_de']",
                    "selected": False
                })


    def check_pull_refresh(self, view, grid):
        """Check the amount of overscroll to decide if we want to trigger the
        refresh or not.
        """
        view.distance_to_top = (1 - view.scroll_y) * view.scrollable_distance

        max_pixel = dp(200)
        to_relative = max_pixel / (grid.height - view.height)
        if view.scroll_y + to_relative >= 0  or self.refreshing:
            return

        self.refresh_data()


    def refresh_data(self):
        # using a Thread to do a potentially long operation without blocking
        # the UI.
        self.refreshing = True
        Thread(target=self._refresh_data).start()


    def _refresh_data(self):
        sleep(2)

        self.prepend_data(
            [{
                "text": f'{random.random()}',
                "chu_de": "dt['chu_de']",
                "selected": False
            } for i in range(10)])


    @mainthread
    def prepend_data(self, data):
        self.data = self.data + data
        self.refreshing = False


if __name__ == '__main__':
    Application().run()