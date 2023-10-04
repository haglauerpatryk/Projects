# Analyzing Stock prices

#### This project contains 4 parts:
    1.Preparation for Data cleaning. Trying to perform data cleaning on smallest file and look for potential flaws of data.
    2.Compressing and performing data cleaning process. 
    3.Creating tables and loading data. 
    4.Ploting data to get some information.


##### I wanted to broadly go through entire process and I've tried to list potential next steps that I would take to improve quality of data even further.


```python
# Libraries:

import os
import csv
import psycopg2
import numpy as np
import pandas as pd
from io import StringIO
from tabulate import tabulate
import matplotlib.pyplot as plt
from multiprocessing import Pool
```

# I. Perform ETL process:
- #### 1. Preparing data cleaning Process.
- #### 2. Optimizing its efficiency.
- #### 3. Performing this process over all files.
- #### 4. Loading data to a database.

## 1. Preparing data cleaning Process.

I obtained data from https://stooq.com/db/h/ and downloaded from cell ["U.S.","daily"]

### I. File preparation:
 - I want to merge all contents of each folder into newly created file.
 - I changed file format into CSV, because I'm way more likely to encounter it as a Data Engineer.
 - Below i check some basic information to inspect a file.


```python
folder_path = [
    "C:/Users/paha3/Desktop/us/nasdaq etfs",
    "C:/Users/paha3/Desktop/us/nasdaq stocks",
    "C:/Users/paha3/Desktop/us/nyse etfs",
    "C:/Users/paha3/Desktop/us/nyse stocks"
]

file_destination = [
    "C:/Users/paha3/Desktop/us/nasdaqetfs.txt",
    "C:/Users/paha3/Desktop/us/nasdaqstocks.txt",
    "C:/Users/paha3/Desktop/us/nyseetfs.txt",
    "C:/Users/paha3/Desktop/us/nysestocks.txt"
]

# Get a list of full file paths in the folder
def get_file_list(folder_path):
    file_list = [os.path.join(folder_path, file_name) for file_name in os.listdir(folder_path)]
    return file_list

def merge_files(file_list, output_file):
    count = 0
    try:
        with open(output_file, "w") as output:
            for file_name in file_list:
                with open(file_name, "r") as input_file:
                    output.write(input_file.read())
                    count += 1
        print(f"Merged {count} files into {output_file}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")

for i in range(len(folder_path)):
    merge_files(get_file_list(folder_path[i]), file_destination[i])
```

    Merged 365 files into C:/Users/paha3/Desktop/us/nasdaqetfs.txt
    Merged 4807 files into C:/Users/paha3/Desktop/us/nasdaqstocks.txt
    Merged 2173 files into C:/Users/paha3/Desktop/us/nyseetfs.txt
    Merged 3687 files into C:/Users/paha3/Desktop/us/nysestocks.txt
    


```python
csv_files = [
    "C:/Users/paha3/Desktop/Python/nasdaqetfs.csv",
    "C:/Users/paha3/Desktop/Python/nasdaqstocks.csv",
    "C:/Users/paha3/Desktop/Python/nyseetfs.csv",
    "C:/Users/paha3/Desktop/Python/nysestocks.csv"
]

df = pd.read_csv(csv_files[0])
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>&lt;TICKER&gt;</th>
      <th>&lt;PER&gt;</th>
      <th>&lt;DATE&gt;</th>
      <th>&lt;TIME&gt;</th>
      <th>&lt;OPEN&gt;</th>
      <th>&lt;HIGH&gt;</th>
      <th>&lt;LOW&gt;</th>
      <th>&lt;CLOSE&gt;</th>
      <th>&lt;VOL&gt;</th>
      <th>&lt;OPENINT&gt;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AADR.US</td>
      <td>D</td>
      <td>20100721</td>
      <td>000000</td>
      <td>23.1646</td>
      <td>23.1646</td>
      <td>22.7969</td>
      <td>22.7969</td>
      <td>45503.680330826</td>
      <td>0</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AADR.US</td>
      <td>D</td>
      <td>20100722</td>
      <td>000000</td>
      <td>23.4621</td>
      <td>23.4621</td>
      <td>23.1929</td>
      <td>23.3129</td>
      <td>18940.045746928</td>
      <td>0</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AADR.US</td>
      <td>D</td>
      <td>20100723</td>
      <td>000000</td>
      <td>23.5713</td>
      <td>23.5713</td>
      <td>23.1471</td>
      <td>23.3324</td>
      <td>9345.9703923893</td>
      <td>0</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AADR.US</td>
      <td>D</td>
      <td>20100726</td>
      <td>000000</td>
      <td>23.4426</td>
      <td>23.4426</td>
      <td>23.2768</td>
      <td>23.4153</td>
      <td>20422.52415713</td>
      <td>0</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AADR.US</td>
      <td>D</td>
      <td>20100727</td>
      <td>000000</td>
      <td>23.3031</td>
      <td>23.3411</td>
      <td>23.2603</td>
      <td>23.3411</td>
      <td>8882.5677358118</td>
      <td>0</td>
    </tr>
  </tbody>
</table>
</div>



### II. Columns and NaN values:
 - Removing redundant columns.
 - Removing "<", ">" signs.
 - Checking for missing(NaN) values.


```python
df.drop(["<PER>", "<TIME>", "<OPENINT>"], axis=1, inplace=True)
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>&lt;TICKER&gt;</th>
      <th>&lt;DATE&gt;</th>
      <th>&lt;OPEN&gt;</th>
      <th>&lt;HIGH&gt;</th>
      <th>&lt;LOW&gt;</th>
      <th>&lt;CLOSE&gt;</th>
      <th>&lt;VOL&gt;</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AADR.US</td>
      <td>20100721</td>
      <td>23.1646</td>
      <td>23.1646</td>
      <td>22.7969</td>
      <td>22.7969</td>
      <td>45503.680330826</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AADR.US</td>
      <td>20100722</td>
      <td>23.4621</td>
      <td>23.4621</td>
      <td>23.1929</td>
      <td>23.3129</td>
      <td>18940.045746928</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AADR.US</td>
      <td>20100723</td>
      <td>23.5713</td>
      <td>23.5713</td>
      <td>23.1471</td>
      <td>23.3324</td>
      <td>9345.9703923893</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AADR.US</td>
      <td>20100726</td>
      <td>23.4426</td>
      <td>23.4426</td>
      <td>23.2768</td>
      <td>23.4153</td>
      <td>20422.52415713</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AADR.US</td>
      <td>20100727</td>
      <td>23.3031</td>
      <td>23.3411</td>
      <td>23.2603</td>
      <td>23.3411</td>
      <td>8882.5677358118</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.columns = df.columns.str.replace("<", "").str.replace(">", "")
df.head()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TICKER</th>
      <th>DATE</th>
      <th>OPEN</th>
      <th>HIGH</th>
      <th>LOW</th>
      <th>CLOSE</th>
      <th>VOL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AADR.US</td>
      <td>20100721</td>
      <td>23.1646</td>
      <td>23.1646</td>
      <td>22.7969</td>
      <td>22.7969</td>
      <td>45503.680330826</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AADR.US</td>
      <td>20100722</td>
      <td>23.4621</td>
      <td>23.4621</td>
      <td>23.1929</td>
      <td>23.3129</td>
      <td>18940.045746928</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AADR.US</td>
      <td>20100723</td>
      <td>23.5713</td>
      <td>23.5713</td>
      <td>23.1471</td>
      <td>23.3324</td>
      <td>9345.9703923893</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AADR.US</td>
      <td>20100726</td>
      <td>23.4426</td>
      <td>23.4426</td>
      <td>23.2768</td>
      <td>23.4153</td>
      <td>20422.52415713</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AADR.US</td>
      <td>20100727</td>
      <td>23.3031</td>
      <td>23.3411</td>
      <td>23.2603</td>
      <td>23.3411</td>
      <td>8882.5677358118</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.isnull().sum()
```




    TICKER    0
    DATE      0
    OPEN      0
    HIGH      0
    LOW       0
    CLOSE     0
    VOL       0
    dtype: int64



### III. Removing row duplicates and converting datatypes:
- Displaying the rows that will be removed and performing their removal.
- Changing data type.


```python
# Context: 
# After running this code. Still I wasn't able to change datatype to float, of rows ["OPEN":]. 

duplicates_to_remove = df[df.duplicated(keep="first")]

print("Rows that will be removed:")
print(duplicates_to_remove)
```

    Rows that will be removed:
              TICKER    DATE    OPEN    HIGH    LOW    CLOSE    VOL
    6819    <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    10714   <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    14608   <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    16258   <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    18573   <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    ...          ...     ...     ...     ...    ...      ...    ...
    862423  <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    863437  <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    864397  <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    868229  <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    870317  <TICKER>  <DATE>  <OPEN>  <HIGH>  <LOW>  <CLOSE>  <VOL>
    
    [363 rows x 7 columns]
    


```python
# Context:
# I've created a first copy of a df and then implemented to it, because of the warning that
# I've encountered. Basically Python didn't know whether to change a view or a copy of a df.
# So the changes would be unpredictable.

def clean_numeric_columns(df):
    df_copy = df.copy()

    for col in df_copy.columns[2:]:
        try:
            df_copy[col] = pd.to_numeric(df_copy[col], errors="coerce")
        except ValueError as e:
            print(f"Error converting column '{col}': {e}")

    df_copy.dropna(subset=df_copy.columns[2:], inplace=True)

    return df_copy

df = clean_numeric_columns(df)
```


```python
for col in df.columns[2:]:
    max_val = df[col].max()
    min_val = df[col].min()
    print(f"Column '{col}':")
    print(f"  Maximum: {max_val}")
    print(f"  Minimum: {min_val}")
```

    Column 'OPEN':
      Maximum: 494372.75
      Minimum: 0.381
    Column 'HIGH':
      Maximum: 499164.5
      Minimum: 0.38545
    Column 'LOW':
      Maximum: 468816.5
      Minimum: 0.3533
    Column 'CLOSE':
      Maximum: 472930.75
      Minimum: 0.37795
    Column 'VOL':
      Maximum: 700105227.85577
      Minimum: 0.0
    


```python
for col in df.columns[2:]:
    try:
        df[col] = df[col].astype("float64")
    except ValueError as e:
        print(f"Error converting column '{col}': {e}")
```


```python
for col in df.columns[1:2]:
    try:
        df[col] = df[col].astype("datetime64[ns]")
    except ValueError as e:
        print(f"Error converting column '{col}': {e}")
```


```python
df.dtypes
```




    TICKER            object
    DATE      datetime64[ns]
    OPEN             float64
    HIGH             float64
    LOW              float64
    CLOSE            float64
    VOL              float64
    dtype: object




```python
for col in df.columns[2:]:
    max_val = df[col].max()
    min_val = df[col].min()
    print(f"Column '{col}':")
    print(f"  Maximum: {max_val}")
    print(f"  Minimum: {min_val}")
```

    Column 'OPEN':
      Maximum: 494372.75
      Minimum: 0.381
    Column 'HIGH':
      Maximum: 499164.5
      Minimum: 0.38545
    Column 'LOW':
      Maximum: 468816.5
      Minimum: 0.3533
    Column 'CLOSE':
      Maximum: 472930.75
      Minimum: 0.37795
    Column 'VOL':
      Maximum: 700105227.85577
      Minimum: 0.0
    

### IV. Searching for outliers and deviations:
- Checking for potential outliers and removing them.


```python
df.head()

```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TICKER</th>
      <th>DATE</th>
      <th>OPEN</th>
      <th>HIGH</th>
      <th>LOW</th>
      <th>CLOSE</th>
      <th>VOL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AADR.US</td>
      <td>2010-07-21</td>
      <td>23.1646</td>
      <td>23.1646</td>
      <td>22.7969</td>
      <td>22.7969</td>
      <td>45503.680331</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AADR.US</td>
      <td>2010-07-22</td>
      <td>23.4621</td>
      <td>23.4621</td>
      <td>23.1929</td>
      <td>23.3129</td>
      <td>18940.045747</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AADR.US</td>
      <td>2010-07-23</td>
      <td>23.5713</td>
      <td>23.5713</td>
      <td>23.1471</td>
      <td>23.3324</td>
      <td>9345.970392</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AADR.US</td>
      <td>2010-07-26</td>
      <td>23.4426</td>
      <td>23.4426</td>
      <td>23.2768</td>
      <td>23.4153</td>
      <td>20422.524157</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AADR.US</td>
      <td>2010-07-27</td>
      <td>23.3031</td>
      <td>23.3411</td>
      <td>23.2603</td>
      <td>23.3411</td>
      <td>8882.567736</td>
    </tr>
  </tbody>
</table>
</div>




```python
df.describe()
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>OPEN</th>
      <th>HIGH</th>
      <th>LOW</th>
      <th>CLOSE</th>
      <th>VOL</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>count</th>
      <td>870991.000000</td>
      <td>870991.000000</td>
      <td>870991.000000</td>
      <td>870991.000000</td>
      <td>8.709910e+05</td>
    </tr>
    <tr>
      <th>mean</th>
      <td>213.718304</td>
      <td>217.785461</td>
      <td>209.819544</td>
      <td>213.384755</td>
      <td>1.417853e+06</td>
    </tr>
    <tr>
      <th>std</th>
      <td>6075.720403</td>
      <td>6225.054927</td>
      <td>5933.147875</td>
      <td>6061.339488</td>
      <td>1.075446e+07</td>
    </tr>
    <tr>
      <th>min</th>
      <td>0.381000</td>
      <td>0.385450</td>
      <td>0.353300</td>
      <td>0.377950</td>
      <td>0.000000e+00</td>
    </tr>
    <tr>
      <th>25%</th>
      <td>22.020400</td>
      <td>22.130350</td>
      <td>21.899700</td>
      <td>22.016900</td>
      <td>6.755000e+03</td>
    </tr>
    <tr>
      <th>50%</th>
      <td>33.111600</td>
      <td>33.289000</td>
      <td>32.906200</td>
      <td>33.099600</td>
      <td>3.428991e+04</td>
    </tr>
    <tr>
      <th>75%</th>
      <td>51.580000</td>
      <td>51.828300</td>
      <td>51.320000</td>
      <td>51.564300</td>
      <td>1.963842e+05</td>
    </tr>
    <tr>
      <th>max</th>
      <td>494372.750000</td>
      <td>499164.500000</td>
      <td>468816.500000</td>
      <td>472930.750000</td>
      <td>7.001052e+08</td>
    </tr>
  </tbody>
</table>
</div>




```python
df = df.sort_values(by=["TICKER", "DATE"])


df = df.assign(DAILY_RETURN=df.groupby("TICKER")["CLOSE"].pct_change())
df["ABS_DAILY_RETURN"] = df["DAILY_RETURN"].abs()

topb_10 = df["DAILY_RETURN"].nlargest(10)
tops_10 = df["DAILY_RETURN"].nsmallest(10)
print(topb_10)
print(tops_10)
```

    245417    0.494235
    28551     0.489117
    272135    0.381943
    548783    0.333933
    759142    0.327490
    207476    0.297563
    759140    0.276486
    234863    0.273844
    776248    0.269884
    776255    0.222908
    Name: DAILY_RETURN, dtype: float64
    776249   -0.344652
    245418   -0.332622
    28552    -0.324570
    602013   -0.311634
    582497   -0.286751
    759141   -0.283556
    776247   -0.274084
    272134   -0.272949
    643152   -0.251901
    225665   -0.236436
    Name: DAILY_RETURN, dtype: float64
    


```python
def replace_outliers(group):
    for i in range(len(group) - 1):
        if (group.iloc[i]["ABS_DAILY_RETURN"] > 0.2 and group.iloc[i + 1]["ABS_DAILY_RETURN"] > 0.15):
            avg_value = (group.iloc[i - 1]["CLOSE"] + group.iloc[i + 1]["CLOSE"]) / 2
            group.at[group.index[i], "CLOSE"] = avg_value
    return group

# Apply the function to each 'TICKER' group
df = df.groupby("TICKER", group_keys=False).apply(replace_outliers)
```


```python
df = df.sort_values(by=["TICKER", "DATE"])
df = df.assign(DAILY_RETURN=df.groupby("TICKER")["CLOSE"].pct_change())


topb_10 = df["DAILY_RETURN"].nlargest(10)
tops_10 = df["DAILY_RETURN"].nsmallest(10)
print(topb_10)
print(tops_10)
```

    548783    0.333933
    207476    0.297563
    234863    0.273844
    776255    0.222908
    47470     0.219403
    776920    0.218750
    136033    0.216915
    780590    0.212153
    728678    0.209774
    501889    0.209373
    Name: DAILY_RETURN, dtype: float64
    602013   -0.311634
    643152   -0.251901
    761277   -0.231284
    759148   -0.225247
    211230   -0.223304
    759813   -0.220142
    274022   -0.219470
    759157   -0.210158
    211228   -0.206475
    43126    -0.196629
    Name: DAILY_RETURN, dtype: float64
    

Taking inefficient code for "replace_outliers(group)" function, making it work for less than an eternity and making it easily replicable for any column.


```python
"""
def replace_outliers(group):
    for i in range(len(group) - 1):
        if (group.iloc[i]["ABS_DAILY_RETURN"] > 0.2 and group.iloc[i + 1]["ABS_DAILY_RETURN"] > 0.15):
            avg_value = (group.iloc[i - 1]["CLOSE"] + group.iloc[i + 1]["CLOSE"]) / 2
            group.at[group.index[i], "CLOSE"] = avg_value
    return group

# Apply the function to each '<TICKER>' group
df = df.groupby("TICKER", group_keys=False).apply(replace_outliers)
"""

df["ABS_DAILY_RETURN"] = df["DAILY_RETURN"].abs()

mask1 = (df["ABS_DAILY_RETURN"] > 0.2) & (df["ABS_DAILY_RETURN"].shift(-1) > 0.15)
mask2 = (df["ABS_DAILY_RETURN"] > 0.2) & (df["ABS_DAILY_RETURN"].shift(1) > 0.15)

df["AVG_CLOSE"] = (df["CLOSE"].shift(-1) + df["CLOSE"].shift(1)) / 2
df["AVG_VALUE"] = df["AVG_VALUE"].round(4)

df.loc[mask1 | mask2, "CLOSE"] = df["AVG_CLOSE"]
df.drop(["ABS_DAILY_RETURN", "AVG_CLOSE"], axis=1, inplace=True)
```


```python
df = df.sort_values(by=["TICKER", "DATE"])
df = df.assign(DAILY_RETURN=df.groupby("TICKER")["CLOSE"].pct_change())


topb_10 = df["DAILY_RETURN"].nlargest(10)
tops_10 = df["DAILY_RETURN"].nsmallest(10)
print(topb_10)
print(tops_10)
```

    548783    0.333933
    207476    0.297563
    234863    0.273844
    776255    0.222908
    47470     0.219403
    776920    0.218750
    136033    0.216915
    780590    0.212153
    728678    0.209774
    501889    0.209373
    Name: DAILY_RETURN, dtype: float64
    602013   -0.311634
    643152   -0.251901
    761277   -0.231284
    759148   -0.225247
    211230   -0.223304
    759813   -0.220142
    274022   -0.219470
    759157   -0.210158
    211228   -0.206475
    43126    -0.196629
    Name: DAILY_RETURN, dtype: float64
    


```python
def remove_outliers(df, check_column, column1="TICKER", column2="DATE"):

    df = df.sort_values(by=[column1, column2])
    df = df.assign(DAILY_CHANGE=df.groupby(column1)[check_column].pct_change().abs())

    mask1 = (df["DAILY_CHANGE"] > 0.2) & (df["DAILY_CHANGE"].shift(-1) > 0.15)
    mask2 = (df["DAILY_CHANGE"] > 0.2) & (df["DAILY_CHANGE"].shift(1) > 0.15)

    df["AVG_VALUE"] = (df[check_column].shift(-1) + df[check_column].shift(1)) / 2

    df.loc[mask1 | mask2, check_column] = df["AVG_VALUE"]
    df.drop(["DAILY_CHANGE", "AVG_VALUE"], axis=1, inplace=True)

    return df
```


```python
remove_outliers(df, "CLOSE")
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>TICKER</th>
      <th>DATE</th>
      <th>OPEN</th>
      <th>HIGH</th>
      <th>LOW</th>
      <th>CLOSE</th>
      <th>VOL</th>
      <th>DAILY_RETURN</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>AADR.US</td>
      <td>2010-07-21</td>
      <td>23.1646</td>
      <td>23.1646</td>
      <td>22.7969</td>
      <td>22.7969</td>
      <td>45503.680331</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>AADR.US</td>
      <td>2010-07-22</td>
      <td>23.4621</td>
      <td>23.4621</td>
      <td>23.1929</td>
      <td>23.3129</td>
      <td>18940.045747</td>
      <td>0.022635</td>
    </tr>
    <tr>
      <th>2</th>
      <td>AADR.US</td>
      <td>2010-07-23</td>
      <td>23.5713</td>
      <td>23.5713</td>
      <td>23.1471</td>
      <td>23.3324</td>
      <td>9345.970392</td>
      <td>0.000836</td>
    </tr>
    <tr>
      <th>3</th>
      <td>AADR.US</td>
      <td>2010-07-26</td>
      <td>23.4426</td>
      <td>23.4426</td>
      <td>23.2768</td>
      <td>23.4153</td>
      <td>20422.524157</td>
      <td>0.003553</td>
    </tr>
    <tr>
      <th>4</th>
      <td>AADR.US</td>
      <td>2010-07-27</td>
      <td>23.3031</td>
      <td>23.3411</td>
      <td>23.2603</td>
      <td>23.3411</td>
      <td>8882.567736</td>
      <td>-0.003169</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>871350</th>
      <td>YLDE.US</td>
      <td>2023-09-11</td>
      <td>42.2200</td>
      <td>42.2200</td>
      <td>42.0600</td>
      <td>42.1025</td>
      <td>2235.000000</td>
      <td>0.003145</td>
    </tr>
    <tr>
      <th>871351</th>
      <td>YLDE.US</td>
      <td>2023-09-12</td>
      <td>42.1300</td>
      <td>42.1300</td>
      <td>42.0150</td>
      <td>42.0150</td>
      <td>1534.000000</td>
      <td>-0.002078</td>
    </tr>
    <tr>
      <th>871352</th>
      <td>YLDE.US</td>
      <td>2023-09-13</td>
      <td>42.0900</td>
      <td>42.1100</td>
      <td>42.0401</td>
      <td>42.0546</td>
      <td>1200.000000</td>
      <td>0.000943</td>
    </tr>
    <tr>
      <th>871353</th>
      <td>YLDE.US</td>
      <td>2023-09-14</td>
      <td>42.4050</td>
      <td>42.5600</td>
      <td>42.4050</td>
      <td>42.4800</td>
      <td>1160.000000</td>
      <td>0.010115</td>
    </tr>
    <tr>
      <th>871354</th>
      <td>YLDE.US</td>
      <td>2023-09-15</td>
      <td>42.3500</td>
      <td>42.3500</td>
      <td>42.2200</td>
      <td>42.2300</td>
      <td>3582.000000</td>
      <td>-0.005885</td>
    </tr>
  </tbody>
</table>
<p>870991 rows × 8 columns</p>
</div>



## 2. Performing data cleaning process:
 - I changed any data greater than 0.9 to 0 for "DAILY_RETURN" column in order to remove incorrect changes from reversed stock splits.
 - I wasn't sure how to clean data in "VOL" column. Just the pure amount of variations within this column makes it really hard to do. So it might contain invalid data.
 - Columns: "OPEN", "HIGH", "LOW", "CLOSE" were simply cleaned by checking if in one day change was greater than 20% and on the next by -15%. It is unusual to see such fluctuations with one day, especially on big stock markets like NASDAQ and NYSE. They'd rather stick to the trend that they,re following. Exact numbers might need work to look for the most optimal values.
 - I was short on time and I haven't sorted "TICKER" column. If i were to sort it, I would check it like so: if ticker[i] != ticker[i-1] and ticker[i-1] == ticker[i+1]: ticker[i] = ticker[i-1].
 If ticker[i] is between two different tickers then I would try to match it by checking other columns. Whether this row matches more with ticker[i-1] or ticker[i+1] by proportions.
 - The next thing I would to is looking for any negative numbers in all columns except "DAILY_RETURN" and replace them.

### I. Combining all what I did in preparation process and defining functions.


```python
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

```

### II. Performing process on all files that I want to add to the database.


```python
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
```

## 3. Creating tables, loading data.
 - Dispersion in data in these columns is huge. One of the things that I would do next to make storing data more efficient is adding more tables to database schema to sort this data.
 Maybe by year, sector or something else to decrease redundancy.
 - **ticker = varchar(9) ==> [2-7] + "." + [1-3] == 11 characters**
!!! If implementing other stock data with different ticker rules it might require adjustment.!!!

 - **numeric == (17, 4) for open to close ==> Some stocks contain absurdly huge values. Mainly from companies that went bancrupt. There should be a first place to look for improvement and isolate bancrupt stocks.**

 - **numeric == (16, 6) for vol ==> Highest volume I've found was a number of size 10^10. On the other hand 6 decimal points are used due to small trafic for some stocks. For big stocks it feels a bit redundant.**

 - **numeric == (7, 6) for daily_return ==> 1 is equal to 100% so there is no point to store any bigger number for big stock market like this.**
!!! If implementing other stock data from startup stock market it may need adjustment in rare cases.!!!

### I. Creating tables and choosing data types.


```python
db_params = {
    "database" : "stocks",
    "user"     : "postgres",
    "password" : "qwerQWER",
    "host"     : "localhost",
    "port"     : '5433'
}

conn = psycopg2.connect(**db_params)
conn.close()

def transaction_commit(transaction_commit):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(transaction_commit)
    conn.commit()
    conn.close()

def transaction_block(query):
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    cur.execute(query)
    result = cur.fetchall()
    conn.commit()
    conn.close()

    return result
```


```python
nasdaq_stock_table = """
    CREATE TABLE nasdaq_stocks
    (
        id            serial PRIMARY KEY,
        ticker        varchar(11),
        date          date, 
        open          numeric(17, 4),
        high          numeric(17, 4),
        low           numeric(17, 4),
        close         numeric(17, 4),
        daily_return  numeric(7, 6),
        volume        numeric(16, 6)
    );
"""


nasdaq_etf_table = """
    CREATE TABLE nasdaq_etf
    (
        id            serial PRIMARY KEY,
        ticker        varchar(11),
        date          date, 
        open          numeric(17, 4),
        high          numeric(17, 4),
        low           numeric(17, 4),
        close         numeric(17, 4),
        daily_return  numeric(7, 6),
        volume        numeric(16, 6)
    );
"""


nyse_stock_table = """
    CREATE TABLE nyse_stocks
    (
        id            serial PRIMARY KEY,
        ticker        varchar(11),
        date          date, 
        open          numeric(17, 4),
        high          numeric(17, 4),
        low           numeric(17, 4),
        close         numeric(17, 4),
        daily_return  numeric(7, 6),
        volume        numeric(16, 6)
    );
"""


nyse_etf_table = """
    CREATE TABLE nyse_etf
    (
        id            serial PRIMARY KEY,
        ticker        varchar(11),
        date          date, 
        open          numeric(17, 4),
        high          numeric(17, 4),
        low           numeric(17, 4),
        close         numeric(17, 4),
        daily_return  numeric(7, 6),
        volume        numeric(16, 6)
    );
"""

transaction_commit(nasdaq_stock_table)
transaction_commit(nyse_stock_table)
transaction_commit(nasdaq_etf_table)
transaction_commit(nyse_etf_table)
```

### II. Loading data to database.


```python
csv_files = [
    "C:/Users/paha3/Desktop/Python/nasdaqetfs.csv",
    "C:/Users/paha3/Desktop/Python/nasdaqstocks.csv",
    "C:/Users/paha3/Desktop/Python/nyseetfs.csv",
    "C:/Users/paha3/Desktop/Python/nysestocks.csv"
]

table_names = [
    "nasdaq_etf",
    "nasdaq_stocks",
    "nyse_etf",
    "nyse_stocks"
]


try:
    connection = psycopg2.connect(**db_params)
    cursor = connection.cursor()

    for i, csv_file in enumerate(csv_files):
        table_name = table_names[i]
    
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  

            data_buffer = StringIO()
            data_writer = csv.writer(data_buffer)
            
            for row in reader:

                reordered_row = [row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7]]
                
                data_writer.writerow(reordered_row)
            

            data_buffer.seek(0)
            
 
            columns = ['ticker', 'date', 'open', 'high', 'low', 'close', 'daily_return', 'volume',]
            cursor.copy_expert(f"COPY {table_name} ({', '.join(columns)}) FROM stdin WITH CSV", data_buffer)

        connection.commit()

    cursor.close()
    connection.close()

    print("Data loaded successfully.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
```

    Data loaded successfully.
    

# 2. Ploting data.

Displaying data of companies with the highest daily_return in january 2023 and limit it to 15 entries.


```python
query = """ 
WITH all_stocks AS (
    SELECT ticker, date, daily_return
    FROM nasdaq_stocks
    WHERE date >= '2023-01-01' AND date <= '2023-01-31'
    UNION ALL
    SELECT ticker, date, daily_return
    FROM nasdaq_etf
    WHERE date >= '2023-01-01' AND date <= '2023-01-31'
    UNION ALL
    SELECT ticker, date, daily_return
    FROM nyse_stocks
    WHERE date >= '2023-01-01' AND date <= '2023-01-31'
    UNION ALL
    SELECT ticker, date, daily_return
    FROM nyse_etf
    WHERE date >= '2023-01-01' AND date <= '2023-01-31'
)
SELECT ticker, date, daily_return
FROM all_stocks
WHERE date >= '2023-01-01' AND date <= '2023-01-31'
ORDER BY daily_return DESC
LIMIT 15;

"""


result = transaction_block(query)
headers = ["Ticker", "Start Date", "End Date"]
print(tabulate(result, headers, tablefmt="pretty"))
```

    +------------+------------+----------+
    |   Ticker   | Start Date | End Date |
    +------------+------------+----------+
    |  IXAQW.US  | 2023-01-04 | 0.884058 |
    |  JAQCW.US  | 2023-01-13 | 0.884000 |
    |  GMBL.US   | 2023-01-24 | 0.880952 |
    |  AIMAW.US  | 2023-01-06 | 0.880184 |
    |  SQLLW.US  | 2023-01-04 | 0.877246 |
    |  VHNAW.US  | 2023-01-11 | 0.873786 |
    |  THCPW.US  | 2023-01-06 | 0.836471 |
    |  FIACW.US  | 2023-01-27 | 0.830283 |
    |  IXAQW.US  | 2023-01-03 | 0.827815 |
    |  HCMAW.US  | 2023-01-30 | 0.823529 |
    |  MMVWW.US  | 2023-01-06 | 0.818182 |
    |  CREXW.US  | 2023-01-05 | 0.813953 |
    | LOCC-WS.US | 2023-01-27 | 0.812987 |
    |  SHUAW.US  | 2023-01-18 | 0.805447 |
    |  GMVDF.US  | 2023-01-30 | 0.803333 |
    +------------+------------+----------+
    

Displaying days with highest daily return for Apple stock.


```python
query = """
SELECT date, daily_return
FROM nasdaq_stocks
WHERE ticker = 'AAPL.US'
ORDER BY daily_return DESC
LIMIT 15;
"""

result = transaction_block(query)
headers = ["Date", "Daily Return"]
print(tabulate(result, headers, tablefmt="pretty"))
```

    +------------+--------------+
    |    Date    | Daily Return |
    +------------+--------------+
    | 1997-08-06 |   0.332533   |
    | 1996-07-18 |   0.237234   |
    | 1998-01-02 |   0.237219   |
    | 1998-01-06 |   0.193173   |
    | 1993-10-15 |   0.188229   |
    | 1987-10-29 |   0.179315   |
    | 1987-10-21 |   0.173787   |
    | 1997-07-11 |   0.145043   |
    | 1999-10-14 |   0.143204   |
    | 1998-10-09 |   0.139042   |
    | 2008-10-13 |   0.138831   |
    | 2000-03-01 |   0.136411   |
    | 2004-10-14 |   0.131279   |
    | 2001-04-19 |   0.129153   |
    | 2008-11-24 |   0.125333   |
    +------------+--------------+
    
