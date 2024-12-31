import streamlit as st
import numpy as np
import math
import matplotlib.pyplot as plt

# Таблица данных для расчётов
data = {
    4: {"distances": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
        "angles": [1418, 1398, 1376, 1355, 1333, 1311, 1288, 1264, 1240, 1215, 1189, 1161, 1133, 1102, 1069, 1034, 995, 950, 896, 820],
        "times": [32.9, 32.9, 32.8, 32.7, 32.6, 32.4, 32.2, 32.1, 31.8, 31.6, 31.3, 31.0, 30.7, 30.3, 29.8, 29.3, 28.7, 27.9, 26.9, 25.3],
        "dispersion": 34, "velocity": 250},
    3: {"distances": [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
        "angles": [1423, 1397, 1370, 1343, 1315, 1286, 1257, 1226, 1193, 1159, 1123, 1084, 1040, 991, 932, 851],
        "times": [28.9, 28.9, 28.8, 28.6, 28.5, 28.3, 28.1, 27.9, 27.6, 27.2, 26.8, 26.4, 25.8, 25.1, 24.2, 22.8],
        "dispersion": 27, "velocity": 200},
    2: {"distances": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
        "angles": [1432, 1397, 1362, 1325, 1288, 1248, 1207, 1162, 1114, 1060, 997, 914, 755],
        "times": [24.8, 24.7, 24.6, 24.4, 24.2, 24.0, 23.7, 23.3, 22.9, 22.3, 21.5, 20.4, 17.8],
        "dispersion": 19, "velocity": 150},
    1: {"distances": [100, 200, 300, 400, 500, 600, 700, 800],
        "angles": [1446, 1392, 1335, 1275, 1212, 1141, 1058, 952],
        "times": [19.5, 19.4, 19.2, 18.9, 18.6, 18.1, 17.4, 16.4],
        "dispersion": 13, "velocity": 100},
}

# Функция расчёта азимута и дистанции
def calculate_distance_and_azimuth(x1, y1, x2, y2):
    dx = (x2 - x1) * 100  # Разница по горизонтали (метры)
    dy = (y2 - y1) * 100  # Разница по вертикали (метры)
    distance = math.sqrt(dx**2 + dy**2)
    azimuth = (math.degrees(math.atan2(dx, dy)) + 360) % 360
    return distance, azimuth

# Функция визуализации
def plot_trajectory_2d(mortar_coords, target_coords, dispersion_radius):
    plt.figure(figsize=(8, 8))
    plt.plot([mortar_coords[0], target_coords[0]], [mortar_coords[1], target_coords[1]], 'b-', label="Траектория")
    plt.scatter(*mortar_coords, c='green', label="Миномёт", zorder=5)
    plt.scatter(*target_coords, c='red', label="Цель", zorder=5)
    circle = plt.Circle(target_coords, dispersion_radius, color='orange', fill=False, linestyle='--', label="Разброс")
    plt.gca().add_artist(circle)
    plt.grid(True)
    plt.axis('equal')
    plt.xlabel("X (м)")
    plt.ylabel("Y (м)")
    plt.legend()
    st.pyplot(plt)

# Основной блок Streamlit
st.title("Баллистический калькулятор 1.1-alpha")

# Выбор режима
mode = st.radio("Выберите режим работы:", ["Ввод дистанции", "Ввод координат"])

# Режим ввода дистанции
if mode == "Ввод дистанции":
    distance = st.number_input("Введите дистанцию до цели (м):", min_value=100, max_value=2300, step=1)
    height_mortar = st.number_input("Высота миномёта (м):", min_value=-100, max_value=5000, step=1)
    height_target = st.number_input("Высота цели (м):", min_value=-100, max_value=5000, step=1)
    charges = st.radio("Выберите количество пороховых зарядов:", options=[4, 3, 2, 1])
    if st.button("Рассчитать"):
        charge_data = data[charges]
        if distance < min(charge_data["distances"]) or distance > max(charge_data["distances"]):
            st.error("Дистанция вне диапазона выбранного заряда!")
        else:
            angle, time = np.interp(distance, charge_data["distances"], charge_data["angles"]), np.interp(distance, charge_data["distances"], charge_data["times"])
            st.write(f"Вертикальный угол: {angle:.2f} тыс")
            st.write(f"Время полёта: {time:.2f} секунд")
            st.write(f"Средняя дисперсия: {charge_data['dispersion']} метров")

# Режим ввода координат
elif mode == "Ввод координат":
    col1, col2 = st.columns(2)
    with col1:
        mortar_x = st.number_input("Координата X миномёта:", min_value=0, max_value=136)
        mortar_y = st.number_input("Координата Y миномёта:", min_value=0, max_value=130)
        mortar_alt = st.number_input("Высота миномёта (м):", min_value=-100, max_value=5000, step=1)
    with col2:
        target_x = st.number_input("Координата X цели:", min_value=0, max_value=136)
        target_y = st.number_input("Координата Y цели:", min_value=0, max_value=130)
        target_alt = st.number_input("Высота цели (м):", min_value=-100, max_value=5000, step=1)
    charges = st.radio("Выберите количество пороховых зарядов:", options=[4, 3, 2, 1])
    if st.button("Рассчитать"):
        distance, azimuth = calculate_distance_and_azimuth(mortar_x, mortar_y, target_x, target_y)
        charge_data = data[charges]
        if distance < min(charge_data["distances"]) or distance > max(charge_data["distances"]):
            st.error("Дистанция вне диапазона выбранного заряда!")
        else:
            angle, time = np.interp(distance, charge_data["distances"], charge_data["angles"]), np.interp(distance, charge_data["distances"], charge_data["times"])
            corrected_angle = angle + math.degrees(math.atan2(target_alt - mortar_alt, distance))
            st.write(f"Дистанция до цели: {distance:.2f} метров")
            st.write(f"Азимут: {azimuth:.2f}°")
            st.write(f"Вертикальный угол: {corrected_angle:.2f} тыс")
            st.write(f"Время полёта: {time:.2f} секунд")
            st.write(f"Средняя дисперсия: {charge_data['dispersion']} метров")
            plot_trajectory_2d((mortar_x * 100, mortar_y * 100), (target_x * 100, target_y * 100), charge_data['dispersion'])
