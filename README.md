# SLNet-Miner
SLNet-Miner is a tool to collect Simulink models from open source repositories such as GitHub and MATLAB Central

## Recent News
Our paper [SLNET] has been accepted at IEEE International Working Conference on Mining Software Repositories (MSR 2022, CORE: A)

### Installation

SLNet-Miner is tested on Ubuntu 18.04 

First, create virtual environment using  [Anaconda] so that the installation does not conflict with system wide installs.
```sh
$ conda create -n <envname> python=3.7
```

Clone the project and install the dependencies
```sh
$ git clone <gitlink>
$ cd SLNet-Miner
```

Activate environment and Install the dependencies.
```sh
$ conda activate <envname>
$ pip install -r requirements.txt
```


Test your installation 
```sh
$ python downloadRepoFromGithub.py -h
```
This should display help information.

### Usage
#### 1. Mining Repository
downloadRepoFromGithub.py is used to automatically download projects from GitHub and update the metadata in a database.
downloadFromMathWorks.py is used to download projects from MATLAB Central.
 
 To download projects from GitHub, 
 1. Create a personal access token refering [here] 
 2. Replace <YOUR_PERSONAL_ACCESS_TOKEN> with your created token in  downloadRepoFromGithub.py
 3. Run the code as follows:
 ```sh
$ python downloadRepoFromGithub.py -q=Simulink -d=Test_dir -db=abc -flag=X
```
Dont include -flag if you dont want to restrict projects with no license file.
Full details on the flag can be viewed by running : 
```sh
$ python downloadRepoFromGithub.py -h
```

 To download projects from MATLAB Central, 
 1. Update directory, dbname and rss_url in downloadFromMathWorks.py . Ideally use the same dbname for both GitHub  
 2. Run the code as follows:
 ```sh
 python downloadFromMathWorks.py 
```


The table name where metadata is stored can be changed MathWorksRepoInfo.py and SimulinkRepoInfo.py file respectively.

#### 2. Duplicate Finder
Download [SLNET-Corpus] and the duplicate projects. Extract it and update the location in duplicate_project.py
```sh
$ python duplicate_project.py
```
If you copy the duplicate files in the SLNET folder to SLNET_MATLABCENtral folder and use the duplicate folder's sqlite file. The script will find the duplicates. 

### Development

Want to contribute? Great!
SLNet-Miner uses python +  sqlAlchemy for fast developing.

#### Todos

 - Write Test case
 - Exception Handling


[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)
   [Anaconda]: <https://www.anaconda.com/distribution/>
   [SLNET-Corpus]: <https://doi.org/10.5281/zenodo.5259648>
   [here]: <https://help.github.com/en/github/authenticating-to-github/creating-a-personal-access-token-for-the-command-line#creating-a-token>
   [SLNET]: <https://ranger.uta.edu/~csallner/papers/Shrestha22SLNET.pdf>
