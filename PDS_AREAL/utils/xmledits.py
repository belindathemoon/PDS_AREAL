import glob
import xml.etree.ElementTree as ET
ET.register_namespace('',"http://pds.nasa.gov/pds4/pds/v1")
ET.register_namespace('xsi',"http://www.w3.org/2001/XMLSchema-instance")
ET.register_namespace('disp',"http://pds.nasa.gov/pds4/disp/v1")

def update_descriptions(textHeader, textImage, pathvar):
	xmlversion = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1A10.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n'''
	search_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	replace_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:disp="http://pds.nasa.gov/pds4/disp/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	for file in glob.glob(pathvar):
		with open(file, 'r') as activefile:
			text = activefile.read()
			text = text.replace(search_text, replace_text)
		with open(file, 'w') as activefile:
			activefile.write(text)
		tree = ET.parse(file)
		root = tree.getroot()
		FileAreaObservational = root.find('{http://pds.nasa.gov/pds4/pds/v1}File_Area_Observational')
		Header = FileAreaObservational.find('{http://pds.nasa.gov/pds4/pds/v1}Header')
		HeaderDescription = Header.find('{http://pds.nasa.gov/pds4/pds/v1}description')
		Array2DImage = FileAreaObservational.find('{http://pds.nasa.gov/pds4/pds/v1}Array_2D_Image')
		ImageDescription = Array2DImage.find('{http://pds.nasa.gov/pds4/pds/v1}description')
		HeaderDescription.text = textHeader
		ImageDescription.text = textImage
		tree.write(file)
		with open(file, 'r') as f:
			filedata = f.read()
		filedata = xmlversion + filedata
		with open(file, 'w') as f:
			f.write(filedata)

def update_pubyear(year, pathvar):
	xmlversion = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1A10.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n'''
	search_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	replace_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:disp="http://pds.nasa.gov/pds4/disp/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	for file in glob.glob(pathvar):
		with open(file, 'r') as activefile:
			text = activefile.read()
			text = text.replace(search_text, replace_text)
		with open(file, 'w') as activefile:
			activefile.write(text)
		tree = ET.parse(file)
		root = tree.getroot()
		IDArea = root.find('{http://pds.nasa.gov/pds4/pds/v1}Identification_Area')
		CitationInfo = IDArea.find('{http://pds.nasa.gov/pds4/pds/v1}Citation_Information')
		PubYear = CitationInfo.find('{http://pds.nasa.gov/pds4/pds/v1}publication_year')
		PubYear.text = year
		tree.write(file)
		with open(file, 'r') as f:
			filedata = f.read()
		filedata = xmlversion + filedata
		with open(file, 'w') as f:
			f.write(filedata)

def update_time(start_date_time, stop_date_time, pathvar):
	xmlversion = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1A10.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n'''
	search_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	replace_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:disp="http://pds.nasa.gov/pds4/disp/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	for file in glob.glob(pathvar):
		with open(file, 'r') as activefile:
			text = activefile.read()
			text = text.replace(search_text, replace_text)
		with open(file, 'w') as activefile:
			activefile.write(text)
		tree = ET.parse(file)
		root = tree.getroot()
		ContextArea = root.find('{http://pds.nasa.gov/pds4/pds/v1}Context_Area')
		TimeCoord = ContextArea.find('{http://pds.nasa.gov/pds4/pds/v1}Time_Coordinates')
		start = TimeCoord.find('{http://pds.nasa.gov/pds4/pds/v1}start_date_time')
		stop = TimeCoord.find('{http://pds.nasa.gov/pds4/pds/v1}stop_date_time')
		start.text = start_date_time
		stop.text = stop_date_time
		tree.write(file)
		with open(file, 'r') as f:
			filedata = f.read()
		filedata = xmlversion + filedata
		with open(file, 'w') as f:
			f.write(filedata)

def fixLIDs(bundleID,collectionID,pathvar):
	xmlversion = '''<?xml version="1.0" encoding="UTF-8"?>
<?xml-model href="https://pds.nasa.gov/pds4/pds/v1/PDS4_PDS_1A10.sch" schematypens="http://purl.oclc.org/dsdl/schematron"?>\n'''
	search_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	replace_text = '''<Product_Observational xmlns="http://pds.nasa.gov/pds4/pds/v1"
		xmlns:disp="http://pds.nasa.gov/pds4/disp/v1"
		xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"'''
	for file in glob.glob(pathvar):
		filename = file.rsplit('/',1)[1]
		fileID = filename.rsplit('.',1)[0]
		with open(file, 'r') as activefile:
			text = activefile.read()
			text = text.replace(search_text, replace_text)
		with open(file, 'w') as activefile:
			activefile.write(text)
		tree = ET.parse(file)
		root = tree.getroot()
		IDArea = root.find('{http://pds.nasa.gov/pds4/pds/v1}Identification_Area')
		LID = IDArea.find('{http://pds.nasa.gov/pds4/pds/v1}logical_identifier')
		LID.text = 'urn:nasa:pds:' + bundleID + ':' + collectionID + ':' + fileID
		tree.write(file)
		with open(file, 'r') as f:
			filedata = f.read()
		filedata = xmlversion + filedata
		with open(file, 'w') as f:
			f.write(filedata)
