from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import GolferUserCreationForm, GolferUserChangeForm
from .models import GolferUser, Tee, TeeColor, Course, Round

# Register your models here.
class GolferUserAdmin(UserAdmin):
    add_form = GolferUserCreationForm
    form = GolferUserChangeForm
    model = GolferUser
    list_display = ['email', 'username',]

admin.site.register(GolferUser, GolferUserAdmin)
admin.site.register(Tee)
admin.site.register(TeeColor)
admin.site.register(Course)
admin.site.register(Round)