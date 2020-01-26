## Creating Random Humans (.mhx2 + Textures)
#### Using MakeHuman 1.2 Cloned Repository @ commit=c00a530 1/18/2020
##### Application /makehuman-master is OFFICIAL and UNMODIFIED  
##### Additions: several /data files as found in packaged application, community plugins
##### Output From Scripts therefore subject to CC0 (No Rights Reserved)
<hr>

## Instructions

Clone Repo and Create Python3.6 venv
```
python3 -m venv /path/to/repo/venv
source venv/bin/activate
``` 
Install Requirements
```
pip install -r requirements.txt
```
#### To Test Asset Loading and Exports
Edit test.py assetsdir, outputdir, and cmu_skel_file to full paths
```
python ./makehuman-master/makehuman/makehuman.py
```
Navigate to Utilities/Scripting Tab and Load test.py  

Execute Script

The test.py script will load and export all assets to make sure they function correctly.  
If the script fails, look for the latest path to an asset in the terminal output. This asset was not able to load and export correctly.

#### To Output Random Makehumans
Edit run.py assetsdir, outputdir, and cmu_skel_file to full paths  

Edit any desired parameter changes in run.py
```
python ./makehuman-master/makehuman/makehuman.py
```
Navigate to Utilities/Scripting Tab and Load run.py  

Execute Script

This script will create a dated directory in 'outputdir'
Directory will include 'num_humans' folders containing full makeHumans (.mhx2 + textures)

## Asset Directory
### makeHumanAssets Dir Must Have the Following Structure
    > makeHumanAssets  
        > hair  
            > male
                 > common
                 > medium
                 > uncommon
                 > beards
            > female
                 > common
                 > medium
                 > uncommon
        > eyebrows  
        > clothes
            > accessories  
            > clothes
                > top
                    > male
                        > common
                        > medium
                        > uncommon
                    > female
                        > common
                        > medium
                        > uncommon
                > bottom
                    > male
                        > common
                        > medium
                        > uncommon
                    > female
                        > common
                        > medium
                        > uncommon
                > full  
                    > male
                        > common
                        > medium
                        > uncommon
                    > female
                        > common
                        > medium
                        > uncommon
            > glasses
            > hats  
            > shoes
                > male
                    > common
                    > medium
                    > uncommon
                > female
                    > common
                    > medium
                    > uncommon
            
### For each Asset Named ''examplename'
Folder 'examplename' must contain  
• examplename.obj or examplename.mhpxy (asset main file)  
• examplename_diffuse.png (texture)


## Attributions:  
#### MakeHuman Software  
The MakeHuman Community  
[License](./makehuman-master/LICENSE.md)  
[Github](https://github.com/makehumancommunity/makehuman)

#### Makehuman Assets
[Assets Page](http://www.makehumancommunity.org/content/user_contributed_assets.html)  
All Assets Used are either CC0 or CC-BY 4.0

