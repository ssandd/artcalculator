import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt, atan2, degrees, radians, cos, sin

# Интерполяция углов по таблице данных
def interpolate_angle(distance, charges_data, charges):
    data = charges_data[charges - 1]
    distances = data["distance"]
    angles = data["angle"]
    return np.interp(distance, distances, angles)

# Функция для расчёта расстояния между координатами
def calculate_distance(coord1, coord2):
    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]
    return sqrt(dx**2 + dy**2)

# Функция для расчёта азимута
def calculate_azimuth(coord1, coord2):
    dx = coord2[0] - coord1[0]
    dy = coord2[1] - coord1[1]
    return (degrees(atan2(dy, dx)) + 360) % 360

# Коррекция угла стрельбы по высоте
def adjust_angle_for_altitude(vertical_angle, distance, alt_mortar, alt_target):
    altitude_difference = alt_target - alt_mortar
    correction = degrees(atan2(altitude_difference, distance))
    return vertical_angle + correction

# Преобразование координат из формата 054885 в 100-метровую сетку
def parse_coordinates(coord):
    main_square_x = int(coord[:3])
    main_square_y = int(coord[3:6])
    return np.array([main_square_x, main_square_y])

# Данные для углов и дистанций
charges_data = [
    {"distance": [100, 200, 300, 400, 500], "angle": [45, 40, 35, 30, 25]},  # Заряд 1
    {"distance": [200, 400, 600, 800, 1000], "angle": [50, 45, 40, 35, 30]},  # Заряд 2
    {"distance": [300, 600, 900, 1200, 1500], "angle": [55, 50, 45, 40, 35]},  # Заряд 3
    {"distance": [400, 800, 1200, 1600, 2000], "angle": [60, 55, 50, 45, 40]},  # Заряд 4
]

# Интерфейс приложения
st.title("Калькулятор миномётной стрельбы")

# Режим ввода
mode = st.radio("Выберите режим ввода", ["Ручной ввод дистанции", "Ввод координат"])

if mode == "Ручной ввод дистанции":
    st.header("Ручной ввод дистанции")
    distance = st.number_input("Введите дистанцию до цели (м)", min_value=100, max_value=2000, step=1)
    alt_mortar = st.number_input("Введите высоту миномёта (м)", step=1)
    alt_target = st.number_input("Введите высоту цели (м)", step=1)
    charges = st.selectbox("Выберите количество зарядов", [1, 2, 3, 4])

    if st.button("Рассчитать"):
        vertical_angle = interpolate_angle(distance, charges_data, charges)
        adjusted_angle = adjust_angle_for_altitude(vertical_angle, distance, alt_mortar, alt_target)
        st.success(f"Вертикальный угол: {adjusted_angle:.2f}°")
        st.info(f"Дистанция: {distance} м")
else:
    st.header("Ввод координат")
    mortar_coords = st.text_input("Введите координаты миномёта (например, 054885 060881)")
    target_coords = st.text_input("Введите координаты цели (например, 058225 063441)")
    alt_mortar = st.number_input("Введите высоту миномёта (м)", step=1)
    alt_target = st.number_input("Введите высоту цели (м)", step=1)
    charges = st.selectbox("Выберите количество зарядов", [1, 2, 3, 4])

    if st.button("Рассчитать"):
        try:
            mortar_coords = parse_coordinates(mortar_coords)
            target_coords = parse_coordinates(target_coords)
            distance = calculate_distance(mortar_coords, target_coords) * 100  # Конвертация в метры
            azimuth = calculate_azimuth(mortar_coords, target_coords)
            vertical_angle = interpolate_angle(distance, charges_data, charges)
            adjusted_angle = adjust_angle_for_altitude(vertical_angle, distance, alt_mortar, alt_target)

            st.success(f"Вертикальный угол: {adjusted_angle:.2f}°")
            st.info(f"Дистанция: {distance:.2f} м")
            st.info(f"Азимут: {azimuth:.2f}°")

            # Визуализация 2D-плана
            fig, ax = plt.subplots()
            ax.scatter(mortar_coords[0], mortar_coords[1], c="blue", label="Миномёт")
            ax.scatter(target_coords[0], target_coords[1], c="red", label="Цель")
            ax.plot(
                [mortar_coords[0], target_coords[0]],
                [mortar_coords[1], target_coords[1]],
                color="green",
                linestyle="--",
                label="Линия огня"
            )
            ax.set_title("2D План огня")
            ax.set_xlabel("Горизонтальная координата")
            ax.set_ylabel("Вертикальная координата")
            ax.legend()
            ax.grid(True)
            st.pyplot(fig)
        except Exception as e:
            st.error(f"Ошибка обработки координат: {e}")
