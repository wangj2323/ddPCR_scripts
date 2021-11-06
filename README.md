# ddPCR_scripts


Install git from https://git-scm.com/download/win. "64-bit Git for Windows Setup." After installation use Git Bash to download script from Github.

Tell it where to place the file. EX: cd c/Users/jgee/'OneDrive - Sangamo Therapeutics'/Documents

![image](https://user-images.githubusercontent.com/93787873/140587499-fe8e790c-d867-4f77-9d90-a136f9d0f704.png)

Type this into Git Bash: git clone https://github.com/wangj2323/ddPCR_scripts.git

![image](https://user-images.githubusercontent.com/93787873/140587774-479b5fc5-05de-4bc8-b15b-dcc9486b153c.png)

You will now see the files in your directory. 
Now open "Command Prompt"

On Command Prompt, type in location of code, EX (include the "cd"):
cd "C:\Users\jgee\OneDrive - Sangamo Therapeutics\Documents\ddPCR_scripts"

Once in directory, type in (only needed once, for setup):
pip install -r requirements.txt 

Then load your files into this directory.
One folder with name of your choice. Inside the folder should be "input_data.csv" and "plate_map.csv" in format Microsoft Excel Comma Separated Values File

![image](https://user-images.githubusercontent.com/93787873/140591785-3e3b7af7-345b-4695-9549-78a7aaed8f73.png)

Then execute python ddPCR_analysis.py inputting the name of the folder.
EX: 
![image](https://user-images.githubusercontent.com/93787873/140591296-de3e9e82-7732-4030-9306-2e5e29a34fee.png)
