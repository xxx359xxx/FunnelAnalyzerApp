import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import numpy as np
from utils import FunnelAnalyzer, detect_anomalies
from generate_mock_data import generate_mock_data
import base64
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
import tempfile
import os

# Настройка страницы
st.set_page_config(
    page_title="FunnelAnalyzerApp",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Заголовок приложения
st.title("📊 FunnelAnalyzerApp")
st.markdown("### Инструмент для анализа воронки конверсий в гемблинге")

# Боковая панель
st.sidebar.header("⚙️ Настройки")

# Контактная информация
st.sidebar.markdown("---")
st.sidebar.markdown("""
<a href="https://t.me/alkash_slayer" target="_blank">
    <svg width="20" height="20" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
        <path d="M12 2C6.48 2 2 6.48 2 12s4.48 10 10 10 10-4.48 10-10S17.52 2 12 2zm4.64 6.8c-.15 1.58-.8 5.42-1.13 7.19-.14.75-.42 1-.68 1.03-.58.05-1.02-.38-1.58-.75-.88-.58-1.38-.94-2.23-1.5-.99-.65-.35-1.01.22-1.59.15-.15 2.71-2.48 2.76-2.69a.2.2 0 00-.05-.18c-.06-.05-.14-.03-.21-.02-.09.02-1.49.95-4.22 2.79-.4.27-.76.41-1.08.4-.36-.01-1.04-.2-1.55-.37-.63-.2-1.12-.31-1.08-.66.02-.18.27-.36.74-.55 2.92-1.27 4.86-2.11 5.83-2.51 2.78-1.16 3.35-1.36 3.73-1.36.08 0 .27.02.39.12.1.08.13.19.14.27-.01.06.01.24 0 .38z" fill="#0088cc"/>
    </svg>
    Telegram
</a>
""", unsafe_allow_html=True)
st.sidebar.markdown("---")

# Выбор источника данных
data_source = st.sidebar.radio(
    "Источник данных:",
    ["Загрузить CSV файл", "Использовать моковые данные"]
)

# Инициализация данных
df = None

if data_source == "Загрузить CSV файл":
    uploaded_file = st.sidebar.file_uploader(
        "Выберите CSV файл",
        type=['csv'],
        help="Файл должен содержать поля: user_id, registration_time, deposit_time, first_bet_time, second_deposit_time, traffic_source, country, device"
    )
    
    if uploaded_file is not None:
        try:
            df = pd.read_csv(uploaded_file)
            st.sidebar.success(f"✅ Файл загружен: {len(df)} записей")
        except Exception as e:
            st.sidebar.error(f"❌ Ошибка загрузки файла: {str(e)}")
else:
    # Параметры для генерации моковых данных
    st.sidebar.subheader("Параметры генерации данных")
    n_users = st.sidebar.slider("Количество пользователей", 1000, 10000, 5000, 500)
    
    if st.sidebar.button("🎲 Сгенерировать данные"):
        with st.spinner("Генерация данных..."):
            df = generate_mock_data(n_users)
            st.sidebar.success(f"✅ Данные сгенерированы: {len(df)} записей")

# Основной интерфейс
if df is not None:
    # Проверка структуры данных
    required_columns = ['user_id', 'registration_time', 'deposit_time', 'first_bet_time', 
                       'second_deposit_time', 'traffic_source', 'country', 'device']
    
    missing_columns = [col for col in required_columns if col not in df.columns]
    
    if missing_columns:
        st.error(f"❌ Отсутствуют обязательные поля: {', '.join(missing_columns)}")
        st.stop()
    
    # Преобразование дат
    date_columns = ['registration_time', 'deposit_time', 'first_bet_time', 'second_deposit_time']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Создание анализатора
    analyzer = FunnelAnalyzer(df)
    
    # Вкладки
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Обзор данных", "🔄 Анализ воронки", "⚠️ Детекция аномалий", "📄 Отчет"])
    
    with tab1:
        st.header("📊 Обзор данных")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("Всего пользователей", len(df))
        
        with col2:
            depositors = len(df[df['deposit_time'].notna()])
            st.metric("Депозитчики", depositors)
        
        with col3:
            bettors = len(df[df['first_bet_time'].notna()])
            st.metric("Сделали ставку", bettors)
        
        with col4:
            second_depositors = len(df[df['second_deposit_time'].notna()])
            st.metric("Второй депозит", second_depositors)
        
        # Распределения
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Распределение по источникам трафика")
            traffic_dist = df['traffic_source'].value_counts()
            fig_traffic = px.pie(values=traffic_dist.values, names=traffic_dist.index, 
                               title="Источники трафика")
            st.plotly_chart(fig_traffic, use_container_width=True)
        
        with col2:
            st.subheader("Распределение по странам")
            country_dist = df['country'].value_counts()
            fig_country = px.bar(x=country_dist.index, y=country_dist.values, 
                               title="Страны")
            st.plotly_chart(fig_country, use_container_width=True)
        
        # Таблица с данными
        st.subheader("Просмотр данных")
        st.dataframe(df.head(100), use_container_width=True)
    
    with tab2:
        st.header("🔄 Анализ воронки")
        
        # Фильтры
        col1, col2, col3 = st.columns(3)
        
        with col1:
            selected_traffic = st.multiselect(
                "Источники трафика",
                options=df['traffic_source'].unique(),
                default=df['traffic_source'].unique()
            )
        
        with col2:
            selected_countries = st.multiselect(
                "Страны",
                options=df['country'].unique(),
                default=df['country'].unique()
            )
        
        with col3:
            selected_devices = st.multiselect(
                "Устройства",
                options=df['device'].unique(),
                default=df['device'].unique()
            )
        
        # Фильтрация данных
        filtered_df = df[
            (df['traffic_source'].isin(selected_traffic)) &
            (df['country'].isin(selected_countries)) &
            (df['device'].isin(selected_devices))
        ]
        
        if len(filtered_df) == 0:
            st.warning("⚠️ Нет данных для выбранных фильтров")
        else:
            # Анализ воронки
            funnel_metrics = analyzer.calculate_funnel_metrics(filtered_df)
            
            # Метрики воронки
            st.subheader("📈 Метрики воронки")
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric(
                    "Регистрация → Депозит",
                    f"{funnel_metrics['conversions']['reg_to_deposit']:.1f}%"
                )
            
            with col2:
                st.metric(
                    "Депозит → Ставка",
                    f"{funnel_metrics['conversions']['deposit_to_bet']:.1f}%"
                )
            
            with col3:
                st.metric(
                    "Ставка → Второй депозит",
                    f"{funnel_metrics['conversions']['bet_to_second_deposit']:.1f}%"
                )
            
            with col4:
                st.metric(
                    "Общая конверсия",
                    f"{funnel_metrics['conversions']['overall_conversion']:.1f}%"
                )
            
            # График воронки
            st.subheader("📊 Воронка конверсий")
            
            funnel_fig = analyzer.create_funnel_chart(funnel_metrics)
            st.plotly_chart(funnel_fig, use_container_width=True)
            
            # Время между этапами
            st.subheader("⏱️ Среднее время между этапами")
            
            time_data = {
                'Этап': ['Регистрация → Депозит', 'Депозит → Ставка', 'Ставка → Второй депозит'],
                'Время (часы)': [
                    funnel_metrics['avg_times_hours']['reg_to_deposit'] or 0,
                    funnel_metrics['avg_times_hours']['deposit_to_bet'] or 0,
                    funnel_metrics['avg_times_hours']['bet_to_second_deposit'] or 0
                ]
            }
            
            time_df = pd.DataFrame(time_data)
            fig_time = px.bar(time_df, x='Этап', y='Время (часы)', 
                            title="Среднее время между этапами")
            st.plotly_chart(fig_time, use_container_width=True)
            
            # Анализ по сегментам
            st.subheader("🎯 Анализ по сегментам")
            
            segment_analysis = analyzer.analyze_by_segments(filtered_df)
            
            for segment_name, segment_df in segment_analysis.items():
                st.write(f"**{segment_name.upper()}:**")
                
                # График конверсий по сегменту
                fig_segment = px.bar(
                    segment_df, 
                    x='segment_value', 
                    y='reg_to_deposit_conv',
                    title=f"Конверсия в депозит по {segment_name}",
                    text='reg_to_deposit_conv'
                )
                fig_segment.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
                st.plotly_chart(fig_segment, use_container_width=True)
    
    with tab3:
        st.header("⚠️ Детекция аномалий")
        
        # Параметры для детекции аномалий
        col1, col2 = st.columns(2)
        
        with col1:
            anomaly_threshold = st.slider(
                "Порог аномалии (%)", 
                min_value=10, 
                max_value=100, 
                value=50,
                help="Процентное изменение, которое считается аномалией"
            )
        
        with col2:
            comparison_period = st.selectbox(
                "Период сравнения",
                ["Предыдущий день", "Предыдущая неделя", "Предыдущий месяц"]
            )
        
        # Детекция аномалий
        anomalies = detect_anomalies(df, threshold=anomaly_threshold/100)
        
        if anomalies:
            st.error("🚨 Обнаружены аномалии:")
            for anomaly in anomalies:
                st.warning(f"• {anomaly}")
        else:
            st.success("✅ Аномалий не обнаружено")
        
        # Тренды конверсий по дням
        st.subheader("📈 Тренды конверсий")
        
        daily_metrics = analyzer.calculate_daily_metrics(df)
        
        if not daily_metrics.empty:
            fig_trends = px.line(
                daily_metrics, 
                x='date', 
                y='reg_to_deposit_conv',
                title="Конверсия регистрация → депозит по дням",
                markers=True
            )
            st.plotly_chart(fig_trends, use_container_width=True)
    
    with tab4:
        st.header("📄 Генерация отчета")
        
        # Параметры отчета
        col1, col2 = st.columns(2)
        
        with col1:
            report_title = st.text_input("Название отчета", "Анализ воронки конверсий")
        
        with col2:
            report_author = st.text_input("Автор отчета", "Gambling Analyst")
        
        # Выбор данных для отчета
        include_overview = st.checkbox("Включить обзор данных", True)
        include_funnel = st.checkbox("Включить анализ воронки", True)
        include_segments = st.checkbox("Включить анализ по сегментам", True)
        include_anomalies = st.checkbox("Включить детекцию аномалий", True)
        
        if st.button("📄 Сгенерировать PDF отчет", type="primary"):
            with st.spinner("Генерация отчета..."):
                try:
                    # Создание PDF отчета
                    pdf_buffer = analyzer.generate_pdf_report(
                        df=filtered_df if 'filtered_df' in locals() else df,
                        title=report_title,
                        author=report_author,
                        include_overview=include_overview,
                        include_funnel=include_funnel,
                        include_segments=include_segments,
                        include_anomalies=include_anomalies
                    )
                    
                    # Кнопка скачивания
                    st.download_button(
                        label="💾 Скачать PDF отчет",
                        data=pdf_buffer.getvalue(),
                        file_name=f"funnel_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf"
                    )
                    
                    st.success("✅ Отчет успешно сгенерирован!")
                    
                except Exception as e:
                    st.error(f"❌ Ошибка генерации отчета: {str(e)}")
else:
    # Стартовая страница
    st.info("👆 Выберите источник данных в боковой панели для начала анализа")
    
    # Инструкции
    st.markdown("""
    ## 🚀 Как использовать FunnelAnalyzerApp:
    
    ### 1. Загрузка данных
    - **CSV файл**: Загрузите файл с полями user_id, registration_time, deposit_time, first_bet_time, second_deposit_time, traffic_source, country, device
    - **Моковые данные**: Сгенерируйте тестовые данные для демонстрации
    
    ### 2. Анализ воронки
    - Просмотрите метрики конверсий между этапами
    - Изучите время между этапами
    - Проанализируйте данные по сегментам
    
    ### 3. Детекция аномалий
    - Настройте пороги для обнаружения аномалий
    - Отслеживайте тренды конверсий
    
    ### 4. Генерация отчетов
    - Создайте PDF отчет с результатами анализа
    - Настройте содержание отчета
    
    ---
    
    **Требования к CSV файлу:**
    ```
    user_id,registration_time,deposit_time,first_bet_time,second_deposit_time,traffic_source,country,device
    1,2025-07-01 10:00:00,2025-07-01 12:00:00,2025-07-01 12:30:00,,google_ads,RU,mobile
    2,2025-07-01 11:00:00,,,,,organic,UA,desktop
    ...
    ```
    """)

# Футер
st.markdown("---")
st.markdown("**FunnelAnalyzerApp** - Инструмент для анализа воронки конверсий в гемблинге | Создано с ❤️ на Streamlit")