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
Processing file: 2-sports-site-9565535999999605792.fit
SPORT:  running
SUB-SPORT:  0
Start Event Timestamp (RAW):  2025-02-03 11:25:17
total_distance_km:  8
File moved to: done/2025-02-03_12h25_running_8km.fit
###########################################

Processing file: 32-sports-site-956553599999960b5a4ebcf.fit
SPORT:  inline_skating
SUB-SPORT:  0
Start Event Timestamp (RAW):  2018-11-11 11:14:57
total_distance_km:  23
File moved to: done/2018-11-11_12h14_roller_23km.fit
###########################################

Processing file: 25-sports-site-95655359999996001714c77.fit
SPORT:  running
SUB-SPORT:  0
Start Event Timestamp (RAW):  2020-06-14 16:47:41
total_distance_km:  9
File moved to: done/2020-06-14_18h47_running_9km.fit
###########################################
```

## Requirements
- Python 3.x
- Python modules:
  - `fitparse`
  - `pytz`

Install dependencies with:
```bash
pip install fitparse pytz
```
or
```bash
pip install -r requirements.txt
```

## Usage
Place your `.fit` files in the same folder as the script, then run:
```bash
python GPS_fit_files_parsing.py
```

Processed files will be moved to the `done/` folder with a descriptive name.
If an error occurs, the file will be renamed with the `error_` prefix.

## Customization
The script translates some sport and sub-sport names to French for readability.
You can modify or add replacements in the `sport` and `subsport` variables as needed.
