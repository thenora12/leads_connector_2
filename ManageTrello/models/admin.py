from django.contrib import admin
from .models_board import WorkSpaceTrello,ListTrello

from .models_card import CardTrello

admin.site.register(CardTrello)
admin.site.register(WorkSpaceTrello)
admin.site.register(ListTrello)
