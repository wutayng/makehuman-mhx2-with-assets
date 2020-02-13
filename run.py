"""
Create Human Assets
Parameters Define the Likelihood for Body Weights and Equipped Assets
"""

# Directory for Clothing Assets
assetsdir = "/home/warren/data/synthetic-training/humans-assets/makeHumanAssets"

# Output Files Directory
outputdir = "/home/warren/data/synthetic-training/humans-assets/makeHumans"

# CMU Skeleton File
cmu_skel_file = (
    "/home/warren/data/synthetic-training/humans-assets/makeHumanAssets/cmu_mb.mhskel"
)

# Number of Humans to Create
num_humans = 20

# Human Create Parameters for Randomization
# Gender: Choose High/Low Threshold for Gender Asset Selection (Scale 0 to 1) - Lower Number = Feminine
# If gender is below or above, asset selection will be male/female - if in range, asset selection will be mixed
gender_low = 0.33
gender_high = 0.66
# Full or Top/Bottom Clothing: Choose between Full Body Clothing or Top/Bottom Configuration. Num = Full Body %
clothing_full = 60
# Age Lower Limit: When Setting Age Parameter, Lowest Age Limit (Scale 0 to 1)
age_limit = 0.1
# Common/Medium/Uncommon Asset Choice: % Of Each Category adding up to 100
assets_common = 60
assets_medium = 30
assets_uncommon = 10

# Percentage of Assets Not added to Human (%)
withoutClothes = 3
withoutHair = 5
withoutBeard = 90
withoutEyebrows = 5
withoutGlasses = 80
withoutHats = 80
withoutShoes = 15
withoutAccessories = 95

import os, re
import time, random, string
from datetime import datetime

start_time = time.time()

from core import G

human = G.app.selectedHuman
api_assets = G.app.mhapi.assets


def extract_number(f):
    """
    Extract Integer Value from filename
    :param f: file
    :return: int
    DUPLICATE FROM ASSETS.PY
        To connect to both run-makehuman and run-textures
    """
    s = re.findall("\d+$", f)
    return (int(s[0]) if s else -1, f)


def genderChoice(gender_Weight):
    """
    Find male/female choice for assets based on Gender Weighting
    :param gender_Weight:
    :return: choice string
    """
    # For Mid Range Gender Weight, Take Random Choice For Male/Female Clothing/Hair
    global gender_low, gender_high
    import random

    genderChoices = ["male", "female"]
    if gender_Weight < gender_low:
        choice = "female"
    elif gender_Weight >= gender_low and gender_Weight <= gender_high:
        choice = random.choice(genderChoices)
    elif gender_Weight > gender_high:
        choice = "male"
    else:
        raise Exception("Random Gender Choice Selection Error")

    return choice


def clothingSectionChoice():
    """
    Find 'full' or 'top and bottom' choice for assets
    :return: selection string 'full' or 'topbottom'
    """
    global clothing_full
    import random

    choice = random.randint(1, 100)
    if choice <= clothing_full:
        selection = "full"
    elif choice > clothing_full:
        selection = "topbottom"
    else:
        raise Exception("Random Clothing Section Selection Error")

    return selection


def asset_equipChoice(type, genderWeight, chance):
    """
    Return Output Vector If Asset is Equipped - otherwise return 0
    :param type: Type of Asset
    :param genderWeight: Gender Weighting of Random Human
    :param chance: from parameters, percentage of human w/o asset e.g. withoutHair, withoutBeard
    :return: output [name, path, asset_file, type]
    """
    import random

    global assetsdir, addRandomAsset
    choice = random.randint(1, 100)
    # Equip Clothing if Random Selection
    if choice > chance:
        if type == "Clothes":
            addRandomAsset("Clothes", assetsdir + "/clothes/clothes/", genderWeight)
        elif type == "Hair" or type == "Beard":
            addRandomAsset("Hair", assetsdir + "/hair/", genderWeight)
        elif type == "Eyebrows":
            addRandomAsset("Eyebrows", assetsdir + "/eyebrows/", genderWeight)
        elif type == "Glasses":
            addRandomAsset("Glasses", assetsdir + "/clothes/glasses/", genderWeight)
        elif type == "Hats":
            addRandomAsset("Hats", assetsdir + "/clothes/hats/", genderWeight)
        elif type == "Shoes":
            addRandomAsset("Shoes", assetsdir + "/clothes/shoes/", genderWeight)
        elif type == "Accessories":
            addRandomAsset(
                "Accessories", assetsdir + "/clothes/accessories/", genderWeight
            )
        else:
            raise Exception("asset_equipChoice Error: Bad Asset Type")
    return


def addFile(selection_dir, asset_type):
    """
    Add Either Proxy or Clo File
    :param selection_dir:
    :param asset_type: "Clothes" or "Eyebrows" or "Hair"
    :return: name, path, file, type
    """
    global randomAsset, addProxyAsset, addCloAsset
    path, typeof = randomAsset(selection_dir)
    if typeof == "proxy":
        addProxyAsset(asset_type, path)
    elif typeof == "clo":
        addCloAsset(asset_type, path)
    else:
        raise Exception("Unknown Asset Type")

    return


def setRandomMHWeights():
    """
    Set Makehuman Person Attributes w/ Random Values
    :return:
    """
    import random

    global age_limit
    # ROUND ALL TO 2 DECIMAL PLACES
    # Gender - 0 to 1 Normal Distribution
    gender = round((random.uniform(0, 1)), 2)
    human.setGender(gender)
    # Breast Size - 0 to 1 Normal Distribution
    human.setBreastSize(round((random.uniform(0, 1)), 2))
    # Age - 0.1 to 1 Normal Distribution
    human.setAge(round((random.uniform(age_limit, 1)), 2))
    # Muscle - 0 to 1 Normal Distribution
    human.setMuscle(round((random.uniform(0, 1)), 2))
    # Weight - 0 to 1 Normal Distribution
    human.setWeight(round((random.uniform(0, 1)), 2))
    # Height - 0 to 1 Normal Distribution
    human.setHeight(round((random.uniform(0, 1)), 2))
    # Proportions - 0 to 1 Normal Distribution
    human.bodyProportions = round((random.uniform(0, 1)), 2)
    # Ethnicity Qualities (3) Sum to 1
    # When One Ethnicity is Set, the other 2 Scale Equally
    # So the setting process must be repeated to approach the asymptote (get closer to true value set)
    african = round(random.random(), 2)
    asian = round(random.random(), 2)
    caucasian = round(random.random(), 2)
    sum = african + asian + caucasian
    # repeat setting of values 3 times to approximate
    for i in range(1, 4):
        # African
        human.setAfrican(african / sum)
        # Asian
        human.setAsian(asian / sum)
        # Caucasian
        human.setCaucasian(caucasian / sum)
    return gender


def addRandomAsset(type, dir, gender_Weight):
    """
    :param type: Type of Asset
        Types = 'Accessories' or 'Clothes' or 'Shoes' or 'Hats' or 'Glasses' or 'Eyebrows' or 'Hair'
    :param dir: Directory of Particular Asset
    :param gender_weight: Gender Weight Value from 0 to 1
    :return:
    """
    global human, addFile, genderChoice, dir_likeihood, clothingSectionChoice
    # Make Random Filepath Choices
    clothingSection = clothingSectionChoice()
    gender = genderChoice(gender_Weight)
    likelihood = dir_likeihood()
    # Iniitalize ouput
    output = []
    if type == "Clothes":
        if clothingSection == "full":
            selection_dir = dir + "full/" + gender + "/" + likelihood + "/"
            addFile(selection_dir, "Clothes")
        elif clothingSection == "topbottom":
            selection_dir_top = dir + "top/" + gender + "/" + likelihood + "/"
            addFile(selection_dir_top, "Clothes")
            # Reselect Randomization for Bottom Clothing Half
            new_gender = genderChoice(gender_Weight)
            new_likelihood = dir_likeihood()
            selection_dir_bottom = (
                dir + "bottom/" + new_gender + "/" + new_likelihood + "/"
            )
            addFile(selection_dir_bottom, "Clothes")
        else:
            raise Exception("Unknown Clothing Section Selection")

    elif type == "Shoes":
        selection_dir = dir + gender + "/" + likelihood + "/"
        addFile(selection_dir, "Clothes")

    elif type == "Accessories" or type == "Hats" or type == "Glasses":
        addFile(dir, "Clothes")

    elif type == "Eyebrows":
        addFile(dir, "Eyebrows")

    elif type == "Hair":
        selection_dir = dir + gender + "/" + likelihood + "/"
        addFile(selection_dir, "Hair")

    return


def dir_likeihood():
    """
    Choose 'common' 'medium' or 'uncommon' subdir to select asset from based on probability
    :return: Random subdir selection
    """
    global assets_common, assets_medium, assets_uncommon
    import random

    # Make Random Selection
    choice = random.randint(1, 100)
    if choice <= assets_common:
        dir_selection = "common"
    elif assets_common < choice <= (assets_common + assets_medium):
        dir_selection = "medium"
    elif choice > (assets_common + assets_medium):
        dir_selection = "uncommon"
    else:
        raise Exception(
            "Random Directory Likelihood Selection Error: choice_num should be >1 & <=100 -- actual value is {}".format(
                choice
            )
        )

    return dir_selection


def randomAsset(directory):
    """
    Random Asset Choice
	:param directory: Directory with Subdirectories to Select From
	:return: pxy Asset Full Path
	:return: pxy Asset Filename
	:return: File Type Avaliable, either 'proxy' or 'clo'
	"""
    import random

    # Make a Random Choice in the directory to get an asset
    namechoice = random.choice(
        [
            dI
            for dI in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, dI))
        ]
    )

    # If Clo File Exists, Use That to Load/Delete Assets
    if os.path.isfile(directory + namechoice + "/" + namechoice + ".mhclo"):
        clopath = directory + namechoice + "/" + namechoice + ".mhclo"
        return clopath, "clo"
    # Else, Use .mhpxy File - If It Exists
    elif os.path.isfile(directory + namechoice + "/" + namechoice + ".mhpxy"):
        pxypath = directory + namechoice + "/" + namechoice + ".mhpxy"
        return pxypath, "proxy"
    else:
        raise Exception(
            "Asset Error: {} does not contain either Proxy or mhclo File".format(
                directory + namechoice
            )
        )


def addProxyAsset(type, pxyfile):
    """
    :param type: Type of Asset
        Types = 'Clothes' or 'Eyebrows' or 'Hair'
    :param pxyfile: Asset Full Path
    :return:
    """
    global human
    import proxy, events3d
    import numpy as np

    pxy = proxy.loadProxy(human, str(pxyfile), type=type)
    mesh, obj = pxy.loadMeshAndObject(human)
    mesh.setPickable(True)
    mesh2 = obj.getSeedMesh()
    fit_to_posed = False
    pxy.update(mesh2, fit_to_posed)
    mesh2.update()
    obj.setSubdivided(human.isSubdivided())
    if type == "Clothes":
        human.addClothesProxy(pxy)
    elif type == "Eyebrows":
        human.setEyebrowsProxy(pxy)
    elif type == "Hair":
        human.setHairProxy(pxy)
    else:
        raise Exception("Unknown Asset Type")

    vertsMask = np.ones(human.meshData.getVertexCount(), dtype=bool)
    proxyVertMask = proxy.transferVertexMaskToProxy(vertsMask, pxy)
    # Apply accumulated mask from previous clothes layers on this clothing piece
    obj.changeVertexMask(proxyVertMask)
    # Modify accumulated (basemesh) verts mask
    verts = np.argwhere(pxy.deleteVerts)[..., 0]
    vertsMask[verts] = False
    human.changeVertexMask(vertsMask)
    event = events3d.HumanEvent(human, "proxy")
    event.pxy = "clothes"
    human.callEvent("onChanged", event)
    return


def addCloAsset(type, clofile):
    """
    :param type: Type of Asset
        Types = 'Clothes' or 'Eyebrows' or 'Hair'
    :param clofile: Asset Full Path
    :return:
    """
    global human
    global api_assets
    if type == "Clothes" or type == "Hair":
        api_assets.equipClothes(clofile)
    elif type == "Eyebrows":
        api_assets.equipEyebrows(clofile)
    else:
        raise Exception("Unknown Asset Type")
    return


def exportMHX2(path):
    """
    Save current human + assets as .mhx2
    :param path: full path to output ending in .mhx2
    :return:
    """
    global human
    # Export file path
    dir, name = os.path.split(path)
    name, ext = os.path.splitext(name)
    # Can't just pass an exporter a path, must give it a validation function
    def filename(targetExt, different=False):
        """
        For exporter
        :param targetExt:
        :param different:
        :return:
        """
        if targetExt.lower() != "mhx2":
            log.warning("expected extension '.%s' but got '%s'", targetExt, "mhx2")
        return os.path.join(dir, name + "." + targetExt)

    # Set Export Directory
    G.app.setSetting("exportdir", dir)

    # Getting exporter and exporting mhx2
    exporter = (
        G.app.getCategory("Files")
        .getTaskByName("Export")
        .getExporter("MakeHuman Exchange (mhx2)")
    )
    exporter.export(human, filename)
    return


def resetAll():
    """
    Resets Human With Base CMU Skeleton
    :return:
    """
    import skeleton

    global cmu_skel_file
    # Reset Human
    G.app._resetHuman()
    # Set Skeleton
    cmu_skel = skeleton.load(cmu_skel_file, human.meshData)
    G.app.selectedHuman.setSkeleton(cmu_skel)
    return


# Start Creating Makehumans
resetAll()
current_date = datetime.now()
suffix = "".join(random.choices(string.ascii_letters + string.digits, k=4))
folder_date = (
    str(current_date.month)
    + "-"
    + str(current_date.day)
    + "-"
    + str(current_date.year)
    + "-"
    + suffix
)
os.mkdir(outputdir + "/" + str(folder_date))

# Create ReadMe
readme_filename = outputdir + "/readme_parameters.md"
if os.path.exists(readme_filename):
    append_write = "a"
else:
    append_write = "w"
readme = open(readme_filename, append_write)
readme.write("Folder No: {} \n".format(folder_date))
readme.write("Number of Humans: {} \n".format(num_humans))
readme.write(
    "Gender Lower Limit {}, Higher Limit {} \n".format(gender_low, gender_high)
)
readme.write(
    "Percentage of Humans will Full (vs Top/Bottom) Clothes: {} \n".format(
        clothing_full
    )
)
readme.write("Lower Age Limit: {} \n".format(age_limit))
readme.write(
    "Percentage of Common/Medium/Uncommon Assets: {} - {} - {} \n".format(
        assets_common, assets_medium, assets_uncommon
    )
)
readme.write(
    "Percentage without: Clothes {} - Hair {} - Beard {} - Eyebrows {} - Glasses {} - Hats {} - Shoes {} - Accessories {} \n".format(
        withoutClothes,
        withoutHair,
        withoutBeard,
        withoutEyebrows,
        withoutGlasses,
        withoutHats,
        withoutShoes,
        withoutAccessories,
    )
)
readme.write(" \n")
readme.close()

# Create Humans
for iter_num in range(num_humans):

    genderWeight = setRandomMHWeights()
    # Choose/Add Random Clothing Asset
    asset_equipChoice("Clothes", genderWeight, withoutClothes)
    # Choose/Add Random Hair Asset
    asset_equipChoice("Hair", genderWeight, withoutHair)
    # Choose/Add Random Eyebrows Asset
    asset_equipChoice("Eyebrows", genderWeight, withoutEyebrows)
    # Choose/Add Random Glasses Asset
    asset_equipChoice("Glasses", genderWeight, withoutGlasses)
    # Choose/Add Random Hats Asset
    asset_equipChoice("Hats", genderWeight, withoutHats)
    # Choose/Add Random Shoes Asset
    asset_equipChoice("Shoes", genderWeight, withoutShoes)
    # Choose/Add Random Accessories Asset
    asset_equipChoice("Accessories", genderWeight, withoutAccessories)
    # Choose/Add Random Beard Asset
    asset_equipChoice("Beard", genderWeight, withoutBeard)

    # Export MHX2 with Random 12dig Filename
    namestr = "".join(random.choices(string.ascii_letters + string.digits, k=12))
    os.mkdir(outputdir + "/" + str(folder_date) + "/" + namestr)
    exportMHX2(
        outputdir + "/" + str(folder_date) + "/" + namestr + "/" + namestr + ".mhx2"
    )

    # Delete All Clothes
    resetAll()

    # Print Time
    print(
        "{} of {} Humans Completed - Runtime {} Minutes".format(
            iter_num, num_humans, round((time.time() - start_time) / 60, 2)
        )
    )

    iter_num += 1

print("Total ElapsedTime {} Minutes".format(round((time.time() - start_time) / 60, 2)))
