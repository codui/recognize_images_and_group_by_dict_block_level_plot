import os
import re
from pathlib import Path
from pprint import pprint


def get_simple_dict_block_level_plot_from_file(
    path_to_file_with_locations_apartments_by_window_titles: Path,
) -> dict[str, tuple[str, ...]]:
    """
    # ! Preferred usage - simple dictionary structure

    Reads a text file containing data about windows relative to Block, Level, and Plot.
    Parses the data and creates a nested dictionary with tuples at the deepest level.

    Args:
        path_to_file_with_locations_apartments_by_window_titles (Path): Relative or absolute path to the text file.
            For example "info/locations_apartments_by_window_titles.txt"

    Returns:
        dict_simple_block_level_plot: (dict[str, tuple[str, ...]])
            A nested dictionary structured as follows:
                dict_simple_block_level_plot = {

                    'A_L1_Plot_1': ('AV-05-60',
                                    'AV-06-60',
                                    'WA0124',
                                    'WA0123',
                                    'EDA0110',
                                    'WA0122',
                                    'AV-07-60'),

                    'A_L1_Plot_2': ('AV-07-60',
                                    'WA0121',
                                    'WA0120',
                                    'WA0119',
                                    'EDA0109',
                                    'AV-08-60',
                                    'WA0118',
                                    'WA0117',
                                    'AV-09-60'),

                    'A_L1_Plot_2_shared hallway': ('AV-09-60', 'EDA0108', 'AV-10-60', 'AV-11-60'),
                }
    """
    dict_simple_block_level_plot: dict = {}
    # If the file path is of type Path
    if isinstance(path_to_file_with_locations_apartments_by_window_titles, Path):
        # Check if file is absolute
        if not path_to_file_with_locations_apartments_by_window_titles.is_absolute():
            # WindowsPath('D:/WORK/Horand_LTD/TASKS_DOING_NOW/recognize_images/info/src.txt')
            abs_path_to_file_with_locations_apartments_by_window_titles: Path = (
                path_to_file_with_locations_apartments_by_window_titles.resolve()
            )

        # Process the data file abs_path_to_file_with_locations_apartments_by_window_titles
        with open(
            abs_path_to_file_with_locations_apartments_by_window_titles, "r"
        ) as file:
            pattern: str = (
                r"\bBLOCK ?[A-Z]\b|\bLevel ?\d+\b|\bPlot ?\d+\b|\bShared hallway\b"
            )
            # Go through each line of the file
            for line in file:
                # Remove extra characters from a string
                line_formatted: str = line.strip("\n\t ")
                if line_formatted not in (" ", "", "\n"):
                    matches: list[str] = re.findall(
                        pattern, line_formatted, re.IGNORECASE
                    )

                    # If block and level are found
                    if (
                        len(matches) == 2
                        and "block" in matches[0].lower()
                        and "level" in matches[-1].lower()
                    ):
                        block_letter = matches[0].upper()[-1]
                        level_letter_number = (
                            matches[-1].upper()[:1] + matches[-1].split(" ")[-1]
                        )
                        block_level = f"{block_letter}_{level_letter_number}_"

                    elif (  # ! If not work - change to if
                        len(matches) == 1
                        and "plot" in matches[0].lower()
                        and len(line_formatted.replace(matches[0], "").strip()) == 0
                    ):
                        # 'Plot_1'
                        plot = "_".join(matches[0].split(" ")).capitalize()
                        # 'A_L1_Plot_1'
                        block_level_plot = block_level + plot
                        is_block_level_plot_not_exist = (
                            dict_simple_block_level_plot.get(
                                block_level_plot, "not exist"
                            )
                        )
                        # If the block does not exist, create a new dictionary for it
                        if is_block_level_plot_not_exist == "not exist":
                            dict_simple_block_level_plot[block_level_plot] = ()

                    elif (
                        len(matches) == 0
                        and len(line_formatted) > 0
                        and "plot" in block_level_plot.lower()
                    ):
                        dict_simple_block_level_plot[block_level_plot] += tuple(
                            line_formatted.split()
                        )

                    elif (
                        len(matches) == 0
                        and len(line_formatted) > 0
                        and "shared hallway" in block_level_plot.lower()
                    ):
                        dict_simple_block_level_plot[block_level_plot] += tuple(
                            line_formatted.split()
                        )

                    elif (
                        len(matches) == 1
                        and "plot" in matches[0].lower()
                        and len(line_formatted.replace(matches[0], "").strip()) > 0
                    ):
                        # 'Plot_1'
                        plot = "_".join(matches[0].split(" ")).capitalize()
                        # 'A_L1_Plot_1'
                        block_level_plot = block_level + plot
                        dict_simple_block_level_plot[block_level_plot] = tuple(
                            line_formatted.replace(matches[0], "").strip().split()
                        )

                    elif (
                        len(matches) == 1
                        and "shared hallway" in matches[0].lower()
                        and len(line_formatted.replace(matches[0], "").strip()) == 0
                    ):
                        block_level_plot = block_level_plot + f"_{matches[0].lower()}"
                        dict_value_exist = dict_simple_block_level_plot.get(
                            block_level_plot, "not exist"
                        )
                        if dict_value_exist == "not exist":
                            dict_simple_block_level_plot[block_level_plot] = ()
                        else:
                            dict_simple_block_level_plot[block_level_plot] = tuple(
                                line_formatted.replace(matches[0], "").strip().split()
                            )

                    elif (
                        len(matches) == 1
                        and "shared hallway" in matches[0].lower()
                        and len(line_formatted.replace(matches[0], "").strip()) > 0
                    ):
                        block_level_plot = block_level_plot + f"_{matches[0].lower()}"
                        dict_value_exist = dict_simple_block_level_plot.get(
                            block_level_plot, "not exist"
                        )
                        if dict_value_exist == "not exist":
                            dict_simple_block_level_plot[block_level_plot] = tuple(
                                line_formatted.replace(matches[0], "").strip().split()
                            )
                        else:
                            dict_simple_block_level_plot[block_level_plot] = tuple(
                                line_formatted.replace(matches[0], "").strip().split()
                            )
    return dict_simple_block_level_plot


if __name__ == "__main__":
    path_to_file_with_locations_apartments_by_window_titles = Path(
        "info/locations_apartments_by_window_titles.txt"
    )
    dict_simple_block_level_plot: dict[str, tuple[str, ...]] = (
        get_simple_dict_block_level_plot_from_file(
            path_to_file_with_locations_apartments_by_window_titles
        )
    )
    pprint(dict_simple_block_level_plot)

    dict_handy_simple_block_level_plot = {
        "A_L1_Plot_1": (
            "AV-05-60",
            "AV-06-60",
            "WA0124",
            "WA0123",
            "EDA0110",
            "WA0122",
            "AV-07-60",
        ),
        "A_L1_Plot_2": (
            "AV-07-60",
            "WA0121",
            "WA0120",
            "WA0119",
            "EDA0109",
            "AV-08-60",
            "WA0118",
            "WA0117",
            "AV-09-60",
        ),
        "A_L1_Plot_2_shared hallway": ("AV-09-60", "EDA0108", "AV-10-60", "AV-11-60"),
        "A_L1_Plot_3": (
            "AV-10-60",
            "AV-11-60",
            "WA0116",
            "EDA0107",
            "AV-12-60",
            "WA0115",
            "WA0114",
            "WA0113",
            "AV-13-60",
        ),
        "A_L1_Plot_4": ("AV-13-60", "EDA0106", "WA0112", "AV-03-120", "AV-02-120"),
        "A_L1_Plot_5": (
            "AV-03-120",
            "AV-02-120",
            "WA0111",
            "WA0110",
            "EDA0105",
            "AV-14-60",
            "AV-15-60",
        ),
        "A_L1_Plot_6": (
            "AV-14-60",
            "AV-15-60",
            "WA0109",
            "EDA0104",
            "AV-04-120",
            "BV-04-120",
        ),
        "A_L1_Plot_7": (
            "BV-01-120",
            "AV-01-120",
            "WA0108",
            "WA0107",
            "EDA0103",
            "WA0106",
            "AV-02-60",
        ),
        "A_L1_Plot_8": (
            "AV-02-60",
            "WA0105",
            "EDA0102",
            "WA0104",
            "WA0103",
            "AV-03-60",
        ),
        "A_L1_Plot_9": (
            "AV-03-60",
            "WA0102",
            "WA0101",
            "EDA0101",
            "AV-04-60",
            "WA0127",
            "WA0126",
            "WA0125",
            "AV-05-60",
            "AV-06-60",
        ),
        "B_L1_Plot_96": ("BV-03-120", "BV-02-120", "WB0113", "EDB0105", "BV-12-60"),
        "B_L1_Plot_97": (
            "BV-12-60",
            "WB0114",
            "WB0115",
            "WB0116",
            "EDB0106",
            "WB0117",
            "BV-11-60",
            "BV-11-60",
            "EDB0107",
            "BV-10-60",
        ),
        "B_L1_Plot_98": (
            "BV-10-60",
            "WB0118",
            "EDB0108",
            "EDB0109",
            "WB0119",
            "WB0120",
            "WB0125",
            "BV-10-60",
            "WB0121",
            "BV-09-60",
            "BV-08-60",
        ),
        "B_L1_Plot_99": (
            "BV-09-60",
            "BV-08-60",
            "EDB0110",
            "WB0122",
            "WB0123",
            "BV-06-60",
            "BV-07-60",
        ),
        "B_L1_Plot_100": (
            "BV-06-60",
            "BV-07-60",
            "WB0124",
            "EDB0111",
            "WB0101",
            "WB0102",
            "WB0103",
            "BV-04-60",
        ),
        "B_L1_Plot_101": (
            "BV-04-60",
            "WB0104",
            "WB0105",
            "EDB0101",
            "WB0106",
            "BV-03-60",
        ),
        "B_L1_Plot_102": (
            "BV-03-60",
            "WB0107",
            "EDB0102",
            "WB0108",
            "WB0109",
            "BV-02-60",
            "BV-01-60",
        ),
        "B_L1_Plot_103": (
            "BV-02-60",
            "BV-01-60",
            "EDB0103",
            "WB0110",
            "BV-01-120",
            "AV-01-120",
        ),
        "B_L1_Plot_104": (
            "AV-04-120",
            "BV-04-120",
            "EDB0104",
            "WB0111",
            "WB0112",
            "BV-03-120",
            "BV-02-120",
        ),
        "C_L1_Plot_174": (
            "CV-03-60",
            "WC0112",
            "WC0111",
            "WC0110",
            "EDC0106",
            "CV-10-60",
            "CV-02-60",
        ),
        "C_L1_Plot_175": (
            "CV-10-60",
            "CV-02-60",
            "WC0109",
            "WC0108",
            "CV-01-120",
            "DV-01-120",
            "CV-02-120",
            "DV-02-120",
            "WC0107",
            "EDC0105",
            "CV-09-60",
        ),
        "C_L1_Plot_175_shared hallway": ("CV-09-60", "EDC0104", "CV-08-60"),
        "C_L1_Plot_176": (
            "CV-08-60",
            "WC0106",
            "WC0105",
            "WC0104",
            "EDC0103",
            "CV-07-60",
        ),
        "C_L1_Plot_177": (
            "CV-07-60",
            "EDC0102",
            "WC0103",
            "WC0102",
            "CV-06-60",
            "WC0101",
            "EDC0101",
            "WC0119",
            "WC0118",
            "CV-05-60",
        ),
        "C_L1_Plot_178": (
            "CV-05-60",
            "WC0117",
            "WC0116",
            "EDC0108",
            "WC0115",
            "CV-04-60",
            "WC0114",
            "WC0113",
            "EDC0107",
            "CV-03-60",
        ),
        "D_L1_Plot_214": (
            "DV-06-60",
            "DV-12-60",
            "WD0101",
            "WD0102",
            "WD0103",
            "EDD0101",
            "WD0121",
            "WD0122",
            "DV-05-60",
        ),
        "D_L1_Plot_215": (
            "DV-05-60",
            "WD0116",
            "WD0117",
            "WD0118",
            "WD0119",
            "WD012O",
            "DV-11-60",
            "DV-04-60",
        ),
        "D_L1_Plot_216": (
            "DV-03-60",
            "DV-10-60",
            "WD0114",
            "WD0115",
            "EDD0107",
            "DV-11-60",
            "DV-04-60",
        ),
        "D_L1_Plot_217": (
            "DV-03-60",
            "DV-10-60",
            "EDD0106",
            "WD0112",
            "WD0113",
            "DV-09-60",
            "DV-02-60",
        ),
        "D_L1_Plot_218": (
            "DV-09-60",
            "DV-02-60",
            "EDD0105",
            "DV-01-60",
            "WD0108",
            "WD0109",
            "WD0110",
            "DV-02-120",
            "CV-02-120",
            "DV-01-120",
            "CV-01-1",
            "EDD0104",
            "DV-08-60",
            "DV-14-60",
        ),
        "D_L1_Plot_219": (
            "DV-08-60",
            "DV-14-60",
            "WD0107",
            "WD0106",
            "EDD0103",
            "DV-07-60",
            "DV-13-60",
        ),
        "D_L1_Plot_220": (
            "DV-07-60",
            "DV-13-60",
            "WD0105",
            "WD0104",
            "EDD0102",
            "DV-12-60",
            "DV-06-60",
        ),
        "A_L2_Plot_10": (
            "AV-05-60",
            "AV-06-60",
            "WA0225",
            "WA0224",
            "EDA0209",
            "WA0223",
            "AV-07-60",
        ),
        "A_L2_Plot_11": (
            "AV-07-60",
            "WA0222",
            "WA0221",
            "WA0220",
            "EDA0208",
            "AV-08-60",
            "WA0219",
            "WA0218",
            "WA0217",
            "AV-10-6",
            "AV-11-60",
        ),
        "A_L2_Plot_12": (
            "AV-10-60",
            "AV-11-60",
            "WA0216",
            "EDA0207",
            "AV-12-60",
            "WA0215",
            "WA0214",
            "WA0213",
            "AV-13-60",
        ),
        "A_L2_Plot_13": ("AV-13-60", "EDA0106", "WA0212", "AV-02-120", "AV-03-120"),
        "A_L2_Plot_14": (
            "AV-03-120",
            "AV-02-120",
            "WA0211",
            "WA0210",
            "EDA0205",
            "AV-14-60",
            "AV-15-60",
        ),
        "A_L2_Plot_15": (
            "AV-14-60",
            "AV-15-60",
            "WA0209",
            "EDA0204",
            "AV-04-120",
            "BV-04-120",
        ),
        "A_L2_Plot_16": ("WA0108", "WA0208", "WA0207", "EDA0203", "WA0206", "AV-02-60"),
        "A_L2_Plot_17": (
            "AV-02-60",
            "WA0205",
            "EDA0202",
            "WA0204",
            "WA0203",
            "AV-03-60",
        ),
        "A_L2_Plot_18": (
            "AV-03-60",
            "WA0202",
            "WA0201",
            "EDA0201",
            "AV-04-60",
            "WA0228",
            "WA0227",
            "WA0226",
            "AV-05-60",
            "AV-06-60",
        ),
        "B_L2_Plot_105": ("BV-03-120", "BV-02-120", "WB0213", "EDB0205", "BV-12-60"),
        "B_L2_Plot_106": (
            "BV-12-60",
            "WB0214",
            "WB0115",
            "WB0216",
            "EDB0206",
            "WB0217",
            "BV-11-60",
        ),
        "B_L2_Plot_107": (
            "BV-11-60",
            "WB0218",
            "EDB0207",
            "EDB0109",
            "WB0219",
            "WB0220",
            "WB0221",
            "WB0226",
            "BV-10-60",
            "WB0222",
            "BV-08-60",
            "BV-09-60",
        ),
        "B_L2_Plot_108": (
            "BV-09-60",
            "BV-08-60",
            "EDB0208",
            "WB0223",
            "WB0224",
            "BV-06-60",
            "BV-07-60",
        ),
        "B_L2_Plot_109": (
            "BV-06-60",
            "BV-07-60",
            "WB0225",
            "EDB0209",
            "WB0201",
            "WB0202",
            "WB0203",
            "BV-04-60",
        ),
        "B_L2_Plot_110": (
            "BV-04-60",
            "WB0204",
            "WB0205",
            "EDB0201",
            "WB0206",
            "BV-03-60",
        ),
        "B_L2_Plot_111": (
            "BV-03-60",
            "WB0207",
            "EDB0202",
            "WB0208",
            "WB0209",
            "BV-02-60",
            "BV-01-60",
        ),
        "B_L2_Plot_112": (
            "BV-02-60",
            "BV-01-60",
            "EDB0203",
            "WB0210",
            "BV-01-120",
            "AV-01-120",
        ),
        "B_L2_Plot_113": (
            "AV-04-120",
            "BV-04-120",
            "EDB0204",
            "WB0211",
            "WB0212",
            "BV-03-120",
            "BV-02-120",
        ),
        "C_L2_Plot_179": (
            "CV-03-60",
            "WC0204",
            "WC0205",
            "WC0206",
            "EDC0203",
            "CV-10-60",
            "CV-02-60",
        ),
        "C_L2_Plot_180": (
            "CV-10-60",
            "CV-02-60",
            "WC0207",
            "WC0208",
            "CV-01-120",
            "DV-01-120",
            "CV-02-120",
            "DV-02-120",
            "WC0209",
            "EDC0204",
            "CV-09-60",
        ),
        "C_L2_Plot_181": (
            "CV-07-60",
            "EDC0206",
            "WC0213",
            "WC0214",
            "WC0215",
            "EDC0207",
            "WC0216",
            "WC0217",
            "CV-05-60",
        ),
        "C_L2_Plot_182": (
            "CV-05-60",
            "WC0218",
            "WC0219",
            "EDC0201",
            "WC0201",
            "CV-04-60",
            "WC0202",
            "WC0203",
            "EDC0202",
            "CV-03-60",
        ),
        "D_L2_Plot_221": (
            "DV-12-60",
            "DV-06-60",
            "WD0203",
            "WD0202",
            "WD0201",
            "EDD0201",
            "WD0121",
            "WD0223",
            "WD0222",
            "DV-05-60",
        ),
        "D_L2_Plot_222": (
            "DV-05-60",
            "WD0221",
            "WD0220",
            "EDD0207",
            "WD0219",
            "WD0218",
            "WD0217",
            "DV-11-60",
            "DV-04-60",
        ),
        "D_L2_Plot_223": (
            "DV-11-60",
            "DV-04-60",
            "EDD0206",
            "WD0216",
            "WD0215",
            "DV-10-60",
            "DV-03-60",
        ),
        "D_L2_Plot_224": (
            "DV-10-60",
            "DV-03-60",
            "EDD0205",
            "WD0214",
            "WD0213",
            "DV-09-60",
            "DV-02-60",
        ),
        "D_L2_Plot_225": (
            "DV-09-60",
            "DV-02-60",
            "WD0211",
            "WD0210",
            "DV-02-120",
            "CV-02-120",
            "DV-01-120",
            "CV-01-1",
            "EDD0204",
            "WED0208",
            "DV-08-60",
            "DV-14-60",
        ),
        "D_L2_Plot_226": (
            "DV-08-60",
            "DV-14-60",
            "WD0207",
            "WD0206",
            "EDD0203",
            "DV-07-60",
            "DV-13-60",
        ),
        "D_L2_Plot_227": (
            "DV-07-60",
            "DV-13-60",
            "WD0205",
            "WD0204",
            "EDD0202",
            "DV-12-60",
            "DV-06-60",
        ),
    }
