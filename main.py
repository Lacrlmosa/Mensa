from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivy.uix.image import AsyncImage
from kivy.clock import Clock
from kivymd.uix.screen import MDScreen
from kivy.uix.floatlayout import FloatLayout
from kivy.core.window import Window
from kivy.metrics import dp
import threading
import requests
from bs4 import BeautifulSoup
from datetime import datetime

TEXT_FOUND = "Today is the Day!"
TEXT_NOT_FOUND = "No Luck Today"
PNG_FOUND = "assets/Gluklich_1-removebg-preview.png"
PNG_NOT_FOUND = "assets/Bose_1-removebg-preview.png"
COLOR_FOUND = (0.6, 1.0, 0.4, 1)
COLOR_NOT_FOUND = "#ffc4b0"
TEXT_COLOR = (1, 1, 1, 1)

def get_today_date():
    return datetime.today().strftime('%Y-%m-%d')

def get_menu_url():
    today_date = get_today_date()
    return f"www.food./{today_date}-mensa.com"

def get_dish_name(session):
    url = get_menu_url()
    try:
        response = session.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        dish_name = soup.find("h1")
        return dish_name.text.strip() if dish_name else None
    except requests.exceptions.RequestException as e:
        print(f"Fehler beim Abrufen des Menüs: {e}")
        return None

def check_dish():
    session = requests.Session()
    dish = get_dish_name(session)
    #dish = None
    if dish:
        result = "Korean Fried Chicken" in dish
        print(f"Gericht gefunden: {dish} - Ergebnis: {result}")
        return (TEXT_FOUND, PNG_FOUND, COLOR_FOUND) if result else (TEXT_NOT_FOUND, PNG_NOT_FOUND, COLOR_NOT_FOUND), dish
    else:
        print("Kein Gericht gefunden.")
        return "Fehler beim Abrufen des Menüs.", PNG_NOT_FOUND, COLOR_NOT_FOUND, None

class MyApp(MDApp):
    def build(self):
        self.screen = MDScreen()
        self.layout = FloatLayout()

        self.image = AsyncImage(
            source="",
            size_hint=(1, 1),
            size=(dp(450), dp(450)),
            pos_hint={"center_x": 0.5, "top": 0.9},
            keep_ratio=True
        )

        self.label1 = MDLabel(
            text="Lade...",
            halign="center",
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            font_style="H2",
            font_size="24sp",
            pos_hint={"center_x": 0.5, "y": 0.3},
            size_hint_y=1,
        )

        self.label2 = MDLabel(
            text="",
            halign="center",
            theme_text_color="Custom",
            text_color=TEXT_COLOR,
            font_style="Body1",
            font_size="24sp",
            pos_hint={"center_x": 0.5, "y": 0.03},
            size_hint_y=1,
        )

        self.layout.add_widget(self.image)
        self.layout.add_widget(self.label1)
        self.layout.add_widget(self.label2)
        self.screen.add_widget(self.layout)

        threading.Thread(target=self.update_ui, daemon=True).start()
        return self.screen

    def update_ui(self):
        # Holen der Daten aus check_dish
        (text, img, color), dish = check_dish()
        Clock.schedule_once(lambda dt: self.update_components(text, img, color, dish))

    def update_components(self, text, img, color, dish):
        self.label1.text = text
        self.label1.text_color = (0.5, 0.0, 0.0, 1.0) if text == TEXT_NOT_FOUND else (0, 0.5, 0, 1)
        if text == TEXT_NOT_FOUND:
            self.label2.text = f"Aber es gibt Heute:\n{dish}"
        else:
            self.label2.opacity = 0

        self.image.source = img
        self.screen.md_bg_color = color


if __name__ == "__main__":
    MyApp().run()
