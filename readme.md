## Creating Random Humans (.mhx2 + Textures)
##### Makehuman Application is OFFICIAL and UNMODIFIED  
##### Output From Scripts therefore subject to CC0 (No Rights Reserved)
<hr>

## Instructions
####Install Makehuman
Download Plugins - 1_mhapi and 9_export_mhx2  
Copy into Plugins Folder and Enable Plugins via Makehuman GUI
#### To Test Asset Loading and Exports
1. Edit test.py assetsdir, outputdir, and cmu_skel_file to full paths  
2. Start MakeHuman
3. Navigate to Utilities/Scripting Tab and Load test.py  
4. Execute Script

The test.py script will load and export all assets to make sure they function correctly.  
If the script fails, look for the latest path to an asset in the terminal output. This asset was not able to load and export correctly.

#### To Output Random Makehumans
1. Edit run.py assetsdir, outputdir, and cmu_skel_file to full paths  
2. Edit any desired parameter changes in run.py
3. Start MakeHuman
4. Navigate to Utilities/Scripting Tab and Load run.py  
5. Execute Script

This script will create a dated directory in 'outputdir'  
Directory will include 'run.py var: num_humans' folders containing full makeHumans (.mhx2 + textures)

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
• examplename.obj or examplename.mhpxy  
• examplename_diffuse.png (texture)


## Attributions:  
#### MakeHuman Software  
The MakeHuman Community  
[License](./makehuman-master/LICENSE.md)  
[Github](https://github.com/makehumancommunity/makehuman)

#### Makehuman Assets
[Assets Page](http://www.makehumancommunity.org/content/user_contributed_assets.html)  
All Assets Used are either CC0 or CC-BY 4.0

