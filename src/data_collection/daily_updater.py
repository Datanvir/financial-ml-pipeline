#!/usr/bin/env python3
"""
Daily BTC/USD Data Updater

This script can be run daily to update BTC/USD price data.
It checks for existing data and only downloads new records to avoid duplicates.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import os
from pathlib import Path
import sys


def get_latest_data_date(csv_file):
    """Get the latest date from existing CSV file."""
    try:
        if csv_file.exists():
            df = pd.read_csv(csv_file)
            if not df.empty and 'timestamp' in df.columns:
                # Convert timestamp to datetime and get the latest
                df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
                return df['timestamp'].max()
    except Exception as e:
        print(f"Warning: Could not read existing data: {e}")
    return None


def download_incremental_data(csv_file, interval="1m", days_back=7):
    """Download new data since the last recorded date."""
    
    print(f"Checking for updates to {csv_file.name}...")
    
    # Get the latest date from existing data
    latest_date = get_latest_data_date(csv_file)
    
    # Set start date
    if latest_date:
        # Start from the last recorded date (with small overlap to ensure continuity)
        start_date = latest_date - timedelta(hours=1)
        # Make start_date timezone-naive for yfinance compatibility
        if start_date.tzinfo is not None:
            start_date = start_date.replace(tzinfo=None)
        print(f"Latest data found: {latest_date}")
        print(f"Updating from: {start_date}")
    else:
        # No existing data, download last few days
        start_date = datetime.now() - timedelta(days=days_back)
        print(f"No existing data found. Downloading last {days_back} days from: {start_date}")
    
    end_date = datetime.now()
    
    try:
        btc_ticker = yf.Ticker("BTC-USD")
        
        print(f"Downloading {interval} data from {start_date.strftime('%Y-%m-%d %H:%M')} to {end_date.strftime('%Y-%m-%d %H:%M')}...")
        
        # For minute data, we need to download in chunks due to yfinance limitations
        if interval == "1m":
            all_data = []
            current_date = start_date
            
            while current_date < end_date:
                # Download 7 days at a time for minute data
                chunk_end = min(current_date + timedelta(days=7), end_date)
                
                try:
                    chunk_data = btc_ticker.history(
                        start=current_date,
                        end=chunk_end,
                        interval=interval
                    )
                    
                    if not chunk_data.empty:
                        all_data.append(chunk_data)
                        
                except Exception as e:
                    print(f"Warning: Failed to download chunk {current_date.strftime('%Y-%m-%d')}: {e}")
                
                current_date = chunk_end
            
            if all_data:
                new_data = pd.concat(all_data, ignore_index=False)
            else:
                print("No new data available.")
                return False
        else:
            # For daily data, we can download larger chunks
            new_data = btc_ticker.history(
                start=start_date,
                end=end_date,
                interval=interval
            )
        
        if new_data.empty:
            print("No new data available.")
            return False
        
        # Process new data
        new_data = new_data[~new_data.index.duplicated(keep='first')]
        new_data = new_data.sort_index()
        
        # Add calculated columns
        new_data['Returns'] = new_data['Close'].pct_change()
        new_data['Price_Range'] = new_data['High'] - new_data['Low']
        new_data['VWAP'] = (new_data['Volume'] * new_data['Close']).cumsum() / new_data['Volume'].cumsum()
        
        # Reset index to make datetime a column
        new_data.reset_index(inplace=True)
        if 'Datetime' in new_data.columns:
            new_data.rename(columns={'Datetime': 'timestamp'}, inplace=True)
        elif 'Date' in new_data.columns:
            new_data.rename(columns={'Date': 'timestamp'}, inplace=True)
        
        # Handle existing data
        if csv_file.exists() and latest_date:
            # Load existing data
            existing_data = pd.read_csv(csv_file)
            existing_data['timestamp'] = pd.to_datetime(existing_data['timestamp'], utc=True)
            new_data['timestamp'] = pd.to_datetime(new_data['timestamp'], utc=True)
            
            # Remove any overlap (keep existing data for overlapping timestamps)
            new_data = new_data[new_data['timestamp'] > latest_date]
            
            if new_data.empty:
                print("✅ Data is already up to date!")
                return True
            
            # Combine data
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
            combined_data = combined_data.drop_duplicates(subset=['timestamp'], keep='first')
            combined_data = combined_data.sort_values('timestamp').reset_index(drop=True)
        else:
            combined_data = new_data
        
        # Save updated data
        combined_data.to_csv(csv_file, index=False)
        
        print(f"✅ Successfully added {len(new_data)} new records")
        print(f"📁 Updated file: {csv_file}")
        print(f"📊 Total records: {len(combined_data)}")
        print(f"📅 Date range: {combined_data['timestamp'].min()} to {combined_data['timestamp'].max()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error updating data: {e}")
        return False


def update_all_data():
    """Update both minute and daily data."""
    
    # Ensure data directory exists
    data_dir = Path("../../data")  # Relative to src/data_collection
    if not data_dir.exists():
        data_dir = Path("data")  # If running from root
    data_dir.mkdir(exist_ok=True)
    
    print("BTC/USD Data Updater")
    print("=" * 50)
    
    success_count = 0
    
    # Update minute data (last 7 days to ensure we get recent data)
    minute_file = data_dir / "BTCUSD_minute.csv"
    if download_incremental_data(minute_file, interval="1m", days_back=7):
        success_count += 1
    
    print()
    
    # Update daily data (last 30 days)
    daily_file = data_dir / "BTCUSD_daily.csv"
    if download_incremental_data(daily_file, interval="1d", days_back=30):
        success_count += 1
    
    print()
    print(f"Update complete! {success_count}/2 datasets updated successfully.")
    
    if success_count == 2:
        print("\n🎉 All data is up to date!")
        print("\n💡 Tip: You can run this script daily to keep your data current:")
        print("   python src/data_collection/daily_updater.py")
        print("\n📅 Consider setting up a daily cron job for automatic updates!")
    
    return success_count == 2


def main():
    """Main function."""
    # Check if yfinance is available
    try:
        import yfinance
        print("✅ yfinance library is available")
    except ImportError:
        print("❌ yfinance library not found. Please install it with:")
        print("   pip install yfinance")
        return
    
    update_all_data()


if __name__ == "__main__":
    main()
