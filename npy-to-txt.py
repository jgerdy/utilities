#!/usr/local/bin/python
# (C) Jim Gerdy 2012
# jjg@vundle.com
# github.com/jgerdy/utilities
#
############################################################
import gzip,os,re
import numpy as np
from optparse import OptionParser

usage = "USAGE: %prog [FILENAME]" + \
	"\n\tConvert numpy (gzipped) binary file to ASCII txt" + \
	"\n\tconverts .npy.gz file to .txt.gz"
parser = OptionParser(usage=usage)
parser.add_option("-f", "-o", "--force", "--overwrite", dest="overwrite",
        action="store_true",
        help="overwrite")
parser.add_option("-n", "--no-zip", dest="no_zip",
        action="store_true",
        help="product txt (not gzip) file")
parser.add_option("-V", "--verbose", dest="verbose",
        action="store_true",
        help="verbose")
(options, args) = parser.parse_args()
if len(args)==0: exit("usage USAGE: [FILENAME]")
fname = args[0]
verbose   = options.verbose

############################################################
# check for input (txt) file
if not os.path.exists(fname): exit("npy-to-txt: %s not found" % (fname, ))

############################################################
# create new filename
regmatch = re.compile(r'^(.*)(\.npy\.gz)$').search(fname)
if not regmatch: 
	exit("npy-to-txt: wrong filename extensions %s" % (fname,))
fname_root = regmatch.group(1)
newname = fname_root + ".txt.gz"
print "newname", newname

############################################################
# check for overwrite
if newname==fname: exit("txt-to-npy: resulting fname same as original.")
if os.path.exists(newname) and not options.overwrite: 
	exit("%s exists, not overwriting." % (newname))

############################################################
# read (using gzip file and numpy binary parsing)
if re.search( '.gz$', fname ):
	fh_in = gzip.open( fname, 'rb' )
else:
	fh_in = open( fname, 'rb' )
mat = np.load( fh_in )
fh_in.close()

############################################################
# numpy save (gzipped by default, given filename extension)
np.savetxt( newname, mat )

if verbose: print "txt-to-npy wrote %s %s" % (newname, mat.shape)

