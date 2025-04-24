import os
import shutil
from pathlib import Path
from pprint import pprint

import cv2
from paddleocr import PaddleOCR

from data import get_simple_dict_block_level_plot_from_file as get_dict_block_level_plot


def get_folder_images(folder_images: str) -> Path:
    """
    The function takes an argument (string) the name of the folder
    in which the images for recognition are.
    Returns the absolute path to the folder with images if folder not empty.

    folder_images: str
        'images'

    folder_images_full_path:
        WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')

    return:
            WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')
    """
    if not folder_images:
        raise TypeError
    folder_images_full_path: Path = Path.cwd() / folder_images
    # Amount folders or files in folder with images
    len_folder: int = len(tuple(folder_images_full_path.iterdir()))
    # If folder_images_path is a folder and not empty
    if Path.is_dir(folder_images_full_path) and len_folder > 0:
        return folder_images_full_path
    elif len_folder == 0:
        raise Exception("Folder is empty!")
    raise Exception("Invalid folder name!")


def get_new_image_name(img_full_path: Path, word_modifier: str = "gray"):
    # ('D:\\', 'WORK', 'Horand_LTD', 'TASKS_DOING_NOW', 'recognize_images', 'images', 'AJLX6735.JPG')
    parts_system_path = img_full_path.parts
    # ('D:\\', 'WORK', 'Horand_LTD', 'TASKS_DOING_NOW', 'recognize_images', 'images')
    first_part_system_path = parts_system_path[:-1]
    # ('AJLX6735.JPG',)
    second_part_system_path = parts_system_path[-1:]
    # 'gray_AJLX6735.JPG'
    name_image = f"{word_modifier}_{second_part_system_path[0]}"
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/gray_AJLX6735.JPG')
    new_image_name = Path(*first_part_system_path, name_image)
    return new_image_name


def recognize_text_from_image(coordinates_roi, only_horizontal=False) -> list[str]:
    # use_angle_cls - определять угол текста
    ocr = PaddleOCR(use_angle_cls=True, lang="en")
    result_recognition = ocr.ocr(coordinates_roi, cls=True, det=True)
    recognized_text = []
    # For now angle - not working
    if only_horizontal:
        for line in result_recognition:
            for box, (text, score) in line:
                if "angle" in box:
                    angle = box["angle"]
                    print(f"{angle=}")
                recognized_text.append(text)
    else:
        recognized_text = [
            text_info[0] for line in result_recognition for _, text_info in line
        ]
    return recognized_text


def get_coordinates_region_of_interest(img_full_path: Path):
    img_gray = cv2.imread(str(img_full_path), cv2.IMREAD_GRAYSCALE)
    # img_height=4032
    img_height: int = img_gray.shape[0]
    # img_width=3024
    img_width: int = img_gray.shape[1]
    width_block_for_recognition: int = 1900
    height_block_for_recognition: int = 1800
    # Coordinates for region of interest
    start_y: int = img_height - height_block_for_recognition
    end_y = img_height
    start_x: int = 0
    end_x = width_block_for_recognition
    # <class 'numpy.ndarray'>
    roi = img_gray[start_y:end_y, start_x:end_x]
    return roi


def get_image_full_path(folder_images_full_path: Path, image_name: str | Path):
    # ! TODO - Test the function !
    """
    Function return absolute path to
    folder_images_full_path: Path
        WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')

    image: Path
        WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AJLX6735.JPG')

    return:
        image
    """
    abs_path_img: None | str | Path = None
    # Если путь к файлу является типом Path
    if isinstance(image_name, Path):
        # Если указан не абсолютный путь к файлу изображения
        if not image_name.is_absolute():
            abs_path_img = folder_images_full_path / image_name
            if abs_path_img.exists():
                # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AENL8576.JPG')
                return abs_path_img
    # Если путь к файлу является типом str
    elif isinstance(image_name, str):
        # Если указан не абсолютный путь к файлу изображения
        if not os.path.isabs(image_name):
            abs_path_img = os.path.abspath(image_name)
            print(f"{abs_path_img=}\n")
    # return abs_path_img


def check_for_match_block_level(key: str, recognized_word: str):
    # dict_number_list=['A', 'L2', 'Plot', '11']
    dict_number_list = key.split("_")
    # recognized_number_list = ['A', 'L2', 'WA0217']
    recognized_number_list = recognized_word.split()

    if len(recognized_number_list) == 3:
        # letter_block_dict='A'
        letter_block_dict: str = dict_number_list[0]
        # letter_block_recognized='A'
        letter_block_recognized = (
            recognized_number_list[0] if recognized_number_list[0].isalpha() else None
        )
        # letter_numb_level_dict='L2'
        letter_numb_level_dict: str = dict_number_list[1]
        # letter_numb_recognized='L2'
        letter_numb_recognized: str | None = (
            recognized_number_list[1]
            if recognized_number_list[1][0].isalpha()
            and recognized_number_list[1][1:].isdigit()
            else None
        )
        if (
            letter_block_recognized is not None
            and letter_block_recognized == letter_block_dict
            and letter_numb_recognized is not None
            and letter_numb_recognized == letter_numb_level_dict
        ):
            return True
        return False
    return False


def get_folder_name_from_dict_block_level_plot(
    dict_block_level_plot: dict[str, tuple[str, ...]], recognized_list: list[str]
) -> str | bool:
    """
    Если распознанный текст с изображения полностью совпал с данными dict_block_level_plot
    то функция возвращает название папки в которую нужно переместить данное изображение.
    Иначе функция возвращает False.
    """
    print("\n")
    print(f"{recognized_list=}")
    all_match: bool = False
    for key, window_names in dict_block_level_plot.items():
        print(f"{key=}, {window_names=}")
        for window_name in window_names:
            # recognized_word = 'D L2 226'
            for recognized_word in recognized_list:
                recognized_word_with_plot = "_".join(
                    recognized_word.split()[:2]
                    + ["Plot"]
                    + recognized_word.split()[-1:]
                )
                # print(f"{recognized_word_with_plot=}")

                if window_name in recognized_word:
                    print(f"{window_name=}, {recognized_word=}")

                    all_match = check_for_match_block_level(key, recognized_word)
                    if all_match:
                        return key
                elif key == recognized_word_with_plot:
                    print(f"{key=}, {recognized_word_with_plot=}")
                    return key

    return all_match


def main() -> None:
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images')
    folder_images_full_path = get_folder_images("images")
    print(f"{folder_images_full_path=}\n")
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/AJLX6735.JPG')
    img_full_path = get_image_full_path(folder_images_full_path, Path("AHUY1123.JPG"))
    print(f"{img_full_path=}\n")
    # # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images/recognized_AJLX6735.JPG')
    # new_image_name = get_new_image_name(img_full_path, "recognized")

    # ROI - region of interest
    coordinates_roi = get_coordinates_region_of_interest(img_full_path)
    recognized_list: list[str] = recognize_text_from_image(coordinates_roi, True)

    dict_block_level_plot: dict[str, tuple[str, ...]] = get_dict_block_level_plot(
        "info/src.txt"
    )
    folder_name_to_remove_image: str | bool = (
        get_folder_name_from_dict_block_level_plot(
            dict_block_level_plot, recognized_list
        )
    )
    # Если folder_name_to_remove_image строка - 'A_L2_Plot_11'
    if folder_name_to_remove_image and type(folder_name_to_remove_image) is str:
        folder_with_target_folders = "folder_by_block_level_plot"
        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/folder_by_block_level_plot/A_L2_Plot_11')
        abs_path_folder_block_level_plot = (
            Path().cwd() / folder_with_target_folders / folder_name_to_remove_image
        )
        # Убедиться что папка abs_path_folder_block_level_plot существует
        # и переместить в неё распознанный файл изображения img_full_path
        if abs_path_folder_block_level_plot.exists():
            shutil.move(img_full_path, abs_path_folder_block_level_plot)

    # # Show image
    # cv2.imshow("gray", coordinates_roi)
    # # Close window by press any key
    # cv2.waitKey(0)
    # # Save image to file
    # cv2.imwrite(new_image_name, coordinates_roi)


if __name__ == "__main__":
    main()
