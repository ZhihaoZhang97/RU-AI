import os
import requests
import shutil
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
        desc=f"{file_name}",
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


def combine_parts(base_name, parts):
    parts_sorted = sorted(parts, key=lambda x: int(x.split("_part_")[-1]))
    with open(base_name, "wb") as combined:
        for part in parts_sorted:
            with open(part, "rb") as part_file:
                shutil.copyfileobj(part_file, combined)
    print(f"Combined parts into {base_name}")
    return base_name


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

downloaded_files = []

# Download all files
for file_info in files_list:
    file_name = file_info["key"]
    file_url = file_info["links"]["self"]
    download_file(file_url, file_name)
    downloaded_files.append(file_name)

# Group files by base name for combining parts
base_files = {}
for file_name in downloaded_files:
    if "_part_" in file_name:
        base_name = file_name.split("_part_")[0]
        if base_name not in base_files:
            base_files[base_name] = []
        base_files[base_name].append(file_name)

# Combine parts and extract
for base_name, parts in base_files.items():
    combined_file = combine_parts(base_name, parts)
    extract_file_to_correct_directory(combined_file)

# Extract single-part files
for file_name in downloaded_files:
    if "_part_" not in file_name:
        extract_file_to_correct_directory(file_name)

print("All files downloaded and extracted to correct directories successfully.")
