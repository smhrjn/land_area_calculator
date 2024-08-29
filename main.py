from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.app import App
from kivy.metrics import dp
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy import platform
import math
import re
import datetime

if platform == "android":
    from android.permissions import request_permissions, Permission, check_permission  # pylint: disable=import-error # type: ignore
    request_permissions([Permission.READ_EXTERNAL_STORAGE,
                        Permission.WRITE_EXTERNAL_STORAGE])
class MainLayout(BoxLayout):
  areas = []
  aa = []
  bb = []
  cc = []
  del_buttons = []
  current = 0
  updating = False

  # def export(self, *args):
  #   date_append = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")
  #   image_name = f"LAC_{date_append}"
  #   self.ids.main_app.export_to_png(f"{image_name}.png")

  def add_area(self):
    values = []
    string_a1 = self.ids.a1.text
    string_a2 = self.ids.a2.text
    string_b1 = self.ids.b1.text
    string_b2 = self.ids.b2.text
    string_c1 = self.ids.c1.text
    string_c2 = self.ids.c2.text

    a1 = float(string_a1 or 0)
    a2 = float(string_a2 or 0)
    b1 = float(string_b1 or 0)
    b2 = float(string_b2 or 0)
    c1 = float(string_c1 or 0)
    c2 = float(string_c2 or 0)

    a = a1 + a2/12
    b = b1 + b2/12
    c = c1 + c2/12

    area = self.calculate_area(a, b, c)

    if area <= 0:
      self.show_popup()
    else:
      if self.updating:
        self.aa[self.current] = a
        self.bb[self.current] = b
        self.cc[self.current] = c
        self.areas[self.current] = area
        self.updating = False
        self.ids.add_button.text = "Add"
        self.ids.message.text = "Click on S. No. to edit the Area."
        self.ids.cancel.disabled = True

      else:
        self.aa.append(a)
        self.bb.append(b)
        self.cc.append(c)
        self.areas.append(area)

      self.update()

      self.ids.a1.text = ""
      self.ids.a2.text = ""
      self.ids.b1.text = ""
      self.ids.b2.text = ""
      self.ids.c1.text = ""
      self.ids.c2.text = ""

  def cancel(self):
    self.ids.a1.text = ""
    self.ids.a2.text = ""
    self.ids.b1.text = ""
    self.ids.b2.text = ""
    self.ids.c1.text = ""
    self.ids.c2.text = ""
    self.updating = False
    self.ids.add_button.text = "Add"
    self.ids.message.text = "Click on S. No. to edit the Area."
    self.ids.cancel.disabled = True
    for btn in self.del_buttons:
      btn.disabled = False

  def close_popup(self, popup_object):
    self.popup.dismiss()

  def show_popup(self):
    layout = BoxLayout(orientation="vertical", padding=dp(16), spacing=dp(10))
    lbl = Label(text="Calculated Area <= 0", color=(0.8, 0, 0), font_size=dp(30))
    btn = Button(text="Close", size_hint = (None, None), size=(dp(100), dp(50)))
    btn.bind(on_press=self.close_popup)
    layout.add_widget(lbl)
    layout.add_widget(btn)
    self.popup = Popup(title="Invalid Input", size_hint=(0.8, None), height=dp(180), content=layout)
    self.popup.open()

  def delete_item(self, instance):
    i = self.del_buttons.index(instance)
    del self.aa[i]
    del self.bb[i]
    del self.cc[i]
    del self.areas[i]
    instance.parent.parent.remove_widget(instance.parent)
    self.update()

  def update(self):
    self.del_buttons = []
    total = 0
    for area in self.areas:
      total += area

    ropani = int(total/5476)
    aana = int((total - 5476*ropani)/342.25)
    paisa = int((total - 5476*ropani - aana*342.25)/85.5625)
    dam = (total - 5476*ropani - aana*342.25 - paisa*85.5625)/21.390625
    self.ids.total_area.text = f"{total:.2f} sq.ft."
    self.ids.total_area_sqm.text = f"{total/(3.2808*3.2808):.2f} sq.m."
    self.ids.total_area_RAPD.text = f"{ropani}-{aana}-{paisa}-{dam:.2f} (RAPD)"

    self.ids.area_list.clear_widgets()
    for i, area in enumerate(self.areas):
      newLayout = BoxLayout(orientation="horizontal", size_hint=(1, None), height= dp(30))
      l0 = Button(text=f"{i+1}.", on_press=self.edit, color="#aabbee", background_color=(0, 1, 0, 0.3))

      l1 = Label(text=f"{int(self.aa[i])}' - {int(self.aa[i]*12%12)}\"")
      l2 = Label(text=f"{int(self.bb[i])}' - {int(self.bb[i]*12%12)}\"")
      l3 = Label(text=f"{int(self.cc[i])}' - {int(self.cc[i]*12%12)}\"")
      l4 = Label(text=f"{self.areas[i]:.2f}")
      b1 = Button(text="Delete", on_press=self.delete_item, color="#aabbee", background_color=(0, 1, 0, 0.3))
      self.del_buttons.append(b1)
      newLayout.add_widget(l0)
      newLayout.add_widget(l1)
      newLayout.add_widget(l2)
      newLayout.add_widget(l3)
      newLayout.add_widget(l4)
      newLayout.add_widget(b1)
      self.ids.area_list.add_widget(newLayout)

  def edit(self, btn):
    ind = int(btn.text[:-1])-1
    self.updating = True
    self.ids.a1.text = str(int(self.aa[ind]))
    self.ids.a2.text = str(int(self.aa[ind]*12%12))
    self.ids.b1.text = str(int(self.bb[ind]))
    self.ids.b2.text = str(int(self.bb[ind]*12%12))
    self.ids.c1.text = str(int(self.cc[ind]))
    self.ids.c2.text = str(int(self.cc[ind]*12%12))
    self.ids.add_button.text = "Update"
    self.current = ind
    self.ids.message.text = f"Updating Area Number: {ind+1}"
    self.ids.cancel.disabled = False
    for btn in self.del_buttons:
      btn.disabled = True

  def calculate_area(self, a, b, c):
    if a*b*c == 0:
      return 0
    if a+b <= c:
      return 0
    if c+b <= a:
      return 0
    if a+c <= b:
      return 0
    s = (a + b + c) / 2
    return math.sqrt(s * (s-a) * (s-b) * (s-c))

class FloatInput(TextInput):
    pat = re.compile('[^0-9]')
    def insert_text(self, substring, from_undo=False):
        pat = self.pat
        if '.' in self.text:
            s = re.sub(pat, '', substring)
        else:
            s = '.'.join(
                re.sub(pat, '', s)
                for s in substring.split('.', 1)
            )
        return super().insert_text(s, from_undo=from_undo)

class LandApp(App):
  pass

LandApp().run()
