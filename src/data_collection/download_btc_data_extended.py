#!/usr/bin/env python3
"""
Enhanced BTC/USD Historical Data Downloader

This script downloads historical BTC/USD data with fallback options:
1. Minute data for the last 30 days (Yahoo Finance limitation)
2. Daily data for the full 90-day period
3. Combines both datasets for comprehensive analysis
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path


def download_minute_data(days=30):
    """Download BTC/USD minute data for the specified number of days (max 30 due to Yahoo Finance limits)."""
    
    print(f"📊 Downloading minute-level data for the last {days} days...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        btc_ticker = yf.Ticker("BTC-USD")
        
        # Download minute data in 7-day chunks
        all_data = []
        current_date = start_date
        
        while current_date < end_date:
            chunk_end = min(current_date + timedelta(days=7), end_date)
            
            try:
                chunk_data = btc_ticker.history(
                    start=current_date,
                    end=chunk_end,
                    interval="1m"
                )
                
                if not chunk_data.empty:
                    all_data.append(chunk_data)
                    print(f"  ✅ Downloaded {len(chunk_data)} minute records for {current_date.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}")
                    
            except Exception as e:
                print(f"  ⚠️  Failed to download chunk {current_date.strftime('%Y-%m-%d')}: {e}")
            
            current_date = chunk_end
        
        if all_data:
            minute_data = pd.concat(all_data, ignore_index=False)
            minute_data = minute_data[~minute_data.index.duplicated(keep='first')]
            minute_data = minute_data.sort_index()
            
            # Add analysis columns
            minute_data['Returns'] = minute_data['Close'].pct_change()
            minute_data['Price_Range'] = minute_data['High'] - minute_data['Low']
            minute_data['VWAP'] = (minute_data['Volume'] * minute_data['Close']).cumsum() / minute_data['Volume'].cumsum()
            
            minute_data.reset_index(inplace=True)
            minute_data.rename(columns={'Datetime': 'timestamp'}, inplace=True)
            minute_data['data_type'] = 'minute'
            
            return minute_data
        
    except Exception as e:
        print(f"❌ Error downloading minute data: {e}")
    
    return None


def download_daily_data(days=90):
    """Download BTC/USD daily data for the specified number of days."""
    
    print(f"📈 Downloading daily data for the last {days} days...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    try:
        btc_ticker = yf.Ticker("BTC-USD")
        
        daily_data = btc_ticker.history(
            start=start_date,
            end=end_date,
            interval="1d"
        )
        
        if not daily_data.empty:
            # Add analysis columns
            daily_data['Returns'] = daily_data['Close'].pct_change()
            daily_data['Price_Range'] = daily_data['High'] - daily_data['Low']
            daily_data['VWAP'] = (daily_data['Volume'] * daily_data['Close']).cumsum() / daily_data['Volume'].cumsum()
            
            daily_data.reset_index(inplace=True)
            daily_data.rename(columns={'Date': 'timestamp'}, inplace=True)
            daily_data['data_type'] = 'daily'
            
            print(f"  ✅ Downloaded {len(daily_data)} daily records")
            return daily_data
        
    except Exception as e:
        print(f"❌ Error downloading daily data: {e}")
    
    return None


def save_data(data, filename, data_dir):
    """Save data to CSV file."""
    if data is not None and not data.empty:
        output_file = data_dir / filename
        data.to_csv(output_file, index=False)
        
        print(f"📁 Data saved to: {output_file}")
        print(f"📊 Records: {len(data)}")
        print(f"📅 Date range: {data['timestamp'].min()} to {data['timestamp'].max()}")
        if 'Close' in data.columns:
            print(f"💰 Price range: ${data['Close'].min():.2f} - ${data['Close'].max():.2f}")
            print(f"💵 Average price: ${data['Close'].mean():.2f}")
        
        return True
    return False


def create_summary_report(minute_data, daily_data, data_dir):
    """Create a summary report of the downloaded data."""
    
    report_file = data_dir / "data_summary.txt"
    
    with open(report_file, 'w') as f:
        f.write("BTC/USD Historical Data Download Summary\n")
        f.write("=" * 50 + "\n")
        f.write(f"Download Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        
        if minute_data is not None:
            f.write("MINUTE DATA:\n")
            f.write(f"  Records: {len(minute_data)}\n")
            f.write(f"  Date Range: {minute_data['timestamp'].min()} to {minute_data['timestamp'].max()}\n")
            f.write(f"  Price Range: ${minute_data['Close'].min():.2f} - ${minute_data['Close'].max():.2f}\n")
            f.write(f"  Average Price: ${minute_data['Close'].mean():.2f}\n")
            f.write(f"  File: BTCUSD_minute.csv\n\n")
        
        if daily_data is not None:
            f.write("DAILY DATA:\n")
            f.write(f"  Records: {len(daily_data)}\n")
            f.write(f"  Date Range: {daily_data['timestamp'].min()} to {daily_data['timestamp'].max()}\n")
            f.write(f"  Price Range: ${daily_data['Close'].min():.2f} - ${daily_data['Close'].max():.2f}\n")
            f.write(f"  Average Price: ${daily_data['Close'].mean():.2f}\n")
            f.write(f"  File: BTCUSD_daily.csv\n\n")
        
        f.write("USAGE:\n")
        f.write("  # Load minute data (if available)\n")
        f.write("  import pandas as pd\n")
        f.write("  minute_data = pd.read_csv('data/BTCUSD_minute.csv')\n\n")
        f.write("  # Load daily data\n")
        f.write("  daily_data = pd.read_csv('data/BTCUSD_daily.csv')\n\n")
        f.write("  # Convert timestamp column to datetime\n")
        f.write("  minute_data['timestamp'] = pd.to_datetime(minute_data['timestamp'])\n")
        f.write("  daily_data['timestamp'] = pd.to_datetime(daily_data['timestamp'])\n")
    
    print(f"📄 Summary report saved to: {report_file}")


def main():
    """Main function to download comprehensive BTC data."""
    print("Enhanced BTC/USD Historical Data Downloader")
    print("=" * 60)
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Check if yfinance is available
    try:
        import yfinance
        print("✅ yfinance library is available")
    except ImportError:
        print("❌ yfinance library not found. Please install it with:")
        print("   pip install yfinance")
        return
    
    print("\nDownloading BTC/USD data with multiple timeframes...")
    print("Note: Yahoo Finance limits minute data to the last 30 days\n")
    
    # Download minute data (last 30 days)
    minute_data = download_minute_data(30)
    
    # Download daily data (last 90 days)
    daily_data = download_daily_data(90)
    
    # Save the data
    minute_saved = False
    daily_saved = False
    
    if minute_data is not None:
        print("\n📊 MINUTE DATA SUMMARY:")
        minute_saved = save_data(minute_data, "BTCUSD_minute.csv", data_dir)
        
        # Show sample data
        print("\n📋 Sample Minute Data:")
        print(minute_data[['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']].head())
    
    if daily_data is not None:
        print("\n📈 DAILY DATA SUMMARY:")
        daily_saved = save_data(daily_data, "BTCUSD_daily.csv", data_dir)
        
        # Show sample data
        print("\n📋 Sample Daily Data:")
        print(daily_data[['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']].head())
    
    # Create summary report
    if minute_saved or daily_saved:
        create_summary_report(minute_data, daily_data, data_dir)
        
        print("\n🎉 Data download completed successfully!")
        print("\n💡 Available datasets:")
        if minute_saved:
            print("   • Minute-level data: data/BTCUSD_minute.csv")
        if daily_saved:
            print("   • Daily data: data/BTCUSD_daily.csv")
        print("   • Summary report: data/data_summary.txt")
        
        print("\n📖 Quick start:")
        print("   import pandas as pd")
        if daily_saved:
            print("   daily_data = pd.read_csv('data/BTCUSD_daily.csv')")
        if minute_saved:
            print("   minute_data = pd.read_csv('data/BTCUSD_minute.csv')")
    else:
        print("\n❌ No data was successfully downloaded.")


if __name__ == "__main__":
    main()
