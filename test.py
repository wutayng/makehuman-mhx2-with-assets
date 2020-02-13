"""
To Test Complete Functionality of All Assets
Load Each Asset in Asset Directory
Export Human and Delete Asset
"""

# Directory for Clothing Assets
assetsdir = "/home/warren/data/synthetic-training/humans-assets/makeHumanAssets"

# Output Files Directory
outputdir = "/home/warren/data/synthetic-training/humans-assets/makeHumans"

# CMU Skeleton File
cmu_skel_file = (
    "/home/warren/data/synthetic-training/humans-assets/makeHumanAssets/cmu_mb.mhskel"
)

import os
import shutil
from core import G

human = G.app.selectedHuman
api_assets = G.app.mhapi.assets


def testAssets(dirs, asset_type, output_dir):
    """
    :param dirs: Directories of Asset
    :param type: Type of Asset
         Types = 'Clothes' or 'Eyebrows' or 'Hair'
    :param output_dir: Directory for Output File
    """
    global addProxyAsset, addCloAsset, exportMHX2, deleteAllAssets, resetAll
    global cmu_skel_file, human
    iter_num = 0
    for directory in dirs:
        list = os.listdir(directory)
        for elem in list:
            print(directory + elem)
            if os.path.isfile(directory + elem + "/" + elem + ".mhpxy"):
                pxy = addProxyAsset(
                    asset_type, (directory + elem + "/" + elem + ".mhpxy")
                )
                print("Asset .mhpxy Added Successfully")
                os.mkdir(output_dir + str(iter_num))
                exportMHX2(output_dir + str(iter_num) + "/testout.mhx2")
                print("Human Exported Successfully")
                resetAll()
            elif os.path.isfile(directory + elem + "/" + elem + ".mhclo"):
                clo = addCloAsset(
                    asset_type, (directory + elem + "/" + elem + ".mhclo")
                )
                print("Asset .mhclo Added Successfully")
                os.mkdir(output_dir + str(iter_num))
                exportMHX2(output_dir + str(iter_num) + "/testout.mhx2")
                print("Human Exported Successfully")
                resetAll()
            iter_num += 1
    return


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
        api_assets.equipClothes(clofile)
    elif type == "Eyebrows":
        api_assets.equipEyebrows(clofile)
    else:
        raise Exception("Unknown Asset Type")

    return clofile


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


# Create Top Level Assets Dirs
top_level_dirs = {
    "eyebrows": assetsdir + "/eyebrows/",
    "clothes": assetsdir + "/clothes/clothes/",
    "hair": assetsdir + "/hair/",
    "shoes": assetsdir + "/clothes/shoes/",
    "hats": assetsdir + "/clothes/hats/",
    "glasses": assetsdir + "/clothes/glasses/",
    "accessories": assetsdir + "/clothes/accessories/",
}

# Create Subdirs
clothing_dirs = ["top/", "bottom/", "full/"]
gender_dirs = ["male/", "female/"]
likelihood_dirs = ["common/", "uncommon/", "medium/"]

# List All Dirs Containing Assets
# Eyebrows
eyebrows = [top_level_dirs["eyebrows"]]
# Hats
hats = [top_level_dirs["hats"]]
# Glasses
glasses = [top_level_dirs["glasses"]]
# Accessories
accessories = [top_level_dirs["accessories"]]
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

try:
    shutil.rmtree(outputdir + "/testing")
except:
    pass
os.mkdir(outputdir + "/testing")
resetAll()

os.mkdir(outputdir + "/testing/hats")
testAssets(hats, "Clothes", outputdir + "/testing/hats/")
print("----- Hats Tested Successfully -----")

os.mkdir(outputdir + "/testing/eyebrows")
testAssets(eyebrows, "Eyebrows", outputdir + "/testing/eyebrows/")
print("----- Eyebrows Tested Successfully -----")

os.mkdir(outputdir + "/testing/hair")
testAssets(hair, "Hair", outputdir + "/testing/hair/")
print("----- Hair Tested Successfully -----")

os.mkdir(outputdir + "/testing/accessories")
testAssets(accessories, "Clothes", outputdir + "/testing/accessories/")
print("----- Accessories Tested Successfully -----")

os.mkdir(outputdir + "/testing/shoes")
testAssets(shoes, "Clothes", outputdir + "/testing/shoes/")
print("----- Shoes Tested Successfully -----")

os.mkdir(outputdir + "/testing/clothes")
testAssets(clothes, "Clothes", outputdir + "/testing/clothes/")
print("----- Clothes Tested Successfully -----")

print("----- All Assets Tested Successfully -----")
shutil.rmtree(outputdir + "/testing")
