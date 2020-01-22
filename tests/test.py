"""
Author: Warren Taylor
Creation Date: 1/11/19
Script to Test All Makehuman Assets Before Using for Creation
Python 2
"""

# Lib Directory
lib_directory = (
    "/Users/warrentaylor/Desktop/movement/synthetic-makehuman/makehumans/lib"
)

import os
from core import G
import shutil

human = G.app.selectedHuman

# Import Lib
import imp

mh_assets = imp.load_source("mh_assets", (lib_directory + "/mh_assets.py"))
mh_core = imp.load_source("mh_core", (lib_directory + "/mh_core.py"))
config = imp.load_source("config", (lib_directory + "/config.py"))
test_functions = imp.load_source("test_functions", (lib_directory[:-4] + "/tests/test_functions.py"))

# Make Test Output Directory
output = config.outputdir + "/testing"
try:
    os.mkdir(output)
except:
    pass
try:
    os.mkdir(output + "/1")
except:
    pass

# Create Top Level Assets Dirs
top_level_dirs = {
    "eyebrows": config.assetsdir + "/eyebrows/",
    "clothes": config.assetsdir + "/clothes/clothes/",
    "hair": config.assetsdir + "/hair/",
    "shoes": config.assetsdir + "/clothes/shoes/",
    "hats": config.assetsdir + "/clothes/hats/",
    "glasses": config.assetsdir + "/clothes/glasses/",
    "accessories": config.assetsdir + "/clothes/accessories/",
}

# Create Subdirs
clothing_dirs = ["top/", "bottom/", "full/"]
gender_dirs = ["male/", "female/"]
likelihood_dirs = ["common/", "uncommon/", "medium/"]

# List All Dirs Containing Assets
# Eyebrows
eyebrows = top_level_dirs["eyebrows"]
# Hats
hats = top_level_dirs["hats"]
# Glasses
glasses = top_level_dirs["glasses"]
# Accessories
accessories = top_level_dirs["accessories"]
# Hair
hair = []
for gender in gender_dirs:
    for likelihood in likelihood_dirs:
        hair.append(top_level_dirs["hair"] + gender + likelihood)
hair.append(top_level_dirs["hair"] + "male/beards/")
# Shoes
shoes = []
for gender in gender_dirs:
    for likelihood in likelihood_dirs:
        shoes.append(top_level_dirs["shoes"] + gender + likelihood)
# Clothes
clothes = []
for sections in clothing_dirs:
    for gender in gender_dirs:
        for likelihood in likelihood_dirs:
            clothes.append(top_level_dirs["clothes"] + sections + gender + likelihood)


test_functions.testAssets(eyebrows,"Eyebrows")
print("----- Eyebrows Tested Successfully -----")
#for dir in hair:
#    print(dir)
#    test_functions.testAssets(dir,"Hair")
#print("----- Hair Tested Successfully -----")

# Delete Testing Directory
shutil.rmtree(output)