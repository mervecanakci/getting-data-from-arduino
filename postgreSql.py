import psycopg2

# Veritabanı bağlantısı oluştur
conn = psycopg2.connect(database="sensor_verileri", user="postgres", password="12345", host="localhost", port="5432")

# Verileri kaydetme
def save_data(data):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO veri (data) VALUES (%s)", (data,))
    conn.commit()
    cursor.close()

# Arduino'dan veri al ve kaydet
arduino_data = "veri_arduino"  # Arduino'dan alınan veri
save_data(arduino_data)

# Veritabanı bağlantısını kapat
conn.close()
# veri tabanı bağlantısı gerek duyulduğunda kullanılabilir
# projede kullanmadık