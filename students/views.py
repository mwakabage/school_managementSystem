from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Student
from academics.models import  Subject,Assignment,Result,Notes
from students.models import User


# Dashboard for students
@login_required
def student_dashboard(request):
    student = Student.objects.get(user=request.user)
    assignments = Assignment.objects.filter(subject__class_room=student.class_room)
    subjects = Subject.objects.filter(class_room=student.class_room)
    results = Result.objects.filter(subjects__class_room=student.class_room)

    context = {
        'student': student,
        'assignments': assignments,
        'subjects': subjects,
        'results': results
    }
    return render(request, 'students/student_dashboard.html', context)
def student_result(request):
    student = Student.objects.get(user=request.user)

    results = Result.objects.filter(student=student)
    
    return render(request, 'students/student_results.html', {
        'results':results
    })
def student_home(request):
    student=Student.objects.get(user=request.user)

    return render(request,'students/home.html',{
        'student':student,
      'user':request.user
    })
    
def student_assignment(request):
        
    student = get_object_or_404(Student, user=request.user)

    assignments=Assignment.objects.filter(
          subject__class_room=student.class_room
      )
  
    context = {
        'student':student,
        'assignments': assignments
    }

    return render(request, 'students/assignment1.html', context)
def assignment_detail(request, pk):
    
    if request.user.role != 'student':
        return redirect('dashboard')

    student = Student.objects.get(user=request.user)

    assignment = get_object_or_404(
        Assignment,
        pk=pk,
        class_room=student.class_room
    )

    return render(request, 'students/assignment_detail.html', {
        'assignment': assignment
    })
    
def student_materials(request):
    student = request.user
    classroom = student.classroom
    
    query = request.GET.get("q")
    notes=Notes.objects.filter(subject__name__icontains=query)
    
    return render(request, "student_materials.html",{
        "notes":notes,
        "query":query,
        "classroom":classroom
    })