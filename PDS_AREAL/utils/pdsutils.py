import glob 
import os

def replace_text(rootdir, search_text, replace_text, print_status=True, file_type='.xml'):
    """ Replace Text
    
    Replace text in labels (or any .txt or .xml file).
    
    Args:
        rootdir (str): The root directory of the files to look for the bad text. For example, if you wanted to
            look for all the xml files in a data_raw collection, they would be in many subdirectories, so the
            root directory would be data raw. Use an absolute path.
        search_text (str): The text you wish to find and replace (the incorrect text).
        replace_text (str): The text you wish to use as a replacement (the correct text)
        print_status (:obj:`bool`, optional): By default, the function will print status to the terminal. For 
            quiet mode, change to False.
        file_type (str): The type of file you wish to edit. By default, the function looks for XML files.

    """
    for dirpath, dirs, files in os.walk(rootdir):
        for file in files:
            if file.endswith(file_type):
                filepath = os.path.join(dirpath, file)
                if print_status:
                    print('checking: ' + filepath)
                with open(filepath, 'r') as activefile:
                    text = activefile.read()
                    text = text.replace(search_text, replace_text)
                with open(filepath, 'w') as activefile:
                    activefile.write(text)
    print('Done')

def shorten_seconds(filestring):
    """ Shorten Seconds
    
    Unless you wish to only edit one file, use dir_shorten_seconds instead.
    
    Args:
        filestring (str): The path to the file you want to fix.

    """
    old_text = open(filestring, 'r')
    new_text = ""
    lines = old_text.readlines()
    for line in lines:
        if '<start_date_time>' not in line:
            new_text += line
        else:
            indent = line.split('<',1)[0]
            opentag = '<' + line.split('<',1)[1].split('>',1)[0] + '>'
            closetag = '<' + line.split('<')[-1]
            timestring = line.split('>',1)[1].split('<',1)[0]
            mseconds = timestring[timestring.find('.'):-1]
            if len(mseconds) > 4:
                print('incorrect: ' + timestring)
                timestring = timestring[:25] + 'Z'
                print('corrected: ' + timestring)
                reassemble = indent + opentag + timestring + closetag
                new_text += reassemble
                print('Edited ' + filestring)
    old_text.close()
    old_text = open(filestring, 'w')
    old_text.write(new_text)
    old_text.close()

def dir_shorten_seconds(directory):
    """ Shorten Seconds - Directory
    
    The newest labeling code includes this, however for older labels, this will fix the extra decimals seconds
        in start_time and end_time. Run this to check and fix all of the files in a directory
    
    Args:
        directory (str): The absolute path to the files in the directory you want to fix, with wildcards. 
            For example "/prvt/juno1/PDART_files/jup_supp.geminis_trecs/data_raw/\*/\*/\*.xml

    """
    for filestring in glob.glob(directory):
        shorten_seconds(filestring)
