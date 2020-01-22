"""
Author: Warren Taylor
Creation Date: 1/11/19
Functions for Testing Script
Python 2
"""

# Lib Directory
lib_directory = (
    "/Users/warrentaylor/Desktop/movement/synthetic-makehuman/makehumans/lib"
)

import os
import shutil
from core import G

human = G.app.selectedHuman

# Import Lib
import imp

mh_assets = imp.load_source("mh_assets", (lib_directory + "/mh_assets.py"))
mh_core = imp.load_source("mh_core", (lib_directory + "/mh_core.py"))
config = imp.load_source("config", (lib_directory + "/config.py"))

output = config.outputdir + "/testing"


def deleteAsset(type, file):
    global human
    if type == "Clothes":
        if type == "proxy":
            human.removeClothesProxy(file.uuid)

    # Delete Eyebrows
    human.setEyebrowsProxy(0)
    # Delete Hair
    human.setHairProxy(0)
    # Delete ALL ELSE (Clothes)
    G.app.mhapi.assets.unequipAllClothes()
    return


def equip_save_and_delete(dir, elem, asset_type, output_num, output):
    print("Asset: {}".format(dir + elem))
    if os.path.isfile(dir + elem + "/" + elem + ".mhpxy"):
        pxy = mh_assets.addProxyAsset(asset_type, (dir + elem + "/" + elem + ".mhpxy"))
        print('Asset .mhpxy Added Successfully')
        mh_core.exportMHX2(output_num, 1, output, 1)
        print('Human Exported Successfully')
        deleteAsset(asset_type, pxy)
    elif os.path.isfile(dir + elem + "/" + elem + ".mhclo"):
        clo = mh_assets.addCloAsset(asset_type, (dir + elem + "/" + elem + ".mhclo"))
        print('Asset .mhclo Added Successfully')
        mh_core.exportMHX2(output_num, 1, output, 1)
        print('Human Exported Successfully')
        deleteAsset(asset_type, clo)
    else:
        raise Exception(
            "No .mhpxy or .mhclo for {}".format(
                asset_dirs + elem + "/" + elem + ".mhpxy"
            )
        )
    return

def checkEmpty():
    """
    Ensure that Human Does not Have any Assets Equipped
    :return:
    """
    if G.app.mhapi.assets.getEquippedClothes() == []:
        pass
    else:
        raise Exception("Clothes not Fully Uneqipped")
    # Check That No Eyebrows on are on Human
    if not G.app.mhapi.assets.getEquippedEyebrows():
       pass
    else:
        raise Exception('Eyebrows not Fully Uneqipped')
    # Check That No Hair is on Human
    if not G.app.mhapi.assets.getEquippedHair():
        pass
    else:
        raise Exception("Hair not Fully Uneqipped")
    return


def testAssets(asset_dirs, asset_type):
    """
    Equip, Export .mhx2, and Unequip Each Asset to Test
    :param asset_dirs: List of Asset Dirs
    :param type: Type of Assets in Dir (For Equipping Purposes)
    :return:
    """
    output_num = 1
    global output
    global mh_core
    global mh_assets
    global deleteAsset
    print(asset_dirs)
    if type(asset_dirs) is not "list":
        list = os.listdir(asset_dirs)
        for elem in list:
            equip_save_and_delete(asset_dirs, elem, asset_type, output_num, output)
            shutil.rmtree(output + '/1/' + str(output_num))
    else:
        raise Exception("Unavaliable Asset Directory for {}".format(asset_dirs))

    # Check That No Clothes on are on Human
    checkEmpty()

    return