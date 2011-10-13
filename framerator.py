from svgfig import *
import os
import config
inkscape_location = '/Applications/Inkscape.app'

def generateFile (detail):

	# load it and save it using SVG fig. This will write out elements on single lines. 
	svg = load(detail[0])
	svg.save ("temp.svg")

	# now we can mess with temp.svg using regex hackery
		
	#<g style="display:none" inkscape:label="head-low" id="layer8" inkscape:groupmode="layer">
	#<g style="display:inline;filter:url(#filter5341)" inkscape:label="head-middle" id="layer7" inkscape:groupmode="layer">
	# we can just use display:inline ... assuming the filter stuff does layer opacity etc. Don't care about that

	fileOut = open ("temp_out.svg", "wt")
	fileIn = open ("temp.svg", "rt")
	lines = fileIn.readlines ()

	for line in lines:
		# is this line a layer?
		exp = "(.*style=\\\")([^\\\"]+)(\\\".*inkscape:label=\\\")([^\\\"]+)(\\\".*inkscape:groupmode=\\\"layer\\\".*)"
		regexp = re.compile(exp, re.I)
		match = regexp.search(line)
		if (match):
			layer = match.group(4)
			if (layer in detail[4]):
				# this is a layer we want
				fileOut.write(match.group(1) + "display:inline" + match.group(3) + match.group(4) + match.group(5))
			else:
				# hide this layer
				fileOut.write (match.group(1) + "display:none" + match.group(3) + match.group(4) + match.group(5))
		else:
			# otherwise just write out the line
			fileOut.write (line)

	fileIn.close ()
	fileOut.close ()

	command = inkscape_location + '/Contents/Resources/script -without-gui -export-area-page --export-width='+ \
	str(detail[2])+' -export-height='+str(detail[3])+' --export-png='+os.getcwd()+'/'+detail[1] + ' ' + os.getcwd() + '/temp_out.svg'
	print (command)
	os.system(command)

for detail in config.config:
	generateFile (detail)
