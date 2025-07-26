# frontend/config_page.py
"""Configuration page implemented with NiceGUI."""

from nicegui import ui
from config import config_manager, paths
from services import file_processing
import shutil

def config_page():
    config = config_manager.load_config()

    new_items_files = file_processing.list_files_in_directory(paths.NEW_ITEMS_DIR)
    po_files = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    new_items_select = ui.select(new_items_files, label="Select New Items File")
    if config.get("newitems_file") in new_items_files:
        new_items_select.value = config.get("newitems_file")

    po_select = ui.select(po_files, label="Select PO Files", multiple=True)
    po_select.value = config.get("po_files", [])

    logging_checkbox = ui.checkbox("Logging On", value=config.get("logging_on", False))

    po_qty_input = ui.input(label="PO Quantity Column Name", value=config.get("po_qty_column", "Sales Products Qty"))

    def handle_po_upload(e) -> None:
        save_path = paths.UPLOADED_PO_DIR / e.name
        with open(save_path, "wb") as f:
            shutil.copyfileobj(e.content, f)
        ui.notify(f"File {e.name} uploaded successfully!")
        po_select.options = file_processing.list_files_in_directory(paths.UPLOADED_PO_DIR)

    with ui.row():
        ui.label("Upload PO File")
        # allow only a single Excel file to be uploaded
        ui.upload(
            on_upload=handle_po_upload,
            multiple=False,
            auto_upload=True,
            file_filter="*.xlsx",
            max_files=1,
        )

    def save_configuration() -> None:
        config["newitems_file"] = new_items_select.value
        config["po_files"] = po_select.value or []
        config["logging_on"] = logging_checkbox.value
        config["po_qty_column"] = po_qty_input.value
        config_manager.save_config(config)
        ui.notify("Configuration Saved!")

    ui.button("Save Configuration", on_click=save_configuration)
