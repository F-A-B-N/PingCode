# PingCode

A Python-based network ping utility with multi-threading support and a visual interface.

## Features

- Multi-threaded ping implementation for efficient network probing
- Real-time visual interface showing ping results
- Configurable target host and thread count
- Cross-platform: Windows, Linux, macOS

## Download

Pre-compiled binaries are available in [Releases](https://github.com/F-A-B-N/PingCode/releases) — no Python installation required.

- `ping.exe` — Windows

## Run from source

Requires Python 3.6+ and Tkinter.

```bash
python ping.py
```

On Debian/Ubuntu, Tkinter may need to be installed separately:

```bash
sudo apt install python3-tk
```

## Usage

1. Enter a target host (IP or domain)
2. Set the number of threads
3. Click Start

**Warning:** Use threading responsibly, only against systems you own or have permission to test. Too many threads can overheat a machine or accidentally DDoS a target.

## Notes

- All other modules used (`platform`, `subprocess`, `threading`, `multiprocessing`) are part of the Python standard library.
- Built and tested on Windows and Linux.

## License

MIT
