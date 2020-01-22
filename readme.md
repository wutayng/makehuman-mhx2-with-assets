## To Create Random Humans (.mhx2)
### Using MakeHuman 1.1.1 Packaged Application
### File Creation

#### Creates: 1000 .mhx2 files and 'textures' folders

#### ~= 200 GB

### Output Directory Structure
    > files      
        > 1,2,3...n
            > __textures.json
            > i (from 1 to 1000)
                    > i.mhx2
                    > textures

## Instructions

### Steps to Create Makehumans
#### 1000 MakeHumans (.mhx2 + 'textures') will be created in 'outputdir/i/'
#### • 'i' will be lowest integer that does not exist in output folder.
#### • run-textures will change textures of output folder i (largest int i)
1. Download MakeHuman 1.1.1
2. Edit config.py assetsdir/outputdir to directory location of 'makeHumanAssets' (asset data) 'makeHumans' (output)
3. Edit lib directory in 'run.py', 'mh_core', 'mh_assets', and 'tests/test_assets.py'
4. Start MakeHuman 1.1.1 Using a Terminal Alias for Output Visibility
5. In Settings/Plugins, make sure 9_export_mhx2, 7_scripting, and 1_MHAPI are enabled
6. Set Pose/Animate Skeleton to 'Cmu mb'
7. Load run.py in Utilities/Scripting
8. Utilities/Execute

## Assets
### Custom Asset Directory Structure  
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
            
### Each asset named dir(examplename)
Must contain   
• examplename.obj or examplename.mhpxy (asset main file)
• examplename_diffuse.png (texture)

### To Test Assets
#### Run tests/test.py
- This script will load each asset, export .mhx2, and delete asset from human to check that each asset functions properly
- Run this script in MakeHuman Script/Execute

Attributions:
...