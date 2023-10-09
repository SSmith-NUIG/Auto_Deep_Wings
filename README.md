# Auto_Deep_Wings
Deep wings is a software which assigns a honey bee lineage result to images of honey bee wings  
It can be found at this website as of 2023_10_09 https://deepwings.ddns.net/  
  
This repository contains scripts made to assist in using this software on a large scale.   
When running this analysis manually it was taking our lab 16 minutes per sample.  
These scripts allows analysis of each sample to take less than 1 minute with the main delay being   
the runtime of using the deepwings website itself.  
  
Current project was analysing 440 honey bee colonies:  
Manual time taken: 7040 minutes (117.3 hours)  
Auto deep wings time taken: 440 minutes. (7.3 hours)  
  
auto_deep_wings_cropping takes as input a glass sample slide containing honey bee wings which have been affixed   
to the slide using transparent tape. Example file can be found in this repository.
  
auto_deep_wings_website then create a firefox instance and uploads these cropped images to the software and  
downloads the resulting excel file  

auto_deep_wings_analysis is an example of how we typically analyse multiple output files at once.  

