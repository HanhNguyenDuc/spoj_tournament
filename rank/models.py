from django.db import models
from .utils import DataProcessor

# Create your models here.
class User(models.Model):
    solved_num = models.IntegerField()
    user_name = models.CharField("user name", default="duchanhctn99", max_length=100)
    name = models.CharField("name", default="name", max_length=100)
    user_url = models.CharField("url", default="/", max_length=100)
    target = models.IntegerField(default = 1)
    lastrank = models.IntegerField(default = 1)

    def __str__(self):
        return "{} rank {}".format(self.name, self.lastrank)


class Problem(models.Model):
    name = models.CharField("name", default="PTIT", max_length=100)
    score = models.FloatField("score", default=1)

    def __str__(self):
        return "{} - {}".format(self.name, self.score)

    def get_url(self):
        return "https://www.spoj.com/PTIT/problems/{}/".format(self.name)

    
    

class Relationship(models.Model):
    user_key = models.ForeignKey(User, on_delete=models.CASCADE)
    problem_key = models.ForeignKey(Problem, on_delete=models.CASCADE)

    def __str__(self):
        return "{} - {}".format(self.user_key, self.problem_key)

    def __eq__(self, param_2):
        return self.problem_key == param_2.problem_key
    

    

    

