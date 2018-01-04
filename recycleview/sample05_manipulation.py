# -*- coding: utf-8 -*-

from kivy.properties import BooleanProperty
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
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
        orientation: 'vertical'
        ActionBar:
            ActionView:
                ActionPrevious:
                ActionButton:
                    text: 'SelectAll'
                    on_release: root.on_selectall()
                ActionButton:
                    text: 'UnselectAll'
                    on_release: root.on_unselectall()
                ActionButton:
                    text: 'Add Data'
                    on_release: root.on_adddata()
                ActionButton:
                    text: 'Del Selected'
                    on_release: root.on_removedata()
                ActionButton:
                    text: 'Reset'
                    on_release: root.on_reset()
        RecycleView:
            id: rv
            viewclass: 'SelectableLabel'
            SelectableRecycleBoxLayout:
                key_selection: 'selectable'  # important to select items by code
                default_size: None, dp(56)
                default_size_hint: 1.0, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: True
                touch_multiselect: True
""")


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    pass

class SelectableLabel(RecycleDataViewBehavior, Label):
    ''' Add selection support to the Label '''
    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

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
        # !important! : index validation
        # if you remove raw data entry, The value of index arg be less than the value of self.index.
        # Or the value of index arg indicates out of bounds of 'data' array.
        # note: after leave this function, refresh_view_attrs() are called. so you should be re-assign self.index.
        if (self.index == index) and (index < len(rv.data)):
            rv.data[index]['selected'] = is_selected


def makedata(text, selectable=True, selected=False):
    return {'text': text, 'selectable': selectable, 'selected': selected}

def makeinitialdata():
    data = []
    for i in range(8):
        data.append(makedata(str(i)))
    return data

class MainView(ModalView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.ids.rv.data = makeinitialdata()

    def on_selectall(self):
        # select all items ( but only 'selectable' attr == True)
        # update raw data
        data = self.ids.rv.data
        for v in data:
            if v['selectable']:
                v['selected'] = True
        # refresh visible items
        lm = self.ids.rv.layout_manager
        for node in lm.get_selectable_nodes():
            lm.select_node(node)  # SelectableRecycleBoxLayout.key_selection: 'selectable' is required

    def on_unselectall(self):
        # deselect all items
        # update raw data
        data = self.ids.rv.data
        for v in data:
            if v['selectable']:
                v['selected'] = False
        # refresh visible items
        lm = self.ids.rv.layout_manager
        lm.clear_selection()

    def on_adddata(self):
        # add 3 items to tail of the view
        # update raw data
        data = self.ids.rv.data
        data.append(makedata('+'))
        data.append(makedata('++(unselectable)', False))  # This item will be not selected
        data.append(makedata('+++'))

    def on_removedata(self):
        # remove all selected data
        rv = self.ids.rv
        lm = rv.layout_manager
        # remove raw data
        rv.data = [v for i, v in enumerate(rv.data) if not (v['selectable'] and v['selected'])]
        # clear all selection state
        lm.clear_selection()

    def on_reset(self):
        # reset application state
        rv = self.ids.rv
        lm = rv.layout_manager
        lm.clear_selection()
        self.ids.rv.data = makeinitialdata()

class TestApp(App):
    def get_application_name(self):
        return "Recycleview sample -data manipulation-"

    def build(self):
        return MainView()


if __name__ == '__main__':
    TestApp().run()
