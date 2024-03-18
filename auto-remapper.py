import json
import subprocess
import time
import pystray
import sys
import os
import threading
from pystray import MenuItem as item
from PIL import Image, ImageDraw

current_game = current_process = current_preset = current_constructor = current_device_name = root_password = ""

def process_exists(process_name):
    """
    Check if process exist
    :param process_name: process_name
    """
    try:
        proc = subprocess.check_output(["pgrep", process_name])
        print(proc)
        return True
    except subprocess.CalledProcessError:
        return False
    
def exit_application():
    """
    Close application
    """
    threading.Thread(target=sys.exit).start()
    os._exit(0)

def update_icon_title(icon):
    """
    Update tray icon title with current game
    :param icon: icon
    """
    global current_game, current_device_name
    if current_game != "":
        icon.title = current_game + " preset started on " + current_device_name
    else:
        icon.title = "No Game"

def watch(icon):
    """
    Watch process for game and start preset
    :param icon: icon
    """
    global current_game, current_process, current_preset, current_constructor, current_device_name, root_password
    if current_game == "":
        with open("/home/blazkowicz/.config/auto-remapper/data.json", "r") as file:
            games_data = json.load(file)
        root_password = games_data["root"]["password"]
        for game in games_data["games"]:
            process_name = game["process_name"]
            game_name = game["name"]
            preset_name = game["preset_name"]
            device_constructor = game["device"]["constructor"]
            device_name = game["device"]["name"]
            
            if process_exists(process_name):
                current_game = game_name
                current_process = process_name
                current_constructor = device_constructor
                current_preset = preset_name
                current_device_name = device_name
                command = f"echo '{root_password}' | sudo -S input-remapper-control --command start --device '{device_constructor} {device_name}' --preset {preset_name}"
                subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                update_icon_title(icon)
    else:
        if not process_exists(current_process):
            command = "echo '{root_password}' | sudo -S input-remapper-control --command stop --device '{current_constructor} {current_device_name}' --preset {current_preset}"
            subprocess.run(command, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            current_game = current_process = current_preset = current_constructor = current_device_name = ""
            update_icon_title(icon)
    time.sleep(3)
    watch(icon)

def main():
    """
    Main Function
    """
    icon_image = Image.open(os.getcwd() + "/icon.png")
    icon = pystray.Icon(
        'aa',
        icon=icon_image
    )
    exit_item = item('Exit', exit_application)
    icon.title = "No Game"
    icon.menu = (exit_item,)
    
    watch_thread = threading.Thread(target=watch, args=(icon,))
    watch_thread.start()
    update_icon_title(icon)
    icon.run()

if __name__ == "__main__":
    main()
