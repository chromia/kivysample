from kivy.app import App
from kivy.lang import Builder
from kivy.uix.modalview import ModalView


Builder.load_string('''
<CustomButton@Button>
    on_press: print(self.text)

<MainView>:
    RecycleView:
        id: rv
        viewclass: 'CustomButton'
        key_selection: True
        RecycleGridLayout:
            cols: 4
            default_size: None, dp(56)
            default_size_hint: 1/4, None
            size_hint_y: None
            height: self.minimum_height
            orientation: 'vertical'
''')


class MainView(ModalView):
    def __init__(self, **kwargs):
        super(MainView, self).__init__(**kwargs)
        self.ids.rv.data = [{'text': str(x)} for x in range(100)]


class TestApp(App):
    def get_application_name(self):
        return "Recycleview sample -unselectable-"

    def build(self):
        return MainView()


if __name__ == '__main__':
    TestApp().run()
