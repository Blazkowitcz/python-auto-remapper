# Auto-Remapper
## input-remapper preset loader

## Features

- Scan process and load your preset if game is found

## Tech

External dependencies:

- [Pystray](https://github.com/moses-palmer/pystray) - system tray icon.
- [Pillow](https://github.com/python-pillow/Pillow/) - Python Imaging Library (Fork)

## JSON Config File

```
{
    "games": [
        {
            "name": "Counter-Strike 2",
            "process_name": "cs2",
            "preset_name": "CS2",
            "device": {
                "constructor": "<Constructor name>",
                "name": "<device name>"
            }
        }
    ],
    "root": {
        "password": "<Dedicated app account password if rights are needed>"
    }
}
```
