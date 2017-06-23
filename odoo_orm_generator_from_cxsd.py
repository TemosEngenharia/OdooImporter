#!/usr/bin/env python
# -*- coding uft-8 -*-
#
# ATT 2017-06-05 v.v10.1.0 - refactoring paths
# ATT 2017-05-22 v.v10.0.57 - first line added to allow execute without python pre-command on prompt
# ATT 2017-05-05 v.v10.0.56 - setting creation using COR27.cxsd
# ATT 2017-05-02 v.v10.0.51 - new child class and relationship
# ATT 2017-04-26 v.v10.0.50 - Added new type of Class (mainClass and childClass)
# ATT 2017-04-26 v.v10.0.49
# ATT 2017-04-25 v.v10.0.48
#
# TOOLS FOR ODOO 10+
#
# GENERATE CLASSES MODEL FOR ODOO 10+
#

import datetime
import conf.odoo_importer_from_xml_cxsd_config as config 
import libs.odoo_importer_from_xml_cxsd_custom_functions as cfuncs


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

    allowedNodeTypes = ["mainClass", "childClass", "simple", "complex", "multipleField", 
                        "complexFieldIdValue", "complexFieldIdRows", "extraField", 
                        "relationship", "mainFields", "childField", "childFieldData"
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
                if element.get('nodeType') in ["mainClass", "childClass"]:

                    #Get Commom Attributes
                    nodesAttributes = list(commonNodeAttributes)
                    
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

                elif element.get('nodeType') in ["mainFields", "childField", "childFieldData"]:
                
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
#           #Fields Loop
#           for f in range(len(modelFields)):
#               #Keep only field where Class Name matches
#               if modelFields[f]['odooClass']==modelClassName: 
#                   
#                   #Write Odoo Default Name Field
#                   output = '\n{}{}{} = "{}"\n'.format(
#                                                       output, 
#                                                       pyIdent, 
#                                                       modelFields[f]['odooField'], 
#                                                       modelFields[f]['odooDT']
#                                                       )
#
#                   del modelFields[f-1]

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

    #Start Up Settings
    config.init("dev_mode")

    config.main_id = -1

    print(config.settings)


    # RUNNING
    #Schema chooser
#    filename = "MCO"
#    config.inputCXSDPath = "data/mco/schemas/"
    
    filename = "IPO"
    config.inputCXSDPath = "/opt/odoo-dev/tools/OdooImporter/data/ipo/schemas/"

    config.inputCXSDFileName = cfuncs.getSchemaFilenameForPrefix(filename[:3])
    config.inputCXSDFile = config.inputCXSDPath + config.inputCXSDFileName

    print("> > > Creating by Custom Schema:" + config.inputCXSDFile)

    #Generate using Schema CXSD
    status, outputText = odooGenerateOrmFromCXSD(config.etree.parse(config.inputCXSDFile).getroot())

    #Save on file model.py for odoo
    #developer usage
    #writeOut(outputText,config.outputORMFile)

    #Save in Data Domain
    writeOut(outputText,config.outputORMFile_InDataDomain)

    #Show result on prompt
    print(outputText)
    print("\n#EOF status:" + str(status))



#---------------------------------------------------
if __name__ == "__main__":
    main()










