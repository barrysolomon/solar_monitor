# Mobile App Development Guide

## 📱 Complete Development Guide for Solar Monitor Mobile App

This guide provides step-by-step instructions for developing the iOS and Android mobile apps that connect to your Raspberry Pi solar monitoring system.

## 🎯 Project Overview

### **App Name**: Solar Monitor Mobile
### **Platforms**: iOS (iPhone/iPad) and Android (Phone/Tablet)
### **Target Users**: SunPower solar system owners
### **Key Value**: Real-time solar monitoring with offline capability

## 🏗️ Development Setup

### **iOS Development Environment**

#### **Required Software**
- **macOS** (latest version)
- **Xcode 15+** (free from App Store)
- **iOS Simulator** (included with Xcode)
- **Git** for version control

#### **Development Account**
- **Apple Developer Account** ($99/year)
- **App Store Connect** access
- **TestFlight** for beta testing

#### **Project Setup**
```bash
# Create new iOS project
mkdir SolarMonitorMobile
cd SolarMonitorMobile

# Initialize Git repository
git init
git add .
git commit -m "Initial iOS project setup"

# Create Xcode project
# File -> New -> Project -> iOS -> App
# Product Name: Solar Monitor Mobile
# Interface: SwiftUI
# Language: Swift
```

### **Android Development Environment**

#### **Required Software**
- **Android Studio** (free from Google)
- **Java Development Kit (JDK) 17+**
- **Android SDK** (latest version)
- **Git** for version control

#### **Development Account**
- **Google Play Console** ($25 one-time fee)
- **Google Play Developer** account
- **Firebase** for analytics and notifications

#### **Project Setup**
```bash
# Create new Android project
mkdir SolarMonitorMobile
cd SolarMonitorMobile

# Initialize Git repository
git init
git add .
git commit -m "Initial Android project setup"

# Create Android project
# File -> New -> New Project -> Empty Activity
# Name: Solar Monitor Mobile
# Language: Kotlin
# Minimum SDK: API 24 (Android 7.0)
```

## 📊 App Architecture

### **iOS App Structure (SwiftUI)**
```
SolarMonitorMobile/
├── SolarMonitorMobile/
│   ├── Models/
│   │   ├── SolarData.swift
│   │   ├── DeviceInfo.swift
│   │   ├── Alert.swift
│   │   └── Settings.swift
│   ├── Views/
│   │   ├── ContentView.swift
│   │   ├── DashboardView.swift
│   │   ├── ChartsView.swift
│   │   ├── DevicesView.swift
│   │   ├── SettingsView.swift
│   │   └── Components/
│   │       ├── PowerCard.swift
│   │       ├── ChartView.swift
│   │       └── StatusIndicator.swift
│   ├── ViewModels/
│   │   ├── DashboardViewModel.swift
│   │   ├── ChartsViewModel.swift
│   │   ├── DevicesViewModel.swift
│   │   └── SettingsViewModel.swift
│   ├── Services/
│   │   ├── BluetoothService.swift
│   │   ├── NetworkService.swift
│   │   ├── DataService.swift
│   │   └── NotificationService.swift
│   ├── Utils/
│   │   ├── Constants.swift
│   │   ├── Extensions.swift
│   │   └── Helpers.swift
│   └── Resources/
│       ├── Assets.xcassets
│       ├── Info.plist
│       └── Localizable.strings
├── SolarMonitorMobileTests/
└── SolarMonitorMobileUITests/
```

### **Android App Structure (Jetpack Compose)**
```
app/
├── src/main/java/com/solarmonitor/mobile/
│   ├── models/
│   │   ├── SolarData.kt
│   │   ├── DeviceInfo.kt
│   │   ├── Alert.kt
│   │   └── Settings.kt
│   ├── ui/
│   │   ├── MainActivity.kt
│   │   ├── dashboard/
│   │   │   ├── DashboardScreen.kt
│   │   │   └── DashboardViewModel.kt
│   │   ├── charts/
│   │   │   ├── ChartsScreen.kt
│   │   │   └── ChartsViewModel.kt
│   │   ├── devices/
│   │   │   ├── DevicesScreen.kt
│   │   │   └── DevicesViewModel.kt
│   │   ├── settings/
│   │   │   ├── SettingsScreen.kt
│   │   │   └── SettingsViewModel.kt
│   │   └── components/
│   │       ├── PowerCard.kt
│   │       ├── ChartView.kt
│   │       └── StatusIndicator.kt
│   ├── services/
│   │   ├── BluetoothService.kt
│   │   ├── NetworkService.kt
│   │   ├── DataService.kt
│   │   └── NotificationService.kt
│   ├── utils/
│   │   ├── Constants.kt
│   │   ├── Extensions.kt
│   │   └── Helpers.kt
│   └── di/
│       ├── NetworkModule.kt
│       ├── DatabaseModule.kt
│       └── ServiceModule.kt
├── src/main/res/
│   ├── layout/
│   ├── values/
│   │   ├── strings.xml
│   │   ├── colors.xml
│   │   └── themes.xml
│   ├── drawable/
│   └── mipmap/
└── build.gradle
```

## 🔌 Pi Integration

### **REST API Endpoints**

The Pi exposes these endpoints for the mobile app:

```python
# Base URL: http://[PI_IP]:5001/api/mobile/

# Dashboard data
GET /dashboard
Response: {
    "success": true,
    "data": {
        "production": 3.2,
        "consumption": 2.1,
        "net_power": 1.1,
        "timestamp": "2024-01-15T10:30:00",
        "status": "online"
    }
}

# Historical data
GET /historical?start=2024-01-01&end=2024-01-15&interval=hour
Response: {
    "success": true,
    "data": [
        {
            "timestamp": "2024-01-15T10:00:00",
            "production": 3.2,
            "consumption": 2.1,
            "net_power": 1.1
        }
    ]
}

# Device list
GET /devices
Response: {
    "success": true,
    "devices": [
        {
            "id": "inverter_1",
            "name": "Solar Panel 1",
            "type": "inverter",
            "status": "online",
            "production": 0.8
        }
    ]
}

# System alerts
GET /alerts
Response: {
    "success": true,
    "alerts": [
        {
            "type": "warning",
            "message": "Low solar production",
            "severity": "medium"
        }
    ]
}
```

### **Bluetooth Low Energy Service**

The Pi also provides BLE services for offline access:

```python
# BLE Service UUID: 12345678-1234-1234-1234-123456789abc
# Data Characteristic: 12345678-1234-1234-1234-123456789ac1
# Notification Characteristic: 12345678-1234-1234-1234-123456789ac2

# Data format (JSON):
{
    "production": 3.2,
    "consumption": 2.1,
    "net_power": 1.1,
    "timestamp": "2024-01-15T10:30:00",
    "status": "online"
}
```

## 📱 Core Features Implementation

### **1. Dashboard Screen**

#### **iOS Implementation (SwiftUI)**
```swift
struct DashboardView: View {
    @StateObject private var viewModel = DashboardViewModel()
    
    var body: some View {
        ScrollView {
            VStack(spacing: 20) {
                // Current Status
                StatusIndicator(status: viewModel.status)
                
                // Power Cards
                HStack(spacing: 15) {
                    PowerCard(
                        title: "Production",
                        value: viewModel.production,
                        unit: "kW",
                        color: .green
                    )
                    
                    PowerCard(
                        title: "Consumption",
                        value: viewModel.consumption,
                        unit: "kW",
                        color: .blue
                    )
                }
                
                // Net Power
                PowerCard(
                    title: "Net Power",
                    value: viewModel.netPower,
                    unit: "kW",
                    color: viewModel.netPower >= 0 ? .green : .red
                )
                
                // Today's Total
                PowerCard(
                    title: "Today's Total",
                    value: viewModel.todayTotal,
                    unit: "kWh",
                    color: .orange
                )
            }
            .padding()
        }
        .onAppear {
            viewModel.startDataRefresh()
        }
    }
}
```

#### **Android Implementation (Jetpack Compose)**
```kotlin
@Composable
fun DashboardScreen(
    viewModel: DashboardViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.startDataRefresh()
    }
    
    LazyColumn(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp),
        verticalArrangement = Arrangement.spacedBy(16.dp)
    ) {
        item {
            StatusIndicator(status = uiState.status)
        }
        
        item {
            Row(
                modifier = Modifier.fillMaxWidth(),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                PowerCard(
                    title = "Production",
                    value = uiState.production,
                    unit = "kW",
                    color = Color.Green,
                    modifier = Modifier.weight(1f)
                )
                
                PowerCard(
                    title = "Consumption",
                    value = uiState.consumption,
                    unit = "kW",
                    color = Color.Blue,
                    modifier = Modifier.weight(1f)
                )
            }
        }
        
        item {
            PowerCard(
                title = "Net Power",
                value = uiState.netPower,
                unit = "kW",
                color = if (uiState.netPower >= 0) Color.Green else Color.Red
            )
        }
        
        item {
            PowerCard(
                title = "Today's Total",
                value = uiState.todayTotal,
                unit = "kWh",
                color = Color.Orange
            )
        }
    }
}
```

### **2. Charts Screen**

#### **iOS Implementation (Charts Framework)**
```swift
import Charts

struct ChartsView: View {
    @StateObject private var viewModel = ChartsViewModel()
    
    var body: some View {
        VStack {
            // Time Range Selector
            Picker("Time Range", selection: $viewModel.selectedRange) {
                Text("Today").tag(ChartRange.today)
                Text("Week").tag(ChartRange.week)
                Text("Month").tag(ChartRange.month)
            }
            .pickerStyle(SegmentedPickerStyle())
            .padding()
            
            // Chart
            Chart(viewModel.chartData) { dataPoint in
                LineMark(
                    x: .value("Time", dataPoint.timestamp),
                    y: .value("Production", dataPoint.production)
                )
                .foregroundStyle(.green)
                
                LineMark(
                    x: .value("Time", dataPoint.timestamp),
                    y: .value("Consumption", dataPoint.consumption)
                )
                .foregroundStyle(.blue)
            }
            .frame(height: 300)
            .padding()
        }
        .onAppear {
            viewModel.loadChartData()
        }
    }
}
```

#### **Android Implementation (MPAndroidChart)**
```kotlin
@Composable
fun ChartsScreen(
    viewModel: ChartsViewModel = hiltViewModel()
) {
    val uiState by viewModel.uiState.collectAsState()
    
    LaunchedEffect(Unit) {
        viewModel.loadChartData()
    }
    
    Column(
        modifier = Modifier
            .fillMaxSize()
            .padding(16.dp)
    ) {
        // Time Range Selector
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            ChartRange.values().forEach { range ->
                FilterChip(
                    onClick = { viewModel.selectRange(range) },
                    label = { Text(range.displayName) },
                    selected = uiState.selectedRange == range
                )
            }
        }
        
        Spacer(modifier = Modifier.height(16.dp))
        
        // Chart
        AndroidView(
            factory = { context ->
                LineChart(context).apply {
                    setupChart()
                }
            },
            update = { chart ->
                chart.updateData(uiState.chartData)
            },
            modifier = Modifier
                .fillMaxWidth()
                .height(300.dp)
        )
    }
}
```

### **3. Bluetooth Service**

#### **iOS Implementation (Core Bluetooth)**
```swift
import CoreBluetooth

class BluetoothService: NSObject, ObservableObject {
    private var centralManager: CBCentralManager!
    private var connectedPeripheral: CBPeripheral?
    private var dataCharacteristic: CBCharacteristic?
    
    @Published var isConnected = false
    @Published var solarData: SolarData?
    
    override init() {
        super.init()
        centralManager = CBCentralManager(delegate: self, queue: nil)
    }
    
    func startScanning() {
        let serviceUUID = CBUUID(string: "12345678-1234-1234-1234-123456789abc")
        centralManager.scanForPeripherals(withServices: [serviceUUID], options: nil)
    }
    
    func connect(to peripheral: CBPeripheral) {
        centralManager.connect(peripheral, options: nil)
    }
}

extension BluetoothService: CBCentralManagerDelegate {
    func centralManagerDidUpdateState(_ central: CBCentralManager) {
        if central.state == .poweredOn {
            startScanning()
        }
    }
    
    func centralManager(_ central: CBCentralManager, didDiscover peripheral: CBPeripheral, advertisementData: [String : Any], rssi RSSI: NSNumber) {
        if peripheral.name?.contains("Solar Monitor") == true {
            connect(to: peripheral)
        }
    }
    
    func centralManager(_ central: CBCentralManager, didConnect peripheral: CBPeripheral) {
        connectedPeripheral = peripheral
        peripheral.delegate = self
        peripheral.discoverServices(nil)
        isConnected = true
    }
}

extension BluetoothService: CBPeripheralDelegate {
    func peripheral(_ peripheral: CBPeripheral, didDiscoverServices error: Error?) {
        guard let services = peripheral.services else { return }
        
        for service in services {
            if service.uuid == CBUUID(string: "12345678-1234-1234-1234-123456789abc") {
                peripheral.discoverCharacteristics(nil, for: service)
            }
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didDiscoverCharacteristicsFor service: CBService, error: Error?) {
        guard let characteristics = service.characteristics else { return }
        
        for characteristic in characteristics {
            if characteristic.uuid == CBUUID(string: "12345678-1234-1234-1234-123456789ac1") {
                dataCharacteristic = characteristic
                peripheral.setNotifyValue(true, for: characteristic)
            }
        }
    }
    
    func peripheral(_ peripheral: CBPeripheral, didUpdateValueFor characteristic: CBCharacteristic, error: Error?) {
        guard let data = characteristic.value else { return }
        
        if let jsonString = String(data: data, encoding: .utf8),
           let jsonData = jsonString.data(using: .utf8),
           let solarData = try? JSONDecoder().decode(SolarData.self, from: jsonData) {
            self.solarData = solarData
        }
    }
}
```

#### **Android Implementation (Bluetooth Low Energy)**
```kotlin
class BluetoothService : Service() {
    private var bluetoothAdapter: BluetoothAdapter? = null
    private var bluetoothGatt: BluetoothGatt? = null
    private var dataCharacteristic: BluetoothGattCharacteristic? = null
    
    private val serviceUuid = ParcelUuid.fromString("12345678-1234-1234-1234-123456789abc")
    private val dataCharacteristicUuid = ParcelUuid.fromString("12345678-1234-1234-1234-123456789ac1")
    
    override fun onBind(intent: Intent?): IBinder? = binder
    
    private val binder = BluetoothBinder()
    
    inner class BluetoothBinder : Binder() {
        fun getService(): BluetoothService = this@BluetoothService
    }
    
    fun startScanning() {
        bluetoothAdapter = (getSystemService(Context.BLUETOOTH_SERVICE) as BluetoothManager).adapter
        
        val scanner = bluetoothAdapter?.bluetoothLeScanner
        val scanFilter = ScanFilter.Builder()
            .setServiceUuid(serviceUuid)
            .build()
        
        val scanSettings = ScanSettings.Builder()
            .setScanMode(ScanSettings.SCAN_MODE_LOW_LATENCY)
            .build()
        
        scanner?.startScan(listOf(scanFilter), scanSettings, scanCallback)
    }
    
    private val scanCallback = object : ScanCallback() {
        override fun onScanResult(callbackType: Int, result: ScanResult) {
            val device = result.device
            if (device.name?.contains("Solar Monitor") == true) {
                connectToDevice(device)
            }
        }
    }
    
    private fun connectToDevice(device: BluetoothDevice) {
        bluetoothGatt = device.connectGatt(this, false, gattCallback)
    }
    
    private val gattCallback = object : BluetoothGattCallback() {
        override fun onConnectionStateChange(gatt: BluetoothGatt, status: Int, newState: Int) {
            if (newState == BluetoothProfile.STATE_CONNECTED) {
                gatt.discoverServices()
            }
        }
        
        override fun onServicesDiscovered(gatt: BluetoothGatt, status: Int) {
            val service = gatt.getService(serviceUuid.uuid)
            dataCharacteristic = service?.getCharacteristic(dataCharacteristicUuid.uuid)
            dataCharacteristic?.let { characteristic ->
                gatt.setCharacteristicNotification(characteristic, true)
            }
        }
        
        override fun onCharacteristicChanged(gatt: BluetoothGatt, characteristic: BluetoothGattCharacteristic) {
            val data = characteristic.value
            val jsonString = String(data, Charsets.UTF_8)
            val solarData = Gson().fromJson(jsonString, SolarData::class.java)
            // Update UI with solar data
        }
    }
}
```

## 🚀 Development Phases

### **Phase 1: Core Functionality (4-6 weeks)**
- [ ] **Project setup** and basic architecture
- [ ] **Dashboard screen** with real-time data
- [ ] **WiFi connectivity** to Pi
- [ ] **Basic charts** for daily data
- [ ] **Settings screen** for configuration
- [ ] **iOS version** first

### **Phase 2: Enhanced Features (4-6 weeks)**
- [ ] **Bluetooth connectivity** for offline access
- [ ] **Advanced charts** with multiple time ranges
- [ ] **Device management** screen
- [ ] **Push notifications** for alerts
- [ ] **Android version** development
- [ ] **Data caching** for offline viewing

### **Phase 3: Advanced Integration (4-6 weeks)**
- [ ] **Smart home integration** (Home Assistant)
- [ ] **Data export** and sharing
- [ ] **Custom alerts** and automation
- [ ] **Performance optimization**
- [ ] **App Store** and Google Play submission
- [ ] **Beta testing** program

### **Phase 4: Premium Features (4-6 weeks)**
- [ ] **Multiple Pi support** for large installations
- [ ] **Cloud backup** and synchronization
- [ ] **Advanced analytics** and insights
- [ ] **Social sharing** of solar achievements
- [ ] **Subscription model** for premium features
- [ ] **Enterprise features** for commercial users

## 📱 App Store Submission

### **iOS App Store**
1. **App Store Connect** - Create app listing
2. **TestFlight** - Beta testing program
3. **App Review** - Apple's review process
4. **Release** - Public availability

### **Google Play Store**
1. **Google Play Console** - Create app listing
2. **Internal Testing** - Beta testing program
3. **App Review** - Google's review process
4. **Release** - Public availability

## 💰 Monetization Strategy

### **Freemium Model**
- **Free tier**: Basic monitoring, 7-day history
- **Premium tier**: Extended history, advanced charts, cloud backup
- **Pro tier**: Multiple Pi support, advanced analytics, priority support

### **Pricing Structure**
- **Free**: $0/month - Basic monitoring (better than SunStrong's free tier)
- **Premium**: $4.99/month - Extended features (50% less than SunStrong)
- **Pro**: $7.99/month - Advanced features (20% less than SunStrong)

### **Value Proposition**
> **"Stop paying SunStrong $10/month for features that used to be free! Get your own local solar monitoring system for $0-8/month with complete data ownership and no cloud dependency."**

### **Revenue Projections**
- **1000 users**: $2,500/month (50% premium conversion at $5/month avg)
- **5000 users**: $12,500/month (50% premium conversion at $5/month avg)
- **10000 users**: $25,000/month (50% premium conversion at $5/month avg)

## 🔧 Testing Strategy

### **Unit Testing**
- **ViewModels** - Business logic testing
- **Services** - API and Bluetooth testing
- **Models** - Data structure testing
- **Utils** - Helper function testing

### **Integration Testing**
- **API integration** - Pi communication testing
- **Bluetooth integration** - BLE service testing
- **Database integration** - Local storage testing
- **Notification integration** - Push notification testing

### **UI Testing**
- **Screen navigation** - User flow testing
- **Data display** - Chart and card testing
- **User interactions** - Button and gesture testing
- **Accessibility** - Screen reader testing

## 📊 Analytics & Monitoring

### **User Analytics**
- **Firebase Analytics** - User behavior tracking
- **Crashlytics** - Crash reporting
- **Performance** - App performance monitoring
- **User engagement** - Feature usage tracking

### **Business Metrics**
- **Download rate** - App store downloads
- **Conversion rate** - Free to premium conversion
- **Retention rate** - User retention tracking
- **Revenue** - Subscription revenue tracking

---

**This mobile app development guide provides everything needed to create professional iOS and Android apps that integrate seamlessly with your Raspberry Pi solar monitoring system!**
