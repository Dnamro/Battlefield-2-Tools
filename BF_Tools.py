import os;
import stat;
import os.path as path;
import sys;
import time;
#import logging;
import datetime;
from optparse import OptionParser;
from shutil import copyfile;

#globals;
_MeshMode = 3;  # 3 = both infantry and vehicle
_NavmeshModes = [ "Infantry", "Vehicle"];
_NavmeshGenerator = "navmesh.exe";
_LogFile = ""
_LogProgressFile = ""
_Mod_Name = ""
_Progress = ""
_MeshLeveldir = ""
_ModLevelDir = ""
_Version = "3.3 Test"
_CPList = {};
_SA_CPList = {};
_SA_Value = "50"
_Veh_Search_Rad_mult = 2.82843
_CP_NameList = [];
_CP_Inf_Set_Order_list = {};
_CP_Veh_Set_Order_list = {};
_CP_hoistMinMax = {};
_CP_TTGC = {};
_CP_TTLC = {};
_CP_PosList = {};
_CP_radius_list = {};
_CP_team_list = {};
_CP_List_set = "";
_Layer = "1"
_unicodeFound = ""
_InitKitTeamNames = {}  # 1 is GE, 2 is US
_InitKitTeamLanguage = {} #1 "German" #2 "English"
_InitKitTeamFlag = {} #0 "flag_neutral", #1 "flag_GE", #2 flag_uk"

#0 gameLogic.setKit 1 0 "GE_early_Sniper" "ger_rilfe_1"
#1 gameLogic.setKit 2 0 "GBR_Sniper" "brit_rilfe_1"
#gameLogic.setKit # # [kit Type] [kit name]
#0 setkit 1 0 = kit 0       
#1 setkit 2 0 = kit 0 + 1 
#2 setkit 1 1 = kit 1
#3 setkit 1 1 = kit 1 + 1

_InitKitType_list = {}
_InitKitName_list = {}

#Classes
class HandWeapon:
    def __init__(self, 
        detonatorobject,
        thrownfirecomp,
        weaponName,
        weaponIndex,
        projectiletemplate,
        replenishingType,
        roundsperminute,
        distToMinDamage,
        target_maxDistance,
        targetSystem,
        abilitymaterial,
        triggerType,
        magsize,
        nrOfMags,
        velocity,        
        projectileDamage,
        aiTemplate
        ):
        self.detonatorobject = detonatorobject
        self.thrownfirecomp = thrownfirecomp        
        self.weaponName = weaponName 
        self.weaponIndex = weaponIndex
        self.projectiletemplate = projectiletemplate
        self.replenishingType = replenishingType
        self.roundsperminute = roundsperminute
        self.distToMinDamage = distToMinDamage
        self.target_maxDistance = target_maxDistance
        self.targetSystem = targetSystem
        self.abilitymaterial = abilitymaterial
        self.triggerType = triggerType
        self.magsize = magsize
        self.nrOfMags = nrOfMags
        self.velocity = velocity
        self.projectileDamage = projectileDamage
        self.aiTemplate = aiTemplate





def cls():
	os.system('cls');
	return;
	
def removeNonAscii(s): 
	return "".join(i for i in s if ord(i)<128)
	
def secsToTimeString(secs):
	seconds = secs % 60;
	minutes = (secs / 60) % 60;
	hours = secs / (60 * 60);

	if (hours >= 1.0):
		return "%02d hours %02d minutes and %02d seconds" % (hours, minutes, seconds);
	elif (minutes >= 1.0):
		return "%02d minutes and %02d seconds" % (minutes, seconds);
	else:
		return "%02d seconds" % (seconds);

def createCmdLineParser():
	usage = "Usage: %prog meshDir [options]"
	parser = OptionParser(usage);
	parser.add_option(
		"--saveStitchSteps",
		dest="saveStitchSteps",
		type="int",
		default=False);
	return parser;

def logMsg(logFile,message):

	#log_filename = path.abspath(path.join(os.getcwd(),"/GTSData/logfiles/navmeshcontrol.log"));
	with open(logFile, 'a') as output_file:
	    output_file.write(message +"\n");
	print(message);
	return;
   

#def print(_LogFile,  message):
	#logger = logging.getLogger(__name__)
	#print(message);
    #logging.info(message);
		
def logOnlyMsg(logFile, message):
	logFile
	#log_filename = path.abspath(path.join(os.getcwd(),"/GTSData/logfiles/navmeshcontrol.log"));
	with open(logFile, 'a') as output_file:
		output_file.write(message +"\n");
	return;
	
def logProgMsg (message):
	global _LogProgressFile
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");
	#log_filename = path.abspath(path.join(os.getcwd(),"/GTSData/logfiles/navmeshcontrol.log"));
	with open(_LogProgressFile, 'a') as output_file:
		output_file.write(timestamp +"\n");
		output_file.write(message +"\n");
	return;
	
def get_last_ProgLog ():
	global _LogProgressFile
	if not path.exists(_LogProgressFile):
		print ("Progress Log file Not found :" + _LogProgressFile)
		
		return ""
	inp_f = open (_LogProgressFile)
 
	line = inp_f.readline ()
	last = line
 
	while (line != ''):
		last = line 
		line = inp_f.readline ()
	
	inp_f.close ()
 
	if len (last) == 0:
		print ("Progress Log File empty :" + _LogProgressFile)
	
		return ""
 
	return last.strip ('\n')	
	



#def print(    message):
	
	#print (_LogFile);
#	print(message);

#	if (_LogFile):
#		_LogFile.write(message);

#def logOnlyMsg(     message):
	
#	if (_LogFile):
#		_LogFile.write(message);		
		
		
def removeReadOnly(srcDir):
	return;
	
def executeCommand(commandLine):
	print ("Executing: " + commandLine) 
	result = os.system(commandLine)
	print ("")
	return result	
			
		

			
def getLargestFile(IslandDir):
	sofar = 0
	name = ""
	#Save current working directory
	owd = os.getcwd();
	#Change to Island directory
	os.chdir(IslandDir);
	objects = os.listdir(".")
	for item in objects:
		size = path.getsize(item)
		print (item)
		print ("File size: " + size)
		print ("Largest File size: " + sofar)
		if size > sofar:
			sofar = size
			name = item
	
	#print ("Largest File Name:" + name);
	#print (IslandDir);
	#print "File size" + size
	# Reset to Original Working Directory
	os.chdir(owd);
	return name

def copyLargestFile(IslandDir, outputFile):
		#print("Island Dir:" + IslandDir);
		#print("Output File:" + outputFile);
	name = getLargestFile(IslandDir);
	if (name.endswith('.obj') and  name != "") :
		srcfile = IslandDir + name
		print ("Copyied : " + outputFile);

		copyfile(srcfile, outputFile);	
	else:
		print(  "File not Copied - Invalid File name: ");
		print( "Source file: " + srcfile);
			
def copyOutputFolderFiles(srcDir, outputDir):
	print( "Copy Folder Files");
	print(  "From: " + srcDir);
	print(  "To: " + outputDir);
	#owd = os.getcwd();
	#os.chdir(srcDir);
	list = os.listdir(srcDir);
	#number_files = len(list);
	#if (number_files <= 1):
	#	print(  "Multiple Islands not found - nothing to do");
	#	os.chdir(owd);
	#	return;
	for file_Name in os.listdir(srcDir): 
		if file_Name != "":
			srcfile = path.join(srcDir, file_Name);
			dstfile = path.join(outputDir, file_Name);
			print(  "Source files:");
			print(  srcfile);
			#os.chmod(file_Name, 0o777);
			#backup obj file 
			copyfile(srcfile, dstfile);	
	#os.chdir(owd);
	return;	

def moveFolderFiles(srcDir, outputDir):
	print(  "Move Folder Files");
	print( "From: " + srcDir);
	print(  "To: " + outputDir);
	owd = os.getcwd();
	os.chdir(srcDir);
	list = os.listdir(srcDir);
	number_files = len(list);
	if (number_files <= 1):
		print(  "Multiple Islands not found - nothing to do");
		os.chdir(owd);
		return;
	for file_Name in os.listdir(srcDir): 
		if file_Name != "":
			srcfile = path.join(srcDir, file_Name);
			dstfile = path.join(outputDir, file_Name);
			print(  "Source files:");
			print(  srcfile);
			os.chmod(file_Name, 0o777);
			#backup obj file 
			copyfile(srcfile, dstfile);
			os.remove(file_Name);			
	os.chdir(owd);
	return;	

def copyFolderFiles(srcDir, outputDir):
	print( "Copy Folder Files");
	print( "From: " + srcDir);
	print( "To: " + outputDir);
	owd = os.getcwd();
	os.chdir(srcDir);
	list = os.listdir(srcDir);
	number_files = len(list);
	if (number_files <= 1):
		print( "Multiple Islands not found - nothing to do");
		os.chdir(owd);
		return;
	for file_Name in os.listdir(srcDir): 
		if file_Name != "":
			srcfile = path.join(srcDir, file_Name);
			dstfile = path.join(outputDir, file_Name);
			print( "Source files:");
			print(srcfile);
			os.chmod(file_Name, 0o777);
			#backup obj file 
			copyfile(srcfile, dstfile);	
	os.chdir(owd);
	return;
	
def createBackupFile (srcFolder, srcFile):
    #if no file is found, do nothing
    #if a .bak file already exists, rename it with a timestamp to archive it
	#then delete the .bak file
	#rename the srcFile with a bak
	#delete the srcFile
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");
	#print( "Backing up :");
    if not (path.isfile(srcFolder + srcFile)):
        print ("file not found to back up");
        print (srcFile);
        return;	
    print ("srcFolder:" + srcFolder);
    print ("srcFile:" + srcFile);	

    file_name, file_extension = os.path.splitext(srcFile)
    print ("file_name:" + file_name);
    print ("file_extension:" + file_extension);

    backupArchiveFile = (file_name + timestamp + ".bak");
    print ("BackupArchiveFile:" + backupArchiveFile);


    backupFile = (file_name + ".bak");
    print ("backupFile:" + backupFile);
		
	#backup  if it exists
    if (path.isfile(backupFile)): 
        copyfile(backupFile, backupArchiveFile);
        print(  "Saved a backup to:");
        print (backupArchiveFile);
        os.remove(backupFile);	

    if (path.isfile(srcFile)): 
        copyfile(srcFile, backupFile);
        print(  "Saved a backup to:");
        print (backupFile);
        os.remove(srcFile);
    return		
		
def restoreBackupFile (srcFolder, srcFile):	
	file_name, file_extension = os.path.splitext(srcFile)
	backupFile = (file_name + ".bak");

	print( "Restoring Backup file :");
	print (srcFile);
	if (path.isfile(srcFile)):
		print ("file already exists - backup aborted")
		return;		
		
	#backup  if it exists
	if (path.isfile(backupFile)): 
		copyfile(backupFile, srcFile);
		print(  "Saved a backup to:");
		print (backupFile);
		os.remove(backupFile)
	else:
		print ("Backup file Not Found: " + backupFile)
		
	return
	

def	createLogBackups(backupFolder):
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");

	print( "Backing up Navmesh log files files in this folder:");
	print (backupFolder);
	#backupFolder = (meshDir + "/GTSData/logfiles");	
	if (not path.isdir(backupFolder)):
		os.makedirs( backupFolder);
		
	srcFile = backupFolder + "/navMesh.log";
	backupName = ("navMesh_" + timestamp + ".log");
	backupFile = ( backupFolder + "/" + backupName);
	
	#backup  if it exists
	if (path.isfile(srcFile)): 
		copyfile(srcFile, backupFile);
		print(  "Saved a backup to:");
		print (backupFile);
		os.remove(srcFile);
	else:
		print(  "File not found to backup:");
		print (srcFile);

	srcFile = backupFolder + "/navmeshcontrol.log";
	backupName = ("navmeshcontrol_" + timestamp + ".log");
	backupFile = ( backupFolder + "/" + backupName);	
	
	#backup  if it exists
	if (path.isfile(srcFile)): 
		copyfile(srcFile, backupFile);
		print(  "Saved a backup to:");
		print (backupFile);
		os.remove(srcFile);
	else:
		print(  "File not found to backup:");
		print (srcFile);
		
	srcFile = backupFolder + "/objectsUsingBbox.log";
	backupName = ("objectsUsingBbox_" + timestamp + ".log");
	backupFile = ( backupFolder + "/" + backupName);	
	
	#backup  if it exists
	if (path.isfile(srcFile)): 
		copyfile(srcFile, backupFile);
		print(  "Saved a backup to:");
		print (backupFile);
		os.remove(srcFile);
	else:
		print(  "File not found to backup:");
		print (srcFile);	
		

	
def	createNavmeshBackups(meshDir):
	global _LogFile
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");

	print( "Backing up Navmesh obj files");
	backupFolder = (meshDir + "/GTSData/backup");	
	if (not path.isdir(backupFolder)):
		os.makedirs( backupFolder);
		
	if (_MeshMode == 1 or _MeshMode == 3): 
		print(  "Backing up Infantry.obj");
		outputFile = meshDir + "/GTSData/output/infantry.obj";
		backupName = ("Infantry_" + timestamp + ".obj");
		backupFile = (meshDir + "/GTSData/backup/" + backupName);
		
		#backup infantry.obj if it exists
		if (path.isfile(outputFile)): 
			copyfile(outputFile, backupFile);
			print(  "Saved a backup of infantry.obj to:");
			print( backupFile);
		else:
			print(  "infantry.obj Not found at:");
			print(  backupFile);	

	if (_MeshMode == 2 or _MeshMode == 3): 
		print("Backing up Vehicle.obj");
		outputFile = meshDir + "/GTSData/output/vehicle.obj";
		backupName = ("Vehicle_" + timestamp + ".obj");
		backupFile = (meshDir + "/GTSData/backup/" + backupName);
		#backup vehicle.obj 
		if (path.isfile(outputFile)): 
			copyfile(outputFile, backupFile);
			print( "Saved a backup of Vehicle.obj to:");
			print(  backupFile);
		else:
			print(  "Vehicle.obj Not found at:");
			print(  backupFile);					

def checkNavmeshIslands(meshDir):
	global _LogFile

	if (_MeshMode == 1 or _MeshMode == 3): 
		print( "Checking Infantry islands");
		IslandDir = meshDir + "/GTSData/debug/islands/infantry/";
		outputFile = meshDir + "/GTSData/output/infantry.obj";
		
		if (not path.isdir(IslandDir)):
			logOnlyMsg(  "print Island Dir:");
			print(  IslandDir);
			print(  "Infantry Island not found - press any key to return to main menu");
			choice = input();
			return;
		if os.listdir(IslandDir):
			print ("\nInfantry Islands Found --");
			print ("Do you want to copy over the largest Navmesh Island?")
			print ("Select  Y to continue ")
			choice = input();
			if (choice == "Y" or choice == "y"):
				copyLargestFile(IslandDir, outputFile);	
				print(  "Infantry island Navmesh Found and Copied");



	if (_MeshMode == 2 or _MeshMode == 3): 
		print(  "Checking Vehicle Islands");
		IslandDir = meshDir + "/GTSData/debug/islands/vehicle/";
		outputFile = meshDir + "/GTSData/output/vehicle.obj";

		if (not path.isdir(IslandDir)):
			print(  "print Island Dir:");
			print(  IslandDir);
			print( "Vehicle Navmesh Island not found - press any key to return to main menu");
			choice = input();
			return;
		if os.listdir(IslandDir):
			print ("\nVehicle Islands Found --");
			print ("Do you want to copy over the largest Navmesh Island?")
			print ("Select  Y to continue ")
			choice = input();
			if (choice == "Y" or choice == "y"):
				copyLargestFile(IslandDir, outputFile);
				print(   "Infantry island Navmesh Found and Copied");		
			
					
	print("Navmesh Island Check Complete - press any key to return to main menu");
	choice = input();			
			

def copyIslands(meshDir):
	global _LogFile

	createNavmeshBackups(meshDir);
		
	# Check for Infantry islands
		
	if (_MeshMode == 1 or _MeshMode == 3): 
		print( "Checking Infantry Islands");
		IslandDir = meshDir + "/GTSData/debug/islands/infantry/";
		outputFile = meshDir + "/GTSData/output/infantry.obj";
		
		if (not path.isdir(IslandDir)):
			print(  "print Island Dir:");
			print(  IslandDir);
			print(  "Infantry Island not found - press any key to return to main menu");
			choice = input();
			return;
		if os.listdir(IslandDir):		
			copyLargestFile(IslandDir, outputFile );	
			print( "Infantry island Navmesh Found and Copied");
			
			
		# Check for vehicle islands
	if (_MeshMode == 2 or _MeshMode == 3): 
		print( "Checking Vehicle Islands");
		IslandDir = meshDir + "/GTSData/debug/islands/vehicle/";
		outputFile = meshDir + "/GTSData/output/vehicle.obj";

		if (not path.isdir(IslandDir)):
			print(  "print Island Dir:");
			print(  IslandDir);
			print("Vehicle Navmesh Island not found - press any key to return to main menu");
			choice = input();
			return;
		if os.listdir(IslandDir):
			copyLargestFile(IslandDir, outputFile);	
			print( "Vehicle island Navmesh Found and Copied");
			
			
	print("Navmesh Island Check Complete - press any key to return to main menu");
	choice = input();		
		
			
def getLevelChoice(LEVELS_DIR):	
	global _LogFile
	print ("Standby - Creating the map list....");
	levelCnt = 0;
	maxScreenLen = 20;
	printRow = 1;
	choice = -1;
	NextScreenPage = (maxScreenLen * 2);
	list = os.listdir(LEVELS_DIR) # dir is your directory path
	number_files = len(list);
	MaxChoice = number_files; 
	pageCount = (number_files / (maxScreenLen * 2));  #number of pages
	if (pageCount > 1):
		NextScreenPage = NextScreenPage + maxScreenLen;
	#cls();	
	print("***********  Generating Map List *************");
		
	# if a small number of files display using a single row
	if (number_files <= maxScreenLen):
		for levelname in os.listdir(LEVELS_DIR): 
			levelCnt = (levelCnt + 1);
			print ("<%-2d> %-30s  " % (levelCnt, levelname));
	else:
		for levelname in os.listdir(LEVELS_DIR):
			levelCnt = (levelCnt + 1);
						
			# if last file
			if (levelCnt == number_files): 
				#print  normally with EOL
				print ("<%-2d> %-30s  " % (levelCnt, levelname));
			elif (printRow == 1):
				#print  Row 1 without EOL
				print ("<%-2d> %-30s  " % (levelCnt, levelname));
				#reset printRow to 2
				printRow = 2;

			else: 	
				#print Row 2 with EOL 
				print ("<%-2d> %-30s  " % (levelCnt, levelname));
				#reset printRow to 1
				printRow = 1;
				if (levelCnt == NextScreenPage):
					NextScreenPage = NextScreenPage + maxScreenLen;
					print("Press any key to continue to next page");
					inp = input();

	MaxLevelCnt = levelCnt;	
	#print ("<<0>> All listed maps");
	print("Choose a level number:");
	inp = input();
	if inp.isdigit(): 
		choice = int(inp);
	while ( choice < 1 or choice > MaxChoice):
		print("Whoops!  Try again:");
		inp = input();
		if inp.isdigit(): 
			choice = int(inp);
		
	
	#if (levelNum == 0):
	#	return "All";
		
	#process the listdir to get the level name
	levelCnt = 0;
	for levelname in os.listdir(LEVELS_DIR): 
		levelCnt = (levelCnt + 1);
		if (levelCnt == choice):
			return levelname;


def ChooseNavmeshMode():
	
	mesh_mode = 0;

	cls();
	print(">>>>>>> Choose Navmesh Mode:");
	print("(1) Infantry");
	print("(2) Vehicle");
	print("(3) Both");
	choice = input();
	while ( mesh_mode == 0):
		if (choice == "3"):
			navmeshModeName = "Both Infantry and Vehicle";
			_NavmeshModes = [ "Infantry", "Vehicle"];
			meshModInf = "Y";
			meshModVeh = "Y";
			break;
		elif (choice == "1"):
			navmeshModeName = "Infantry Only";
			_NavmeshModes = [ "Infantry"];	
			meshModInf = "Y";
			meshModVeh = "N";
			break;
		elif (choice == "2"):  
			navmeshModeName = "Vehicle Only";
			_NavmeshModes = ["Vehicle"];	
			meshModInf = "N";
			meshModVeh = "Y";
			break;
		else:
			print("Whoops!  Try again:");
			choice = input();
	mesh_mode = int(choice);
	return mesh_mode;		
		

	
def setFolderFilesMode( path, mode):
	return True;

def deleteFolderFiles( path ):
    return True;
	
def checkGTSdataWorkFiles ( WorkDir):
	global _LogFile	
	destWorkDir = WorkDir + "/GTSData/Meshes";
	if not os.path.isdir(destWorkDir):
		print(  "No GTSdata exists - Can not create navmesh");
		return False;
	elif not os.listdir(destWorkDir):
		print(  "No GTSdata exists - Can not create navmesh");
		return False;
	return True

def CopyGTSdataWorkFiles ( levelDir, WorkDir):
	global _LogFile

	# check for empty source folder - if empty display warning message and return;
	# Check for target empty folder - if not delete files
	# remove readonly from file
	srclevelDir = levelDir + "/GTSData/Meshes";
	destWorkDir = WorkDir + "/GTSData/Meshes";
	print(  "Copy GTSdata");
	print(  "From: " + srclevelDir);
	print( "To: " + destWorkDir);
	if not os.listdir(srclevelDir):

		print(  "No GTSdata to copy");
		print(    "Mod level folder: " );
		print(    srclevelDir );
		if not os.path.isdir(destWorkDir):
			print(  "No GTSdata exists - Can not create navmesh");
			return False;	
		elif not os.listdir(destWorkDir):
			print(  "No GTSdata exists - Can not create navmesh");
			return False;
 
	owd = os.getcwd();
	os.chdir(destWorkDir);
	for levelname in os.listdir(destWorkDir): 
		#levelpath = normpath(path.join(destWorkDir, levelname));
		os.chmod(levelname, 0o777);
		#print(filepath);
		#os.chmod(full_level_path, stat.S_IWRITE)
		os.remove(levelname);	
	os.chdir(owd);
	moveFolderFiles(srclevelDir, destWorkDir);
	return True	

def checkGTSdataOutputFiles ( destDir):
	global _LogFile	
	destOutputDir = destDir + "/GTSData/output";
	if not os.path.isdir(destOutputDir):
		print(  "No GTSdata folder exists - Can not create AI pathfinding");
		return False;
	elif not os.listdir(destOutputDir):
		print(  "No GTSdata files exists - Can not AI pathfinding");
		return False;
	return True	
	
def CopyGTSdataOutputFiles ( sourceDir, destDir):
	global _LogFile
	# Check for target empty folder - if not delete files
	
	sourceOutputDir = sourceDir + "/GTSData/output";
	destOutputDir = destDir + "/GTSData/output";
	print( "Copy GTSdata Output folder files");
	print(  "From: " + sourceOutputDir);
	print(  "To: " + destOutputDir);
	owd = os.getcwd();
	if (not path.isdir(destOutputDir)):
		os.makedirs(destOutputDir);
		print(  "Output Folder did not exist - created");
	#os.chdir(destOutputDir);
		#for levelname in os.listdir(destWorkDir): 
			#levelpath = normpath(path.join(destWorkDir, levelname));
		#	os.chmod(levelname, 0o777);
			#print(filepath);
			#os.chmod(full_level_path, stat.S_IWRITE)
		#	os.remove(levelname);
		#os.chdir(owd);
	# Check for source empty folder - if not error and return
	if os.listdir(sourceOutputDir):	
		copyOutputFolderFiles(sourceOutputDir, destOutputDir);
	else: 	
		print(  "Failed to copy GTSdata Output files");
		print(   "Mod level folder: " );
		print(  sourceOutputDir );
		print(   "Mesh level folder: "  );
		print(   destOutputDir );
		print ("GTSdata output is empty - nothing copied");
		return False;
	return True;			

def SetupNavWorkArea(levelName):
	global _LogFile
	global _Progress
	#global _LogProgressFile
	#print(    "Set up Nav Work Area");
	#print ("Setting up Navmesh work area");
	navmesh_dir = path.abspath(path.join(os.getcwd(),"."));
	print ("For selected Map: " + levelName);
	workDir = navmesh_dir + "/work/";
	#print(    "Set up Nav Work Area" + workDir);
	workLevelDir = workDir + levelName; 
	workGTSdataDir = workLevelDir + "/GTSData";
	workMeshDir = workGTSdataDir + "/meshes";
	logDir = workLevelDir + "/GTSData/logfiles";
	_LogFile = logDir + "/navmeshcontrol.log";
	#modLevelmesh = workMeshDir + levelName + "/GTSData/Meshes";
	#REM make sure work dir exists
	#check if navmesh folders exist - create if they don't



	if (not path.isdir(workDir)):
		os.makedirs(workDir);	
		print("Creating :" + workDir);
	
	if (not path.isdir(workLevelDir)):
		os.makedirs(workLevelDir);	
		print("Creating :" + workLevelDir);
		
	if (not path.isdir(workGTSdataDir)):
		os.makedirs(workGTSdataDir);
		print("Creating :" + workGTSdataDir);
		
	if (not path.isdir(workMeshDir)):
		os.makedirs(workMeshDir);
		print("Creating :" + workMeshDir);
		
	#if (not path.isdir(modLevelmesh)):
	#	os.makedirs(modLevelmesh);	
	#	print("Creating :" + modLevelmesh);
		
	if (not path.isdir(logDir)):
		os.makedirs(logDir);
		print("Creating :" + logDir);
	else:
		createLogBackups(logDir);
		#if not (path.exists(_LogProgressFile)):  
	_Progress = get_last_ProgLog();
		
	#elif (path.exists(_LogFile)):
	#	os.remove(_LogFile);
	#	print("Remove old Log file");
		
	return;

	#if not os.listdir(LEVELS_DIR):			

	#rem create the work\level name folder needed
	#if not exist work\%level_name% md work\%level_name%

	#rem check for GTSdtat\meshes - and delete if they exist
	#if exist work\%level_name%\GTSData\ goto del_GTSdata

	#rem create GTSData folder
	#echo setup navmesh\work\%level_name%\GTSData\
	#md work\%level_name%\GTSData\

	#goto copy_GTSdata

#convert End of Line from Unix format to Windows

		#os.remove(infantryFile);

def nextword(searchtxt, targetline):
	words_list = targetline.split();
	next_word = words_list[words_list.index(searchtxt) + 1];
	return next_word;

def strip_end(text, suffix):
	suffixLow = suffix.lower();
	textLow = text.lower();
	if (textLow.endswith(suffixLow)):	
		return text[:len(text)-len(suffix)];
	return "";

def SetUpNavStandInFile(ModFolder):
	global _LogFile
	cwd = os.getcwd();
	Nav_StandIn_conversion_file = cwd + "/Nav_Stand_in_conv.txt";
	Nav_StandIn_conversion_backup_file = cwd + "/Nav_Stand_in_conv.bak";
	Nav_statics_FilePath = ModFolder + "/Objects/nav_statics";
	if not path.exists(Nav_statics_FilePath):
		print(   "Nav Statics Folder Not found:");
		print (   Nav_StandIn_conversion_file);
		print ("Press a key to return to menu");
		choice = input();
	if path.exists(Nav_StandIn_conversion_backup_file):	
		os.remove(Nav_StandIn_conversion_backup_file);
	if path.exists(Nav_StandIn_conversion_file):
		print ("Nav Stand-In List already exist!  Do you want to overwrite? ");
		print ("Press 1 to continue or any other key to abort");
		choice = input();
		if choice != "1":
			return;
		copyfile(Nav_StandIn_conversion_file, Nav_StandIn_conversion_backup_file);
		os.remove(Nav_StandIn_conversion_file);	
		
	os.walk(Nav_statics_FilePath)
	with open(Nav_StandIn_conversion_file, 'w') as output_file:
		for root, dirs, files in os.walk(Nav_statics_FilePath):

			#iterate through them
			for i in dirs: 
				firstName = strip_end(i, "_nav");
				secondName = i;
				if firstName != "":
					output_file.write(firstName + " " + secondName + "\n");

	print ("Nav Stand in File Created: ");
	print (Nav_StandIn_conversion_file);

	
	return;
	
	
def createNavStandInList():
	global _LogFile
	cwd = os.getcwd();
	Nav_StandIn_conversion_file = cwd + "/Nav_Stand_in_conv.txt";
	NavSIdict = {};
	count = 0;
	print(   "Creating Navmesh Stand-In List");
	print(  "Nav Mesh stand-In file path: " + Nav_StandIn_conversion_file);
	
	if not path.exists(Nav_StandIn_conversion_file):
		print(   "Nav Stand-In List Not found");
		print ("Press any key to return to menu");
		choice = input();
		return NavSIdict;
		
	with open(Nav_StandIn_conversion_file, 'r') as Conv_file:
		for line in Conv_file:
			#if "rem" in line:
			#output_file.write(line);
			wordList=line.split(' ');
			if wordList[0].lower() != "rem":
				key = wordList[0];
				value = wordList[1].rstrip("\n\r");
				print("Key: ", key);
				print("Value: ",value);
				NavSIdict[key] = value;
				count+=1;
	print (str(NavSIdict));
	return NavSIdict;	
	
def setupStaticObjectsForNavmeshing(modLevelFolder):

	global _LogFile
	#StaticObjects.con
	staticObjectsPath = modLevelFolder + "/StaticObjects.con";
	staticObjectsBackupPath = modLevelFolder + "/StaticObjects.bak";
	if not path.exists(staticObjectsPath):
		print (   "Static Objecst file Not found:");
		print (staticObjectsPath);
		print ("Press any key to return to menu");
		choice = input();
		return;
	
	NavSIdict = createNavStandInList();
	if NavSIdict == {}:
		print ("Nav Stand in list not created - Press any key to return to menu");
		choice = input();
		return;	
	if path.exists(staticObjectsBackupPath):	
		os.remove(staticObjectsBackupPath);
	copyfile(staticObjectsPath, staticObjectsBackupPath);
	os.remove(staticObjectsPath);	
	
	#Object.create 
	
	#print(  "Updating StaticObjects.con File - This can take awhile");
	count = 0;
	with open(staticObjectsBackupPath, 'r') as input_file, open(staticObjectsPath, 'w') as output_file:
		for line in input_file:
			lineLC = line.lower();
			wordList=lineLC.split(' ');
			keyfound = 0;
			if wordList[0] == "rem":
				output_file.write(line);
			elif "object.create" in lineLC:
				#print ("object.create found");				

				for key, value in NavSIdict.items():
					#print ("Comparing " + key );
					if keyfound == 0:
						if key.lower() in lineLC:
							keyfound = 1;
							count += 1;
							print (key + " found - replacing with " + value);
							output_file.write("Object.create " + value + "\n" );	
							
				if keyfound == 0:
					output_file.write(line);
				
			else:
				output_file.write(line);	
				
	print ("Static Object file updated: ");
	print (staticObjectsPath);
	print ("Number of static objects replaced: " + str(count));
	return	
				

			
			
	
def createBF2142ConvList():

	global _LogFile
	cwd = os.getcwd();
	BF2142_spawn_conversion_file = cwd + "/editor_conv.txt";
	BF2142dict = {};
	count = 0;
	print(   "Creating BF2142 Conversion List");
	print (  "BF2142 Conversion file path: " + BF2142_spawn_conversion_file);
	
	if not path.exists(BF2142_spawn_conversion_file):
		print(   "BF2142 Conversion List Not found");
		return BF2142dict;
	with open(BF2142_spawn_conversion_file, 'r') as Conv_file:
		for line in Conv_file:
			#if "rem" in line:
			#output_file.write(line);
			wordList=line.split(' ');
			key = wordList[0];
			value = wordList[1].rstrip("\n\r");
			#print("Key: ", key);
			#print("Value: ",value);
			BF2142dict[key] = value;
			count+=1;
	#print (str(BF2142dict));
	return BF2142dict;
	
def cleanGPO(ModFolder):
# REM ObjectTemplate.setScatterSpawnPositions 1
# REM ObjectTemplate.teamOnVehicle
# Set layer to 1
# add combatarea.usedbypathfinding if missing
# change CP IDs = -1 to a correct number 

    global _LogFile
    global _CPList
    global _wCP_NameList	

    usedByPathFinding = False
    teamOnVehicle = False
    setScatterSpawnPositions = False

    GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
    GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";
    #print ("Clean GPO - Start")

    #print(  "clean Editor GPO");
    #logOnlyMsg(  "GPO path: " + GPO_FilePath);

    if not _CPList:
        getCP_NameList(ModFolder);
        build_CP_ID_name_list (ModFolder);
        
    createBackupFile (ModFolder + "/editor/", "GamePlayObjects.con")
    if path.exists(GPO_FilePathBackup):
        os.remove(GPO_FilePathBackup);
    copyfile(GPO_FilePath, GPO_FilePathBackup);
    os.remove(GPO_FilePath);
    print ("Cleaning :" + GPO_FilePath );
    print ("Backup :" + GPO_FilePathBackup );

    #ObjectTemplate.setObjectTemplate


    combatLayer = 0;
    indent = "";
    identset = False;
    offset = "   " # spaces to indent - current set to 3
    output_file = open(GPO_FilePath, 'w');
    currentOjbSpawnerName = "";
    with open(GPO_FilePathBackup, 'r') as input_file, open(GPO_FilePath, 'w') as output_file:	

        for line in input_file:
            tempLine = removeNonAscii(line)
            wordList=tempLine.split(' ');
            firstWord = wordList[0].lower().lstrip();
            lineLC = tempLine.lower();


            if "rem" in firstWord :
                #print ("rem found - output line and skip ");
                output_file.write(tempLine);
                

            elif "v_arg1" in lineLC:
                #print ("Indent Section started");
                identset = True;
                indent = offset;		
                output_file.write(tempLine);
                
            elif "endif" in lineLC:
                #print ("Indent Section ended");
                identset = False;
                indent = "";		
                output_file.write(tempLine);

            elif "object.create" in lineLC:
                if not wordList[1]:  # blank
                    tempLine = lineLC.lstrip();
                    wordList = tempLine.split(' ')
                    currentOjbSpawnerName =  wordList[1]
                else:
                    currentOjbSpawnerName = wordList[1].lower();
                if identset:
                    tempLine = indent + tempLine;
                output_file.write(tempLine);
                            
            elif "object.setcontrolpointid" in lineLC:
                CP_id = wordList[1];
                #print ("object.setcontrolpointid: " + CP_id)
                if "-1" in CP_id:
                    WriteLine = ""
                    for id, CPName in _CPList.items():
                        if CPName in currentOjbSpawnerName:
                            if not WriteLine:
                                output_file.write(indent + "ObjectTemplate.setControlPointId " + id + "\n")
                                WriteLine = 1;	
                else: 
                    output_file.write(tempLine);
                
            elif "objectemplate.setscatterspawnpositions" in lineLC:
                output_file.write(indent + "REM ObjectTemplate.setScatterSpawnPositions 1\n");
                setScatterSpawnPositions = True

            elif "objecttemplate.teamonvehicle" in lineLC:
                output_file.write(indent + "REM ObjectTemplate.teamOnVehicle 1\n");
                teamOnVehicle = True

            elif "object.layer" in lineLC:

                output_file.write(indent + "Object.layer 1\n");

            elif "combatarea.layer" in lineLC:
                combatLayer = 1;
                #print ("Combat layer found - next line should be usedbyPathfinding");
                output_file.write("CombatArea.layer 1\n");
            elif "combatarea.usedbypathfinding" in lineLC:
                #print ("usedbyPathfinding Line found");
                output_file.write(tempLine);
                combatLayer = 0;

            #elif combatLayer == 1:
            #	combatLayer = 0;
            #	print ("Pathfinding not found Line found - writing line to file");
            #	output_file.write("CombatArea.usedByPathFinding 1\n");
            else:	
                output_file.write(tempLine);
    if combatLayer == 1:
        #print ("CombatArea.usedByPathFinding not found - writing line to file");
        output_file.write("CombatArea.usedByPathFinding 1\n");
        usedByPathFinding = True
        
    output_file.close();

    print ("GPO Update complete");
    print ("- All layers set to 1")
    if (setScatterSpawnPositions):
        print ("- Set REM setScatterSpawnPositions") 
    if (teamOnVehicle):
        print ("- Set REM teamOnVehicle")    
    if (usedByPathFinding):
        print ("- Set UsedByPathFinding to Combat Area")
      
             
    return;	

def checkforOvergrowthFile(ModFolder):
    global _LogFile
    overgrowth_basePath = ModFolder + "/overgrowth";
    overgrowth_FilePath = overgrowth_basePath + "/overgrowthCollision.con";
    if not path.exists(overgrowth_basePath):
        os.makedirs(overgrowth_basePath);
    if not path.exists(overgrowth_FilePath):
        print ("Overgrowth file does not exist - creating");
        with open(overgrowth_FilePath, 'w') as output_file:
            output_file.write("\n");
    else:
        print ("Overgrowth file exists");
    return;
		
def chooseAIsettings(AIdata):
    global _Mod_Name
    global _MeshMode
    global _LogFile
    global _BF_Type #(BF2, BF2142)
    global _MechOption #(True, False)
    global _Vehicle_type #("Tank", "Armed Car", "Landing Craft")
    MaxChoice = 2;


    # cls();
    # print("*****************************");
    #print("Current Level setting: " + levelName);
    #print ("Current Navmesh settings: Infantry : Vehicle");
    #print ("Radius    : " + AIdata["inf_radius"] + " : " + AIdata["veh_radius"]) ;
    #print ("Max Slope : " + AIdata["inf_slope"] + " : " + AIdata["veh_slope"]) ;
    #print ("Head Clear: " + AIdata["inf_headclearance"] + " : " + AIdata["veh_headclearance"]) ;
    #print "Radius:     %-5s : %-5s" % (AIdata["inf_radius"], AIdata["veh_radius"]) ;
    #print "Max Slope:  %-5s : %-5s"% (AIdata["inf_slope"], AIdata["veh_slope"]) ;
    #print "Head Clear:  %-5s : %-5s"; % (AIdata["inf_headclearance"],AIdata["veh_headclearance"]) ;
    #print "<%-2d> %-30s  " % (levelCnt, levelname),
    #print("******************************");
    #print("*** Choose the Map type to determine the Navmesh settings ****");
    #print("*****************************");
    #print("(1) BF2 ");
    #print("(2) BF2142 ");
    # print("(3) Ca ");
    #print("(0) Return to Main Menu");

    #ans = input();
    #if ans.isdigit():
    #    choice = int(ans);
    #while ( choice < 0 or choice > MaxChoice):
    #    print("Whoops!  Try again:");
    #    ans = input();
    #    if ans.isdigit():
    #        choice = int(ans);
    #clean navmesh
    if ("BF2142" in _BF_Type):
        AIdata["inf_slope"] ="45";
        AIdata["veh_slope"] ="28";
        AIdata["inf_radius"] ="0.19";
        AIdata["veh_radius"] ="3.5";
        AIdata["inf_headclearance"] ="1.9";
        AIdata["veh_headclearance"] ="8";
        AIdata["inf_ThresholdHeight"] ="1.0";
        AIdata["veh_ThresholdHeight"]="0.1";
    elif ("BF2" in _BF_Type):
        AIdata["inf_slope"] ="45";
        AIdata["veh_slope"] ="28";
        AIdata["inf_radius"] ="0.19";
        AIdata["veh_radius"] ="3.5";
        AIdata["inf_headclearance"] ="";
        AIdata["veh_headclearance"] ="";
        AIdata["inf_ThresholdHeight"] ="";
        AIdata["veh_ThresholdHeight"]="";
    else:
        print ("BF Type not set propertly:");
        print (_BF_Type);
        print ("Program will end")
        return False;
    return True;
	
	
def CreateAiFile(AI_FilePath, AIdata):
	global _Mod_Name
	global _MeshMode
	global _LogFile

	if not chooseAIsettings(AIdata):
		return;
	
	with open(AI_FilePath, 'w') as output_file:
		output_file.write("rem ************** LEVEL SPECIFIC AI SETTINGS ***************************\n");
		output_file.write("\n");
		output_file.write("rem *** Init AI using current settings ****\n");
		output_file.write("ai.init 2\n");
		output_file.write("\n");
		output_file.write("aiPathfinding.setActiveMap Infantry\n");
		if AIdata["inf_headclearance"] =="":
			output_file.write("rem aiPathfinding.map.headClearance " + AIdata["inf_headclearance"] +"\n");
		else:	
			output_file.write("aiPathfinding.map.headClearance " + AIdata["inf_headclearance"] +"\n");
		if AIdata["inf_radius"] =="":
			output_file.write("rem aiPathfinding.map.radius " + AIdata["inf_radius"] +"\n");
		else:
			output_file.write("aiPathfinding.map.radius " + AIdata["inf_radius"] +"\n");
		if AIdata["inf_slope"] =="":	
			output_file.write("rem aiPathfinding.map.maxSlope " + AIdata["inf_slope"] +"\n");
		else:	
			output_file.write("aiPathfinding.map.maxSlope " + AIdata["inf_slope"] +"\n");
		if AIdata["inf_ThresholdHeight"] =="":
			output_file.write("rem aiPathfinding.map.allowedThresholdHeight " + AIdata["inf_ThresholdHeight"] +"\n");
		else:	
			output_file.write("aiPathfinding.map.allowedThresholdHeight " + AIdata["inf_ThresholdHeight"] +"\n");
			
		output_file.write("aiPathfinding.map.addVehicleForClusterCost Infantery\n");
		output_file.write("\n");
		output_file.write("aiPathfinding.setActiveMap Vehicle\n");
		if AIdata["veh_headclearance"] =="":
			output_file.write("rem aiPathfinding.map.headClearance " + AIdata["veh_headclearance"] +"\n");
		else:	
			output_file.write("aiPathfinding.map.headClearance " + AIdata["veh_headclearance"] +"\n");
		if AIdata["veh_radius"]	=="":
			output_file.write("rem aiPathfinding.map.radius " + AIdata["veh_radius"] +"\n");
		else:
			output_file.write("aiPathfinding.map.radius " + AIdata["veh_radius"] +"\n");
		if AIdata["veh_slope"] =="":
			output_file.write("rem aiPathfinding.map.maxSlope " + AIdata["veh_slope"] +"\n");
		else:
			output_file.write("aiPathfinding.map.maxSlope " + AIdata["veh_slope"] +"\n");
		if AIdata["veh_ThresholdHeight"] =="":	
			output_file.write("rem aiPathfinding.map.allowedThresholdHeight " + AIdata["veh_ThresholdHeight"] +"\n");
		else:	
			output_file.write("aiPathfinding.map.allowedThresholdHeight " + AIdata["veh_ThresholdHeight"] +"\n");
		output_file.write("aiPathfinding.map.addVehicleForClusterCost Tank\n");
		output_file.write("aiPathfinding.map.addVehicleForClusterCost ArmedCar\n");
		output_file.write("aiPathfinding.map.addVehicleForClusterCost LandingCraft\n");
		output_file.write("aiPathfinding.map.addVehicleForClusterCost Boat\n");

	return;	
	
def initAIdata():
	AIdata = {\
	"inf_radius":"0.19",\
	"inf_slope":"45",\
	"inf_headclearance":"",\
	"inf_thresholdheight":"",\
	"veh_radius":"3.5",\
	"veh_slope":"28",\
	"veh_headclearance":"","veh_thresholdheight":""}	

	
	return AIdata;
	

	
def checkAiFiles(ModFolder):
    #global _Mod_Name
    #global _MeshMode
    #global _LogFile
    AI_FilePath = ModFolder + "/ai/Ai.ai";
    AI_FilePathBackup = ModFolder + "/ai/Ai.bak";
    VT_Tank = 0;
    VT_car = 0;
    VT_LC = 0;
    VT_Boat = 0;
    ActiveMapType = "I"  #I or V - default is I for Infantry
    AIdata = initAIdata();
    infantry_found = 0;
    vehicle_found = 0;

    #print ("Ready to check for AI files as follows:");
    #print ("-Check for Overgrowth ");
    #print ("-Clean up editor GPO for AI");
    #print ("-Create AI\AI file if it does not exist");
    print ("Level Selected: " );
    print (ModFolder );
    print ("Press any key to Start");
    choice = input();
	
    checkforOvergrowthFile(ModFolder);

    cleanGPO(ModFolder )

	
    if not path.exists(AI_FilePath):
        print ("AI file does not exist - creating");
        CreateAiFile(AI_FilePath,AIdata);
    else:
        with open(AI_FilePath, 'r') as input_file:
            for line in input_file:
                lineLC = line.lower();
                if "aipathfinding.setactivemap" in lineLC:
                    #logOnlyMsg(   "found activemap");
                    if "infantry" in lineLC:
                        #logOnlyMsg(   "activemap type is infantry");
                        ActiveMapType = "I";
                        infantry_found = 1;
                    else:	
                        if "vehicle" in lineLC:
                            #logOnlyMsg(   "activemap type is vehicle");
                            ActiveMapType = "V";
                            vehicle_found = 1;
                elif "aipathfinding.map.maxslope" in lineLC:
                    info=line.split(' ')
                    #logOnlyMsg(   "maxslope found:" + info[1]);
                    if ActiveMapType == "I":
                        AIdata["inf_slope"] = info[1];
                    else:
                        AIdata["veh_slope"] = info[1];
                elif "aiPathfinding.map.headClearance" in lineLC:
                    info=line.split(' ')
                    #logOnlyMsg(   "headclearance found found:" + info[1]);
                    if ActiveMapType == "I":			
                        AIdata["inf_headclearance"] = info[1];
                    else:
                        AIdata["veh_headclearance"] = info[1];						
                elif "aipathfinding.map.radius" in lineLC:
                    info=line.split(' ')
                    #logOnlyMsg(   "radius found:" + info[1]);
                    if ActiveMapType == "I":
                        AIdata["inf_radius"] = info[1];
                    else:
                        AIdata["veh_radius"] = info[1];	
                elif "aipathfinding.map.allowedthresholdheight" in lineLC:
                    info=line.split(' ')
                    #logOnlyMsg(   "Thresholdheight found:" + info[1]);
                    if ActiveMapType == "I":
                        AIdata["inf_ThresholdHeight"] = info[1];
                    else:
                        AIdata["veh_ThresholdHeight"] = info[1];							
                elif "tank" in lineLC:
                    VT_Tank = 1;
                elif "armedcar" in lineLC:
                    VT_car = 1;
                elif "landingcraft" in lineLC:
                    VT_LC = 1;
                elif "boat" in lineLC:
                    VT_Boat = 1;
			
		#logOnlyMsg(   "VT_Tank:" + VT_Tank);		
		#logOnlyMsg(   "VT_car:" + VT_car);		
		#logOnlyMsg(   "VT_LC:" + VT_Tank);		
		#logOnlyMsg(   "VT_Boat:" + VT_Tank);		
	
        if 	(VT_Tank == 0 or VT_car == 0 or VT_LC == 0 or VT_Boat == 0 or vehicle_found == 0 or infantry_found == 0):
            if path.exists(AI_FilePathBackup):
                os.remove(AI_FilePathBackup);
                copyfile(AI_FilePath, AI_FilePathBackup);
                os.remove(AI_FilePath);
            CreateAiFile(AI_FilePath,AIdata );
				
        print ("AI file Check complete");
    return;
	
def create_SA_File(ModFolder):	
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _SA_CPList
	global _CPList
	global _SA_Value
	global _Veh_Search_Rad_mult
	global _CP_radius_list
	global _CP_team_list
	global _CP_Inf_Set_Order_list
	global _CP_Veh_Set_Order_list	
	global _Layer
	global _CP_PosList
	global _CP_hoistMinMax
	global _CP_TTGC
	global _CP_TTLC	
	
	
	cleanGPO(ModFolder);
	get_GPO_Info (ModFolder)
	print ("Create SA file")
	neighborList =[];
	timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S");
	SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
	SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
	tempFileName = "StrategicAreas" + timestamp + ".bak"
	SA_FilePathTimeBackup = ModFolder + "/editor/AI/" + tempFileName;
	print(   "Create Strategic Area file");
	print(   "SA path: " + SA_FilePath);

	if path.exists(SA_FilePathBackup):
		copyfile(SA_FilePathBackup, SA_FilePathTimeBackup);
		os.remove(SA_FilePathBackup);	
			
	if path.exists(SA_FilePath):
		copyfile(SA_FilePath, SA_FilePathBackup);
		os.remove(SA_FilePath);	
#rem *** Create strategic areas ***
#aiStrategicArea.createFromControlPoint CPNAME_RC_32_Central_Camp 4 50
#aiStrategicArea.layer 1
		
	with open(SA_FilePath, 'w') as output_file:
		output_file.write("rem *** Create strategic areas ***\n")

		# write the CP lines	
		for id, CPName in _CPList.items():
		
			neighborList = neighborList + [CPName]	
			output_file.write("aiStrategicArea.createFromControlPoint " + CPName + " " + id + " " + _SA_Value + "\n")
			output_file.write("aiStrategicArea.layer " + _Layer + "\n")
			output_file.write("\n")

#aiStrategicArea.setActive CPNAME_RC_32_Central_Camp
#aiStrategicArea.addObjectTypeFlag ControlPoint
#AIStrategicArea.setOrderPosition Infantry 94.864/22.29/90.91
#AIStrategicArea.setOrderPosition Vehicle 94.864/22.29/90.91
#aiStrategicArea.setSide 0
#aiStrategicArea.vehicleSearchRadius 45.2548

		# write the CP templates	
		for id, CPName in _CPList.items():	
			output_file.write("aiStrategicArea.setActive " + CPName + "\n")
			#write the neighbors
			for SAname in neighborList:
				if (SAname not in CPName):
					output_file.write("aistrategicarea.addneighbour " + SAname + "\n");
			output_file.write("aiStrategicArea.addObjectTypeFlag ControlPoint" + "\n")
			output_file.write("AIStrategicArea.setOrderPosition Infantry " + _CP_Inf_Set_Order_list[id] + "\n")
			output_file.write("AIStrategicArea.setOrderPosition Vehicle " + _CP_Inf_Set_Order_list[id] + "\n")
			output_file.write("aiStrategicArea.setSide " + _CP_team_list[id] + "\n")
			vehSearchRad = int(_CP_radius_list[id]) * _Veh_Search_Rad_mult
			output_file.write("aiStrategicArea.vehicleSearchRadius %2.2f \n"% (vehSearchRad) )
			output_file.write("\n")
			
			
	
def update_SA_CPList (ModFolder):
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _SA_CPList
	global _CPList
	SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
	SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
	print(   "Update Strategic Area file ");
	print(   "SA path: " + SA_FilePath);
	if not path.exists(SA_FilePath):
		print( "SA path: " + SA_FilePath);
		print(  "SA Path not found");
		_SA_CPList = []
		print (" Error - Action Canceled. Press a key to return to menu");
		choice = input();
		return;
		
	if path.exists(SA_FilePathBackup):
		os.remove(SA_FilePathBackup);
	copyfile(SA_FilePath, SA_FilePathBackup);
	os.remove(SA_FilePath);		
		
	with open(SA_FilePathBackup, 'r') as input_file, open(SA_FilePath, 'w') as output_file:
		for line in input_file:
			lineLC = line.lower();
			wordList=line.split(' ');
			
			firstWord = wordList[0].lower();
			
			if "rem" in firstWord :
				rem_found = "1"			

			
			elif "aistrategicarea.createfromcontrolpoint" in lineLC:
				CP_Name = wordList[1];
				CP_Id = wordList[2];
				CP_Value = wordList[3];
				if "-1" in CP_Id:
				
					for id, CPName in _CPList.items():
						if CP_Name in CPName:
							output_file.write("ObjectTemplate.setControlPointId " + id + "\n")

					#return;
					#print (" Error - Invalid CP ID = -1 found. Press a key to return to menu");
					#choice = input();					
				if not CP_Name in _SA_CPList:
						
					CP_NameLC = CP_Name.strip().lower()
					print ("Searching for : " + CP_NameLC)
					for id, CPName in _CPList.items():
						if CP_Name in CPName:
							output_file.write("ObjectTemplate.setControlPointId " + id + "\n")					 
			else: output_file.write(line)	

	
	return;	

# check SA file for valid CPs (not -1)	
def check_SA_CPList (ModFolder):
    global _Mod_Name
    global _MeshMode
    global _LogFile
    global _SA_CPList
    SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
    SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
    print(    "Check Strategic Area file ");
    #print(   "SA path: " + SA_FilePath);
    if not path.exists(SA_FilePath):
        print(   "SA Path not found");
        print(  "SA path: " + SA_FilePath);
        _SA_CPList = []
        print (" Error - Action Canceled. Press a key to return to menu");
        choice = input();
        return False

    with open(SA_FilePath, 'r') as SAinput_file:
        for line in SAinput_file:
            lineLC = line.lower();
            wordList=line.split(' ');
            firstWord = wordList[0].lower();
            if "rem" in firstWord :
                rem_found = "1"			

            elif "aistrategicarea.createfromcontrolpoint" in lineLC:
                CP_Name = wordList[1];
                CP_Id = wordList[2];
                CP_Value = wordList[3];
                if "-1" in CP_Id:
                    _SA_CPList = []
                    SAinput_file.close();
                    print (" Error - Invalid CP ID = -1 found. Press a key to return to menu");
                    choice = input();
                    return False;					
                if not CP_Name in _CPList:
                    _CPList[CP_Id] = CP_Name				
    SAinput_file.close();
    print ("Stategic Area check complete - no issues found")
    return;	
		
# get SP list from SA file
def get_SA_CPList (ModFolder):
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _SA_CPList
#ObjectTemplate.setControlPointName CPNAME_SS_64_IndustrialHarbor
#ObjectTemplate.team 2
#ObjectTemplate.controlPointId 309
#ObjectTemplate.unableToChangeTeam 1
#ObjectTemplate.supplyGroupId 0
#ObjectTemplate.hoistMinMax 0.2/0.9

#rem [SpawnPointTemplate: CPNAME_OS_64_CommandCenter_3_0]
#ObjectTemplate.create SpawnPoint CPNAME_OS_64_CommandCenter_3_0
#ObjectTemplate.activeSafe SpawnPoint CPNAME_OS_64_CommandCenter_3_0
#ObjectTemplate.modifiedByUser "Administrator"
#ObjectTemplate.isNotSaveable 1
#ObjectTemplate.setSpawnPositionOffset 0/1.25/0
#ObjectTemplate.setControlPointId 5
#aiStrategicArea.createFromControlPoint CPNAME_RC_32_Harbor 2 50


	SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
	SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
	print(    "Check Strategic Area file for neighbors");
	#print(   "SA path: " + SA_FilePath);
	if not path.exists(SA_FilePath):
		print(   "SA Path not found");
		print(  "SA path: " + SA_FilePath);        
        
		_SA_CPList = []
		print (" Error - Action Canceled. Press a key to return to menu");
		choice = input();
		return;

	with open(SA_FilePath, 'r') as SAinput_file:
		for line in SAinput_file:
			lineLC = line.lower();
			wordList=line.split(' ');	

			firstWord = wordList[0].lower();
			
			if "rem" in firstWord :
				rem_found = "1"			
			
			elif "aistrategicarea.createfromcontrolpoint" in lineLC:
				CP_Name = wordList[1];
				CP_Id = wordList[2];
				CP_Value = wordList[3];
				if "-1" in CP_Id:
					_SA_CPList = []
					SAinput_file.close();
					return;
					print (" Error - Invalid CP ID = -1 found. Press a key to return to menu");
					choice = input();					
				if not CP_Name in _SA_CPList:
					 _SA_CPList[CP_Id] = CP_Name			


	SAinput_file.close();
	
	return;	
	
def add_CP_List(CP_Id, CP_name):
	global _CPList
	temp_CP_ID = CP_Id;
	
	if CP_Id not in _CPList:
		_CPList[CP_Id] = CP_name
		
def checkUnicode(line):
	global _unicodeFound
	if not _unicodeFound:  # only ask once.
		if isinstance(line, unicode):
			print ("WARNING: Non standard English characters found.")
			print ("If you do not want to have those characters stripped out, then abort and fix the GPO file ");
			print ("Otherwise, Press a key to Continue.")
			choice = input();
			_unicodeFound = "True"
			return "True"	
		else:
			return ""	
		

#Get a list of CP Names from the GPO, sorted by Length		
def getCP_NameList(ModFolder):
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _CPList
	global _CP_NameList
	global _unicodeFound

	
	#print ("print Get CP Name List from GPO");
	if _CPList:
		#print ("CP List already set")
		return;

	temp_CP_List = [];
	CP_Found = ""
	GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
	#GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";	

	if not path.exists(GPO_FilePath):
		print ("Not Found: ")
		print (GPO_FilePath)
		print ("Press a key to abort");
		choice = input();
		return;		
	with open(GPO_FilePath, 'r') as input_file:
		for line in input_file:
			#checkUnicode(line)
				
			lineLC = line.lower();
			wordList=line.split(' ');
			#print (line)
			firstWord = wordList[0].lower();
			
			if "rem" in firstWord :  #skip
				rem_found = "1"

			elif "objecttemplate.create controlpoint" in lineLC:	# control point template
				CP_Found = "1"
				CurrentControlPointName = removeNonAscii(wordList[2].lower())
				#wwprint ("objecttemplate.create controlpoint: " + CurrentControlPointName)
				
				temp_CP_Name = CurrentControlPointName.rstrip()
				if temp_CP_Name not in temp_CP_List:
					temp_CP_List.append(temp_CP_Name)

	#print ("Unsorted CP Name List");			
	#print (temp_CP_List)				
			
	_CP_NameList = sorted(temp_CP_List, key=len, reverse = True)
	#print ("Sorted CP Name List");			
	#print (_CP_NameList)
	input_file.close();
	#check_SA_CPList (ModFolder)
	#print ("Press a key to continue");
	#choice = input();

	return;

# Build the Control Point ID name list from GPO	
def build_CP_ID_name_list (ModFolder):	
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _CPList
	global _CP_NameList

	CP_ID_tracker_list =[]
	#print ("build_CP_ID_name_list")
	#get a basic list of CP Names from the GPO CP templates
	if _CPList:
		print ("CP List already set")
		return;

	temp_CP_List = {};
	CP_Found = ""
	curObjTemplateName = ""
	GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
	#GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";	

	if not path.exists(GPO_FilePath):
		print ("Not Found: ")
		print (GPO_FilePath)
		print ("Press a key to abort");
		choice = input();
		return;	
		
	with open(GPO_FilePath, 'r') as input_file:
		for tempLine in input_file:
			line = removeNonAscii(tempLine).lstrip()
			lineLC = line.lower();
			wordList=line.split(' ');
			wordListLC = lineLC.split(' ');
			firstWord = wordList[0].lower();	
			if "rem" in firstWord:
				rem_found = "1";

			elif "object.create" in lineLC:  # spawner
				tempName = wordList[1]
				curObjTemplateName = tempName.lower()
				#print ("Current Object template " + curObjTemplateName)
				#curObjTemplateName = tempName.rstrip()
				#print (line)
				
			elif "objecttemplate.setcontrolpointid" in lineLC :   # spawner
				
				CP_ID = wordList[1].rstrip()
				#print ("CP ID Found: " + CP_ID)
				if CP_ID not in CP_ID_tracker_list:
					if not "-1" in CP_ID:  # Make sure CP ID is not -1
						CP_ID_tracker_list.append(CP_ID)
						for CP_name in _CP_NameList:  # Loop through the CP Name list
							#print ("CP Name: " + CP_name )

							if CP_name in curObjTemplateName:  # If CP Name is found in the Object Template name
								#print ("CP Name in current : " + CP_name )
								if CP_name not in _CPList:   # does CP ID already exist in CP ID name list
									#print ("Add to CPList: "+ CP_ID + " " +  CP_name);
									_CPList[CP_ID] = CP_name
					


	#print ("CP name and ID List:")			
	#print (	_CPList)
	input_file.close();


	return;
	
def get_current_CP_ID (currentCPName):	
	global _CP_NameList
	CP_NameLC = currentCPName.lower()
	#print ("Get Current CP ID")
	for id, CPName in _CPList.items():
		#print ("ID " + id + "CPname " + CPName )
		#print ("CPNameLC " + CPName.lower())
		#print ("Current CP Name LC " + CP_NameLC)
		if CPName.lower() in CP_NameLC:
			return id;
		else:
			print ("CP ID Not found - CP List:")
			print (_CPList)
			

	return ""
		
	
def get_GPO_Info (ModFolder):
	global _Mod_Name
	global _MeshMode
	global _LogFile
	global _CPList
	global _CP_NameList
	global _SA_CPList
	global _CP_radius_list
	global _CP_team_list
	global _CP_Inf_Set_Order_list
	global _CP_Veh_Set_Order_list	
	global _Layer
	global _CP_PosList
	global _CP_hoistMinMax
	global _CP_TTGC
	global _CP_TTLC	
		
	#get a basic list of CP Names from the GPO CP templates
	getCP_NameList(ModFolder)
	build_CP_ID_name_list (ModFolder)
	CP_Found = ""  # CP template section flag
	GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
	#GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";	
	current_CP_ID = ""
	print ("Get GPO Info - start")

	if not path.exists(GPO_FilePath):
		print ("Not Found: ")
		print (GPO_FilePath)
		print ("Press a key to abort");
		choice = input();
		return;		
	with open(GPO_FilePath, 'r') as input_file:
		for line in input_file:
			
			lineLC = line.lower();
			lineStripLC = lineLC.lstrip()
			wordList=line.lstrip().split(' ');
			wordListStripLC=lineStripLC.split(' ');
			firstWord = wordListStripLC[0]
			print (lineLC)
			if "rem" in firstWord :
				rem_found = "1"
			
			elif "objecttemplate.create controlpoint" in lineLC:  # control point template
				currentCPName = wordList[2].rstrip();
				current_CP_ID = get_current_CP_ID (currentCPName)
				#print ("currentCPName: " + currentCPName)
				#print ("current CP ID: " + current_CP_ID)				
				if current_CP_ID == "":
					print ("Could not determine CP ID - Abort")
					choice = input();
					exit
					
				CP_Found = "1"
				
			elif "object.create" in lineLC:
				#print (" Object.create")			
				if CP_Found == "1":
					currentCPName = wordList[1].rstrip();
					current_CP_ID = get_current_CP_ID (currentCPName)

					#print ("currentCPName: " + currentCPName)
					#print ("current CP ID: " + current_CP_ID)
	
#			elif "objecttemplate.controlpointid" in lineLC :
#				print (" objecttemplate.controlpointid")	
#				if CP_Found == "1":
#					current_CP_ID = wordList[1].rstrip()
#w					print ("current CP ID: " + current_CP_ID)					
						
			elif "objecttemplate.radius" in lineLC:	
				
				if CP_Found == "1":
					if current_CP_ID == "":
						current_CP_ID = get_current_CP_ID (currentCPName)
					_CP_radius_list[current_CP_ID] = wordList[1].rstrip();
					#print (" radius " + wordList[1].rstrip())	
										
					#print ("current CP Name: " + currentCPName)
					#print ("current CP ID: " + current_CP_ID)

			elif "objecttemplate.team" in lineLC:
				if CP_Found == "1":
					if current_CP_ID == "":

						current_CP_ID = get_current_CP_ID (currentCPName)
					_CP_team_list[current_CP_ID] = wordList[1].rstrip();
					#print (" team " + wordList[1].rstrip() )					
					#print ("current CP Name: " + currentCPName)
					#print ("current CP ID: " + current_CP_ID)					
		

			elif "object.absoluteposition" in lineLC:
				if CP_Found == "1":	
					if current_CP_ID == "":

						current_CP_ID = get_current_CP_ID (currentCPName)				
					_CP_Inf_Set_Order_list[current_CP_ID] = wordList[1].rstrip();
					_CP_Veh_Set_Order_list[current_CP_ID] = wordList[1].rstrip();
					_CP_PosList[current_CP_ID] = wordList[1].rstrip();
					#print ("current CP Name: " + currentCPName)
					#print ("current CP ID: " + current_CP_ID)					
					

			elif "objecttemplate.hoistminmax" in lineLC:  
				if current_CP_ID == "":

					current_CP_ID = get_current_CP_ID (currentCPName)			
				_CP_hoistMinMax[current_CP_ID] = wordList[1].rstrip();
				#print ("current CP Name: " + currentCPName)
				#print ("current CP ID: " + current_CP_ID)				
				
			elif "Objecttemplate.timetogetcontrol" in lineLC: 
				if current_CP_ID == "":
					#print ("current CP Name: " + currentCPName)
					#print ("current CP ID: " + current_CP_ID)
					current_CP_ID = get_current_CP_ID (currentCPName)			
				_CP_TTGC[current_CP_ID] = wordList[1].rstrip();	

			elif "Objecttemplate.timetolosecontrol" in lineLC:  
				if current_CP_ID == "":

					current_CP_ID = get_current_CP_ID (currentCPName)			
				_CP_TTLC[current_CP_ID] = wordList[1].rstrip();
				#print ("current CP Name: " + currentCPName)
				#print ("current CP ID: " + current_CP_ID)					


					
					
				

				
	#print (	_CPList)
	input_file.close();
	print ("GPO get info complete");
	#print ( _CPList)
	#print ( _CP_NameList)

	#print ( _CP_radius_list)
	#print ( _CP_team_list)
	#print ( _CP_Inf_Set_Order_list)
	#print ( _CP_Veh_Set_Order_list)	
	#print ( _Layer)
	#print ( _CP_PosList)
	#print ( _CP_hoistMinMax)
	#print ( _CP_TTGC)
	#print ( _CP_TTLC	)
	print ("Press a key to continue");
	choice = input();
	return;
	
	

def FixBF2142GPO(ModFolder):
    global _Mod_Name
    global _MeshMode
    global _LogFile
    global _CPList
    global _CP_NameList
    global _SA_CPList
    global _CP_radius_list
    global _CP_team_list
    global _CP_Inf_Set_Order_list
    global _Layer


    temp_CP_List = {};
    GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
    GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";
    print (   "Making GPO editor friendly");
    #print(  "GPO path: " + GPO_FilePath);
    BF2142dict = createBF2142ConvList();
    if not BF2142dict:
        print ("Press a key to abort");
        choice = input();
        return;
	#Check for
    if not path.exists(GPO_FilePath):
        print ("Not Found: ")
        print (GPO_FilePath)
        print ("Press a key to abort");
        choice = input();
        return;		
	
    if path.exists(GPO_FilePathBackup):
        os.remove(GPO_FilePathBackup);
    copyfile(GPO_FilePath, GPO_FilePathBackup);
    os.remove(GPO_FilePath);	
	#ObjectTemplate.setObjectTemplate
	#ObjectTemplate.create ControlPoint
	#ObjectTemplate.controlPointId 6
#ObjectTemplate.physicsType Mesh
#rem -------------------------------------
#ObjectTemplate.addTemplate flagpole
#rem -------------------------------------

#ObjectTemplate.setControlPointName CPNAME_SS_64_IndustrialHarbor
#ObjectTemplate.team 2
#ObjectTemplate.controlPointId 309
#ObjectTemplate.unableToChangeTeam 1
#ObjectTemplate.supplyGroupId 0
#ObjectTemplate.hoistMinMax 0.2/0.9

#rem [SpawnPointTemplate: CPNAME_OS_64_CommandCenter_3_0]
#ObjectTemplate.create SpawnPoint CPNAME_OS_64_CommandCenter_3_0
#ObjectTemplate.activeSafe SpawnPoint CPNAME_OS_64_CommandCenter_3_0
#ObjectTemplate.modifiedByUser "Administrator"
#ObjectTemplate.isNotSaveable 1
#ObjectTemplate.setSpawnPositionOffset 0/1.25/0
#ObjectTemplate.setControlPointId 5
	
    flagpoleFound  = False;
    controlPointIDFound = False;
    ControlPointName ="";
    current_CP_ID =0;
    
    with open(GPO_FilePathBackup, 'r') as input_file, open(GPO_FilePath, 'w') as output_file:
        for line in input_file:
            lineLC = line.lower();
            wordList=line.split(' ');
            keyfound = 0;
            if "flagpole" in lineLC:	
                flagpoleFound = True;
                output_file.write(line);
            elif "object.create" in lineLC:	
                temp_CP_Name = wordList[1];
                output_file.write(line);
            elif "Object.setControlPointId" in lineLC:
                temp_CP_ID = wordList[1];
                current_CP_ID = temp_CP_ID 
                if temp_CP_ID not in temp_CP_List:
                    temp_CP_List[temp_CP_ID] = temp_CP_Name
            elif "objecttemplate.create controlpoint" in lineLC:	
                ControlPointName = wordList[2];
                #print ("CP name: " + ControlPointName)
                output_file.write(line);
            elif "objecttemplate.setcontrolpointid" in lineLC:
                if "-1" in wordList[1]:
                    for id, CPName in temp_CP_List.items():
                        if ControlPointName in CPName:
                            output_file.write("ObjectTemplate.setControlPointId " + id+ "\n")
                            current_CP_ID = id					
                            _CPList[id] = ControlPointName
                elif not ControlPointName =="" :
                    controlPointIDFound = True;
                    #print ("ID line found")
                    output_file.write(line);
            elif "objecttemplate.radius" in lineLC:	
                _CP_radius_list[current_CP_ID] = wordList[1];
                output_file.write(line);
            elif "objecttemplate.team" in lineLC:
                _CP_team_list[current_CP_ID] = wordList[1];
                output_file.write(line);
            elif "object.absoluteposition" in lineLC:
                _CP_Inf_Set_Order_list[current_CP_ID] = wordList[1];
                output_file.write(line);				
            elif "object.layer" in lineLC:
                _Layer = wordList[1];
                output_file.write(line);
            elif "objecttemplate.hoistminmax" in lineLC:  #end of Control point definition
                #print ("hoistminmax Found - ")
                if flagpoleFound == False:
                    output_file.write("rem -------------------------------------\n");
                    output_file.write("ObjectTemplate.addTemplate flagpole\n");
                    output_file.write("rem -------------------------------------\n");
                else: flagpoleFound = False;
                if 	controlPointIDFound == False:
                    #print ("CP ID line not found")
                    CP_NameLC = ControlPointName.strip().lower()
                    #print ("Searching for : " + CP_NameLC)
                    for id, CPName in temp_CP_List.items():
                        if ControlPointName in CPName:
                            output_file.write("ObjectTemplate.setControlPointId " + id + "\n")
                            _CPList[id] = ControlPointName
                            controlPointIDFound = True
                            ControlPointName =""
                else: controlPointIDFound = False
                output_file.write(line);
            elif "objecttemplate.setobjecttemplate" in lineLC:
                #print ("ObjectTemplateLine found");
				#info=line.split(' ');
				#for key, value in BF2142dict.items():
                for key, value in BF2142dict.items():
                    #print ("Comparing " + key );
                    if keyfound == 0:
                        if key.lower() in lineLC:
                            keyfound = 1;
                            #print (key + " found - replacing with " + value);
                            output_file.write("ObjectTemplate.setObjectTemplate " + wordList[1] + " " + value + "\n" );	
                if keyfound == 0:
                    output_file.write(line);	
            else:
                output_file.write(line);
    #print (	_CPList)
    check_SA_CPList (ModFolder)
    print ("GPO Update complete");		
    return;	
	
def parse_coordinates(input_line, coordinate_list ):
#returns the adjusted coordinates in string format
# receives a line in this format
#Object.absolutePosition -75.017/28.021/136.579 
# splits line into temp_list[0] = Object.absolutePosition  temp_list[0] = -75.017/28.021/136.579 
#splits -75.017/28.021/136.579  coord_list[0] = -75.017 ...
#splits -75.017 x_value[0] = -75 x_value[1] = 017
#adds the offsets to the int value only
# creates new string with updated coordinates in the format ###.###/###.###/###.###
#absolutePosition
    temp_list = input_line.split("absoluteposition")
    coord_list = temp_list[1].split("/")
    x_value = coord_list[0].split(".") #split float value into int and decimal
    z_value = coord_list[1].split(".") #split float value into int and decimal
    y_value = coord_list[2].split(".") #split float value into int and decimal
    x_adjusted = int(x_value[0]) + int(coordinate_list[0])  #add only to the int value
    z_adjusted = int(z_value[0]) + int(coordinate_list[1])  #add only to the int value
    y_adjusted = int(y_value[0]) + int(coordinate_list[2])  #add only to the int value
    x_coord = ( str(x_adjusted) + "."  + x_value[1] )
    y_coord = ( str(y_adjusted) + "."  + y_value[1] )  
    z_coord = ( str(z_adjusted) + "."  + z_value[1] ) 
    new_coord = (x_coord + "/"+ z_coord + "/" + y_coord ) 
    return new_coord

def set_offsets():
    coordinate_list =[]
    print ("Set the offsets for the format as shown:")
    print ("Example:-75.017/28.021/136.579  x/z/y with Z being height")
    print ("Enter X Offset as an integer:")
    x_offset = input();
    print ("Enter Z Offset as an integer:")
    z_offset = input();    
    print ("Enter Y Offset as an integer:")
    y_offset = input();
    coordinate_list.append(x_offset)
    coordinate_list.append(y_offset)
    coordinate_list.append(z_offset)    
    return coordinate_list

def apply_offsets_menu(ModFolder):
    coordinate_list =[]
    coordinate_list = set_offsets()
    maxchoice =0
    minchoice =3
    exitMenu = False
    while exitMenu:
        cls()
        print ("X Offset:" + coordinate_list[0])
        print ("X Offset:" + coordinate_list[1])    
        print ("Y Offset:" + coordinate_list[2])

        print ("Applying Offsets Menu")
        print ("(1) Change offsets")
        print ("(2) Apply to Map editor folder GPO file")
        print ("(3) Apply to Map Static Object file") 
        print ("(0) Return to Main Menu")
        print ("Choose an option ")
        temp = input()
        choice = integer(temp)
        if choice == 0:
            return
        elif choice == 1:
            coordinate_list = set_offsets()
        elif choice == 2:
            apply_offsets_GPO(ModFolder, coordinate_list)
        elif choice == 3:
            apply_offsets_SO(ModFolder, coordinate_list)
        else:
            print ("Invalid Choice - Press Enter to Try again")
            choice = input()
    return


def apply_offsets_GPO(ModFolder, coordinate_list):	
# Apply offsets to absolute postions in GPO	 and static objects
#Object.absolutePosition -75.017/28.021/136.579  x/z/y with Z being height
    print ("Applying Offsets to GPO")	
    print ("This will update the GPO in the selected map editor folder")
    print ("GamePlayObjects.bak will be created as a backup")
    GPO_FilePath = ModFolder + "/editor/GamePlayObjects.con";
    GPO_FilePathBackup = ModFolder + "/editor/GamePlayObjects.bak";
    #print(  "GPO path: " + GPO_FilePath);
    if not path.exists(GPO_FilePath):
        print ("Not Found: ")
        print (GPO_FilePath)
        print ("Press a key to abort");
        choice = input();
        return;		
	
    if path.exists(GPO_FilePathBackup):
        os.remove(GPO_FilePathBackup);
    copyfile(GPO_FilePath, GPO_FilePathBackup);
    os.remove(GPO_FilePath);	
    indent_setting = "   ";
    indent_on =False;

    with open(GPO_FilePathBackup, 'r') as input_file, open(GPO_FilePath, 'w') as output_file:
        for line in input_file:
            print (line)
            lineLC = line.lower();
            wordList=line.split(' ');
            keyfound = 0;
            if "if v_arg1 == host" in lineLC:
                indent_on = True
                output_file.write(line);
            elif "endif" in lineLC:	
                indent_on = False
                output_file.write(line);
            elif "object.absoluteposition" in lineLC:
                new_coord = parse_coordinates(lineLC, coordinate_list )
                if (indent_on):
                    new_line = (indent_setting + "Object.absolutePosition " + new_coord + "\n")
                else:
                    new_line = ( "Object.absolutePosition " + new_coord + "\n")
                print (new_line);
                output_file.write(new_line);                    

            else:
                output_file.write(line);
    print ("Update complete");	
    print ("Press any key to return to menu");
    choice = input(); 
		
		
def apply_offsets_SO(coordinate_list):	
# Apply offsets to absolute postions in static objects file
#Object.absolutePosition -75.017/28.021/136.579  x/z/y with Z being height
    print ("Applying Offsets to static objects file (SO)")	
    print ("This will update the SO in the selected map folder")
    print ("StaticObjects.bak will be created as a backup")
    staticObjectsPath = ModFolder + "/StaticObjects.con";
    staticObjectsBackupPath = ModFolder+ "/StaticObjects.bak";
    if not path.exists(staticObjectsPath):
        print (   "Static Objecst file Not found:");
        print (staticObjectsPath);
        print ("Press any key to return to menu");
        choice = input();
        return;
    if path.exists(staticObjectsBackupPath):	
        os.remove(staticObjectsBackupPath);
    copyfile(staticObjectsPath, staticObjectsBackupPath);
    os.remove(staticObjectsPath);	
    with open(staticObjectsBackupPath, 'r') as input_file, open(staticObjectsPath, 'w') as output_file:
        for line in input_file:
            lineLC = line.lower();
            wordList=lineLC.split(' ');
            keyfound = 0;
            if "object.absoluteposition" in lineLC:
                new_coord = parse_coordinates(coordinate_list )
                new_line = ("Object.absolutePosition " + new_coord + "\n")
                print (new_line);
                output_file.write(new_line);                    
            else:
                output_file.write(line);
    print ("Update complete");	
    print ("Press any key to return to menu");
    choice = input();                 
    return;	
			
def AddNeighborsToSAfile(ModFolder):	

#rem *** Create strategic areas ***
#aiStrategicArea.createFromControlPoint CP_BS_AntiAirBase 106 50
#aiStrategicArea.layer 2

#aiStrategicArea.setActive CP_BS_AntiAirBase
#AIStrategicArea.addNeighbour CP_BS_USBASE
#aiStrategicArea.addObjectTypeFlag ControlPoint
#AIStrategicArea.setOrderPosition Infantry -83.467/28.398/-241.872
#AIStrategicArea.setOrderPosition Vehicle -83.467/28.398/-241.872
#aiStrategicArea.setSide 0
#aiStrategicArea.vehicleSearchRadius 2.82843

	global _Mod_Name
	global _MeshMode
	global _LogFile
	SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
	SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
	print (   "Adding Neighbors to SA file");
	print (  "SA path: " + SA_FilePath);

	#Check for
	
	if path.exists(SA_FilePathBackup):
		os.remove(SA_FilePathBackup);
	copyfile(SA_FilePath, SA_FilePathBackup);
	os.remove(SA_FilePath);	
	
	SAlist =[];
	LayerSearchfield = "aiStrategicarea.layer"
	SASearchfield = "aistrategicarea.createfromcontrolpoint"
	SAactiveSearchField = "aistrategicarea.setactive"
	AddNeighborText = "aistrategicarea.addneighbour ";
	NeighborSearchText = "aistrategicarea.addneighbour";
	
	with open(SA_FilePathBackup, 'r') as input_file, open(SA_FilePath, 'w') as output_file:
		for line in input_file:
			lineLC = line.lower();	
			info=line.split(' ');
	
			#if "rem" in line:
			#output_file.write(line);
			#aiStrategicArea.layer 1
			#print(  line  );
			if "aistrategicarea.layer" in lineLC:
				output_file.write("aiStrategicArea.layer 1\n");
				
			elif SASearchfield in lineLC:
				
				SAname = info[1].rstrip("\n\r");
				#SAname = nextword(SASearchfield, lineLC);
				#print(  "Found SA: "  );
				#print(  line  );
				#print(  SAname );
				SAlist = SAlist + [SAname];
						
				output_file.write(line);
			#elif LayerSearchfield in line:
			#	output_file.write(line);
			
			elif SAactiveSearchField in lineLC:
				#print(  "Found active search field: "  );
				#print(  line  );
				currentSA = info[1].rstrip("\n\r");
				
				#print(   "Current SA:" + currentSA );
				#currentSA = nextword(SAactiveSearchField, line)
				output_file.write(line);
				for SAname in SAlist:
					#print(  "Found active search field: "  );
					#print( "SA Name: " + SAname );
					if (SAname != currentSA):
						output_file.write(AddNeighborText + SAname + "\n");
			elif NeighborSearchText in lineLC:
				#print(  "Neighbor line skipped: "  );
				neighbor = 1;  # do nothing line - skips printing the neighbor line
			else:
				#print(  "Write line out without edits: "  );
				#print(  line  );
				output_file.write(line);
	print ("Stratgic Area File Update complete");
			
				
	return;


	
	
def CheckSAFile(ModFolder):
	global _Mod_Name
	global _MeshMode
	global _LogFile

	NeighborSearchField = "aistrategicArea.addneighbour";

	SA_FilePath = ModFolder + "/editor/AI/StrategicAreas.AI";
	SA_FilePathBackup = ModFolder + "/editor/AI/StrategicAreas.bak";
	#print(   "Check Strategic Area file for neighbors");
	#print(   "SA path: " + SA_FilePath);
	if not path.exists(SA_FilePath):
		print (  "SA path: " + SA_FilePath);
		print (  "SA Path not found");
		print (" Error - Action Canceled. Press a key to return to menu");
		return;
	#Check for
	NeighborFieldFound = 0;
	with open(SA_FilePath, 'r') as SAinput_file:
		for line in SAinput_file:
			lineLC = line.lower();
			if NeighborSearchField in lineLC:
				NeighborFieldFound = 1;
				print (" +++++++++++++++++++++++++++++++++++++++++++++++++ ");
				print ("The Strategic Areas file is already set up for SA Neighbors");
				print (" Press 1 to continue and update the neighbors ");
				print (" Press any other key to cancel");
				print (" This will set default neigbors between all SAs");
		
				choice = input();
				if (choice == "1" ):
					SAinput_file.close();
					AddNeighborsToSAfile(ModFolder );
					return
				else:	
					print (   "Neighbors found in SA file - user abort");
					return;
	if (NeighborFieldFound == 0):
		print (   "Neighbors not found in Srategic Area file - Adding");
		SAinput_file.close();
		AddNeighborsToSAfile(ModFolder );
		return;
	return;

def parse_objects(objectPath):
 

    extensions = {
        ".ai",
        ".tweak"
    }

    filePathDict = {
        ".ai": set(),
        ".tweak": set()
    }

    templateKeyWords = {
        "aiTemplate.create",
        "aiTemplatePlugin.create",
        "kitTemplate.create",
        "weaponTemplate.create"
    }

    aiTemplates = set()
    AI_template_issue_found = False;

    if not path.exists(objectPath):
        print ("path Not Found - can not continue");
        print (objectPath);
        return False;

    print("Search all files in the object folder");
    print(objectPath); 
    print("This will take a minute ...");

    # [1] Get all AI and object files
    print("Creating a list of all AI and Object files")
    for root, dir, files, in os.walk(objectPath):
        for fileName in files:
            fileExtension = os.path.splitext(fileName)[-1]
            if fileExtension in extensions:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathDict[fileExtension].add(realFilePath)

    # [2] Get created aiTemplates
    print("Creating a list of aiTemplates")
    for filePath in filePathDict[".ai"]:
        with open(filePath, "r") as file:
            for line in file:
                templateString = line.strip().split(" ")
                if templateString[0] in templateKeyWords:
                    aiTemplates.add(templateString[1])

    # [3] See if aiTemplate in file exists
    print ("Checking for aiTemplate Issues")
    for filePath in filePathDict[".tweak"]:
        with open(filePath, "r") as file:
            for line in file:
                if (".aiTemplate" not in line) or ("rem" in line):
                    continue
                aiTemplate = line.strip().split(" ")[-1]
                if aiTemplate not in aiTemplates:
                    AI_template_issue_found = True;
                    string = f"{filePath}\n{aiTemplate}"
                    print(string)
    if not (AI_template_issue_found): 
        print ("No AItemplate issues found");
    else:
        print ("AItemplate issues found");
    print ("Press 1 to return to main menu");
    choice = input()
    while choice != "1": choice = input()
    
    return True;



def replaceMaterialsFile(materials_path):
	global _Mod_Name
	global _MeshMode
	global _LogFile
		
	# check for materials.mtl and copy over with known good materials.mtl 
	if (path.exists(materials_path)):
		os.remove(materials_path);
		print( "Remove old materials.mtl file");
	print(  "Creating New Materials.mtl file");	
	with open(materials_path, 'w') as output_file:
		output_file.write("newmtl ground\n");
		output_file.write("Ka 0.0000 0.1986 0.0000\n");
		output_file.write("Kd 0.0166 0.5922 0.0000\n");
		output_file.write("illum 1\n");
		output_file.write("\n");
		output_file.write("newmtl ladder\n");
		output_file.write("Ka 0.1986 0.1986 0.1986\n");
		output_file.write("Kd 0.5922 0.5922 0.5922\n");
		output_file.write("illum 1\n");
		output_file.write("\n");
		output_file.write("newmtl water\n");
		output_file.write("Ka 0.3200 0.3200 0.0000\n");
		output_file.write("Kd 0.9400 0.9400 0.1410\n");
		output_file.write("illum 1\n");
		output_file.write("\n");
		output_file.write("newmtl deepwater\n");
		output_file.write("Ka 0.0000 0.0000 0.3200\n");
		output_file.write("Kd 0.0000 0.0000 0.9400\n");
		output_file.write("illum 1\n");
		output_file.write("\n");
	return;

	
		
def cleanNavmesh(NavmeshInFilePath, NavmeshOutFilePath):
	global _Mod_Name
	global _MeshMode
	global _LogFile
	#mtllib materials.mtl
	#g ground
	#usemtl ground 
	#g ladder
	#usemtl ladder
	#g water
	#usemtl water
	#g deepwater
	#usemtl deepwater
	
	ground_mtl_fix = 0;
	water_mtl_fix = 0;
	deepwater_mtl_fix = 0;
	ladder_mtl_fix = 0;
	print(   "Cleaning Navmesh");
	print(  "Input file:" + NavmeshInFilePath);
	print(  "Output file:" + NavmeshOutFilePath);
	with open(NavmeshInFilePath, 'r') as input_file, open(NavmeshOutFilePath, 'w') as output_file:
		for line in input_file:
			lineLC = line.lower();
			if "mtllib" in lineLC:
			#(line.strip() == "mtllib"):
				output_file.write("mtllib materials.mtl\n");
			elif (line[0] == "g"): #do nothing
				found_g = 1;
			
			elif "usemtl" in lineLC:
			
				if "deepwater" in lineLC: 
					output_file.write("g deepwater\n");
					output_file.write("usemtl deepwater\n");
					deepwater_mtl_fix = 1;	
				elif "water" in lineLC: 
					output_file.write("g water\n");
					output_file.write("usemtl water\n");
					water_mtl_fix = 1;	

				elif "ladder" in lineLC:  
					output_file.write("g ladder\n");
					output_file.write("usemtl ladder\n");	
					ladder_mtl_fix = 1;
				else:
					# default to ground
					output_file.write("g ground\n");
					output_file.write("usemtl ground\n");	
					ground_mtl_fix = 1;	
			
			else:
				line.replace('\n', '\r\n')
				output_file.write(line);
	if (ground_mtl_fix == 1): print(  "Ground Material Fixed");
	if (water_mtl_fix == 1): print(  "water Material Fixed");
	if (deepwater_mtl_fix == 1): print(  "deepwater Material Fixed");
	if (ladder_mtl_fix == 1): print(  "ladder Material Fixed");
	os.remove(NavmeshInFilePath);		
    #with open(path, 'r') as f:
    #    text = f.read()
    #    print path
    #with open(path, 'wb') as f:
    #    f.write(text.replace('\r', '').replace('\n', '\r\n'))	
	return

def CreateHandHeldDict(objectPath):
    handHeldDict = {}

    extensions = {
        ".tweak"
    }

    filePathDict = {
        ".tweak": set()
    }

    templateKeyWords = {
        "GenericFireArm",
        "ObjectTemplate.itemIndex"
    }

    aiTemplates = set()


    if not path.exists(objectPath):
        print ("path Not Found - can not continue");
        print (objectPath);
        return False;

    print("Search all files in the object folder");
    print(objectPath);        

    # [1] Get all AI and object files
    for root, dir, files, in os.walk(objectPath):
        for fileName in files:
            fileExtension = os.path.splitext(fileName)[-1]
            if fileExtension in extensions:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathDict[fileExtension].add(realFilePath)

    # [3] See if aiTemplate in file exists
    for filePath in filePathDict[".tweak"]:
        with open(filePath, "r") as file:
            for line in file:
                lineLC = line.lower();
                if ("genericfirearm" in lineLC):
                    temp_list = lineLC.strip().split("genericfirearm") 
                    weaponName = temp_list[1]
                elif ("objecttemplate.itemindex" in lineLC): 
                    temp_list = lineLC.strip().split("objecttemplate.itemindex") 
                    WeaponIndex = temp_list[1]                
                    handHeldDict[weaponName] = WeaponIndex

    #print ("Handheld list with item index")
    #print (handHeldDict)
    return handHeldDict;
    
def CreateHandHeldBF2ProjDict():
    handHeldBF2ProjDict = {
        'usrif_mp5_a3_Projectile' : '27',
        'rurif_ak47_Projectile' : '38',
        'chrif_type95Projectile' : '25',
        'gbrif_l96a1_Projectile' : '95',
        'USRIF_M203_Projectile' : '30',
        'G36C_Projectile' : '25',
        'RURIF_AK101_Projectile' : '37',
        'usrif_fnscarl_Projectile' : '27',
        'sasrif_g36e_Projectile' : '32',
        'JackhammerProjectile' : '15',
        'usrif_m24_Projectile' : '95',
        'hk21Projectile' : '33',
        'gbrif_sa80a2_l85_Projectile' : '34',
        'RULMG_PKM_Projectile' : '45',
        'M4Projectile' : '25',
        'usrif_remington11-87_Projectile' : '30',
        'sasrif_mp7_Projectile' : '19',
        'chlmg_type95_Projectile' : '25',
        'USSNI_M95_Barret_Projectile' : '190',
        'RURIF_GP30_Projectile' : '37',
        'M16a2Projectile' : '30',
        'chrif_Type85_Projectile' : '19',
        'eurif_fnp90_Projectile' : '19',
        'rpk74Projectile' : '35',
        'chpis_qsz92_silencer_Projectile' : '20',
        'chsht_norinco982_Projectile' : '30',
        'rurif_gp25_Projectile' : '38',
        'sasrif_mg36_Projectile' : '30',
        'chpis_qsz92_Projectile' : '20',
        'chsni_type88_Projectile' : '45',
        'm249Projectile' : '25',
        'g3a3_Projectile' : '40',
        'chsht_protecta_Projectile' : '12',
        'RUPIS_Baghira_Projectile' : '20',
        'usrif_mp5_a3_Projectile' : '19',
        'sasrif_fn2000_Projectile' : '34',
        'USPIS_92FS_silencer_Projectile' : '20',
        'RUPIS_Baghira_silencer_Projectile' : '20',
        'usrif_sa80_Projectile' : '34',
        'gbrif_benelli_m4_Projectile' : '24',
        'kni_knife_Projectile' : '30',
        'rurif_bizon_Projectile' : '19',
        'rurif_dragunov_Projectile' : '45',
        'rusht_saiga12_Projectile' : '12',
        'rurrif_ak74u_Projectile' : '29',
        'M82a1Projectile' : '75',
        'USPIS_92FS_Projectile' : '20',
        'eurif_famas_Projectile' : '30'   
        }    
 
    return (handHeldBF2ProjDict)
    
def CreateHandHeldProjDict_report(handHeldProjDict):   
    current_dir = path.abspath(path.join(os.getcwd(),"."));
    outputPath = (current_dir +  "/handheld_prj_dmg.csv"); 
    output_file = open(outputPath, 'w') 
    print("Creating Projectile Report:"); 
    for ProjName, ProjDam in handHeldProjDict.items():
        proj_name = ProjName.replace(",", " ")
        output_file.write(proj_name + "," + ProjDam + "\n") 
        print (proj_name + "," + ProjDam + "\n") 
    output_file.close()        
    print (outputPath)    
    
    return
    
def CreateHandHeldProjDict(objectPath):
    handHeldProjDict = CreateHandHeldBF2ProjDict()

    extensions = {
        ".tweak"
    }

    filePathDict = {
        ".tweak": set()
    }

    templateKeyWords = {
        "GenericFireArm",
        "ObjectTemplate.itemIndex"
    }

    aiTemplates = set()


    if not path.exists(objectPath):
        print ("path Not Found - can not continue");
        print (objectPath);
        return False;

    print("Search all files in the object folder");
    print(objectPath);        

    # [1] Get all AI and object files
    for root, dir, files, in os.walk(objectPath):
        for fileName in files:
            fileExtension = os.path.splitext(fileName)[-1]
            if fileExtension in extensions:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathDict[fileExtension].add(realFilePath)

    for filePath in filePathDict[".tweak"]:
        with open(filePath, "r") as file:
            projectiletemplate =""
            projectileDamage =""
            proj_found = False
            for line in file:
                lineLC = line.lower();
                if ("objecttemplate.projectiletemplate" in lineLC): 
                    temp_list = line.strip().split() 
                    projectiletemplate = temp_list[1] 
                    if (projectiletemplate == ""):
                        proj_found = False 
                    else: 
                        proj_found = True
                    print (">>> projectiletemplate : " + projectiletemplate)
                elif ("objecttemplate.damageowner" in lineLC):  pass;
                elif ("objecttemplate.damage" in lineLC): 
                    temp_list = line.strip().split() 
                    projectileDamage = temp_list[1]
                    print (">>> projectileDamage :" + projectileDamage) 
                    if (projectiletemplate == "" or projectileDamage == ""): proj_found = False
                    elif ( float (projectileDamage) < 2) : proj_found = False
                    else:
                        proj_found = True
                        if projectiletemplate not in handHeldProjDict.keys():
                            print ("Add to Proj Dict: " + projectiletemplate + " : " + projectileDamage)
                            handHeldProjDict[projectiletemplate] = projectileDamage

    #print (handHeldProjDict)
    CreateHandHeldProjDict_report(handHeldProjDict)
    return handHeldProjDict;    

def CreateHandHeldDictTypes(objectPath):
    # Handheld class items
       # detonatorobject,
       # thrownfirecomp,
       # weaponName,
       # weaponIndex,
       # projectiletemplate,
       # replenishingType,
       # roundsperminute,
       # distToMinDamage,
       # target_maxDistance,
       # targetSystem,
       # abilitymaterial,
       # triggerType,
       # magsize,
       # nrOfMags,
       # velocity,        
       # projectileDamage,
       # aiTemplate       
    handHeldProjDict = CreateHandHeldProjDict(objectPath)
    handHeldDict = {}
    handHeldTypeDict = {}
    
    rifle_projectiles ={
    
    }

    extensions = {
        ".tweak"
    }

    filePathDict = {
        ".tweak": set()
    }

    templateKeyWords = {
        "GenericFireArm",
        "ObjectTemplate.itemIndex"
    }

    aiTemplates = set()


    if not path.exists(objectPath):
        print ("path Not Found - can not continue");
        print (objectPath);
        return False;



    print("Search all files in the object folder");
    print(objectPath);        

    # [1] Get all AI and object files
    for root, dir, files, in os.walk(objectPath):
        for fileName in files:
            fileExtension = os.path.splitext(fileName)[-1]
            if fileExtension in extensions:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathDict[fileExtension].add(realFilePath)

    if not (filePathDict):
        print ("Cound not create File Path Dic - can not continue");
        print ("File Path Dict:")       
        print (filePathDict)
        return False;
    current_dir = path.abspath(path.join(os.getcwd(),"."));
    outputPath = (current_dir +  "/handheld.csv");      
    #print (filePathDict)
    #print (filePathDict)
    # [3] See if aiTemplate in file exists
    #with open(SA_FilePathBackup, 'r') as input_file, open(SA_FilePath, 'w') as output_file:
    output_file = open(outputPath, 'w')
    temp_line = (
       "weapon Name," +
       "weapon Type," +
       "detonator object," +
       "thrown fire comp," +
       "weapon Index," +
       "projectile template," +
       "replenishing Type," +
       "rounds per minute," +
       "dist To Min Damage," +
       "target maxDistance," +
       "targe System," +
       "ability material," +
       "trigger Type," +
       "mag size," +
       "nr Of Mags," +
       "velocity," +      
       "projectile Damage," +
       "ai Template")                  
    output_file.write(temp_line + "\n")
    print (temp_line + "\n")
    
    
    for filePath in filePathDict[".tweak"]:
        print (filePath)
        with open(filePath, "r") as file: 
       # magsize,
       # nrOfMags,
       # velocity,        
       # projectileDamage,
       # aiTemplate 
            weaponName = "";
            isFirearm = True;
            weapon = HandWeapon(False,False,"Uknown Type", "","","","","","","","","None","20","1","1000","30", "NONE")
            for line in file:
                #print (line)
                lineLC = line.lower();
                #ObjectTemplate.activeSafe SupplyObject
                #ObjectTemplate.activeSafe SimpleObject
                if ("objecttemplate.activesafe genericfirearm" in lineLC):
                    temp_list = lineLC.strip().split()                   
                    weaponName = temp_list[2].lstrip()
                    if (weaponName.strip() == ""): 
                        print ("Problem with the Weapon name: " + weaponName) 
                        isFirearm = False; 
                    else:
                        weapon.weaponName = weaponName
                        if weaponName in handHeldProjDict.keys():
                            weapon.projectileDamage = handHeldProjDict[projectiletemplate]
                    print (">>> : " + weaponName)  
                elif ("objecttemplate.activesafe supplyobject" in lineLC): 
                    temp_list = lineLC.strip().split("objecttemplate.activesafe supplyobject")                   
                    weapon.weaponName = temp_list[1].lstrip()                
                    isFirearm = False;
                elif ("objecttemplate.activesafe simpleobject" in lineLC): 
                    temp_list = lineLC.strip().split("objecttemplate.activesafe supplyobject")                   
                    weapon.weaponName = temp_list[1].lstrip()                  
                    isFirearm = False;
                elif ("objecttemplate.itemindex" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.weaponIndex = temp_list[1]   
                    handHeldDict[weaponName] = weapon.weaponIndex               
                elif ("objecttemplate.projectiletemplate" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.projectiletemplate = temp_list[1]  
                    print (">>> projectiletemplate : " + weapon.projectiletemplate)
                elif ("objecttemplate.detonation.triggertype" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.triggerType = temp_list[1]                  
                elif ("objecttemplate.fire.detonatorobject" in lineLC): 
                    weapon.detonatorobject = True 
                elif ("objecttemplate.ammo.replenishingtype" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.replenishingType = temp_list[1] 
                    print (">>> replenishingtype :" + temp_list[1]  )
                elif ("objecttemplate.createcomponent thrownfirecomp" in lineLC): 
                    weapon.thrownfirecomp = True  
                elif ("objecttemplate.fire.roundsperminute" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.roundsperminute = temp_list[1]    
                elif ("objecttemplate.disttomindamage" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.distToMinDamage = temp_list[1]  
                    print (">>> distToMinDamage :" + weapon.distToMinDamage )                      
                elif ("objecttemplate.ammo.magsize" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.magsize = temp_list[1]   
                    print (">>> magsize:" + weapon.magsize )                       
                elif ("objecttemplate.ammo.nrofmags" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.nrOfMags = temp_list[1] 
                    print (">>> nrOfMags :" + weapon.nrOfMags )                       
                elif ("objecttemplate.aitemplate" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.aiTemplate = temp_list[1] 
                    print (">>>  aiTemplate :" + weapon.aiTemplate  )                    
                elif ("objecttemplate.velocity" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.velocity = temp_list[1]
                    print (">>> velocity :" + weapon.velocity)                      
                elif ("objecttemplate.target.maxdistance" in lineLC): 
                    temp_list = lineLC.strip().split("objecttemplate.target.maxdistance") 
                    weapon.target_maxDistance = temp_list[1] 
                elif ("objecttemplate.target.targetsystem" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.targetSystem = temp_list[1] 
                    print (">>> Target System :" + weapon.targetSystem )                     
                elif ("objecttemplate.ammo.abilitymaterial" in lineLC): 
                    temp_list = line.strip().split() 
                    weapon.abilitymaterial = temp_list[1]   
                    print (">>> abilitymaterial :" + weapon.abilitymaterial ) 
            if ((isFirearm) and (weaponName != "")):
                if weapon.detonatorobject : handHeldTypeDict[weaponName] =  "Detonator" 
                elif ( weapon.projectiletemplate == "Parachute") : handHeldTypeDict[weaponName] =  "Parachute"             
                elif ( weapon.replenishingType == "RTAmmo") : handHeldTypeDict[weaponName] =  "AmmoKit" 
                elif ( weapon.replenishingType == "RTHeal") : 
                    if (weapon.abilitymaterial == "84"): handHeldTypeDict[weaponName] =  "VehicleRepairKit"   
                    else:
                        if (weapon.nrOfMags == "-1"): handHeldTypeDict[weaponName] =  "defib"       
                        else: handHeldTypeDict[weaponName] =  "medkit" 
                elif ( weapon.targetSystem != "" ):               
                    if ( weapon.targetSystem == "TSWireGuided" ): handHeldTypeDict[weaponName] =  "WireGuided" 
                    elif ( weapon.targetSystem == "TSLaserGuided" ): handHeldTypeDict[weaponName] =  "LaserGuided" 
                    else: handHeldTypeDict[weaponName] =  "Unknown Target system"      
                elif ( weapon.thrownfirecomp): 
                    if( float(weapon.velocity) > 5 )  : # Thrown greater than 5 should be grenade
                        if (weapon.projectiletemplate == "nshgr_flashbang_Projectile"):  
                            handHeldTypeDict[weaponName] = "flashbang"
                        else: handHeldTypeDict[weaponName] =  "grenade" 
                    else: 
                        if (weapon.projectiletemplate == "at_mine_Projectile"):
                            handHeldTypeDict[weaponName] =  "ATmine" 
                        elif (weapon.projectiletemplate == "usmin_claymore_Projectile"):
                            handHeldTypeDict[weaponName] =  "APmine"  
                        else: handHeldTypeDict[weaponName] =  "Unknown deployable"                         
                elif ( weapon.distToMinDamage == "200"): handHeldTypeDict[weaponName] =  "Pistol"
                elif ( weapon.distToMinDamage == "100"): handHeldTypeDict[weaponName] =  "Shotgun"
                elif ( weapon.magsize == "-1"): handHeldTypeDict[weaponName] =  "Knife"
                elif ( weapon.magsize == "1") :
                    if (float(weapon.velocity) < 60 ): handHeldTypeDict[weaponName] =  "Grenade Launcher"
                    else: handHeldTypeDict[weaponName] =  "Not AI supported"
                elif (  float(weapon.magsize) > 99): handHeldTypeDict[weaponName] =  "LMG"
                elif ( float (weapon.projectileDamage) > 40): handHeldTypeDict[weaponName] =  "Sniper"     
                elif ( float (weapon.projectileDamage)  < 40): handHeldTypeDict[weaponName] =  "Rifle"               
                else: handHeldTypeDict[weaponName] =  "Uknown type"
                print (weaponName + " == " + handHeldTypeDict[weaponName])
                projectiletemplate = weapon.projectiletemplate.replace(",", " ")
                temp_line = (
                    weaponName+","+
                    handHeldTypeDict[weaponName]+","+
                    str(weapon.detonatorobject) +","+
                    str(weapon.thrownfirecomp)+","+
                    weapon.weaponIndex+","+
                    projectiletemplate +","+
                    weapon.replenishingType+","+
                    weapon.roundsperminute+","+
                    weapon.distToMinDamage+","+
                    weapon.target_maxDistance+","+
                    weapon.targetSystem+","+
                    weapon.abilitymaterial+","+
                    weapon.triggerType+","+
                    weapon.magsize+","+
                    weapon.nrOfMags+","+
                    weapon.velocity+","+        
                    weapon.projectileDamage+","+
                    weapon.aiTemplate)  
                output_file.write(temp_line + "\n")  
                print (temp_line + "\n")
            else: print ("Not a Firearm: " + weapon.weaponName)           
            del weapon 
    output_file.close()    
    #print ( handHeldTypeDict);        
    #print ("Handheld list with item index")
    #print (handHeldDict)
    return handHeldDict;

def checkHandheldinKits(objectPath, handHeldDict):
    kitWeaponDict = {}
    kitweapon_list = ["","","","","","","","","","","","",""]
    extensions = {
        ".con"
    }

    filePathlist = []


    templateKeyWords = {
        "ObjectTemplate.addTemplate",
        "ObjectTemplate.create ItemContainer"
    }

    if not path.exists(objectPath):
        print ("path Not Found - can not continue");
        print (objectPath);
        return False;

    if not (handHeldDict):
        print ("Cound not create Hand Held List - can not continue");
        print ("hand Held Dict:")       
        print (handHeldDict)
        return False;

    print("Search all files in the folder:");
    print(objectPath);           

    # [1] Get all AI and object files
    for root, dir, files, in os.walk(objectPath):
        for fileName in files:
            fileExtension = os.path.splitext(fileName)[-1]
            if fileExtension in extensions:
                realDirPath = os.path.realpath(root)
                realFilePath = os.path.join(realDirPath, fileName)
                filePathlist.append(realFilePath)
      

    file_check_done = False
    for filePath in filePathlist:
        with open(filePath, "r") as file:
            print ("\n")
            print (filePath);
            kit_empty = True;
            kitWeaponDict = {}
            x=0
            for item in kitweapon_list:
                kitweapon_list[x] = "";
                x=x+1
            unlocks_found = False 
            weapon_found = False
            unlocks_list =[]
            for line in file:
                lineLC = line.lower();
                #done with checking file
                if ("objecttemplate.create itemcontainer" in lineLC): #unlock container
                    unlocks_found = True
                    unlock_index = 0
                    temp_list = lineLC.strip().split("objecttemplate.create itemcontainer") 
                    unlockname = temp_list[1]                    
                    unlocks_list.append ("Unlock Name: " + unlockname)  
                elif ("objecttemplate.create kit" in lineLC):   
                    temp_list = lineLC.strip().split("objecttemplate.create kit") 
                    KitName = temp_list[1] 
                    print ("checking Kit" +  KitName)                   
                elif ("objecttemplate.replaceitem" in lineLC):   #unlocks
                    temp_list = lineLC.strip().split("objecttemplate.replaceitem" ) 
                    weaponName = temp_list[1] 
                    #print ("Unlock Replacement : " + weaponName)
                    for name, index in handHeldDict.items():  #parse the handheld list
                        if weaponName == name:  # found match in handheld dict
                            #print ("Unlock weapon found in Handheld list")
                            #print ("Unlock replacement: " + index + " == " + weaponName);
                            weapon_found = True
                            unlocks_list.append ("Replace: " + index + " == " + weaponName);
                            if unlock_index == 0:
                                unlocks_list.append ("Replace : " + weaponName + " <<<Non-Weapon unlock>>>" );
                            elif unlock_index != index:
                                unlocks_list.append ("Replace <<<Index mismatch>>>: " + index + " == " + weaponName);
                    if not (weapon_found):
                        unlocks_list.append ("Replace: <<< Not Found >>> " +  weaponName );
                        weapon_found = False
                elif ("objecttemplate.addtemplate" in lineLC): 
                    temp_list = lineLC.strip().split("objecttemplate.addtemplate") 
                    weaponName = temp_list[1]
                    #print ("Looking for " + weaponName )                    
                    for name, index in handHeldDict.items():  #parse the handheld list
                        if weaponName == name:  # found match in handheld dict
                            #print ("found " + name + " " + index ) 
                            weapon_found = True;
                            if (unlocks_found): 
                                unlocks_list.append ("Unlock : " + index + " == " + weaponName);
                                unlock_index = index
                                if unlock_index != index:
                                    unlocks_list.append (" <<<Unlock Index Problem>>> : " + index + " == " + weaponName + "  >>> Should be : " + unlock_index)  
                            else:
                                kit_empty = False;
                                #print (name + "=" + index)
                                if weaponName == kitweapon_list[int(index)]:  #found duplicate in kitweapon list
                                    kitweapon_list[int(index)] = kitweapon_list[int(index)] + " <<< Duplicate Index>>> " +  weaponName;
                                else:  # add to kitweappon list
                                    kitweapon_list[int(index)] = weaponName;
                    if not (weapon_found):
                        print (">>>>> Weapon index not found: " + weaponName)
                        weapon_found = False                                    
   
            if kit_empty: print ("<<<Kit is empty>>>") 
            else:
                x=0
                for item in kitweapon_list:
                    if kitweapon_list[x] != "":
                        print (str(x) + " == " + kitweapon_list[x])
                    else:
                        if x==1: print (str(x) + " == " + ">>>> No Meelee Weapon");
                        elif x==2: print (str(x) + " == " + ">>>> No Pistol Weapon");
                        elif x==3: print (str(x) + " == " + ">>>> No Primary Weapon - This can cause a CTD");
                    x=x+1
                if not (unlocks_list):
                    print ("No Unlocks found")
                else:
                    x=0
                    for item in unlocks_list:
                        if unlocks_list[x] != "":
                            print (unlocks_list[x])   
                            x=x+1
    return True;


def getKitMapInfo(modLevelDir):
    global _InitKitTeamNames  
    global _InitKitTeamLanguage  
    global _InitKitTeamFlag  
    global _InitKitType_list 
    global _InitKitName_list 
    print ("Mod Leve Dir")
    print (modLevelDir)
    init_con_file = modLevelDir + "/init.con" 
    if not path.exists(init_con_file):
        print ("path Not Found - can not continue");
        print (init_con_file);
        return False;      
    with open(init_con_file, 'r') as input_file:
        for line in input_file:
            lineLC = line.lower();
            if "gamelogic.setteamname 1" in lineLC:
                tempstringlist =line.split('1');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamNames[1] = tempstring
            elif "gamelogic.setteamname 2" in lineLC: 
                tempstringlist = line.split('2');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamNames[2] = tempstring            
            elif "gamelogic.setteamlanguage 1" in lineLC: 
                tempstringlist =line.split('1');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamNames[1] = tempstring              
            elif "gamelogic.setteamlanguage 2" in lineLC:    
                tempstringlist =line.split('2');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamNames[2] = tempstring              
            elif "gamelogic.setteamflag 0" in lineLC: 
                tempstringlist =line.split('0');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamLanguage[0] = tempstring              
            elif "gamelogic.setteamflag 1" in lineLC: 
                tempstringlist =line.split('1');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamLanguage[1] = tempstring             
            elif "gamelogic.setteamflag 2" in lineLC: 
                tempstringlist =line.split('2');
                tempstring = tempstringlist[1].strip('\"')
                _InitKitTeamLanguage[2] = tempstring                      
            elif "gamelogic.setkit 1 0" in lineLC: 
                tempstringlist =line.split('1 0');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[0] = tempstring1  
                _InitKitName_list[0] = tempstring2                 
            elif "gamelogic.setkit 2 0" in lineLC: 
                tempstringlist =line.split('2 0');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[1] = tempstring1  
                _InitKitName_list[1] = tempstring2               
            elif "gamelogic.setkit 1 1" in lineLC:
                tempstringlist =line.split('1 1');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[2] = tempstring1  
                _InitKitName_list[2] = tempstring2               
            elif "gamelogic.setkit 2 1" in lineLC: 
                tempstringlist =line.split('2 1');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[3] = tempstring1  
                _InitKitName_list[3] = tempstring2               
            elif "gamelogic.setkit 1 2" in lineLC: 
                tempstringlist =line.split('1 2');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[4] = tempstring1  
                _InitKitName_list[4] = tempstring2              
            elif "gamelogic.setkit 2 2" in lineLC: 
                tempstringlist =line.split('2 2');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[5] = tempstring1  
                _InitKitName_list[5] = tempstring2              
            elif "gamelogic.setkit 1 3" in lineLC:
                tempstringlist =line.split('1 3');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[6] = tempstring1  
                _InitKitName_list[6] = tempstring2              
            elif "gamelogic.setkit 2 3" in lineLC: 
                tempstringlist =line.split('2 3');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[7] = tempstring1  
                _InitKitName_list[7] = tempstring2            
            elif "gamelogic.setkit 1 4" in lineLC:
                tempstringlist =line.split('1 4');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[8] = tempstring1  
                _InitKitName_list[8] = tempstring2             
            elif "gamelogic.setkit 2 4" in lineLC: 
                tempstringlist =line.split('2 4');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[9] = tempstring1  
                _InitKitName_list[9] = tempstring2             
            elif "gamelogic.setkit 1 5" in lineLC: 
                tempstringlist =line.split('1 5');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[10] = tempstring1  
                _InitKitName_list[10] = tempstring2             
            elif "gamelogic.setkit 2 5" in lineLC: 
                tempstringlist =line.split('2 5');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[11] = tempstring1  
                _InitKitName_list[11] = tempstring2               
            elif "gamelogic.setkit 1 6" in lineLC: 
                tempstringlist =line.split('1 6');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[12] = tempstring1  
                _InitKitName_list[12] = tempstring2               
            elif "gamelogic.setkit 2 6" in lineLC:  
                tempstringlist =line.split('2 6');
                tempstringlist2 = tempstringlist[1].split(" ")
                tempstring1 = tempstringlist2[1].strip('\"')
                tempstring2 = tempstringlist2[2].strip('\"')
                _InitKitType_list[13] = tempstring1  
                _InitKitName_list[13] = tempstring2                
    print ("team Names")
    print (_InitKitTeamNames)
    print ("team languages") 
    print (_InitKitTeamLanguage)    
    print ("team Flags")  
    print (_InitKitTeamFlag)   
    print ("Kit Types")  
    print (_InitKitType_list)
    print ("Kit names")  
    print (_InitKitName_list) 
    return            

def selectObjectChoice():
    choice_options_list = ["1","2","3","4"]
    print("Check object files choice:")
    print("(1) All Vehicles and Weapons ");
    print("(2) Vehicles ");
    print("(3) All Weapons");
    print("(4) Hand Weapons");
    print("(0) Exit Menu");
    choice = input();
    while ( choice != "0" ):
        if (choice == "1"): # vehicles and weapons
            objectSelection = "ALL"
            return objectSelection
        elif (choice == "2"): #vehicles :
            objectSelection = "vehicles"
            return objectSelection
        elif (choice == "3"): #weapons : 
            objectSelection = "weapons"
            return objectSelection
        elif (choice == "4"): #handweapons : 
            objectSelection = "handheld"
            return objectSelection
        else:
            print("Invalid choice - Try Again")
            choice = input();
                
    return ""

def checkObjectsAItemplates(mod_folder):
    objects_folder_name = "/objects"
    objectSelection = selectObjectChoice()
    if (objectSelection == "ALL"):
        objectPath = (mod_folder + objects_folder_name + "/vehicles");    
        parse_objects(objectPath);     
        objectPath = (mod_folder + objects_folder_name + "/weapons");    
        parse_objects(objectPath); 
    elif (objectSelection == "handheld"):
        subfolder = "/weapons/handheld"
        objectPath = (mod_folder + objects_folder_name + subfolder);        
        parse_objects(objectPath);     
    elif (objectSelection == ""):
        print ("Invalid Selection")
        return
    else :
        objectPath = (mod_folder + objects_folder_name + "/" + objectSelection);    
        parse_objects(objectPath);     
    return


def chooseBF_type():
    
    MaxChoice = 2
    choice =0;
    print("(1) Battlefield 2");
    print("(2) Battlefield 2142");
    temp_input = input();
    if temp_input.isdigit(): 
        choice = int(temp_input);
    while ( choice < 1 or choice > MaxChoice):
        print("Value out of Range!  Try again:");
        temp_input = input();
        if temp_input.isdigit(): 
            choice = int(temp_input);
    return choice
            
def setModLevel (mod_folder):
    levelName = getLevelChoice(mod_folder + "/levels");
    if not levelName: 
        print ("Level Name Error")
        return ""
    modLevelDir = mod_folder + "/levels/" + levelName;
    return modLevelDir
	
def main():
	#parser = createCmdLineParser();
	#(options, args) = parser.parse_args();	
	#mesh_mode = "3";
	#logMode = 2; # 1 = log only; 2 = log and print
	
		
    #if (len(sys.argv) != 1):
    #    print("Error: Incorrect number of arguments");
    #    return

	#print ("Mod name:" + _Mod_Name);

    global _LogFile
    global _Progress
    global _MeshLeveldir
    global _ModLevelDir
    global _Version
    choice_options_list = ["A","a","B","b","C","c","D","d","E","e","F","f","G","g","H","h"]
    handHeldProjDict = {}
    handHeldDict = {}
    objects_folder_name = "/objects"
    modLevelDir =""
    
    current_dir = path.abspath(path.join(os.getcwd(),"."));
    navmesh_dir = path.abspath(path.join(os.getcwd(),"."));
    mod_folder = path.abspath(path.join(os.getcwd(),".."));
    BF2_dir = path.abspath(path.join(os.getcwd(),".."));
    #print ("BF2 DIR:" + BF2_dir);
    #mod_folder = BF2_dir + "/mods/" + current_dir;
    print ("mod folder:" + mod_folder);
    #print ("Command Line Choice: " );
    #print (sys.argv[1]);
    #tool_choice = (sys.argv[1]);
    #print (tool_choice)
    #xcopy ..\mods\ww%_Mod_Name%\levels\%level_name%\GTSData\Meshes\*.* work\%level_name%\GTSData\Meshes\
#    meshLeveldir = navmesh_dir + "/work/" + levelName;
#    _MeshLeveldir = meshLeveldir
    #print (meshLeveldir);
    #print (modLevelDir);	
    
    #_LogFile = (meshLeveldir + "/GTSData/logfiles/navmeshcontrol.log");
    while (True):
        cls();
        print("*****************************");
        print("  Dnamro Battlefield Tools v3.5 ");
        print("        Main Menu ");
        print("*****************************");
        #print("Current Level: " + levelName);
        #print("Navmesh Mode: " + list (navmeshModes)[navmeshMode]);
        print("Mod Folder: " + mod_folder); 
        print("Mod Level Folder: " + modLevelDir); 
        print("*****************************");
        #print("Level Folder: " + level_folder); 
        print("(A) Create Strategic Area file");
        print("(B) Check and Update Strategic Area file");
        print("(C) Clean Editor GPO file for BF2");
        print("(D) Clean Editor GPO file for BF2142");
        print("(E) Check Map for Single Player issues");
        print("(F) Set Up Static Object file with Nav-stand-ins");
#        print("(H) Check Object folder AItemplates");
#        print("(G) Apply Offsets");
        #print("(I) Check Map Kits for Conflicts");
        print("(0) Quit");
        #print("(0) Go To the Advanced Menu");
        #print("(9) Quit");

        choice = input();
        if (choice == "A" or choice == "a"):  # Create Strategic  Area file
            modLevelDir = setModLevel (mod_folder); #choose map level
            create_SA_File (modLevelDir)
            print (" Press a key to Continue");
            choice = input();
        elif (choice == "B" or choice == "b"): # check SA File 
            modLevelDir = setModLevel (mod_folder); #choose map level
            CheckSAFile(modLevelDir);
            print (" Press a key to Continue");
            choice = input();            
        elif (choice == "C" or choice == "c"): # Clean up the GPO
            modLevelDir = setModLevel (mod_folder); #choose map level
            cleanGPO(modLevelDir);
            print (" Press a key to Continue");
            choice = input();            
        elif (choice == "D" or choice == "d"): # Clean up the GPO for BF2142 use in Editor
            modLevelDir = setModLevel (mod_folder); #choose map level
            FixBF2142GPO(modLevelDir);
            print (" Press a key to Continue");
            choice = input();             
        elif (choice == "E" or choice == "e"): # Check the map for AI Files
            modLevelDir = setModLevel (mod_folder); #choose map level
            checkAiFiles(modLevelDir);
            print (" Press a key to Continue");
            choice = input();            
        elif (choice == "F" or choice == "f"):
            modLevelDir = setModLevel (mod_folder); #choose map level
            setupStaticObjectsForNavmeshing(modLevelDir)
            print (" Press a key to Continue");
            choice = input();   
        elif (choice == "0"):
            return True;
#            elif  (choice == "G" or choice == "g"):  # apply offsets
#                modLevelDir = setModLevel (mod_folder); #choose map level
#                apply_offsets(modLevelDir ); 
#                print (" Press a key to Continue");
#                choice = input();   
                     
#            elif (choice == "H" or choice == "h"): # check objects for AItemplates 
#                checkObjectsAItemplates(mod_folder)
#                print (" Press a key to Continue");
#                choice = input();           
        else:
            print ("Invalid Choice - Try again")          
    return True;            
    #elif (choice == "I" or choice == "i"): 
    #    objects_folder_name = "/objects"
    #    getKitMapInfo (modLevelDir)
    #    objectPath = (mod_folder + objects_folder_name + "/weapons/handheld");  
    #    parse_objects(objectPath);              
    #elif (choice == "J" or choice == "j"):
    #    objectPath = (mod_folder + objects_folder_name + "/weapons/handheld");  
    #    print ("Creating list of Hand Helds")
    #    handHeldDict = CreateHandHeldDict(objectPath);
    #    objectPath = (mod_folder + objects_folder_name + "/Kits");  
    #    print("Checking Kits")
    #    checkHandheldinKits(objectPath, handHeldDict);
    #    print ("Kit check completed")
    #    CreateHandHeldDictTypes
    #elif (choice == "K" or choice == "k"):
    #def CreateHandHeldProjDict(objectPath):
    #handHeldProjDict = {}
        #current_dir = path.abspath(path.join(os.getcwd(),"."));
        
        #objectPath = (mod_folder + objects_folder_name + "/weapons/handheld");  
        #handHeldProjDict = CreateHandHeldProjDict(objectPath);
        #CreateHandHeldDictTypes(objectPath);  
        #print ("Handweapon check comwpleted")        
	
    #elif (choice == "F" or choice == "f"):
    #    setupStaticObjectsForNavmeshing(modLevelDir) 
    #elif (choice == "D" or choice == "d"):
    #    _BF_Type = (sys.argv[2]);
    #    checkAiFiles(modLevelDir);
    #    FixBF2142GPO(modLevelDir);    


success = main();

if success:
	sys.exit(0);
else:
	sys.exit(1);