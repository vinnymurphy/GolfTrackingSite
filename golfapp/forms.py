from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import NON_FIELD_ERRORS # Allow the use of a custom error message 

from .models import GolferUser, Hole, Tee, Course, TeeColor, Score, CoursePicture

class GolferUserCreationForm(UserCreationForm):
    class Meta:
        model = GolferUser
        fields = ('username', 'email', 'gender')

class GolferUserChangeForm(UserChangeForm):
    class Meta:
        model = GolferUser
        fields = ('username', 'email', 'gender')

class HoleForm(ModelForm):
    class Meta:
        model = Hole
        fields = ('number', 'name', 'course', 'mens_par', 'womens_par')
        # Course is set automaticaly 
        widgets = {
            'course': forms.HiddenInput,
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "The %(model_name)s already exists for this course.",
            }
        }

class TeeColorForm(ModelForm):
    class Meta:
        model = TeeColor
        fields = ('color',)
        widgets = {
        # Course is set automaticaly 
            'course': forms.HiddenInput,
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "The %(model_name)s already exists for this course.",
            }
        }

class TeeForm(ModelForm):
    class Meta:
        model = Tee
        fields = ('color', 'yards', 'hole')
        widgets = {
        # Hole is set automaticaly 
            'hole': forms.HiddenInput,
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "The %(model_name)s already exists for this course.",
            }
        }

class ScoreForm(ModelForm):
    class Meta:
        model = Score
        fields = ('round', 'hole', 'strokes')
        widgets = {
        # Hole and Round are set automaticaly 
            'hole': forms.HiddenInput,
            'round': forms.HiddenInput,
        }
        error_messages = {
            NON_FIELD_ERRORS: {
                'unique_together': "The %(model_name)s already exists for this course.",
            }
        }

class CoursePictureForm(ModelForm):
    class Meta:
        model = CoursePicture
        fields = ('picture', 'course',)
        # Course is set automaticaly 
        widgets = {
            'course': forms.HiddenInput,
        }