

# RU-AI

This is the official repo for paper: RU-AI: A Large Multimodal Dataset for Machine Generated Content Detection

## Requirement
The dataset is publicly avaliable at zenodo: 
```url
https://zenodo.org/records/11406538
```

The dataset requires at least 200Gb of disk space to be fully downloaded. 

The model inference requires a Nvidia GPU with at least 16GB of vRAM to run. We recommend to have **NVIDIA RTX 3090, 24GB or anything above** to run this project.

### Dependencies
We highly recommend to have packages installed within a **virtual environment** such as **[conda](https://conda.io/projects/conda/en/latest/user-guide/install/index.html)** or **[venv](https://docs.python.org/3/library/venv.html)**.

Clone the project:
```bash
git clone https://github.com/ZhihaoZhang97/RU-AI.git
```
Create the virtual environment via conda and Python 3.8:
```bash
conda create -n ruai python=3.8
```
Activate the environment:
```bash
conda activate ruai
```
Move into the project path:
```bash
cd RU-AI
```
Install the dependencies:
```bash
pip3 install -r requirements.txt
```

## Data Sample
We provide a quick tutorial on how to download and inspect the dataset on the ```data-example.ipynb``` notebook. 

You can also directly run the follwoing code to download smaple data sourced from flickr8k:
```bash
python ./download_flickr.py
```
You can also download all the data sourced from by running thw following code:

Please note the whole dataset **is over 157GB** in compression, it will take a while for downloading, the actual speed depends on your internet.
```bash
python ./download_all.py
```

 Then go to ```./data``` to manually check the data after downloading.



## Model Inference


