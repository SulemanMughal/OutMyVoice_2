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

