"""The module contains helper functions for the project and for the tests"""

from pathlib import Path


def get_folder_images(folder_images: str) -> Path | None:
    """
    The function takes an argument (string) the name of the folder
    in which the images for recognition are.
    Returns the absolute path to the folder with images if the folder is not empty.

    Args:
        folder_images: (str) The name of the folder with images for recognition.
            For example: 'images_for_recognize'

    Returns:
        folder_images_full_path: (Path) The absolute path to the folder with images for recognition.
            WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize')
    """
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize')
    folder_images_full_path: Path = Path.cwd() / folder_images
    # print(f"{folder_images_full_path=}")

    # Amount folders or files in folder with images
    len_folder: int = len(tuple(folder_images_full_path.iterdir()))
    # If folder_images_path is a folder and not empty
    if Path.is_dir(folder_images_full_path) and len_folder > 0:
        return folder_images_full_path
    elif len_folder == 0:
        raise Exception("Folder is empty!")
    return None


def get_image_full_path(folder_images_full_path: Path, image_name_to_recognize: Path):
    """
    The function takes as input the path to the folder with images "folder_images_full_path"
    and the image name "image_name_to_recognize".
    If the path to the image is relative, the function returns the absolute path to the image.
    If the path to the image is absolute, the function returns it as is.

    Args:
        folder_images_full_path: Path
            WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize')

        image_name_to_recognize: (Path)
            WindowsPath('ADRX7565.JPG')

    Rreturns:
        abs_path_img: (Path)
            WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize/ADRX7565.JPG')
    """
    abs_path_img: Path | None = None
    # If the file path is of type Path
    if isinstance(image_name_to_recognize, Path):
        # If the specified path to the image file is not absolute
        if not image_name_to_recognize.is_absolute():
            # Absolute path to the image file
            abs_path_img = folder_images_full_path / image_name_to_recognize
            # Check if the image file exists
            if abs_path_img.exists():
                # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AENL8576.JPG')
                return abs_path_img
            return "Invalid path to image file specified!"

        # If absolute path to image file is specified
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AENL8576.JPG')
        abs_path_img = image_name_to_recognize
        return abs_path_img

    # If the file path is not of type Path
    raise TypeError(
        f"Type of image_name_to_recognize is not Path: {type(image_name_to_recognize)}. Must be Path."
    )


def main() -> None:
    """
    The main function for testing the module.
    """
    # ! Only for test
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize')
    folder_images_full_path = get_folder_images(r"images_for_recognize")
    # print(f"{folder_images_full_path=}")
    # WindowsPath('ADRX7565.JPG')
    image_name_to_recognize: Path = Path("ADRX7565.JPG")
    # print(f"{image_to_recognize=}")

    if folder_images_full_path is not None:
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize/ADRX7565.JPG')
        img_full_path = get_image_full_path(
            folder_images_full_path, image_name_to_recognize
        )
        print(f"{img_full_path=}\n")


if __name__ == "__main__":
    main()
