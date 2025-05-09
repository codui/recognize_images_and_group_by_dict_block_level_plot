import logging
import os
import shutil
from pathlib import Path
from pprint import pprint

import cv2
import numpy as np
from numpy.typing import NDArray
from paddleocr import PaddleOCR

from helpers.data import get_simple_dict_block_level_plot_from_file as get_dict_block_level_plot
from helpers.helpers_func import get_folder_images


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


def recognize_text_from_image(
    ocr: PaddleOCR, coordinates_roi: NDArray[np.uint8], only_horizontal: bool = True
) -> list[str]:
    """Function to recognize text from image.

    Args:
        ocr (PaddleOCR): Экземпляр класса PaddleOCR

        coordinates_roi (NDArray[np.uint8]): Region of interest in the image for recognition
            For example:
                array([
                        [ 95, 100, 100, ..., 203, 206, 207],
                        [ 98,  99,  98, ..., 207, 207, 206],
                        [100,  99,  97, ..., 211, 209, 208],
                        ...,
                        [ 39,  40,  39, ...,  86,  85,  84],
                        [ 39,  41,  39, ...,  88,  85,  88],
                        [ 41,  28,  39, ...,  89,  81,  87]
                    ],
                        shape=(1800, 1900), dtype=uint8)

        only_horizontal (bool, optional): Опция для распознавания только горизонтального текста.
            Defaults to True.

    Values:
        result_recognition (list[list[list[list[float, float], tuple[str, float]]]]):
            For example:
                [
                    [
                        [
                            [[0.0, 0.0], [1.0, 1.0], [2.0, 2.0], [3.0, 3.0]],
                            ("text", 0.99),
                        ]
                    ]
                ]

    Returns:
        list[str]: _description_
    """
    result_recognition: list[
        list[list[list[list[float, float],], tuple[str, float]]]
    ] = ocr.ocr(coordinates_roi, cls=True, det=True)
    # print(f"result_recognition in recognize_text_from_image: {result_recognition=}")

    recognized_text_list = []
    # If result_recognition is not empty and value is not None
    if len(result_recognition) == 1 and result_recognition[0] is not None:
        # For now angle - not working
        if only_horizontal:
            # Get only horizontal text from result_recognition and add to list recognized_text_list
            for line in result_recognition:
                for box, (text, score) in line:
                    if "angle" in box:
                        angle = box["angle"]
                        # print(f"{angle=}")
                    recognized_text_list.append(text)
        else:
            recognized_text_list = [
                text_info[0] for line in result_recognition for _, text_info in line
            ]
    # print(f"recognized_text_list: {recognized_text_list=}")
    return recognized_text_list


def get_coordinates_region_of_interest(img_full_path: Path) -> NDArray[np.uint8]:
    """Function to get coordinates of the region of interest
    in the image for recognition.

    Args:
        img_full_path (Path): Abs path to the image
            For example:
                WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize/AADC5918.JPG')

    Values:
        width_block_for_recognition (int): Width of the block for recognition
            1900

        height_block_for_recognition (int): Height of the block for recognition
            1800

    Returns:
        roi (NDArray[np.uint8]): Region of interest in the image for recognition
            For example:
                array([
                        [ 95, 100, 100, ..., 203, 206, 207],
                        [ 98,  99,  98, ..., 207, 207, 206],
                        [100,  99,  97, ..., 211, 209, 208],
                        ...,
                        [ 39,  40,  39, ...,  86,  85,  84],
                        [ 39,  41,  39, ...,  88,  85,  88],
                        [ 41,  28,  39, ...,  89,  81,  87]
                    ],
                        shape=(1800, 1900), dtype=uint8)
    """
    # Read image in grayscale
    img_gray = cv2.imread(str(img_full_path), cv2.IMREAD_GRAYSCALE)
    # img_height=4032
    img_height: int = img_gray.shape[0]
    # img_width=3024
    img_width: int = img_gray.shape[1]
    # Width of the block for recognition
    width_block_for_recognition: int = 1900
    # Height of the block for recognition
    height_block_for_recognition: int = 1800
    # Coordinates for region of interest
    start_y: int = img_height - height_block_for_recognition
    end_y: int = img_height
    start_x: int = 0
    end_x: int = width_block_for_recognition
    # <class 'numpy.ndarray'>
    roi: NDArray[np.uint8] = img_gray[start_y:end_y, start_x:end_x]
    return roi


def check_for_match_block_level_plot(key: str, recognized_word_with_plot: str) -> bool:
    """
    Checks if the recognized word with plot matches the given key based on specific criteria.

    Args:
        key (str): The reference key representing a block-level plot.
            Example: "C_L2_Plot_182"

        recognized_word_with_plot (str): The recognized word containing plot information.
            Example: "C_L2_Plot_182_WC0214"

    Returns:
        bool: True if the recognized word matches the key based on block and level criteria, False otherwise.

    Example:
        key = "C_L2_Plot_182"
        recognized_word_with_plot = "C_L2_Plot_182_WC0214"
        Result: True (if block and level match)
    """
    # print(f"{key=}, {recognized_word_with_plot=}")

    # key = "C_L2_Plot_182"
    # recognized_word_with_plot = "C_L2_Plot_182_WC0214"

    # list_block_level_plot = ["C", "L2", "Plot", "182"]
    list_block_level_plot: list[str] = key.split("_")
    # recognized_number_list = ["C", "L2", "Plot", "182", "WC0214"]
    recognized_number_list: list[str] = recognized_word_with_plot.split()

    # If length of recognized_number_list is 3
    if len(recognized_number_list) == 3:
        # letter_block_from_dict='C'
        letter_block_from_dict: str = list_block_level_plot[0]
        # letter_block_recognized='C'
        letter_block_recognized: str | None = (
            recognized_number_list[0] if recognized_number_list[0].isalpha() else None
        )

        # level_from_dict='L2'
        level_from_dict: str = list_block_level_plot[1]
        # level_recognized='L2'
        level_recognized: str | None = (
            recognized_number_list[1]
            if recognized_number_list[1][0].isalpha()
            and recognized_number_list[1][1:].isdigit()
            else None
        )
        """
        If letter_block_recognized and level_recognized are not None and equal to
        letter_block_from_dict and level_from_dict
        """
        if (
            letter_block_recognized is not None and letter_block_recognized == letter_block_from_dict
            and level_recognized is not None and level_recognized == level_from_dict
        ):
            return True
        """
        Else if letter_block_recognized is None and level_recognized is None
        or level_recognized is not equal to level_from_dict
        or letter_block_recognized is not equal to letter_block_from_dict
        """
        return False
    # Else if length of recognized_number_list not equal 3 - return False
    return False


def get_folder_name_from_dict_block_level_plot(
    dict_block_level_plot: dict[str, tuple[str, ...]], recognized_text_list: list[str]
) -> str | bool:
    """
    Determines the folder name to which an image should be moved based on recognized text
        and a dictionary of block-level plot data.

        Args:
            dict_block_level_plot (dict[str, tuple[str, ...]]): A dictionary mapping block-level plot keys
                to tuples of associated window names.
                Example:
                    {
                        "C_L2_Plot_182": ("WC0218", "WC0219", "EDC0201"),
                        "A_L1_Plot_101": ("WC0101", "WC0102")
                    }
            recognized_text_list (list[str]): A list of recognized text strings from the image.
                Example:
                    [
                        "C L2 182 wC0214",
                        "Time",
                        "Mon, 24/03/2025 16:04",
                        "Address",
                        "265 Burlington Road, New",
                        "Malden,KT3 4NE,England",
                        "Lat/Long",
                        "51.402211N.0.237727W",
                        "Company",
                        "LMB",
                        "Name",
                    ]

        Returns:
            str | bool: The name of the folder to move the image to if a match is found,
            or False if no match is found.
                Example:
                    'C_L2_Plot_182'
                    False

        Example:
            dict_block_level_plot = {
                "C_L2_Plot_182": ("WC0218", "WC0219", "EDC0201"),
                "A_L1_Plot_101": ("WC0101", "WC0102")
            }
            recognized_text_list = ["C L2 182 wC0214", "Time", "Mon, 24/03/2025 16:04"]
            result = get_folder_name_from_dict_block_level_plot(dict_block_level_plot, recognized_text_list)
            print(result)  # Output: 'C_L2_Plot_182'
    """
    print(f"{recognized_text_list=}")

    all_match: bool = False
    for key, window_names in dict_block_level_plot.items():
        # key="C_L2_Plot_182"
        # window_names
        # ("CV-05-60","WC0218","WC0219","EDC0201","WC0201","CV-04-60","WC0202","WC0203","EDC0202", "CV-03-60")

        print(f"{key=}, {window_names=}")
        for window_name in window_names:
            # recognized_word = "C L2 182 wC0214"
            for recognized_word in recognized_text_list:
                # Process recognized_word_with_plot to make - 'C_L2_Plot_182_WC0214'
                recognized_word_with_plot: str = "_".join(
                    recognized_word.upper().split()[:2]
                    + ["Plot"]
                    + recognized_word.upper().split()[-1:]
                )
                # print(f"{recognized_word_with_plot=}")

                # Check if key is equal to recognized_word_with_plot
                # "C_L2_Plot_182" == 'C_L2_Plot_182_WC0214'
                if key == recognized_word_with_plot:
                    # print(f"{key=}, {recognized_word_with_plot=}")
                    # "C_L2_Plot_182"
                    # TODO - сделать проверку key на правильность номера квартиры с помощью файла filter_plots.py
                    # ! Логика filter_plots.py создана на основе файла Flat_Numbering_Formatted.xlsx
                    return key
                # Check if window_name is in recognized_word
                # if "WC0214" in "C_L2_Plot_182_WC0214" check the match letter block and number level
                elif window_name in recognized_word_with_plot:
                    # print(f"{window_name=}, {recognized_word=}")
                    # Check if letter block and number level match
                    all_match = check_for_match_block_level_plot(
                        key, recognized_word_with_plot
                    )
                    # If all_match is True return key "C_L2_Plot_182"
                    if all_match:
                        return key
        print("\n")
    return all_match


def main() -> None:
    # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize')
    folder_images_full_path = get_folder_images(r"images_for_recognize")
    # print(f"{folder_images_full_path=}")
    # use_angle_cls - определять угол текста
    ocr: PaddleOCR = PaddleOCR(use_angle_cls=True, lang="en")
    # If folder_images_full_path not None
    if folder_images_full_path is not None:
        path_to_file_with_locations_apartments_by_window_titles = Path(
            "info/locations_apartments_by_window_titles.txt"
        )
        dict_block_level_plot: dict[str, tuple[str, ...]] = get_dict_block_level_plot(
            path_to_file_with_locations_apartments_by_window_titles
        )
        # print(f"{dict_block_level_plot=}")

        folder_with_target_folders_by_location_apartments = "folder_by_block_level_plot"

        for img_full_path in folder_images_full_path.iterdir():
            # img_full_path:
            # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize/AADC5918.JPG')
            # print(f"{img_full_path.suffix.lower()=}")

            if img_full_path.suffix.lower() == ".jpg":
                print(f"Processing image: {img_full_path}")

                # # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/images_for_recognize/recognized_AJLX6735.JPG')
                # new_image_name = get_new_image_name(img_full_path, "recognized")

                # roi - region of interest, type - NDArray[np.uint8]
                coordinates_roi: NDArray[np.uint8] = get_coordinates_region_of_interest(
                    img_full_path
                )
                # recognized_text_list: ['CUSTOMER', 'POSTCODE', 'LEEM', 'NO.OF PALLETS', 'LEY', 'K734', '42']
                recognized_text_list: list[str] = recognize_text_from_image(
                    ocr, coordinates_roi, only_horizontal=True
                )
                # print(f"recognized_text_list: {recognized_text_list}")

                if len(recognized_text_list) > 0:
                    # 'A_L2_Plot_11'
                    folder_name_to_remove_image: str | bool = (
                        get_folder_name_from_dict_block_level_plot(
                            dict_block_level_plot, recognized_text_list
                        )
                    )
                    print(f"folder_name_to_remove_image: {folder_name_to_remove_image}")

                    # Если folder_name_to_remove_image существует и это строка - 'A_L2_Plot_11'
                    if (
                        folder_name_to_remove_image
                        and type(folder_name_to_remove_image) is str
                    ):
                        # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/folder_by_block_level_plot/A_L2_Plot_11')
                        abs_path_folder_block_level_plot = (
                            Path().cwd()
                            / folder_with_target_folders_by_location_apartments
                            / folder_name_to_remove_image
                        )
                        # Убедиться что папка abs_path_folder_block_level_plot существует
                        # и переместить в неё распознанный файл изображения img_full_path
                        if abs_path_folder_block_level_plot.exists():
                            shutil.move(img_full_path, abs_path_folder_block_level_plot)
                            print(
                                f"Move image: {img_full_path} to folder: {abs_path_folder_block_level_plot}"
                            )
                            # TODO - записати у текстовий документ номер вікна розпізнаного з фото.
                            # TODO - реалізувати можливість отримати список вікон з назвами папок де вони знаходяться
                            # TODO - в текстовому файлі записувати які вікна є в яких квартирах і скільки вікон
                            # TODO - автоматизувати додавання TODO - фото з D:\WORK\Horand_LTD\TASKS_DOING_NOW\recognize_images\folder_by_block_level_plot
                            # TODO - у пункт side_rise 2.3 і procore

                            # TODO - через 1-2 тиждні одним скриптом реалізувати завантаження фото із whatsapp групи
                            # TODO - у side-rise на asite і в procore

    # # Show image
    # cv2.imshow("gray", coordinates_roi)
    # # Close window by press any key
    # cv2.waitKey(0)
    # # Save image to file
    # cv2.imwrite(new_image_name, coordinates_roi)


if __name__ == "__main__":
    main()
