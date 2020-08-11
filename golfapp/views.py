from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.views.generic import ListView, UpdateView, DeleteView, DetailView
from datetime import datetime, time, date

from django.db.models import Sum

from .forms import GolferUserCreationForm, HoleForm, TeeForm, TeeColorForm, ScoreForm, CoursePictureForm
from .models import Course, TeeColor, Hole, Tee, Round, Score, CoursePicture


# Create your views here.

# Round for logged in user are displayed on the home page 
class HomeView(TemplateView):
    template_name = 'home.html'
    
    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        if (self.request.user.is_active):
            context['rounds'] = Round.objects.select_related().filter(created_by=self.request.user)
        return context 

# Create a new GolferUser
class SignUpView(CreateView):
    form_class = GolferUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'

# Display a list of the courses in the database
class CourseList(ListView):
    model = Course
    context_object_name = 'course_list'

# Course Model C.R.U.D.
class CourseCreate(CreateView):
    model = Course
    fields = ['name', 'city', 'state', 'tee_colors']
    success_url = reverse_lazy('course_list')

# The course page will display information about the holes and tees of a course. 
class CourseDetail(DetailView):
    model = Course
    context_object_name = 'course'

    # Get the holes associated with the course and the tees associated with the holes
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['holes'] = Hole.objects.filter(course_id=self.object.pk).order_by('number')
        context['tees'] = Tee.objects.select_related('hole')
        context['pictures'] = CoursePicture.objects.filter(course_id=self.object.pk).order_by('created_on')
        return context

class CourseUpdate(UpdateView):
    model = Course 
    fields = ['name', 'city', 'state', 'tee_colors',]
    success_url = reverse_lazy('course_list')

class CourseDelete(DeleteView):
    model = Course 
    success_url = reverse_lazy('course_list')

# Allow the user to select the color of tees that the course has
class TeeColorCreate(CreateView):
    model = TeeColor
    form_class = TeeColorForm

    # Gets the course pk from the url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        return context

    def get_initial(self):
        initial = super(TeeColorCreate, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        return initial

    # Returns the user to the course this tee color was created for
    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

class CoursePictureCreate(CreateView):
    model = CoursePicture
    #fields = ['picture',]
    form_class = CoursePictureForm

    # Gets the course pk from the url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        return context

    # set the Holes course value to the course in context data
    def get_initial(self):
        initial = super(CoursePictureCreate, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        return initial

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(CoursePictureCreate, self).form_valid(form)

    # Returns the user to the course this hole was created for
    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

class CoursePictureDetail(DetailView):
    model = CoursePicture
    form_class = CoursePictureForm

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

# Holes currently make the user input which number the hole is. 
# In the future I want holes to be added autmatically. Hole number would increment. 
class HoleCreate(CreateView):
    model = Hole
    form_class = HoleForm

    # Gets the course pk from the url
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        return context

    # set the Holes course value to the course in context data
    def get_initial(self):
        initial = super(HoleCreate, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        return initial

    # Returns the user to the course this picture was created for
    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})
    
class CoursePictureDelete(DeleteView):
    model = CoursePicture

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        context['coursepicture'] = CoursePicture.pk
        return context

    def get_initial(self):
        initial = super(CoursePictureDelete, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        return initial

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})


# In the future I will want the Hole to be deleted off the end of the course.
# An update view will need to be added to modify the data of holes
class HoleDelete(DeleteView):
    model = Hole 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        context['hole'] = Hole.pk
        return context

    def get_initial(self):
        initial = super(HoleDelete, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        return initial

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})


class TeeCreate(CreateView):
    model = Tee
    form_class = TeeForm

    def get_initial(self):
        initial = super(TeeCreate, self).get_initial()
        initial['hole'] = self.kwargs['hole_pk']
        return initial

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

class TeeUpdate(UpdateView):
    model = Tee
    form_class = TeeForm

    def get_initial(self):
        initial = super(TeeUpdate, self).get_initial()
        initial['hole'] = self.kwargs['hole_pk']
        return initial

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

# I dont believe this view is ever used... 
#  When a user deletes a hole its tees are deleted, if a user needs to change a tees data they would update an existing one.
# Theres no real reason a user would want to manually delete a tee
class TeeDelete(DeleteView):
    model = Tee 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['hole'] = Hole.objects.get(pk=self.kwargs['hole_pk'])
        context['course'] = Course.objects.get(pk=self.kwargs['course_pk'])
        context['tee'] = Tee.pk
        return context

    def get_initial(self):
        initial = super(HoleDelete, self).get_initial()
        initial['course'] = self.kwargs['course_pk']
        initial['hole'] = self.kwargs['hole_pk']
        return initial

    def get_success_url(self, **kwargs):
        course_id = self.kwargs['course_pk']
        return reverse_lazy('course_detail', kwargs= {'pk': course_id})

# Rounds save the key of which user created the round. 
# Planned to change the success url to the newly created round instead of the round list
class RoundCreate(CreateView):
    model = Round
    fields = ['name', 'course', 'tee_color']
    success_url = reverse_lazy('home')
    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.created_by = self.request.user
        return super(RoundCreate, self).form_valid(form)

class RoundDetail(DetailView):
    model = Round
    context_object_name = 'round'

    # Score calcutlation is done by comparing the total_par to the rounds total_score
    # Planned to change this to include womens par
    # Planned to change this to automaticaly show only the score difference relevent to the user's gender
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['holes'] = Hole.objects.filter(course_id=self.object.course.pk).order_by('number')
        context['tees'] = Tee.objects.filter(color=self.object.tee_color)
        context['scores'] = Score.objects.filter(round_id=self.object.pk)
        context['total_score'] = Score.objects.filter(round_id=self.object.pk).aggregate(total_score=Sum('strokes'))
        context['total_mens_par'] = Hole.objects.filter(course_id=self.object.course.pk).aggregate(total_mens_par=Sum('mens_par'))
        context['total_womens_par'] = Hole.objects.filter(course_id=self.object.course.pk).aggregate(total_womens_par=Sum('womens_par'))
        ##context['total_par'] = Hole.objects.filter(course_id=self.object.course.pk).aggregate(total_mens_par=Sum('mens_par'))
        if (context['total_score'].get('total_score') and (context['total_mens_par'].get('total_mens_par') or context['total_womens_par'].get('total_womens_par'))):
            if (self.object.created_by.gender != 'MALE'):
                context['player_par'] = context['total_score'].get('total_score') - context['total_womens_par'].get('total_womens_par')
            else:
                context['player_par'] = context['total_score'].get('total_score') - context['total_mens_par'].get('total_mens_par')
        return context

class RoundUpdate(UpdateView):
    model = Round
    fields = ['name', 'course', 'tee_color']

    def get_success_url(self, **kwargs):
        round_id = self.kwargs['pk']
        return reverse_lazy('round_detail', kwargs= {'pk': round_id})

class RoundDelete(DeleteView):
    model = Round 
    success_url = reverse_lazy('home')

# Create a new score for the round 
class ScoreCreate(CreateView):
    model = Score
    form_class = ScoreForm

    def get_initial(self):
        initial = super(ScoreCreate, self).get_initial()
        initial['hole'] = self.kwargs['hole_pk']
        initial['round'] = self.kwargs['round_pk']
        return initial

    def get_success_url(self, **kwargs):
        round_id = self.kwargs['round_pk']
        return reverse_lazy('round_detail', kwargs= {'pk': round_id})

# Need to add update view for score model