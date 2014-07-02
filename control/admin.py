from django.contrib import admin
from control.models import Method
from django import forms
from django.db import models
            
class MethodAdmin(admin.ModelAdmin):
    list_display = ('Run_Type', 'Operator_Name', 'Sample_Name', 'Diameter',
                    'mass', 'pub_date')

    
admin.site.register(Method, MethodAdmin)
    


