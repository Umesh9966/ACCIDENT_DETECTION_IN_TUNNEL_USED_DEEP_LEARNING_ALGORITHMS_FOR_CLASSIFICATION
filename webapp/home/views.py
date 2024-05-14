from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from tensorflow.keras.models import *
from tensorflow.keras.layers import *
from django.contrib.auth import authenticate,login,logout
from .models import *
from tensorflow.keras.preprocessing import image
import os
import pandas as pd
import numpy as np
from PIL import Image
from django.shortcuts import render
from keras.models import load_model
from keras.preprocessing import image
from .models import Ccrack

# Create your views here.
index="index.html"
registerpage="register.html"
loginpage="login.html"
Userhome = 'userhome.html'
uploadpage = 'upload.html'
resultpage = "result.html"

def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request,'about.html')

def register(request):   
        if request.method == 'POST':
            name = request.POST['name']
            email = request.POST['email']
            password = request.POST['password']
            conpassword = request.POST['conpassword']
            # age = request.POST['Age']
            contact = request.POST['contact']
            if password == conpassword:
                register = Register(name=name, email=email, password=password,
                                contact=contact)
                register.save()
                print(register)

            msg = f"You've signed up successfully   {name}"
            return render(request, loginpage)
        # else:
        #     msg = "Registration failed. Please try again."
            return render(request, registerpage, {"msg": msg})
        return render(request,'register.html')

def login(request):
    if request.method == 'POST':
        lemail = request.POST['email']
        lpassword = request.POST['password']

        d = Register.objects.filter(email=lemail, password=lpassword).exists()
        print(d)
        if d:
            return redirect(userhome)


        else:
            msg = 'Login failed'
            return render(request, login, {'msg': msg})
    return render(request,'login.html')

def userhome(request):
    return render(request, Userhome)
def upload(request):
    pathss = os.listdir(r"../data")
    classes = ['Accident','No Accident']
    for i in pathss:
        classes.append(i)
    if request.method == "POST":
        file = request.FILES['file']        
        s = Ccrack(image=file)  
        s.save()
        path1 = os.path.join('home/static/save/' + s.filename())
       
        model = load_model(r'D:\project\CODE\confusion metrix\mobilenet.ipynb')

        # Resize the input image to (100, 100) while using CNN and Desnet for MobileNet use 224, 244
        img = Image.open(path1)
        img = img.resize((224,224))
        
        x1 = np.array(img, dtype=np.float32)  # Convert image to float32
        x1 = np.expand_dims(x1, axis=0)
        x1 /= 255.0  # Divide by 255.0 to ensure floating-point division
        
        result = model.predict(x1)
        b1 = np.argmax(result)
        prediction = classes[b1]

        return render(request, 'result.html', {"result": prediction, "path1": 'static/save/' + s.filename()})

    return render(request, 'upload.html')