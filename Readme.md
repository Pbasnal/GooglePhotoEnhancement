This repo uses the ML Model from the github repo (https://github.com/aiff22/DPED)

## To Run
There are 2 files that can be used
1. enhacegphotos.py - This script connects to Google Photos and iterates over the first 5 photos to edit them. Future work will add support for resuming where it left editing and cover the whole photos library.
2. loadnef.py - This script loads the image file kept in DPED/dped/iphone/test_data/full_size_test_images/ and performs enhancement on it. It then saves the enhanced photo in DPED/visual_results folder.
    
    * Command to use it 
    > python loadnef.py model=iphone_orig test_subset=full

## Sample results
![Sample image after editing](SampleResults.jpg)