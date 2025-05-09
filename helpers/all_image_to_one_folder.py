import shutil
from pathlib import Path
from pprint import pprint


def remove_all_images_to_one_folder(
    path_src_folder: Path,
    path_target_folder: Path,
    format_image: str = ".jpg",
) -> None:
    """
    Функция проходит по всем папкам внутри папки path_src_folder
    и проверяет является ли файл изображением указанного формата (по умолчанию ".jpg").
    Если файл нужного формата то переносит его в папку path_target_folder.
    Args:
        path_src_folder (Path): Relative or absolute path to the folder with folders and images inside folders.

        path_target_folder (Path): Relative or absolute path to the target folder.
                                    Where all the images should be in the end of work function.

        format_image (str): Format of image file. By default ".jpg".
    Returns:
        None
    """
    path_src_folder.is_absolute()
    # Check if path_src_folder is absolute
    if not path_src_folder.is_absolute():
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_to_recognize')
        path_src_folder = path_src_folder.resolve()
    # Check if path_target_folder is absolute
    if not path_target_folder.is_absolute():
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')
        path_target_folder = path_target_folder.resolve()

    # Если path_obj это файл с расширением ".jpg" то перемещаем его в папку path_target_folder
    for path_obj in path_src_folder.iterdir():
        # path_obj = ('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_to_recognize/Pictures/AEGO8215.JPG')
        if path_obj.is_file() and path_obj.suffix.lower() == ".jpg":
            print(f"{path_obj=}")
            # target_file = ('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AEGO8215.JPG')
            target_file = path_target_folder / path_obj.name
            print(f"{target_file=}")

            # Если path_obj существует в целевой папке то создать копию файла и сохранить в целевой папке
            if target_file.exists():
                base = path_obj.stem
                ext = path_obj.suffix
                counter = 1
                while True:
                    new_name = f"{base}_copy{counter}{ext}"
                    new_target = path_target_folder / new_name
                    if not new_target.exists():
                        break
                    counter += 1
                shutil.move(str(path_obj), str(new_target))
            else:
                shutil.move(str(path_obj), str(path_target_folder))

    for path_obj in path_src_folder.iterdir():
        if path_obj.is_dir():
            remove_all_images_to_one_folder(path_obj, path_target_folder)


if __name__ == '__main__':
    remove_all_images_to_one_folder(
        path_src_folder=Path("images_in_folders"),
        path_target_folder=Path("images_to_recognize"),
    )
