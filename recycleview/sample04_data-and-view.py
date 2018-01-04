# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty, AliasProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
import random


Builder.load_string("""
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: self.bgcolor
        Rectangle:
            pos: self.pos
            size: self.size
    color: self.textcolor

<MainView>
    RecycleView:
        id: rv
        viewclass: 'SelectableLabel'
        SelectableRecycleBoxLayout:
            default_size_x: None
            default_size_hint: 1.0, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
            multiselect: False
            touch_multiselect: False
""")


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def _get_bgcolor(self):
        if self.selectable:
            if self.selected:
                return [0, 0.4, 0.6, 1]
            else:
                return [0.3, 0.3, 0.3, 1]
        else:
            return [0, 0, 0, 1]
    bgcolor = AliasProperty(_get_bgcolor, None, bind=['selected', 'selectable'])

    def _get_textcolor(self):
        if self.selectable:
            if self.selected:
                return [0, 0, 0, 1]
            else:
                return [1, 1, 1, 1]
        else:
            return [0.5, 0.5, 0.5, 1.0]
    textcolor = AliasProperty(_get_textcolor, None, bind=['selected', 'selectable'])

    def refresh_view_attrs(self, rv, index, data):
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        self.selected = is_selected


class MainView(ModalView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        data = []
        for i in range(100):
            data.append({  # these attributes are assigned to SelectableLabel
                'text': str(i),
                'selectable': (i % 2 != 0),  # you can set selectable/unselectable state for each item
                'height': dp(56) * (0.2+1.2*random.random()),  # also can set size/position attributes
                'size_hint_y': None,
            })
        self.ids.rv.data = data


class TestApp(App):
    def get_application_name(self):
        return "Recycleview sample -data&view-"

    def build(self):
        return MainView()


if __name__ == '__main__':
    TestApp().run()
