import os
import re
from pathlib import Path


def remove_duplicates_images_from_folder(path_target_folder: str | Path) -> None:
    """
    Removes duplicate image files from the specified folder.
    A duplicate is identified as a file containing "copy" or "Copy" in its name,
    and its size matches the size of the original file.

    Args:
        path_target_folder (str | Path): The target folder containing image files.
            Can be provided as a string or a Path object.

    Returns:
        None: This function does not return a value. It performs file deletion
        operations directly on the filesystem.

    Raises:
        FileNotFoundError: If the specified folder does not exist.
        PermissionError: If the function lacks permissions to access or delete files.
    """
    # Ensure path_target_folder is an absolute Path object
    if not os.path.isabs(path_target_folder):
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')
        path_target_folder = Path(path_target_folder).resolve()

    # Check if path_target_folder is type Path
    if isinstance(path_target_folder, Path):
        for path_obj in path_target_folder.iterdir():
            # Check if the file name contains "copy" or "Copy"
            if "copy" in path_obj.name.lower():
                pattern = r"^(.*?)(?:_copy\d+| - Copy)"
                match = re.match(pattern, str(path_obj))
                if match:
                    # 'D:\\WORK\\Horand_LTD\\TASKS_DOING_NOW\\recognize_images\\images\\ADAI3306.JPG'
                    # Remove "copy" or "Copy" from path_obj and get path to original file
                    original_file_name: Path = Path(match.group(1) + path_obj.suffix)
                    # Compare file sizes and delete the duplicate if sizes match
                    if path_obj.stat().st_size == original_file_name.stat().st_size:
                        path_obj.unlink()


remove_duplicates_images_from_folder(path_target_folder="images")
