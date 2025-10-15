# main.py (без изменений)
from kivy.app import App
from kivy.core.window import Window
from ui_layouts import MainLayout

Window.clearcolor = (0.95, 0.95, 0.95, 1)

class CalorieCounterApp(App):
    def build(self):
        return MainLayout()

if __name__ == '__main__':
    CalorieCounterApp().run()