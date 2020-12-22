import requests
from PIL import Image
from argparse import ArgumentParser
from sqlite_database import *
from utils import get_response, fetch_flickr_image

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("--dbFile", type = str, default = "database.db")
    parser.add_argument("--keyword", help = "tag to search for", type = str, default = None)
    parser.add_argument("--numImages", help = "number of images to download", type = int, default = None)
    args = parser.parse_args()
    return args

def results_to_db(database, results):
    for record in results["photos"]["photo"]:
        image_data = fetch_flickr_image(record)
        database.insert(image_data)

def wrap(args):
    args = parse_arguments()
    db = ImageDatabase(args.dbFile)
    result = get_response(args.keyword, args.numImages)
    results_to_db(db, result)
    red_img = db.find_the_most_red_colored_image()
    response = requests.get(red_img, stream = True)
    image = Image.open(response.raw)
    image.show()


if __name__ == "__main__":
    args = parse_arguments()
    wrap(args)

