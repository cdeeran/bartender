# Compile the resource files -- MUST BE DONE FIRST --
pyrcc5 ./ui/ui_files/splashScreenResource.qrc -o ./ui/output_files/splashScreenResource_rc.py
pyrcc5 ./ui/ui_files/bartenderMainWindowResource.qrc -o ./ui/output_files/bartenderMainWindowResource_rc.py
pyrcc5 ./ui/ui_files/spotifyWidgetResource.qrc -o ./ui/output_files/spotifyWidgetResource_rc.py
pyrcc5 ./ui/ui_files/customDrinkWidgetResource.qrc -o ./ui/output_files/customDrinkWidgetResource_rc.py
pyrcc5 ./ui/ui_files/premadeDrinksWidgetResource.qrc -o ./ui/output_files/premadeDrinksWidgetResource_rc.py

# Compile the UI files
pyuic5 -x ./ui/ui_files/bartender.ui -o ./ui/output_files/bartenderUi.py --from-imports
pyuic5 -x ./ui/ui_files/spotify.ui -o ./ui/output_files/spotifyUi.py --from-imports
pyuic5 -x ./ui/ui_files/customDrink.ui -o ./ui/output_files/customDrinkUi.py --from-imports
pyuic5 -x ./ui/ui_files/premadeDrinks.ui -o ./ui/output_files/premadeDrinkUi.py --from-imports
pyuic5 -x ./ui/ui_files/splashScreen.ui -o ./ui/output_files/splashScreenUi.py --from-imports
pyuic5 -x ./ui/ui_files/settings.ui -o ./ui/output_files/settingsUi.py