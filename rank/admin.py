from django.contrib import admin
from .models import User, Problem, Relationship

# Register your models here.
admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Relationship)

