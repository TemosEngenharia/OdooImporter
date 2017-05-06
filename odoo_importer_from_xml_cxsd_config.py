
#
# ATT 2017-04-26 v10.0.52 - New odoo config loader
# ATT 2017-04-26 v10.0.1
#
# TOOLS
#
# SETTINGS
#
from db_config import odoo_config


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
	
  global settings
  settings = []
  settings.append(arg)

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
  outputORMPath = "/Users/andersontagata/TemosEngenharia/custom-addons/corretiva/models/"
  outputORMFileName = "corretiva_model.py"
  outputORMFile = outputORMPath + outputORMFileName

  global outputORMPath_InDataDomain, outputORMFileName_InDataDomain, outputORMFile_InDataDomain
  outputORMPath_InDataDomain = "../OdooImporterData/corretiva/models/"
  outputORMFileName_InDataDomain = "corretiva_model.py"
  outputORMFile_InDataDomain = outputORMPath_InDataDomain + outputORMFileName_InDataDomain

  

