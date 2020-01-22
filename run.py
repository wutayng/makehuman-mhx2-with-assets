"""
Author: Warren Taylor
Creation Date: 1/5/19
Script to Generate Makehuman .mhx2 Models w/Assets
Python 2
"""

# Lib Directory
lib_directory = (
    "/Users/warrentaylor/Desktop/movement/synthetic-makehuman/makehumans/lib"
)

# Time Iterations (Print to Exec Terminal)
import time

start_time = time.time()

# Initialize Texture Names json
import json

texture_data = {}

# Import Lib
import imp

mh_assets = imp.load_source("mh_assets", (lib_directory + "/mh_assets.py"))
mh_core = imp.load_source("mh_core", (lib_directory + "/mh_core.py"))
config = imp.load_source("config", (lib_directory + "/config.py"))

# Create Output Directory i+1 (After existing directory i)
dir_list = os.listdir(config.outputdir)
# If no Existing Directories
if dir_list == [".DS_Store"]:
    dir_number = 1
else:
    dir_number = int(max(dir_list, key=mh_core.extract_number)) + 1
# Create New Directory To Store MakeHumans
os.mkdir(config.outputdir + "/" + str(dir_number))

from core import G

human = G.app.selectedHuman

# Loop to run 1000 MakeHuman Iterations
print("<--------------- STARTING MAKEHUMAN CREATION --------------->")
for i in range(1, 2):
    # Initialize json texture
    texture_data[str(i)] = []

    # Set Human Slider Weights to Random Distribution
    genderWeight = mh_core.setRandomMHWeights()

    # Choose/Add Random Clothing Asset
    clothes_output = mh_core.asset_equipChoice("Clothes", genderWeight)
    # Choose/Add Random Hair Asset
    hair_output = mh_core.asset_equipChoice("Hair", genderWeight)
    # Choose/Add Random Eyebrows Asset
    eyebrows_output = mh_core.asset_equipChoice("Eyebrows", genderWeight)
    # Choose/Add Random Glasses Asset
    glasses_output = mh_core.asset_equipChoice("Glasses", genderWeight)
    # Choose/Add Random Hats Asset
    hats_output = mh_core.asset_equipChoice("Hats", genderWeight)
    # Choose/Add Random Shoes Asset
    shoes_output = mh_core.asset_equipChoice("Shoes", genderWeight)
    # Choose/Add Random Accessories Asset
    accessories_output = mh_core.asset_equipChoice("Accessories", genderWeight)
    # Choose/Add Random Beard Asset
    beard_output = mh_core.asset_equipChoice("Beard", genderWeight)

    # Save .mhx2 Human w/Assets
    mh_core.exportMHX2(i, dir_number, config.outputdir, 0)

    # Delete Current Assets
    mh_assets.deleteAllAssets(clothes_output, hats_output, shoes_output, hair_output)

    # Write Asset Names to json for Texture Modification
    texture_data[str(i)] = mh_core.json_assets(
        clothes_output,
        hair_output,
        eyebrows_output,
        glasses_output,
        hats_output,
        shoes_output,
        accessories_output,
        beard_output,
        i,
    )

    # Write to json file in outputdir
    with open(
        config.outputdir + "/" + str(dir_number) + "/__textures.json", "w"
    ) as outfile:
        json.dump(texture_data[str(i)], outfile)

    # Print Output Time Progress
    print(str(i) + " Iterations Complete")
    print(
        str(round(((int(time.time()) - start_time) / 60), 2)) + " Minutes Taken So Far"
    )
    print("...")

# Print Successful Complete
print("--- FINISH SUCCESSFUL ---")
print(str(round(((int(time.time()) - start_time) / 60), 2)) + " Minutes Taken")
