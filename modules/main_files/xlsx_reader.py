# Module that reads and extracts information from xlsx modules. It also stores the last reading in a .pkl
import pandas as pd
import pickle
from .config_control import read_json


def xlsx_reader(only_read=False):
    """
    Simple function that reads a xlsx file and stores its data in a .pkl or returns it in a direct read
    :param only_read: Controls if the data file is going to be updated or only the Excel reading is going to be returned
    :return: Data extracted directly from the Excel file
    """
    config_data, status = read_json()
    df = pd.read_excel(config_data["path"], sheet_name=config_data["sheet_name"])
    # We change the day parameters with value 0 to 25. This is depending on the context of use of the program.
    df[df.columns.values[1]] = df[df.columns.values[1]].replace(0, 25)
    # Storing the reading in the .pkl file
    if not only_read:
        with open("modules/data/data.pkl", "wb") as file:
            pickle.dump(df, file)
    else:
        return df
