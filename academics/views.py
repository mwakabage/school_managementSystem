from django.shortcuts import render,redirect,get_object_or_404
from academics.models import AcademicYear,TeacherSubject,Subject,ClassRoom,Result,Assignment,Notes
from students.models import Student
from .forms import NotesForm
from django.contrib.auth import get_user_model
 
User = get_user_model()
# Create your views here.

def academic_year_list(request):
    years = AcademicYear.objects.all()
    return render(request, 'academics/academic_year_list.html', {'years': years})


def add_academic_year(request):
    if request.method == 'POST':
        year = request.POST['year']

        AcademicYear.objects.create(
            year=year,
            active=True
        )

        return redirect('academic_year_list')

    return render(request, 'academics/academic_year_add.html')

def classroom_list(request):
    classes = ClassRoom.objects.all()
    return render(request, 'academics/class_room.html', {'classes': classes})


def add_classroom(request):
    if request.method == 'POST':
        name = request.POST['name']
        stream = request.POST['stream']

        ClassRoom.objects.create(
            name=name,
            stream=stream
        )

        return redirect('classroom_list')

    return render(request, 'academics/add_class_room.html')
def subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'academics/subject.html', {'subjects': subjects})


def add_subject(request):
    if request.method == 'POST':
        name = request.POST['name']
        code = request.POST['code']

        Subject.objects.create(
            name=name,
            code=code
        )

        return redirect('subject_list')

    return render(request, 'academics/add_subject.html')

def teacher_subject_list(request):
    data = TeacherSubject.objects.all()
    return render(request, 'academics/teacher_list.html', {'data': data})


def add_teacher_subject(request):
    teachers = User.objects.filter(role="TEACHER")
    subjects = Subject.objects.all()
    classes = ClassRoom.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST.get("teacher")
        subject_id = request.POST.getlist('subject')
        classroom_id = request.POST.getlist('classroom')
        
        if not teacher_id:
            return redirect("add_teacher_subject")
        
        teacher=get_object_or_404(User, id=teacher_id)
        for subject in subject_id:
            for classroom in classroom_id:
                if subject.isdigit() and classroom.isdigit():
                    
                   TeacherSubject.objects.get_or_create(
                       subject_id=int(subject),
                        classroom_id=int(classroom),
                        teacher=teacher
        )

        return redirect('teacher_subject_list')

    context = {
        'teachers': teachers,
        'subjects': subjects,
        'classes': classes
    }

    return render(request, 'academics/add_teacher.html', context)


def assignment_detail(request, pk):

    if request.user.role != 'student':
        return redirect('dashboard')

    student = Student.objects.get(user=request.user)

    assignment = get_object_or_404(
        Assignment,
        pk=pk,
        class_room=student.classroom
    )

    return render(request, 'academics/assignment_detail.html', {
        'assignment': assignment
    })


def student_results(request):

    if request.user.role != 'student':
        return redirect('dashboard')

    student = Student.objects.get(user=request.user)

    results = Result.objects.filter(student=student)

    context = {
        'results': results
    }

    return render(request, 'students/results.html', context)

def teacher_add_assignment(request):
  
    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        subject_id = request.POST.get("subject")
        class_room_id = request.POST.get("classroom")
        due_date = request.POST.get("due_date")
        
      
        Assignment.objects.create(
            title=title,
            description=description,
            subject_id=subject_id,
            class_room_id=class_room_id,
            due_date=due_date,
            teacher=request.user
        )
        return redirect("dashboard")
    subjects = Subject.objects.all()
    classrooms = ClassRoom.objects.all()
    
    
    return render(request, "academics/add_assignment.html", {
        "subjects": subjects,
        "classrooms": classrooms
        
    })
def teacher_detail(request, teacher_id):
    teacher = User.objects.get(id=teacher_id)
    teacher_subject = TeacherSubject.objects.filter(
        teacher=teacher
    )
    context={
        "teacher":teacher,
        "teacher_subject":teacher_subject
    }
    return render(request, "academics/teacher_detail.html", context)
def teacher_add_result(request):
    if request.method == "POST":
        student_id = request.POST.get("student")
        subject_id = request.POST.get("subject")
        marks = request.POST.get("marks")
        term = request.POST.get("term")
        class_room_id = request.POST.get("classroom")

        # Automatic grade calculation
        marks = float(marks)
        if marks >= 80:
            grade = "A"
        elif marks >= 70:
            grade = "B"
        elif marks >= 60:
            grade = "C"
        elif marks >= 50:
            grade = "D"
        else:
            grade = "F"

        Result.objects.create(
            student_id=student_id,
            subject_id=subject_id,
            marks=marks,
            grade=grade,
            term=term,
            class_room_id=class_room_id,
            teacher=request.user
        )
        return redirect("dashboard")
    teacher_subject=TeacherSubject.objects.filter(
        teacher= request.user
    )
   
    subjects = Subject.objects.filter(
        id__in=teacher_subject.values_list("subject", flat=True)
    )
    classrooms = ClassRoom.objects.filter(
        id__in=teacher_subject.values_list("classroom", flat=True)
    )
    students = Student.objects.filter(
        class_room__in=classrooms
    )
    return render(request, "academics/add_result.html", {
        "students": students,
        "subjects": subjects,
        "classrooms": classrooms,
        "teacher_subject":teacher_subject
    })
    
def edit_assignment(request, pk):
    
      assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)

      if request.method == "POST":
        assignment.title = request.POST.get("title")
        assignment.description = request.POST.get("description")
        assignment.due_date = request.POST.get("due_date")
        assignment.save()

        return redirect("dashboard")

      return render(request, "academics/edit_assignment.html", {"assignment": assignment})
  
def delete_assignment(request, pk):
    
    assignment = get_object_or_404(Assignment, pk=pk, teacher=request.user)
    assignment.delete()

    return redirect("dashboard")
def edit_result(request, pk):
    
    result = get_object_or_404(Result, pk=pk, teacher=request.user)

    if request.method == "POST":
        result.marks = request.POST.get("marks")
        result.save()

        return redirect("dashboard")

    return render(request, "academics/edit_result.html", {"result": result})
def delete_result(request, pk):
    
    result = get_object_or_404(Result, pk=pk, teacher=request.user)
    result.delete()

    return redirect("dashboard")

def upload_notes(request):
    teacher = request.user
    teacher_subjects = TeacherSubject.objects.filter(teacher=teacher)
    
    if request.method == "POST":
        form=NotesForm(request.POST, request.FILES)
        
        if form.is_valid():
            notes = form.save(commit=False)
            notes.teacher = teacher
            notes.save()
            return redirect("teacher_notes")
    else:
        form=NotesForm()
        
    form.fields['subject'].queryset=Subject.objects.filter(
        id__in=teacher_subjects.values_list('subject', flat=True)
    )
       
    form.fields['class_room'].queryset=ClassRoom.objects.filter(
        id__in=teacher_subjects.values_list('classroom', flat=True)
    )
      
    return render(request, "academics/upload_materials.html", {"form":form})   
    
def teacher_notes(request):
    teacher= request.user
    
    notes = Notes.objects.filter(teacher=teacher)
    
    return render(request, "academics/teacher_notes.html",{"notes":notes})