#!/usr/bin/env python3
"""
BTC/USD Historical Data Downloader

This script downloads historical BTC/USD minute price data for the past 90 days
using yfinance and saves it to the data directory as BTCUSD_minute.csv.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path


def download_btc_data():
    """Download BTC/USD minute data for the past 90 days."""
    
    # Ensure data directory exists
    data_dir = Path("data")
    data_dir.mkdir(exist_ok=True)
    
    # Calculate date range (past 90 days)
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    
    print(f"Downloading BTC/USD minute data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}...")
    
    try:
        # Download BTC-USD data with 1-minute interval
        # Note: yfinance uses BTC-USD as the ticker symbol
        btc_ticker = yf.Ticker("BTC-USD")
        
        # Download historical data
        # yfinance supports up to 7 days of 1-minute data in a single request
        # For 90 days, we'll download in chunks and combine
        
        all_data = []
        current_date = start_date
        
        while current_date < end_date:
            # Download 7 days at a time (yfinance limitation for 1m interval)
            chunk_end = min(current_date + timedelta(days=7), end_date)
            
            print(f"  Downloading chunk: {current_date.strftime('%Y-%m-%d')} to {chunk_end.strftime('%Y-%m-%d')}")
            
            try:
                chunk_data = btc_ticker.history(
                    start=current_date,
                    end=chunk_end,
                    interval="1m"
                )
                
                if not chunk_data.empty:
                    all_data.append(chunk_data)
                    
            except Exception as e:
                print(f"  Warning: Failed to download chunk {current_date.strftime('%Y-%m-%d')}: {e}")
            
            current_date = chunk_end
        
        if not all_data:
            print("❌ No data was downloaded. Please check your internet connection and try again.")
            return False
        
        # Combine all chunks
        btc_data = pd.concat(all_data, ignore_index=False)
        
        # Remove duplicates and sort by datetime
        btc_data = btc_data[~btc_data.index.duplicated(keep='first')]
        btc_data = btc_data.sort_index()
        
        # Add some additional columns that might be useful for ML
        btc_data['Returns'] = btc_data['Close'].pct_change()
        btc_data['Price_Range'] = btc_data['High'] - btc_data['Low']
        btc_data['VWAP'] = (btc_data['Volume'] * btc_data['Close']).cumsum() / btc_data['Volume'].cumsum()
        
        # Reset index to make datetime a column
        btc_data.reset_index(inplace=True)
        btc_data.rename(columns={'Datetime': 'timestamp'}, inplace=True)
        
        # Save to CSV
        output_file = data_dir / "BTCUSD_minute.csv"
        btc_data.to_csv(output_file, index=False)
        
        print(f"✅ Successfully downloaded {len(btc_data)} records of BTC/USD minute data")
        print(f"📁 Data saved to: {output_file}")
        print(f"📊 Date range: {btc_data['timestamp'].min()} to {btc_data['timestamp'].max()}")
        print(f"💰 Price range: ${btc_data['Close'].min():.2f} - ${btc_data['Close'].max():.2f}")
        
        # Display basic statistics
        print("\n📈 Basic Statistics:")
        print(f"   Average Price: ${btc_data['Close'].mean():.2f}")
        print(f"   Average Volume: {btc_data['Volume'].mean():.0f}")
        print(f"   Total Records: {len(btc_data)}")
        
        # Show first few rows
        print("\n📋 Sample Data:")
        print(btc_data[['timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']].head())
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading BTC data: {e}")
        return False


def main():
    """Main function to download BTC data."""
    print("BTC/USD Historical Data Downloader")
    print("=" * 50)
    
    # Check if yfinance is available
    try:
        import yfinance
        print("✅ yfinance library is available")
    except ImportError:
        print("❌ yfinance library not found. Please install it with:")
        print("   pip install yfinance")
        return
    
    # Download the data
    success = download_btc_data()
    
    if success:
        print("\n🎉 BTC data download completed successfully!")
        print("\n💡 You can now use this data in your notebooks:")
        print("   import pandas as pd")
        print("   btc_data = pd.read_csv('data/BTCUSD_minute.csv')")
    else:
        print("\n❌ Data download failed. Please check the error messages above.")


if __name__ == "__main__":
    main()
