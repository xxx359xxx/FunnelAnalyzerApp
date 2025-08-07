# FunnelAnalyzerApp 📊

**Инструмент для анализа воронки конверсий в гемблинге**

Приложение с визуальным интерфейсом на Streamlit для анализа пользовательских воронок конверсий, детекции аномалий и генерации отчетов.

## 🚀 Возможности

- **Загрузка данных**: CSV файлы или генерация моковых данных
- **Анализ воронки**: Регистрация → Депозит → Первая ставка → Второй депозит
- **Метрики**: Конверсии между этапами, время между событиями
- **Сегментация**: Анализ по источникам трафика, странам, устройствам
- **Детекция аномалий**: Автоматическое обнаружение падений конверсий
- **Визуализация**: Интерактивные графики Plotly
- **Отчеты**: Генерация PDF отчетов

## 📋 Требования

- Python 3.8+
- Зависимости из `requirements.txt`

## 🛠️ Установка

### 1. Клонирование и установка зависимостей

```bash
# Перейти в директорию проекта
cd FunnelAnalyzerApp

# Создать виртуальное окружение (рекомендуется)
python -m venv venv

# Активировать виртуальное окружение
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Установить зависимости
pip install -r requirements.txt
```

### 2. Запуск приложения

```bash
# Запуск Streamlit приложения
streamlit run app.py
```

Приложение откроется в браузере по адресу: `http://localhost:8501`

## 📁 Структура проекта

```
FunnelAnalyzerApp/
├── app.py                          # Основное Streamlit приложение
├── utils.py                        # Класс FunnelAnalyzer и утилиты
├── generate_mock_data.py           # Генерация тестовых данных
├── requirements.txt                # Зависимости Python
├── mock_data.csv                   # Тестовые данные (5000 записей)
├── mock_data_with_segments.csv     # Тестовые данные с сегментами
└── README.md                       # Документация
```

## 📊 Формат данных

### Обязательные поля CSV файла:

| Поле | Тип | Описание |
|------|-----|----------|
| `user_id` | int/string | Уникальный идентификатор пользователя |
| `registration_time` | datetime | Время регистрации |
| `deposit_time` | datetime | Время первого депозита (может быть пустым) |
| `first_bet_time` | datetime | Время первой ставки (может быть пустым) |
| `second_deposit_time` | datetime | Время второго депозита (может быть пустым) |
| `traffic_source` | string | Источник трафика (google_ads, organic, etc.) |
| `country` | string | Код страны (RU, UA, DE, etc.) |
| `device` | string | Тип устройства (mobile, desktop, tablet) |

### Пример CSV файла:

```csv
user_id,registration_time,deposit_time,first_bet_time,second_deposit_time,traffic_source,country,device
1,2025-07-01 10:00:00,2025-07-01 12:00:00,2025-07-01 12:30:00,,google_ads,RU,mobile
2,2025-07-01 11:00:00,,,,,organic,UA,desktop
3,2025-07-01 12:00:00,2025-07-01 13:00:00,2025-07-01 13:15:00,2025-07-02 10:00:00,facebook_ads,DE,mobile
```

## 🎯 Использование

### 1. Загрузка данных
- **CSV файл**: Загрузите файл через боковую панель
- **Моковые данные**: Выберите "Использовать моковые данные" и нажмите "Сгенерировать данные"

### 2. Анализ воронки
- Просмотрите основные метрики конверсий
- Изучите время между этапами
- Примените фильтры по сегментам
- Анализируйте данные по источникам трафика, странам и устройствам

### 3. Детекция аномалий
- Настройте пороги для обнаружения аномалий
- Отслеживайте тренды конверсий по дням
- Получайте предупреждения о резких изменениях

### 4. Генерация отчетов
- Настройте содержание отчета
- Сгенерируйте PDF отчет
- Скачайте отчет с результатами анализа

## 🔧 Сборка в .exe (Desktop версия)

### Установка PyInstaller

```bash
pip install pyinstaller
```

### Создание .exe файла

```bash
# Простая сборка
pyinstaller --onefile --windowed app.py

# Расширенная сборка с иконкой и дополнительными файлами
pyinstaller --onefile --windowed --add-data "utils.py;." --add-data "generate_mock_data.py;." --add-data "mock_data.csv;." --name "FunnelAnalyzerApp" app.py
```

### Альтернативный способ с spec файлом

Создайте файл `FunnelAnalyzerApp.spec`:

```python
# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('utils.py', '.'),
        ('generate_mock_data.py', '.'),
        ('mock_data.csv', '.'),
        ('requirements.txt', '.')
    ],
    hiddenimports=[
        'streamlit',
        'plotly',
        'pandas',
        'numpy',
        'reportlab'
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyi_splash = Splash(
    'splash.png',  # Опционально: добавьте splash screen
    binaries=a.binaries,
    datas=a.datas,
    text_pos=None,
    text_size=12,
    minify_script=True,
    always_on_top=True,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    splash,
    splash.binaries,
    [],
    name='FunnelAnalyzerApp',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
```

Затем выполните:

```bash
pyinstaller FunnelAnalyzerApp.spec
```

### Запуск .exe файла

После сборки исполняемый файл будет находиться в папке `dist/`:

```bash
# Запуск
.\dist\FunnelAnalyzerApp.exe
```

**Примечание**: При запуске .exe файла Streamlit автоматически откроет браузер с приложением.

## 📈 Примеры использования

### Анализ конверсий по источникам трафика

1. Загрузите данные
2. Перейдите на вкладку "Анализ воронки"
3. Выберите интересующие источники трафика
4. Изучите метрики конверсий и графики

### Детекция аномалий

1. Перейдите на вкладку "Детекция аномалий"
2. Настройте порог аномалии (например, 50%)
3. Просмотрите обнаруженные аномалии
4. Изучите тренды конверсий

### Генерация отчета

1. Перейдите на вкладку "Отчет"
2. Настройте параметры отчета
3. Выберите разделы для включения
4. Нажмите "Сгенерировать PDF отчет"
5. Скачайте готовый отчет

## 🐛 Устранение неполадок

### Проблемы с установкой зависимостей

```bash
# Обновите pip
python -m pip install --upgrade pip

# Установите зависимости по одной
pip install streamlit
pip install pandas
pip install plotly
pip install reportlab
```

### Проблемы с кодировкой CSV

Если возникают проблемы с кодировкой при загрузке CSV:

1. Сохраните CSV файл в кодировке UTF-8
2. Используйте точку с запятой (;) как разделитель
3. Убедитесь, что даты в формате YYYY-MM-DD HH:MM:SS

### Проблемы с .exe файлом

1. Убедитесь, что все зависимости установлены
2. Проверьте, что все файлы включены в сборку
3. Запустите из командной строки для просмотра ошибок

## 📞 Поддержка

Для получения помощи:

1. Проверьте раздел "Устранение неполадок"
2. Убедитесь, что используете правильный формат данных
3. Проверьте логи в терминале при запуске

## 📄 Лицензия

Проект создан для образовательных и коммерческих целей.

---

**FunnelAnalyzerApp** - Мощный инструмент для анализа воронки конверсий в гемблинге 🎰📊