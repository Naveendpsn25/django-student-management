from django.shortcuts import render, redirect,get_object_or_404
from .models import Student
from .forms import StudentForm
from django.http import HttpResponse
from django.db.models import Q


from django.contrib import messages

def student_list(request):
    query = request.GET.get('q')

    students = Student.objects.all()

    if query:
        students = students.filter(
            Q(name__icontains=query) |
            Q(course__icontains=query)
        )

    return render(request, 'students/student_list.html', {
        'students': students
    })


def add_student(request):
    if request.method == "POST":
        Student.objects.create(
            name=request.POST['name'],
            email=request.POST['email'],
            course=request.POST['course'],
            age=request.POST['age']
        )
        return redirect('/')  

    return render(request, 'students/add_student.html')

def edit_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = StudentForm(instance=student)

    return render(request, 'students/edit_student.html', {'form': form})

def delete_student(request, id):
    student = get_object_or_404(Student, id=id)

    if request.method == "POST":
        student.delete()
        messages.success(request, "Student deleted successfully")
        return redirect('/')

    return render(request, 'students/delete_student.html', {'student': student})

