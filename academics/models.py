from django.db import models

# Create your models here.
class  AcademicYear(models.Model):
    year_of_study=models.CharField(max_length=78)
    active=models.BooleanField(default=True)
    
class ClassRoom(models.Model):
    name = models.CharField(max_length=20)   # Form 1
    stream = models.CharField(max_length=10) # A, B, C
    def __str__(self):
        return self.name
class Subject(models.Model): 
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=10)
    class_room=models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True, related_name="subjects")
    def __str__(self):
         return self.name
class TeacherSubject(models.Model):
    teacher = models.ForeignKey(
        'authentication.User',
        on_delete=models.CASCADE
    )
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="teacher_assignments", null=True, blank=True)
    classroom = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True, blank=True)
    def __str__(self):
        return f"{self.teacher} - {self.subject} - {self.classroom}"
class Assignment(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name="assignments")
    due_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    class_room=models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True) 

    def __str__(self):
        return self.title

class Result(models.Model):
    student = models.ForeignKey("students.Student", on_delete=models.CASCADE, related_name="results")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    marks = models.FloatField()
    grade = models.CharField(max_length=2, blank=False,null=False)
    term = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class_room=models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True)
    teacher = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True)  # Add teacher

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.marks}"
class Notes(models.Model):
    teacher = models.ForeignKey("authentication.User", on_delete=models.CASCADE, null=True, blank=True)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    class_room = models.ForeignKey(ClassRoom, on_delete=models.CASCADE,null=True)
    title = models.CharField(max_length=255)
     
    file = models.FileField(upload_to="notes/files/", blank=True, null=True)
     
    video = models.FileField(upload_to="noets/video/", blank=True, null=True)
    
    created_at = models.DateTimeField(auto_created=True)
    def __str__(self):
        return self.title