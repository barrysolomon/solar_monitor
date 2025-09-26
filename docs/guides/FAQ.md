# Frequently Asked Questions

## General Questions

### Q: Do I need to be technical to use this?
**A: No!** This guide is designed for complete beginners. You just need to follow the step-by-step instructions. No programming or technical knowledge required.

### Q: How much does this cost?
**A: About $100** for all the hardware (Raspberry Pi, SD card, power supply, Ethernet cable, case). This is a one-time cost.

### Q: How long does setup take?
**A: 2-3 hours** total, including hardware setup, software installation, and testing.

### Q: Will this work with my SunPower system?
**A: Yes!** This works with SunPower PVS5 and PVS6 gateways. If you have a SunPower system with microinverters, this should work.

### Q: Do I need internet for this to work?
**A: No!** Once set up, this works completely offline. You only need internet for the initial setup and software updates.

## Hardware Questions

### Q: Why do I need a Raspberry Pi?
**A: The Raspberry Pi acts as a bridge between your home network and your solar system. It's the most reliable and cost-effective way to access your PVS6 gateway.

### Q: Can I use a different computer instead?
**A: Yes, but it's more complex.** You could use an old laptop or desktop, but the Raspberry Pi is designed for this purpose and much easier to set up.

### Q: Do I need to buy everything new?
**A: No!** You can use an old Raspberry Pi if you have one, or buy used components. Just make sure they're compatible.

### Q: What if I don't have an Ethernet port on my computer?
**A: You'll need a USB-to-Ethernet adapter (~$10) or use a Raspberry Pi with built-in Ethernet.

### Q: How long should my Ethernet cable be?
**A: Measure the distance from your PVS6 to where you'll place the Pi, then add 10-15 feet for flexibility. Most people need 25-50 feet.

## Installation Questions

### Q: Where should I place the Raspberry Pi?
**A: Inside your house or garage** - somewhere protected from weather, with good WiFi signal, and access to power.

### Q: Do I need to drill holes in my wall?
**A: Yes, you'll need to run an Ethernet cable from your outdoor PVS6 to inside your house. This usually requires drilling one small hole.

### Q: Is it safe to drill holes in my wall?
**A: Yes, but be careful!** Use a stud finder to avoid electrical wiring, and seal the hole properly to prevent water damage.

### Q: What if I can't run a cable inside?
**A: You could use a weatherproof enclosure for the Pi outside, but this is more complex and less reliable.

### Q: Do I need special tools?
**A: Just basic tools:** drill, drill bit, screwdriver, and maybe a stud finder. Nothing fancy required.

## Technical Questions

### Q: Why can't I just use WiFi to connect to my PVS6?
**A: The PVS6 WiFi puts you on an isolated network that can't access your home network. The Ethernet connection is the only reliable way to access the API.

### Q: Which Ethernet port should I use on my PVS6?
**A: Always use the BLUE Ethernet port (LAN/Installer). The WHITE port (WAN/Internet) is for cloud services only and won't provide access to solar data.

### Q: What's the difference between this and SunPower's app?
**A: This gives you more data, works offline, and you control it completely. SunPower's app was limited and dependent on their servers.

### Q: Will this void my warranty?
**A: No!** You're only accessing data that's already available through the PVS6's built-in API. You're not modifying any hardware.

### Q: What if SunPower updates their firmware?
**A: This system uses the same API that SunPower's own tools use, so it should continue working. If they change the API, the community will update the code.

### Q: Can I access this from my phone?
**A: Yes!** The web dashboard works on any device with a web browser - phone, tablet, computer.

## Troubleshooting Questions

### Q: I can't connect to my PVS6. What's wrong?
**A: Check these things:**
- Ethernet cable is connected to the "LAN" or "Installer" port
- Your Pi's IP is set correctly (172.27.153.3)
- Try rebooting the PVS6 (unplug for 30 seconds)

### Q: The dashboard shows no data. What do I do?
**A: Check these things:**
- Pi is connected to your home WiFi
- Pi can ping the PVS6 (172.27.153.1)
- Data collector is running
- Check the logs for error messages

### Q: My Pi keeps turning off. Why?
**A: Check these things:**
- Power supply is connected securely
- Using official Raspberry Pi power supply (5V, 3A)
- Power outlet is working
- Pi isn't overheating

### Q: I can't see the dashboard on my phone. Help!
**A: Check these things:**
- Pi is connected to your home WiFi
- You're using the correct IP address
- Firewall isn't blocking the connection
- Try accessing from a computer first

### Q: The system worked yesterday but not today. What happened?
**A: Check these things:**
- Pi is still running
- Ethernet cable is still connected
- PVS6 is still powered on
- Check the logs for error messages

## Advanced Questions

### Q: Can I add more features to this?
**A: Yes!** The code is open source and modular. You can add features like email alerts, data export, or integration with home automation systems.

### Q: Can I use this with other solar systems?
**A: This is specifically designed for SunPower systems with PVS5/PVS6 gateways. Other systems would need different code.

### Q: Can I run this on a different operating system?
**A: The code is Python-based and should work on Linux, macOS, or Windows, but the setup instructions are written for Raspberry Pi OS.

### Q: Can I backup my data?
**A: Yes!** The data is stored in a SQLite database that you can backup, export, or move to another system.

### Q: Can I run multiple solar systems?
**A: You'd need separate Pi setups for each system, or modify the code to handle multiple PVS gateways.

## Safety Questions

### Q: Is it safe to work with electrical equipment?
**A: Yes, but be careful!** Always turn off power before working on electrical connections, use proper tools, and follow local electrical codes.

### Q: Can this damage my solar system?
**A: No!** You're only reading data, not modifying anything. The PVS6 is designed to provide this data to authorized users.

### Q: Is it safe to drill holes in my house?
**A: Yes, but be careful!** Use a stud finder to avoid electrical wiring, and seal holes properly to prevent water damage.

### Q: Can I get electrocuted?
**A: Very unlikely!** You're working with low-voltage Ethernet cables, not high-voltage electrical wiring. Still, be careful and follow safety guidelines.

## Support Questions

### Q: Where can I get help?
**A: Check these resources:**
- GitHub Issues for technical problems
- GitHub Discussions for questions
- Community forums for general help
- Local solar installers for hardware help

### Q: What if I break something?
**A: Don't worry!** The most expensive part is the Raspberry Pi (~$65), and you can always start over. Your solar system won't be damaged.

### Q: Can I hire someone to set this up?
**A: Yes!** A local IT person or solar installer could help with the setup, though the guide is designed to be DIY-friendly.

### Q: Is there a warranty?
**A: This is open source software with no warranty. However, the community is very helpful and the code is well-tested.

---

**Still have questions?** Check the troubleshooting section in `PROJECT_SETUP.md` or open an issue on GitHub!
