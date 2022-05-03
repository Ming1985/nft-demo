from curses import meta
from pathlib import Path
from brownie import AdvancedCollectible, network
import requests

from scripts.helpful_scripts import get_breed
from metadata.sample_metadata import metadata_template


def main():
    advanced_collectible = AdvancedCollectible[-1]
    number_of_advanced_colelctibles = advanced_collectible.tokenCounter()
    print(f"you have created {number_of_advanced_colelctibles} collectibles ")
    # need to create a json file contains all attributes
    for token_id in range(number_of_advanced_colelctibles):
        breed = get_breed(advanced_collectible.tokenIdToBreed(token_id))
        metadata_file_name = (
            f"./metadata/{network.show_active()}/{token_id}-{breed}.json"
        )
        collectible_metadata = metadata_template
        if Path(metadata_file_name).exists():
            print(f"{metadata_file_name} already exists ! delete it to overwrite")
        else:
            print(f"creating metadata file {metadata_file_name}")
            collectible_metadata["name"] = breed
            collectible_metadata["description"] = f"an adorable {breed} pup!"
            image_path = "./img/" + breed.lower().replace("_", "-") + ".png"
            print(collectible_metadata)
            image_uri = upload_to_ipfs(image_path)
            collectible_metadata["image_uri"]


def upload_to_ipfs(filepath):
    with Path(filepath).open("rb") as fp:
        image_binary = fp.read()
    ipfs_url = "http://127.0.0.1:5001"
    end_point = "/api/v0/add"
    response = requests.post(ipfs_url + end_point, files={"file": image_binary})
    # respons format:
    # {'Bytes' : , "Hash": , "Name":, "Size":}
    # ipfs saves file with a hash, like following file
    # ipfs.io/ipfs/xxxxxxxxxxxxxxx?filename=0-PUG.json
    ipfs_hash = response.json()["Hash"]
    # "./img/PUG.png" -> "PUG.png"
    filename = filepath.split("/")[-1:][0]
    image_url = f"https://ipfs.io/ipfs/{ipfs_hash}?filename={filename}"
