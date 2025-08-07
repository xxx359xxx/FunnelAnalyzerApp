#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test English PDF report generation
"""

import pandas as pd
from utils import FunnelAnalyzer
from datetime import datetime

# Create test data
test_data = {
    'registration_time': ['2024-01-01 10:00:00', '2024-01-01 11:00:00', '2024-01-01 12:00:00', '2024-01-02 09:00:00', '2024-01-02 10:00:00'],
    'deposit_time': ['2024-01-01 10:30:00', '2024-01-01 11:30:00', None, '2024-01-02 09:30:00', None],
    'first_bet_time': ['2024-01-01 11:00:00', None, None, '2024-01-02 10:00:00', None],
    'second_deposit_time': ['2024-01-03 10:00:00', None, None, None, None],
    'traffic_source': ['email', 'direct', 'referral', 'email', 'direct'],
    'country': ['US', 'UK', 'CA', 'AU', 'DE'],
    'device': ['desktop', 'mobile', 'tablet', 'desktop', 'mobile']
}

df = pd.DataFrame(test_data)

# Create analyzer
analyzer = FunnelAnalyzer(df)

print("Testing English PDF report generation...")
print("=" * 50)

try:
    # Generate PDF report in English
    buffer = analyzer.generate_pdf_report(
        df, 
        title="Gambling Funnel Conversion Analysis",
        author="Data Analyst"
    )
    
    # Save PDF file
    with open('english_funnel_report.pdf', 'wb') as f:
        f.write(buffer.getvalue())
    
    print("\n🎉 English PDF report created successfully!")
    print("📄 File saved as: english_funnel_report.pdf")
    print("\nThe report now contains:")
    print("- Main Funnel Metrics")
    print("- Segment Analysis")
    print("- Recommendations")
    print("- All text in English")
    
except Exception as e:
    print(f"\n❌ Error creating PDF: {e}")
    import traceback
    traceback.print_exc()