import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def generate_mock_data(n_users=5000, start_date=None, end_date=None):
    """
    Генерация моковых данных для анализа воронки конверсий в гемблинге
    
    Parameters:
    -----------
    n_users : int
        Количество пользователей для генерации
    start_date : datetime
        Начальная дата для генерации (по умолчанию 30 дней назад)
    end_date : datetime
        Конечная дата для генерации (по умолчанию сегодня)
    
    Returns:
    --------
    pd.DataFrame
        DataFrame с пользовательскими данными
    """
    
    if start_date is None:
        start_date = datetime.now() - timedelta(days=30)
    if end_date is None:
        end_date = datetime.now()
    
    # Настройка генератора случайных чисел
    np.random.seed(42)
    random.seed(42)
    
    # Списки возможных значений
    traffic_sources = [
        'google_ads', 'facebook_ads', 'instagram_ads', 'tiktok_ads',
        'organic', 'direct', 'referral', 'email', 'affiliate', 'youtube_ads'
    ]
    
    countries = [
        'RU', 'UA', 'BY', 'KZ', 'DE', 'PL', 'CZ', 'SK', 'LT', 'LV',
        'EE', 'FI', 'SE', 'NO', 'DK', 'NL', 'BE', 'AT', 'CH', 'FR'
    ]
    
    devices = ['mobile', 'desktop', 'tablet']
    
    # Веса для более реалистичного распределения
    traffic_weights = [0.25, 0.20, 0.15, 0.10, 0.12, 0.08, 0.05, 0.03, 0.01, 0.01]
    country_weights = [0.30, 0.15, 0.10, 0.08, 0.05, 0.04, 0.03, 0.03, 0.02, 0.02,
                      0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02, 0.02]
    device_weights = [0.65, 0.30, 0.05]
    
    # Нормализация весов для обеспечения суммы = 1
    traffic_weights = np.array(traffic_weights) / np.sum(traffic_weights)
    country_weights = np.array(country_weights) / np.sum(country_weights)
    device_weights = np.array(device_weights) / np.sum(device_weights)
    
    users_data = []
    
    for user_id in range(1, n_users + 1):
        # Базовые характеристики пользователя
        traffic_source = np.random.choice(traffic_sources, p=traffic_weights)
        country = np.random.choice(countries, p=country_weights)
        device = np.random.choice(devices, p=device_weights)
        
        # Время регистрации
        reg_time = start_date + timedelta(
            seconds=random.randint(0, int((end_date - start_date).total_seconds()))
        )
        
        # Вероятности конверсий (зависят от источника трафика и устройства)
        base_deposit_prob = 0.25
        base_bet_prob = 0.80
        base_second_deposit_prob = 0.35
        
        # Корректировка вероятностей по источнику трафика
        traffic_multipliers = {
            'google_ads': 1.2,
            'facebook_ads': 1.1,
            'instagram_ads': 0.9,
            'tiktok_ads': 0.8,
            'organic': 1.3,
            'direct': 1.4,
            'referral': 1.5,
            'email': 1.6,
            'affiliate': 1.1,
            'youtube_ads': 0.9
        }
        
        # Корректировка по устройству
        device_multipliers = {
            'mobile': 0.9,
            'desktop': 1.2,
            'tablet': 1.0
        }
        
        # Корректировка по стране (некоторые страны более конвертируемые)
        country_multipliers = {
            'RU': 1.0, 'UA': 0.9, 'BY': 0.8, 'KZ': 0.7, 'DE': 1.3,
            'PL': 1.1, 'CZ': 1.0, 'SK': 0.9, 'LT': 0.8, 'LV': 0.8,
            'EE': 0.9, 'FI': 1.4, 'SE': 1.3, 'NO': 1.5, 'DK': 1.4,
            'NL': 1.3, 'BE': 1.2, 'AT': 1.2, 'CH': 1.6, 'FR': 1.1
        }
        
        multiplier = (traffic_multipliers.get(traffic_source, 1.0) * 
                     device_multipliers.get(device, 1.0) * 
                     country_multipliers.get(country, 1.0))
        
        deposit_prob = min(base_deposit_prob * multiplier, 0.8)
        bet_prob = min(base_bet_prob * multiplier, 0.95)
        second_deposit_prob = min(base_second_deposit_prob * multiplier, 0.6)
        
        # Генерация событий
        deposit_time = None
        first_bet_time = None
        second_deposit_time = None
        
        # Депозит
        if random.random() < deposit_prob:
            # Время до депозита (от 5 минут до 48 часов)
            deposit_delay = timedelta(
                minutes=random.randint(5, 2880)  # 5 мин - 48 часов
            )
            deposit_time = reg_time + deposit_delay
            
            # Первая ставка (если есть депозит)
            if random.random() < bet_prob:
                # Время до первой ставки (от 1 минуты до 24 часов после депозита)
                bet_delay = timedelta(
                    minutes=random.randint(1, 1440)  # 1 мин - 24 часа
                )
                first_bet_time = deposit_time + bet_delay
                
                # Второй депозит (если есть первая ставка)
                if random.random() < second_deposit_prob:
                    # Время до второго депозита (от 1 часа до 7 дней после первой ставки)
                    second_deposit_delay = timedelta(
                        hours=random.randint(1, 168)  # 1 час - 7 дней
                    )
                    second_deposit_time = first_bet_time + second_deposit_delay
        
        # Добавление пользователя в данные
        users_data.append({
            'user_id': user_id,
            'registration_time': reg_time,
            'deposit_time': deposit_time,
            'first_bet_time': first_bet_time,
            'second_deposit_time': second_deposit_time,
            'traffic_source': traffic_source,
            'country': country,
            'device': device
        })
    
    # Создание DataFrame
    df = pd.DataFrame(users_data)
    
    # Добавление некоторых аномалий для демонстрации детекции
    if n_users >= 1000:
        # Создание "плохого" дня с низкой конверсией
        bad_day_start = start_date + timedelta(days=random.randint(5, 25))
        bad_day_end = bad_day_start + timedelta(days=1)
        
        bad_day_mask = (
            (df['registration_time'] >= bad_day_start) & 
            (df['registration_time'] < bad_day_end)
        )
        
        # Снижение конверсии в этот день на 70%
        bad_day_users = df[bad_day_mask].index
        for idx in bad_day_users:
            if random.random() < 0.7:  # 70% пользователей теряют депозит
                df.loc[idx, 'deposit_time'] = None
                df.loc[idx, 'first_bet_time'] = None
                df.loc[idx, 'second_deposit_time'] = None
    
    return df

def save_mock_data_to_csv(df, filename='mock_data.csv'):
    """
    Сохранение моковых данных в CSV файл
    
    Parameters:
    -----------
    df : pd.DataFrame
        DataFrame с данными
    filename : str
        Имя файла для сохранения
    """
    df.to_csv(filename, index=False)
    print(f"Данные сохранены в файл: {filename}")
    print(f"Количество записей: {len(df)}")
    print(f"Период: {df['registration_time'].min()} - {df['registration_time'].max()}")
    
    # Статистика по конверсиям
    total_users = len(df)
    depositors = len(df[df['deposit_time'].notna()])
    bettors = len(df[df['first_bet_time'].notna()])
    second_depositors = len(df[df['second_deposit_time'].notna()])
    
    print(f"\nСтатистика:")
    print(f"Всего пользователей: {total_users}")
    print(f"Сделали депозит: {depositors} ({depositors/total_users*100:.1f}%)")
    print(f"Сделали ставку: {bettors} ({bettors/depositors*100:.1f}% от депозитчиков)")
    print(f"Второй депозит: {second_depositors} ({second_depositors/bettors*100:.1f}% от игроков)")

def generate_sample_data_with_segments():
    """
    Генерация образцовых данных с интересными сегментами для демонстрации
    """
    # Генерация базовых данных
    df = generate_mock_data(5000)
    
    # Добавление специальных сегментов
    
    # VIP сегмент (высокие конверсии)
    vip_users = df.sample(n=100)
    for idx in vip_users.index:
        # Гарантированный депозит
        if pd.isna(df.loc[idx, 'deposit_time']):
            df.loc[idx, 'deposit_time'] = df.loc[idx, 'registration_time'] + timedelta(minutes=random.randint(5, 60))
        
        # Высокая вероятность ставки
        if pd.isna(df.loc[idx, 'first_bet_time']) and pd.notna(df.loc[idx, 'deposit_time']):
            df.loc[idx, 'first_bet_time'] = df.loc[idx, 'deposit_time'] + timedelta(minutes=random.randint(1, 30))
        
        # Высокая вероятность второго депозита
        if pd.isna(df.loc[idx, 'second_deposit_time']) and pd.notna(df.loc[idx, 'first_bet_time']):
            if random.random() < 0.8:  # 80% вероятность
                df.loc[idx, 'second_deposit_time'] = df.loc[idx, 'first_bet_time'] + timedelta(hours=random.randint(1, 48))
    
    return df

if __name__ == "__main__":
    # Генерация и сохранение тестовых данных
    print("Генерация моковых данных...")
    
    # Стандартные данные
    df_standard = generate_mock_data(5000)
    save_mock_data_to_csv(df_standard, 'mock_data.csv')
    
    print("\n" + "="*50)
    
    # Данные с сегментами
    df_segments = generate_sample_data_with_segments()
    save_mock_data_to_csv(df_segments, 'mock_data_with_segments.csv')
    
    print("\nГенерация завершена!")