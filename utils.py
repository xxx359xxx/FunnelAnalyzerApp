import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import io
from reportlab.lib.pagesizes import letter, A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os
import tempfile
import os

def register_fonts():
    """Регистрация шрифтов с поддержкой кириллицы"""
    try:
        # Получаем абсолютный путь к папке со скриптом
        script_dir = os.path.dirname(os.path.abspath(__file__))
        local_fonts_dir = os.path.join(script_dir, "fonts")
        
        # Список путей для поиска шрифтов (приоритет локальным)
        font_paths = [
            # Локальные шрифты (высший приоритет)
            local_fonts_dir,
            "./fonts/",
            # Системные пути Windows
            "C:/Windows/Fonts/",
            "C:/WINDOWS/Fonts/",
            # Пути для различных ОС
            "/usr/share/fonts/truetype/dejavu/",
            "/usr/share/fonts/TTF/",
            "/System/Library/Fonts/",
            "/Library/Fonts/",
        ]
        
        # Приоритетные шрифты с поддержкой кириллицы
        priority_fonts = [
            # DejaVu (лучшая поддержка кириллицы)
            ("DejaVuSans.ttf", "DejaVuSans"),
            ("DejaVuSans-Bold.ttf", "DejaVuSans-Bold"),
            # Liberation (хорошая альтернатива)
            ("LiberationSans-Regular.ttf", "LiberationSans"),
            ("LiberationSans-Bold.ttf", "LiberationSans-Bold"),
            # Системные шрифты Windows
            ("arial.ttf", "Arial"),
            ("arialbd.ttf", "Arial-Bold"),
            ("times.ttf", "Times"),
            ("timesbd.ttf", "Times-Bold"),
        ]
        
        registered_fonts = []
        
        # Попытка регистрации приоритетных шрифтов
        for font_file, font_name in priority_fonts:
            for base_path in font_paths:
                font_path = os.path.join(base_path, font_file)
                if os.path.exists(font_path):
                    try:
                        pdfmetrics.registerFont(TTFont(font_name, font_path))
                        registered_fonts.append(font_name)
                        print(f"✓ Зарегистрирован шрифт: {font_name} ({font_path})")
                        break
                    except Exception as e:
                        print(f"✗ Ошибка регистрации {font_name}: {e}")
                        continue
        
        # Fallback: регистрация Unicode CID шрифтов
        if not registered_fonts:
            try:
                # Попытка использовать встроенные Unicode шрифты ReportLab
                from reportlab.pdfbase.cidfonts import UnicodeCIDFont
                pdfmetrics.registerFont(UnicodeCIDFont('HeiseiKakuGo-W5'))
                registered_fonts.append('HeiseiKakuGo-W5')
                print("✓ Зарегистрирован fallback Unicode шрифт: HeiseiKakuGo-W5")
            except:
                pass
        
        if registered_fonts:
            print(f"✓ Всего зарегистрировано шрифтов: {len(registered_fonts)}")
            return registered_fonts
        else:
            print("⚠ Не удалось зарегистрировать ни одного шрифта с поддержкой кириллицы")
            return []
            
    except Exception as e:
        print(f"✗ Ошибка при регистрации шрифтов: {e}")
        return []

class FunnelAnalyzer:
    """Класс для анализа воронки конверсий в гемблинге"""
    
    def __init__(self, df):
        self.df = df.copy()
        self.prepare_data()
    
    def prepare_data(self):
        """Подготовка данных для анализа"""
        # Преобразование дат
        date_columns = ['registration_time', 'deposit_time', 'first_bet_time', 'second_deposit_time']
        for col in date_columns:
            self.df[col] = pd.to_datetime(self.df[col], errors='coerce')
        
        # Создание флагов для каждого этапа
        self.df['has_registration'] = True  # Все пользователи зарегистрированы
        self.df['has_deposit'] = self.df['deposit_time'].notna()
        self.df['has_first_bet'] = self.df['first_bet_time'].notna()
        self.df['has_second_deposit'] = self.df['second_deposit_time'].notna()
        
        # Расчет времени между этапами (в часах)
        self.df['time_reg_to_deposit'] = (
            self.df['deposit_time'] - self.df['registration_time']
        ).dt.total_seconds() / 3600
        
        self.df['time_deposit_to_bet'] = (
            self.df['first_bet_time'] - self.df['deposit_time']
        ).dt.total_seconds() / 3600
        
        self.df['time_bet_to_second_deposit'] = (
            self.df['second_deposit_time'] - self.df['first_bet_time']
        ).dt.total_seconds() / 3600
    
    def calculate_funnel_metrics(self, df=None):
        """Расчет основных метрик воронки"""
        if df is None:
            df = self.df
        else:
            # Если передан другой DataFrame, подготовим его
            df = df.copy()
            # Преобразование дат
            date_columns = ['registration_time', 'deposit_time', 'first_bet_time', 'second_deposit_time']
            for col in date_columns:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Создание флагов для каждого этапа
            df['has_deposit'] = df['deposit_time'].notna()
            df['has_first_bet'] = df['first_bet_time'].notna()
            df['has_second_deposit'] = df['second_deposit_time'].notna()
            
            # Расчет времени между этапами (в часах)
            df['time_reg_to_deposit'] = (
                df['deposit_time'] - df['registration_time']
            ).dt.total_seconds() / 3600
            
            df['time_deposit_to_bet'] = (
                df['first_bet_time'] - df['deposit_time']
            ).dt.total_seconds() / 3600
            
            df['time_bet_to_second_deposit'] = (
                df['second_deposit_time'] - df['first_bet_time']
            ).dt.total_seconds() / 3600
        
        # Количество пользователей на каждом этапе
        registrations = len(df)
        deposits = len(df[df['has_deposit']])
        first_bets = len(df[df['has_first_bet']])
        second_deposits = len(df[df['has_second_deposit']])
        
        # Конверсии между этапами
        reg_to_deposit = (deposits / registrations * 100) if registrations > 0 else 0
        deposit_to_bet = (first_bets / deposits * 100) if deposits > 0 else 0
        bet_to_second_deposit = (second_deposits / first_bets * 100) if first_bets > 0 else 0
        overall_conversion = (second_deposits / registrations * 100) if registrations > 0 else 0
        
        # Среднее время между этапами
        avg_time_reg_to_deposit = df['time_reg_to_deposit'].mean()
        avg_time_deposit_to_bet = df['time_deposit_to_bet'].mean()
        avg_time_bet_to_second_deposit = df['time_bet_to_second_deposit'].mean()
        
        return {
            'counts': {
                'registrations': registrations,
                'deposits': deposits,
                'first_bets': first_bets,
                'second_deposits': second_deposits
            },
            'conversions': {
                'reg_to_deposit': reg_to_deposit,
                'deposit_to_bet': deposit_to_bet,
                'bet_to_second_deposit': bet_to_second_deposit,
                'overall_conversion': overall_conversion
            },
            'avg_times_hours': {
                'reg_to_deposit': avg_time_reg_to_deposit,
                'deposit_to_bet': avg_time_deposit_to_bet,
                'bet_to_second_deposit': avg_time_bet_to_second_deposit
            }
        }
    
    def create_funnel_chart(self, metrics):
        """Создание графика воронки"""
        stages = ['Регистрация', 'Депозит', 'Первая ставка', 'Второй депозит']
        values = [
            metrics['counts']['registrations'],
            metrics['counts']['deposits'],
            metrics['counts']['first_bets'],
            metrics['counts']['second_deposits']
        ]
        
        # Расчет процентов от предыдущего этапа
        percentages = [100]
        percentages.append(metrics['conversions']['reg_to_deposit'])
        percentages.append(metrics['conversions']['deposit_to_bet'])
        percentages.append(metrics['conversions']['bet_to_second_deposit'])
        
        # Создание воронки
        fig = go.Figure()
        
        # Основные бары
        fig.add_trace(go.Bar(
            x=stages,
            y=values,
            text=[f'{v:,}<br>({p:.1f}%)' for v, p in zip(values, percentages)],
            textposition='auto',
            marker_color=['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728'],
            name='Пользователи'
        ))
        
        fig.update_layout(
            title='Воронка конверсий',
            xaxis_title='Этапы',
            yaxis_title='Количество пользователей',
            showlegend=False,
            height=500
        )
        
        return fig
    
    def create_sankey_chart(self, metrics):
        """Создание Sankey диаграммы"""
        # Узлы
        node_labels = ['Регистрация', 'Депозит', 'Первая ставка', 'Второй депозит', 'Отток']
        
        # Связи
        source = [0, 0, 1, 1, 2, 2]  # Откуда
        target = [1, 4, 2, 4, 3, 4]  # Куда
        value = [
            metrics['counts']['deposits'],
            metrics['counts']['registrations'] - metrics['counts']['deposits'],
            metrics['counts']['first_bets'],
            metrics['counts']['deposits'] - metrics['counts']['first_bets'],
            metrics['counts']['second_deposits'],
            metrics['counts']['first_bets'] - metrics['counts']['second_deposits']
        ]
        
        fig = go.Figure(data=[go.Sankey(
            node=dict(
                pad=15,
                thickness=20,
                line=dict(color="black", width=0.5),
                label=node_labels,
                color="blue"
            ),
            link=dict(
                source=source,
                target=target,
                value=value
            )
        )])
        
        fig.update_layout(
            title_text="Sankey диаграмма воронки конверсий",
            font_size=10,
            height=500
        )
        
        return fig
    
    def analyze_by_segments(self, df=None):
        """Анализ по сегментам"""
        if df is None:
            df = self.df
        
        segments = ['traffic_source', 'country', 'device']
        results = {}
        
        for segment in segments:
            segment_analysis = []
            
            for segment_value in df[segment].unique():
                if pd.isna(segment_value):
                    continue
                    
                segment_df = df[df[segment] == segment_value]
                metrics = self.calculate_funnel_metrics(segment_df)
                
                segment_analysis.append({
                    'segment_value': segment_value,
                    'users': len(segment_df),
                    'reg_to_deposit_conv': metrics['conversions']['reg_to_deposit'],
                    'deposit_to_bet_conv': metrics['conversions']['deposit_to_bet'],
                    'bet_to_second_deposit_conv': metrics['conversions']['bet_to_second_deposit'],
                    'overall_conv': metrics['conversions']['overall_conversion']
                })
            
            results[segment] = pd.DataFrame(segment_analysis)
        
        return results
    
    def calculate_daily_metrics(self, df=None):
        """Расчет ежедневных метрик"""
        if df is None:
            df = self.df
        
        # Группировка по дням регистрации
        df['reg_date'] = df['registration_time'].dt.date
        daily_stats = []
        
        for date in df['reg_date'].unique():
            if pd.isna(date):
                continue
                
            day_df = df[df['reg_date'] == date]
            metrics = self.calculate_funnel_metrics(day_df)
            
            daily_stats.append({
                'date': date,
                'registrations': metrics['counts']['registrations'],
                'deposits': metrics['counts']['deposits'],
                'reg_to_deposit_conv': metrics['conversions']['reg_to_deposit'],
                'overall_conv': metrics['conversions']['overall_conversion']
            })
        
        return pd.DataFrame(daily_stats).sort_values('date')
    
    def generate_pdf_report(self, df, title="Funnel Conversion Analysis", author="Analyst", 
                          include_overview=True, include_funnel=True, 
                          include_segments=True, include_anomalies=True):
        """Генерация PDF отчета"""
        # Register fonts for better text support
        registered_fonts = register_fonts()
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=A4)
        styles = getSampleStyleSheet()
        story = []
        
        # Определение шрифта для использования
        font_name = 'Helvetica'
        font_bold = 'Helvetica-Bold'
        
        if registered_fonts:
            # Проверяем доступные шрифты в порядке приоритета
            font_priority = [
                ('DejaVuSans', 'DejaVuSans-Bold'),
                ('LiberationSans', 'LiberationSans-Bold'),
                ('Arial', 'Arial-Bold'),
                ('Times', 'Times-Bold'),
                ('HeiseiKakuGo-W5', 'HeiseiKakuGo-W5')  # Unicode CID fallback
            ]
            
            for regular, bold in font_priority:
                if regular in registered_fonts:
                    font_name = regular
                    font_bold = bold if bold in registered_fonts else regular
                    print(f"✓ Используется шрифт: {font_name} / {font_bold}")
                    break
        else:
            print("⚠ Используются стандартные шрифты (без поддержки кириллицы)")
            
        print(f"Финальные шрифты: {font_name}, {font_bold}")
        
        # Заголовок
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=24,
            spaceAfter=30,
            alignment=1,  # Центрирование
            fontName=font_bold
        )
        story.append(Paragraph(title, title_style))
        story.append(Spacer(1, 12))
        
        # Report information
        info_style = ParagraphStyle(
            'InfoStyle',
            parent=styles['Normal'],
            fontSize=10,
            spaceAfter=20,
            alignment=1,
            fontName=font_name
        )
        story.append(Paragraph(f"<b>Author:</b> {author}", info_style))
        story.append(Paragraph(f"<b>Created:</b> {datetime.now().strftime('%Y-%m-%d %H:%M')}", info_style))
        story.append(Paragraph(f"<b>Total Records:</b> {len(df):,}", info_style))
        story.append(Spacer(1, 20))
        
        # Main metrics
        if include_funnel:
            story.append(Paragraph("Main Funnel Metrics", styles['Heading2']))
            
            metrics = self.calculate_funnel_metrics(df)
            
            # Metrics table
            data = [
                ['Stage', 'Count', 'Conversion'],
                ['Registration', f"{metrics['counts']['registrations']:,}", "100.0%"],
                ['Deposit', f"{metrics['counts']['deposits']:,}", f"{metrics['conversions']['reg_to_deposit']:.1f}%"],
                ['First Bet', f"{metrics['counts']['first_bets']:,}", f"{metrics['conversions']['deposit_to_bet']:.1f}%"],
                ['Second Deposit', f"{metrics['counts']['second_deposits']:,}", f"{metrics['conversions']['bet_to_second_deposit']:.1f}%"]
            ]
            
            table = Table(data)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), font_bold),
                    ('FONTNAME', (0, 1), (-1, -1), font_name),
                    ('FONTSIZE', (0, 0), (-1, 0), 14),
                    ('FONTSIZE', (0, 1), (-1, -1), 12),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black)
            ]))
            
            story.append(table)
            story.append(Spacer(1, 20))
        
        # Анализ по сегментам
        if include_segments:
            # Заголовок раздела
            section_style = ParagraphStyle(
                'SectionStyle',
                parent=styles['Heading2'],
                fontSize=16,
                spaceAfter=12,
                spaceBefore=20,
                fontName=font_bold
            )
            story.append(Paragraph("Segment Analysis", section_style))
            
            segment_analysis = self.analyze_by_segments(df)
            
            for segment_name, segment_df in segment_analysis.items():
                story.append(Paragraph(f"By {segment_name}:", styles['Heading3']))
                
                # Top-3 segments by conversion
                top_segments = segment_df.nlargest(3, 'reg_to_deposit_conv')
                
                for _, row in top_segments.iterrows():
                    story.append(Paragraph(
                        f"• {row['segment_value']}: {row['reg_to_deposit_conv']:.1f}% ({row['users']} users)",
                        styles['Normal']
                    ))
                
                story.append(Spacer(1, 12))
        
        # Recommendations
        story.append(Paragraph("Recommendations", styles['Heading2']))
        
        metrics = self.calculate_funnel_metrics(df)
        recommendations = []
        
        if metrics['conversions']['reg_to_deposit'] < 20:
            recommendations.append("• Low deposit conversion rate. Consider improving onboarding and bonus programs.")
        
        if metrics['conversions']['deposit_to_bet'] < 80:
            recommendations.append("• Low first bet conversion rate. Review the betting process UX.")
        
        if metrics['conversions']['bet_to_second_deposit'] < 30:
            recommendations.append("• Low second deposit conversion rate. Improve retention mechanics.")
        
        if not recommendations:
            recommendations.append("• All funnel metrics are within normal ranges.")
        
        # Style for recommendations
        rec_style = ParagraphStyle(
            'RecStyle',
            parent=styles['Normal'],
            fontName=font_name
        )
        
        for rec in recommendations:
            story.append(Paragraph(rec, rec_style))
        
        # Сборка документа
        doc.build(story)
        buffer.seek(0)
        
        return buffer

def detect_anomalies(df, threshold=0.5):
    """Детекция аномалий в воронке конверсий"""
    anomalies = []
    
    # Анализ по дням
    df['reg_date'] = pd.to_datetime(df['registration_time']).dt.date
    daily_stats = []
    
    for date in sorted(df['reg_date'].unique()):
        if pd.isna(date):
            continue
            
        day_df = df[df['reg_date'] == date]
        
        registrations = len(day_df)
        deposits = len(day_df[day_df['deposit_time'].notna()])
        
        conv_rate = (deposits / registrations * 100) if registrations > 0 else 0
        
        daily_stats.append({
            'date': date,
            'registrations': registrations,
            'deposits': deposits,
            'conv_rate': conv_rate
        })
    
    daily_df = pd.DataFrame(daily_stats)
    
    if len(daily_df) < 2:
        return anomalies
    
    # Проверка резких падений конверсии
    for i in range(1, len(daily_df)):
        current_conv = daily_df.iloc[i]['conv_rate']
        prev_conv = daily_df.iloc[i-1]['conv_rate']
        
        if prev_conv > 0:
            change = (current_conv - prev_conv) / prev_conv
            
            if abs(change) > threshold:
                direction = "упала" if change < 0 else "выросла"
                anomalies.append(
                    f"Конверсия в депозит {direction} на {abs(change)*100:.1f}% "
                    f"({daily_df.iloc[i]['date']})"
                )
    
    # Проверка аномально низких объемов регистраций
    if len(daily_df) >= 7:
        avg_registrations = daily_df['registrations'].mean()
        std_registrations = daily_df['registrations'].std()
        
        for _, row in daily_df.iterrows():
            if row['registrations'] < (avg_registrations - 2 * std_registrations):
                anomalies.append(
                    f"Аномально низкое количество регистраций: {row['registrations']} "
                    f"({row['date']})"
                )
    
    return anomalies

def calculate_cohort_analysis(df):
    """Когортный анализ (дополнительная функция)"""
    # Группировка по месяцам регистрации
    df['reg_month'] = pd.to_datetime(df['registration_time']).dt.to_period('M')
    df['deposit_month'] = pd.to_datetime(df['deposit_time']).dt.to_period('M')
    
    cohorts = []
    
    for reg_month in df['reg_month'].unique():
        if pd.isna(reg_month):
            continue
            
        cohort_df = df[df['reg_month'] == reg_month]
        
        # Расчет retention по месяцам
        for period in range(0, 6):  # 6 месяцев
            target_month = reg_month + period
            
            retained_users = len(cohort_df[
                (cohort_df['deposit_month'] == target_month) |
                (cohort_df['deposit_month'] < target_month)
            ])
            
            cohorts.append({
                'cohort': str(reg_month),
                'period': period,
                'users': len(cohort_df),
                'retained': retained_users,
                'retention_rate': retained_users / len(cohort_df) * 100
            })
    
    return pd.DataFrame(cohorts)