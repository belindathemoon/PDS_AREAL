def create_fits_labels(pathvar, templatevar, collection_name, bundle_name, title, product_class, product_author_list, observing_system, telescope_name, telescope_lid, instrument_name, instrument_lid, document_lid, fits_desc, fits_prolvl, fits_primdesc, mu_desc = 'Ground Based FITS, emission angle adjustment for cylindrical map.', cmap_desc = 'Ground Based FITS, cylindrical map projection.', vdop_desc = 'Ground Based FITS, doppler shift adjustment for cylindrical map.', mu_prolvl = 'Derived', cmap_prolvl = 'Derived', vdop_prolvl = 'Derived', mu_primdesc = 'Cosine of the emission angle for each point on cylindrical map from the angle between the local zenith and direction of the Earth-based observer', cmap_primdesc = 'Projection onto linear cylindrical coordinate system longitude in System III along abscissa and planetocentric latitude in the ordinate', vdop_primdesc = 'Radial velocity of cylindrical map according to an Earth-based observer for CH4 emission interference at 7.9 microns with telluric CH4 absorption', extrablocks = 0, editor_list = 'Neakrase, Lynn; Huber, Lyle', publication_year = str(datetime.date.today().year), wavelength_range = 'Infrared', investigation_name = 'Jupiter Support Monitoring Observations', investigation_type = 'Observing Campaign', investigation_lid = 'observing_campaign.jupiter_support', observatory_name = 'NASA InfraRed Telescope Facility', observatory_lid = 'observatory.irtf-maunakea.3m2', target_name = 'Jupiter', target_type = 'Planet', target_lid = 'planet.jupiter', parsing_standard = 'FITS 3.0', header_description = 'The header contains information about how the image was collected and any processing that may have happened.', image_description = "The image shows Jupiter's atmosphere.", array_type = 'IEEE754MSBSingle', array_unit = 'DN', rewrite = False): 
    errors = ''
    error_count = 0
    for path in glob.glob(pathvar):
        if rewrite == False:
            if os.path.exists(path.replace('.fits', '.xml')):
                continue
        template = open(templatevar, 'r')
        filename = path.rsplit('/',1)[1]
        print('Opening: ' + path)
        try:
            img = fits.open(path)
            img[0].verify('fix')
            hdr = img[0].header
        except OSError as e:
            errors += 'Error: ' + str(e) + ' | File: ' + path + '\n'
            error_count += 1
            print(e)
            print('************\n!!!!!!!!!!!!!!\nSkipping ', path, ' due to error (see above)\n!!!!!!!!!!!!\n**************')
            continue
        new_label = open(path.replace('.fits', '.xml'), 'w')
        print('Writing label: ' + filename)
        #prepare variables for filling in values below
        #Prepare date and time for PRODUCT_CREATION_DATE
        try:
            obsdate = str(hdr['DATE-OBS'])
        except KeyError:
            try:
                obsdate = str(hdr['DATEOBS'])
            except KeyError:
                try:
                    obsdate = str(hdr['DATE_OBS'])
                except KeyError:
                    print('MISSING DATE! Check header key for observation date.')
                    datenil = True
                    obsdate = ''
        if re.match("\d\d/\d\d/\d\d\d\d", obsdate):
            yyyy = obsdate[6:]
            mm = obsdate[0:2]
            dd = obsdate[3:5]
            datecoord = str(yyyy + '-' + mm + '-' + dd)
        elif re.match("\d\d/\d\d/\d\d", obsdate):
            yy = obsdate[6:]
            mm = obsdate[0:2]
            dd = obsdate[3:5]
            if yy[0] == '9':
                yyyy = '19' + yy
            elif yy[0] == '0' or yy[0] == '1' or yy[0] == '2' or yy[0] == '3':
                yyyy = '20' + yy
            datecoord = str(yyyy + '-' + mm + '-' + dd)
        elif re.match("\d\d\d\d\-\d\d\-\d\d", obsdate):
            datecoord = str(obsdate)
        elif obsdate == '':
            datecoord = ''
        else:
            print('DATE FORMAT ERROR! Check header key for observation date.')
            datenil = True
            datecoord = ''
        try:
            obstime = 'T' + str(hdr['TIME-OBS'])
        except KeyError:
            try:
                obstime = 'T' + str(hdr['TIME-STR'])
            except KeyError:
                try:
                    obstime = 'T' + str(hdr['TIME_OBS'])
                except KeyError:
                    print('MISSING TIME! Check header key for observation start time.')
                    obstime = ''
        seconds = obstime.rsplit(':',1)[1]
        splitseconds = seconds.rsplit('.',1)[1]
        while len(splitseconds) > 4:
            splitseconds = splitseconds[:-1]
        obstime = obstime.rsplit('.',1)[0] + '.' + splitseconds
        timecoord = datecoord + obstime + 'Z'
        #prepare date and time for PRODUCT_STOP_TIME
        try:
            endtime = 'T' + str(hdr['TIME-END'])
        except KeyError:
            endtime = ''
            endtimenil = True
        endtimecoord = '>' + datecoord + endtime + 'Z'
        #start_date_time and stop_date_time can't be the same, so check if they are, and if so, set the stop_date_time as nil
        endtimenil = False
        if endtimecoord == timecoord:
            endtimenil = True
        if endtimenil:
            product_stop_time = ' xsi:nil="true" nilReason="unknown">'
        else:
            product_stop_time = endtimecoord
        #prepare header offset for BYTES value
        headerlen = len(hdr) #number of lines in the header
        numbercards = headerlen/36 #number of 80-byte cards
        hdrblocks = math.ceil(numbercards) #number of logical blocks
        hdrblocks = hdrblocks + extrablocks #accounts for additional header blocks that can't be read by astropy
        offsetbytes = str(hdrblocks * 2880) #offset bytes from the header to the array
        #dictionaries
        if filename[-7:] == 'mu.fits':
            key = 'mu.fits'
        elif filename[-9:] == 'cmap.fits':
            key = 'cmap.fits'
        elif filename[-9:] == 'vdop.fits':
            key = "vdop.fits"
        elif filename[-5:] == '.fits':
            key = "fits"
        else:
            print('Filename extension error. Not a fits file. Description may be missing in label.')
        desc = {"mu.fits": mu_desc, "cmap.fits": cmap_desc, "vdop.fits": vdop_desc, "fits": fits_desc}
        prolvl = {"mu.fits": mu_prolvl, "cmap.fits": cmap_prolvl, "vdop.fits": vdop_prolvl, "fits": fits_prolvl}
        primdesc = {"mu.fits": mu_primdesc, "cmap.fits": cmap_primdesc, "vdop.fits": vdop_primdesc, "fits": fits_primdesc}
        for line in template:
            if '$' not in line:
                new_label.write(line)
            else:
                var = line[line.find('$')+1:line.rfind('$')]
                val = {
                   'PRODUCT_ID': filename.rsplit('.',1)[0],
                   'LID': bundle_name + ':' + collection_name + ':' + filename.rsplit('.',1)[0],
                   'COLLECTION_NAME': collection_name,
                   'BUNDLE_NAME': bundle_name,
                   'TITLE': title,
                   'PRODUCT_CLASS': product_class,
                   'PRODUCT_AUTHOR_LIST': product_author_list,
                   'EDITOR_LIST': editor_list,
                   'PUBLICATION_YEAR': publication_year,
                   'DESCRIPTION':  desc.get(key),
                   'MODIFICATION_DATE': datetime.date.fromtimestamp(os.path.getctime(path)).isoformat(),
                   'FILE_NAME': filename,
                   'REFERENCE_LID': bundle_name + ':document:' + document_lid,
                   'PRODUCT_CREATION_DATE': timecoord,
                   'PRODUCT_STOP_TIME': product_stop_time,
                   'PROCESSING_LEVEL': prolvl.get(key),
                   'PRIMARY_DESCRIPTION': primdesc.get(key),
                   'WAVELENGTH_RANGE': wavelength_range,
                   'INVESTIGATION_NAME': investigation_name,
                   'INVESTIGATION_TYPE': investigation_type,
                   'INVESTIGATION_LID': investigation_lid,
                   'OBSERVING_SYSTEM': observing_system,
                   'OBSERVATORY_NAME': observatory_name,
                   'OBSERVATORY_LID': observatory_lid,
                   'TELESCOPE_NAME': telescope_name,
                   'TELESCOPE_LID': telescope_lid,
                   'INSTRUMENT_NAME': instrument_name,
                   'INSTRUMENT_LID': instrument_lid,
                   'TARGET_NAME': target_name,
                   'TARGET_TYPE': target_type,
                   'TARGET_LID': target_lid,
                   'DOCUMENT_LID': document_lid,
                   'FILE_SIZE': str(os.path.getsize(path) - offsetbytes),
                   'PARSING_STANDARD': parsing_standard,
                   'HEADER_DESCRIPTION': header_description,
                   'IMAGE_DESCRIPTION': image_description,
                   'ARRAY_TYPE': array_type,
                   'ARRAY_UNIT': array_unit,
                   'BYTES': offsetbytes,
                   'LINE_SAMPLES': str(hdr['NAXIS1']),
                   'LINES': str(hdr['NAXIS2']),
                }[var]
                new_label.write(line.replace('$' + var + '$', val))
        template.close()
        new_label.close()
    print('****************\nCollection labels complete.\n****************')
    if error_count == 0:
        print('No file errors were found!')
    else:
        print('Error log:\nError count:', error_count, '\n', errors)
