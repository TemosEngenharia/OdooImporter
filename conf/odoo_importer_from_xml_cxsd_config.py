
#
# ATT 2017-06-06 v10.1.00 - Refactoring project.
# ATT 2017-04-26 v10.0.52 - New odoo config loader
# ATT 2017-04-26 v10.0.1
#
# TOOLS
#
# SETTINGS
#
#Logging Required Imports
from . import logging_config as lc
import logging

from .db_config import odoo_config


try:
  from lxml import etree
  print("running with lxml.etree")
except ImportError:
  try:
    # Python 2.5
    import xml.etree.cElementTree as etree
    print("running with cElementTree on Python 2.5+")
  except ImportError:
    try:
      # Python 2.5
      import xml.etree.ElementTree as etree
      print("running with ElementTree on Python 2.5+")
    except ImportError:
      try:
        # normal cElementTree install
        import cElementTree as etree
        print("running with cElementTree")
      except ImportError:
        try:
          # normal ElementTree install
          import elementtree.ElementTree as etree
          print("running with ElementTree")
        except ImportError:
          print("Failed to import ElementTree from any known place")

def init(arg):
  logger = logging.getLogger(__name__)
	
  global settings
  settings = []
  settings.append(arg)

  global sourceFilenameFieldName
  global inputXMLPath, inputXMLFileName, inputXMLFile
  global inputCXSDPath, inputCXSDFileName, inputCXSDFile

  #inputXMLPath = "../OdooImporterData/corretiva_v20/xml/" 
  #inputXMLFileName = "corretiva_v20_20170110-121749.xml"
  #inputXMLFile = inputXMLPath + inputXMLFileName

  #inputCXSDPath = "../OdooImporterData/corretiva/schemas/"
  #inputCXSDFileName = "COR20.cxsd"
  #inputCXSDFile = inputCXSDPath + inputCXSDFileName

  #custom global var
  global main_id
  global formDateTime

  global odooConfigDict
  odooConfigDict = odoo_config() #comes from db_tools + db_config.ini

  global outputORMPath, outputORMFileName, outputORMFile
  #outputORMPath = "../../odoo-dev/custom-addons/mcorretiva/models/"
  #outputORMFileName = "mcorretiva_model.py"
  #outputORMFile = outputORMPath + outputORMFileName

  global outputORMPath_InDataDomain, outputORMFileName_InDataDomain, outputORMFile_InDataDomain
  outputORMPath_InDataDomain = "/opt/odoo-dev/tools/OdooImporter/data/ipo/models/"
  outputORMFileName_InDataDomain = "ipo_main_model.py"
  outputORMFile_InDataDomain = outputORMPath_InDataDomain + outputORMFileName_InDataDomain

  

