REM rd /s /q __pycahce__
REM rd /s /q dist
REM rd /s /q C:\tmp
REM mkdir c:\tmp
REM xcopy *.* C:\tmp
REM C:
REM cd C:\tmp\
REM pyinstaller oghmanano.py --exclude-module matplotlib --icon=Z:\pub\images\icon.ico
pyinstaller oghmanano.py --exclude-module matplotlib --icon=C:\share\pub\images\icon.ico
time /t
REM z:
REM cd z:\pub\gui
