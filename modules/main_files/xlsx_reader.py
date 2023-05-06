# Module that reads and extracts information from xlsx modules. It also stores the last reading in a .pkl
import pandas as pd
from .file_builder import (config_json, PKLFile)


def xlsx_reader(only_read=False):
    config_data = config_json.file
    df = pd.read_excel(config_data["path"], sheet_name=config_data["sheet_name"])
    df[df.columns.values[1]] = df[df.columns.values[1]].replace(0, 25)
    if not only_read:
        data = PKLFile("modules/data/data.pkl")
        data.add_item(df)
        del data
    else:
        return df
