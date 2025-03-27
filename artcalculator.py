import streamlit as st
import numpy as np

def interpolate_value(x, x1, y1, x2, y2):
    return y1 + (y2 - y1) * ((x - x1) / (x2 - x1))

def calculate_aiming_angle(distance, height_mortar, height_target, table):
    distances = table['distance']
    angles = table['angle']
    height_corrections = table['height_correction']
    
    idx = np.searchsorted(distances, distance, side='right')
    if idx == 0 or idx >= len(distances):
        return None
    
    d1, d2 = distances[idx-1], distances[idx]
    a1, a2 = angles[idx-1], angles[idx]
    h1, h2 = height_corrections[idx-1], height_corrections[idx]
    
    base_angle = interpolate_value(distance, d1, a1, d2, a2)
    avg_height_correction = (h1 + h2) / 2
    delta_height = height_target - height_mortar
    height_adjustment = avg_height_correction * (delta_height / 100)
    
    return round(base_angle - height_adjustment)

def main():
    st.set_page_config(page_title="Минометный калькулятор", layout="centered")
    st.title("Минометный калькулятор")
    
    charge_options = {
        "0 зарядов": 0, "1 заряд": 1, "2 заряда": 2, "3 заряда": 3, "4 заряда": 4
    }
    charge = st.selectbox("Выберите количество пороховых зарядов:", list(charge_options.keys()))
    
    distance = st.number_input("Введите дистанцию до цели (м):", min_value=50, max_value=2300, step=1)
    height_mortar = st.number_input("Введите высоту миномета (м):", min_value=0, max_value=500, step=1)
    height_target = st.number_input("Введите высоту цели (м):", min_value=0, max_value=500, step=1)
    
    if st.button("Рассчитать угол наведения"):
        table = load_table(charge_options[charge])
        angle = calculate_aiming_angle(distance, height_mortar, height_target, table)
        
        if angle:
            st.success(f"Установите прицел на {angle} тысячных.")
        else:
            st.error("Дистанция вне диапазона таблицы!")

def load_table(charge):
    tables = {
        0: {'distance': [50, 100, 150, 200, 250, 300, 350, 400, 450, 500],
            'angle': [1455, 1411, 1365, 1318, 1268, 1217, 1159, 1095, 1023, 922],
            'height_correction': [44, 46, 47, 50, 51, 58, 64, 72, 101, 0]},
        1: {'distance': [100, 200, 300, 400, 500, 600, 700, 800],
            'angle': [1446, 1392, 1335, 1275, 1212, 1141, 1058, 952],
            'height_correction': [27, 28, 29, 31, 35, 40, 48, 81]},
        2: {'distance': [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
            'angle': [1432, 1397, 1362, 1325, 1288, 1248, 1207, 1162, 1114, 1060, 997, 914, 755],
            'height_correction': [17, 18, 18, 18, 20, 20, 22, 23, 26, 29, 37, 55, 0]},
        3: {'distance': [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
            'angle': [1423, 1397, 1370, 1343, 1315, 1286, 1257, 1226, 1193, 1159, 1123, 1084, 1040, 991, 932, 851],
            'height_correction': [13, 14, 13, 14, 14, 14, 16, 16, 16, 18, 19, 22, 24, 28, 36, 68]},
        4: {'distance': [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
            'angle': [1418, 1398, 1376, 1355, 1333, 1311, 1288, 1264, 1240, 1215, 1189, 1161, 1133, 1102, 1069, 1034, 995, 950, 896, 820],
            'height_correction': [10, 11, 10, 11, 11, 12, 12, 12, 13, 13, 14, 14, 15, 16, 17, 19, 22, 26, 34, 65]}
    }
    return tables.get(charge, tables[0])

if __name__ == "__main__":
    main()
