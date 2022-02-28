# -*- coding: utf-8 -*-
from django.db import models

class dp(models.Model):
    X = models.DecimalField(max_digits=6,decimal_places=4)
    def __str__(self):
        return self.X

class successcount(models.Model):
    contador = models.CharField(max_length=200)
    def __str__(self):
        return self.contador