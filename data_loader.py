import pandas as pd
import ast

def normalize_points(points):
    """
    Приводит загруженные из CSV/JSON точки к единому формату:
    ключи: 'id', 'name', 'координаты', 'вес', 'объем'
    """
    normalized = []
    for p in points:
        # 1. Получаем id и name
        id_ = int(
            p.get('id')
            or p.get('ID')
            or p.get('Id')
            or p.get('номер')
            or 0
        )
        name = (
            p.get('name')
            or p.get('Name')
            or p.get('название')
            or ''
        )
        # 2. Получаем координаты
        coords = [0.0, 0.0]
        # Вариант 1: одна строка "[lat, lon]"
        if 'координаты' in p and p['координаты']:
            try:
                coords = ast.literal_eval(p['координаты'])
            except Exception:
                pass
        # Вариант 2: две колонки lat/lon
        elif ('lat' in p and 'lon' in p) and (p['lat'] and p['lon']):
            try:
                coords = [float(p['lat']), float(p['lon'])]
            except Exception:
                pass
        # Вариант 3: русские широта/долгота
        elif ('широта' in p and 'долгота' in p) and (p['широта'] and p['долгота']):
            try:
                coords = [float(p['широта']), float(p['долгота'])]
            except Exception:
                pass

        # 3. Получаем вес и объем
        def str2float(val):
            try:
                return float(val)
            except Exception:
                return 0.0

        weight = str2float(
            p.get('вес')
            or p.get('weight')
            or p.get('Вес')
            or 0
        )
        volume = str2float(
            p.get('объем')
            or p.get('volume')
            or p.get('Объем')
            or 0
        )
        normalized.append({
            'id': id_,
            'name': name,
            'координаты': coords,
            'вес': weight,
            'объем': volume
        })
    return normalized

def load_data():
    choice = input("Загрузить из файла (1) или ввести вручную (2)? Введите 1 или 2: ")
    if choice == '1':
        file_path = input("Введите путь к файлу (.csv или .json) или 'q' для выхода: ")
        if file_path.lower() == 'q':
            return None
        try:
            if file_path.endswith('.csv'):
                data = pd.read_csv(file_path, encoding="utf-8")
            elif file_path.endswith('.json'):
                data = pd.read_json(file_path, encoding="utf-8")
            else:
                print("Неподдерживаемый формат файла.")
                return None
            points = data.to_dict(orient='records')
            # Нормализация!
            points = normalize_points(points)
            return points
        except Exception as e:
            print(f"Ошибка при чтении файла: {e}")
            return None
    elif choice == '2':
        points = []
        try:
            num_points = int(input("Введите количество пунктов (или 0 для отмены): "))
        except Exception:
            print("Ошибка: введите число.")
            return None

        if num_points == 0:
            print("Ввод отменен.")
            return None
        for i in range(num_points):
            print(f"\nПункт {i+1}:")
            print("Введите 'q' или 'stop' для завершения ввода.")
            point_id_input = input("ID пункта: ")
            if point_id_input.lower() in ['q', 'stop']:
                print("Ввод остановлен пользователем.")
                break
            try:
                point_id = int(point_id_input)
            except:
                print("Некорректный ID.")
                continue

            name = input("Название: ")
            lat_input = input("Широта: ")
            if lat_input.lower() in ['q', 'stop']:
                print("Ввод остановлен.")
                break
            try:
                lat = float(lat_input)
            except:
                print("Некорректная широта.")
                continue

            lon_input = input("Долгота: ")
            if lon_input.lower() in ['q', 'stop']:
                print("Ввод остановлен.")
                break
            try:
                lon = float(lon_input)
            except:
                print("Некорректная долгота.")
                continue

            weight_input = input("Вес (кг): ")
            if weight_input.lower() in ['q', 'stop']:
                print("Ввод остановлен.")
                break
            try:
                weight = float(weight_input)
            except:
                print("Некорректный вес.")
                continue

            volume_input = input("Объем: ")
            if volume_input.lower() in ['q', 'stop']:
                print("Ввод остановлен.")
                break
            try:
                volume = float(volume_input)
            except:
                print("Некорректный объем.")
                continue

            points.append({
                'id': point_id,
                'name': name,
                'координаты': [lat, lon],
                'вес': weight,
                'объем': volume
            })
        return points
    else:
        print("Некорректный ввод.")
        return None