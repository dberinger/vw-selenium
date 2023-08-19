import gspread


class SheetBots:
    def __init__(self, credentials_path: str):
        self.service_acc = gspread.service_account(filename=credentials_path)
        self.spreadsheet = ""
        self.sheet = ""

    def set_sheet(self, spreadsheet_id: str, sheet_name: str):
        self.spreadsheet = spreadsheet_id
        self.sheet = sheet_name

    def open_sheet(self):
        self.service_acc.open_by_key(self.spreadsheet).worksheet(self.sheet)
