import tkinter as tk
from tkinter import messagebox
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import os

def fetch_dollar_rate():
    url = "https://bigpara.hurriyet.com.tr/doviz/dolar/"
    try:
        response = requests.get(url)
        response.raise_for_status()  # Hata durumunda exception fırlat
    except requests.RequestException as e:
        return "Sayfa erişilemedi.", str(e)

    soup = BeautifulSoup(response.content, "html.parser")

    # Dolar fiyatını içeren öğeyi bulma
    price_tag = soup.find("span", class_="value")
    if price_tag:
        price = price_tag.text.strip().replace(",", ".")
        try:
            return float(price), None
        except ValueError:
            return "Fiyat formatı hatalı.", None
    return "Dolar fiyatı bulunamadı.", None

def save_to_file():
    dollar_rate, error = fetch_dollar_rate()
    if error:
        messagebox.showerror("Hata", f"Dolar fiyatı alınırken bir sorun oluştu: {error}")
        return

    # Geçerli tarih
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Dosyaya kaydetme
    file_name = "dolar_fiyatlari.txt"
    with open(file_name, "a") as file:
        file.write(f"{timestamp} - Dolar: {dollar_rate} TL\n")

    messagebox.showinfo("Başarı", f"Dolar fiyatı ve tarih kaydedildi:\n{timestamp} - {dollar_rate} TL")
    print(f"Dolar fiyatı {os.path.abspath(file_name)} dosyasına kaydedildi.")

def show_dollar_rate():
    dollar_rate, error = fetch_dollar_rate()
    if error:
        messagebox.showerror("Hata", f"Dolar fiyatı alınırken bir sorun oluştu: {error}")
        return

    # Fiyatı gösteren yeni pencere açma
    rate_window = tk.Toplevel(root)
    rate_window.title("Dolar Fiyatı")
    
    rate_label = tk.Label(rate_window, text=f"Anlık Dolar Kuru: {dollar_rate} TL", font=("Arial", 14))
    rate_label.pack(padx=10, pady=10)

    rate_window.geometry("300x100")

def setup_main_window():
    global root
    root = tk.Tk()
    root.title("Dolar Fiyatı Uygulaması")
    
    # Dolar fiyatını göster butonu
    show_button = tk.Button(root, text="Doları Görüntüle", font=("Arial", 14), command=show_dollar_rate)
    show_button.pack(pady=20)
    
    # Dolar fiyatını kaydet butonu
    save_button = tk.Button(root, text="Dolar Fiyatını Kaydet", font=("Arial", 14), command=save_to_file)
    save_button.pack(pady=20)

    root.geometry("350x250")
    root.mainloop()

if __name__ == "__main__":
    setup_main_window()