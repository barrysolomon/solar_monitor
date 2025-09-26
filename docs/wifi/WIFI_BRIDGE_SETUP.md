# WiFi Bridge Setup - Using Existing Cat5 Cable

## 🔌 Your Proposed Setup

### **Current PVS6 Connection:**
```
PVS6 Box (Outside) ←→ Cat5 Cable ←→ Router (Inside)
```

### **Your WiFi Bridge Solution:**
```
PVS6 Box (Outside) ←→ Cat5 Cable ←→ WiFi Dongle ←→ WiFi ←→ Home Router
```

## 🎯 How This Would Work

### **Physical Setup:**
1. **Find the Cat5 cable** running from PVS6 to inside
2. **Cut the cable** at a convenient location (inside the house)
3. **Install WiFi dongle** at the cut point
4. **Connect both ends** to the dongle's Ethernet ports
5. **Configure dongle** to bridge WiFi to Ethernet

### **Network Flow:**
```
PVS6 (172.27.153.1) 
    ↓ Ethernet
WiFi Dongle (Bridge Mode)
    ↓ WiFi
Home Router (192.168.1.1)
    ↓ WiFi/Ethernet
Monitoring System (192.168.1.100)
```

## 🔧 Required Hardware

### **WiFi Bridge Device Options:**

#### **1. TP-Link AC750 WiFi Bridge**
- **Model**: TL-WA850RE
- **Ethernet ports**: 1 (need 2 for your setup)
- **Size**: 2.4" x 1.6" x 0.8"
- **Price**: $15-25
- **Issue**: Only 1 Ethernet port

#### **2. GL.iNet GL-MT300N-V2 (Mango)**
- **Model**: GL-MT300N-V2
- **Ethernet ports**: 1 (need 2 for your setup)
- **Size**: 2.2" x 1.4" x 0.6"
- **Price**: $20-30
- **Issue**: Only 1 Ethernet port

#### **3. TP-Link AC600 WiFi Bridge**
- **Model**: TL-WA860RE
- **Ethernet ports**: 1 (need 2 for your setup)
- **Size**: 2.8" x 1.8" x 0.9"
- **Price**: $12-20
- **Issue**: Only 1 Ethernet port

## ⚠️ **Problem: Most WiFi Dongles Only Have 1 Ethernet Port**

### **What You Need:**
- **2 Ethernet ports** - One for PVS6, one for router
- **WiFi capability** - To connect to home network
- **Bridge mode** - To pass traffic between Ethernet and WiFi

### **What Most Dongles Have:**
- **1 Ethernet port** - Only one connection
- **WiFi capability** - Can connect to home network
- **Bridge mode** - But only for one Ethernet connection

## 💡 **Alternative Solutions**

### **Option 1: Use a Small Router**
- **TP-Link AC750 Router** - Has 4 Ethernet ports
- **Size**: 6.3" x 4.1" x 1.1" (larger but still small)
- **Price**: $30-50
- **Setup**: Configure as bridge mode

### **Option 2: Use a WiFi Extender with Ethernet**
- **TP-Link AC750 Extender** - Has Ethernet port
- **Size**: 3.9" x 2.6" x 1.1"
- **Price**: $25-35
- **Setup**: Connect PVS6 to Ethernet, bridge to WiFi

### **Option 3: Use a Small Switch + WiFi Dongle**
- **5-port Ethernet switch** - $10-15
- **WiFi dongle** - $15-25
- **Total cost**: $25-40
- **Setup**: More complex but flexible

## 🔍 **Recommended Solution: TP-Link AC750 Extender**

### **Why This Works:**
- **Ethernet port** - Connect PVS6 cable
- **WiFi capability** - Connect to home network
- **Bridge mode** - Pass traffic between Ethernet and WiFi
- **Small size** - Can fit in small space
- **Easy setup** - Simple configuration

### **Setup Process:**
1. **Cut Cat5 cable** at convenient location inside
2. **Connect PVS6 end** to extender's Ethernet port
3. **Connect router end** to extender's Ethernet port (if needed)
4. **Configure extender** to bridge mode
5. **Connect to home WiFi** - Extender joins home network
6. **Test connection** - Verify PVS6 is accessible

## 🛠️ **Installation Guide**

### **Step 1: Locate Cat5 Cable**
- **Find cable** running from PVS6 to inside
- **Identify cut point** - Inside house, accessible location
- **Measure cable** - Ensure enough length for connections

### **Step 2: Prepare Cable**
- **Cut cable** at chosen location
- **Strip ends** - Expose wires for connection
- **Test continuity** - Verify cable is working

### **Step 3: Install WiFi Bridge**
- **Mount extender** - Secure in location
- **Connect PVS6 end** - To extender's Ethernet port
- **Connect router end** - To extender's Ethernet port (if needed)
- **Power extender** - Connect to power source

### **Step 4: Configure Bridge**
- **Access extender** - Via web interface
- **Set bridge mode** - Enable Ethernet to WiFi bridging
- **Connect to WiFi** - Join home network
- **Test connection** - Verify PVS6 accessibility

## 📊 **Network Architecture**

### **Before (Direct Connection):**
```
PVS6 (172.27.153.1) ←→ Cat5 ←→ Router (192.168.1.1)
```

### **After (WiFi Bridge):**
```
PVS6 (172.27.153.1) 
    ↓ Ethernet
WiFi Bridge (192.168.1.100)
    ↓ WiFi
Home Router (192.168.1.1)
    ↓ WiFi/Ethernet
Monitoring System (192.168.1.101)
```

## 💰 **Cost Analysis**

### **WiFi Bridge Solution:**
| Component | Cost | Notes |
|-----------|------|-------|
| **WiFi Extender** | $25-35 | TP-Link AC750 |
| **Installation** | $0-20 | DIY or professional |
| **Total Cost** | $25-55 | Much cheaper than cables |

### **vs. Other Solutions:**
| Solution | Cost | Pros | Cons |
|----------|------|------|------|
| **WiFi Bridge** | $25-55 | No new cables, easy install | WiFi dependency |
| **New Ethernet** | $50-150 | Reliable, fast | Cables, installation |
| **Powerline** | $80-120 | Uses existing wiring | Electrical interference |

## 🎯 **Recommendations**

### **Best Choice: TP-Link AC750 Extender**
- **Model**: TL-WA850RE or TL-WA860RE
- **Features**: Ethernet port, WiFi bridge mode
- **Size**: Small enough for most locations
- **Price**: $25-35
- **Setup**: Easy configuration

### **Alternative: Small Router**
- **Model**: TP-Link AC750 Router
- **Features**: 4 Ethernet ports, WiFi bridge
- **Size**: Larger but more flexible
- **Price**: $30-50
- **Setup**: More complex but powerful

## ⚠️ **Important Considerations**

### **Cable Management:**
- **Cut location** - Choose accessible spot
- **Cable length** - Ensure enough for connections
- **Protection** - Protect cut ends from damage
- **Labeling** - Mark which end goes where

### **Power Requirements:**
- **Extender power** - Needs 5V/1A adapter
- **Power location** - Near cut point
- **Backup power** - Consider UPS for reliability

### **Network Configuration:**
- **IP conflicts** - Avoid duplicate IPs
- **Subnet routing** - Ensure proper routing
- **Firewall rules** - Allow PVS6 access
- **Testing** - Verify end-to-end connectivity

---

**Your idea is solid! Using the existing Cat5 cable with a WiFi bridge eliminates the need for new cables while providing a clean, professional solution. The TP-Link AC750 extender is probably your best bet for this setup.**
