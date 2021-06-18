import threading
import multiprocessing as mp


from app import systray


if __name__ == '__main__':
    mp.freeze_support()

    threading.Thread(target=systray.start_tray, daemon=False).start()
