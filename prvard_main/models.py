from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# <<<<<<<<<<<<<<<<<<\\\\\\\\\\    University   //////////>>>>>>>>>>>>>>>>> #
class University(models.Model):
    Prvard_id = models.CharField(max_length=30)
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Theme = models.CharField(max_length=30)

class P_U_real(models.Model):
    University = models.ForeignKey(University, on_delete=models.CASCADE)
    Student = models.ForeignKey(User, on_delete=models.CASCADE)
    def __str__(self):
        return f"{self.Student.first_name} --> ({self.University.Prvard_id})"


# <<<<<<<<<<<<<<<<<<\\\\\\\\\\    User & Student   //////////>>>>>>>>>>>>>>>>> #
class Student(models.Model):
    User_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="student")
    Points = models.IntegerField()
    Photo = models.ImageField(upload_to='Photos/Students_Profiles_Photos/%y/%m/%d',)
    def __str__(self):
        return f"{self.id}: {self.User_id.first_name}"

class E_Message(models.Model):
    From = models.CharField(max_length=70)
    To = models.CharField(max_length=70)
    Title = models.CharField(max_length=70)
    Subject = models.TextField()
    DateTime = models.DateTimeField()
    active = models.BooleanField(default=True)
    opened = models.BooleanField(default=False)






# <<<<<<<<<<<<<<<<<<\\\\\\\\\\    Classes   //////////>>>>>>>>>>>>>>>>> #
class Class(models.Model):
    Admin = models.ForeignKey(User, on_delete=models.CASCADE)
    Name = models.CharField(max_length=50)
    # Description = models.CharField(max_length=200)
    # Img = models.ImageField(upload_to='Photos/Classes_IMG/%y/%m/%d',)

class Content(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Type = models.CharField(max_length=30)

class Weeks(models.Model):
    Content = models.ForeignKey(Content, on_delete=models.CASCADE)
    Number = models.IntegerField()
    Title = models.CharField(max_length=50)
    Markdown = models.TextField()


class Chat_Message(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Student = models.ForeignKey(User, on_delete=models.CASCADE)
    Message = models.CharField(max_length=700)



class C_P_real(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Student = models.ForeignKey(User, on_delete=models.CASCADE)

class C_U_real(models.Model):
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    University = models.ForeignKey(University, on_delete=models.CASCADE)


class Login(models.Model):
    Date = models.DateField()
    Class = models.ForeignKey(Class, on_delete=models.CASCADE)
    Student = models.ForeignKey(User, on_delete=models.CASCADE) 