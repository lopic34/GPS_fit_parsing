# GPS_fit_files_parsing.py

This script automatically processes and renames a batch of `.fit` files (GPS activity files, typically from Garmin, Suunto, or similar devices) based on their content, extracting key information such as sport type, distance, and activity start date.

## Features
- Scans all `.fit` files in the current folder.
- Extracts session and event information (sport, sub-sport, total distance, start timestamp).
- Renames each file using the format:
  `YYYY-MM-DD_HHhMM_<sport or sub-sport>_<distance>km.fit`
- Translates the sport name to French (can be customized)
- Moves processed files to a `done/` subfolder.
- Handles parsing or renaming errors by prefixing the file with `error_`.

## Example Output Files
```
2022-04-05_18h24_velo_11km.fit
2022-04-05_08h57_velo_11km.fit
2022-04-04_15h28_roller_10km.fit
2022-04-02_15h12_marche_3km.fit
2022-03-30_18h43_velo_9km.fit
2022-03-30_08h57_velo_11km.fit
2022-03-29_18h38_velo_6km.fit
```

## Example of logs
```
Processing file: 3181129719.fit
Start Event Timestamp (RAW):  2020-01-05 11:44:56
SPORT:  inline_skating       /      SUB-SPORT:  0
Total_distance_km:  7
File exported to: done/2020-01-05_12h44_roller_7km.fit
################################################################

Processing file: 3181129179.fit
Start Event Timestamp (RAW):  2020-01-05 14:19:14
SPORT:  inline_skating       /      SUB-SPORT:  0
Total_distance_km:  8
File exported to: done/2020-01-05_15h19_roller_8km.fit
################################################################

Processing file: 3150854002.fit
Start Event Timestamp (RAW):  2019-12-26 17:26:59
SPORT:  cycling       /      SUB-SPORT:  0
Total_distance_km:  2
File exported to: done/2019-12-26_18h26_velo_2km.fit
################################################################
```

## Requirements
- Python 3.x
- Python modules:
  - `fitparse`
  - `pytz`
  - `zipfile`
  - `shutil`

Install dependencies with:
```bash
pip install -r requirements.txt
```
or
```bash
pip install fitparse pytz
```

## Usage
Place your `.fit` files in the same folder as the script, then run:
```bash
python3 GPS_fit_files_parsing.py
```

Processed files will be moved to the `done/` folder with a descriptive name.
If an error occurs, the file will be renamed with the `error_` prefix.

## Customization
The script translates some sport and sub-sport names to French for readability.
You can modify or add replacements in the `sport` and `subsport` variables as needed.
