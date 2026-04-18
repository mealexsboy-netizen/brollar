import tkinter as tk
from PIL import Image, ImageTk
import requests
import io

# Настройки твоего экрана
WIDTH = 16
HEIGHT = 53
SCALE = 10  # Увеличим в 10 раз для монитора

def get_usd_rate():
    try:
        url = "https://api.exchangerate-api.com/v4/latest/USD"
        data = requests.get(url).json()
        rate = str(int(data['rates']['KZT']))
        return rate[:3] # Берем только первые 3 цифры
    except:
        return "495" # Заглушка если нет интернета

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Dipsik Simulator")
        self.root.geometry(f"{WIDTH * SCALE}x{HEIGHT * SCALE}")
        self.root.configure(bg='black')

        self.canvas = tk.Canvas(root, width=WIDTH*SCALE, height=HEIGHT*SCALE, bg='black', highlightthickness=0)
        self.canvas.pack()

        self.update_display()

    def update_display(self):
        rate = get_usd_rate()
        print(f"Пытаюсь найти картинки для курса: {rate}")
        
        self.canvas.delete("all")
        single_h = (HEIGHT // 3) * SCALE
        self.images = [] 
        
        for i, digit in enumerate(rate):
            full_path = f"{digit}.png"
            import os
            if os.path.exists(full_path):
                try:
                    img = Image.open(full_path)
                    img = img.resize((WIDTH * SCALE, single_h), Image.NEAREST)
                    photo = ImageTk.PhotoImage(img)
                    self.images.append(photo)
                    self.canvas.create_image(0, i * single_h, anchor=tk.NW, image=photo)
                    print(f"Ок: файл {full_path} загружен.")
                except Exception as e:
                    print(f"Ошибка при чтении {full_path}: {e}")
            else:
                print(f"ОШИБКА: Файл {full_path} НЕ НАЙДЕН в папке {os.getcwd()}")
                self.canvas.create_text(WIDTH*SCALE//2, i*single_h + single_h//2, 
                                        text=digit, fill="red", font=("Arial", 30))

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()