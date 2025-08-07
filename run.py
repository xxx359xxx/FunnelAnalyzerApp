#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Скрипт для запуска FunnelAnalyzerApp

Использование:
    python run.py              # Запуск с настройками по умолчанию
    python run.py --port 8502   # Запуск на другом порту
    python run.py --debug       # Запуск в режиме отладки
"""

import os
import sys
import subprocess
import argparse
from pathlib import Path

def check_dependencies():
    """Проверка установленных зависимостей"""
    required_packages = [
        'streamlit',
        'pandas', 
        'numpy',
        'plotly',
        'reportlab'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Отсутствуют зависимости: {', '.join(missing_packages)}")
        print("Установите их командой: pip install -r requirements.txt")
        return False
    
    print("✅ Все зависимости установлены")
    return True

def run_streamlit_app(port=8501, debug=False):
    """Запуск Streamlit приложения"""
    
    # Проверка существования app.py
    app_path = Path(__file__).parent / 'app.py'
    if not app_path.exists():
        print(f"❌ Файл app.py не найден: {app_path}")
        return False
    
    # Команда для запуска Streamlit
    cmd = [
        sys.executable, 
        '-m', 'streamlit', 'run', 
        str(app_path),
        '--server.port', str(port),
        '--server.headless', 'false',
        '--browser.gatherUsageStats', 'false'
    ]
    
    if debug:
        cmd.extend(['--logger.level', 'debug'])
    
    print(f"🚀 Запуск FunnelAnalyzerApp на порту {port}...")
    print(f"📱 Приложение будет доступно по адресу: http://localhost:{port}")
    print("⏹️  Для остановки нажмите Ctrl+C")
    print("-" * 50)
    
    try:
        # Запуск приложения
        subprocess.run(cmd, check=True)
    except KeyboardInterrupt:
        print("\n👋 Приложение остановлено пользователем")
    except subprocess.CalledProcessError as e:
        print(f"❌ Ошибка запуска приложения: {e}")
        return False
    except FileNotFoundError:
        print("❌ Streamlit не найден. Установите его: pip install streamlit")
        return False
    
    return True

def main():
    """Главная функция"""
    parser = argparse.ArgumentParser(
        description='Запуск FunnelAnalyzerApp - инструмента для анализа воронки конверсий'
    )
    
    parser.add_argument(
        '--port', 
        type=int, 
        default=8501,
        help='Порт для запуска приложения (по умолчанию: 8501)'
    )
    
    parser.add_argument(
        '--debug', 
        action='store_true',
        help='Запуск в режиме отладки'
    )
    
    parser.add_argument(
        '--skip-check', 
        action='store_true',
        help='Пропустить проверку зависимостей'
    )
    
    args = parser.parse_args()
    
    print("📊 FunnelAnalyzerApp - Анализ воронки конверсий в гемблинге")
    print("=" * 60)
    
    # Проверка зависимостей
    if not args.skip_check:
        if not check_dependencies():
            sys.exit(1)
    
    # Запуск приложения
    success = run_streamlit_app(port=args.port, debug=args.debug)
    
    if not success:
        sys.exit(1)

if __name__ == '__main__':
    main()