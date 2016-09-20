"""
Measures features of the PSFs, 
individually for each subfield.
"""
import multiprocessing
import datetime
import numpy as np
import astropy.table

import megalut.tools as tools
import megalut.meas as meas

import megalutgreat3 as mg3

import config
import measfcts

import logging
logging.basicConfig(format=config.loggerformat, level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Loading the run
great3 = config.load_run()


for subfield in config.subfields:


	# We don't bother reading the starcat, and just make one
	stars = []
	for i in range(3):
		for j in range(3):
			stars.append( [0.5 + great3.stampsize()/2.0 + i*great3.stampsize(), 0.5 + great3.stampsize()/2.0 + j*great3.stampsize()] )
	stars = np.array(stars)
	
	starcat = astropy.table.Table([stars[:,0], stars[:,1]], names=('psfx', 'psfy'))
	#print starcat
	
	# We add the subfield number to the catalog, might be handy later.
	starcat["psfsubfield"] = subfield
	
	
	# To measure the stars, we attach the image:
	starcat.meta["img"] = tools.imageinfo.ImageInfo(
		filepath=great3.starimgfilepath(subfield),
		xname="psfx",
		yname="psfy",
		stampsize=great3.stampsize(),
		workdir=great3.path("obs", "star_%i_measworkdir" % subfield)
		)

	starcat = measfcts.psf(starcat, branch=great3)
	#print starcat[["psfx", "psfy", "psf_sewpy_XWIN_IMAGE", "psf_sewpy_YWIN_IMAGE", "psf_adamom_x", "psf_adamom_y"]]
	#print starcat

	tools.io.writepickle(starcat, great3.path("obs", "star_%i_meascat.pkl" % subfield))
	

