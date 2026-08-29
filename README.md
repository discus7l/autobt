AutoBT

Automatically switch muOS audio to your connected Bluetooth headphones, earbuds, or speaker.

🎮 What is AutoBT?

AutoBT is a small script for muOS that automatically selects your connected Bluetooth audio device as the default audio output when your handheld starts.

Instead of manually selecting your Bluetooth headphones every time you boot, AutoBT does it for you.

Boot → Bluetooth connects → AutoBT selects it → Start gaming. 🎮

📋 Requirements
A muOS device
Bluetooth audio device
Bluetooth device already paired with your handheld
(use Bluetooth app https://github.com/nvcuong1312/bltMuos to pair)

Tested with muOS AW Banana on rg35xxsp. No other muOS versions or devices have been tested so far. Use at your own risk.

📥 Installation

Download autobt_vX.X.X.zip from the releases, extract the following three files:

autobt.py
autobt_conf.ini
start-autobt.sh

Copy them to your muOS SD card:

autobt.py
autobt_conf.ini
        → /mnt/mmc/MUOS/application/

start-autobt.sh
        → /mnt/mmc/MUOS/init/

That's it.

Reboot your handheld and AutoBT will start automatically.

🔊 How it works

AutoBT checks for connected Bluetooth devices and looks for the corresponding audio sink in PipeWire.

If it finds one, it automatically sets it as the default audio output using wpctl.

For example, if your Bluetooth device appears as:

58. TX612 [vol: 0.25]

AutoBT will automatically set sink 58 as the default audio output.

📝 Logs

AutoBT creates a log file here:

/mnt/mmc/MUOS/application/autobt.log

If something isn't working, this is the first place to look.

⚙️ Configuration

The script currently waits for a Bluetooth audio device for a limited amount of time during startup. This is to minimize workload during gameplay.

Advanced users can edit autobt_conf.ini to change the behavior.

💖 Support Dev
[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/yu2kataoka)

🛠️ Troubleshooting
Bluetooth connects but audio stays on the built-in speakers

Check the PipeWire audio sinks:

wpctl status

Your Bluetooth device should appear under Sinks.

AutoBT doesn't appear to run

Check the startup log:

cat /mnt/mmc/MUOS/init/start_autobt.log

Also make sure the files are in the correct locations:

/mnt/mmc/MUOS/application/autobt.py
/mnt/mmc/MUOS/application/autobt_conf.ini
/mnt/mmc/MUOS/init/start-autobt.sh

Then reboot.

💡 Why does this exist?

muOS is awesome for retro gaming, but switching Bluetooth audio manually every time can be a little tedious.

AutoBT is meant to make Bluetooth audio feel more seamless:

Turn on your handheld. Put on your headphones. Start playing.

No menu diving required.

📜 License

See the repository for license information.