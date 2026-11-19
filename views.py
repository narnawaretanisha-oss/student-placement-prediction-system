from django.shortcuts import render, redirect

from .models import Student

import joblib


# HOME PAGE
def home(request):

    return render(request, 'home.html')


# REGISTRATION PAGE
def registration(request):

    return render(request, 'registration.html')


# SAVE STUDENT DATA
def save_student(request):

    if request.method == 'POST':

        student_id = request.POST['student_id']

        student_name = request.POST['student_name']

        student_password = request.POST['student_password']

        student_email = request.POST['student_email']


        Student.objects.create(

            student_id=student_id,

            student_name=student_name,

            student_password=student_password,

            student_email=student_email

        )


        # Registration ke baad Login page
        return redirect('login')


    return redirect('registration')


# LOGIN PAGE
def login(request):

    return render(request, 'login.html')


# LOGIN CHECK
def login_validation(request):

    if request.method == 'POST':

        student_name = request.POST['student_name']

        student_password = request.POST['student_password']


        try:

            student = Student.objects.get(

                student_name=student_name,

                student_password=student_password

            )


            request.session['student_name'] = student.student_name


            return redirect('prediction')


        except Student.DoesNotExist:

            return render(

                request,

                'login.html',

                {
                    'error': 'Invalid Student Name or Password'
                }

            )


    return redirect('login')


# PLACEMENT PREDICTION PAGE
def prediction(request):

    if 'student_name' not in request.session:

        return redirect('login')


    return render(

        request,

        'prediction.html',

        {
            'student_name': request.session['student_name']
        }

    )


# ML RESULT
def result(request):
    if 'student_name' not in request.session:
        return redirect('login')

    if request.method == 'POST':

        cgpa = float(request.POST['cgpa'])
        iq = float(request.POST['iq'])
        profile_score = float(request.POST['profile_score'])

        # ML MODEL LOAD
        scaler = joblib.load('scalermodel1.pkl')
        model = joblib.load('mlmodel1.pkl')

        # Input data
        data = [[cgpa, iq, profile_score]]

        # Scaling
        scaled_data = scaler.transform(data)

        # Prediction
        prediction_value = model.predict(scaled_data)[0]

        if prediction_value == 1:
            result_text = "Eligible for Placement"
        else:
            result_text = "Not Eligible for Placement"

        return render(request, 'result.html', {
            'student_name': request.session['student_name'],
            'cgpa': cgpa,
            'iq': iq,
            'profile_score': profile_score,
            'result': result_text
        })

    return redirect('prediction')