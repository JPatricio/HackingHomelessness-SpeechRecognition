from django.db import models


class Report(models.Model):
    """
    Our single model, will report all relevant details on a Coaching session
    """
    client = models.CharField(max_length=30)
    date = models.DateTimeField(auto_now=True)
    transcript = models.TextField()
    topics = models.CharField(max_length=300)
