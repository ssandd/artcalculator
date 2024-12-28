import math
import pandas as pd
import numpy as np
import streamlit as st

# Данные таблицы стрельбы
data = {
    "Distance (m)": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300,
                     1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
    "Angle (°)": [80, 78, 76, 74, 72, 70, 68, 66, 64, 62,
                  60, 58, 56, 54, 52, 50, 48, 46, 44, 42],
    "Flight Time (s)": [32.9, 32.9, 32.8, 32.7, 32.6, 32.4, 32.2, 32.1, 31.8, 31.6,
                        31.3, 30.7, 30.3, 29.8, 29.3, 28.7, 27.9, 26.9, 25.3, 25.3],
    "Charges": [4, 4, 4, 4, 3, 3, 3, 3, 3, 3,
                3, 2, 2, 2, 2, 2, 2, 1, 1, 1]
}

df = pd.DataFrame(data)

# Функция для интерполяции
def interpolate_values(distance, df, column):
    return np.interp(distance, df["Distance (m)"], df[column])

# Интерфейс Streamlit
st.title("Баллистический калькулятор для миномёта")
st.write("Введите данные для расчёта")

# Ввод данных
distance = st.number_input("Дистанция до цели (м):", min_value=0.0, step=1.0)
height_mortar = st.number_input("Высота миномёта над уровнем моря (м):", min_value=0.0)
height_target = st.number_input("Высота цели над уровнем моря (м):", min_value=0.0)
desired_dispersion = st.slider("Желаемый разброс (м):", 0, 50, 10)

# Кнопка расчёта
if st.button("Рассчитать"):
    # Разница высот
    delta_h = height_target - height_mortar
    correction_angle = math.degrees(math.atan(delta_h / distance)) if distance > 0 else 0

    # Интерполяция значений таблицы
    angle = interpolate_values(distance, df, "Angle (°)")
    flight_time = interpolate_values(distance, df, "Flight Time (s)")
    charges = interpolate_values(desired_dispersion, df, "Charges")

    # Учет поправки по высоте
    adjusted_angle = angle + correction_angle

    # Результаты
    st.subheader("Результаты расчёта:")
    st.write(f"Дистанция: {distance:.2f} м")
    st.write(f"Разница высот: {delta_h:.2f} м")
    st.write(f"Поправка по углу: {correction_angle:.2f}°")
    st.write(f"Вертикальный угол: {adjusted_angle:.2f}°")
    st.write(f"Время полёта снаряда: {flight_time:.2f} с")
    st.write(f"Количество пороховых зарядов: {int(charges)}")