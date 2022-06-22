import datetime
import glob
import os

def create_header_observing_labels(pathvar, templatevar, collection_name, bundle_name, bundle_title, product_author_list, instrument_lid, editor_list = 'Neakrase, Lynn; Huber, Lyle', publication_year = str(datetime.date.today().year), keyword = 'Jupiter', description = 'Observing log produced from FITS image headers'): 
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
