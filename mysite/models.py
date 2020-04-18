from django.db import models
from django.contrib.auth  import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField


COVERAGE_CHOICES =  (
    ('Nigeria','Nigeria'),
    ('Abuja','Abuja'),
    ('Abia','Abia'),
    ('Adamawa','Adamawa'),
    ('Akwa Ibom','Akwa Ibom'),
    ('Anambra','Anambra'),
    ('Bauchi','Bauchi'),
    ('Bayelsa','Bayelsa'),
    ('Benue','Benue'),
    ('Cross River','Cross River'),     
    ('Delta','Delta'),
    ('Ebonyi','Ebonyi'),
    ('Enugu','Enugu'),
    ('Edo','Edo'),
    ('Ekiti','Ekiti'),
    ('Gombe','Gombe'),
    ('Imo','Imo'),
    ('Jigawa','Jigawa'),
    ('Kaduna','Kaduna'),
    ('Kano','Kano'),
    ('Katsina','Katsina'),
    ('Kebbi','Kebbi'),
    ('Kogi','Kogi'),
    ('Kwara','Kwara'),
    ('Lagos','Lagos'),
    ('Nasarawa','Nasarawa'),
    ('Niger','Niger'),
    ('Ogun','Ogun'),
    ('Ondo','Ondo'),
    ('Osun','Osun'),
    ('Oyo','Oyo'),
    ('Plateau','Plateau'),
    ('Rivers','Rivers'),
    ('Sokoto','Sokoto'),
    ('Taraba','Taraba'),
    ('Yobe','Yobe'),
    ('Zamfara','Zamfara'),
    ('National Coverage', 'National Coverage')
)

CATEGORY_CHOICES = (
    ('Corporate Accountability','Corporate Accountability'),
    ('Corruption','Corruption'),
    ('Entertainment','Entertainment'),
    ('Environment','Environment'),
    ('Governance','Governance'),
    ('Health','Health'),
    ('Judiciary','Judiciary'),
    ('Media, Arts and Culture','Media, Arts and Culture'),
    ('Power Electricity','Power Electricity'),
    ('Politic, Election','Politic, Election'),
    ('Road and Transport','Road and Transport'),
    ('Safety and Security','Safety and Security'),
    ('Others','Others'),
)

ACTION_PERSON_CHOICES= (
    ('President','President'),
    ('Minister','Minister'),
    ('Senate','Senate'),
    ('State Governor','State Governor'),
    ('State Assembly','State Assembly'),
    ('Local Gov. Chairman','Local Gov. Chairman'),
    ('Others','Others')
)


# Create your models here.

# Petition Model
class Petition(models.Model):
    user                    =       models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    Petition_Coverage       =       models.CharField(max_length=100,choices=COVERAGE_CHOICES)
    Petition_Title          =       models.CharField(max_length=100)
    Petition_Category       =       models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    Petition_Category_Other =       models.CharField(max_length=100, blank=True)
    Action_Person           =       models.CharField(max_length=100,choices=ACTION_PERSON_CHOICES)
    Action_Person_Other     =       models.CharField(max_length=100, blank=True)
    Expalnation             =       RichTextUploadingField() 
    Image                   =       models.ImageField(blank=True)
    approve                 =       models.BooleanField(blank=True, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.Petition_Title

# User Profile Model
class  UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Coverage_Admin = models.CharField(max_length=100,choices=COVERAGE_CHOICES )
    
    def __str__(self):
        return "{user}-{admin}".format(user=self.user.username, admin = self.Coverage_Admin)
    
# Petition Response Feedback Model
class PetitionResponseFeedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    Coverage_Admin = models.CharField(max_length=100,choices=COVERAGE_CHOICES )
    Feedback =  RichTextUploadingField()
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{user}-{petition}-response".format(user=self.user.username, petition = self.petition.Petition_Title)