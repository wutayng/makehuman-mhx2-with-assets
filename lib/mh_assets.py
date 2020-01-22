"""
Author: Warren Taylor
Creation Date: 1/9/19
Functions For Makehuman Data Creation
Python 2
"""

import os
import random
import numpy as np

# makeHuman imports
import proxy
import events3d

# Lib Directory
lib_directory = (
    "/Users/warrentaylor/Desktop/movement/synthetic-makehuman/makehumans/lib"
)

import imp

config = imp.load_source("config", lib_directory + "/config.py")

from core import G

human = G.app.selectedHuman
api_assets = G.app.mhapi.assets


def dir_likeihood():
    """
    Choose 'common' 'medium' or 'uncommon' subdir to select asset from based on probability
    :return: Random subdir selection
    """
    # Make Random Selection
    choice = random.randint(1, 100)
    if choice <= config.assets_common:
        dir_selection = "common"
    elif config.assets_common < choice <= (config.assets_common + config.assets_medium):
        dir_selection = "medium"
    elif choice > (config.assets_common + config.assets_medium):
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
    # Make a Random Choice in the directory to get an asset
    namechoice = random.choice(
        [
            dI
            for dI in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, dI))
        ]
    )
    # If Proxy File Exists, Use That to Load/Delete Assets
    if os.path.isfile(directory + namechoice + "/" + namechoice + ".mhpxy"):
        pxypath = directory + namechoice + "/" + namechoice + ".mhpxy"
        return pxypath, namechoice, "proxy"

    # Else, Use .mhclo File - If It Exists
    elif os.path.isfile(directory + namechoice + "/" + namechoice + ".mhclo"):
        clopath = directory + namechoice + "/" + namechoice + ".mhclo"
        return clopath, namechoice, "clo"
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
    pxy = proxy.loadProxy(human, unicode(pxyfile, "utf-8"), type=type)
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
    return pxy


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
        print(clofile)
        api_assets.equipClothes(clofile)
    elif type == "Eyebrows":
        api_assets.equipEyebrows(clofile)
    else:
        raise Exception("Unknown Asset Type")

    return clofile


def deleteAllAssets(clothes_output,hats_output,shoes_output,hair_output):
    """
    Deletes All Assets Currently on Human
    Takes as Input Several Output Factors from Assets to Decide What to Eliminate
    :param clothes_output:
    :param hats_output:
    :param shoes_output:
    :param hair_output:
    :return:
    """
    global human
    # Delete Clothes (Either 'Full' or if exists: 'Top' and 'Bottom')
    if clothes_output != 0: # To Account for No Clothes Equipped
        if clothes_output[3] == "proxy":
            human.removeClothesProxy(clothes_output[2].uuid)
        if len(clothes_output) >= 5:
            if clothes_output[7] == "proxy":
                human.removeClothesProxy(clothes_output[6].uuid)

    # Delete Hat if Proxy
    if hats_output != 0:  # To Account for No Hats Equipped
        if hats_output[3] == "proxy":
            human.removeClothesProxy(hats_output[2].uuid)

    # Delete Shoes if Proxy
    if shoes_output != 0:  # To Account for No Shoes Equipped
        if shoes_output[3] == "proxy":
            human.removeClothesProxy(shoes_output[2].uuid)

    # Delete Hair by Filename if .mhclo
    if hair_output != 0:  # To Account for No Hair Equipped
        human.setHairProxy(0)
        if hair_output[3] == "clo":
            G.app.mhapi.assets.unequipClothes(hair_output[2])

    # Delete Eyebrows
    human.setEyebrowsProxy(0)

    # Delete ALL ELSE (Clothes)
    G.app.mhapi.assets.unequipAllClothes()

    return
