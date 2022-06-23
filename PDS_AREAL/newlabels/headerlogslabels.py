import datetime
import glob
import os

def create_header_observing_labels(pathvar, templatevar, collection_name, bundle_name, bundle_title, product_author_list, instrument_lid, editor_list = 'Neakrase, Lynn; Huber, Lyle', publication_year = str(datetime.date.today().year), keyword = 'Jupiter', description = 'Observing log produced from FITS image headers'): 
    """Create Header Observing Logs Labels
    
    Create new xml labels for .txt observing logs (created from the FITS headers) in the documents collection.
    
    Args:
        pathvar (str): The absolute path to the logs files you wish to label. 
            Ex. '/prvt/juno1/PDART_files/jup_supp.irtf_mirsi/documents/header_observing_logs/\*.txt'.
        templatevar (str): The absolute path to the label template. 
            Ex. '/home/bblakley/scripts/header_observing_logs_labels.txt'
        collection_name (str): The name of the collection directory. Usually 'documents'.
        bundle_name (str): The name of the bundle directory. Ex. 'jup_supp.geminis_trecs' 
            or 'jup_supp.irtf_mirsi'.
        bundle_title (str): A descriptive title for the labels that matches the fits collections. 
            Ex. 'NASA IRTF 3-Meter Telescope - MIRSI Observation' or 'T-ReCS Observation'.
        product_author_list (str): The authors of the observations (not to be confused with the 
            authors of the labels). Ask Glenn if you can't tell from the image headers. Must be a list of 
            authors' 'last name, first name' separated by semicolons.
            Ex. 'Orton, Glenn; Venkatesan, Malavika; Kim, Min Hyuk; Yanamandra-Fisher, Padma; Chung, Jennie'
        instrument_lid (str): The PDS LID of the instrument. Ex. 'irtf-maunakea.3m2.mirsi'. Check with Lynn.
        editor_list (:obj:`str`, optional): PDS editors. Defaults to 'Neakrase, Lynn; Huber, Lyle'.
        publication_year (:obj:`str`, optional): Year that the bundle will be published to the PDS. 
            With no user input, defaults to this year (uses datetime).
        keyword (:obj:`str`, optional): The target of these observations. Defaults to 'Jupiter'.
        description (:obj:`str`, optional): A description for the logs label. 
            Defaults to 'Observing log produced from FITS image headers'.

    """
    for path in glob.glob(pathvar):
        if os.path.exists(path.replace('.txt', '.xml')):
            continue
        template = open(templatevar, 'r')
        filename = path.rsplit('/',1)[1]
        new_label = open(path.replace('.txt', '.xml'), 'w')
        print('Writing label: ' + filename)
        for line in template:
            if '$' not in line:
                new_label.write(line)
            else:
                var = line[line.find('$')+1:line.rfind('$')]
                val = {
                   'LID': bundle_name + ':' + collection_name + ':' + filename,
                   'TITLE': bundle_title + 'Observing Log',
                   'PRODUCT_AUTHOR_LIST': product_author_list,
                   'EDITOR_LIST': editor_list,
                   'PUBLICATION_YEAR': publication_year,
                   'KEYWORD': keyword,
                   'DESCRIPTION':  description,
                   'MODIFICATION_DATE': datetime.date.fromtimestamp(os.path.getctime(path)).isoformat(),
                   'INSTRUMENT_LID': instrument_lid,
                   'FILE_NAME': filename,
                   'CREATION_DTIME': datetime.datetime.utcfromtimestamp(int(os.path.getmtime(path))).strftime('%Y-%m-%dT%H:%M:%SZ'),
                   'LOCAL_ID': filename.rsplit('.',1)[0],
                }[var]
                new_label.write(line.replace('$' + var + '$', val))
        template.close()
        new_label.close()
    print('****************\nHeader logs labels complete.\n****************')
