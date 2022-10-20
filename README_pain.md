**Python version of 3.11 is needed for this code**

In case you didn't look in requirements.txt, these are the modules you will need for the code:
# for google
pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib
import google
# for bs4
pip install beautifulsoup4
import bs4
# for Bio
pip install biopython
import Bio
# about importing MatrixInfo as matlist from Bio.SubsMat:
# Bio.SubsMat has been deprecated, and we intend to remove it in a future release of Biopython. 
# As an alternative, please consider using Bio.Align.substitution_matrices as a replacement, 
# and contact the Biopython developers if you still need the Bio.SubsMat module."
# for aiohttp
pip install aiohttp
import pip aiohttp
# for pandas you need version higher than 1.5
pip install pandas
import pandas
# for cv2
pip install opencv-python
import cv2
# for lxml
pip install lxml

**Or you can just do this**
pip install -r myproject/requirements.txt

_To be honest I didn't succeed in executing the whole code, only some parts of it, but the last line will definitely cheer anyone up!_
