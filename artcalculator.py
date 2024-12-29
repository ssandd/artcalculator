import streamlit as st
import numpy as np

# Таблица данных
data = {
    4: {"distances": [400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800, 1900, 2000, 2100, 2200, 2300],
        "angles": [1418, 1398, 1376, 1355, 1333, 1311, 1288, 1264, 1240, 1215, 1189, 1161, 1133, 1102, 1069, 1034, 995, 950, 896, 820],
        "times": [32.9, 32.9, 32.8, 32.7, 32.6, 32.4, 32.2, 32.1, 31.8, 31.6, 31.3, 31.0, 30.7, 30.3, 29.8, 29.3, 28.7, 27.9, 26.9, 25.3],
        "dispersion": 34},
    3: {"distances": [300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400, 1500, 1600, 1700, 1800],
        "angles": [1423, 1397, 1370, 1343, 1315, 1286, 1257, 1226, 1193, 1159, 1123, 1084, 1040, 991, 932, 851],
        "times": [28.9, 28.9, 28.8, 28.6, 28.5, 28.3, 28.1, 27.9, 27.6, 27.2, 26.8, 26.4, 25.8, 25.1, 24.2, 22.8],
        "dispersion": 27},
    2: {"distances": [200, 300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200, 1300, 1400],
        "angles": [1432, 1397, 1362, 1325, 1288, 1248, 1207, 1162, 1114, 1060, 997, 914, 755],
        "times": [24.8, 24.7, 24.6, 24.4, 24.2, 24.0, 23.7, 23.3, 22.9, 22.3, 21.5, 20.4, 17.8],
        "dispersion": 19},
    1: {"distances": [100, 200, 300, 400, 500, 600, 700, 800],
        "angles": [1446, 1392, 1335, 1275, 1212, 1141, 1058, 952],
        "times": [19.5, 19.4, 19.2, 18.9, 18.6, 18.1, 17.4, 16.4],
        "dispersion": 13},
}

# Функция интерполяции
def interpolate(distance, charge_data):
    angle = np.interp(distance, charge_data["distances"], charge_data["angles"])
    time = np.interp(distance, charge_data["distances"], charge_data["times"])
    return angle, time

# Функция расчета
def calculate(distance, height_mortar, height_target, charges):
    delta_h = height_target - height_mortar
    charge_data = data[charges]

    # Проверка на диапазон дистанции
    if distance < min(charge_data["distances"]) or distance > max(charge_data["distances"]):
        return {"error": "Дистанция вне диапазона выбранного заряда!"}

    # Интерполяция для получения данных
    angle, time = interpolate(distance, charge_data)
    return {
        "Charges": charges,
        "Angle": angle,
        "Time": time,
        "Dispersion": charge_data["dispersion"],
        "Height Difference": delta_h
    }

# Streamlit интерфейс
st.title("Баллистический калькулятор 1.0-alpha")

# Ввод данных
distance = st.number_input("Введите дистанцию до цели (м):", min_value=100, max_value=2300, step=1)
height_mortar = st.number_input("Высота миномёта (м):", min_value=-100, max_value=5000, step=1)
height_target = st.number_input("Высота цели (м):", min_value=-100, max_value=5000, step=1)

# Выбор пороховых зарядов
charges = st.radio("Выберите количество пороховых зарядов:", options=[4, 3, 2, 1])

# Кнопка расчёта
if st.button("Рассчитать"):
    result = calculate(distance, height_mortar, height_target, charges)
    if "error" in result:
        st.error(result["error"])
    else:
        st.subheader("Результаты расчёта:")
        st.write(f"Пороховые заряды: {result['Charges']}")
        st.write(f"Угол вертикальной наводки: {result['Angle']:.2f} тыс")
        st.write(f"Время полёта снаряда: {result['Time']:.2f} сек")
        st.write(f"Средняя дисперсия: ~{result['Dispersion']} метров")
        st.write(f"Разница высот между миномётом и целью: {result['Height Difference']} м")
