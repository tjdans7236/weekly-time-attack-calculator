# Time Trial Record Parser

This project is to help parse the weekly time attack records for KartRider Rush+ club Synergy.

## Using the parser

1. Have `python>=3.7` installed on your computer
1. Clone the repo to a location on your computer with `git clone https://github.com/r-luo/weekly-time-attack-calculator.git`
1. Install dependency `pyyaml` either by running `python -m pip install pyyaml` or `python -m pip install -r requirements.txt`
1. Add the `name_to_webhook.yml` file. 
    - in this file, the keys are names that will be used in the time record yaml file as keys to time trial records
    - each key should have a unique string value which is the Discord webhook of the corresponding member
1. Add the time trial records to the data folder following the format of `data/time_record_example.yml`
1. Execute `python parse_time.py <name_to_time_record_file>`
    - For example, `python parse_time.py time_record_example.yml`
1. Output will be generated as a json file in the `output` folder, with the same name as the input file but `yml` suffix changed to `json`