#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Тест шрифтов с поддержкой кириллицы
"""

import pandas as pd
from utils import FunnelAnalyzer
from datetime import datetime

# Создаем тестовые данные
test_data = {
    'registration_time': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00'],
    'deposit_time': ['2024-01-01 10:30:00', '2024-01-01 11:30:00', None],
    'first_bet_time': ['2024-01-01 11:00:00', None, None],
    'second_deposit_time': [None, None, None],
    'traffic_source': ['email', 'direct', 'referral'],
    'country': ['RU', 'UA', 'KZ'],
    'device': ['desktop', 'mobile', 'tablet']
}

df = pd.DataFrame(test_data)

# Создаем анализатор
analyzer = FunnelAnalyzer(df)

print("Тестирование системы шрифтов...")
print("=" * 50)

try:
    # Генерируем PDF отчет с кириллицей
    buffer = analyzer.generate_pdf_report(
        df, 
        title="Тест кириллицы: Анализ воронки конверсий",
        author="Тестовый аналитик"
    )
    
    # Сохраняем PDF файл
    with open('test_cyrillic_report.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    
    print("\n🎉 PDF отчет успешно создан!")
    print("📄 Файл сохранен как: test_cyrillic_report.pdf")
    print("\nПроверьте файл на корректное отображение кириллицы.")
    
except Exception as e:
    print(f"\n❌ Ошибка при создании PDF: {e}")
    import traceback
    traceback.print_exc()