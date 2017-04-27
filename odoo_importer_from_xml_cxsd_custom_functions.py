
#
# ATT 2017-04-26 v10.0.1
#
# TOOLS FOR ODOO 10+
#
# CUSTOM FUNCTIONS FOR XML IMPORT
#
 
import odoo_importer_from_xml_cxsd_config as config
import odoo_importer_from_xml_cxsd as importer

def getXMLFilename():
	return config.inputXMLFileName