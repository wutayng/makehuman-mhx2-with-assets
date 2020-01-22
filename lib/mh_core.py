"""
Author: Warren Taylor
Creation Date: 1/4/19
Functions For Makehuman Data Creation
Python 2
"""

import os
import random
import re

# Lib Directory
lib_directory = (
    "/Users/warrentaylor/Desktop/movement/synthetic-makehuman/makeHumans/lib"
)

import imp

mh_assets = imp.load_source("mh_assets", lib_directory + "/mh_assets.py")
config = imp.load_source("config", lib_directory + "/config.py")

from core import G

human = G.app.selectedHuman


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
    genderChoices = ["male", "female"]
    if gender_Weight < config.gender_low:
        choice = "female"
    elif gender_Weight >= config.gender_low and gender_Weight <= config.gender_high:
        choice = random.choice(genderChoices)
    elif gender_Weight > config.gender_high:
        choice = "male"
    else:
        raise Exception("Random Gender Choice Selection Error")

    return choice


def clothingSectionChoice():
    """
    Find 'full' or 'top and bottom' choice for assets
    :return: selection string 'full' or 'topbottom'
    """
    choice = random.randint(1, 100)
    if choice <= config.clothing_full:
        selection = "full"
    elif choice > config.clothing_full:
        selection = "topbottom"
    else:
        raise Exception("Random Clothing Section Selection Error")

    return selection


def asset_equipChoice(type, genderWeight):
    """
    Return Output Vector If Asset is Equipped - otherwise return 0
    :param type: Type of Asset
    :return: output [name, path, asset_file, type]
    """
    choice = random.randint(1, 100)
    # if type == "Clothes":
    #    if choice > config.withoutClothes:
    #        return addRandomAsset(
    #            "Clothes", config.assetsdir + "/clothes/clothes/", genderWeight
    #        )
    #    else:
    #        return 0
    if type == "Clothes":
        return addRandomAsset(
            "Clothes", config.assetsdir + "/clothes/clothes/", genderWeight
        )
    if type == "Hair" or type == "Beard":
        return addRandomAsset("Hair", config.assetsdir + "/hair/", genderWeight)
    if type == "Eyebrows":
        return addRandomAsset("Eyebrows", config.assetsdir + "/eyebrows/", genderWeight)
    if type == "Glasses":
        return addRandomAsset(
            "Glasses", config.assetsdir + "/clothes/glasses/", genderWeight
        )
    if type == "Hats":
        return addRandomAsset("Hats", config.assetsdir + "/clothes/hats/", genderWeight)
    if type == "Shoes":
        return addRandomAsset(
            "Shoes", config.assetsdir + "/clothes/shoes/", genderWeight
        )
    if type == "Accessories":
        return addRandomAsset(
            "Accessories", config.assetsdir + "/clothes/accessories/", genderWeight
        )
    else:
        raise Exception("asset_equipChoice Error: Bad Asset Type")


def addFile(selection_dir, asset_type):
    """
    Add Either Proxy or Clo File
    :param selection_dir:
    :param asset_type: "Clothes" or "Eyebrows" or "Hair"
    :return: name, path, file, type
    """
    path, name, type = mh_assets.randomAsset(selection_dir)
    if type == "proxy":
        asset_file = mh_assets.addProxyAsset(asset_type, path)
    elif type == "clo":
        asset_file = mh_assets.addCloAsset(asset_type, path)
    else:
        raise Exception("Unknown Asset Type")

    return name, (selection_dir + name), asset_file, type


def setRandomMHWeights():
    """
    Set Makehuman Person Attributes w/ Random Values
    :return:
    """
    # ROUND ALL TO 2 DECIMAL PLACES
    # Gender - 0 to 1 Normal Distribution
    gender = round((random.uniform(0, 1)), 2)
    human.setGender(gender)
    # Breast Size - 0 to 1 Normal Distribution
    human.setBreastSize(round((random.uniform(0, 1)), 2))
    # Age - 0.1 to 1 Normal Distribution
    human.setAge(round((random.uniform(config.age_limit, 1)), 2))
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
    global human
    # Iniitalize ouput
    output = []

    if type == "Clothes":
        clothingSection = clothingSectionChoice()
        gender = genderChoice(gender_Weight)
        likelihood = mh_assets.dir_likeihood()
        if clothingSection == "full":
            selection_dir = dir + "full/" + gender + "/" + likelihood + "/"
            name, path, asset_file, type = addFile(selection_dir, "Clothes")
            output = [name, path, asset_file, type]
            return output
        elif clothingSection == "topbottom":
            selection_dir_top = dir + "top/" + gender + "/" + likelihood + "/"
            name_top, path_top, asset_file_top, type_top = addFile(
                selection_dir_top, "Clothes"
            )
            output = [name_top, path_top, asset_file_top, type_top]
            # if two clothing choices, append output len
            selection_dir_bottom = dir + "bottom/" + gender + "/" + likelihood + "/"
            name_bottom, path_bottom, asset_file_bottom, type_bottom = addFile(
                selection_dir_bottom, "Clothes"
            )
            output.append(name_bottom)
            output.append(path_bottom)
            output.append(asset_file_bottom)
            output.append(type_bottom)
            return output
        else:
            raise Exception("Unknown Clothing Section Selection")

    elif type == "Shoes":
        gender = genderChoice(gender_Weight)
        likelihood = mh_assets.dir_likeihood()
        selection_dir = dir + gender + "/" + likelihood + "/"
        name, path, asset_file, type = addFile(selection_dir, "Clothes")
        output = [name, path, asset_file, type]
        return output

    elif type == "Accessories" or type == "Hats" or type == "Glasses":
        selection_dir = dir
        name, path, asset_file, type = addFile(selection_dir, "Clothes")
        output = [name, path, asset_file, type]
        return output

    elif type == "Eyebrows":
        selection_dir = dir
        name, path, asset_file, type = addFile(selection_dir, "Eyebrows")
        output = [name, path, asset_file, type]
        return output

    elif type == "Hair":
        gender = genderChoice(gender_Weight)
        likelihood = mh_assets.dir_likeihood()
        selection_dir = dir + gender + "/" + likelihood + "/"
        name, path, asset_file, type = addFile(selection_dir, "Hair")
        output = [name, path, asset_file, type]
        return output

    else:
        raise Exception("Unknown Asset Type")


def json_assets(
    clothes_output,
    hair_output,
    eyebrows_output,
    glasses_output,
    hats_output,
    shoes_output,
    accessories_output,
    beard_output,
    i,
):
    texture_data = {}
    texture_data[str(i)] = []
    # Clothes Folder Path + Name
    if len(clothes_output) >= 2:
        texture_data[str(i)].append({"clothes_dir": clothes_output[1]})
        texture_data[str(i)].append({"clothes_name": clothes_output[0]})
    # Clothes-2 Folder Path IF EXISTS
    if len(clothes_output) >= 5:
        texture_data[str(i)].append({"clothes_dir-2": clothes_output[5]})
        texture_data[str(i)].append({"clothes_name-2": clothes_output[4]})
    # Hair Folder Path + Name
    if len(hair_output) >= 2:
        texture_data[str(i)].append({"hair_dir": hair_output[1]})
        texture_data[str(i)].append({"hair_name": hair_output[0]})
    # Eyebrows Folder Path + Name
    if len(eyebrows_output) >= 2:
        texture_data[str(i)].append({"eyebrows_dir": eyebrows_output[1]})
        texture_data[str(i)].append({"eyebrows_name": eyebrows_output[0]})
    # Glasses Folder Path + Name
    if len(glasses_output) >= 2:
        texture_data[str(i)].append({"glasses_dir": glasses_output[1]})
        texture_data[str(i)].append({"glasses_name": glasses_output[0]})
    # Hats Folder Path + Name
    if len(hats_output) >= 2:
        texture_data[str(i)].append({"hats_dir": hats_output[1]})
        texture_data[str(i)].append({"hats_name": hats_output[0]})
    # Shoes Folder Path + Name
    if len(shoes_output) >= 2:
        texture_data[str(i)].append({"shoes_dir": shoes_output[1]})
        texture_data[str(i)].append({"shoes_name": shoes_output[0]})
    # Accessories Folder Path + Name
    if len(accessories_output) >= 2:
        texture_data[str(i)].append({"accessories_dir": accessories_output[1]})
        texture_data[str(i)].append({"accessories_name": accessories_output[0]})
    # Beard Folder Path + Name
    if len(beard_output) >= 2:
        texture_data[str(i)].append({"beard_dir": beard_output[1]})
        texture_data[str(i)].append({"beard_name": beard_output[0]})

    return texture_data


def exportMHX2(i, dir_number, outputdir, visibility):
    """
    Save current human + assets as .mhx2
    :param i: iteration number to save as foldername/filename
    :param dir_number: full directory number passed from main
    :param visibility: Export Error Tracking Log: 0 = off, 1 = on
    :return:
    """
    global human
    # Export file path
    os.mkdir(outputdir + "/" + str(dir_number) + "/" + str(i))
    path = outputdir + "/" + str(dir_number) + "/" + str(i) + "/" + str(i) + ".mhx2"
    dir, name = os.path.split(path)
    name, ext = os.path.splitext(name)
    # Error Track the Export
    print(dir)
    print(name)
    print(ext)
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
    #exporter.export(human, filename)

    outputFilename = name + ext
    G.app.mhapi.exports.exportAsMHX2('testing', useExportsDir=True)
    return
