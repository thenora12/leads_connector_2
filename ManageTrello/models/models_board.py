from django.db import models

class WorkSpaceTrello(models.Model):
    name = models.CharField(max_length=200)
    id_workspace = models.CharField(max_length=200, blank=True)  # ID unique de l'espace de travail dans Trello
    api_key = models.CharField(max_length=200, blank=True)  # ID unique de l'espace de travail dans Trello
    secret = models.CharField(max_length=200, blank=True)  # ID unique de l'espace de travail dans Trello

class TableTrello(models.Model):
    workspace = models.ForeignKey(WorkSpaceTrello, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    id_table = models.CharField(max_length=200, blank=True)  # ID unique du tableau dans Trello

class ListTrello(models.Model):
    STATUS_CHOICES = [
        ('nouvelle_entree', 'Nouvelle entrée'),
        ('en_attente_de_saisie', 'En attente de saisie'),
        ('confirme', 'Confirmé'),
        ('a_retraiter', 'À retraiter'),
        ('injoignable', 'Injoignable'),
        ('a_relancer', 'À relancer'),
        ('rendez_vous_fixe', 'Rendez-vous fixé'),
        ('communique', 'Communiqué'),
        ('a_resoudre', 'À résoudre'),
        ('livre', 'Livré'),
        ('retourne', 'Retourné'),
        ('annule', 'Annulé'),
        ('a_verifier', 'À vérifier'),
        ('non_modifiable', 'Non modifiable'),
    ]

    table = models.ForeignKey(TableTrello, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    id_list = models.CharField(max_length=200, blank=True)  # ID unique de la liste dans le tableau Trello
    role = models.CharField(max_length=50, choices=STATUS_CHOICES, default='En attente')  # Nouveau champ ajouté

class CustomFieldTrello(models.Model):
    table = models.ForeignKey(TableTrello, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    id_field = models.CharField(max_length=200, blank=True)
    field_type = models.CharField(max_length=50)  # Type de champ (texte, numéro, date, etc.)

class CustomFieldOptionTrello(models.Model):
    custom_field = models.ForeignKey(CustomFieldTrello, related_name='options', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    option_id = models.CharField(max_length=200, blank=True)  # ID de l'option dans Trello
    color = models.CharField(max_length=200, blank=True)  # ID de l'option dans Trello

class LabelTrello(models.Model):
    table = models.ForeignKey(TableTrello, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    color = models.CharField(max_length=50)  # Couleur de l'étiquette




