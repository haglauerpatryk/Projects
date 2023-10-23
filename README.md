Hi!

I uploaded for the time being only one project, because:
  - I prefered to do one bigger project than 10 smaller.
  - I wanted to show some of my actual work and not mini projects from various courses.

I went broadly through entire data pipeline process and it still is in a state of "work in progress."
I tried to list at least different things that I wanted to do next.

To sum up this project I cleaned this data by using this code:
  1.These are the functions that I defined after inspecting those files:

  # 1-3
def file_preparation(df):
    df.drop(["<PER>", "<TIME>", "<OPENINT>"], axis=1, inplace=True)
    df.columns = df.columns.str.replace("<", "").str.replace(">", "")
    df.isnull().sum()

    return df
###
def remove_strings(df):
    df_copy = df.copy()

    for col in df_copy.columns[2:]:
        try:
            df_copy[col] = pd.to_numeric(df_copy[col], errors='coerce')
        except ValueError as e:
            print(f"Error converting column '{col}': {e}")

    df_copy.dropna(subset=df_copy.columns[2:], inplace=True)

    df_copy.dropna(subset=df_copy.columns[2:], inplace=True)
    return df_copy
###
# 4-6
def change_datatype(df):
    for col in df.columns[2:]:
        try:
            df[col] = df[col].astype("float64")
        except ValueError as e:
            print(f"Error converting column '{col}': {e}")

    for col in df.columns[1:2]:
        try:
            df[col] = df[col].astype("datetime64[ns]")
        except ValueError as e:
            print(f"Error converting column '{col}': {e}")

    return df
###
def remove_outliers(df, check_column, column1="TICKER", column2="DATE"):

    df = df.sort_values(by=[column1, column2])
    df = df.assign(DAILY_CHANGE=df.groupby(column1)[check_column].pct_change().abs())

    mask1 = (df["DAILY_CHANGE"] > 0.2) & (df["DAILY_CHANGE"].shift(-1) > 0.15)
    mask2 = (df["DAILY_CHANGE"] > 0.2) & (df["DAILY_CHANGE"].shift(1) > 0.15)

    df["AVG_VALUE"] = (df[check_column].shift(-1) + df[check_column].shift(1)) / 2
    df["AVG_VALUE"] = df["AVG_VALUE"].round(4)

    df.loc[mask1 | mask2, check_column] = df["AVG_VALUE"]
    df.drop(["DAILY_CHANGE", "AVG_VALUE"], axis=1, inplace=True)

    return df





    

      2.And this is an actual performing of data cleaning:

    csv_files = [
    "C:/Users/paha3/Desktop/Python/nasdaqetfs.csv",
    "C:/Users/paha3/Desktop/Python/nasdaqstocks.csv",
    "C:/Users/paha3/Desktop/Python/nyseetfs.csv",
    "C:/Users/paha3/Desktop/Python/nysestocks.csv"
]

for file_path in csv_files:
    df = pd.read_csv(file_path)

    df = file_preparation(df)
    df = remove_strings(df)
    df = change_datatype(df)

    df = df.sort_values(by=["TICKER", "DATE"])
    df = df.assign(DAILY_RETURN=df.groupby("TICKER")["CLOSE"].pct_change())

    df = remove_outliers(df, "OPEN")
    df = remove_outliers(df, "HIGH")
    df = remove_outliers(df, "LOW")
    df = remove_outliers(df, "CLOSE")

    df = df.sort_values(by=["TICKER", "DATE"])
    df = df.assign(DAILY_RETURN=df.groupby("TICKER")["CLOSE"].pct_change().round(6))
    df["DAILY_RETURN"].fillna(0, inplace=True)

    df["VOLUME"] = df["VOL"].round(6)
    df.drop(columns=["VOL"], inplace=True)

    df.loc[df["DAILY_RETURN"] > 0.9, "DAILY_RETURN"] = 0
    
    df.to_csv(file_path, index=False)
    




    Also I created a database and plotted some data using SQL queries.
