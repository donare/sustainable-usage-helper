import win32gui
import win32api
import win32ui
import win32con
import win32process
import base64
import os
from PIL import Image
import tempfile

ICON_SIZE = win32api.GetSystemMetrics(win32con.SM_CXICON)


def window_enumeration_handler(hwnd, window_list):
    window_list.append((hwnd, win32gui.GetWindowText(hwnd)))


def get_windows():
    window_list = []

    win32gui.EnumWindows(window_enumeration_handler, window_list)

    return window_list


def get_application_path(pid):
    handle = win32api.OpenProcess(win32con.PROCESS_QUERY_INFORMATION | win32con.PROCESS_VM_READ, False, pid)
    return win32process.GetModuleFileNameEx(handle, 0)


def get_icon(application_path):
    try:
        h_icon = win32gui.ExtractIcon(0, application_path, 0)

        h_dc = win32ui.CreateDCFromHandle(win32gui.GetDC(0))

        h_bmp = win32ui.CreateBitmap()
        h_bmp.CreateCompatibleBitmap(h_dc, ICON_SIZE, ICON_SIZE)

        h_dc = h_dc.CreateCompatibleDC()
        h_dc.SelectObject(h_bmp)

        h_dc.DrawIcon((0, 0), h_icon)
        bitmap_raw = h_bmp.GetBitmapBits(True)

        r,g,b,a = Image.frombytes("RGBA", (ICON_SIZE, ICON_SIZE), bitmap_raw).split()
        img = Image.merge("RGBA", (b,g,r,a))

        with tempfile.TemporaryFile() as tf:
            img.save(tf, format="png")
            tf.seek(0)
            icon = base64.b64encode(tf.read())
    except:
        icon = ""

    return icon


def generate_image(bitmap):
    bm = tuple([x + 128 for x in bitmap])

    img = Image.new("RGBA", (32,32))

    for i in range(1024):
        x = i%32
        y = i//32

        img.putpixel((x,y), tuple([bm[x+1024]]*3+[255]))

    return img


def get_process_list():
    running_processes = win32process.EnumProcesses()

    rows = []

    for pid in running_processes[1:]:
        try:
            application_path = get_application_path(pid)
        except:
            print(f"Couldn't open Process {pid}.")
            continue

        rows.append({
            "pid": pid,
            "application": os.path.basename(application_path),
            "icon": get_icon(application_path)
        })

    return rows


def get_foreground_process():
    hwnd = win32gui.GetForegroundWindow()
    tid, pid = win32process.GetWindowThreadProcessId(hwnd)

    return pid