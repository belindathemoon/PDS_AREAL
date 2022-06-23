####--------About the variables------######
# The header entries might have different key names in each collection, and so the keys are variables which you may change, however they have defaults set (ex. waveleng = 'WAVELENG').
# *logs_path* is the path to where the logs should be saved. !!!Make sure there is a trailing slash!!! For example: /prvt/juno1/PDART_files/jup_supp.geminis_trecs/document/header_observing_logs/
# *day_path* is the path to the day-level directories of the data in the form of '/prvt/juno1/PDART_files/bundle_name/data_raw/*/*'. The fits files should be in these day directories (the code below is set up for data in a directory with the format of '/path-to-bundle/data_raw/yyyy/mm-dd/filename.fits'). This path variable should go only as deep as the mm-dd subdirectory, with the year and date as wilcards, for example: 'prvt/juno1/PDART_files/jup_supp.geminis_trecs/data_raw/*/*' (NO TRAILING SLASH)
# *documents* is the name of your documents folder (it should be in the path in logs_path)
########--------End Variables--------#####
import glob
import os
from astropy.io import fits

def create_header_observing_logs(logs_path, day_path, documents = 'document', WAVELENG = 'WAVELENG', DATEOBS = 'DATE-OBS', TIMEOBS = 'TIME-OBS', CHPFREQ = 'CHPFREQ', OBSMODE = 'OBSMODE',AIRMASS = 'AIRMASS'):
    """Create Header Observing Logs

    Use this to create the observing logs of a data_raw collection. It takes specific data from the header, uses Astropy fits to create a dictionary, and then prints the header logs. A text file is created for each day.

    Args:
        logs_path (str): the path to where the logs should be saved. 
            !!!Make sure there is a trailing slash!!! 
            For example: /prvt/juno1/PDART_files/jup_supp.geminis_trecs/document/header_observing_logs/
        day_path (str): The path to the day-level directories of the data in the form of 
            '/prvt/juno1/PDART_files/bundle_name/data_raw/\*/\*'. The fits files should be in these day 
            directories (the code below is set up for data in a directory with the format of 
            '/path-to-bundle/data_raw/yyyy/mm-dd/filename.fits'). 
            This path variable should go only as deep as the mm-dd subdirectory, with the year and date 
            as wilcards, for example: 'prvt/juno1/PDART_files/jup_supp.geminis_trecs/data_raw/\*/\*' 
            (NO TRAILING SLASH)
        documents (:obj:`str`, optional): The name of your documents folder (it should be in the path in logs_path).
        WAVELENG (:obj:`str`, optional): The header entries might have different key names in each collection. This
            defaults to 'WAVELENG', however check a sample fits header for the correct wavelength key.
        DATEOBS (:obj:`str`, optional): The header entries might have different key names in each collection. This
            defaults to 'DATE-OBS', however check a sample fits header for the correct observation date key.
        TIMEOBS (:obj:`str`, optional):The header entries might have different key names in each collection. This
            defaults to 'TIME-OBS', however check a sample fits header for the correct observation time key.
        CHPFREQ (:obj:`str`, optional): The header entries might have different key names in each collection. This
            defaults to 'CHPFREQ', however check a sample fits header for the correct chop frequency key.
        OBSMODE (:obj:`str`, optional): The header entries might have different key names in each collection. This
            defaults to 'OBSMODE', however check a sample fits header for the correct observation mode key.
        AIRMASS (:obj:`str`, optional): The header entries might have different key names in each collection. This
            defaults to 'AIRMASS', however check a sample fits header for the correct airmass key.

    """
    for day in glob.glob(day_path):
        print('Accessing: ' + day)
        #Get the year from the path, then check to make sure it's not the documents folder. We'll also use the year in the second for-loop.
        year = day.rsplit('/')[-2]
        if year == documents:
            continue
        #gets the name of the date folder and assigns it to variable 'date'
        date = day.rsplit('/',1)[1]
        print('Looping through folder: ' + date)
        #gets the rest of the path. We use this below in the second for-loop
        path = day.rsplit('/',2)[0]
        #gets the logs_path, adds the date from previous line, and adds .txt file extention
        log_name = str(logs_path + year + '_' + date + '.txt')
        print('Creating: ' + log_name)
        #checks that the file doesn't already exists
        if os.path.exists(log_name) == True:
            print(log_name + ' already exists. Starting back at the top.')
            continue
        #Creates the new text file
        log = open(log_name, 'x')
        print('Opening ' + log_name)
        #This is the heading of our new text file.
        #You might have to adjust the tabs to get this perfect.
        log.write('File Name\t\t\t\tWavelength\t\tObservation Date\tTime in UT\t\tChop Frequency\t\tObservation Mode\t\tAir Mass')
        print('Wrote heading')
        ### Need to add something here that will limit the data_path in the next for-loop so that it only looks in the data of that day!
        data_path = path + '/' + year + '/' + date + '/*.fits'
        #This for loop now goes through each fits file in the date folder
        for path in glob.glob(data_path):
            print('Adding ' + path + ' to log.')
            #gets the filename from the path 
            filename = path.rsplit('/',1)[1]
            #uses astropy fits to create a header object. A data object is also created, but we don't use it here.
            img = fits.open(path)
            header = img[0].header
            #uses astropy verify to fix the header before continuing.
            img[0].verify('fix')
            #create the strings for printing, dealing with any errors that come up
            try:
                wavelength = str(header[WAVELENG])
            except KeyError:
                try:
                    if str(header['FILTER']) == 'K':
                        wavelength = str('2.2   ')
                    elif str(header['FILTER']) == 'N0':
                        wavelength = str('7.9   ')
                    elif str(header['FILTER']) == 'N1':
                        wavelength = str('8.7   ')
                    elif str(header['FILTER']) == 'N2':
                        wavelength = str('9.6   ')
                    elif str(header['FILTER']) == 'N3':
                        wavelength = str('10.3  ')
                    elif str(header['FILTER']) == 'N4':
                        wavelength = str('11.7  ')
                    elif str(header['FILTER']) == 'N5':
                        wavelength = str('12.5  ')
                    elif str(header['FILTER']) == 'Q0':
                        wavelength = str('17.24 ')
                    elif str(header['FILTER']) == 'Q1':
                        wavelength = str('17.93 ')
                    elif str(header['FILTER']) == 'Q2':
                        wavelength = str('18.67 ')
                    elif str(header['FILTER']) == 'Q3':
                        wavelength = str('20.82 ')
                    elif str(header['FILTER']) == 'Q4':
                        wavelength = str('22.79 ')
                    elif str(header['FILTER']) == 'Qt':
                        wavelength = str('24.2  ')
                    elif str(header['FILTER']) == 'Q5':
                        wavelength = str('24.2  ')
                    elif str(header['FILTER']) == 'Q-s':
                        wavelength = str('17.9  ')
                    elif str(header['FILTER']) == 'Q-1':
                        wavelength = str('22.43 ')
                    elif str(header['FILTER']) == 'N':
                        wavelength = str('10.79 ')
                    elif str(header['FILTER']) == 'M':
                        wavelength = str('4.8   ')
                    else:
                        wavelength = 'unknown'
                except KeyError:
                    wavelength = 'unknown'
            # Make the wavelength entries the same length for proper formatting.
            if len(wavelength) == 3:
                wavelength = wavelength + '   '
            if len(wavelength) == 4:
                wavelength = wavelength + '  '
            if len(wavelength) == 5:
                wavelength = wavelength + ' '
            try:
                observationDate = str(header[DATEOBS])
            except KeyError:
                observationDate = 'unknown'
            try:
                observationTime = str(header[TIMEOBS])
            except KeyError:
                observationTime = 'unknown'
            try:
                frequency = str(header[CHPFREQ])
            except KeyError:
                frequency = 'unknown'
            try:
                observationMode = str(header[OBSMODE])
            except KeyError:
                observationMode = 'unknown'
            try:
                airmass = str(header[AIRMASS])
            except KeyError:
                airmass = 'unknown'
            #This is the data of our new text file.
            #You might have to adjust the tabs and spaces here depending on the lengths of the strings
            log.write('\n' + filename + '\t\t' + wavelength + '  ' + '\t\t' + observationDate + '\t\t' + observationTime + '\t\t\t' + frequency + '  ' + '\t\t\t' + observationMode + '    ' + '\t\t\t' + airmass)
        #Always make sure to close up shop!
        log.close()
        print('Done.')

def create_logs_instructions():
    print("####--------About the variables------######\n# The header entries might have different key names in each collection, and so the keys are variables which you may change, however they have defaults set (ex. waveleng = 'WAVELENG').\n# *logs_path* is the path to where the logs should be saved. !!!Make sure there is a trailing slash!!! For example: /prvt/juno1/PDART_files/jup_supp.geminis_trecs/document/header_observing_logs/\n# *day_path* is the path to the day-level directories of the data in the form of '/prvt/juno1/PDART_files/bundle_name/data_raw/*/*'. The fits files should be in these day directories (the code below is set up for data in a directory with the format of '/path-to-bundle/data_raw/yyyy/mm-dd/filename.fits'). This path variable should go only as deep as the mm-dd subdirectory, with the year and date as wilcards, for example: 'prvt/juno1/PDART_files/jup_supp.geminis_trecs/data_raw/*/*' (NO TRAILING SLASH)\n# *documents* is the name of your documents folder (it should be in the path in logs_path)\n########--------End Variables--------#####")
