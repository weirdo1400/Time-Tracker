from pywinauto import Application
app = Application(backend='uia')
app.connect(title_re=".*Chrome.*")
element_name="Adress- und Suchleiste"
dlg = app.top_window()
url = dlg.child_window(title=element_name, control_type="Edit").get_value()
print(url)