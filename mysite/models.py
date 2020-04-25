from django.db import models
from django.contrib.auth  import get_user_model
from ckeditor_uploader.fields import RichTextUploadingField
from .managers import ApprovedManager, showCommentsManager, ApprovedCommendationManager, showCommentsCommendationManager

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
    ('National Coverage', 'National Coverage'),
    ('None', 'None')
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


GLOBAL_ADMIN_CHOICES = (
    ("True", "Yes"),
    ("False", "No"),
    ('None', 'None')
)

PETITION_RESPONSE_CHOICES = (
    ("True", "Yes"),
    ("False", "No")
)

# Create your models here.

# Petition Model
class Petition(models.Model):
    user                    =       models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    Petition_Coverage       =       models.CharField(max_length=100,choices=COVERAGE_CHOICES)
    # Petition_Coverage -> Select the Coverage admin to which it will be send
    Petition_Title          =       models.CharField(max_length=100)
    Petition_Category       =       models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    Petition_Category_Other =       models.CharField(max_length=100, blank=True)
    Action_Person           =       models.CharField(max_length=100,choices=ACTION_PERSON_CHOICES)
    Action_Person_Other     =       models.CharField(max_length=100, blank=True)
    Expalnation             =       RichTextUploadingField() 
    Image                   =       models.ImageField(blank=True)
    approve                 =       models.BooleanField(blank=True, default=False)
    timestamp               =       models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    approved_objects = ApprovedManager()

    def __str__(self):
        return self.Petition_Title

# User Profile Model
class  UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    Coverage_Admin = models.CharField(max_length=100,choices=COVERAGE_CHOICES, default = 'None' )
    golbal_Admin = models.CharField(max_length = 6, choices = GLOBAL_ADMIN_CHOICES, default="None")
    
    def __str__(self):
        return "{user}-{admin}".format(user=self.user.username, admin = self.Coverage_Admin)
    
# Petition Response Feedback Model
class PetitionResponseFeedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    Coverage_Admin = models.CharField(max_length=100,choices=COVERAGE_CHOICES )
    Feedback =  RichTextUploadingField()
    response = models.CharField(max_length=6, choices= PETITION_RESPONSE_CHOICES, default = "False")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{user}-{petition}-response".format(user=self.user.username, petition = self.petition.Petition_Title)
    
# Commendation Model
class Commendation(models.Model):
    user                        =       models.ForeignKey(get_user_model(), on_delete= models.CASCADE)
    Commendation_Coverage       =       models.CharField(max_length=100,choices=COVERAGE_CHOICES)
    Commendation_Title          =       models.CharField(max_length=100)
    Commendation_Category       =       models.CharField(max_length=100,choices=CATEGORY_CHOICES)
    Commendation_Category_Other =       models.CharField(max_length=100, blank=True)
    Action_Person               =       models.CharField(max_length=100, choices=ACTION_PERSON_CHOICES)
    Action_Person_Other         =       models.CharField(max_length=100, blank=True)
    Expalnation                 =       RichTextUploadingField() 
    Image                       =       models.ImageField(blank=True)
    approve                     =       models.BooleanField(blank=True, default=False)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    approved_objects = ApprovedCommendationManager()
    
    # Extra Method
    def get_CommendationSigner_objects(self):
        return self.commendation_signer_set.all().filter(show_comment=True)

    def __str__(self):
        return self.Commendation_Title

# Commendation Response Feedback Model
class CommendationResponseFeedback(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    commendation = models.ForeignKey(Commendation, on_delete=models.CASCADE)
    Coverage_Admin = models.CharField(max_length=100,choices=COVERAGE_CHOICES )
    Feedback =  RichTextUploadingField()
    response = models.CharField(max_length=6, choices= PETITION_RESPONSE_CHOICES, default = "False")
    timestamp = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return "{user}-{petition}-response".format(user=self.user.username, petition = self.commendation.Commendation_Title)
    
    
# Petition Live Signature Model  
class Petition_Signer(models.Model):
    Name                    =       models.CharField(max_length=100)
    Email                   =       models.CharField(max_length=100)
    Reason                  =       models.TextField(blank=True) 
    show_comment            =       models.BooleanField(blank=True, default=True)
    petition = models.ForeignKey(Petition, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    approved_objects = showCommentsManager()

    def __str__(self):
        return self.Name

  
# Petition Live Signature Model  
class Commendation_Signer(models.Model):
    Name                    =       models.CharField(max_length=100)
    Email                   =       models.CharField(max_length=100)
    Reason                  =       models.TextField(blank=True) 
    show_comment            =       models.BooleanField(blank=True, default=True)
    commendation = models.ForeignKey(Commendation, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()
    approved_objects = showCommentsCommendationManager()

    def __str__(self):
        return self.Name

