import math
import numpy as np
import streamlit as st

# Таблица данных
data = {
    4: {"dispersion": 34, "distances": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
        "angles": [1418, 1398, 1376, 1355, 1333, 1311, 1288, 1264, 1240, 1215, 1189, 1161, 1133, 1102, 1069, 1034, 995, 950, 896, 820],
        "times": [32.9, 32.9, 32.8, 32.7, 32.6, 32.4, 32.2, 32.1, 31.8, 31.6, 31.3, 31.0, 30.7, 30.3, 29.8, 29.3, 28.7, 27.9, 26.9, 25.3]},
    3: {"dispersion": 27, "distances": [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
        "angles": [1423, 1397, 1370, 1343, 1315, 1286, 1257, 1226, 1193, 1159, 1123, 1084, 1040, 991, 932, 851],
        "times": [28.9, 28.9, 28.8, 28.6, 28.5, 28.3, 28.1, 27.9, 27.6, 27.2, 26.8, 26.4, 25.8, 25.1, 24.2, 22.8]},
    2: {"dispersion": 19, "distances": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
        "angles": [1432, 1397, 1362, 1325, 1288, 1248, 1207, 1162, 1114, 1060, 997, 914, 755],
        "times": [24.8, 24.7, 24.6, 24.4, 24.2, 24.0, 23.7, 23.3, 22.9, 22.3, 21.5, 20.4, 17.8]},
    1: {"dispersion": 13, "distances": [100, 200, 300, 400, 500, 600, 700, 800],
        "angles": [1446, 1392, 1335, 1275, 1212, 1141, 1058, 952],
        "times": [19.5, 19.4, 19.2, 18.9, 18.6, 18.1, 17.4, 16.4]}
}

# Функция для интерполяции
def interpolate(distance, charge_data):
    angles = np.interp(distance, charge_data["distances"], charge_data["angles"])
    times = np.interp(distance, charge_data["distances"], charge_data["times"])
    return angles, times

# Выбор подходящего заряда
def choose_charge(distance):
    for charge, charge_data in data.items():
        if min(charge_data["distances"]) <= distance <= max(charge_data["distances"]):
            return charge, charge_data
    return None, None

# Интерфейс Streamlit
st.title("Баллистический калькулятор для миномёта alpha 1.0")
st.write("Введите параметры для расчёта")

# Ввод данных
distance = st.number_input("Дистанция до цели (м):", min_value=0.0, step=1.0)
height_mortar = st.number_input("Высота миномёта над уровнем моря (м):", min_value=0.0)
height_target = st.number_input("Высота цели над уровнем моря (м):", min_value=0.0)

if st.button("Рассчитать"):
    charge, charge_data = choose_charge(distance)

    if charge is None:
        st.error("Для данной дистанции нет данных в таблице!")
    else:
        angle, flight_time = interpolate(distance, charge_data)
        delta_h = height_target - height_mortar
        correction_angle = math.degrees(math.atan(delta_h / distance)) if distance > 0 else 0
        adjusted_angle = angle + correction_angle

        st.subheader("Результаты расчёта:")
        st.write(f"Рекомендуемый заряд: {charge}")
        st.write(f"Средняя дисперсия: {charge_data['dispersion']} м")
        st.write(f"Вертикальный угол (с учётом высоты): {adjusted_angle:.2f} тысячных")
        st.write(f"Время полёта: {flight_time:.2f} секунд")
        st.write(f"Разница высот: {delta_h:.2f} м")
