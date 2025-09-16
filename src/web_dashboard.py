"""
Web dashboard for solar monitoring system
Provides real-time and historical data visualization
"""
from flask import Flask, render_template, jsonify, request
import json
import plotly
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime, timedelta
import config
from database import SolarDatabase
from pvs_client import PVSClient

app = Flask(__name__)
db = SolarDatabase()
pvs_client = PVSClient()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/current_status')
def current_status():
    """Get current system status"""
    try:
        # Get latest system status from database
        status_data = db.get_system_status(hours=1)
        if status_data:
            latest_status = status_data[0]
        else:
            latest_status = {
                'total_production_kw': 0,
                'total_consumption_kw': 0,
                'net_export_kw': 0,
                'system_online': False,
                'pvs_online': False
            }
        
        # Get live data from PVS if available
        try:
            live_summary = pvs_client.get_system_summary()
            latest_status.update(live_summary)
        except:
            pass  # Use database data if live data unavailable
        
        return jsonify(latest_status)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/power_chart')
def power_chart():
    """Get power data for charting"""
    try:
        hours = int(request.args.get('hours', 24))
        data = db.get_latest_data(hours=hours)
        
        if not data:
            return jsonify({'error': 'No data available'}), 404
        
        # Convert to DataFrame for easier processing
        df = pd.DataFrame(data)
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Group by device type and create traces
        traces = []
        device_types = df['device_type'].unique()
        
        colors = ['#2E8B57', '#FF6B6B', '#4ECDC4', '#45B7D1', '#96CEB4', '#FFEAA7']
        
        for i, device_type in enumerate(device_types):
            device_data = df[df['device_type'] == device_type]
            
            trace = go.Scatter(
                x=device_data['timestamp'],
                y=device_data['power_kw'],
                mode='lines+markers',
                name=device_type.replace('_', ' ').title(),
                line=dict(color=colors[i % len(colors)], width=2),
                marker=dict(size=4)
            )
            traces.append(trace)
        
        layout = go.Layout(
            title='Solar Power Production Over Time',
            xaxis=dict(title='Time'),
            yaxis=dict(title='Power (kW)'),
            hovermode='closest',
            showlegend=True,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig = go.Figure(data=traces, layout=layout)
        return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/energy_chart')
def energy_chart():
    """Get energy data for charting"""
    try:
        days = int(request.args.get('days', 7))
        data = db.get_daily_summary(days=days)
        
        if not data:
            return jsonify({'error': 'No data available'}), 404
        
        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'])
        
        trace = go.Bar(
            x=df['date'],
            y=df['daily_energy_kwh'],
            name='Daily Energy Production',
            marker=dict(color='#2E8B57')
        )
        
        layout = go.Layout(
            title='Daily Energy Production',
            xaxis=dict(title='Date'),
            yaxis=dict(title='Energy (kWh)'),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig = go.Figure(data=[trace], layout=layout)
        return jsonify(plotly.utils.PlotlyJSONEncoder().encode(fig))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/system_summary')
def system_summary():
    """Get system summary data"""
    try:
        # Get daily summary for last 30 days
        daily_data = db.get_daily_summary(days=30)
        
        if not daily_data:
            return jsonify({'error': 'No data available'}), 404
        
        df = pd.DataFrame(daily_data)
        
        summary = {
            'total_energy_30_days': df['daily_energy_kwh'].sum(),
            'average_daily_energy': df['daily_energy_kwh'].mean(),
            'peak_daily_energy': df['daily_energy_kwh'].max(),
            'total_days': len(df),
            'last_update': datetime.now().isoformat()
        }
        
        return jsonify(summary)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/devices')
def devices():
    """Get list of devices and their current status"""
    try:
        # Get latest data for each device
        data = db.get_latest_data(hours=1)
        
        if not data:
            return jsonify({'error': 'No device data available'}), 404
        
        # Group by device_id and get latest reading
        devices = {}
        for record in data:
            device_id = record['device_id']
            if device_id not in devices or record['timestamp'] > devices[device_id]['timestamp']:
                devices[device_id] = record
        
        return jsonify(list(devices.values()))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health')
def health():
    """Health check endpoint"""
    try:
        pvs_online = pvs_client.test_connection()
        
        # Check database
        db_status = "OK"
        try:
            db.get_latest_data(hours=1)
        except:
            db_status = "ERROR"
        
        return jsonify({
            'pvs_online': pvs_online,
            'database_status': db_status,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host=config.WEB_HOST, port=config.WEB_PORT, debug=config.DEBUG)
