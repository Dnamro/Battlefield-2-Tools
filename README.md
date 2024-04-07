# Battlefield-2-Tools
Battlefield 2 Tools
Battlefield 2 (2142) tools
Python script

Requires Python 3  
Release date:  April 7, 2023

Author: Dnamro

Setup:  Mods must be set up with extracted map intended to update.   Normally this would the be same set up for BF2 editor.   
- In the [mod name] folder  create a \tools folder and extract the files in there.
- Run the BF_TOOLS.bat file from the folder.
This way, if there is an error, the message will remain on the screen.  A list of maps will display with a number next to each one.  
Type the number of the map. 

How this works:  The Python script, BF_TOOLS.py, is a collection of Ptyhon scripts that share common code.  The *.bat file is used to launch the BF_TOOLS.py code.  This will allow an error message to remaing on the screen to help with any necessary debugging and also allow the tool to support a dual install of Python 2 and 3.  

Note:  It is recommended to make sure you have a backup of the files that can go back to.  Some will create a backup automatically.

Dual Python 2 and 3 install:
If you have both python 2 and 3 installed, you should change the BF_TOOLS.bat file to point to the specific location of the python.exe in the python 3 folder.


Function Description:

The following functions are currently available:
(A) Create Strategic Area file
(B) Check and Update Strategic Area file
(C) Clean Editor GPO file for BF2
(D) Clean Editor GPO file for BF2142
(E) Check Map for Single Player issues
(F) Set Up Static Object file with Nav-stand-ins
(0) Quit 

Function: (A) Create Strategic Area file

Purpose:  Creates the Strategic Area file if missing and adds neighbors.  The editor can create an SA file, but does not add neighbors automatically.


Function: (B) Check and Update Strategic Area file

Purpose:  Checks the Stratgic Area file and then gives an option to update if neighbors are not set as in Function(A)


Function: (C) Clean Editor GPO file for BF2
Purpose:  This tool looks through GamePlayObjects.con (GPO) file in the selected map's editor folder and performs the following cleanup actions:

- Sets all layers to 1

- Disabled the following lines by adding "REM" in front because they are known to have issues with SP/COOP:

  REM ObjectTemplate.setScatterSpawnPositions 1
  REM ObjectTemplate.teamOnVehicle

- Checks and updates the control point numbers if they are not sequential (Due to known issues with SP/COOP).  Updates the spawners as well

- Checks for CP ID # set to -1 or missing and fixed them by assinging to the nearest CP.  (This is a known issue with adding SP/COOP to BF2142 maps that don't have Conquest)

- Adds the following line to the combat area if missing (required for adding SP/COOP to a map)
  combatarea.usedbypathfinding


Function: (D) Clean Editor GPO file for BF2142
Purpose:  This tool looks through GamePlayObjects.con (GPO) file in the selected map's editor folder and performs the  cleanup actions as for the BF2 version in Function (C) but it also replaces the BF2142 vehicle spawners with similar BF2 spawners.  This is important because the editor was never updated to support BF2142 and can not handle the mechs and some other BF2142 vehicles in the editor. The covnersion file is a text file called editor_conv.txt.  Each line as a BF2142 vehicle name and then a BFeditor friendly version, usually a BF2 vehicle or object. 


Function: (E) Check Map for Single Player issues

Purpose:  Checks fixes the following AI issues for BF2/BF2142 on the selected map:

-Check for Overgrowth:  Creates a blank one if not found.
-Clean up editor GPO for AI:  Performs all the same checks for the GPO as in (C)
-Create AI\AI file if it does not exist


Function: (F) Set Up Static Object file with Nav-stand-ins

Purpose:  Replaces the static objects in the map's strategic Objects file with the nav stand-ins based on the Nav_Stand_in_con.txt.  
