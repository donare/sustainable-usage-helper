# Build Application

```powershell
pyinstaller --additional-hooks-dir=pyinstaller-hooks --onefile --add-data "icon.png;." --icon "icon.ico" --noconsole --name="SUH" main.py
```

# Attribution

[Hookfile for pystray](https://github.com/moses-palmer/pystray/issues/55#issuecomment-652294752)
