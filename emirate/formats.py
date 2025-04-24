# formats.py
from import_export.formats.base_formats import XLSX as BaseXLSX, CSV as BaseCSV

class CustomXLSX(BaseXLSX):
    def get_title(self):
        return "Excel"

class CustomCSV(BaseCSV):
    def get_title(self):
        return "CSV"
