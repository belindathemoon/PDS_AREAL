import glob 
import os

def replace_text(rootdir, search_text, replace_text, print_status=True, file_type='.xml'):
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
    for filestring in glob.glob(directory):
        shorten_seconds(filestring)
