import graph_model
import data_loader
import visualization
import route_optimization

def print_points(points):
    print('___________________________________________________________________________________')
    print()
    print("Список загруженных пунктов:")
    print()
    print("-" * 70)
    print(f"{'ID':<5} {'Название':<25} {'Широта':<10} {'Долгота':<10} {'Вес':<8} {'Объем':<8}")
    print("-" * 70)
    for p in points:
        lat, lon = p['координаты']
        print(f"{p['id']:<5} {p['name']:<25} {lat:<10.5f} {lon:<10.5f} {p['вес']:<8} {p['объем']:<8}")
    print("-" * 70)

def save_route_to_file(path, distance, filename="route_result.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as f:
            print('___________________________________________________________________________________')
            print()
            f.write("Маршрут:\n")
            f.write(" -> ".join(str(p) for p in path) + "\n")
            f.write(f"Общее расстояние: {distance:.2f} км\n")
        print(f"Результат успешно сохранён в файл {filename}")
    except Exception as e:
        print(f"Ошибка при сохранении файла: {e}")

def main_menu():
    print('___________________________________________________________________________________')
    print()
    print("=== Добро пожаловать в систему оптимизации маршрутов! ===")
    print('___________________________________________________________________________________')

    points = None
    G = None

    while True:
        print("\n--- Главное меню ---")
        print()
        print("1. Загрузить или ввести данные")
        print("2. Кратчайший путь между двумя точками")
        print("3. Оптимальный маршрут через все точки (TSP)")
        print("4. Выйти")
        choice = input("Выберите действие (1-4): ").strip()

        if choice == '1':
            print('___________________________________________________________________________________')
            print()
            print("\nЗагрузка данных...")
            points = data_loader.load_data()
            if points is None:
                print("Ошибка загрузки данных или ввод отменён.")
                G = None
            else:
                print("Построение графа...")
                G = graph_model.build_graph_from_points(points)
                print("Данные успешно загружены и граф построен!")
                print_points(points)

        elif choice == '2':
            print('___________________________________________________________________________________')
            print()
            if G is None:
                print("Сначала загрузите данные (пункт 1 в меню)!")
                continue
            print('___________________________________________________________________________________')
            print()
            print("\nПоиск кратчайшего пути между двумя точками")
            try:
                start_id = int(input("Введите ID начальной точки: "))
                end_id = int(input("Введите ID конечной точки: "))
            except ValueError:
                print("Ошибка: введите корректные ID.")
                continue
            print('___________________________________________________________________________________')
            print()
            print("Выберите алгоритм поиска маршрута:")
            print("1. Дейкстра")
            print("2. Беллмана-Форда")
            algo_choice = input("Введите номер: ").strip()
            print('___________________________________________________________________________________')
            print()
            print("Поиск маршрута...")
            if algo_choice == '1':
                path, distance = route_optimization.find_shortest_path_dijkstra(G, start_id, end_id)
            elif algo_choice == '2':
                path, distance = route_optimization.find_shortest_path_bellman_ford(G, start_id, end_id)
            else:
                print("Некорректный выбор алгоритма.")
                continue
            print('___________________________________________________________________________________')
            print()
            if path:
                print(f"Маршрут найден: {path}")
                print(f"Общее расстояние: {distance:.2f} км")
                visualization.plot_graph(G)
                visualization.plot_route(G, path)
                print('___________________________________________________________________________________')
                print()
                save = input("Сохранить маршрут в файл? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Имя файла (по умолчанию route_result.txt): ").strip()
                    if filename == '':
                        filename = "route_result.txt"
                    save_route_to_file(path, distance, filename)
            else:
                print("Маршрут не найден.")

        elif choice == '3':
            if G is None:
                print("Сначала загрузите данные (пункт 1 в меню)!")
                continue
            print("\nПоиск оптимального маршрута через все точки (TSP)...")
            tsp_path, tsp_distance = route_optimization.find_best_path_tsp(G)
            if tsp_path:
                print(f"\nОптимальный маршрут: {tsp_path}")
                print(f"Общее расстояние: {tsp_distance:.2f} км")
                visualization.plot_graph(G)
                visualization.plot_route(G, tsp_path)
                save = input("Сохранить маршрут в файл? (y/n): ").strip().lower()
                if save == 'y':
                    filename = input("Имя файла (по умолчанию route_result.txt): ").strip()
                    if filename == '':
                        filename = "route_result.txt"
                    save_route_to_file(tsp_path, tsp_distance, filename)
            else:
                print("Не удалось найти оптимальный маршрут по всем точкам.")

        elif choice == '4':
            print("До свидания!")
            break
        else:
            print("Некорректный ввод. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()