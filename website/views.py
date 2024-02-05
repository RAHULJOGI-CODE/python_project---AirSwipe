from django.http import HttpResponse
from .forms import FileUploadForm
from .models import UserFile
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import messages, auth
from .gesture_module import main as x
import threading
import multiprocessing

from django.shortcuts import get_object_or_404
from django.http import FileResponse
from django.core.exceptions import PermissionDenied


running = []


def signin(request):
    if request.method == "POST":
        submitaction = request.POST.get("submitted")

        print(f"Submit Action: {submitaction}")

        if submitaction == "SignUp":
            username = request.POST["uname"]
            email = request.POST["mail"]
            password = request.POST["pass"]
            cpassword = request.POST["cpass"]

            print(f"Username: {username}, Email: {email}")

            if password == cpassword:
                if User.objects.filter(username=username).exists():
                    messages.info(request, "Username Taken")
                    print("Username Taken")
                    return redirect("signin")
                if User.objects.filter(email=email).exists():
                    messages.info(request, "Email Taken")
                    print("Email Taken")
                    return redirect("signin")

                user = User.objects.create_user(
                    username=username, email=email, password=password
                )

                user.save()

                return redirect("/")
            else:
                messages.info(request, "Password Not Matching")
                print("Password Not Matching")
                return redirect("signin")

        elif submitaction == "Login":
            username = request.POST["uname"]
            password = request.POST["pass"]

            print(f"Username: {username}")

            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                # Redirect to the home page after successful login
                return redirect("home")
            else:
                messages.info(request, "Invalid Credentials")
                print("Invalid Credentials")  # Add this line
                return redirect("signin")

    return render(request, "signin.html")


def logout(request):
    auth.logout(request)
    # Redirect to the home page after logout
    return redirect("home")


# Create your views here.
def home(request):
    return render(request, "home.html")


def myaccount(request):
    if request.method == "POST":
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            form.instance.user_id = request.user.id
            form.save()
            return redirect("myaccount")
    else:
        form = FileUploadForm()

    user_files = UserFile.objects.filter(user=request.user)

    return render(request, "myacc.html", {"form": form, "user_files": user_files})


def run_main_function():
    x()


def present(request, file_id):
    user_file = get_object_or_404(UserFile, id=file_id)

    main_thread = threading.Thread(target=lambda: run_main_function())
    main_thread.start()
    # running.append[main_thread
    return redirect(user_file.file.url)


# def present(request, file_id):
#     # Get the UserFile object or return a 404 response if not found
#     user_file = get_object_or_404(UserFile, id=file_id)

#     # You can pass additional data if needed
#     context = {
#         "user_file": user_file,
#         # Add other data you want to pass to the template
#     }

#     # Render the template with the context data
#     return render(request, "present.html", context)
