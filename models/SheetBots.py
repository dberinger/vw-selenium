from __future__ import annotations
from datetime import datetime

import gspread


class SheetBots:
    def __init__(self, credentials_path: str, spreadsheet_id: str, sheet_name: str):
        self.service_acc = gspread.service_account(filename=credentials_path)
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        # wk - worksheet
        self.wk = self.open_sheet()

    def set_service_account(self, credentials_path: str):
        self.service_acc = gspread.service_account(filename=credentials_path)

    def set_sheet(self, spreadsheet_id: str, sheet_name: str):
        self.spreadsheet_id = spreadsheet_id
        self.sheet_name = sheet_name
        self.wk = self.open_sheet()

    def open_sheet(self):
        return self.service_acc.open_by_key(self.spreadsheet_id).worksheet(self.sheet_name)


class VwBot(SheetBots):
    # model name to model name in url
    model_map = {
        'Taigo': 'taigo',
        'ID.4': 'id4',
        'Tiguan': 'tiguan',
        'Arteon': 'arteon'
    }
    # mapping of cells in vw.pl Demo sheet (ID = 1WPSCNLxT1mwd09kQp_xcTVr7EMhSHTpH4P3dYyCn4Ps)
    # c - column | r - row | cr - single cell
    sheet_map = {
        'time_cr': 'B1',
        'messages_cr': 'B2',
        'human_input_range': 'A6:C100',
        'in_start_r': 6,
        'qa_start_r': 6,
        'in_monthly_c': 'B',
        'in_price_c': 'C',
        'qa_monthly_c': 'E',
        'qa_price_c': 'F',
    }

    def update_t(self):
        t = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.wk.update(self.sheet_map['time_cr'], t)

    def update_msg(self, msg: str):
        self.wk.update(self.sheet_map['messages_cr'], msg)

    def get_input(self):
        sheet_data = self.wk.get(self.sheet_map['human_input_range'])
        car_data = []

        # validate data
        for i, row in enumerate(sheet_data):
            is_valid = True
            if len(row) == 3:
                for val in row:
                    if val == '':
                        is_valid = False
                        break
            else:
                is_valid = False

            if is_valid:
                car_data.append({
                    'slug': self.model_map[row[0]],
                    'monthly': row[1].strip(),
                    'price': row[2].strip(),
                    'row': self.sheet_map['in_start_r'] + i,
                    'qa_monthly': False,
                    'qa_price': False
                })

        # clean monthly and price
        for car in car_data:
            for k in ['monthly', 'price']:
                car[k] = car[k].replace(',', '').replace(' ', '')

        return car_data

    def fill_qa(self, car_data: dict):
        for car in car_data:
            self.wk.update(self.sheet_map['qa_monthly_c'] + str(car['row']), car['qa_monthly'])
            self.wk.update(self.sheet_map['qa_price_c'] + str(car['row']), car['qa_price'])

