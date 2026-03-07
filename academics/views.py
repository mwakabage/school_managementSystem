from django.shortcuts import render,redirect,get_object_or_404
from academics.models import AcademicYear,TeacherSubject,Subject,ClassRoom,Result,Assignment
from students.models import Student
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
    teachers = User.objects.all()
    subjects = Subject.objects.all()
    classes = ClassRoom.objects.all()

    if request.method == 'POST':
        teacher_id = request.POST['teacher']
        subject_id = request.POST['subject']
        class_id = request.POST['classroom']

        TeacherSubject.objects.create(
            teacher_id=teacher_id,
            subject_id=subject_id,
            classroom_id=class_id
        )

        return redirect('teacher_list')

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
        
        subject = Subject.objects.get(id=subject_id)
        classroom = ClassRoom.objects.get(id=class_room_id)

        Assignment.objects.create(
            title=title,
            description=description,
            subject_id=subject_id,
            class_room_id=class_room_id,
            due_date=due_date,
            teacher=request.user
        )
        return redirect("teacher_dashboard")

    subjects = Subject.objects.all()
    classrooms = ClassRoom.objects.all()
    return render(request, "academics/assignment.html", {
        "subjects": subjects,
        "classrooms": classrooms
    })

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
        return redirect("teacher_dashboard")

    students = Student.objects.all()
    subjects = Subject.objects.all()
    classrooms = ClassRoom.objects.all()
    return render(request, "academics/add_result.html", {
        "students": students,
        "subjects": subjects,
        "classrooms": classrooms
    })