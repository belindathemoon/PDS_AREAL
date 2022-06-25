import glob
import os

def create_inventory(bundle_name, collection_path, data_path, file_extension):
	"""Create Inventory

	Create a CSV inventory for any collection.

	Args:
		bundle_name (str): The name of the bundle directory.
			Ex. 'jup_supp.geminis_trecs' or 'jup_supp.irtf_mirsi'.
		collection_path (str): The path to the collection which needs the inventory.
			Do not include a trailing slash! Ex. '/prvt/juno1/PDART_files/jup_supp.irtf_mirsi/data_raw'
		data_path (str): The path all the way to individual fits files, using wildcards for the
			subdirectories of the collection.
			Ex. '/prvt/juno1/PDART_files/jup_supp.irtf_mirsi/data_raw/\*/\*/\*.fits'
		file_extension (str): The type of file to be included. Ex. '.fits', '.txt' or '.tif'
		
	"""
	collection_name = collection_path.rsplit('/',1)[1]
	inventory_filename = 'collection_' + bundle_name + '_' + collection_name + '_inventory.csv'
	inventory_path = collection_path + '/' + inventory_filename
	if os.path.exists(inventory_path):
		print('File already exists')
		return
	print('Creating temp file ' + inventory_filename + ' for ' + collection_name)
	inventory_rows = ''
	for path in glob.glob(data_path):
		if path[-len(file_extension):] == file_extension:
			filename = path.rsplit('/',1)[1]
			file_id = filename[:-len(file_extension)]
			inventory_rows += 'P, ' + 'urn:nasa:pds:' + bundle_name + ':' + collection_name + ':' + file_id + '::1.0\n\n'
	inventory = open(inventory_path, 'w')
	print('Writing temp file to permanent file')
	inventory.write(inventory_rows)
	inventory.close
	print('Done. Nice work!')

def create_inventory_instructions():
    print("'*bundle_name* is a string that is the directory name within which the collection exists. Ex. 'jup_supp.irtf_mirsi'\n*collection_path* is a string that is the path to the collection which needs the inventory. Do not include a trailing slash. Ex. '/prvt/juno1/PDART_files/jup_supp.irtf_mirsi/data_raw'\n*data_path* is a string that is the path all the way to individual fits files, using wildcards for the subdirectories of the collection. Ex. '/prvt/juno1/PDART_files/jup_supp.irtf_mirsi/data_raw/*/*/*.fits'\n*file_extension* is a string and the type of file (including '.') that should be included. Ex. '.fits' or '.tif'")

