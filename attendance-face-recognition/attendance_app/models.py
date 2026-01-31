from django.db import models

class Student(models.Model):
    name = models.CharField(max_length=200)
    roll_number = models.CharField(max_length=50, unique=True)
    embedding = models.JSONField(null=True, blank=True)  # 512D face vector

    def __str__(self):
        return f"{self.roll_number} - {self.name}"


class Attendance(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="present")

    def __str__(self):
        return f"{self.student.name} - {self.timestamp} - {self.status}"
