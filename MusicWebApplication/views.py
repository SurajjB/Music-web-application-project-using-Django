from cgitb import text
from contextvars import Context
import email
import string
import uuid
from django.shortcuts import render, HttpResponse, redirect
from MusicWebApplication.models import Profile, Song, Contact
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.models import User, auth
from django.contrib import messages
from MusicWebApplication.helpers import User_Account_Recovery_Email_Token

# Create your views here.
def login(request):
    #return HttpResponse("This is login page")
    if request.method == 'POST':
        Email_ID = request.POST.get('Email_ID')
        Password = request.POST.get('Password')
        User_Authentication = auth.authenticate(username = Email_ID, password = Password)
        
        if User_Authentication is not None:
            auth.login(request, User_Authentication)
            return redirect('/home')
        
        elif User.objects.filter(email = Email_ID).exists() == False:
            messages.info(request, "User not registered. <a href = '/signup' style = 'color : black'> Click here to signup. </a>")
            return redirect('/')
            
        else:
            messages.error(request, "Email ID and password doesnot match. <a href = '/forgotPassword' style = 'color : black'> Click here to recover password. </a>")
            return redirect('/')
        
    else:
        return render(request, 'login.html')

def signup(request):
    #return HttpResponse("This is signup page")
    if request.method == 'POST':
        First_Name = request.POST['First_Name']
        Last_Name = request.POST['Last_Name']
        Email_ID = request.POST['Email_ID']
        User_Name = Email_ID
        Password = request.POST['Password']
        Confirm_Password = request.POST['Confirm_Password']
        
        if Password == Confirm_Password:   
            
            Alphabetic_Characters = False
            
            for characters in Password:
                if (characters.isalpha() == True):
                    Alphabetic_Characters = True
                    break
                        
            Numeric_Characters = any(map(str.isdigit, Password))
            Special_Characters = string.punctuation
            Special_Characters = any(map(lambda char: char in Special_Characters, Password))
            
            if User.objects.filter(email = Email_ID).exists():
                messages.info(request, "User already registered. <a href = '/' style = 'color : black'> Click here to login. </a>")
                return redirect('/signup')
            
            elif (len(Password) < 6) and (len(Password) <= 12):              
                messages.error(request, "Password should be atleast six characters and must not exceed 12 characters")                
                return redirect('/signup')
            
            elif ((Alphabetic_Characters == False) or (Numeric_Characters == False) or (Special_Characters == False)):
                    messages.error(request, "Password should contain atleast one alphanumeric character and atleast one special character")
                    return redirect('/signup')
                           
            else:
                User_Instance = User.objects.create_user(first_name = First_Name, last_name = Last_Name, email = Email_ID, username = User_Name, password = Password)
                User_Instance.save()
                Profile_Instance = Profile.objects.create(App_User = User_Instance)
                Profile_Instance.save()
                return redirect('/home')
            
        else:
            messages.error(request, "Passwords does not match.")
            return redirect('/signup')
        
    else:
        return render(request, 'signup.html')

def logout(request):
    #return HttpResponse("This is logout page")
    auth.logout(request)
    return redirect('/home')


def forgotPassword(request):
    #return HttpResponse("This is logout page")
    if request.method == 'POST':
        Email_ID = request.POST['Email_ID']
        
        if User.objects.filter(email = Email_ID).exists() == False:
            messages.info(request, "User not registered. <a href = '/signup' style = 'color: black'> Click here to signup. </a>")
            return redirect('/forgotPassword')
        
        else:
            User_Instance = User.objects.filter(username = Email_ID).first()
            Token = str(uuid.uuid4())
            Profile_Instance = Profile.objects.get(App_User = User_Instance)
            Profile_Instance.Reset_Password_Token = Token
            Profile_Instance.save()
            User_Account_Recovery_Email_Token(User_Instance, Token)
            messages.success(request, "<p style = 'color: black'>Password reset link sent to email. </p>")
            return redirect('/forgotPassword')
    else:
        return render(request, 'forgotPassword.html')

def changePassword(request, token):
    #return HttpResponse("This is logout page")
    Profile_Instance = Profile.objects.filter(Reset_Password_Token = token).first()
    Context = {'User_ID' : Profile_Instance.App_User.id, 'token' : token}
    
    if request.method == 'POST':
        New_Password = request.POST['New_Password']
        Confirm_New_Password = request.POST['Confirm_New_Password']
        User_ID = request.POST['User_ID']
        
        if New_Password == Confirm_New_Password:   
            
            Alphabetic_Characters = False
            
            for characters in New_Password:
                if (characters.isalpha() == True):
                    Alphabetic_Characters = True
                    break
                        
            Numeric_Characters = any(map(str.isdigit, New_Password))
            Special_Characters = string.punctuation
            Special_Characters = any(map(lambda char: char in Special_Characters, New_Password))
            
            if (len(New_Password) < 6) and (len(New_Password) <= 12):              
                messages.error(request, "Password should be atleast six characters and must not exceed 12 characters")                
                return redirect(f'/changePassword/{token}/')
            
            elif ((Alphabetic_Characters == False) or (Numeric_Characters == False) or (Special_Characters == False)):
                messages.error(request, "Password should contain atleast one alphanumeric character and atleast one special character")
                return redirect(f'/changePassword/{token}/')
                           
            else:
                try: 
                    User_Instance = User.objects.get(id = User_ID)
                except Exception as e:print(e)
                User_Instance.set_password(New_Password)
                User_Instance.save()
                messages.success(request, "Password changed successfully. <a href ='/' style = 'color : black'> Click here to login. </a>")
                return redirect('/')
        
        else:
            messages.error(request, "Passwords does not match.")
            return redirect(f'/changePassword/{token}/')
        
    return render(request, 'changePassword.html', Context)

def home(request):
    #return HttpResponse("This is home page")
    Songs = Song.objects.all().order_by('-Song_Released').values()
    context = {'Songs' : Songs}
    return render(request, 'home.html', context)

def search(request):
    #return HttpResponse("This is search page")
    #order_by('-Song_Released').values() sort Song objects in descending order
    if request.method == 'POST':
        
        Search_Results = request.POST.get('Search_Results')
        Search_Results = Search_Results.title()
        Songs = Song.objects.filter(Song_Title = Search_Results)
        
        if len(Songs) == 0:
            Songs = Song.objects.filter(Song_Artist = Search_Results).order_by('-Song_Released')
            
        if len(Songs) == 0:
            messages.info(request, "<div class='message' style='position: relative; top: 100px; padding-bottom: 156px'> <h5> No results found by search. </h5> </div>")
            return redirect('/search')
        
        messages.info(request, "<div class='message' style='position: relative; top: 15px;'> <h3> Search Results </h3> </div>") 
        context = {'Songs' : Songs, 'Flag' : 1}
        return render(request, 'search.html', context)
    
    return render(request, 'search.html')

def aboutSong(request, slug):
    #There can be slugs with same slug name (Slug in database). So to access objects in first slug.
    Songs = Song.objects.filter(Slug = slug).first()
    context = {'Song' :Songs}
    print(Context)
    return render(request, 'aboutSong.html', context)

def addASongToMusicApp(request):
    #return HttpResponse("This is addASongToMusicApp page")
    
    Song_Audio_Path = FileSystemStorage(location='Media/SongAudios')
    Song_Cover_Path = FileSystemStorage(location='Media/SongCovers')
    Song_Video_Path = FileSystemStorage(location='Media/SongVideos')
    
    if request.method == 'POST':
        
        Song_Title = request.POST['Song_Title']
        Song_Artist = request.POST['Song_Artist']
        Slug = Song_Title + "_By_" + Song_Artist
        Slug = Slug.split()
        Slug = "_".join(Slug)
        
        if 'Song_Featured_Artist' in request.POST:
            Song_Featured_Artist = request.POST['Song_Featured_Artist']
        else:
            Song_Featured_Artist = None
        
        Song_Released = request.POST['Song_Released']
        
        if 'Song_Lyrics' in request.POST:
            Song_Lyrics = request.POST['Song_Lyrics']
        else:
            Song_Lyrics = " "
        
        Song_Audio = request.POST.get('Song_Audio')    
        Song_Audio_File = request.FILES['Song_Audio']
        
        Song_Duration = request.POST['Song_Duration']
        
        Song_Cover = request.POST.get('Song_Cover')
        Song_Cover_File = request.FILES['Song_Cover']
        
        Song_Video_Flag = 0
        if 'Song_Video' in request.POST:
            Song_Video = request.POST.get('Song_Video')
            Song_Video_File = request.FILES['Song_Video']
            Song_Video_Flag = 1
        else:
            Song_Video_File = None
            Song_Video = None
            
        Song_Description = request.POST['Song_Description']
        
        Song_Audio_File_Name = Song_Audio_File.name  
        Song_Audio_File_Name = Song_Audio_File_Name.split()
        Song_Audio_File_Name = "_".join(Song_Audio_File_Name)
        print(Song_Audio_File_Name)
        Song_Audio_Path.save(Song_Audio_File_Name, Song_Audio_File)
        
        Song_Cover_File_Name = Song_Cover_File.name  
        Song_Cover_File_Name = Song_Cover_File_Name.split()
        Song_Cover_File_Name = "_".join(Song_Cover_File_Name)
        print(Song_Cover_File_Name)
        Song_Cover_Path.save(Song_Cover_File_Name, Song_Cover_File)
        
        if (Song_Video_Flag == 1):
            Song_Video_File_Name = Song_Video_File.name  
            Song_Video_File_Name = Song_Video_File_Name.split()
            Song_Video_File_Name = "_".join(Song_Video_File_Name)
            print(Song_Video_File_Name)
            Song_Video_Path.save(Song_Video_File_Name, Song_Video_File)
        else:
            Song_Video_File_Name = " "
                
        Song_Upload_Instance = Song(Slug = Slug, Song_Title = Song_Title, Song_Artist = Song_Artist, Song_Featured_Artist = Song_Featured_Artist, Song_Released = Song_Released, Song_Lyrics = Song_Lyrics, Song_Audio = Song_Audio, Song_Audio_File_Name = Song_Audio_File_Name, Song_Duration = Song_Duration, Song_Cover = Song_Cover, Song_Cover_File_Name = Song_Cover_File_Name, Song_Video = Song_Video, Song_Video_File_Name = Song_Video_File_Name, Song_Description = Song_Description)
        Song_Upload_Instance.save()
        
    return render(request, 'addASongToMusicApp.html')

def contact(request):
    #return HttpResponse("This is contact page")
    if request.method == 'POST':
        First_Name = request.POST['First_Name']
        Last_Name = request.POST['Last_Name']
        Email_ID = request.POST['Email_ID']
        
        if 'Phone_Number' in request.POST:
            Phone_Number = request.POST['Phone_Number']
        else:
            Phone_Number = None
        
        Description = request.POST['Description']
        Contact_Instance = Contact(First_Name = First_Name, Last_Name = Last_Name, Email_ID = Email_ID, Phone_Number = Phone_Number, Description = Description)
        Contact_Instance.save()
        
    return render(request, 'contact.html')