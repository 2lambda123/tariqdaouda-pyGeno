import sys, os, time
from configparser import SafeConfigParser
import rabaDB.rabaSetup
import rabaDB.Raba

class PythonVersionError(Exception) :
	pass

pyGeno_FACE = "~-~-:>"
pyGeno_BRANCH = "V2"

pyGeno_VERSION_NAME = 'Lean Viper!'
pyGeno_VERSION_RELEASE_LEVEL = 'Release'
pyGeno_VERSION_NUMBER = 14.09
pyGeno_VERSION_BUILD_TIME = time.ctime(os.path.getmtime(__file__))

pyGeno_RABA_NAMESPACE = 'pyGenoRaba'

pyGeno_SETTINGS_DIR = os.path.normpath(os.path.expanduser('~/.pyGeno/'))
pyGeno_SETTINGS_PATH = None
pyGeno_RABA_DBFILE = None
pyGeno_DATA_PATH = None
pyGeno_REMOTE_LOCATION = 'http://bioinfo.iric.ca/~feghalya/pyGeno_datawraps'

db = None #proxy for the raba database
dbConf = None #proxy for the raba database configuration

def version() :
	"""returns a tuple describing pyGeno's current version"""
	return (pyGeno_FACE, pyGeno_BRANCH, pyGeno_VERSION_NAME, pyGeno_VERSION_RELEASE_LEVEL, pyGeno_VERSION_NUMBER, pyGeno_VERSION_BUILD_TIME )

def prettyVersion() :
	"""returns pyGeno's current version in a pretty human readable way"""
	return "pyGeno %s Branch: %s, Name: %s, Release Level: %s, Version: %s, Build time: %s" % version()

def checkPythonVersion() :
	"""pyGeno needs python 3.5+"""
	
	if sys.version_info[0] < 3 or (sys.version_info[0] == 3  and sys.version_info[1] < 5) :
		return False
	return True

def getGenomeSequencePath(specie, name) :
	return os.path.normpath(pyGeno_DATA_PATH+'/%s/%s' % (specie.lower(), name))

def createDefaultConfigFile() :
	"""Creates a default configuration file"""
	s = "[pyGeno_config]\nsettings_dir=%s\nremote_location=%s" % (pyGeno_SETTINGS_DIR, pyGeno_REMOTE_LOCATION)
	f = open('%s/config.ini' % pyGeno_SETTINGS_DIR, 'w')
	f.write(s)
	f.close()

def getSettingsPath() :
	"""Returns the path where the settings are stored"""
	parser = SafeConfigParser()
	try :
		parser.read(os.path.normpath(pyGeno_SETTINGS_DIR+'/config.ini'))
		return parser.get('pyGeno_config', 'settings_dir')
	except :
		createDefaultConfigFile()
		return getSettingsPath()

def removeFromDBRegistery(obj) :
	"""rabaDB keeps a record of loaded objects to ensure consistency between different queries.
	This function removes an object from the registery"""
	rabaDB.Raba.removeFromRegistery(obj)

def freeDBRegistery() :
	"""rabaDB keeps a record of loaded objects to ensure consistency between different queries. This function empties the registery"""
	rabaDB.Raba.freeRegistery()

def reload() :
	"""reinitialize pyGeno"""
	pyGeno_init()

def pyGeno_init() :
	"""This function is automatically called at launch"""
	
	global db, dbConf
	
	global pyGeno_SETTINGS_PATH
	global pyGeno_RABA_DBFILE
	global pyGeno_DATA_PATH
	
	if not checkPythonVersion() :
		raise PythonVersionError("==> FATAL: pyGeno only works with python 3.5 and above, please upgrade your python version")

	if not os.path.exists(pyGeno_SETTINGS_DIR) :
		os.makedirs(pyGeno_SETTINGS_DIR)
	
	pyGeno_SETTINGS_PATH = getSettingsPath()
	pyGeno_RABA_DBFILE = os.path.normpath( os.path.join(pyGeno_SETTINGS_PATH, "pyGenoRaba.db") )
	pyGeno_DATA_PATH = os.path.normpath( os.path.join(pyGeno_SETTINGS_PATH, "data") )
	
	if not os.path.exists(pyGeno_SETTINGS_PATH) :
		os.makedirs(pyGeno_SETTINGS_PATH)

	if not os.path.exists(pyGeno_DATA_PATH) :
		os.makedirs(pyGeno_DATA_PATH)

	#launching the db
	rabaDB.rabaSetup.RabaConfiguration(pyGeno_RABA_NAMESPACE, pyGeno_RABA_DBFILE)
	db = rabaDB.rabaSetup.RabaConnection(pyGeno_RABA_NAMESPACE)
	dbConf = rabaDB.rabaSetup.RabaConfiguration(pyGeno_RABA_NAMESPACE)
