# frontend/main_page.py
"""Main processing page implemented with NiceGUI."""

from nicegui import ui
from config import config_manager, paths
from services import file_processing, file_matching
import pandas as pd

def main_page():
    config = config_manager.load_config()

    new_items_file = config.get("newitems_file")
    if new_items_file:
        ui.label(f"New Items File: {new_items_file}")
    else:
        ui.label("No New Items File selected.")

    po_files = config.get("po_files", [])
    if po_files:
        for po in po_files:
            ui.label(f"PO File: {po}")
    else:
        ui.label("No PO Files selected.")

    table_container = ui.element()

    def start_matching() -> None:
        matched_list = []
        for po_filename in po_files:
            po_path = paths.UPLOADED_PO_DIR / po_filename
            new_items_path = paths.NEW_ITEMS_DIR / new_items_file
            matched_items = file_matching.match_items(po_path, new_items_path, config["po_qty_column"])
            output_filename = f"matched_{po_filename.replace('.xlsx', '')}.csv"
            file_processing.save_matched_items(matched_items, output_filename)
            ui.notify(f"Matched items saved to Newfiletemp/{output_filename}")
            matched_list.append(matched_items)

        if matched_list:
            matched_df = pd.concat(matched_list, ignore_index=True)
            show_table(matched_df)
        else:
            ui.notify("No matched items")

    def show_table(df: pd.DataFrame) -> None:
        table_container.clear()
        table = table_container.table.from_pandas(df, selection="multiple")

        def create_file() -> None:
            selected_rows = [df.iloc[i] for i in table.selected]
            if selected_rows:
                export_df = pd.DataFrame(selected_rows)
                output_path = file_processing.save_selected_items(export_df, new_items_file)
                ui.notify(f"Selected items saved to Newfiletemp/{output_path.name}")
                ui.navigate("/process")
            else:
                ui.notify("No items selected")

        ui.button("Create new file", on_click=create_file)

    ui.button("Start Matching", on_click=start_matching)
