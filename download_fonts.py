#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для загрузки DejaVu шрифтов с поддержкой кириллицы
"""

import os
import urllib.request
import zipfile
import shutil

def download_dejavu_fonts():
    """Загрузка DejaVu шрифтов"""
    fonts_dir = "./fonts/"
    os.makedirs(fonts_dir, exist_ok=True)
    
    # URL для загрузки DejaVu шрифтов
    dejavu_url = "https://sourceforge.net/projects/dejavu/files/dejavu/2.37/dejavu-fonts-ttf-2.37.zip/download"
    zip_path = os.path.join(fonts_dir, "dejavu-fonts.zip")
    
    try:
        print("Загрузка DejaVu шрифтов...")
        urllib.request.urlretrieve(dejavu_url, zip_path)
        
        print("Распаковка архива...")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(fonts_dir)
        
        # Поиск и копирование нужных шрифтов
        for root, dirs, files in os.walk(fonts_dir):
            for file in files:
                if file in ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf']:
                    src = os.path.join(root, file)
                    dst = os.path.join(fonts_dir, file)
                    if src != dst:
                        shutil.copy2(src, dst)
                        print(f"Скопирован: {file}")
        
        # Удаление временных файлов
        os.remove(zip_path)
        
        # Удаление временных папок
        for item in os.listdir(fonts_dir):
            item_path = os.path.join(fonts_dir, item)
            if os.path.isdir(item_path):
                shutil.rmtree(item_path)
        
        print("✓ DejaVu шрифты успешно загружены!")
        return True
        
    except Exception as e:
        print(f"✗ Ошибка загрузки шрифтов: {e}")
        return False

def create_fallback_fonts():
    """Создание fallback шрифтов если загрузка не удалась"""
    fonts_dir = "./fonts/"
    os.makedirs(fonts_dir, exist_ok=True)
    
    # Создаем символические ссылки на системные шрифты Windows
    system_fonts = {
        'arial.ttf': 'DejaVuSans.ttf',
        'arialbd.ttf': 'DejaVuSans-Bold.ttf'
    }
    
    windows_fonts_dir = "C:/Windows/Fonts/"
    
    for system_font, target_name in system_fonts.items():
        system_path = os.path.join(windows_fonts_dir, system_font)
        target_path = os.path.join(fonts_dir, target_name)
        
        if os.path.exists(system_path) and not os.path.exists(target_path):
            try:
                shutil.copy2(system_path, target_path)
                print(f"✓ Скопирован fallback шрифт: {target_name}")
            except Exception as e:
                print(f"✗ Ошибка копирования {system_font}: {e}")

if __name__ == "__main__":
    print("Настройка шрифтов для поддержки кириллицы...")
    
    # Попытка загрузить DejaVu шрифты
    if not download_dejavu_fonts():
        print("Попытка использовать системные шрифты...")
        create_fallback_fonts()
    
    # Проверка результата
    fonts_dir = "./fonts/"
    required_fonts = ['DejaVuSans.ttf', 'DejaVuSans-Bold.ttf']
    
    all_found = True
    for font in required_fonts:
        font_path = os.path.join(fonts_dir, font)
        if os.path.exists(font_path):
            print(f"✓ {font} найден")
        else:
            print(f"✗ {font} не найден")
            all_found = False
    
    if all_found:
        print("\n🎉 Все шрифты готовы к использованию!")
    else:
        print("\n⚠ Некоторые шрифты не найдены. Будут использованы стандартные.")