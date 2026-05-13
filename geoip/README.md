# GeoIP Database Setup

This directory should contain the MaxMind GeoLite2 City database for IP-based geolocation.

## Download Instructions

1. **Sign up for a free MaxMind account**:

   - Go to https://www.maxmind.com/en/geolite2/signup
   - Create a free account

2. **Download GeoLite2 City database**:

   - Log in to your MaxMind account
   - Go to "Download Files" section
   - Download "GeoLite2 City" in MMDB format
   - Extract the downloaded file

3. **Place the database file**:
   - Copy `GeoLite2-City.mmdb` to this directory
   - The final path should be: `geoip/GeoLite2-City.mmdb`

## File Structure

```
geoip/
├── README.md (this file)
└── GeoLite2-City.mmdb (download this file)
```

## Note

The GeoLite2 database is not included in the repository due to:

- Large file size (~70MB)
- MaxMind license requirements
- Regular updates needed

The application will use this database for automatic city detection based on user IP addresses.
