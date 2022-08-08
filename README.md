Configuration Structure:
    myPipeline
    | - build
    | - myPipeline
    | | - __init__.py
    | | - quality_check.py
    | | - utility.py
    | - myPipeline.egg-info
    | - readme.txt
    | - setup.py

Install Command: 
    If current location is at the parent directory myPipeline, use:
        "pip install myPipeline" 
    else:
        "pip install absolutePathToMyPipeline/myPipeline"