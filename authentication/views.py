from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from .forms import UserForm,ProfileForm
from django.contrib import messages
from .models import User 
from academics.models import Assignment,Result,TeacherSubject
from students.models import Student
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
import random
# Create your views here.
def login_form(request):
    if request.method == "POST":
       email=request.POST.get("email")
       password=request.POST.get("password") 
       user=authenticate(request, username=email, password=password)
    
    
       if user is not None:
          login(request,user)
          return redirect("dashboard")
       else:
            messages.error(request, "Invalid username or password",extra_tags="login error")
            
            
    return render(request,"authentication/login.html")
    
def register_form(request):
    if request.method=="POST":
        form=UserForm(request.POST)
        
        if form.is_valid():
            user=form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.role="STUDENT"
            user.save()
            
            admission_number = f"UDOM/ADM{random.randint(1000,9999)}"

            Student.objects.create(
                user=user,
                admission_number=admission_number
            )
            messages.success(request, "Registered successfully!!!")
            return redirect("login")
         
    else:
        form=UserForm()
    return render(request,'authentication/register.html',{ 
                                                          
                                                        "first_name":form["first_name"],
                                                        "middle_name":form["middle_name"],
                                                        "last_name":form["last_name"],
                                                        "email":form["email"],
                                                        "year":form["year"],
                                                        "phone_number":form["phone_number"],
                                                        "national_number":form["national_number"],
                                                        "birth_of_date":form["Date of Birth"],
                                                        "password":form["password"],
                                                                      #"form":form        
                                                                          })
@login_required
def dashboard(request):
    if request.user.role == 'STUDENT': 
      student=request.user.students
      assignments=Assignment.objects.filter(
          subject__class_room=student.class_room
      )

      subjects = student.class_room.subjects.all()
      results = Result.objects.filter(student=student)
      return render(request,'students/student_dashboard.html',{
          'student':student,
          'assignments':assignments,
          'results':results,
          'subjects':subjects
      })

    elif request.user.role == 'TEACHER': 
       teacher = request.user
       if teacher.groups.filter(name="Headmaster").exists():
    
        assignments = Assignment.objects.all()
        results = Result.objects.all()
        teacher_subjects = User.objects.filter(role="TEACHER")
        is_headmaster = True
        is_academic = False
        is_normal = False

       elif teacher.groups.filter(name="Academic Teacher").exists():
        assignments = Assignment.objects.all()
        results = Result.objects.all()
        teacher_subjects = TeacherSubject.objects.all()
        is_headmaster = False
        is_academic = True
        is_normal = False
        
       elif teacher.groups.filter(name="Normal Teacher").exists():
           
        teacher_subjects = TeacherSubject.objects.filter(teacher=teacher)
        assignments = Assignment.objects.filter(teacher=teacher)

        results = Result.objects.filter(teacher=teacher)
        is_headmaster = False
        is_academic = False
        is_normal = True

    
       else:
            assignments = []
            results = []
            teacher_subjects = []
            is_headmaster = False
            is_academic = False
            is_normal = False
         
       context = {
        "teacher": teacher,
        "assignments": assignments,
        "results":results,
        "teacher_subjects": teacher_subjects,
        "is_headmaster": is_headmaster,
        "is_academic": is_academic,
        "is_normal": is_normal
         }
       return render(request,'academics/teacher_dashboard.html', context)

    else:
      return redirect('login')

        # Default redirect if unknown role return redirect('login')

def logout_view(request):
    logout(request)
    return redirect('login')



def edit_profile(request):
    
    
    
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=request.user)
        
      
        if form.is_valid():
           form.save()
           return redirect('dashboard')
       
    else:
           form = ProfileForm(instance=request.user)
    return render(request,'',{'form':form})