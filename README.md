 (Ctrl+Shift+P) Python: Create Environment
инициализхация виртуального окружения
python -m venv .venv

установка необходимых зависимостей
pip install -r Requirements.txt

сохранение необходимых зависимостей
pip freeze > Requirements.txt

git config --global user.email "andkir@mail.ru"
git config --global user.name "andkir1024"

pip install PyInstaller

создание выполняемого файла
pyinstaller --onefile main.py

параметры запуска с командной строкой
1. источник файлов png для обработки
--dirSrc=../popular/
2. включение оконного режима иначи консоль отрабатывает всю заданную директорию dirSrc
--wnd
3. коэффициэнт перемасштабирования для  создания svg (9.066)
--svg=9.066
4. директория для результата
--dirDst=../popular/

пример запуска
