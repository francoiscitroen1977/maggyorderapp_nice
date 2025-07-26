# Maggys Order App

Maggys Order App is a NiceGUI application for matching product orders and preparing item files for import. The app reads purchase order (PO) spreadsheets and new item CSV files, matches items using UPC codes, and lets you review or edit the results.

## Requirements

- Python 3
- pip

## Setup

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Configure file locations**

   Edit `config/paths.py` and adjust `BASE_DIR` to point to the folder that contains your data files. The app expects these subfolders inside `BASE_DIR`:

   ```
   Docs/          # existing price spreadsheets
   New/           # new item CSV files
   Newfiletemp/   # output for matched and preprocessed files
   UploadedPO/    # PO spreadsheets
   JsonFiles/     # category, subcategory and account code JSON lists
   log/           # optional log files
   ```

   The directories will be created automatically if they do not exist.

3. **Run the app**

   ```bash
   python app.py
   ```

   The NiceGUI server will start on `http://localhost:8080`. Open this URL in your browser to use the application.

## Using the App

### 1. Configure Matching

- Open the **Configure matching** page.
- Choose a new items file and one or more PO files.
- Enter the column name that holds the PO quantity (default is `Sales Products Qty`).
- Enable **Logging On** if you want processing details saved under `log/`.
- Click **Save Configuration** to store your selections.

### 2. Pre-process Matching

- Go to **Pre-process matching** (the main page).
- Click **Start Matching** to compare the selected files. Matched rows are saved in `Newfiletemp/` with names like `matched_<PO>.csv`.
- Select any rows you wish to keep and click **Create new file**. The output will
  be saved as `preprocessed_<NewItemsFileName>` in the same folder.

### 3. Process Configured Matches

- Open the **Process configured matches** page.
- Pick one of the `preprocessed_` files.
- Edit values directly in the table. Category, subcategory, and account codes are loaded from JSON files in `JsonFiles/`.
 - Click **Save Changes** and then **Save new Files** to write the updated and price files into the `ProcessedNew` folder.

## Configuration File

Your selections are stored in `config.json`. Remove or edit this file if you need to reset the configuration.

## Logging

When logging is enabled, daily log files are created in `<BASE_DIR>/log`.
