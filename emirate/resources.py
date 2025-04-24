from import_export import resources
from .models import EmiratesTangermed, Tac

class EmiratesTangermedResource(resources.ModelResource):
    class Meta:
        model = EmiratesTangermed
        export_order = ('date', 'heure_prelevement', 'administration', 'cellule1', 'cellule2', 'mezannine', 'tgbt')
        # Assure que les données exportées sont dans le bon ordre

class TacResource(resources.ModelResource):
    class Meta:
        model = Tac
        export_order = ('date', 'heure_prelevement', 'q1_clim_hvac', 'q2_local_de_charge', 'q7_eclairage_z1', 'q8_admin', 'q9_eclairage_z2', 'q10_eclairage_z3', 'tgbt')
        # Assure que les données exportées sont dans le bon ordre
