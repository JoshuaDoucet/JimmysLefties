from django.db import models
from django.contrib.auth.models import User

SHOE_WIDTHS = [
    ("AAA", "AAA"),
    ("AA", "AA"),
    ("A", "A"),
    ("B", "B"),
    ("C", "C (Narrow)"),
    ("D", "D (Medium)"),
    ("E", "E (Wide)"),
    ("EE", "EE"),
    ("EEE", "EEE"),
    ("?", "Unknown")
]

# The foot that a shoe belongs to
FOOT = [
  ("L", "Left"),
  ("R", "Right"),
  ("B", "Both"),
  ("?", "Unknown")
]

#The sex the shoe is designed for
SEX = [
  ('M', 'Man'),
  ('W', 'Woman'),
  ("NA", "N/A")
] 

# Create your models here.
class Shoe(models.Model):
    # Standardized US size of shoe wifth
    shoe_id = models.AutoField(primary_key=True)
    # description of shoe
    title = models.CharField(max_length=200, blank=True, null=True)
    # long description of shoe
    description = models.CharField(max_length=400, blank=True, null=True)
    # company brand of shoe
    brand = models.CharField(max_length=80, blank=True, null=True)
    # size or length of shoe
    length = models.FloatField(blank=True, null=True)
    # size of second shoe
    length2 = models.FloatField(blank=True, null=True)
    # width type of shoe
    width = models.CharField(max_length=10, choices = SHOE_WIDTHS, blank=True, null=True)
    # width 2
    width2 = models.CharField(max_length=10, choices = SHOE_WIDTHS, blank=True, null=True)

    # which foot the shoe belongs to
    foot = models.CharField(max_length=10, choices = FOOT, blank=True, null=True)
    sex = models.CharField(max_length=5, choices = SEX, blank=True, null=True)
    # URL to purchase shoe
    purchaseURL = models.URLField(max_length=2000, blank=True, null=True)
    # image URL of shoe
    imageURL = models.URLField(max_length=2000, blank=True, null=True)
    # Main color of shoe
    color = models.CharField(max_length=20, blank=True, null=True)
    # show object creation date and time
    created_on = models.DateTimeField(auto_now_add=True)

    class Meta:
        #db_table = "shoe"
        verbose_name = u'Shoe'
        verbose_name_plural = u'Shoes'

    def __unicode__(self):
        return self.title

# class model to store information about a user
class SiteUser(models.Model):
  user_ID = models.AutoField(primary_key=True, )
  # for django auth built in user
  authUser = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)  
  firstname = models.CharField(max_length=50)
  lastname = models.CharField(max_length=50)
  email = models.EmailField(max_length=254)
  username = models.CharField(max_length=50)
  leftSize = models.FloatField(blank=True, null=True)
  leftWidth = models.CharField(max_length=10, choices = SHOE_WIDTHS)
  rightSize = models.FloatField(blank=True, null=True)
  rightWidth = models.CharField(max_length=10, choices = SHOE_WIDTHS)
  sex = models.CharField(max_length=10, choices = SEX, blank=True, null=True)

#Class model for a search request to find a certain type of shoe
class SearchRequest(models.Model):
  search_id = models.AutoField(primary_key=True)
  phrase = models.CharField(max_length=200, blank=True, null=True)
  size = models.FloatField(blank=True, null=True)
  width = models.CharField(max_length=10, choices = SHOE_WIDTHS, blank=True, null=True)
  color = models.CharField(max_length=20, blank=True, null=True)
  foot = models.CharField(max_length=10, choices = FOOT, blank=True, null=True)
  sex = models.CharField(max_length=5, choices = SEX, blank=True, null=True)
  #userId = models.IntegerField(blank=True, null=True)
  userID = models.ForeignKey(SiteUser, on_delete=models.CASCADE)
  createdOn = models.DateTimeField(auto_now_add=True)