
#
# ATT 2017-05-02 v10.0.53 - Record special fields on postgresql (create and write (date and uid)) + Force Content for Add Rem childs
# ATT 2017-05-02 v10.0.52 - New odoo Functions / Insert of Main and Childs working fine / Delete before Add repeated file
# ATT 2017-05-02 v10.0.51 - New odoo Functions / Insert of Main and Childs error on insert childs
# ATT 2017-04-27 v10.0.50 - Allowing multiple Inserts for Childs Classes
# ATT 2017-04-26 v10.0.48
#
# TOOLS FOR ODOO 10+
#
# INSERT ON ODOO TABLES BASED ON CXSD/XML
#

import logging
import datetime
import odoo_importer_from_xml_cxsd_config as config 
import odoo_importer_from_xml_cxsd_custom_functions as cfuncs
import db_tools as dbtools 
from os import listdir
from os.path import isfile, join
from os import walk

from os import rename

def odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, runInsertsOnDB):

	status = False
	
	#pyIdent = "    "

	#Write Output Odoo Structure
	output = '# -*- coding: utf-8 -*-\n# ATT Generated at {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	output = output + "\n\nfrom odoo import models, fields, api\n"

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

	allowedNodeTypes = ["mainClass", "childClass", "simple", "extraField", 
						"relationship", "mainFields", "childField", "childFieldData"
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

				elif cxsdElem.get('nodeType') in ["mainFields", "childField", "childFieldData"]:
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdValue":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') == "complexFieldIdRows":
				
					modelFields.append(commomElemAttribDict)

				elif cxsdElem.get('nodeType') in ["extraField"]:
					
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

	#	exit()

	#Only create valid classes models
	if len(modelsClasses)>0:

		config.main_id = -1

		#Looping Classes to generate
		for i in range(len(modelsClasses)):
			
			insertRolls = 0

			fieldsNamesList = []
			fieldsValuesList = []
			sqlInsertOutput = "" 
			status = False
			
			#Control n times inserts
			if modelsClasses[i]['nodeType']  == "mainClass":
				#once time

				#Transform Table Name (Dot to Underlines)
				tableClassName = 'public.' + modelsClasses[i]['odooDT'].replace('.', '_')

				fieldsNamesList, fieldsValuesList = mountFieldsAndValues(modelsClasses[i], modelFields, 0, xmlDoc)

				sqlInsertOutput = mountSQlInsert(sqlInsertOutput, tableClassName, fieldsNamesList, fieldsValuesList)

				#Print out SQL That will be run on cursor
				#print("SQL Main:" + sqlInsertOutput)

				deleteBeforeInsert = "DELETE FROM " + tableClassName + " WHERE entry_xml_filename LIKE '" + config.inputXMLFileName + "';"

				print("Running:" + deleteBeforeInsert)
				dbtools.deleteFromDB(deleteBeforeInsert)

				#Run INSERT ON SQL POSTGREE
				config.main_id = dbtools.insertInToDB(sqlInsertOutput)

				#Print Inserted ID
				print("\n  *>>indexRow:[" + str(i) + "] Inserted Main ID:[" + str(config.main_id) + "]")

				if config.main_id is None:
					config.main_id = -1
					status = False
				else:
					status = True
				
				#exit()

			#Special childClass for multiple inserts in relationshop to main
			elif modelsClasses[i]['nodeType']  == "childClass" and config.main_id > 0:
				#multiple times based on elements count of Xpath defined on nodePath

				try:
					insertRolls = int(xmlDoc.xpath("count(" + modelsClasses[i]["nodePath"] + ")"))
					#insertRolls = 0
				except Exception:
					print("\n<CError> Invalid nodePath:" + modelsClasses[i]["nodePath"] + " for Class:" + modelsClasses[i]['odooClass'] + " nodeType:" + modelsClasses[i]['nodeType'])
					print("<CError> Must allow XPath count(nodePath) function on it!! Skipping this insert...\n")
					insertsRolls = 0
					pass

				#Mount Insert n times and Run It
				for n in range(insertRolls): #xrange(1,10):

					print("\n\n>> [" + str(n) + "] Running: OdooClass:" + modelsClasses[i]['odooClass'] + "  >>  NodeType:" + modelsClasses[i]["nodeType"]  + "  >>  NodePath:" + modelsClasses[i]["nodePath"] )

					#Transform Table Name (Dot to Underlines)
					tableClassName = 'public.' + modelsClasses[i]['odooDT'].replace('.', '_')

					fieldsNamesList, fieldsValuesList = mountFieldsAndValuesOfMainFields(
																						modelsClasses[i], 
																						modelFields, 
																						n, 
																						cxsd, 
																						xmlDoc
																						)

					sqlInsertOutput = mountSQlInsert(sqlInsertOutput, tableClassName, fieldsNamesList, fieldsValuesList)
					
					#Run INSERT ON SQL POSTGREE
					child_id = dbtools.insertInToDB(sqlInsertOutput)

					if child_id is None:
						child_id = -1
						status = False
					else:
						status = True
					#Print Inserted ID
					print("\n  *>>indexRow:[" + str(i) + "] Inserted Child ID:[" + str(child_id) + "]")

					#exit()

	

	return status



def mountSQlInsert(sqlInsertOutput, tableClassName, fieldsNamesList, fieldsValuesList):

	sqlInsertFormat = "INSERT INTO {0} (\n {1} \n) VALUES (\n {2} \n) RETURNING {3};"
	
	#Fields of Oddo Internal Control
	fieldsNamesOdoo = "create_date, write_date, create_uid, write_uid"
	fieldsValuesOdoo = []
	fieldsValuesOdoo.append("'" + cfuncs.getCurrentDateTimeForSQL() + "'")
	fieldsValuesOdoo.append("'" + cfuncs.getCurrentDateTimeForSQL() + "'")
	fieldsValuesOdoo.append(cfuncs.getOdooUserId())
	fieldsValuesOdoo.append(cfuncs.getOdooUserId())

	#print(fieldsValuesOdoo)
	#exit()

	fieldsNamesList.extend(fieldsNamesOdoo.split(", "))
	fieldsValuesList.extend(fieldsValuesOdoo)

	#print(fieldsNamesList)
	#print(fieldsValuesList)

	#Fields and Values from XML to SQL
	fieldsNames = ', '.join(fieldsNamesList)
	fieldsValues = ', '.join(fieldsValuesList)
	
	return sqlInsertOutput + "\n" + sqlInsertFormat.format(
														tableClassName,
														fieldsNames,
														fieldsValues,
														"id"
														)



def mountFieldsAndValues(modelClass, modelFields, indexRow, xmlDoc):
	
	#init fields names list and values list
	fieldsNamesList = []
	fieldsValuesList = []

	#Model Class attributes
	modelClassName = modelClass['odooClass']
	modelClassNodeType = modelClass['nodeType']
	modelClassNodePath = modelClass['nodePath']
	modelClassDataType = modelClass['odooDT']
	#modelClassGetValueOf = modelClass['getValueOf']

	#print("\n-------------------------------------------------------------------------\n\n")
	#print(">>> [" + str(indexRow) + "]" +
	#	" Running: OdooClass=[" + modelClassName + 
	#	"  >>  NodePath=[" + modelClassNodePath + 
	#	"  >>  NodeType=[" + modelClassNodeType +
	#	"  >>  DataType=[" + modelClassDataType + "]")

	#Fields Loop
	for field in modelFields:

		#Keep only field where Class Name matches
		if field['odooClass'] == modelClassName:	#modelClassNodePath
			
			fieldClassName = field['odooClass']
			fieldName = field['odooField']
			fieldNodeType = field['nodeType']
			fieldNodePath = field['nodePath']
			fieldDataType = field['odooDT']
			fieldValue = ""
			#fieldGetValueOf = field['getValueOf']

			#print("\n  >>>-  ClassName=[" + fieldClassName + "] - FieldNodeType=[" + fieldNodeType + 
			#			"] - FieldNodePath=[" + fieldNodePath + "]\n     >> FieldName=[" + fieldName + "]  -  FieldDataType=[" + fieldDataType + "]")

			#Get value for this field on xml
			fieldValue = getValueForFieldByNodeType(field, fieldNodeType, fieldNodePath, xmlDoc, indexRow)

			#Append Field Name
			fieldsNamesList.append(fieldName)

			#Append value formatted for sql datatype
			fieldsValuesList.append(getFormattedSQLValue(fieldDataType, fieldValue))

			#print("      > VALUE=[" + fieldValue[:64] + "]")

	return fieldsNamesList, fieldsValuesList





def mountFieldsAndValuesOfMainFields(modelClass, modelFields, indexRow, cxsd, xmlDoc):
	#
	# Uses cxsd for get info about fields and xmlDoc to get the value considering index Row
	#

	#init fields names list and values list
	fieldsNamesList = []
	fieldsValuesList = []

	#Model Class attribute20
	modelClassName = modelClass['odooClass']
	modelClassNodeType = modelClass['nodeType']
	modelClassNodePath = modelClass['nodePath']
	modelClassDataType = modelClass['odooDT']
	#modelClassGetValueOf = modelClass['getValueOf']
	mainPath = ""

	print("\n-------------------------------------------------------------------------\n\n")
	#print(">>> [" + str(indexRow) + "]" +
	#	" Running: OdooClass=[" + modelClassName + 
	#	"  >>  NodePath=[" + modelClassNodePath + 
	#	"  >>  NodeType=[" + modelClassNodeType +
	#	"  >>  DataType=[" + modelClassDataType + "]")

	for schema in cxsd.iter():

		#modelClassName MainField
		if schema.get('odooClass')==modelClassName and schema.get('nodeType')=="mainFields":

			mainPath = schema.get('nodePath')

			#print (mainPath)

		#childField nodePath
		if schema.get('odooClass')==modelClassName and schema.get('nodeType')=="childField":

			childFieldPrefixPath = schema.get('nodePath')

			#print (childFieldPrefixPath)
			
		if schema.get('odooClass')==modelClassName and schema.get('nodeType')=="childFieldData":

			if schema.get('nodePath').startswith(mainPath, 0, len(mainPath)):
				fieldClassName = schema.get('odooClass')
				fieldName = schema.get('odooField')
				fieldNodeType = schema.get('nodeType')
				fieldDataType = schema.get('odooDT')
				fieldValuePath = schema.get('nodePath')
				fieldValuePath = fieldValuePath.replace('?', str(indexRow+1))
				fieldValue = ""
				#fieldGetValueOf = field['getValueOf']

				#Append Field Name
				fieldsNamesList.append(fieldName)
				
				#Get Value for IndexRow
				fieldValue = xmlDoc.xpath(fieldValuePath)[0].text

				#Append value formatted for sql datatype
				fieldsValuesList.append(getFormattedSQLValue(fieldDataType, fieldValue))

				print("\n  >>>-  ClassName=[" + fieldClassName + "] - FieldNodeType=[" + fieldNodeType + 
						"] - FieldNodePath=[" + fieldValuePath + "]\n     >> FieldName=[" + fieldName + "]  -  FieldDataType=[" + fieldDataType + "]")
				print("      > VALUE=[" + fieldValue[:64] + "]")


		#Get ID of Main based on RelationShip using GetValueOf content
		if schema.get('odooClass')==modelClassName and schema.get('nodeType')=="relationship":

			fieldGetValueOf = schema.get('getValueOf')

			if len(fieldGetValueOf) > 0:
				fieldClassName = schema.get('odooClass')
				fieldName = schema.get('odooField')
				fieldNodeType = schema.get('nodeType')
				fieldDataType = schema.get('odooDT')
				fieldValuePath = schema.get('nodePath')
				fieldValuePath = fieldValuePath.replace('?', str(indexRow+1))
				fieldValue = -1

				#Append Field Name
				fieldsNamesList.append(fieldName)
				
				
				if fieldGetValueOf.find("(")>0:

					#Testing User Custom Functions and handling it on error case
					getValueOf = "cfuncs." + fieldGetValueOf

					try:
					    fieldValue = eval(getValueOf)
					     
					except AttributeError:

						fieldValue = - 1

				#Append value formatted for sql datatype
				fieldsValuesList.append(str(fieldValue))

				#print("\n  >>>-  ClassName=[" + fieldClassName + "] - FieldNodeType=[" + fieldNodeType + 
				#		"] - FieldNodePath=[" + fieldValuePath + "]\n     >> FieldName=[" + fieldName + "]  -  FieldDataType=[" + fieldDataType + "]")
				#print("      > VALUE=[" + fieldValue[:64] + "]")

	return fieldsNamesList, fieldsValuesList




def getValueForFieldByNodeType(field, nodeType, nodePath, xmlDoc, indexRow):
						
	outputValue=""

	#Only odoo fields and datatype defined

	if nodeType in ["simple"]:
		print("indexRow["+str(indexRow)+"]"+field['nodePath'])
		try:
			#Get value for this field on xml
			outputValue = xmlDoc.xpath(nodePath.replace('?', '1'))[indexRow].text

		except Exception as e:
			outputValue = "NONE"			

	#Deal with custom fields with has not value on xml
	elif nodeType in ["extraField"]:

		if field['getValueOf'].find("(")>0:
			#Testing User Custom Functions and handling it on error case
			getValueOf = "cfuncs." + field['getValueOf']

			try:
			    outputValue = eval(getValueOf)
			     
			except AttributeError:

				outputValue = 'ERR:' + getValueOf
		else:

			try:
				#Get value for this field on xml
				outputValue = xmlDoc.xpath(nodePath.replace('?', '1'))[indexRow].text

			except Exception as e:
				outputValue = "NONE"

	else:
		try:
			#Get value for this field on xml
			outputValue = xmlDoc.xpath(nodePath.replace('?', '1'))[indexRow].text

		except Exception as e:
			outputValue = "NODE UNDEFINED:" + nodePath

	#Removing apostrophe avoiding SQL syntax error 
	if isinstance(outputValue, str):
		outputValue=str(outputValue).translate(str.maketrans({"'":None}))

	print(outputValue)
	
	return outputValue

						

def getFormattedSQLValue(format, value):

	if format.startswith("fields.Char("):
		return "'{}'".format(value)

	elif format.startswith("fields.Integer("):
		return value

	elif format.startswith("fields.Binary("):
		return "'{}'".format(value)

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
	#    names = schemaDoc.xpath("//xsd:element[@type = $n]/@name"
	#                            namespaces={"xsd": 
	#                                        "http://www.w3.org/2001/XMLSchema"},
	#                            n=typeName)


	#---------------------------------------------------
	# RUNNING


	file_prefix = 'COR'
	
	config.inputXMLPath = "../OdooImporterData/corretiva/xml/QUEUE/" # + file_prefix + "/"
	#inputXMLFileName = "corretiva_v20_20170110-121749.xml"
	#inputXMLFileName = "COR16_1.xml"
	#inputXMLFileName = "COR16_2.xml"
	#inputXMLFileName = "COR19_1.xml"
	#inputXMLFileName = "COR20_1.xml"
	#inputXMLFileName = "COR20_2.xml"
	#inputXMLFileName = "COR20_3.xml"
	#inputXMLFileName = "COR20_4.xml"
	#inputXMLFileName = "COR20_5.xml" #faltava um field Checkout PA

	files = []
	files = [f for f in listdir(config.inputXMLPath) if isfile(join(config.inputXMLPath, f))]
	print(config.inputXMLPath)
	print("files in folder:"+str(len(files)))
	
	#f = []
	#for (dirpath, dirnames, filenames) in walk(mypath):
	#	f.extend(filenames)
		#break

	#print(dirpath)
	##print(dirnames)
	#print(filenames)

#	exit()

	print("\n____________________\n")
	
	counter = 0

	for filename in files:
		if filename[:len(file_prefix)]==file_prefix:  
			counter=counter+1
			
	print(file_prefix + " to process:"+str(counter))



	print("\n____________________\n")

	#Process all
	for filename in files:
		if filename[:len(file_prefix)]==file_prefix: 
			print("> > > >"+ filename)

			try:

				config.inputXMLFileName = filename
				config.inputXMLFile = config.inputXMLPath + config.inputXMLFileName
				
				#print(config.inputXMLFile)
				print("> > > Processing XML Doc:" + cfuncs.getXMLFilename())

				xmldoc_Parsed_Root = config.etree.parse(config.inputXMLFile).getroot()


				#Schema chooser
				config.inputCXSDFileName = cfuncs.getSchemaFilenameForPrefix(filename[:5])
				config.inputCXSDFile = config.inputCXSDPath + config.inputCXSDFileName
				
				
				print("> > > Processing With Custom Schema:" + config.inputCXSDFile)

				schema_Parsed_Root = config.etree.parse(config.inputCXSDFile).getroot()

				#Custom Vars for Custom Functions
				config.formDateTime=xmldoc_Parsed_Root.xpath('/Entry/EntryDateFromEpoch')[0].text

				status = odooInsert(schema_Parsed_Root, xmldoc_Parsed_Root, False)

				print("\n#EOF status:" + str(status))

				
			except Exception as e:
				#raise e
				print("Error:" + config.inputXMLFile + "\n" + str(e))

				status = False
			

			if status==True:
				rename(config.inputXMLFile, config.inputXMLPath + "OK/" + config.inputXMLFileName)	
			#if status==False:
				#rename(config.inputXMLFile, config.inputXMLPath + "ERRORS/" + config.inputXMLFileName)	






#---------------------------------------------------
if __name__ == "__main__":
	main()








