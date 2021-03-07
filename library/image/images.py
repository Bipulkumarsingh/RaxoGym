import os
import re
from typing import Union
from werkzeug.datastructures import FileStorage
from library.flask_uploads.flask_uploads import UploadSet, IMAGES

IMAGES_SET = UploadSet("images", IMAGES)


def save_image(image: FileStorage, folder: str = None, name: str = None) -> str:
    """Takes FileStorage and saves it to a folder"""
    return IMAGES_SET.save(image, folder, name)


def get_path(filename: str = None, folder: str = None) -> str:
    """Takes image name and folder and return full path"""
    return IMAGES_SET.path(filename, folder)


def find_image_any_format(filename: str, folder: str) -> Union[str, None]:
    """Takes a filename and return an image on any of the accepted formats."""
    for _format in IMAGES:
        image = f"{filename}.{_format}"
        image_path = IMAGES_SET.path(filename=image, folder=folder)
        if os.path.isfile(image_path):
            return image_path
    return None


def _retrieve_filename(file: Union[str, FileStorage]) -> str:
    """Take FileStorage and return the file name.
        Allows our function to call this with boht file names and
        FileStorages and always gets back a file name."""
    if isinstance(file, FileStorage):
        return file.filename
    return file


def is_filename_safe(file: Union[str, FileStorage]) -> bool:
    """check our regex and return whether the string mataches or not"""
    filename = _retrieve_filename(file)
    allowed_format = "|".join(IMAGES)  # png|svg|jpe|jpg|jpeg
    reg = fr"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
    return re.match(reg, filename) is not None


def get_basename(file: Union[str, FileStorage]) -> str:
    """
        Return full name of image in the path
        get_basename('some/folder/images.jgp') return 'image.jpg'
    """
    filename = _retrieve_filename(file)
    return os.path.split(filename)[1]


def get_extension(file: Union[str, FileStorage]) -> str:
    """Return file extension
       get_extension('images.jpg') return '.jpg'"""
    filename = _retrieve_filename(file)
    return os.path.splitext(filename)[1]
