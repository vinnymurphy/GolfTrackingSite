from datetime import datetime

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Hardcoded list of possible Tee colors to choose from. Currently used
# to set the options for the tee select fields
# Planned to change the way the select list chooses tee colors

COLOR_CHOICES = (
    ("BLACK", "Black"),
    ("BLUE", "Blue"),
    ("GOLD", "Gold"),
    ("GREEN", "Green"),
    ("RED", "Red"),
    ("WHITE", "White"),
)

# Custom User Model Golfer.

# Gender chocies are planned to be used to properly determine the
# score on a course
class GolferUser(AbstractUser):
    GENDER_CHOICES = (
        ("MALE", "Male"),
        ("FEMALE", "Female"),
    )

    gender = models.CharField(choices=GENDER_CHOICES, max_length=255)
    pass

    def __str__(self):
        return self.username


# # # # # # # # # # # # # # #
#   Course related models   #
# # # # # # # # # # # # # # #


# Course model
class Course(models.Model):
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=255)
    tee_colors = models.ManyToManyField(
        "TeeColor", blank=False, related_name="courses"
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


# Tee color model is planned to replace the hardcoded COLOR_CHOICES
class TeeColor(models.Model):
    color = models.CharField(
        choices=COLOR_CHOICES, blank=True, null=True, max_length=255
    )

    def __str__(self):
        return self.color


# Hole model. Each course can have any number of holes, typicaly in
# multiples of 9's.  9, 18, and 27 are common

# Par is different for men and women players.

# Each course "Should" only have one of each number. Some courses have
# multiple 1-9 holes. This is a possible change to make to the
# application in the future
class Hole(models.Model):
    number = models.IntegerField(unique=False)
    name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        verbose_name="Name of this hole (optional)",
    )  # Optional: Most courses do not name their holes
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="holes",
    )  # Each hole must be attached to a course.
    mens_par = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(3)]
    )
    womens_par = models.IntegerField(
        validators=[MaxValueValidator(5), MinValueValidator(3)]
    )

    class Meta:
        unique_together = (
            ("number", "course"),
            ("name", "course"),
        )  

    def __str__(self):
        if self.name:
            return "{0} at {1}".format(self.name, self.course.name)
        else:
            return "Hole {0} at {1}".format(str(self.number), self.course.name)


# Each Course's hole can have multiple tees. Tees are differentiated
# by color. Each hole can only have one tee of each color
# Tees have a different distance(yards) to the hole from the tee box
class Tee(models.Model):
    color = models.CharField(
        choices=COLOR_CHOICES, blank=True, null=True, max_length=255
    )
    yards = models.IntegerField(
        validators=[MaxValueValidator(1000), MinValueValidator(1)]
    )
    hole = models.ForeignKey(
        "Hole",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="tees",
    )

    class Meta:
        unique_together = (
            ("color", "hole"),
        )  # only have one of each color on the hole

    def __str__(self):
        return "{0}{1}".format(self.yards, Hole)


class CoursePicture(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(default=datetime.now)
    picture = models.ImageField(
        upload_to="uploads/course/", verbose_name="image"
    )
    course = models.ForeignKey(
        "Course",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="pictures",
    )

    class Meta:
        ordering = ["-created_on"]


# # # # # # # # # # # # # # #
#   Round related models   #
# # # # # # # # # # # # # # #


# Each round of golf a user will be able to add their score for each hole.
#
# Each round is played at a single golf course. The total number of
# scores is the number of holes.
#
# Currently the user will choose a set of tees to play. That is the
# usual way to play. In the future I may want to allow the user to
# choose a tee color for each hole
#
# Planned to use the completed_on field to sum up scores and display
# them if the round is completed
class Round(models.Model):
    course = models.ForeignKey("Course", on_delete=models.SET_NULL, null=True)
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name="Title this round (optional)",
    )
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
    )
    created_on = models.DateTimeField(default=datetime.now)
    completed_on = models.DateTimeField(null=True, blank=True)
    tee_color = models.ForeignKey(
        "TeeColor",
        on_delete=models.SET_NULL,
        null=True,
        blank=False,
        related_name="teecolor",
    )

    class Meta:
        ordering = ["-created_on"]


# Scores will hold the number of strokes a player takes
#
# To function the Score model will need to be attached to a round as
# well as a hole. Each round can only have one score per hole.
#
# Future expansion can be added to display the average score on a
# course's hole

class Score(models.Model):
    """Score needs to be able to golf only nine holes"""
    round = models.ForeignKey("Round", on_delete=models.SET_NULL, null=True)
    hole = models.ForeignKey("Hole", on_delete=models.SET_NULL, null=True)
    strokes = models.IntegerField(
        validators=[MaxValueValidator(100), MinValueValidator(1)]
    )
    print(round)

    class Meta:
        unique_together = (
            ("round", "hole"),
        )  # only have one of each hole per round
