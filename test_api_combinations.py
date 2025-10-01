#!/usr/bin/env python3
"""
Comprehensive API Test Suite for Solar Monitor
Tests all time period and granularity combinations
"""

import requests
import json
from datetime import datetime, timedelta
import sys

# API base URL
BASE_URL = "http://192.168.1.126:5000"

# All time periods from the frontend
TIME_PERIODS = [
    '15min', '30min', '1h', '2h', '4h', '6h', '12h',
    'today', '24h', '2d', '3d', 'week',
    'thisweek', 'thismonth', 'thisyear',
    'month', '3months', '6months', 'year'
]

# All granularities from the frontend
GRANULARITIES = [
    'minute', '5min', '15min', 'hour', 'day', 'week', 'month', 'year'
]

def test_api_combination(period, granularity):
    """Test a specific period/granularity combination"""
    url = f"{BASE_URL}/api/historical_data"
    params = {'period': period, 'granularity': granularity}
    
    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()
        
        if not data.get('success'):
            return {
                'period': period,
                'granularity': granularity,
                'status': 'FAILED',
                'error': data.get('error', 'Unknown error'),
                'data_count': 0,
                'timeframe_valid': False
            }
        
        records = data.get('data', [])
        data_count = len(records)
        
        # Validate timeframe if we have data
        timeframe_valid = True
        earliest_time = None
        latest_time = None
        
        if records:
            try:
                timestamps = [datetime.fromisoformat(r['timestamp'].replace('Z', '+00:00')) for r in records]
                earliest_time = min(timestamps)
                latest_time = max(timestamps)
                
                # Basic timeframe validation
                now = datetime.now()
                timeframe_valid = validate_timeframe(period, earliest_time, latest_time, now)
                
            except Exception as e:
                timeframe_valid = False
                print(f"  Timestamp parsing error: {e}")
        
        return {
            'period': period,
            'granularity': granularity,
            'status': 'SUCCESS',
            'data_count': data_count,
            'timeframe_valid': timeframe_valid,
            'earliest': earliest_time.isoformat() if earliest_time else None,
            'latest': latest_time.isoformat() if latest_time else None,
            'error': None
        }
        
    except requests.exceptions.RequestException as e:
        return {
            'period': period,
            'granularity': granularity,
            'status': 'NETWORK_ERROR',
            'error': str(e),
            'data_count': 0,
            'timeframe_valid': False
        }
    except Exception as e:
        return {
            'period': period,
            'granularity': granularity,
            'status': 'ERROR',
            'error': str(e),
            'data_count': 0,
            'timeframe_valid': False
        }

def validate_timeframe(period, earliest, latest, now):
    """Validate that the data falls within the expected timeframe"""
    try:
        # Calculate expected start time based on period
        if period == '15min':
            expected_start = now - timedelta(minutes=15)
        elif period == '30min':
            expected_start = now - timedelta(minutes=30)
        elif period == '1h':
            expected_start = now - timedelta(hours=1)
        elif period == '2h':
            expected_start = now - timedelta(hours=2)
        elif period == '4h':
            expected_start = now - timedelta(hours=4)
        elif period == '6h':
            expected_start = now - timedelta(hours=6)
        elif period == '12h':
            expected_start = now - timedelta(hours=12)
        elif period == '24h':
            expected_start = now - timedelta(hours=24)
        elif period == '2d':
            expected_start = now - timedelta(days=2)
        elif period == '3d':
            expected_start = now - timedelta(days=3)
        elif period == 'week':
            expected_start = now - timedelta(days=7)
        elif period == 'month':
            expected_start = now - timedelta(days=30)
        elif period == '3months':
            expected_start = now - timedelta(days=90)
        elif period == '6months':
            expected_start = now - timedelta(days=180)
        elif period == 'year':
            expected_start = now - timedelta(days=365)
        elif period == 'today':
            expected_start = now.replace(hour=0, minute=0, second=0, microsecond=0)
        elif period in ['thisweek', 'thismonth', 'thisyear']:
            # These are more complex, just check that data is reasonably recent
            expected_start = now - timedelta(days=365)
        else:
            # Unknown period, skip validation
            return True
        
        # Allow some tolerance (data might be slightly outside expected range)
        tolerance = timedelta(minutes=5)
        
        # Check if earliest data is reasonably close to expected start
        if earliest < expected_start - tolerance:
            print(f"    Warning: Data starts too early. Expected: {expected_start}, Got: {earliest}")
            return False
        
        # Check if latest data is not in the future
        if latest > now + tolerance:
            print(f"    Warning: Data in future. Now: {now}, Latest: {latest}")
            return False
        
        return True
        
    except Exception as e:
        print(f"    Timeframe validation error: {e}")
        return False

def main():
    """Run all API combination tests"""
    print("🧪 Solar Monitor API Test Suite")
    print("=" * 50)
    
    total_tests = len(TIME_PERIODS) * len(GRANULARITIES)
    current_test = 0
    results = []
    
    print(f"Testing {total_tests} combinations...")
    print()
    
    for period in TIME_PERIODS:
        print(f"📅 Testing period: {period}")
        
        for granularity in GRANULARITIES:
            current_test += 1
            print(f"  [{current_test:3d}/{total_tests}] {period} + {granularity}... ", end="", flush=True)
            
            result = test_api_combination(period, granularity)
            results.append(result)
            
            # Print result
            if result['status'] == 'SUCCESS':
                status_icon = "✅" if result['timeframe_valid'] else "⚠️"
                print(f"{status_icon} {result['data_count']} records")
                if not result['timeframe_valid']:
                    print(f"      Timeframe validation failed")
            else:
                print(f"❌ {result['status']}: {result['error']}")
        
        print()
    
    # Summary
    print("📊 Test Summary")
    print("=" * 50)
    
    successful = [r for r in results if r['status'] == 'SUCCESS']
    failed = [r for r in results if r['status'] != 'SUCCESS']
    timeframe_valid = [r for r in successful if r['timeframe_valid']]
    timeframe_invalid = [r for r in successful if not r['timeframe_valid']]
    
    print(f"Total Tests: {total_tests}")
    print(f"✅ Successful: {len(successful)} ({len(successful)/total_tests*100:.1f}%)")
    print(f"❌ Failed: {len(failed)} ({len(failed)/total_tests*100:.1f}%)")
    print(f"⚠️  Timeframe Issues: {len(timeframe_invalid)} ({len(timeframe_invalid)/total_tests*100:.1f}%)")
    print()
    
    if failed:
        print("❌ Failed Tests:")
        for result in failed:
            print(f"  {result['period']} + {result['granularity']}: {result['error']}")
        print()
    
    if timeframe_invalid:
        print("⚠️  Timeframe Validation Issues:")
        for result in timeframe_invalid:
            print(f"  {result['period']} + {result['granularity']}: {result['data_count']} records")
        print()
    
    # Data count analysis
    print("📈 Data Count Analysis:")
    data_counts = {}
    for result in successful:
        key = f"{result['period']}+{result['granularity']}"
        data_counts[key] = result['data_count']
    
    # Show some interesting stats
    max_data = max(data_counts.values()) if data_counts else 0
    min_data = min(data_counts.values()) if data_counts else 0
    avg_data = sum(data_counts.values()) / len(data_counts) if data_counts else 0
    
    print(f"  Max records: {max_data}")
    print(f"  Min records: {min_data}")
    print(f"  Avg records: {avg_data:.1f}")
    
    # Export results to JSON
    with open('api_test_results.json', 'w') as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n📄 Detailed results saved to: api_test_results.json")
    
    # Return exit code based on results
    if failed:
        print(f"\n❌ {len(failed)} tests failed!")
        return 1
    elif timeframe_invalid:
        print(f"\n⚠️  {len(timeframe_invalid)} tests have timeframe issues!")
        return 2
    else:
        print(f"\n✅ All {len(successful)} tests passed!")
        return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
