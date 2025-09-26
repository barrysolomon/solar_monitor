# Solar Monitor Version Management

This directory contains organized releases and deployment artifacts for the Solar Monitor system.

## Directory Structure

```
versions/
├── v1.0.0/                          # Production Release
│   ├── solar_monitor_v1.0.0_PRODUCTION/    # Clean production code
│   ├── solar_monitor_v1.0.0_PRODUCTION_RELEASE.tar.gz  # Release archive
│   ├── solar_monitor_v1.0.0_PRODUCTION_BACKUP.tar.gz   # Pre-deployment backup
│   ├── RELEASE_NOTES.md             # Detailed release notes
│   └── deploy.sh                    # Production deployment script
├── v1.1.0/                          # Future release
├── v1.2.0/                          # Future release
└── README.md                        # This file
```

## Version Naming Convention

- **Major.Minor.Patch** (e.g., v1.0.0)
- **Major**: Breaking changes, complete redesigns
- **Minor**: New features, significant improvements
- **Patch**: Bug fixes, minor improvements

## Deployment Process

### For New Versions

1. **Create version directory:**
   ```bash
   mkdir -p versions/v1.x.x
   ```

2. **Prepare release:**
   ```bash
   cp -r production_code versions/v1.x.x/solar_monitor_v1.x.x_PRODUCTION
   ```

3. **Create deployment script:**
   ```bash
   # Copy and modify deploy.sh template
   # Update version numbers and specific changes
   ```

4. **Document release:**
   ```bash
   # Create RELEASE_NOTES.md with changes, fixes, and migration notes
   ```

5. **Deploy:**
   ```bash
   cd versions/v1.x.x/solar_monitor_v1.x.x_PRODUCTION
   ./deploy.sh
   ```

### Rollback Process

```bash
# Emergency rollback to previous version
cd versions/v1.x.x/solar_monitor_v1.x.x_PRODUCTION
./rollback.sh  # If available, or manual restore from backup
```

## Current Production Version

**v1.0.0** - Complete system redesign with modern UI, real-time analytics, and production-ready architecture.

## Archive Policy

- **Keep all major versions** (v1.0.0, v2.0.0, etc.)
- **Keep last 3 minor versions** for each major
- **Keep last 5 patch versions** for current minor
- **Archive older versions** to separate storage if needed

## Development vs Production

- **Development**: Work in main project directory
- **Production**: Clean, tested code in version directories
- **Deployment**: Always from version directories with proper scripts

This structure ensures:
- ✅ Clean separation of development and production
- ✅ Easy rollback capabilities
- ✅ Proper version tracking
- ✅ Deployment automation
- ✅ Historical preservation
