#!/usr/local/bin/python
# (c) Jim Gerdy 2012
# jjg@vundle.com
# github.com/jgerdy/utilities
############################################################
import gzip,os,re
import numpy as np
from optparse import OptionParser

usage = "USAGE: %prog [FILENAME]" + \
	"\n\tconverts .txt.gz file to .npy.gz"
parser = OptionParser(usage=usage)
parser.add_option("-c", "--csv",
	dest="csv",
        action="store_true",
        help="csv")
parser.add_option("-f", "-o", "--force", "--overwrite", dest="overwrite",
        action="store_true",
        help="overwrite")
parser.add_option("-v", "--verbose", dest="verbose",
        action="store_true",
        help="verbose")
parser.add_option("-n", "--no-zip", 
	dest="no_zip",
        action="store_true",
        help="write npy (no gz) file")
(options, args) = parser.parse_args()
if len(args)==0: exit("usage USAGE: [FILENAME]")
fname = args[0]
verbose   = options.verbose

############################################################
# check for input (txt) file
i os.path.exists(fname): exit("txt-to-npy: %s not found" % (fname, ))

############################################################
# create new filename
regmatch = re.compile(r'^(.*)(\.txt(\.gz|))$').search(fname)
if not regmatch: 
	exit("txt-to-npy: wrong filename extensions %s" % (fname,))
fname_root = regmatch.group(1)
newname = fname_root + ".npy"

############################################################
# check for overwrite
if newname==fname: exit("txt-to-npy: resulting fname same as original.")
if os.path.exists(newname) and not options.overwrite: 
	exit("%s exists, not overwriting." % (newname))

############################################################
# read file
if options.csv:
	mat = np.loadtxt( fname, delimiter=',' )
else:
	mat = np.loadtxt( fname )

############################################################
# write npy
if options.no_zip:
	fh_out = open( newname, 'wb' )
	np.save(fh_out, mat)
	fh_out.close()
else:
	newname = newname + ".gz"
	fh_out = gzip.open( newname, 'wb' )
	np.save(fh_out, mat)
	fh_out.close()
if verbose: print "txt-to-npy wrote %s %s" % (newname, mat.shape)

