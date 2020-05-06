from django.db import models


class ApprovedManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedManager, self).get_queryset().filter(approve = True)
    
    
class showCommentsManager(models.Manager):
    def get_queryset(self):
        return super(showCommentsManager, self).get_queryset().filter(show_comment = True)
    
        
class ApprovedCommendationManager(models.Manager):
    def get_queryset(self):
        return super(ApprovedCommendationManager, self).get_queryset().filter(approve = True)
    

class showCommentsCommendationManager(models.Manager):
    def get_queryset(self):
        return super(showCommentsCommendationManager, self).get_queryset().filter(show_comment = True)


class AccountManager(models.Manager):
    def get_queryset(self):
        return super(AccountManager, self).get_queryset().filter(category = "Account")

class PetitionManager(models.Manager):
    def get_queryset(self):
        return super(PetitionManager, self).get_queryset().filter(category = "Petition")


class CommendationManager(models.Manager):
    def get_queryset(self):
        return super(CommendationManager, self).get_queryset().filter(category = "Commendation")


class DonationManager(models.Manager):
    def get_queryset(self):
        return super(DonationManager, self).get_queryset().filter(category = "Donation")


class BlogManager(models.Manager):
    def get_queryset(self):
        return super(BlogManager, self).get_queryset().filter(category = "Blog")


class OthersManager(models.Manager):
    def get_queryset(self):
        return super(OthersManager, self).get_queryset().filter(category = "Others")
