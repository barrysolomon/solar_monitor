# Quick Start Guide

**Get your SunPower local monitoring up and running in just a few hours!**

## 🚀 Quick Start

### Option 1: Raspberry Pi Setup (RECOMMENDED)
**Total Time: 2-3 hours | Cost: ~$100 | Difficulty: Medium**

#### Step 1: Buy Hardware (15 minutes)
- Raspberry Pi 4 (4GB) - $65
- 32GB MicroSD card - $10  
- Power supply - $10
- Ethernet cable (25-50 feet) - $15-25
- Case - $10
- **Total: ~$110**

#### Step 2: Set Up Raspberry Pi (30 minutes)
1. Download Raspberry Pi Imager
2. Flash SD card with Raspberry Pi OS Lite
3. Enable SSH and set password
4. Boot Pi and find it on your network

#### Step 3: Connect to Your PVS Gateway (45 minutes)
1. Run Ethernet cable from outdoor PVS6 to your garage/house
2. Connect cable to PVS6 "LAN" or "Installer" port
3. Configure Pi network settings
4. Test connection: `ping 172.27.153.1`

#### Step 4: Install Software (30 minutes)
1. Copy this code to your Pi
2. Install Python dependencies
3. Configure the application
4. Test: `python3 solar_monitor.py --test-connection`

#### Step 5: Access Your Dashboard (5 minutes)
- Open web browser
- Go to `http://YOUR_PI_IP:5000`
- See your solar data in real-time!

**That's it! You now have local solar monitoring.**

*See [PROJECT_SETUP.md](RASPBERRY_PI_SETUP.md) for detailed instructions*

---

### Option 2: Desktop Computer Setup
**Total Time: 1-2 hours | Cost: ~$8 | Difficulty: Easy**

#### Step 1: Find Hardware (5 minutes)
- Old WiFi router with Ethernet ports - $0 (you already own this!)
- Ethernet cable (10-25 feet) - ~$8
- Your computer - $0 (you already own this!)
- **Total: ~$8**

#### Step 2: Set Up Router Bridge (30 minutes)
1. Connect PVS6 BLUE port to router WAN port via Ethernet
2. Power on router and connect to its WiFi (temporarily)
3. Access router web interface (usually 192.168.1.1)
4. Configure router WiFi to connect to your home network
5. **Important**: Your computer stays connected to your normal home WiFi

#### Step 3: Install Software (45 minutes)
1. Install Python 3.7+ on your computer
2. Download the solar monitoring software
3. Install dependencies: `pip install -r requirements.txt`
4. Test PVS6 connection: `python solar_monitor.py --test-connection`

#### Step 4: Run Monitoring Software (30 minutes)
1. Start data collection: `python solar_monitor.py --mode collector`
2. Start web dashboard: `python solar_monitor.py --mode dashboard`
3. Access dashboard at http://localhost:5000
4. Verify data collection and charts

#### Step 5: Set Up Auto-Start (Optional)
1. Configure as Windows service, macOS launchd, or Linux systemd
2. Set up automatic startup on computer boot
3. Monitor logs and performance

**🎉 Congratulations! You now have local solar monitoring for just $8!**

*See [DESKTOP_SETUP.md](DESKTOP_SETUP.md) for detailed instructions*

## 📚 Need More Help?

### Detailed Guides
- **[PROJECT_SETUP.md](PROJECT_SETUP.md)** - Complete Raspberry Pi setup guide
- **[DESKTOP_SETUP.md](DESKTOP_SETUP.md)** - Complete desktop computer setup guide
- **[APPROACH_COMPARISON.md](APPROACH_COMPARISON.md)** - Compare all setup options

### Hardware & Network
- **[HARDWARE_CHECKLIST.md](HARDWARE_CHECKLIST.md)** - Detailed shopping list
- **[NETWORK_SETUP.md](NETWORK_SETUP.md)** - Network configuration help
- **[PVS6_PORTS_GUIDE.md](PVS6_PORTS_GUIDE.md)** - Understanding PVS6 ports

### Troubleshooting
- **[FAQ.md](FAQ.md)** - Frequently asked questions
- **[BEGINNER_GUIDE.md](BEGINNER_GUIDE.md)** - Non-technical user guide

## ⚠️ Important Notes

### PVS6 Port Usage
- **Always use the BLUE port** (LAN/Installer) on your PVS6
- **Never use the WHITE port** (WAN/Internet) for local monitoring
- The BLUE port provides full API access to solar data

### Network Requirements
- PVS6 creates an isolated network (172.27.153.x)
- You need a bridge (Pi or router) to access it from your home network
- Direct WiFi connection to PVS6 won't work for monitoring

### Cost Comparison
- **Raspberry Pi**: ~$100 (dedicated device, most reliable)
- **Desktop Computer**: ~$8 (uses existing hardware, budget option)
- **See APPROACH_COMPARISON.md for complete analysis**

## 🎯 Quick Decision Guide

### Choose Raspberry Pi If:
- You want a **dedicated monitoring device**
- You want **maximum reliability** and 24/7 operation
- You're comfortable with **basic Linux commands**
- You want **professional, clean setup**

### Choose Desktop Computer If:
- You want to **save money** (~$92 savings)
- You want **quickest setup** (1-2 hours vs 2-3 hours)
- You're comfortable with **Python and software installation**
- You want to **use existing hardware**

## 🚀 Ready to Start?

1. **Choose your approach** (Pi recommended, Desktop for budget)
2. **Follow the steps** above for your chosen approach
3. **Reference detailed guides** if you need help
4. **Enjoy your local solar monitoring!**

**Need help?** Check the [FAQ](FAQ.md) or [Beginner Guide](BEGINNER_GUIDE.md) for additional support.
