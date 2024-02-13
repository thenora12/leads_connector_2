from django.contrib import admin
from .models_board import WorkSpaceTrello

from .models_card import *

admin.site.register(CardTrello)

admin.site.register(WorkSpaceTrello)
