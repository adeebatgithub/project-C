from datetime import datetime

from kivy import platform
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.relativelayout import RelativeLayout
from plyer import battery

if platform == "android":
    from android.permissions import request_permissions, Permission

    request_permissions([
        Permission.WAKE_LOCK,
        Permission.BATTERY_STATS,
    ])


class MainScreen(RelativeLayout):

    def update_time(self, *args):
        self.ids.aod.ids.hour_label.text = datetime.now().strftime("%I")
        self.ids.aod.ids.minute_label.text = datetime.now().strftime("%M")

    def update_date(self, *args):
        self.ids.aod.ids.date_label.text = datetime.now().strftime("%a %d %b")

    @staticmethod
    def get_battery_status(*args):
        if platform == "android":
            return battery.status
        return {"isCharging": False, "percentage": 80}

    def update_battery_status(self, *args):
        status = self.get_battery_status()
        self.ids.aod.ids.percentage_label.text = str(int(status["percentage"])) + "%"
        if status["isCharging"]:
            self.ids.aod.ids.charging_label.text = "Connected to Charger"
        else:
            self.ids.aod.ids.charging_label.text = ""


class MainApp(App):

    def build(self):
        screen = MainScreen()
        Clock.schedule_interval(screen.update_time, 0)
        Clock.schedule_interval(screen.update_date, 0.1)
        Clock.schedule_interval(screen.update_battery_status, 0.2)
        return screen


MainApp().run()
