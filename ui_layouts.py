# ui_layouts.py
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from datetime import datetime


class MealItem(BoxLayout):
    def __init__(self, meal_id, food, calories, grams, protein, fats, carbs, timestamp, controller, **kwargs):
        super().__init__(**kwargs)
        self.meal_id = meal_id
        self.controller = controller
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = 60  # Увеличил высоту для лучшей читаемости
        self.spacing = 10
        self.padding = [10, 5]

        if isinstance(timestamp, str):
            try:
                time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
                time_str = time_obj.strftime("%H:%M")
            except:
                time_str = timestamp
        elif isinstance(timestamp, datetime):
            time_str = timestamp.strftime("%H:%M")
        else:
            time_str = str(timestamp)

        # Формируем текст в зависимости от данных
        base_text = f"{time_str} - {food}: {calories}к"

        # Добавляем граммы только если не 100
        if grams and grams != 100:
            base_text += f" ({grams}г)"

        # Добавляем КБЖУ если они есть
        kbju_text = ""
        if protein or fats or carbs:
            kbju_parts = []
            if protein:
                kbju_parts.append(f"Б:{protein}")
            if fats:
                kbju_parts.append(f"Ж:{fats}")
            if carbs:
                kbju_parts.append(f"У:{carbs}")
            if kbju_parts:
                kbju_text = " " + " ".join(kbju_parts)

        meal_text = base_text + kbju_text

        self.label = Label(
            text=meal_text,
            size_hint_x=0.7,
            text_size=(None, None),
            halign='left',
            valign='middle',
            color=(0, 0, 0, 1),
            font_size='16sp'  # Увеличил шрифт для лучшей читаемости
        )
        self.label.bind(size=self.label.setter('text_size'))

        # Контейнер для кнопок
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_x=0.3,
            spacing=5
        )

        self.edit_btn = Button(
            text='✏️',
            size_hint_x=0.5,
            background_color=(0.9, 0.7, 0.3, 1),
            font_size='18sp'
        )
        self.edit_btn.bind(on_press=self.edit_meal)

        self.delete_btn = Button(
            text='🗑️',
            size_hint_x=0.5,
            background_color=(0.9, 0.3, 0.3, 1),
            font_size='18sp'
        )
        self.delete_btn.bind(on_press=self.delete_meal)

        buttons_layout.add_widget(self.edit_btn)
        buttons_layout.add_widget(self.delete_btn)

        self.add_widget(self.label)
        self.add_widget(buttons_layout)

    def edit_meal(self, instance):
        self.controller.edit_meal(self.meal_id)

    def delete_meal(self, instance):
        self.controller.delete_meal(self.meal_id)


class MainLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.padding = 20
        self.spacing = 15
        self.create_ui()

        from ui_control import UIControl
        self.controller = UIControl(self)

    def create_ui(self):
        # Заголовок
        header = Label(
            text="Счетчик калорий",
            size_hint_y=None,
            height=60,
            font_size='28sp',  # Увеличил шрифт
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        self.add_widget(header)

        # Основная кнопка добавления
        input_layout = BoxLayout(size_hint_y=None, height=70, spacing=10)
        self.add_button = Button(
            text='➕ Добавить прием пищи',
            background_color=(0.3, 0.7, 0.3, 1),
            color=(1, 1, 1, 1),
            size_hint_x=1,
            font_size='20sp',  # Увеличил шрифт
            bold=True
        )
        input_layout.add_widget(self.add_button)
        self.add_widget(input_layout)

        # Статистика
        stats_layout = BoxLayout(size_hint_y=None, height=70, spacing=10)
        self.stats_label = Label(
            text="Сегодня: 0/2000 ккал",
            font_size='20sp',  # Увеличил шрифт
            bold=True,
            color=(0.2, 0.2, 0.2, 1)
        )
        self.settings_button = Button(
            text='⚙️ Настройки',
            background_color=(0.4, 0.4, 0.6, 1),
            color=(1, 1, 1, 1),
            size_hint_x=0.4,
            font_size='16sp'
        )

        stats_layout.add_widget(self.stats_label)
        stats_layout.add_widget(self.settings_button)
        self.add_widget(stats_layout)

        # Прогресс
        self.progress_label = Label(
            text="Добавьте первую запись!",
            size_hint_y=None,
            height=50,
            color=(0.5, 0.5, 0.5, 1),
            font_size='16sp'  # Увеличил шрифт
        )
        self.add_widget(self.progress_label)

        # Кнопки навигации
        buttons_layout = BoxLayout(size_hint_y=None, height=70, spacing=10)
        self.history_button = Button(
            text='📊 История',
            background_color=(0.7, 0.5, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.reports_button = Button(
            text='📈 Отчеты',
            background_color=(0.4, 0.6, 0.8, 1),
            color=(1, 1, 1, 1),
            font_size='16sp'
        )
        self.profile_button = Button(
            text='👤 Профиль',
            background_color=(0.8, 0.8, 0.4, 1),
            color=(0.2, 0.2, 0.2, 1),
            font_size='16sp'
        )

        buttons_layout.add_widget(self.history_button)
        buttons_layout.add_widget(self.reports_button)
        buttons_layout.add_widget(self.profile_button)
        self.add_widget(buttons_layout)

        # Список приемов пищи
        scroll = ScrollView()
        self.meals_layout = BoxLayout(
            orientation='vertical',
            size_hint_y=None,
            spacing=8,
            padding=10
        )
        self.meals_layout.bind(minimum_height=self.meals_layout.setter('height'))
        scroll.add_widget(self.meals_layout)
        self.add_widget(scroll)