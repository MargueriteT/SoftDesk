from django.db import models
from users.models import User


class Project(models.Model):
    """Define project's attributes"""

    TYPES = (('BACK-END', 'BACK-END'), ('FRONT-END', 'FRONT-END'),
             ('IOS', 'IOS'), ('ANDROID', 'ANDROID'))

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    type = models.CharField(max_length=120, choices=TYPES)
    contributors = models.ManyToManyField(User, through='Contributor')
    author_id = models.IntegerField(null=True)


class Contributor(models.Model):
    """Define contributor's attributes"""

    CHOICES = (('NO', 'NO'), ('YES', 'YES'))
    ROLES = (('AUTHOR', 'AUTHOR'), ('CONTRIBUTOR', 'CONTRIBUTOR'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    permission = models.CharField(max_length=3, choices=CHOICES)
    role = models.CharField(max_length=11, choices=ROLES)


class Issue(models.Model):
    """Define Issue's attributes"""

    PRIORITY = (('FAIBLE', 'FAIBLE'),
                ('MOYENNE', 'MOYENNE'),
                ('ELEVEE', 'ELEVEE'))
    TAG = (('BUG', 'BUG'),
           ('AMELIORATION', 'AMELIORATION'),
           ('TÂCHE', 'TÂCHE'))
    STATUS = (('A FAIRE', 'A FAIRE'),
              ('EN COURS', 'EN COURS'),
              ('TERMINE', 'TERMINE'))

    title = models.CharField(max_length=120)
    description = models.CharField(max_length=120)
    tag = models.CharField(max_length=120, choices=TAG)
    priority = models.CharField(max_length=120, choices=PRIORITY)
    project_id = models.IntegerField(null=True)
    status = models.CharField(max_length=120, choices=STATUS)
    author_user = models.ForeignKey(User,
                                    on_delete=models.CASCADE)
    assigned_user = models.ForeignKey(Contributor, null=True,
                                      on_delete=models.CASCADE,
                                      related_name='assigned')
    created_time = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    """Define Comment's attributes"""

    description = models.CharField(max_length=120)
    author_user = models.ForeignKey(User, on_delete=models.CASCADE)
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE)
    created_time = models.DateTimeField(auto_now_add=True)