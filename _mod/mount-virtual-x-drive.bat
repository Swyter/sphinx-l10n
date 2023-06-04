@echo off && title [Mounting EngineX partition until next reboot] && color 1e && mode con: cols=130 lines=10

echo. 

subst | findstr "X:" > nul
if "%errorlevel%" == "0" (
  echo.  [-] Unmounting the temporary X: partition,
  echo.      run this again to remount it...
  subst X: /D
) else ( 
  echo.  [+] Temporarily mounting the "%cd%"
  echo.      folder as the X: partition...
  subst X: "%cd%"
)

echo. 

if "%errorlevel%" == "0" (
  echo.  [i] All done... :^)
) else (
  echo.  [!] Oops, something went wrong...
)

echo. && pause