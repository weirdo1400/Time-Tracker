from pywinauto import Application
import time

app = Application(backend='uia')
app.connect(title_re=".*Chrome.*")
element_name="Adress- und Suchleiste"
dlg = app.top_window()

while True:
    url = dlg.child_window(title=element_name, control_type="Edit").get_value()
    print(url)
    time.sleep(10)