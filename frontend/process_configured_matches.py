# frontend/process_configured_matches.py
"""Page to review and edit preprocessed item files using NiceGUI."""

from nicegui import ui
from services import file_processing, utils
from config import paths


def process_configured_matches_page() -> None:
    """Display an editable view of a preprocessed file."""
    ui.label("Process Configured Matches")

    preprocessed_files = file_processing.list_preprocessed_files()
    if not preprocessed_files:
        ui.label("No preprocessed files found in Newfiletemp.")
        return

    file_select = ui.select(preprocessed_files)
    table_container = ui.element()

    def load_file() -> None:
        df = file_processing.read_preprocessed_file(file_select.value)
        for col in ["ITEM_NO", "DESCR", "ITEM_VEND_NO", "CATEG_COD", "SUBCAT_COD", "ACCT_COD"]:
            if col in df.columns:
                df[col] = df[col].astype(str).fillna("")

        table_container.clear()
        grid = table_container.aggrid.from_pandas(df, options={"editable": True})

        def save_changes() -> None:
            edited_df = grid.get_dataframe()
            updated_filename = f"updated_{file_select.value}"
            file_processing.save_preprocessed_file(edited_df, updated_filename)
            required_cols = {"ITEM_NO", "PRC_1", "PRC_2"}
            if required_cols.issubset(edited_df.columns):
                price_df = edited_df[["ITEM_NO", "PRC_1", "PRC_2"]].copy()
                price_df.insert(1, "LOC_ID", "*")
                price_df.insert(2, "DIM_1_UPR", "*")
                price_df.insert(3, "DIM_2_UPR", "*")
                price_df.insert(4, "DIM_3_UPR", "*")
                price_df = price_df[
                    [
                        "ITEM_NO",
                        "LOC_ID",
                        "DIM_1_UPR",
                        "DIM_2_UPR",
                        "DIM_3_UPR",
                        "PRC_1",
                        "PRC_2",
                    ]
                ]
                price_filename = f"price_{updated_filename}"
                file_processing.save_preprocessed_file(price_df, price_filename)
            ui.notify("Changes saved. You can now save the new files.")

        def save_new_files() -> None:
            updated_filename = f"updated_{file_select.value}"
            price_filename = f"price_{updated_filename}"
            file_processing.copy_to_processed_new(updated_filename)
            file_processing.copy_to_processed_new(price_filename)
            ui.notify("Files saved to ProcessedNew.")

        ui.button("Save Changes", on_click=save_changes)
        ui.button("Save new Files", on_click=save_new_files)

    file_select.on("change", load_file)
    file_select.value = preprocessed_files[0]
    load_file()
