#/usr/bin/sh
pyuic5 -xo design_main.py Main.ui
pyuic5 -xo design_settings_demod.py settings/Settings_Demod.ui
pyuic5 -xo design_settings_decode.py settings/Settings_Decode.ui
pyuic5 -xo design_settings_analyze.py settings/Settings_Analyze.ui
