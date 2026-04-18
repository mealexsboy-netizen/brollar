import tkinter as tk
from PIL import Image, ImageTk, ImageSequence
import requests
import time

# Настройки
WIDTH, HEIGHT, SCALE = 16, 53, 15
FX_DURATION = 5 # Сколько секунд крутить гифку каждую минуту

def get_rate():
    try:
        r = requests.get("https://api.exchangerate-api.com/v4/latest/USD").json()
        return str(int(r['rates']['KZT']))[:3]
    except: return "495"

class DipsikGif:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=WIDTH*SCALE, height=HEIGHT*SCALE, bg='black', highlightthickness=0)
        self.canvas.pack()
        
        self.current_rate = get_rate()
        self.last_update = time.time()
        
        # --- МАГИЯ ГИФКИ ---
        self.frames = []
        try:
            gif = Image.open("перебивка.gif")
            # Разрезаем гифку на кадры программно
            for frame in ImageSequence.Iterator(gif):
                # Подгоняем каждый кадр под размер экрана
                frame_resized = frame.convert("RGBA").resize((WIDTH*SCALE, HEIGHT*SCALE), Image.NEAREST)
                self.frames.append(ImageTk.PhotoImage(frame_resized))
            print(f"Загружено кадров гифки: {len(self.frames)}")
        except Exception as e:
            print(f"Гифка fx.gif не найдена: {e}")

        self.fx_idx = 0
        self.tick()

    def tick(self):
        now = int(time.time())
        self.canvas.delete("all")

        # Если первые FX_DURATION секунд минуты — крутим гифку
        if now % 60 < FX_DURATION and self.frames:
            self.canvas.create_image(0, 0, anchor=tk.NW, image=self.frames[self.fx_idx])
            self.fx_idx = (self.fx_idx + 1) % len(self.frames)
            delay = 100 # Скорость гифки (100 мс)
        else:
            # Показываем курс
            if time.time() - self.last_update > 3600: # Раз в час обновляем
                self.current_rate = get_rate()
                self.last_update = time.time()
                
            h = (HEIGHT // 3) * SCALE
            self.digits = [] # Храним ссылки
            for i, digit in enumerate(self.current_rate):
                try:
                    img = Image.open(f"{digit}.png").resize((WIDTH*SCALE, h), Image.NEAREST)
                    ph = ImageTk.PhotoImage(img)
                    self.digits.append(ph)
                    self.canvas.create_image(0, i*h, anchor=tk.NW, image=ph)
                except: pass
            delay = 1000 # Курс можно обновлять реже

        self.root.after(delay, self.tick)

root = tk.Tk()
root.title("Dipsik GIF Mode")
app = DipsikGif(root)
root.mainloop()