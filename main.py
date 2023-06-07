
# Импортирование модуля argparse для обработки аргументов командной строки
import argparse

# Определение функции для вычисления площади прямоугольника
def calculate_rectangle_area(length, width):
    area = length * width
    return area

# Проверка, что код выполняется как самостоятельная программа, а не импортирован в другой модуль
if __name__ == "__main__":
    # Создание объекта парсера argparse.ArgumentParser()
    parser = argparse.ArgumentParser()

    # Определение аргументов командной строки с помощью метода add_argument()
    parser.add_argument("--length", type=float, help="Length of the rectangle")
    parser.add_argument("--width", type=float, help="Width of the rectangle")

    # Парсинг аргументов командной строки
    args = parser.parse_args()

    # Проверка наличия значений длины и ширины прямоугольника в аргументах командной строки
    if args.length is None or args.width is None:
        print("Ошибка: необходимо указать длину и ширину прямоугольника.")
    else:
        # Вычисление площади прямоугольника с помощью функции calculate_rectangle_area()
        area = calculate_rectangle_area(args.length, args.width)

        # Вывод площади прямоугольника на экран
        print("Площадь прямоугольника:", area)

