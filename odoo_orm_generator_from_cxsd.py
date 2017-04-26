
#
# ATT 2017-04-25 v.v10.0.48
#
# TOOLS FOR ODOO 10+
#
# GENERATE CLASSES MODEL FOR ODOO 10+
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


def odooGenerateOrmFromCXSD(schema_Parsed_Root):

	status = False
	
	pyIdent = "    "

	#Write Output Odoo Structure
	output = '# -*- coding: utf-8 -*-\n# ATT Generated at {0:%Y-%m-%d %H:%M:%S}'.format(datetime.datetime.now())
	output = output + "\n\nfrom odoo import models, fields, api\n"

	xml = schema_Parsed_Root
	
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
	for element in xml.iter():

		# Has Attributes?
		if len(element.attrib) > 0:
	
			#Only care about allowed nodeTypes
			if element.get('nodeType') in allowedNodeTypes:

				#Getting Node Attributes Values
				elementAttribValues = [
					element.get('nodeType'),
					element.get('nodePath'),
					element.get('odooClass'),
					element.get('odooField'),
					element.get('odooDT')
					]
					
				#Zip method, which combines two iterables and make it dictionary
				elementAttribDict = dict(zip(commonNodeAttributes, elementAttribValues)) 


				#Simple Classes List
				if element.get('nodeType') == "simpleClass":

					#Get Commom Attributes
					nodesAttributes = commonNodeAttributes
					
					#Add Specific Nodes
					nodesAttributes.append("odooRecName")
					nodesAttributes.append("odooSQLConstraints")

					#Getting Node Attributes Values
					elementAttribValues = [
						element.get('nodeType'),
						element.get('nodePath'),
						element.get('odooClass'),
						element.get('odooField'),
						element.get('odooDT'),
						element.get('odooRecName'),
						element.get('odooSQLConstraints')
					]
					
					#Zip method, which combines two iterables and make it dictionary
					elementAttribDict = dict(zip(nodesAttributes, elementAttribValues)) 
					
					#Keep on memory
					modelsClasses.append(elementAttribDict)
				
				elif element.get('nodeType') == "simple":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "complex":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "multipleField":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "complexFieldIdValue":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "complexFieldIdRows":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "extraField":
				
					modelFields.append(elementAttribDict)

				elif element.get('nodeType') == "relationship":
				
					modelFields.append(elementAttribDict)

				elementAttribValues.clear #Saving Memory
					
		element.clear #Saving Memory



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

	return status, output.lstrip()


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
	#	elements = []
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

	#inputXMLFile = "../corretiva_v20/xml/corretiva_v20_20170110-121749.xml"
	inputXMLFile = "../OdooImporterData/corretiva_v20/schemas/corretiva_v20_20170110.cxsd"

	parser = etree.XMLParser() 
	
	cxsdSchema = etree.parse(inputXMLFile).getroot()

	status, outputText = odooGenerateOrmFromCXSD(cxsdSchema)

	#outputText = strip_one_space(outputText)

	writeOut(outputText,"/Users/andersontagata/TemosEngenharia/custom-addons/corretiva/models/corretiva_model_v20.py")
	writeOut(outputText,"../OdooImporterData/corretiva_v20/models/corretiva_model_v20.py")

	print(outputText)
	print("\n#EOF status:" + str(status))









#---------------------------------------------------
if __name__ == "__main__":
	main()








