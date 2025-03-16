import pandas as pd

# อ่านข้อมูลจากไฟล์ CSV
def load_pm25_data():
    return pd.read_csv("D:/dash/pm_2.5_Term_Project/pm_2.5/predicted_pm25.csv")

def load_humidity_data():
    return pd.read_csv("D:/dash/pm_2.5_Term_Project/pm_2.5/predicted_humidity.csv")

def load_temperature_data():
    return pd.read_csv("D:/dash/pm_2.5_Term_Project/pm_2.5/predicted_temperature.csv")

# อ่านข้อมูล
pm25_df = load_pm25_data()
humidity_df = load_humidity_data()
temperature_df = load_temperature_data()

# ข้อมูลสำหรับสถานีเทศบาลนครหาดใหญ่ แยกโรงแรมวีแอล
pm25_data = {
    "location": "สถานีเทศบาลนครหาดใหญ่ แยกโรงแรมวีแอล",
    "pm25": 3.7,
    "unit": "มก./ลบ.ม.",
    "latitude": 7.0084,  # ละติจูดของหาดใหญ่
    "longitude": 100.4767  # ลองจิจูดของหาดใหญ่
}

# ข้อมูลสำหรับการคำนวณค่าเฉลี่ย
data = {
    'PM 2.5': {
        'df': pm25_df,  # DataFrame สำหรับ PM 2.5
        'col': 'prediction_label'  # คอลัมน์ที่ต้องการคำนวณค่าเฉลี่ย
    },
    'Humidity': {
        'df': humidity_df,  # DataFrame สำหรับความชื้น
        'col': 'prediction_label'  # คอลัมน์ที่ต้องการคำนวณค่าเฉลี่ย
    },
    'Temperature': {
        'df': temperature_df,  # DataFrame สำหรับอุณหภูมิ
        'col': 'prediction_label'  # คอลัมน์ที่ต้องการคำนวณค่าเฉลี่ย
    }
}

# คำนวณค่าเฉลี่ย
avg_pm25 = data['PM 2.5']['df'][data['PM 2.5']['col']].mean()
avg_humidity = data['Humidity']['df'][data['Humidity']['col']].mean()
avg_temperature = data['Temperature']['df'][data['Temperature']['col']].mean()

print(avg_pm25, avg_humidity, avg_temperature)
