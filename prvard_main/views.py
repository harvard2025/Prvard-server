from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import E_Message, Class, Chat_Message, C_P_real, Content, Login, University, Student, P_U_real, C_U_real, Weeks
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from datetime import datetime
import markdown
import random
from django.utils.safestring import mark_safe
# Create your views here.
def index(request):
    if request.user.is_authenticated:
        # if user is loged in.
        student = Student.objects.get(User_id=request.user)
        University = ""

        reals = P_U_real.objects.all()
        for real in reals:
            if real.Student == request.user:
                University =  real.University
        if University != "":
            # if user has a University
            is_admin = False
            if University.Admin == request.user:
                is_admin = True
            classes_u = []
            realsc = C_U_real.objects.all()
            for realc in realsc:
                if realc.University == University: 
                    classes_u.append(realc.Class)
            classes = []
            realsp = C_P_real.objects.all()
            for realp in realsp:
                if realp.Student == request.user and realp.Class in classes_u: 
                    classes.append(realp.Class)
            if University.Theme == "Harvard":
                return render(request, "harvard/index.html", {
                    'university': University,
                    'user': request.user,
                    'student': student,
                    'is_admin': is_admin,
                    'classes': classes,

                })
            else:
                return HttpResponse(f"You should to see the university main page that's id is >>>>>> ({University.Prvard_id}), But right now the theme you choose does not exist.")

        
        else:
            # if user didn't has a University
            return render(request, 'prvard/index.html')

    
    else:
        # if user not logged in.
        return redirect("main:login")
    return HttpResponse("nothing to return")





def login_f(request):
    if request.method == "POST":
        
        username = request.POST.get("username").lower()
        if not username:
            return render(request, "prvard/login.html", {'message':"Missed username :("})
        password = request.POST.get("password")
        if not password:
            return render(request, "prvard/login.html", {'message':"Missed password :("})
        
        user_a = authenticate(request, username=username, password=password)
        if user_a is not None:
            login(request, user_a)
            return redirect("main:index")
        return render(request, "prvard/login.html", {'message':"Invalid username or password :("})
    return render(request, "prvard/login.html")


def logout_f(request):
    if request.user.is_authenticated:
        logout(request)
        return redirect("main:index")
    return HttpResponse("403 --> Not allawed")



def leave(request):
    if request.user.is_authenticated:
        # if user is loged in.
        reals = P_U_real.objects.all()
        for real in reals:
            if real.Student == request.user:
                P_U_real.objects.filter(Student = real.Student).delete()
        user = request.user
        user.email = ""
        user.save()
        return redirect("main:index")
    return HttpResponse("Not allawed to acces")

def delete(request, university_id):
    if request.user.is_authenticated:
        # if user is loged in.
        university = University.objects.get(pk=university_id)
        if not university.Admin == request.user:
            return HttpResponse("Not allawed to deleate the University")
        university.delete()
        reals = P_U_real.objects.all()
        for real in reals:
            if real.University == university:
                P_U_real.objects.filter(University = real.University).delete()
        user = request.user
        user.email = ""
        user.save()
        return redirect("main:index")
    return HttpResponse("Not allawed to acces")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").lower()
        if not username:
            return render(request, "prvard/register.html", {'message':"Missed username :("})
        password = request.POST.get("password")
        if not password:
            return render(request, "prvard/register.html", {'message':"Missed password :("})
        confirmation = request.POST.get("confirmation")
        if not confirmation:
            return render(request, "prvard/register.html", {'message':"Missed confirmation :("})
        if not confirmation == password:
            return render(request, "prvard/register.html", {'message':"Password didn't match :("})

        name = request.POST.get("name")
        if not name:
            return render(request, "prvard/register.html", {'message':"Missed name :("})

        photo = request.FILES.get("photo")
        if not photo:
            return render(request, "prvard/register.html", {'message':"Missed photo :("})

        try:
            user = User.objects.create_user(username, password=password, first_name=name)
            user.save()
        except:
            return render(request, "register.html", {
                "message": "Username already taken."
            })

        student = Student(User_id=user, Photo=photo, Points=0)
        student.save()

        return redirect("main:login")

    return render(request, "prvard/register.html")


def join(request):
    if request.method == "POST":
        if not request.user.is_authenticated:
            return redirect("main:index")
        prvard_id = request.POST.get("id")
        if not prvard_id:
            return render(request, "prvard/join.html", {"message": "Missed ID"})

        try:
            university = University.objects.get(Prvard_id=prvard_id)
        except:
            return render(request, "prvard/join.html", {"message": "Invalid ID"})
        username = request.user.username
        mail = f"{username.lower()}@{university.Theme.lower()}.edu"
        print(">>>>>>>>>>>>>>>>>>>>>> mail:")
        print(mail)
        user = request.user
        user.email = mail
        user.save()
        P_U_real.objects.create(Student=user, University=university)
        return redirect("main:index")
    return render(request, "prvard/join.html")



def createu(request):
    return render(request, "prvard/createu.html")

def createu_f(request, Theme):
    if not request.user.is_authenticated:
        return redirect("main:index")
    if Theme == "Harvard":
        prvard_id = f"Prvard_id{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}.{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}.{random.randint(0,9)}{random.randint(0,9)}{random.randint(0,9)}"
        print(prvard_id)
        Admin = request.user
        university = University.objects.create(Prvard_id=prvard_id, Admin=Admin, Theme=Theme)
        university.save()
        
        P_U_real.objects.create(Student=request.user, University=university).save()

        username = request.user.username
        mail = f"{username.lower()}@{university.Theme.lower()}.edu"
        user = request.user
        user.email = mail
        user.save()

        return redirect("main:index")

        return HttpResponse("<h1 style='color: green;'>Supported</h1>")
    if Theme == "MIT":
        return HttpResponse("<h1 style='color: red;'>not supported yet! :(</h1>")
    if Theme == "Yale":
        return HttpResponse("<h1 style='color: red;'>not supported yet! :(</h1>")
    







def mobile_blocked(request):
    return render(request, 'mobile_blocked.html')

def profile(request):
    if not request.user.is_authenticated:
        return redirect("main:index")
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")

    classes_u = []
    realsc = C_U_real.objects.all()
    for realc in realsc:
        if realc.University == university: 
            classes_u.append(realc.Class)
    classes = []
    realsp = C_P_real.objects.all()
    for realp in realsp:
        if realp.Student == request.user and realp.Class in classes_u: 
            classes.append(realp.Class)

    
    return render(request, "harvard/profile.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=user),
        "other": False,
        "classes": classes,
    })



def members(request):
    if not request.user.is_authenticated:
        return redirect("main:index")
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == request.user:
            university = real.University
    if university == "":
        return redirect("main:index")
    

    reals = P_U_real.objects.filter(University=university)


    if request.method == "POST":
        fname = request.POST.get("q").lower()
        reals_f = []
        for real in reals:
            name = real.Student.first_name.lower()
            print(name)
            is_s = True
            if len(name) >= len(fname):
                for i in range(0, len(fname)):
                    if not name[i] == fname[i]:
                        print(f"{i}: {name[i]} = {fname[i]}")
                        is_s = False
                        pass
            else:
                is_s = False
            if is_s:
                reals_f.append(real)


        students = []
        for real in reals_f:
            real = real.Student
            student = Student.objects.get(User_id=real)
            name = real.first_name
            Photo = student.Photo
            Points = student.Points
            mail = real.email
            students.append({'Name': name, 'Photo': Photo, 'Points': Points, 'Mail_1': mail, 'Id': real.id})
    else:      
        students = []
        for real in reals:
            real = real.Student
            student = Student.objects.get(User_id=real)
            name = real.first_name
            Photo = student.Photo
            Points = student.Points
            mail = real.email
            students.append({'Name': name, 'Photo': Photo, 'Points': Points, 'Mail_1': mail, 'Id': real.id})

    return render(request, "harvard/members.html", {
        "people": reals,
        "university": university,
        "students": students,
        'student': Student.objects.get(User_id=request.user),
    })




def profile_other(request, id):
    user = User.objects.get(pk=id)
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    is_Admin = False
    if university.Admin == request.user:
        is_Admin = True
    other = True
    if user.id == request.user.id:
        other = False

    classes_u = []
    realsc = C_U_real.objects.all()
    for realc in realsc:
        if realc.University == university: 
            classes_u.append(realc.Class)
    classes = []
    realsp = C_P_real.objects.all()
    for realp in realsp:
        if realp.Student == user and realp.Class in classes_u: 
            classes.append(realp.Class)

    return render(request, "harvard/profile.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=request.user),
        "is_Admin": is_Admin,
        "other": other,
        "classes": classes,
    })



# class E_Message(models.Model):
#     From = models.CharField(max_length=70)
#     To = models.CharField(max_length=70)
#     Title = models.CharField(max_length=70)
#     Subject = models.TextField()
#     DateTime = models.DateTimeField()


def send_message(request):
    if not request.user.is_authenticated:
        return redirect("main:index")
    if request.method == "POST":
        
        from_f = request.user.email
        to = request.POST.get("to")
        title = request.POST.get("title")
        message = request.POST.get("message")
        if not from_f or not to or not title or not message:
            return redirect("main:message")
        now = datetime.now()
        e_message = E_Message.objects.create(From=from_f, To=to, Title=title, Subject=message, DateTime=now)
        e_message.save()
        for message in E_Message.objects.all():
            print(message.Subject)
        return redirect("main:send")


    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    
    return render(request, "harvard/message.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
    })


def inbox(request):
    messages = E_Message.objects.filter(To=(request.user.email))
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    
    return render(request, "harvard/inbox.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'messages': reversed(messages),
        'title': "Inbox",
    })

def send(request):
    messages = E_Message.objects.filter(From=(request.user.email))
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    
    return render(request, "harvard/inbox.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'messages': reversed(messages),
        'title': "Send",
    })




def show_message(request, message_id):
    is_sender = False
    message = E_Message.objects.get(pk=message_id)
    sender = User.objects.get(email=message.From)
    if User.objects.get(email=message.To) == request.user:
        message.opened = True
        message.save()
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    if sender == request.user:
        is_sender = True
    
    
    return render(request, "harvard/show.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'message': message,
        'sender': sender,
        'to': User.objects.get(email=message.To),
        'is_sender': is_sender,

    })



def delete_m(request, message_id):
    if not request.user.is_authenticated:
        return redirect("main:index")
    if not message_id:
        return redirect("main:send")
    message = E_Message.objects.get(pk=message_id)
    message.active = False
    message.save()
    return redirect("main:send")


def all_classes(request):


    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    
    classes = []
    reals = C_U_real.objects.all()
    for real in reals:
        if real.University == university:
            classes.append(real.Class)


    if request.method == "POST":
        fname = request.POST.get("q").lower()
        classes_f = []
        for class_f in classes:
            name = class_f.Name.lower()
            is_s = True
            if len(name) >= len(fname):
                for i in range(0, len(fname)):
                    if not name[i] == fname[i]:
                        print(f"{i}: {name[i]} = {fname[i]}")
                        is_s = False
                        pass
                if is_s:
                    classes_f.append(class_f)
            else:
                is_s = False
        classes = classes_f


    return render(request, "harvard/all_classes.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        "classes": classes,
    })



def Entroll(request, id):
    if not request.user.is_authenticated:
        return redirect("main:index")
    if not id:
        return redirect("main:index")
    
    class_C = Class.objects.get(pk=id)
    filtered = C_P_real.objects.filter(Class=class_C)
    for filter1 in filtered:
        if filter1.Student == request.user:
            return redirect("main:index")
    real = C_P_real.objects.create(Class=class_C, Student=request.user)
    real.save()
    return redirect("main:index")


def createC(request):
    if not request.user.is_authenticated:
        return redirect("main:index")
    if request.method == "POST":
        # get the university
        user = request.user
        university = ""
        reals = P_U_real.objects.all()
        for real in reals:
            if real.Student == user:
                university = real.University
        if university == "":
            return redirect("main:index")
        # main
        Name = request.POST.get("name")
        Admin = request.user
        Type = request.POST.get("type")
        
        Cclass = Class.objects.create(Name=Name, Admin=Admin)
        Cclass.save()
        # content
        content = Content.objects.create(Class=Cclass, Type=Type)
        content.save()
        # add the class to the university
        realU = C_U_real.objects.create(University=university, Class=Cclass)
        realU.save()
        #add the user to the class
        realS = C_P_real.objects.create(Student=Admin, Class=Cclass)
        realS.save()
        #<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<</////////////////// TODO : redirect to the class page  \\\\\\\\\\\\\\\\>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>..
        login = Login.objects.create(Date=datetime.now().date(), Class=Cclass, Student=request.user).save()
        return redirect("main:Opclass", Cclass.id)
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    
    return render(request, "harvard/createC.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
    })

def Delete_u(request, id):
    if not request.user.is_authenticated:
        return redirect("main:index") 
    user = User.objects.get(pk=id)
    if user.id == request.user.id:
        return redirect("main:index")
    print(user.first_name)
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            real.delete()
    return redirect("main:index")



def Delete_L(request, id):
    if not request.user.is_authenticated:
        return redirect("main:index") 
    if not id:
        return redirect("main:index")
    lesson = Weeks.objects.get(pk=id)
    content = lesson.Content
    class1 = content.Class
    lesson.delete()
    return redirect("main:Opclass", class1.id)


def Open_Class(request, id):
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    is_Admin = False
    if university.Admin == request.user:
        is_Admin = True
    other = True
    if user.id == request.user.id:
        other = False

    class1 = Class.objects.get(pk=id)
    login_all = Login.objects.filter(Class=class1, Student=request.user)
    login_date = None
    for login in login_all:
        login_date = login.Date
    if login_date:
        if not datetime.now().date() == login_date:
            return render(request, "class/login.html", {
                'id': id,
                'message':"Should Login :(",
            })
    else:
        return render(request, "class/login.html", {
            'id': id,
            'message':"Should Login :(",
        }) 
    user = request.user
    Type = Content.objects.get(Class=class1).Type
    Weekss = Weeks.objects.filter(Content=Content.objects.get(Class=class1))
    print(Weekss)

        

    return render(request, "class/main.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=request.user),
        "is_Admin": is_Admin,
        "other": other,
        'class':class1,
        "type": Type,
        'is_t': "1",
        "lessons": Weekss,
        "is_admin": class1.Admin == request.user,
        
    })




def Oclass(request, id):
    if request.method == "POST":
        username = request.POST.get("username").lower()

        if username == request.user.username:
            login = Login.objects.create(Date=datetime.now().date(), Class=Class.objects.get(pk=id), Student=request.user).save()
            stud = Student.objects.get(User_id=request.user)
            print(stud.Points)
            points = stud.Points + 5
            print(points)
            stud.Points = points
            stud.save()
            return redirect("main:Opclass", id)
        else:
            return render(request, "class/login.html", {
                'id': id,
                'message':"Not your Username :(",
            })
    class1 = Class.objects.get(pk=id)
    login_all = Login.objects.filter(Class=class1, Student=request.user)
    login_date = None
    for login in login_all:
        login_date = login.Date
    if login_date:
        if datetime.now().date() <= login_date:
            return redirect("main:Opclass", id)
    
    return render(request, "class/login.html", {
    'id': id,
    })
    


    

def leaveC(request, id):
    if not request.user.is_authenticated:
        return redirect("main:index")
    class1 = Class.objects.get(pk=id)
    reals = C_P_real.objects.filter(Class=class1)
    for real in reals:
        if real.Student == request.user:
            real.delete()
    return redirect("main:index")

def DeleteC(request, id):
    if not request.user.is_authenticated:
        return redirect("main:index")
    class1 = Class.objects.get(pk=id)
    reals = C_P_real.objects.filter(Class=class1)
    for real in reals:
        real.delete()
    class1.delete()
    return redirect("main:index")






def Cmember(request, id):
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    is_Admin = False
    if university.Admin == request.user:
        is_Admin = True
    other = True
    if user.id == request.user.id:
        other = False

    class1 = Class.objects.get(pk=id)
    login_all = Login.objects.filter(Class=class1, Student=request.user)
    login_date = None
    for login in login_all:
        login_date = login.Date
    if login_date:
        if not datetime.now().date() == login_date:
            return render(request, "class/login.html", {
                'id': id,
                'message':"Should Login :(",
            })
    else:
        return render(request, "class/login.html", {
            'id': id,
            'message':"Should Login :(",
        }) 
    user = request.user


    if request.method == "POST":
        reals = C_P_real.objects.filter(Class=class1)
        fname = request.POST.get("q").lower()
        reals_f = []
        for real in reals:
            name = real.Student.first_name.lower()
            print(name)
            is_s = True
            if len(name) >= len(fname):
                for i in range(0, len(fname)):
                    if not name[i] == fname[i]:
                        print(f"{i}: {name[i]} = {fname[i]}")
                        is_s = False
                        pass
            else:
                is_s = False
            if is_s:
                reals_f.append(real)


        students = []
        for real in reals_f:
            real = real.Student
            student = Student.objects.get(User_id=real)
            name = real.first_name
            Photo = student.Photo
            Points = student.Points
            mail = real.email
            students.append({'Name': name, 'Photo': Photo, 'Points': Points, 'Mail_1': mail, 'Id': real.id})
    else:
        reals = C_P_real.objects.filter(Class=class1)
        students = []
        for real in reals:
            real = real.Student
            student = Student.objects.get(User_id=real)
            name = real.first_name
            Photo = student.Photo
            Points = student.Points
            mail = real.email
            students.append({'Name': name, 'Photo': Photo, 'Points': Points, 'Mail_1': mail, 'Id': real.id})
        


    return render(request, "class/Cmember.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=request.user),
        "is_Admin": is_Admin,
        "other": other,
        'class':class1,
        'is_t': "2",
        "is_admin": class1.Admin == request.user,

        "people": C_P_real.objects.filter(Class=class1),
        "students": students,
        
    })




def Cweek(request, id):
    if request.method == "POST":
        title = request.POST.get("title")
        mark = request.POST.get("mark")
        id1 = request.POST.get("id")
        class1 = Class.objects.get(pk=id1)
        content = Content.objects.get(Class=class1)
        
        reals = Weeks.objects.filter(Content=content)
        num = None
        for real in reals:
            num = real.Number 
        if num == None:
            num = 0
        else:
            num += 1
        


        week1 = Weeks.objects.create(Content=content,Number=num, Title=title, Markdown=mark)
        return redirect("main:Opclass", id1)
    # <<<<<<<<<<<<<<< Just open the form page >>>>>>>>>>>>>>>>>>>
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    class1 = Class.objects.get(pk=id)
    Type = Content.objects.get(Class=class1).Type
    return render(request, "class/createW.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        "class": class1,
        "type": Type,
    })



def Eweek(request, id):
    if request.method == "POST":
        title = request.POST.get("title")
        mark = request.POST.get("mark")
        id1 = request.POST.get("id")
        lesson = Weeks.objects.get(pk=id)
        content = lesson.Content
        class1 = content.Class

        lesson.Title=title
        lesson.Markdown=mark
        lesson.save()

        return redirect("main:Opclass", id1)
    # <<<<<<<<<<<<<<< Just open the form page >>>>>>>>>>>>>>>>>>>
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    lesson = Weeks.objects.get(pk=id)
    content = lesson.Content
    class1 = content.Class
    Type = Content.objects.get(Class=class1).Type

    mark = lesson.Markdown
    tit = lesson.Title
    return render(request, "class/editW.html", {
        "lesson_id": lesson.id,
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        "class": class1,
        "type": Type,
        "mark": mark,
        "title": tit,
    })



def ShowW(request, id):
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    is_Admin = False
    if university.Admin == request.user:
        is_Admin = True
    other = True
    if user.id == request.user.id:
        other = False

    lesson = Weeks.objects.get(pk=id)
    content = lesson.Content
    class1 = content.Class
    user = request.user
    Type = Content.objects.get(Class=class1).Type
    
    title = lesson.Title
    num = lesson.Number
    mark = mark_safe(markdown.markdown(lesson.Markdown, extensions=['extra']))
    lesson_id = lesson.id

        

    return render(request, "class/showW.html", {
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=request.user),
        "is_Admin": is_Admin,
        "other": other,
        'class':class1,
        "type": Type,
        'is_t': "1",
        "is_admin": class1.Admin == request.user,
        "title": title,
        "num": num,
        "mark": mark,
        "lesson_id":lesson_id,
        "lessoni": True,

    })






def Chat1(request, id):
    user = request.user
    university = ""
    reals = P_U_real.objects.all()
    for real in reals:
        if real.Student == user:
            university = real.University
    if university == "":
        return redirect("main:index")
    is_Admin = False
    if university.Admin == request.user:
        is_Admin = True
    other = True
    if user.id == request.user.id:
        other = False

    class1 = Class.objects.get(pk=id)
    login_all = Login.objects.filter(Class=class1, Student=request.user)
    login_date = None
    for login in login_all:
        login_date = login.Date
    if login_date:
        if not datetime.now().date() == login_date:
            return render(request, "class/login.html", {
                'id': id,
                'message':"Should Login :(",
            })
    else:
        return render(request, "class/login.html", {
            'id': id,
            'message':"Should Login :(",
        }) 
    user = request.user
    Type = Content.objects.get(Class=class1).Type

    messages = Chat_Message.objects.filter(Class=class1).order_by("id")
    # .reverse()
    messages = Chat_Message.objects.filter(Class=class1).order_by("-id")[:30][::-1]

    messages_new = []
    for message in messages:
        Message = message.Message
        name = message.Student.first_name
        student = Student.objects.get(User_id=message.Student)
        img_url = student.Photo.url
        id1 = message.Student.id
        messages_new.append({"message":Message, "name":name, "img_url":img_url, "id":id1})
    messages = messages_new

    return render(request, "class/Chat.html", {
        "id": id,
        "university": university,
        'user': user,
        "student": Student.objects.get(User_id=user),
        'user_st': Student.objects.get(User_id=request.user),
        "is_Admin": is_Admin,
        "other": other,
        'class':class1,
        "type": Type,
        'is_t': "3",
        "is_admin": class1.Admin == request.user,
        "messages": messages,
    })



def add_message(request, id):
    if not id:
        return redirect("main:index")
    if not request.user.is_authenticated:
        return redirect("main:index")
    class1 = Class.objects.get(pk=id)
    message_n = Chat_Message.objects.create(Class=class1, Student=request.user, Message=request.POST.get("message"))
    message_n.save()
    return redirect("main:Cclass", id)