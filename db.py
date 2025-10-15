# db.py
import sqlite3
from datetime import datetime
from kivy.uix.label import Label
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.togglebutton import ToggleButton
from ui_layouts import MealItem


class CalorieLogic:
    def __init__(self, ui_control):
        self.ui_control = ui_control
        self.init_db()
        self.load_today_data()

    def init_db(self):
        self.conn = sqlite3.connect('calories.db', check_same_thread=False)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS meals (
                id INTEGER PRIMARY KEY,
                food TEXT NOT NULL,
                calories INTEGER NOT NULL,
                grams INTEGER DEFAULT 100,
                protein REAL DEFAULT 0,
                fats REAL DEFAULT 0,
                carbs REAL DEFAULT 0,
                timestamp TEXT DEFAULT CURRENT_TIMESTAMP
            )
        ''')

        # Добавляем недостающие колонки
        columns_to_add = [
            ('grams', 'INTEGER DEFAULT 100'),
            ('protein', 'REAL DEFAULT 0'),
            ('fats', 'REAL DEFAULT 0'),
            ('carbs', 'REAL DEFAULT 0')
        ]

        for column_name, column_type in columns_to_add:
            try:
                self.cursor.execute(f"ALTER TABLE meals ADD COLUMN {column_name} {column_type}")
            except sqlite3.OperationalError:
                pass

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS settings (
                key TEXT PRIMARY KEY,
                value TEXT
            )
        ''')

        self.cursor.execute('SELECT value FROM settings WHERE key = "daily_goal"')
        if not self.cursor.fetchone():
            self.cursor.execute('INSERT INTO settings VALUES ("daily_goal", "2000")')

        self.conn.commit()

    def load_today_data(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute('''
            SELECT id, food, calories, grams, protein, fats, carbs, timestamp FROM meals 
            WHERE date(timestamp) = ? ORDER BY timestamp DESC
        ''', (today,))

        meals = self.cursor.fetchall()
        self.ui_control.meals = []
        self.ui_control.layout.meals_layout.clear_widgets()

        for meal_id, food, calories, grams, protein, fats, carbs, timestamp in meals:
            try:
                time_obj = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")
            except:
                time_obj = datetime.now()

            meal_item = MealItem(
                meal_id=meal_id,
                food=food,
                calories=calories,
                grams=grams,
                protein=protein,
                fats=fats,
                carbs=carbs,
                timestamp=time_obj,
                controller=self.ui_control
            )
            self.ui_control.layout.meals_layout.add_widget(meal_item)

        self.update_stats()

    def add_meal(self, food: str, calories_text: str, grams_text: str = "100",
                 protein_text: str = "", fats_text: str = "", carbs_text: str = ""):
        if not food or not calories_text:
            self.show_message("Ошибка", "Введите название и калории!")
            return False

        try:
            calories = int(calories_text)
            grams = int(grams_text) if grams_text else 100
            protein = float(protein_text) if protein_text else 0
            fats = float(fats_text) if fats_text else 0
            carbs = float(carbs_text) if carbs_text else 0

            self.cursor.execute(
                'INSERT INTO meals (food, calories, grams, protein, fats, carbs) VALUES (?, ?, ?, ?, ?, ?)',
                (food, calories, grams, protein, fats, carbs)
            )
            self.conn.commit()

            self.load_today_data()
            return True

        except ValueError:
            self.show_message("Ошибка", "Проверьте правильность введенных чисел!")
            return False

    def edit_meal(self, meal_id: int):
        self.cursor.execute('SELECT food, calories, grams, protein, fats, carbs FROM meals WHERE id = ?', (meal_id,))
        result = self.cursor.fetchone()

        if not result:
            self.show_message("Ошибка", "Запись не найдена!")
            return

        current_food, current_calories, current_grams, current_protein, current_fats, current_carbs = result

        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        food_input = TextInput(
            text=current_food,
            hint_text='Название еды',
            multiline=False,
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        calories_input = TextInput(
            text=str(current_calories),
            hint_text='Калории',
            multiline=False,
            input_filter='int',
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        grams_input = TextInput(
            text=str(current_grams),
            hint_text='Граммы',
            multiline=False,
            input_filter='int',
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        # Поля КБЖУ
        protein_input = TextInput(
            text=str(current_protein),
            hint_text='Белки (г)',
            multiline=False,
            input_filter='float',
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        fats_input = TextInput(
            text=str(current_fats),
            hint_text='Жиры (г)',
            multiline=False,
            input_filter='float',
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        carbs_input = TextInput(
            text=str(current_carbs),
            hint_text='Углеводы (г)',
            multiline=False,
            input_filter='float',
            size_hint_y=0.15,
            background_color=(1, 1, 1, 1),
            foreground_color=(0, 0, 0, 1)
        )

        btn_layout = BoxLayout(spacing=10, size_hint_y=0.1)

        def save_changes(btn):
            new_food = food_input.text.strip()
            new_calories_text = calories_input.text.strip()
            new_grams_text = grams_input.text.strip()
            new_protein_text = protein_input.text.strip()
            new_fats_text = fats_input.text.strip()
            new_carbs_text = carbs_input.text.strip()

            if not new_food or not new_calories_text:
                self.show_message("Ошибка", "Заполните название и калории!")
                return

            try:
                new_calories = int(new_calories_text)
                new_grams = int(new_grams_text) if new_grams_text else 100
                new_protein = float(new_protein_text) if new_protein_text else 0
                new_fats = float(new_fats_text) if new_fats_text else 0
                new_carbs = float(new_carbs_text) if new_carbs_text else 0

                self.cursor.execute(
                    'UPDATE meals SET food = ?, calories = ?, grams = ?, protein = ?, fats = ?, carbs = ? WHERE id = ?',
                    (new_food, new_calories, new_grams, new_protein, new_fats, new_carbs, meal_id)
                )
                self.conn.commit()

                self.load_today_data()
                popup.dismiss()
                self.show_message("Успех", "Запись обновлена!")

            except ValueError:
                self.show_message("Ошибка", "Проверьте правильность введенных чисел!")

        btn_save = Button(text='Сохранить', on_press=save_changes)
        btn_cancel = Button(text='Отмена', on_press=lambda x: popup.dismiss())

        btn_layout.add_widget(btn_save)
        btn_layout.add_widget(btn_cancel)

        content.add_widget(Label(text='Редактировать запись:', color=(0, 0, 0, 1)))
        content.add_widget(food_input)
        content.add_widget(calories_input)
        content.add_widget(grams_input)
        content.add_widget(protein_input)
        content.add_widget(fats_input)
        content.add_widget(carbs_input)
        content.add_widget(btn_layout)

        popup = Popup(title='Редактирование', content=content, size_hint=(0.9, 0.8))
        popup.open()

    # Остальные методы без изменений
    def delete_meal(self, meal_id: int):
        content = BoxLayout(orientation='vertical', spacing=10, padding=10)

        btn_layout = BoxLayout(spacing=10, size_hint_y=0.4)

        def confirm_delete(btn):
            self.cursor.execute('DELETE FROM meals WHERE id = ?', (meal_id,))
            self.conn.commit()

            self.load_today_data()
            popup.dismiss()
            self.show_message("Успех", "Запись удалена!")

        btn_yes = Button(text='Да, удалить', on_press=confirm_delete)
        btn_no = Button(text='Отмена', on_press=lambda x: popup.dismiss())

        btn_layout.add_widget(btn_yes)
        btn_layout.add_widget(btn_no)

        content.add_widget(Label(text='Вы уверены, что хотите удалить эту запись?', color=(0, 0, 0, 1)))
        content.add_widget(btn_layout)

        popup = Popup(title='Подтверждение удаления', content=content, size_hint=(0.7, 0.3))
        popup.open()

    def update_stats(self):
        today = datetime.now().strftime("%Y-%m-%d")

        self.cursor.execute('''
            SELECT SUM(calories) FROM meals WHERE date(timestamp) = ?
        ''', (today,))

        total = self.cursor.fetchone()[0] or 0

        self.cursor.execute('SELECT value FROM settings WHERE key = "daily_goal"')
        daily_goal = int(self.cursor.fetchone()[0])

        self.ui_control.total_calories = total
        self.ui_control.daily_goal = daily_goal
        self.ui_control.layout.stats_label.text = f"Сегодня: {total}/{daily_goal} ккал"

        remaining = daily_goal - total
        if remaining > 0:
            self.ui_control.layout.progress_label.text = f"Осталось: {remaining} ккал"
            self.ui_control.layout.progress_label.color = (0.3, 0.6, 0.3, 1)
        else:
            self.ui_control.layout.progress_label.text = "Норма превышена!"
            self.ui_control.layout.progress_label.color = (0.8, 0.2, 0.2, 1)

    def update_daily_goal(self, new_goal: int):
        try:
            self.cursor.execute(
                'UPDATE settings SET value = ? WHERE key = "daily_goal"',
                (str(new_goal),)
            )
            self.conn.commit()
            self.update_stats()
            return True
        except:
            return False

    def get_weekly_report(self):
        self.cursor.execute('''
            SELECT date(timestamp), SUM(calories) FROM meals 
            WHERE timestamp >= date('now', '-7 days') 
            GROUP BY date(timestamp) ORDER BY date(timestamp) DESC
        ''')
        return self.cursor.fetchall()

    def clear_today_meals(self):
        today = datetime.now().strftime("%Y-%m-%d")
        self.cursor.execute('DELETE FROM meals WHERE date(timestamp) = ?', (today,))
        self.conn.commit()
        self.load_today_data()
        self.show_message("Успех", "Сегодняшние приемы пищи очищены!")

    def clear_all_meals(self):
        self.cursor.execute('DELETE FROM meals')
        self.conn.commit()
        self.load_today_data()
        self.show_message("Успех", "Вся история очищена!")

    def show_message(self, title, message):
        content = Label(text=message, color=(0, 0, 0, 1))
        popup = Popup(title=title, content=content, size_hint=(0.8, 0.4))
        popup.open()

    def close_db(self):
        self.conn.close()