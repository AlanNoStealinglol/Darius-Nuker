import sys
import os
import time
import requests
import zipfile
import io

GITHUB_REPO = "AlanNoStealinglol/Darius-Nuker"  # GitHub username/repo
VERSION = "1.0.1"  # Current version of the script

def gradient_text(text, start_color, end_color, steps):
    """Generate a gradient effect from start_color to end_color"""
    def interpolate_color(start, end, factor):
        """Interpolate between two colors"""
        return tuple(int(start[i] + (end[i] - start[i]) * factor) for i in range(3))

    def rgb_to_ansi(rgb):
        """Convert RGB color to ANSI escape code"""
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"

    start_rgb = [0, 128, 0] if start_color == 'green' else [255, 255, 255]
    end_rgb = [255, 255, 255] if end_color == 'white' else [0, 128, 0]

    gradient = []
    for step in range(steps):
        factor = step / (steps - 1)
        color = interpolate_color(start_rgb, end_rgb, factor)
        gradient.append(rgb_to_ansi(color))
    
    return ''.join(gradient[i % len(gradient)] + char for i, char in enumerate(text)) + '\033[0m'

def banner():
    """Handler for non-unicode consoles with a blue-to-white gradient"""
    shadow = '''\
 _____             _          __ ____ ______ ___   ___  __  ___    _   _       _                ____        
|  __ \\           (_)        /_ |___ \\____  / _ \\ / _ \\_  |/ _ \\  | \\ | |     | |              / __ \\       
| |  | | __ _ _ __ _ _   _ ___| | __) |  / / (_) | (_) || | | | | |  \\| |_   _| | _____ _ __  | |  | |_ __  
| |  | |/ _` | '__| | | | / __| ||__ <  / / > _ < \\__, || | | | | | . ` | | | | |/ / _ \\ '__| | |  | | '_ \\ 
| |__| | (_| | |  | | |_| \\__ \\ |___) |/ / | (_) |  / / | | |_| | | |\\  | |_| |   <  __/ |    | |__| | |_) |
|_____/ \\__,_|_|  |_|\__,_|___/_|____//_/   \\___/  /_/  |_|\___/  |_| \\_|\__,_|_|\_\\___|_|     \\____/| .__/ 
                                                                                                      | |    
                                                                                                      |_|     
    '''
    
    banner_width = len(max(shadow.splitlines(), key=len)) + 4
    print(gradient_text('╭' + '─' * (banner_width - 2) + '╮', 'blue', 'white', 10))
    for line in shadow.splitlines():
        print(gradient_text(f"│ {line.ljust(banner_width - 4)} │", 'blue', 'white', 10))
    print(gradient_text('╰' + '─' * (banner_width - 2) + '╯', 'blue', 'white', 10))

def check_for_updates():
    """Check GitHub for a new release and update if available"""
    print("Checking for updates...")
    try:
        response = requests.get(f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest")
        latest_release = response.json()
        latest_version = latest_release['tag_name']

        if latest_version != VERSION:
            print(f"New version available: {latest_version}. Downloading update...")
            download_and_replace_script(latest_release['zipball_url'])
            print("Update complete. Restarting...")
            sys.exit(0)
        else:
            print("No new updates found. Proceeding with the current version.")
    except Exception as e:
        print(f"Failed to check for updates: {e}. Proceeding with the current version.")

def download_and_replace_script(zip_url):
    """Download and replace the script with the latest version from GitHub"""
    response = requests.get(zip_url)
    zip_data = zipfile.ZipFile(io.BytesIO(response.content))
    
    # Extract the contents of the zip file to the current directory
    zip_data.extractall()

def print_menu(options, selected_index):
    """Prints the menu options with the current selection highlighted and a blue outline"""
    os.system('cls' if os.name == 'nt' else 'clear')  # Clear the console for a fresh display
    banner()
    
    print("\nMain Menu:")
    options_list = list(options.items())
    
    # Find the maximum width of the menu option lines
    menu_width = max(len(f"[{key}] {description}") for key, description in options_list)
    
    # Print menu with border
    print(gradient_text('╭' + '─' * (menu_width + 4) + '╮', 'blue', 'white', 10))
    for i, (key, description) in enumerate(options_list):
        if i == selected_index:
            print(gradient_text(f"│ -> [{key}] {description.ljust(menu_width - 4)} │", 'blue', 'white', 10))
        else:
            print(gradient_text(f"│    [{key}] {description.ljust(menu_width - 4)} │", 'blue', 'white', 10))
    print(gradient_text('╰' + '─' * (menu_width + 4) + '╯', 'blue', 'white', 10))

def show_credits():
    """Display the credits with a green-to-white gradient"""
    credits = '''\
  _____                _           _   ____                   _             
 / ____|              | |         | | |  _ \\            /\\   | |            
| |     _ __ ___  __ _| |_ ___  __| | | |_) |_   _     /  \\  | | __ _ _ __  
| |    | '__/ _ \\/ _` | __/ _ \\/ _` | |  _ <| | | |   / /\\ \\ | |/ _` | '_ \\ 
| |____| | |  __/ (_| | ||  __/ (_| | | |_) | |_| |  / ____ \\| | (_| | | | |
 \\_____|_|  \\___|\\__,_|\\__\\___|\\__,_| |____/ \\__, | /_/    \\_\\_|\\__,_|_| |_|
                                              __/ |                         
                                             |___/                         
    '''
    print(gradient_text(credits, 'green', 'white', 20))
    input("\nPress Enter to return to the main menu...")

def main_menu():
    options = {
        '1': "Nuke",
        '2': "Stealer Builders",
        '3': "Credits",
        '4': "Exit"
    }
    selected_index = 0

    while True:
        print_menu(options, selected_index)
        choice = input("\nSelect an option: ").strip()

        if choice == '1':
            print("Nuking...")  # Displaying a message before running bot.py
            os.system('python bot.py')  # Runs bot.py using the system's Python interpreter
        elif choice == '2':
            print("Opening Stealer Builders...")  # Displaying a message before running Builder.py
            os.system('python Builder.py')  # Runs Builder.py using the system's Python interpreter
        elif choice == '3':
            show_credits()  # Display the credits
        elif choice == '4':
            print("Exiting...")
            sys.exit(0)  # Exit the program
        else:
            print("Invalid choice, please select 1, 2, 3, or 4.")
            time.sleep(1)  # Pause to allow user to see the message

if __name__ == "__main__":
    check_for_updates()  # Check for updates before launching the menu
    main_menu()
