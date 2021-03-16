import sys
from pyautoupdate.launcher import Launcher

# Run code and return with exit code of launched code
launch=Launcher("code_1.py","https://update-url")

# Check for update before running
need_update = launch.check_new()
if need_update:
    # Prompt user for upgrade
    response = ""
    while response not in "yn":
        response=input("An update is available."
                       "Would you like to update? (y/n)")
    if response == "y":
        # Update code
        launch.update_code()
# Run developer code here
sys.exit(launch.run())