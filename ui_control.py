# ui_control.py
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from datetime import datetime
from db import CalorieLogic


class UIControl:
    def __init__(self, layout):
        self.layout = layout
        self.total_calories = 0
        self.daily_goal = 2000
        self.meals = []

        self.logic = CalorieLogic(self)
        self.setup_events()

    def setup_events(self):
        self.layout.add_button.bind(on_press=self.show_add_meal_popup)
        self.layout.settings_button.bind(on_press=self.open_settings)
        self.layout.history_button.bind(on_press=self.show_history)
        self.layout.reports_button.bind(on_press=self.show_reports)
        self.layout.profile_button.bind(on_press=self.show_profile)

    def show_add_meal_popup(self, instance):
        content = BoxLayout(orientation='vertical', spacing=15, padding=25)

        # Заголовок
        content.add_widget(Label(
            text='Добавить прием пищи:',
            color=(0, 0, 0, 1),
            font_size='28sp',
            size_hint_y=0.08,
            bold=True
        ))

        # Переключатель типа ввода
        input_type_layout = BoxLayout(size_hint_y=0.08, spacing=10)
        simple_btn = ToggleButton(
            text='Только калории',
            group='input_type',
            state='down',
            font_size='18sp'
        )
        detailed_btn = ToggleButton(
            text='Калории + граммы',
            group='input_type',
            font_size='18sp'
        )
        input_type_layout.add_widget(simple_btn)
        input_type_layout.add_widget(detailed_btn)
        content.add_widget(input_type_layout)

        # Поле названия еды с подписью
        food_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.1)
        food_label = Label(
            text='Название еды:',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        food_label.bind(size=food_label.setter('text_size'))
        food_input = TextInput(
            multiline=False,
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        food_layout.add_widget(food_label)
        food_layout.add_widget(food_input)
        content.add_widget(food_layout)

        # Поля для простого ввода (только калории)
        simple_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.1)
        simple_calories_label = Label(
            text='Общие калории:',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        simple_calories_label.bind(size=simple_calories_label.setter('text_size'))
        calories_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        simple_layout.add_widget(simple_calories_label)
        simple_layout.add_widget(calories_input)
        content.add_widget(simple_layout)

        # Поля для подробного ввода (калории + граммы)
        detailed_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.2)
        detailed_layout.height = 0
        detailed_layout.opacity = 0

        # Калории на 100г
        calories_100_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.5)
        calories_100_label = Label(
            text='Калорий на 100г:',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        calories_100_label.bind(size=calories_100_label.setter('text_size'))
        calories_per_100_input = TextInput(
            multiline=False,
            input_filter='int',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        calories_100_layout.add_widget(calories_100_label)
        calories_100_layout.add_widget(calories_per_100_input)

        # Граммы
        grams_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.5)
        grams_label = Label(
            text='Съедено грамм:',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        grams_label.bind(size=grams_label.setter('text_size'))
        grams_input = TextInput(
            text='100',
            multiline=False,
            input_filter='int',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        grams_layout.add_widget(grams_label)
        grams_layout.add_widget(grams_input)

        detailed_layout.add_widget(calories_100_layout)
        detailed_layout.add_widget(grams_layout)
        content.add_widget(detailed_layout)

        # Заголовок КБЖУ
        content.add_widget(Label(
            text='КБЖУ (опционально):',
            size_hint_y=0.05,
            color=(0, 0, 0, 1),
            font_size='22sp',
            bold=True
        ))

        # Поля КБЖУ
        kbju_layout = BoxLayout(orientation='vertical', spacing=10, size_hint_y=0.3)

        # Белки
        protein_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.33)
        protein_label = Label(
            text='Белки (г):',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        protein_label.bind(size=protein_label.setter('text_size'))
        protein_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        protein_layout.add_widget(protein_label)
        protein_layout.add_widget(protein_input)

        # Жиры
        fats_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.33)
        fats_label = Label(
            text='Жиры (г):',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        fats_label.bind(size=fats_label.setter('text_size'))
        fats_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        fats_layout.add_widget(fats_label)
        fats_layout.add_widget(fats_input)

        # Углеводы
        carbs_layout = BoxLayout(orientation='horizontal', spacing=15, size_hint_y=0.33)
        carbs_label = Label(
            text='Углеводы (г):',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_x=0.4,
            halign='left',
            text_size=(None, None)
        )
        carbs_label.bind(size=carbs_label.setter('text_size'))
        carbs_input = TextInput(
            multiline=False,
            input_filter='float',
            size_hint_x=0.6,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15]
        )
        carbs_layout.add_widget(carbs_label)
        carbs_layout.add_widget(carbs_input)

        kbju_layout.add_widget(protein_layout)
        kbju_layout.add_widget(fats_layout)
        kbju_layout.add_widget(carbs_layout)
        content.add_widget(kbju_layout)

        # Функции переключения
        def toggle_input_type(instance, value):
            if instance.text == 'Калории + граммы' and value == 'down':
                detailed_layout.height = 120
                detailed_layout.opacity = 1
                simple_layout.height = 0
                simple_layout.opacity = 0
            else:
                detailed_layout.height = 0
                detailed_layout.opacity = 0
                simple_layout.height = 60
                simple_layout.opacity = 1

        simple_btn.bind(state=toggle_input_type)
        detailed_btn.bind(state=toggle_input_type)

        # Кнопки
        btn_layout = BoxLayout(spacing=20, size_hint_y=0.15)

        def save_meal(instance):
            food = food_input.text.strip()

            if not food:
                self.logic.show_message("Ошибка", "Введите название еды!")
                return

            # Определяем тип ввода
            if detailed_btn.state == 'down':
                # Ввод: калорийность на 100г + граммовка
                calories_per_100 = calories_per_100_input.text.strip()
                grams_eaten = grams_input.text.strip()

                if not calories_per_100 or not grams_eaten:
                    self.logic.show_message("Ошибка", "Заполните калорийность и граммы!")
                    return

                try:
                    total_calories = int(calories_per_100) * int(grams_eaten) // 100
                    grams = grams_eaten
                except ValueError:
                    self.logic.show_message("Ошибка", "Проверьте правильность чисел!")
                    return
            else:
                # Простой ввод: общие калории
                calories_total = calories_input.text.strip()

                if not calories_total:
                    self.logic.show_message("Ошибка", "Введите калории!")
                    return

                try:
                    total_calories = int(calories_total)
                    grams = '100'  # По умолчанию
                except ValueError:
                    self.logic.show_message("Ошибка", "Введите число калорий!")
                    return

            # Получаем КБЖУ
            protein_text = protein_input.text.strip()
            fats_text = fats_input.text.strip()
            carbs_text = carbs_input.text.strip()

            if self.logic.add_meal(food, str(total_calories), grams, protein_text, fats_text, carbs_text):
                # Очищаем поля после сохранения
                food_input.text = ''
                calories_input.text = ''
                calories_per_100_input.text = ''
                grams_input.text = '100'
                protein_input.text = ''
                fats_input.text = ''
                carbs_input.text = ''
                popup.dismiss()

        btn_save = Button(
            text='Добавить',
            on_press=save_meal,
            font_size='24sp',
            background_color=(0.3, 0.7, 0.3, 1),
            size_hint_y=1
        )
        btn_cancel = Button(
            text='Отмена',
            on_press=lambda x: popup.dismiss(),
            font_size='24sp',
            background_color=(0.8, 0.3, 0.3, 1),
            size_hint_y=1
        )

        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)
        content.add_widget(btn_layout)

        popup = Popup(
            title='Добавить еду',
            content=content,
            size_hint=(0.95, 0.95),
            title_size='20sp',
            title_align='center'
        )

        # Инициализируем видимость
        simple_layout.height = 60
        simple_layout.opacity = 1
        detailed_layout.height = 0
        detailed_layout.opacity = 0

        popup.open()

    # Остальные методы остаются без изменений...
    def edit_meal(self, meal_id):
        self.logic.edit_meal(meal_id)

    def delete_meal(self, meal_id):
        self.logic.delete_meal(meal_id)

    def update_stats(self):
        pass

    def open_settings(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button
        from kivy.uix.textinput import TextInput

        content = BoxLayout(orientation='vertical', spacing=15, padding=20)

        goal_label = Label(
            text='Дневная норма калорий:',
            color=(0, 0, 0, 1),
            font_size='22sp',
            size_hint_y=0.2
        )
        content.add_widget(goal_label)

        goal_input = TextInput(
            text=str(self.daily_goal),
            multiline=False,
            input_filter='int',
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1),
            font_size='22sp',
            padding=[15, 15],
            size_hint_y=0.3
        )
        content.add_widget(goal_input)

        def save_goal(instance):
            try:
                new_goal = int(goal_input.text)
                if self.logic.update_daily_goal(new_goal):
                    popup.dismiss()
            except ValueError:
                pass

        btn_layout = BoxLayout(spacing=15, size_hint_y=0.3)
        btn_layout.add_widget(Button(
            text='Отмена',
            on_press=lambda x: popup.dismiss(),
            font_size='20sp'
        ))
        btn_layout.add_widget(Button(
            text='Сохранить',
            on_press=save_goal,
            font_size='20sp'
        ))
        content.add_widget(btn_layout)

        popup = Popup(title='Настройки', content=content, size_hint=(0.8, 0.5))
        popup.open()

    def show_history(self, instance):
        meals_count = len(self.meals)
        self.layout.progress_label.text = f"Записей сегодня: {meals_count}"
        self.layout.progress_label.color = (0.6, 0.4, 0.8, 1)

    def show_reports(self, instance):
        report = self.logic.get_weekly_report()
        if report:
            today_calories = self.total_calories
            self.layout.progress_label.text = f"Неделя: {len(report)} дней"
        else:
            self.layout.progress_label.text = "Нет данных за неделю"
        self.layout.progress_label.color = (0.4, 0.6, 0.8, 1)

    def show_profile(self, instance):
        self.layout.progress_label.text = f"Цель: {self.daily_goal} ккал"
        self.layout.progress_label.color = (0.8, 0.8, 0.4, 1)

    def show_history(self, instance):
        from kivy.uix.popup import Popup
        from kivy.uix.boxlayout import BoxLayout
        from kivy.uix.button import Button

        content = BoxLayout(orientation='vertical', spacing=15, padding=20)

        def clear_today(instance):
            self.logic.clear_today_meals()
            popup.dismiss()

        def clear_all(instance):
            self.logic.clear_all_meals()
            popup.dismiss()

        btn1 = Button(
            text='Очистить сегодня',
            size_hint_y=0.25,
            on_press=clear_today,
            font_size='18sp'
        )
        btn2 = Button(
            text='Очистить всю историю',
            size_hint_y=0.25,
            on_press=clear_all,
            font_size='18sp'
        )
        btn3 = Button(
            text='Отмена',
            size_hint_y=0.25,
            on_press=lambda x: popup.dismiss(),
            font_size='18sp'
        )

        content.add_widget(Label(
            text=f'Записей сегодня: {len(self.meals)}',
            color=(0, 0, 0, 1),
            font_size='20sp',
            size_hint_y=0.25
        ))
        content.add_widget(btn1)
        content.add_widget(btn2)
        content.add_widget(btn3)

        popup = Popup(title='Управление историей', content=content, size_hint=(0.8, 0.6))
        popup.open()