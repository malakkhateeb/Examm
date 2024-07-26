from django.shortcuts import render, redirect
from .models import*
from django.contrib import messages
# this method render the main page to add Registration or to log in 
def logIn(request):
    context={
        'users':all_users(),
        'pies':all_pies()
    }
    return render(request, 'index.html', context)
# _______________________________________________________________________________
#this method to add new user to database
def addRegistrations(request):
    errors = User.objects.basic_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    if request.method == 'POST':
            user=add_regestraion(request.POST)
            request.session['user_id'] = user.id 
            messages.success(request, "Successfully registered")
            
    return redirect('/')
# -------------------------------------------------------------------------
#this method to add the email and passswored and hash the password and returns the error when logi with email and password invalid
def addLogin(request):
    errors = User.objects.basic_validatorlogin(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            # redirect the user back to the form to fix the errors
            return redirect('/')
    
    if request.method == 'POST':
        user = User.objects.filter(email=request.POST['email'])
        if user:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                request.session['user_id'] = logged_user.id
                return redirect('/dashboard')
        messages.error(request, 'Invalid login credentials')
        return redirect('/')
    return redirect('/')
# _________________________________________________________________________________________________________________________
# Displays the pie page if the user is logged in,Passes the logged-in user and all pies to the addfav.html template.
def pies(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'user': get_user_id(request.session['user_id']),
        'pies':all_pies()
    }
    
    return render(request, 'addpie.html', context)
# _____________________________________________________________________________________________________________________
# add new pie on addpie.html 
def addPies(request):
    if request.method == 'POST':
        errors = Pie.objects.basic_validatorpie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/dashboard')
        else:
            add_pies(request, request.POST)
            return redirect('/dashboard') 
# ______________________________________________________________
# it should access to audate page which its called edit.html
def updatePies(request, pie_id):
    get_pie = get_pie_id(pie_id)
    logged_in_user_id = request.session.get('user_id')
    context = {
        'pie': get_pie_id(pie_id),
        'user': get_user_id(request.session['user_id'])
    }
    if request.method == 'POST' and logged_in_user_id == get_pie.made_by.id:
        errors = Pie.objects.basic_validatorpie(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect(f'/pies/{pie_id}/update')
        else:
            update_pies(request.POST,pie_id)
            return redirect('/dashboard')
    
    return render(request, 'edit.html', context)
# _____________________________________________________________________
def deletePies(request):
    get_pie = get_pie_id(request.POST['id'])
    logged_in_user_id = request.session.get('user_id')
    if request.method == 'POST' and logged_in_user_id == get_pie.made_by.id:
        delete_pies(request.POST['id'])
    return redirect('/dashboard')
# ________________________________________________________________________
def allPies(request):
    context={
        'pies':all_pies()
    }
    return render (request, 'allpies.html', context)
# _________________________________________________________
def showPies(request, pie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'pie': get_pie_id(pie_id),
        'user': get_user_id(request.session['user_id'])
    }
    return render(request, 'show.html', context)
# Allows the logged-in user to add pies from their favorites.
def favoritePie(request, pie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user =  get_user_id(request.session['user_id'])
    pie = get_pie_id(pie_id)
    pie.users_who_like.add(user)
    return redirect(f'/pies/{pie_id}')
# _______________________________________________________________________________________
# Allows the logged-in user to remove apies from their favorites.
def unfavoritePie(request, pie_id):
    if 'user_id' not in request.session:
        return redirect('/')
    user = get_user_id(request.session['user_id'])
    pie = get_pie_id(pie_id)
    pie.users_who_like.remove(user)
    return redirect(f'/pies/{pie_id}')
# _____________________________________________________________________________________
def logOut(request):
    request.session.clear()
    return redirect('/')