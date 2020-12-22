from config import AUTH_KEY
import requests
from io import BytesIO
from PIL import Image
import numpy as np
import cv2
from errors import ConnectionFailure
def get_response(keyword = None, numImages = None):
    """
    [Get response from Flickr API. If keyword and numImages are not passed, fetches 100 most recent photos data]

    Args:
        keyword ([str], optional): [Tag to search for]. Defaults to None.
        numImages ([int], optional): [Number of images to download]. Defaults to None.

    Returns:
        [dict]: [json style dictionary containing Flickr response]
    """
    if keyword:
        kwargs = {
        "method": "flickr.photos.search",
        "tags": keyword,
        "safe_search": 1,
        "per_page": numImages
                }
    else:
        kwargs = {
            "method": "flickr.photos.getRecent",
            "per_page": 100
                }

    params = {
        "api_key": AUTH_KEY,
        "format": "json",
        "nojsoncallback": 1,
        **kwargs
    }

    response = requests.get("https://api.flickr.com/services/rest/", params)
    if response.status_code != 200:
        raise ConnectionFailure(response)
    return response.json()

def construct_image_url(image_info):
    """
    [Construct an image URL from json data]

    Args:
        image_info ([dict]): [dictionary containing information of specified image]

    Returns:
        [str]: [URL path to specified image]
    """
    serverId = image_info["server"]
    id = image_info["id"]
    secret = image_info["secret"]
    return f"https://live.staticflickr.com/{serverId}/{id}_{secret}.jpg"

def fetch_flickr_image(image_info):
    """
    [Get image url and byte image representation]

    Args:
        image_info ([res]): [dictionary containing information of specified image]

    Returns:
        [tuple]: [URL and byte representation of an image]
    """
    stream = BytesIO()
    image_url = construct_image_url(image_info)
    response = requests.get(image_url, stream = True)
    image = Image.open(response.raw)
    image.save(stream, format = "JPEG")
    image_bytes = stream.getvalue()
    return (image_url, image_bytes)

def reconstruct_from_bytes(img_bytes):
    """
    Returns:
        [np.array]: [Image reconstructed from bytes]
    """
    img_array = np.frombuffer(img_bytes, dtype = np.uint8)
    return cv2.imdecode(img_array, cv2.IMREAD_COLOR)

def evaluate_img_red(img):
    """
    [Get red pixels mask]

    Args:
        img ([np.array]): [Image to get mask from]

    Returns:
        [np.array]: [mask of red pixels in original image]
    """
    img = cv2.resize(img, (512, 512), img)
    img_hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lower_red = np.array([0,50,50])
    upper_red = np.array([10,255,255])
    mask0 = cv2.inRange(img_hsv, lower_red, upper_red)

    lower_red = np.array([170,50,50])
    upper_red = np.array([180,255,255])
    mask1 = cv2.inRange(img_hsv, lower_red, upper_red)

    return np.sum(mask0 + mask1, dtype = int)

