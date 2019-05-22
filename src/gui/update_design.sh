#/usr/bin/sh
pyuic5 -xo design_main.py qtDesigner/Main.ui
pyuic5 -xo settings/design_settings_demod.py qtDesigner/settings/Settings_Demod.ui
pyuic5 -xo settings/design_settings_decode.py qtDesigner/settings/Settings_Decode.ui
pyuic5 -xo settings/design_settings_analyze.py qtDesigner/settings/Settings_Analyze.ui
