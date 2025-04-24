from django.contrib import admin
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors
from openpyxl import Workbook
from io import BytesIO
import io
from .models import EmiratesTangermed, Tac
from .resources import EmiratesTangermedResource, TacResource
from import_export.admin import ExportActionModelAdmin
from import_export.formats.base_formats import XLSX

admin.site.site_header = "Emirates Logistics"
admin.site.site_title = "Emirates Logistics Admin"
admin.site.index_title = "Welcome to Emirates Logistics Admin"

def download_pdf(modeladmin, request, queryset):
    model_name = modeladmin.model.__name__
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_report.pdf"'
    
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer, pagesize=landscape(letter))  # Use landscape orientation
    pdf.setTitle(f'{model_name} PDF Report')

    # Define headers and data based on the model
    if model_name == 'EmiratesTangermed':
        headers = ['Date and Time', 'Heure de Prélèvement', 'Administration', 'Cellule1', 'Cellule2', 'Mezannine', 'TGBT']
        data = [headers]
        for obj in queryset:
            row = [
                obj.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
                obj.heure_prelevement,
                obj.administration,
                obj.cellule1,
                obj.cellule2,
                obj.mezannine,
                obj.tgbt,
            ]
            data.append(row)
        col_widths = [1.1*inch, 1.2*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch]
    elif model_name == 'Tac':
        headers = ['Date and Time', 'Heure de Prélèvement', 'Q1 Clim HVAC', 'Q2 Local de Charge', 'Q7 Éclairage Z1', 'Q8 Admin', 'Q9 Éclairage Z2', 'Q10 Éclairage Z3', 'TGBT']
        data = [headers]
        for obj in queryset:
            row = [
                obj.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
                obj.heure_prelevement,
                obj.q1_clim_hvac,
                obj.q2_local_de_charge,
                obj.q7_eclairage_z1,
                obj.q8_admin,
                obj.q9_eclairage_z2,
                obj.q10_eclairage_z3,
                obj.tgbt,
            ]
            data.append(row)
        col_widths = [1.1*inch, 1.2*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.0*inch, 1.1*inch]
    
    table = Table(data, colWidths=col_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
    ]))
    
    table.wrapOn(pdf, 0.5*inch, 0.5*inch)
    table.drawOn(pdf, 0.1*inch, 5.5*inch)  # Adjust the y-coordinate to fit the table on the page
    
    pdf.save()
    buffer.seek(0)
    response.write(buffer.read())
    buffer.close()
    return response


def export_to_xlsx(modeladmin, request, queryset):
    model_name = modeladmin.model.__name__
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_report.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = model_name

    if model_name == 'EmiratesTangermed':
        headers = ['Date and Time', 'Heure de Prélèvement', 'Administration', 'Cellule1', 'Cellule2', 'Mezannine', 'TGBT']
        ws.append(headers)
        for obj in queryset:
            row = [
                obj.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
                obj.heure_prelevement,
                obj.administration,
                obj.cellule1,
                obj.cellule2,
                obj.mezannine,
                obj.tgbt,
            ]
            ws.append(row)
        col_widths = [20, 18, 15, 15, 15, 15, 15]
    elif model_name == 'Tac':
        headers = ['Date and Time', 'Heure de Prélèvement', 'Q1 Clim HVAC', 'Q2 Local de Charge', 'Q7 Éclairage Z1', 'Q8 Admin', 'Q9 Éclairage Z2', 'Q10 Éclairage Z3', 'TGBT']
        ws.append(headers)
        for obj in queryset:
            row = [
                obj.date_and_time.strftime('%Y-%m-%d %H:%M:%S'),
                obj.heure_prelevement,
                obj.q1_clim_hvac,
                obj.q2_local_de_charge,
                obj.q7_eclairage_z1,
                obj.q8_admin,
                obj.q9_eclairage_z2,
                obj.q10_eclairage_z3,
                obj.tgbt,
            ]
            ws.append(row)
        col_widths = [20, 18, 15, 15, 15, 15, 15, 15, 15]

    for i, width in enumerate(col_widths, start=1):
        ws.column_dimensions[chr(64 + i)].width = width

    output = BytesIO()
    wb.save(output)
    response.write(output.getvalue())
    return response


export_to_xlsx.short_description = "Export selected to XLSX"

class CustomExportActionModelAdmin(ExportActionModelAdmin):
    def get_export_formats(self):
        # Retourne uniquement le format XLSX
        return [XLSX]

    def get_actions(self, request):
        actions = super().get_actions(request)
        # Conserver uniquement l'action 'export_to_xlsx' et supprimer les autres actions d'exportation
        actions_to_keep = ['export_to_xlsx']
        for action in list(actions.keys()):
            if 'export' in action and action not in actions_to_keep:
                del actions[action]
        return actions

@admin.register(EmiratesTangermed)
class EmiratesTangermedAdmin(CustomExportActionModelAdmin):
    resource_class = EmiratesTangermedResource
    list_display = ('date_and_time', 'heure_prelevement', 'administration', 'cellule1', 'cellule2', 'mezannine', 'tgbt')
    list_filter = ('date_and_time', 'heure_prelevement')
    search_fields = ('date_and_time', 'heure_prelevement', 'administration', 'cellule1', 'cellule2', 'mezannine', 'tgbt')
    actions = [download_pdf, export_to_xlsx]

@admin.register(Tac)
class TacAdmin(CustomExportActionModelAdmin):
    resource_class = TacResource
    list_display = ('date_and_time', 'heure_prelevement', 'q1_clim_hvac', 'q2_local_de_charge', 'q7_eclairage_z1', 'q8_admin', 'q9_eclairage_z2', 'q10_eclairage_z3', 'tgbt')
    list_filter = ('date_and_time', 'heure_prelevement')
    search_fields = ('date_and_time', 'heure_prelevement', 'q1_clim_hvac', 'q2_local_de_charge', 'q7_eclairage_z1', 'q8_admin', 'q9_eclairage_z2', 'q10_eclairage_z3', 'tgbt')
    actions = [download_pdf, export_to_xlsx]
