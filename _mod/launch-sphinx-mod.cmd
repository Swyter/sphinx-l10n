:: sphinx PC install search batch script thingie -- created by swyter in january 2019
:: --
:: run this to automatically find either the GOG or the Steam version of the game (the former has priority)
:: and launch it with the current folder's path in the mod parameter. easy peasy lemon squeezy :)

@echo off && setlocal EnableExtensions && setlocal EnableDelayedExpansion && setlocal && set arguments="%*"

:: https://stackoverflow.com/a/23328830/674685

:: reg query HKLM\SOFTWARE\GOG.com\Games\1118073204 /v exe /reg:32
::    exe    REG_SZ    C:\Program Files (x86)\GOG Galaxy\Games\Sphinx and the Cursed Mummy\SphinxD_GL.exe

for /f "tokens=2*" %%a in ('reg query HKLM\SOFTWARE\GOG.com\Games\1118073204 /v exe /reg:32 2^>^&1 ^| find "REG_"') do @set sphinx_gog=%%b

::reg query HKLM\SOFTWARE\Valve\Steam /v InstallPath /reg:32 | findstr /ri "REG_SZ"
::    InstallPath    REG_SZ    C:\Program Files (x86)\Steam

for /f "tokens=2*" %%a in ('reg query HKLM\SOFTWARE\Valve\Steam /v InstallPath      /reg:32 2^>^&1 ^| find "REG_"') do @set steam_path=%%b

if exist "%sphinx_gog%" (
	echo [i] The GOG version of Sphinx is installed in "%sphinx_gog%"
	call :run_game_with_mod "%sphinx_gog%"
)

if exist "%steam_path%" (
	echo [i] Steam is installed in "%steam_path%", searching in SteamLibraries
	
	:: swy: try first to locate the game in the default SteamLibrary, which is the Steam folder.
	call :find_in_steam_library "%steam_path%"
	
	:: swy: get the number of lines in our libraryfolders.vdf and use it to iterate over all the possible
	::      extra SteamLibraries in other drives where the game might be installed.
	for /f "tokens=*" %%g in ('type "%steam_path%\steamapps\libraryfolders.vdf" ^| find /v /c ""') do set libraryfolders_line_count=%%g

	:: https://stackoverflow.com/a/9102569/674685
	for /l %%h in (1,1,!libraryfolders_line_count!) do ( 
		for /f delims^=^"^ tokens^=4 %%g in ('type "%steam_path%\steamapps\libraryfolders.vdf" ^| find """%%h"""') do call :find_in_steam_library "%%g"
	)
)

endlocal
goto :eof

:: --

:find_in_steam_library
	if "%~1" == "" goto :eof

	echo     [?] Searching in SteamLibrary "%~1"
	
	if not exist "%~1\steamapps\appmanifest_606710.acf" (
		echo         \ The manifest is not here && goto :eof
	)
	
	:: swy: get the install folder (which should always be "Sphinx and the Cursed Mummy", but just in case)
	::      from the App Manifest; keep in mind that 606710 is the Steamworks AppID for our game.
	for /f delims^=^"^ tokens^=4 %%G in ('type "%~1\steamapps\appmanifest_606710.acf" ^| find "installdir" 2^>^&1') do @set sphinx_steam_dir=%%~G
	
	if not "%~1" == "" call :run_game_with_mod "%~1\steamapps\common\%sphinx_steam_dir%\SphinxD_GL.exe"
goto :eof


:run_game_with_mod
	if exist "%~1" (
		echo [-] Found game binary at "%~1"; launching it.
		:: https://stackoverflow.com/a/72758/674685
		start "Dummy title" "%~1" %arguments% -mod "%cd%/Sphinx/Binary/_bin_PC/"
		exit
	) else (
		echo [e] The game path to "%~1" does not exist, broken install?
	)
goto :eof