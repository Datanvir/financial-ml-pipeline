# Financial ML Pipeline

A comprehensive machine learning pipeline for cryptocurrency price prediction and analysis, focused on BTC/USD data.

## 🚀 Quick Start

### 1. Setup Environment
```bash
# Activate virtual environment
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Download Initial Data
```bash
# Download historical data (initial setup)
python src/data_collection/download_btc_data_extended.py

# Or for daily updates
python update_data.py
```

### 3. Set Up Daily Updates (Optional)
```bash
# Setup automatic daily updates
./setup_cron.sh
```

## 📁 Project Structure

```
financial-ml-pipeline/
├── src/
│   ├── data_collection/     # Data download and update scripts
│   ├── features/           # Feature engineering modules
│   ├── models/            # ML model implementations
│   └── utils/             # Utility functions
├── data/                  # Downloaded datasets
├── notebooks/             # Jupyter notebooks for analysis
├── reports/              # Generated reports and outputs
└── logs/                 # Application logs
```

## 📊 Available Data

- **Minute-level data**: Last 30 days of BTC/USD prices (Yahoo Finance limit)
- **Daily data**: Last 90 days of BTC/USD prices
- **Features**: OHLCV data + calculated indicators (Returns, Price Range, VWAP)

### Data Files
- `data/BTCUSD_minute.csv` - Minute-level price data
- `data/BTCUSD_daily.csv` - Daily price data
- `data/data_summary.txt` - Dataset statistics and info

## 🔄 Daily Updates

The pipeline supports incremental daily updates:

```bash
# Manual update
python update_data.py

# Check what data you have
python -c "
import pandas as pd
minute_data = pd.read_csv('data/BTCUSD_minute.csv')
daily_data = pd.read_csv('data/BTCUSD_daily.csv')
print(f'Minute data: {len(minute_data)} records, latest: {minute_data.timestamp.max()}')
print(f'Daily data: {len(daily_data)} records, latest: {daily_data.timestamp.max()}')
"
```

### Automatic Updates with Cron
```bash
# Set up daily updates at 9 AM
./setup_cron.sh

# Or manually add to crontab:
# 0 9 * * * cd /path/to/project && .venv/bin/python update_data.py >> logs/data_update.log 2>&1
```

## 🛠 Usage Examples

### Load Data in Python
```python
import pandas as pd

# Load minute data
minute_data = pd.read_csv('data/BTCUSD_minute.csv')
minute_data['timestamp'] = pd.to_datetime(minute_data['timestamp'])

# Load daily data
daily_data = pd.read_csv('data/BTCUSD_daily.csv')
daily_data['timestamp'] = pd.to_datetime(daily_data['timestamp'])

print(f"Latest price: ${minute_data['Close'].iloc[-1]:.2f}")
```

### Basic Analysis
```python
# Price statistics
print(f"Price range: ${daily_data['Close'].min():.2f} - ${daily_data['Close'].max():.2f}")
print(f"Average daily return: {daily_data['Returns'].mean()*100:.2f}%")
print(f"Volatility: {daily_data['Returns'].std()*100:.2f}%")
```

## 📈 Next Steps

1. **Feature Engineering**: Add technical indicators (RSI, MACD, Bollinger Bands)
2. **Exploratory Analysis**: Create visualization notebooks
3. **Model Development**: Implement prediction models
4. **Backtesting**: Test strategy performance
5. **Production**: Deploy real-time prediction system

## 🔧 Development

### Adding New Features
```bash
# Add to src/features/
python src/features/technical_indicators.py
```

### Running Tests
```bash
# Add tests and run with pytest
pytest tests/
```

## 📝 Notes

- Yahoo Finance limits minute data to ~30 days per request
- Daily data can go back much further (years)
- Data is automatically deduplicated on updates
- All timestamps are in UTC
- Missing data during market closures is normal

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Add your changes
4. Submit a pull request

## 📄 License

