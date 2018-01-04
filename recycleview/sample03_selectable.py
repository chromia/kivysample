# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.app import App
from kivy.lang import Builder


Builder.load_string("""
<SelectableLabel>:
    # Draw a background to indicate selection
    canvas.before:
        Color:
            rgba: (0, 0.4, 0.6, 1) if self.selected else (0, 0, 0, 1)
        Rectangle:
            pos: self.pos
            size: self.size
    color: (0, 0, 0, 1) if self.selected else (1, 1, 1, 1)

<MainView>
    BoxLayout:
        RecycleView:
            id: rv1
            viewclass: 'SelectableLabel'
            SelectableRecycleBoxLayout:
                default_size: None, dp(56)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: False
        RecycleView:
            id: rv2
            viewclass: 'SelectableLabel'
            SelectableRecycleGridLayout:
                cols: 4
                default_size: None, dp(56)
                default_size_hint: 1/4, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
                touch_multiselect: False
""")


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class SelectableRecycleGridLayout(LayoutSelectionBehavior, RecycleGridLayout):
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        ''' Catch and handle the view changes '''
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(
            rv, index, data)

    def on_touch_down(self, touch):
        ''' Add selection on touch down '''
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        ''' Respond to the selection of items in the view. '''
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class MainView(ModalView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        data = [{'text': str(x)} for x in range(100)]
        self.ids.rv1.data = data
        self.ids.rv2.data = data


class TestApp(App):
    def get_application_name(self):
        return "Recycleview sample -selectable-"

    def build(self):
        return MainView()


if __name__ == '__main__':
    TestApp().run()
