#!/bin/bash

_fold_start_ "[Packaging and stripping revision $SVNREV into a Steam Workshop build]"

_fold_final_


_fold_start_ '[Final Workshop tree view]'
    ls -lash
   #tree .

_fold_final_


_fold_start_ '[Deploying Steam Workshop build]'
    mkdir -p _steamcmd && cd _steamcmd
    CONT_FLDR='../_mod/Sphinx/Binary/_bin_PC'

    echo '"workshopitem"                           '   > workshop_entry.vdf
    echo '{                                        '  >> workshop_entry.vdf
    echo '   "appid"                      "606710" '  >> workshop_entry.vdf
    echo '   "publishedfileid"        "3138744735" '  >> workshop_entry.vdf
    echo "  \"contentfolder\"       \"$CONT_FLDR\" "  >> workshop_entry.vdf
   #echo "  \"changenote\"      \"$WORKSHOP_DESC\" "  >> workshop_entry.vdf
    echo "  \"changenote\" \"r$SVNREV - r$PREREV\" "  >> workshop_entry.vdf
    echo '}                                        '  >> workshop_entry.vdf
    echo "[i] downloading and launching the Steam client..."

    curl --fail -LOJs 'https://steamcdn-a.akamaihd.net/client/installer/steamcmd.zip' && unzip steamcmd.zip

    if [ -z $steam_ac ]; then read -p "Enter your Steam account name: " steam_ac; clear; fi
    if [ -z $steam_tk ]; then read -p "Enter your Steam password: "     steam_tk; clear; fi


    # do the actual submission using this (totally stable) work of art
    ./steamcmd.exe +login "$steam_ac" "$steam_tk" +workshop_build_item workshop_entry.vdf +quit | tee workshop.log

    # fail the build if things didn't go as expected
    grep --no-messages 'Success.' workshop.log || exit 1;

_fold_final_
