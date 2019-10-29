from django.contrib import admin
from simulation.models import Simulation
# Register your models here.


class SimulationAdmin(admin.ModelAdmin):
    pass


admin.site.register(Simulation, SimulationAdmin)