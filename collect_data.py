from datetime import datetime
from openpyxl import load_workbook
import os
import pandas as pd
import glob
import re
#set factory different model
class model_fab():
    def __init__(self,read_file,export_file):
        self.read_file = read_file
        self.export_file = export_file
        self.model_name = "FAB"
        month_list = self.get_month_abbr()
        self.rack_fields = month_list[0]
        self.server_fields = "{} Server QTY".format(month_list[0])
        self.mb_fields = "{} MB QTY".format(month_list[0])
        self.sb_fields = "{} SB QTY".format(month_list[0])
        self.col = self.get_excel_col()
        self.export_file_index = {
            "QMF":{"rack":3,"server":4,"mb":5,"sb":6,"fa":8},
            "QMN":{"rack":21,"server":22,"mb":23,"sb":24},
            "QCG":{"rack":37,"server":38,"mb":39,"sb":40}
        }
    def read_excel(self):
        model_fac = ["QMF","QMN","QCG"]
        sheet_name = pd.ExcelFile(self.read_file).sheet_names
        for fac in model_fac:
            pattern = re.compile(fr'.*{fac}.*',re.IGNORECASE)
            match_sheet = [name for name in sheet_name if pattern.match(name)]
            if not match_sheet[0]:
                print(f"not exit sheet {fac} in {self.read_file} excel")
                continue
            df = pd.read_excel(self.read_file, sheet_name=match_sheet[0])
            last_row = df.tail(1)
            #get columns name list
            columns_index  = df.columns.tolist()
            if fac == "QMF" and self.model_name == "FAB":
                fa_index = columns_index.index(self.rack_fields)
                fa_data = last_row.iloc[:,fa_index:fa_index+5]  
                self.export_to_excel(fa_data,self.export_file_index[fac]["fa"])
                last_row = df.tail(2).head(1)
            rack_index = columns_index.index(self.rack_fields)
            server_index = columns_index.index(self.server_fields)
            mb_index = columns_index.index(self.mb_fields)
            sb_index = columns_index.index(self.sb_fields)
            
            rack_data = last_row.iloc[:,rack_index:rack_index+5]
            server_data = last_row.iloc[:,server_index:server_index+5]
            mb_data = last_row.iloc[:,mb_index:mb_index+5]
            sb_data = last_row.iloc[:,sb_index:sb_index+5]
            
            self.export_to_excel(rack_data,self.export_file_index[fac]["rack"])
            self.export_to_excel(server_data,self.export_file_index[fac]["server"])
            self.export_to_excel(mb_data,self.export_file_index[fac]["mb"])
            self.export_to_excel(sb_data,self.export_file_index[fac]["sb"])

    def get_month_abbr(self):
        now = datetime.now()
        month_abbr = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
        current_month_index=now.month - 2
        export_month_index=[(current_month_index + i ) % 12 for i in range(5)]
        month_list = [month_abbr[i] for i in export_month_index]
        return month_list
    
    def get_excel_col(self):
        workbook = load_workbook(self.export_file)
        worksheet = workbook["Loading by model"]
        for cell in worksheet.iter_rows(min_row=1,max_row=1,values_only=True):
            for index, value in enumerate(cell):
                if value == self.rack_fields:
                    index = index
                    break
            if index is not None:
                break
        return index

    def export_to_excel(self,data,row):
        df = pd.DataFrame(data)
        with pd.ExcelWriter(self.export_file, mode='a', engine='openpyxl',if_sheet_exists='overlay') as writer:
            df.to_excel(writer,sheet_name='Loading by model',index=False,header=False,startrow=row-1,startcol=self.col)

class model_ama():
    pass

class model_msf():
    pass

def main():
    get_cwd = os.getcwd()
    all_files = glob.glob('*.xlsx')
    fab_pattern = re.compile(r'^fab.*\.xlsx$',re.IGNORECASE)
    ama_pattern = re.compile(r'^ama.*\.xlsx$',re.IGNORECASE)
    msf_pattern = re.compile(r'^msf.*\.xlsx$',re.IGNORECASE)
    loading_pattern = re.compile(r'.*loading.*\.xlsx$',re.IGNORECASE)
    fab_file_name = [file for file in all_files if fab_pattern.match(file) and not file.startswith('~')][0]
    ama_file_name = [file for file in all_files if ama_pattern.match(file) and not file.startswith('~')][0]
    #msf_file_name = [file for file in all_files if msf_pattern.match(file) and not file.startswith('~')][0]
    loading_file_name = [file for file in all_files if loading_pattern.match(file) and not file.startswith('~')][0]
    loading_file_path = os.path.join(get_cwd,loading_file_name)
    fab_data = model_fab(os.path.join(get_cwd,fab_file_name),loading_file_path)
    fab_data.read_excel()
    
main()
