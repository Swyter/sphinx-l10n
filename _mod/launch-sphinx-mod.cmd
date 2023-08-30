:: sphinx PC install search batch script thingie -- created by swyter in january 2019
:: --
:: run this to automatically find either the GOG or the Steam version of the game (the former has priority)
:: and launch it with the current folder's path in the mod parameter. easy peasy lemon squeezy :)

@echo off && color 71 && mode con: cols=201 lines=12 && cls && title [trying to launch sphinx mod] && chcp 65001 > nul && setlocal EnableExtensions && setlocal EnableDelayedExpansion && setlocal && set arguments="%*"


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
) else (
	echo [i] The GOG version of Sphinx does not seem to be installed right now
)

if exist "%steam_path%" (
	echo [i] Steam is installed in "%steam_path%", searching in SteamLibraries
	
	rem swy: loop for each line in our libraryfolders.vdf and use it to iterate over all the possible
	rem      extra SteamLibraries in other drives where the game might be installed.
	for /f "usebackq tokens=*" %%l in ("%steam_path%\steamapps\libraryfolders.vdf") do (
		set cur_line=%%l
		set cur_key=!cur_line:~1,4!

		rem swy: if we've found a key-value line with something like this, get the value part:
		rem      "path" "C:\\Program Files (x86)\\Steam"
		if /i "!cur_key!" == "path" (
			rem swy: escaped version of for /f "delims=" tokens=3" with working " as delimiter
			rem      https://stackoverflow.com/a/13217838/674685
			for /f delims^=^"^ tokens^=3 %%t in ("!cur_line!") do (
				rem swy: move the contents of the %t token to %cur_path_val% and then
				rem      replace the double backslashes from the VDF \\ to \.
				rem      e.g. 'C:\\Program Files (x86)\\Steam' -> 'C:\Program Files (x86)\Steam'
				set cur_path_val=%%t
				set "cur_path_val=!cur_path_val:\\=\!"

				if exist "!cur_path_val!\" (
					call :find_in_steam_library "!cur_path_val!"
				) else (
					echo     [e] Weird; the library folder seems missing: "!cur_path_val!"
				)
			)
		) 
	)
)

rem swy: if we arrived here at the end, then we probably didn't launch;
rem      pause so that the user can see/copy any errors.
pause

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
		start "Dummy title" "%~1" %arguments% -lang uk -mod "%cd%/Sphinx/Binary/_bin_PC/"
		exit
	) else (
		echo [e] The game path to "%~1" does not exist, broken install?
	)
goto :eof
