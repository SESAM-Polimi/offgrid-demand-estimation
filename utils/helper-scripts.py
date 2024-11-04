import pandas as pd
import pathlib
# def generate_categories(master_file, sheet_name):
#
#     df = pd.read_excel(master_file, sheet_name=sheet_name)
#     df = df.dropna(subset=['Category'])
#     df = df[['Category']]
#     df = df.drop_duplicates()
#     df.to_csv(out_file, index=False)
#
#     return df
#

DB_ROOT = "../../playground/data/LSMS/Tanzania"
root = pathlib.Path(DB_ROOT)

df = pd.read_excel(root.joinpath("_master_xlsx"), sheet_name=sheet_name)
df = df.dropna(subset=['Category'])
df = df[['Category']]
df = df.drop_duplicates()
df.to_csv(out_file, index=False)
