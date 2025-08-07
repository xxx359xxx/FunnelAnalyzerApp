# Gambling Funnel Analysis Tool

A comprehensive tool for analyzing gambling conversion funnels with interactive Streamlit interface and PDF report generation.

## Features

### 🎯 Core Analytics
- **Funnel Analysis**: Registration → Deposit → First Bet → Second Deposit
- **Conversion Metrics**: Step-by-step conversion rates and drop-off analysis
- **Segment Analysis**: Traffic source, country, and device breakdowns
- **Time-based Analysis**: Conversion timing and patterns

### 📊 Interactive Dashboard
- **Streamlit Web Interface**: User-friendly data upload and visualization
- **Real-time Charts**: Interactive funnel visualizations and metrics
- **Data Upload**: CSV file upload with automatic validation
- **Export Options**: PDF report generation with professional formatting

### 📄 PDF Reports
- **Professional Reports**: Clean, formatted PDF output
- **Multi-language Support**: English reports with proper font handling
- **Comprehensive Analysis**: Funnel metrics, segments, and recommendations
- **Custom Branding**: Configurable titles and author information

## Installation

### Prerequisites
- Python 3.8+
- pip package manager

### Setup
1. Clone this repository:
```bash
git clone <repository-url>
cd gambling-funnel-analysis
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download fonts (optional, for better PDF rendering):
```bash
python download_fonts.py
```

## Usage

### Streamlit Web Interface
1. Start the application:
```bash
streamlit run app.py
```

2. Open your browser and navigate to `http://localhost:8501`

3. Upload your CSV data file with the following columns:
   - `registration_time`: User registration timestamp
   - `deposit_time`: First deposit timestamp (optional)
   - `first_bet_time`: First bet timestamp (optional)
   - `second_deposit_time`: Second deposit timestamp (optional)
   - `traffic_source`: Traffic source (email, direct, referral, etc.)
   - `country`: User country code
   - `device`: Device type (desktop, mobile, tablet)

### Command Line Usage
```python
from utils import FunnelAnalyzer
import pandas as pd

# Load your data
df = pd.read_csv('your_data.csv')

# Create analyzer
analyzer = FunnelAnalyzer(df)

# Generate PDF report
pdf_buffer = analyzer.generate_pdf_report(
    df, 
    title="Gambling Funnel Analysis",
    author="Your Name"
)

# Save report
with open('funnel_report.pdf', 'wb') as f:
    f.write(pdf_buffer.getvalue())
```

## Data Format

Your CSV file should contain the following columns:

| Column | Type | Description | Required |
|--------|------|-------------|----------|
| `registration_time` | datetime | User registration timestamp | Yes |
| `deposit_time` | datetime | First deposit timestamp | No |
| `first_bet_time` | datetime | First bet timestamp | No |
| `second_deposit_time` | datetime | Second deposit timestamp | No |
| `traffic_source` | string | Traffic source identifier | Yes |
| `country` | string | Country code (US, UK, etc.) | Yes |
| `device` | string | Device type (desktop/mobile/tablet) | Yes |

### Example Data
```csv
registration_time,deposit_time,first_bet_time,second_deposit_time,traffic_source,country,device
2024-01-01 10:00:00,2024-01-01 10:30:00,2024-01-01 11:00:00,2024-01-03 10:00:00,email,US,desktop
2024-01-01 11:00:00,2024-01-01 11:30:00,,,direct,UK,mobile
2024-01-01 12:00:00,,,,referral,CA,tablet
```

## Project Structure

```
├── app.py                    # Streamlit web interface
├── utils.py                  # Core analysis functions
├── requirements.txt          # Python dependencies
├── download_fonts.py         # Font download utility
├── generate_mock_data.py     # Test data generator
├── test_english_report.py    # PDF report testing
├── test_fonts.py            # Font system testing
├── run.py                   # Alternative runner
├── fonts/                   # Font files directory
│   ├── DejaVuSans.ttf
│   └── DejaVuSans-Bold.ttf
└── README.md               # This file
```

## Key Metrics

### Funnel Stages
1. **Registration**: Total users who registered
2. **Deposit**: Users who made their first deposit
3. **First Bet**: Users who placed their first bet
4. **Second Deposit**: Users who made a second deposit

### Conversion Rates
- **Registration to Deposit**: % of registered users who deposited
- **Deposit to First Bet**: % of depositors who placed a bet
- **First Bet to Second Deposit**: % of bettors who made a second deposit

### Segment Analysis
- **Traffic Source Performance**: Conversion by acquisition channel
- **Geographic Analysis**: Performance by country
- **Device Analysis**: Mobile vs Desktop vs Tablet performance

## Dependencies

- `streamlit`: Web interface framework
- `pandas`: Data manipulation and analysis
- `plotly`: Interactive visualizations
- `reportlab`: PDF generation
- `requests`: HTTP requests for font downloads

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For questions or issues, please create an issue in the GitHub repository.

---

**Note**: This tool is designed for gambling industry analysis and should be used in compliance with local regulations and responsible gambling practices.