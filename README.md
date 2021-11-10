# ddPCR_scripts

HOW TO SET UP AND INSTALL CODE (ONE TIME): 

First install Python on your laptop by going to the Sangamo IT Self Help Portal (click on the arrow in the lower left of your desktop, and then the Sangamo logo) or ask IT.

Install git from https://git-scm.com/download/win. "64-bit Git for Windows Setup" with all default settings. After installation, open Git Bash to download script from Github.

Tell it where to place the file by typing the location. You can do this by opening your computer folder directory, going to the folder you want it in. Then right click, "Git Bash here." It'll open a new window of Git Bash with the correct location at the top of the window, type that after "cd" in the example and then X out that extra window.

EX: **cd /C/Users/jgee/Documents** and then click Enter.

![image](https://user-images.githubusercontent.com/93787873/141066932-0de89b78-0b6a-4c93-9f11-a44dee195283.png)


Type this into Git Bash as is, and click Enter: **git clone https://github.com/wangj2323/ddPCR_scripts.git**

This is an example of what it would look like when the action is complete:

![image](https://user-images.githubusercontent.com/93787873/141067261-4a4b2726-b3fe-412d-a13b-3aab9db28212.png)


You will now see the files in your directory in a new folder called "ddPCR_scripts." 

Now open "Command Prompt" from your computer, and X out the Git Bash window.

On Command Prompt, type in location of code and click Enter. EX (include the "cd", same as above, but in different format shown below, and "ddPCR_scripts" at the end):
**cd "C:\Users\jgee\Documents\ddPCR_scripts"**


Once in directory, type in exactly (only needed once, for setup):
**pip install -r requirements.txt**

It will look like this when finished. Ignore yellow warnings.

![image](https://user-images.githubusercontent.com/93787873/141069176-a1d6ee29-efa8-4b0e-bf57-7ff431b8b502.png)


HOW TO RUN CODE:

Load your files into this "ddPCR_scripts" folder in your directory for each run. One folder per run.

Name folder with name of your choice. Inside the folder should be these two sheets "input_data.csv" and "plate_map.csv," both in Microsoft Excel Comma Separated Values File format (aka CSV UTF-8 (comma delimited)(*.csv)").

Here's an example of what the files look like in the code folder:

![image](https://user-images.githubusercontent.com/93787873/140591785-3e3b7af7-345b-4695-9549-78a7aaed8f73.png)


Here's an example of what the files in the named run folder look like:

![image](https://user-images.githubusercontent.com/93787873/140591815-89218f02-ba64-4f88-9da5-f6d5d3dc116e.png)


This is an example of how the plate map should be formatted with only this in the Excel (Assay SPACE SampleName SPACE Dilution)

"NA" for blank wells

"Assay SPACE 'NTC'" for NTC wells

"Map" in the upper right corner, 1-12 horizontal, A-H vertical from there

![image](https://user-images.githubusercontent.com/93787873/140591875-5db28829-7851-4edb-a913-c2cf8a635fe2.png)

Type in the location of the ddPCR_scripts folder again as mentioned above.

![image](https://user-images.githubusercontent.com/93787873/141070746-aa72ef7b-ecf7-4d0f-b24c-6273234e6b76.png)


Then execute python ddPCR_analysis.py copy/pasting the below and only changing the name of the folder run.

Type in **python ddPCR_analysis.py ASRv65/input_data.csv ASRv65/plate_map.csv** changing the "ASRv65" to the run folder name you want to analyze.

Click Enter to execute. Run is completed when it says "PROCESS COMPLETE." It will create new "Output" files in the code folder. One output file per channel.
There are 3 tabs; one with output calculations for samples and NTC at bottom, one NTC only, and one summary.

The code excludes high OOR values and "No Call" but manual analysis and check and recalculation of Linearity and CV are needed.

If errors occur in code, please double check the plate map and file formats.



