
#
# ATT 2017-04-26 v10.0.48
#
# TOOLS FOR ODOO 10+
#
# INSERT ON ODOO TABLES BASED ON CXSD/XML
#

import datetime

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


def odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, runInsertsOnDB):

	status = False
	
	pyIdent = "    "

	#Write Output Odoo Structure
	output = '# -*- coding: utf-8 -*-\n# ATT Generated at {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	output = output + "\n\nfrom odoo import models, fields, api\n"

	cxsd = schema_Parsed_Root
	
	schema_Parsed_Root = None #saving memory

	modelsClasses = []
	modelFields = []

	#List of Ordered Required Attributes (Order/Case Sensitive) 
	#  All Nodes must to have those attributes
	#  Nodes without attributes will be ignored
	commonNodeAttributes = ["nodeType", "nodePath", "odooClass", "odooField", "odooDT"]

	allowedNodeTypes = ["simpleClass", "simple", "complex", "multipleField", 
						"complexFieldIdValue", "complexFieldIdRows", "extraField", 
						"relationship"
						]

	#Load XML Schema

	#Iter Schema
	for cxsdElem in cxsd.iter():

		# Has Attributes?
		if len(cxsdElem.attrib) > 0:
	
			#Only care about allowed nodeTypes
			if cxsdElem.get('nodeType') in allowedNodeTypes:

				#Getting Node Attributes Values
				cxsdElemAttribValues = [
					cxsdElem.get('nodeType'),
					cxsdElem.get('nodePath'),
					cxsdElem.get('odooClass'),
					cxsdElem.get('odooField'),
					cxsdElem.get('odooDT')
					]
					
				#Zip method, which combines two iterables and make it dictionary
				cxsdElemAttribDict = dict(zip(commonNodeAttributes, cxsdElemAttribValues)) 


				#Simple Classes List
				if cxsdElem.get('nodeType') == "simpleClass":

					#Get Commom Attributes
					nodesAttributes = commonNodeAttributes
					
					#Add Specific Nodes
					nodesAttributes.append("odooRecName")
					nodesAttributes.append("odooSQLConstraints")

					#Getting Node Attributes Values
					cxsdElemAttribValues = [
						cxsdElem.get('nodeType'),
						cxsdElem.get('nodePath'),
						cxsdElem.get('odooClass'),
						cxsdElem.get('odooField'),
						cxsdElem.get('odooDT'),
						cxsdElem.get('odooRecName'),
						cxsdElem.get('odooSQLConstraints')
					]
					
					#Zip method, which combines two iterables and make it dictionary
					cxsdElemAttribDict = dict(zip(nodesAttributes, cxsdElemAttribValues)) 
					
					#Keep on memory
					modelsClasses.append(cxsdElemAttribDict)
				
				elif cxsdElem.get('nodeType') == "simple":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "complex":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "multipleField":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdValue":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdRows":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "extraField":
				
					modelFields.append(cxsdElemAttribDict)

				elif cxsdElem.get('nodeType') == "relationship":
				
					modelFields.append(cxsdElemAttribDict)

				cxsdElemAttribValues.clear #Saving Memory
					
		cxsdElem.clear #Saving Memory



	#Only create valid classes models
	if len(modelsClasses)>0:

		#Looping Classes to generate
		for i in range(len(modelsClasses)):
			
			#Model Class Name
			modelClassName = modelsClasses[i]['odooClass']
			
			#rec_name
			modelClassRecName = modelsClasses[i]['odooRecName']

			#sql_constraints
			modelClassSQLConstraints = modelsClasses[i]['odooSQLConstraints']

			#Write Odoo Class Name
			output = "{}\nclass {}(models.Model):\n".format(output, modelClassName)

			#Write Odoo Default Name Field
			output = "\n{}{}{} = '{}'\n".format(
												output, 
												pyIdent, 
												modelsClasses[i]['odooField'], 
												modelsClasses[i]['odooDT']
												)
			if not modelClassRecName == "":
				#Write Odoo Rec Name Field
				output = "{}{}_rec_name = '{}'\n".format(
													output,
													pyIdent,
													modelClassRecName
													)

			if not modelClassSQLConstraints == "":
				#Write Odoo Constraints Definition
				output = "{}{}_sql_constraints = {}\n".format(
													output,
													pyIdent,
													modelClassSQLConstraints
													)
			#line for beautify
			output = output + "\n"

# TENTATIVA DE REMOVE ITEM DA LISTA APOS USO, MAS DA ERRO DE LIST INDEX OUT OF RANGE
# TALVEZ FAZER UMA LISTA DE USADOS E DEPOIS MANDAR EXCLUIR QUANDO SAIR DO FOR			
#			#Fields Loop
#			for f in range(len(modelFields)):
#				#Keep only field where Class Name matches
#				if modelFields[f]['odooClass']==modelClassName:	
#					
#					#Write Odoo Default Name Field
#					output = '\n{}{}{} = "{}"\n'.format(
#														output, 
#														pyIdent, 
#														modelFields[f]['odooField'], 
#														modelFields[f]['odooDT']
#														)
#
#					del modelFields[f-1]

			#Fields Loop
			for field in modelFields:

				#Keep only field where Class Name matches
				if field['odooClass'] == modelClassName:	
					
					#Only odoo fields and datatype defined
					if not ((field['odooField'] == "") and (field['odooDT'] == "")):

						#Write Odoo Default Name Field
						output = '\n{}{}{} = {}\n'.format(
															output, 
															pyIdent, 
															field['odooField'], 
															field['odooDT']
															)
						#TENTATIVA NAO DEU CERTO TBM
						#Remove Field Used for saving process and memory 
						#modelFields.remove(field)

	status = True

	return status, output.lstrip() #Removes empty lines before 


def writeOut(outputText, filename):
	with open(filename,"w+") as f:
		f.write(outputText)

def strip_one_space(s):
    if s.endswith(" "): s = s[:-1]
    if s.startswith(" "): s = s[1:]
    return s

#---------------------------------------------------
def main():

	#---------------------------------------------------
	#TESTS

	#def findElements():
	#	cxsdElems = []
	#	for name in names: 
	#	    namedElements = xmlDoc.xpath("//*[local-name() = $name]", name=name)
	#	    elements.extend(namedElements)
	#	return elements


	#def getElems(schemaDoc, xmlDoc, typeName):
	#    names = schemaDoc.xpath("//xsd:element[@type = $n]/@name",
	#                            namespaces={"xsd": 
	#                                        "http://www.w3.org/2001/XMLSchema"},
	#                            n=typeName)


	#---------------------------------------------------
	# RUNNING

	inputXMLFile = "../OdooImporterData/corretiva_v20/xml/corretiva_v20_20170110-121749.xml"
	inputXSDFile = "../OdooImporterData/corretiva_v20/schemas/corretiva_v20_20170110.cxsd"

	parser = etree.XMLParser() 
	
	schema_Parsed_Root = etree.parse(inputXSDFile).getroot()
	xmldoc_Parsed_Root = etree.parse(inputXMLFile).getroot()

	#status, outputText = odooGenerateOrmFromCXSD(cxsdSchema)

	status, outputText = odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, False)

	#outputText = strip_one_space(outputText)

	#writeOut(outputText,"/Users/andersontagata/TemosEngenharia/custom-addons/corretiva/models/corretiva_model_v20.py")
	#writeOut(outputText,"../OdooImporterData/corretiva_v20/models/corretiva_model_v20.py")

	print(outputText)
	print("\n#EOF status:" + str(status))









#---------------------------------------------------
if __name__ == "__main__":
	main()








