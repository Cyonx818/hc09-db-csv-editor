# hc09-db-csv-editor
A script to handle bulk attribute editing of CSV dumps from NFL Head Coach '09 save games and roster databases.

Usage requires HC09 Editor v1.3.2 or newer. 

Open the savegame using DB editor (not 'Load Career File' or 'Edit Game Files')

Export the PLAY, COCH, CSKL, GMVW, GMSK, and TRVW databases to csv files of the same name (E.G. The PLAY DB should be exported as 'play.csv')

Run python, calling the script (E.G. python3 .\hc09-db-csv-editor.py). You can specify the location of the target play, coch, gmvw, or trvw csv file as a command line argument

Be sure to import the the modified csv file back into the DB editor on top of the original DB, and then save the modified savegame.
