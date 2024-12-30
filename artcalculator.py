import streamlit as st
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

# CSS-стили для логотипа и заголовка
st.markdown("""
    <style>
    .main {
        background-color: #333333;  /* Тёмно-серый фон */
        padding: 20px;
        border-radius: 10px;
    }
    .title {
        font-family: Arial, sans-serif;
        font-size: 30px;
        color: #ffffff;
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Логотип и заголовок
st.markdown("<div class='main'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png", width=120)

with col2:
    st.markdown("<h1 class='title'>Баллистический калькулятор 1.0-alpha</h1>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Основной функционал
st.title("Калькулятор баллистики")

# Ввод данных
distance = st.number_input("Введите дистанцию до цели (м):", min_value=100, max_value=2300, step=1)
mortar_height = st.number_input("Высота миномёта над уровнем моря (м):", value=0)
target_height = st.number_input("Высота цели над уровнем моря (м):", value=0)
charge_option = st.radio("Выберите количество пороховых зарядов:", [1, 2, 3, 4])

# Таблица данных для расчётов
charge_data = {
    4: {"distances": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
        "angles": [1418, 1398, 1376, 1355, 1333, 1311, 1288, 1264, 1240, 1215, 1189, 1161, 1133, 1102, 1069, 1034, 995, 950, 896, 820],
        "times": [32.9, 32.9, 32.8, 32.7, 32.6, 32.4, 32.2, 32.1, 31.8, 31.6, 31.3, 31.0, 30.7, 30.3, 29.8, 29.3, 28.7, 27.9, 26.9, 25.3]},
    3: {"distances": [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
        "angles": [1423, 1397, 1370, 1343, 1315, 1286, 1257, 1226, 1193, 1159, 1123, 1084, 1040, 991, 932, 851],
        "times": [28.9, 28.9, 28.8, 28.6, 28.5, 28.3, 28.1, 27.9, 27.6, 27.2, 26.8, 26.4, 25.8, 25.1, 24.2, 22.8]},
    2: {"distances": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
        "angles": [1432, 1397, 1362, 1325, 1288, 1248, 1207, 1162, 1114, 1060, 997, 914, 755],
        "times": [24.8, 24.7, 24.6, 24.4, 24.2, 24.0, 23.7, 23.3, 22.9, 22.3, 21.5, 20.4, 17.8]},
    1: {"distances": [100, 200, 300, 400, 500, 600, 700, 800],
        "angles": [1446, 1392, 1335, 1275, 1212, 1141, 1058, 952],
        "times": [19.5, 19.4, 19.2, 18.9, 18.6, 18.1, 17.4, 16.4]},
}

# Логика расчётов
def interpolate_data(distance, charge_option):
    distances = charge_data[charge_option]["distances"]
    angles = charge_data[charge_option]["angles"]
    times = charge_data[charge_option]["times"]
    angle = np.interp(distance, distances, angles)
    time = np.interp(distance, distances, times)
    return angle, time

# Построение графика
def plot_trajectory(angle, charge_option):
    g = 9.81
    velocity = 200 + charge_option * 20
    theta = math.radians(angle / 1000)
    t_flight = 2 * velocity * math.sin(theta) / g
    t = np.linspace(0, t_flight, num=500)
    x = velocity * t * math.cos(theta)
    y = velocity * t * math.sin(theta) - 0.5 * g * t**2

    plt.figure(figsize=(8, 4))
    plt.plot(x, y, label=f"Траектория для {charge_option} зарядов")
    plt.axhline(0, color="black", linewidth=0.5, linestyle="--")
    plt.title("Траектория полёта снаряда")
    plt.xlabel("Дистанция (м)")
    plt.ylabel("Высота (м)")
    plt.legend()
    st.pyplot(plt)

# Расчёты и отображение
if st.button("Рассчитать"):
    angle, flight_time = interpolate_data(distance, charge_option)
    height_correction = math.degrees(math.atan((target_height - mortar_height) / distance))
    adjusted_angle = angle + height_correction
    st.subheader("Результаты расчётов:")
    st.write(f"Дистанция: {distance} м")
    st.write(f"Угол наводки: {adjusted_angle:.2f}° (с учётом поправки на высоту)")
    st.write(f"Время полёта: {flight_time:.2f} секунд")
    st.write(f"Количество зарядов: {charge_option}")
    plot_trajectory(adjusted_angle, charge_option)
