
#
# ATT 2017-04-26 v10.0.48
#
# TOOLS FOR ODOO 10+
#
# INSERT ON ODOO TABLES BASED ON CXSD/XML
#


import datetime
import odoo_importer_from_xml_cxsd_config as config 
import odoo_importer_from_xml_cxsd_custom_functions as cfuncs

def odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, runInsertsOnDB):

	status = False
	
	#pyIdent = "    "

	#Write Output Odoo Structure
	output = '# -*- coding: utf-8 -*-\n# ATT Generated at {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	output = output + "\n\nfrom odoo import models, fields, api\n"

	sqlInsertFormat = "INSERT INTO {0} (\n {1} \n) VALUES (\n {2} \n);"
	sqlInsertOutput = ""

	cxsd = schema_Parsed_Root
	schema_Parsed_Root = None #saving memory

	xmlDoc = xmldoc_Parsed_Root
	xmldoc_Parsed_Root = None

	modelsClasses = []
	modelFields = []

	#List of Ordered Required Attributes (Order/Case Sensitive) 
	#  All Nodes must to have those attributes
	#  Nodes without attributes will be ignored
	commonNodeAttributes = ["nodeType", "nodePath", "odooClass", "odooField", "odooDT"]

	allowedNodeTypes = ["mainClass", "childClass", "simple", "complex", "multipleField", 
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
				commomElemAttribValues = [
					cxsdElem.get('nodeType'),
					cxsdElem.get('nodePath'),
					cxsdElem.get('odooClass'),
					cxsdElem.get('odooField'),
					cxsdElem.get('odooDT')
					]
					
				#Zip method, which combines two iterables and make it dictionary
				commomElemAttribDict = dict(zip(commonNodeAttributes, commomElemAttribValues)) 


				#Simple Classes List
				if cxsdElem.get('nodeType') in ["mainClass", "childClass"]:

					#Get Commom Attributes
					nodesAttributes = list(commonNodeAttributes)
					
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
					modelsClasses.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "simple":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "complex":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "multipleField":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdValue":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdRows":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') in ["extraField", "relationship"]:
					
					#Get Copy of Commom Attributes
					nodesAttributes = list(commonNodeAttributes)
					
					#Add Specific Nodes
					nodesAttributes.append("getValueOf")

					#Getting Node Attributes Values
					cxsdElemAttribValues = [
						cxsdElem.get('nodeType'),
						cxsdElem.get('nodePath'),
						cxsdElem.get('odooClass'),
						cxsdElem.get('odooField'),
						cxsdElem.get('odooDT'),
						cxsdElem.get('getValueOf')
					]
					
					#Zip method, which combines two iterables and make it dictionary
					cxsdElemAttribDict = dict(zip(nodesAttributes, cxsdElemAttribValues)) 

					modelFields.append(cxsdElemAttribDict)

				#elif cxsdElem.get('nodeType') == "relationship":
				
				#	modelFields.append(commomElemAttribDict)

					
		cxsdElem.clear #Saving Memory

	#print(modelFields)

	#exit()

	#Only create valid classes models
	if len(modelsClasses)>0:

		#Looping Classes to generate
		for i in range(len(modelsClasses)):
			
			insertRolls = 0

			#Control n times inserts
			if modelsClasses[i]['nodeType']  == "mainClass":
				#once time
				insertRolls = 1
			
			elif modelsClasses[i]['nodeType']  == "childClass":
				#multiple times based on elements count of Xpath defined on nodePath
				
				try:
					insertRolls = int(xmlDoc.xpath("count(" + modelsClasses[i]["nodePath"] + ")"))
					#insertRolls = 0
				except Exception:
					print("\n<CError> Invalid nodePath:" + modelsClasses[i]["nodePath"] + " for Class:" + modelsClasses[i]['odooClass'] + " nodeType:" + modelsClasses[i]['nodeType'])
					print("<CError> Must allow XPath count(nodePath) function on it!! Skipping this insert...\n")
					insertsRolls = 0
					pass

			#Mount Insert and Run It
			for n in range(insertRolls):

				#Model Class Name
				modelClassName = modelsClasses[i]['odooClass']

				#Discovery with one is rolling
				nodePath = modelsClasses[i]["nodePath"]

				print("\n>> [" + str(n) + "] Running: " + modelClassName + "  >>  " + nodePath )

				#Transform Table Name (Dot to Underlines)
				tableClassName = 'public.' + modelsClasses[i]['odooDT'].replace('.', '_')

				#init fields names list and values list
				fieldsNamesList = []
				fieldsValuesList = []

				#Fields Loop
				for field in modelFields:

					#Keep only field where Class Name matches
					if field['odooClass'] == modelClassName:	
						

						print("\n  >>>-  " + field['odooField'] + "  -  " + field['nodePath'] + "  -  " + field['nodeType'])



						#Only odoo fields and datatype defined
						if not ((field['odooField'] == "") and (field['odooDT'] == "")):

							#Get Field Name
							fieldName = field['odooField']


							#Append Field Name
							fieldsNamesList.append(fieldName)

							#Get Odoo Datatype
							fieldDataType = field['odooDT']
							

							#Deal with custom fields with has not value on xml
							if field['nodeType'] in ["extraField", "relationship"]:
								#Get value for this field on xml
								fieldValue = getValueForNodeType(field['nodeType'], "", field['getValueOf'])

							elif modelsClasses[i]['nodeType'] == "childClass":
								#Get value for this field on xml
								#print("\n\n>>>"+field["nodePath"].replace('?', str(n)))
								#Get value for this field on xml
								fieldValue = getValueForNodeType(field['nodeType'], xmlDoc.xpath(field["nodePath"].replace('?', str(n+1))), "")

							elif field['nodeType'] in ["simple"]:

								#print("\n\n>>>"+field["nodePath"].replace('?', '1'))
								#Get value for this field on xml
								fieldValue = getValueForNodeType(field['nodeType'], xmlDoc.xpath(field["nodePath"].replace('?', '1')), "")
							#else:
								#print(fieldName + " : " + getFormattedValue(fieldDataType, fieldValue) + " : " + field["nodePath"] + "\n")

							#Append value formatted for sql datatype
							fieldsValuesList.append(getFormattedValue(fieldDataType, fieldValue))

				
				#Fields of Oddo Internal Control
				fieldsNamesOdoo = "entry_form_file_id, write_date, entry_form_file_data, entry_form_file_description"
				fieldsValuesOdoo = "entry_form_file_id, write_date, entry_form_file_data, entry_form_file_description"

				#fieldsNamesList.append(fieldsNamesOdoo.split(", "))
				#fieldsValuesList.append(fieldsValuesOdoo.split(", "))

				#print(fieldsNamesList)
				#print(fieldsValuesList)

				#Fields and Values from XML to SQL
				fieldsNames = ', '.join(fieldsNamesList)
				fieldsValues = ', '.join(fieldsValuesList)


				
				#Write Odoo Default Name Field
				#field['odooField'], 
				#field['odooDT']
							
				#TENTATIVA NAO DEU CERTO TBM
				#Remove Field Used for saving process and memory 
				#modelFields.remove(field)

				sqlInsertOutput = sqlInsertOutput + "\n" + sqlInsertFormat.format(
																	tableClassName,
																	fieldsNames,
																	fieldsValues
																	)

		#sqlInsertFormat = "INSERT INTO {0} (\n {1} \n) VALUES (\n {2} \n);"
	
	# entry_form_file_id, write_date, entry_form_file_data, entry_form_file_description)
	#VALUES (?, ?, ?, ?, ?, ?, ?, ?);

	status = True

	return status, sqlInsertOutput.lstrip() #Removes empty lines before 



def getValueForNodeType(nodeType, xmlDoc_XPath_nodePath, getValueOfFunction):
						
	outputValue=""

	#Deal with custom fields with has not value on xml
	if nodeType in "extraField":

		#Testing User Custom Functions and handling it on error case
		getValueOf = "cfuncs." + getValueOfFunction

		try:
		    outputValue = eval(getValueOf)
		     
		except AttributeError:

			outputValue = 'ERR:' + getValueOfFunction


	#Deal with custom fields with has not value on xml
	elif nodeType in "relationship":

		#Testing User Custom Functions and handling it on error case
		getValueOf = "cfuncs." + getValueOfFunction

		try:
		    outputValue = eval(getValueOf)
		     
		except AttributeError:

			outputValue = 'ERR:' + getValueOfFunction


	else:

		outputValue=xmlDoc_XPath_nodePath[0].text

	return outputValue
						
						

def getFormattedValue(format, value):

	if format.startswith("fields.Char("):
		return "'{}'".format(value)

	elif format.startswith("fields.Integer("):
		return value

	elif format.startswith("fields.Binary("):
		return str(len(value))

	else:
		return value


	
def writeOut(outputText, filename):
	with open(filename,"w+") as f:
		f.write(outputText)



def strip_one_space(s):
    if s.endswith(" "): s = s[:-1]
    if s.startswith(" "): s = s[1:]
    return s



#---------------------------------------------------
def main():

	#Start Up Settings
	config.init("dev_mode")

	print(config.settings)

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

	schema_Parsed_Root = config.etree.parse(config.inputCXSDFile).getroot()
	xmldoc_Parsed_Root = config.etree.parse(config.inputXMLFile).getroot()


	#status, outputText = odooGenerateOrmFromCXSD(cxsdSchema)

	status, outputText = odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, False)

	#outputText = strip_one_space(outputText)

	#writeOut(outputText,"/Users/andersontagata/TemosEngenharia/custom-addons/corretiva/models/corretiva_model_v20.py")
	#writeOut(outputText,"../OdooImporterData/corretiva_v20/models/corretiva_model_v20.py")

	print(outputText)
	print("\n#EOF status:" + str(status))


	#print(cfuncs.getXMLFilename())






#---------------------------------------------------
if __name__ == "__main__":
	main()








