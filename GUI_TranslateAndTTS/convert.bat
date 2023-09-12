REM Add %python versiob%\Scripts\ to Path   before running this code
pyside6-rcc.exe -o resources_rc.py resources.qrc
Python310\Scripts\pyside6-uic.exe -o ui_form.py form.ui
pyside6-uic.exe -o item.py item.ui



