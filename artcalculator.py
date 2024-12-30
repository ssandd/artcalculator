import streamlit as st
import pandas as pd
import numpy as np
import math

# CSS-стили для оформления логотипа и заголовка
st.markdown("""
    <style>
    .main {
        background-color: #333333;  /* Тёмно-серый фон */
        padding: 20px;
        border-radius: 10px;  /* Скругление краёв */
    }
    .title {
        font-family: Arial, sans-serif;
        font-size: 30px;
        color: #ffffff;  /* Белый цвет текста */
        margin-top: 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Оформление логотипа и заголовка
st.markdown("<div class='main'>", unsafe_allow_html=True)
col1, col2 = st.columns([1, 4])

with col1:
    st.image("logo.png", width=120)  # Отображение логотипа

with col2:
    st.markdown("<h1 class='title'>Баллистический калькулятор 1.0-alpha</h1>", unsafe_allow_html=True)

st.markdown("</div>", unsafe_allow_html=True)

# Основной функционал калькулятора
st.title("Калькулятор баллистики")

# Ввод данных пользователем
distance = st.number_input("Введите дистанцию до цели (м):", min_value=100, max_value=2300, step=1)
mortar_height = st.number_input("Высота миномёта над уровнем моря (м):", value=0)
target_height = st.number_input("Высота цели над уровнем моря (м):", value=0)
charge_option = st.radio("Выберите количество пороховых зарядов:", [1, 2, 3, 4])

# Логика для расчётов (пример)
def calculate_fire_parameters(distance, mortar_height, target_height, charge_option):
    # Здесь используйте вашу таблицу и логику
    delta_height = target_height - mortar_height
    correction_angle = math.degrees(math.atan(delta_height / distance))
    flight_time = 30 - 0.01 * distance  # Примерная формула для времени полёта
    return {
        "Вертикальный угол (градусы)": 45 + correction_angle,
        "Время полёта (с)": flight_time,
        "Используемый заряд": charge_option
    }

# Расчёт значений
if st.button("Рассчитать"):
    results = calculate_fire_parameters(distance, mortar_height, target_height, charge_option)
    st.subheader("Результаты расчётов:")
    st.write(f"Дистанция: {distance} м")
    st.write(f"Вертикальный угол: {results['Вертикальный угол (градусы)']:.2f}°")
    st.write(f"Время полёта: {results['Время полёта (с)']:.2f} секунд")
    st.write(f"Количество зарядов: {results['Используемый заряд']}")

