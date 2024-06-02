import os
import requests
import subprocess
from tqdm import tqdm

DEPOSIT_ID = "11406538"


def get_deposition_files(deposit_id):
    url = f"https://zenodo.org/api/records/{deposit_id}"

    r = requests.get(url)
    r.raise_for_status()

    deposition = r.json()
    return deposition["files"]


def download_file(file_url, file_name):
    response = requests.get(file_url, stream=True)
    response.raise_for_status()

    total_size = int(response.headers.get("content-length", 0))
    block_size = 8192

    with open(file_name, "wb") as file, tqdm(
        desc=f"./data/{file_name}",
        total=total_size,
        unit="iB",
        unit_scale=True,
        unit_divisor=1024,
    ) as bar:
        for chunk in response.iter_content(chunk_size=block_size):
            file.write(chunk)
            bar.update(len(chunk))
    print(f"Downloaded {file_name}")


def create_directories():
    os.makedirs("./data/text", exist_ok=True)
    os.makedirs("./data/image", exist_ok=True)
    os.makedirs("./data/audio", exist_ok=True)


def extract_file_to_correct_directory(file_name):
    extract_path = ""
    if file_name.startswith("text_"):
        extract_path = "./data/text"
    elif file_name.startswith("image_"):
        extract_path = "./data/image"
    elif file_name.startswith("audio_"):
        extract_path = "./data/audio"
    else:
        print(f"Unknown file type for {file_name}, not extracted.")
        return

    try:
        subprocess.run(["tar", "-xf", file_name, "-C", extract_path], check=True)
        print(f"Extracted {file_name} to {extract_path}")
    except subprocess.CalledProcessError as e:
        print(f"Failed to extract {file_name}: {e}")


# Main script
files_list = get_deposition_files(DEPOSIT_ID)

create_directories()

for file_info in files_list:
    file_name = file_info["key"]
    file_url = file_info["links"]["self"]
    download_file(file_url, file_name)
    extract_file_to_correct_directory(file_name)

print("All files downloaded and extracted to correct directories successfully.")
