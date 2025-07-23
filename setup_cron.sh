#!/bin/bash
"""
Setup script for daily BTC data updates using cron.

This script helps you set up automatic daily updates for your BTC price data.
"""

# Get the absolute path to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PYTHON_PATH="$PROJECT_DIR/.venv/bin/python"
UPDATE_SCRIPT="$PROJECT_DIR/update_data.py"

echo "🔧 BTC Data Auto-Update Setup"
echo "================================"
echo "Project directory: $PROJECT_DIR"
echo "Python path: $PYTHON_PATH"
echo "Update script: $UPDATE_SCRIPT"
echo

# Check if virtual environment exists
if [ ! -f "$PYTHON_PATH" ]; then
    echo "❌ Virtual environment not found at $PYTHON_PATH"
    echo "Please run 'python -m venv .venv' and install requirements first."
    exit 1
fi

# Check if update script exists
if [ ! -f "$UPDATE_SCRIPT" ]; then
    echo "❌ Update script not found at $UPDATE_SCRIPT"
    exit 1
fi

echo "✅ All required files found!"
echo

# Create the cron job command
CRON_COMMAND="0 9 * * * cd $PROJECT_DIR && $PYTHON_PATH $UPDATE_SCRIPT >> $PROJECT_DIR/logs/data_update.log 2>&1"

echo "📅 Suggested cron job (runs daily at 9 AM):"
echo "$CRON_COMMAND"
echo

# Create logs directory
mkdir -p "$PROJECT_DIR/logs"

echo "📝 To set up the cron job, run:"
echo "1. Open crontab: crontab -e"
echo "2. Add this line:"
echo "   $CRON_COMMAND"
echo "3. Save and exit"
echo

echo "📋 Alternative: Run this command to add the cron job automatically:"
echo "(echo '$CRON_COMMAND') | crontab -"
echo

echo "💡 Tips:"
echo "- Check logs at: $PROJECT_DIR/logs/data_update.log"
echo "- Test manually: python $UPDATE_SCRIPT"
echo "- View current cron jobs: crontab -l"
echo "- Remove cron job: crontab -e (then delete the line)"
