from django.http import request
from django.http.response import HttpResponse
from .models import Account,UserProfile,FarmerProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib import messages,auth
from django.shortcuts import redirect, render
from django.contrib.auth.decorators import login_required

import random


import requests

# verification email


from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage

# Create your views here.




def register(request):
    if request.user.is_authenticated:
        return HttpResponse("Already logged in!!")

    
    if request.method == 'POST':
        first_name = request.POST['f_name']
        last_name = request.POST['l_name']
        em = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']


        if password != confirm_password:
            messages.error(request,"Passwords do not match!!")
            return redirect('register')
        
        
        phone = request.POST['phone']
        profile = request.POST['profile']
        email = em.lower()
        username = email.split('@')[0]
        check = None
        try:
            check = Account.objects.get(email = email)
            
        except:
            pass
        if check is not None:
            messages.error(request,"This email id is already in use!!")
            return redirect('register')
        user = Account.objects.create_user(first_name = first_name,last_name = last_name,email = email,username = username,password = password)
        user.profile = profile
        user.phone_number = phone
        user.save()
        if profile == 'farmer':
            farmer = FarmerProfile()
            farmer.user = user
            farmer.save()
            
        else:
            merchant = UserProfile()
            merchant.user = user
            merchant.save()

        current_site = get_current_site(request)


        mail_subject = "Please Verify your Account"
        message = render_to_string('accounts/account_verification_email.html',{
            'user' : user,
            'domain': current_site,
            'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
            'token' : default_token_generator.make_token(user)
        })
        to_email = email

        send_email = EmailMessage(mail_subject,message,to = [to_email])

        send_email.send()
        messages.info(request,'We have sent a verification email to you!! Please verify your account before logging in!!')
        return redirect('home')
        
        


    
    return render(request,'accounts/register.html')

def activate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)

    except:
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congratulations! Your Account is Activated')
        return redirect('login')

    else:
        messages.error(request,'Invalid Activation Link')
        return redirect('register')







def login(request):

    if request.method == 'POST':
        em = request.POST['email']
        password = request.POST['password']

        email = em.lower()
        
        user = authenticate(email = email,password = password)
        
        if user is not None:
            auth.login(request,user)
            messages.info(request, 'You are logged in')
            return redirect('home')
        else:   
            messages.warning(request, 'Invalid credentials')
            return redirect('login')


        
    return render(request,'accounts/login.html')


@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    return redirect('login')



def profile(request,username):
    user = Account.objects.get(username=username)
    data = None
    if user is not None:
        if user.profile == 'farmer':
            farmer = FarmerProfile.objects.get(user = user)

            data = {
                'profile' : farmer,
                'user_main' : user
            }

        else:
            merchant = UserProfile.objects.get(user = user)
            data = {
                'profile' : merchant,
                'user_main' : user
            }

        return render(request,'profile.html',data)

    else:
        return redirect('home')
        



@login_required(login_url='login')
def dashboard(request):

    user = request.user
    prof_instance = None
    
    if request.method == 'POST':
        if user.profile == 'farmer':
            prof_instance = FarmerProfile.objects.get(user = user)
        else:
            prof_instance = UserProfile.objects.get(user = user)

    
        first_name = request.POST['f_name']
        
        last_name = request.POST['l_name']

        phone = request.POST['phone']
        image = None
        try:
            image = request.FILES['img']
    
        except:
            image = prof_instance.image
        
        
        aadhar_number = request.POST['aadhar']


        address_line_1 = request.POST['address_line_1']
        
        address_line_2 = request.POST['address_line_2']
        
        city = request.POST['city']

        state = request.POST['state']

        country = request.POST['country']

        user.first_name = first_name
        user.last_name = last_name
        user.phone = phone

        user.save()

        prof_instance.image = image

        prof_instance.aadhar_number = aadhar_number
        prof_instance.address_line_1 = address_line_1
        prof_instance.address_line_2 = address_line_2
        prof_instance.city = city
        prof_instance.state = state
        prof_instance.country = country
        
        prof_instance.save()
        
        messages.success(request,"Your Profile has been updated!!")
        return redirect('dashboard')

    
    
    
    
    
    
    data = None
    if user.profile == 'farmer':
        prof = FarmerProfile.objects.get(user=user)
        data = {
            'user' : user,
            'profile' : prof
        }
    else:
        prof = UserProfile.objects.get(user=user)
        data = {
            'user' : user,
            'profile' : prof
        }
    
    return render(request,'accounts/dashboard.html',data)




@login_required(login_url='login')
def change_password(request):
    if request.method == 'POST':
        current_pass = request.POST['current_password']
        new_pass = request.POST['new_password']
        confirm_new_pass = request.POST['confirm_new_password']
        
        if new_pass != confirm_new_pass:
            messages.error(request,"Password and Confirm password do not match!!")
            return render('change_password')

        user  = request.user

        success = user.check_password(current_pass)

        if success:
            user.set_password(new_pass)
            user.save()
            messages.success(request,"Your password has been changed!! Please login")
            return redirect('change_password')

        else:
            messages.error(request,"Your current password does not match")
            return redirect('change_password')


    return render(request,'accounts/change_password.html')



def reset_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        email = email.lower()
        if Account.objects.filter(email = email).exists():
            user = Account.objects.get(email__iexact = email)
            current_site = get_current_site(request)

            mail_subject = "Reset Your Password"
            message = render_to_string('accounts/reset_password_email.html',{
                'user' : user,
                'domain': current_site,
                'uid' : urlsafe_base64_encode(force_bytes(user.pk)),
                'token' : default_token_generator.make_token(user)
            })
            to_email = email
            send_email = EmailMessage(mail_subject,message,to = [to_email])
            send_email.send()
            messages.success(request,"Password Reset Email Has Been Sent to Your Email")
            return redirect('login')
        else:
            messages.error(request,"Account Does Not exist")
            return redirect('reset_password')


    return render(request,'accounts/reset_password.html')




def reset_password_validate(request,uidb64,token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk = uid)

    except:
        user = None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid'] = uid
        messages.success(request,"Please Reset Your Password")

        return redirect('forgot_password')

    else:
        messages.error(request,"This Link Has Been Expired")
        return redirect('login')



def forgot_password(request):
    if request.method == 'POST':
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk = uid)
            user.set_password(password)
            user.save()
            messages.success(request,"Password Reset Successful")
            return redirect('login')
        else:
            messages.error(request,"Password does not Match")
            return redirect('forgot_password')
    else:
        return render(request, 'accounts/forgot_password.html')


def send_otp(mobile,otp):

    authKey = "OTk2o1zrBQqv0MWdDwX49jmnVCLelafiFphybUcZuPIYEAxJ3gJaxQXrkq8NFMEGKO0B75AztjbnUgow"
    url2 = "https://www.fast2sms.com/dev/bulkV2"



    querystring = {"authorization":authKey,"variables_values":otp,"route":"otp","numbers":mobile}


    headers = {
        'cache-control': "no-cache"
    }
    response = requests.request("GET", url2, headers=headers, params=querystring)
    print(response.text)
    return None

    








    
    
    
    
    






def login_otp(request):
    if request.method == 'POST':
        phone = request.POST['phone']
        user = None
        try:
            user = Account.objects.get(phone_number = phone)
        except:
            pass
        
        if user is not None:
            otp = str(random.randint(1000,9999))
            user.otp = otp
            user.save()
            send_otp(phone,otp)
            request.session['mobile'] = phone
            messages.info(request,"Otp has been sent to your phone number")
            return redirect('otp_verify')

        else:
            messages.warning(request,"Your Phone number is not registered with us!!")
            return redirect('login_otp')

        


    return render(request,'accounts/login_otp.html')



def otp_verify(request):
    if request.method == 'POST':
        otp = request.POST['otp']
        phone = request.session['mobile']
        user = Account.objects.get(phone_number = phone)

        if user is None:
            messages.warning(request,"Invalid request")
            return redirect('login_otp')
        
        if user.otp == otp:
            auth.login(request,user)
            messages.success(request,"You are now logged in!!")
            return redirect("dashboard")
        
        else:
            messages.warning(request,"OTP is not correct please enter again")
            return redirect('otp_verify')


    return render(request,"accounts/otp_verify.html")



def view_profile(request, id):
    print("View Enter Final")
    a_id = Account.objects.get(id = id)
    print(a_id)
    profile_type = a_id.profile
    a_name = a_id.full_name()
    p_info = {
        "pname": a_name,
        "email": a_id.email, 
        "phone_no": a_id.phone_number,
    }
    print(profile_type)
    if(profile_type == "farmer"):
        f_id = FarmerProfile.objects.get(user=a_id)
        print(f_id)
        print(f_id.state)
        p_info["address1"] = f_id.address_line_1
        p_info["city"] = f_id.city
        p_info["state"] = f_id.state
        p_info["country"] = f_id.country
        p_info["image"] = f_id.image
        p_info["adhr_no"] = f_id.aadhar_number
    
    else:
        m_id = UserProfile.objects.get(user=a_id)
        p_info["address1"] = m_id.address_line_1
        p_info["city"] = m_id.city
        p_info["state"] = m_id.state
        p_info["country"] = m_id.country
        p_info["image"] = m_id.image
        p_info["adhr_no"] = m_id.aadhar_number

    data = {
        'p_info': p_info,
    }

    print(p_info)


    return render(request,'accounts/user_profile.html', data)
    



def get_farmer_profile(Request, fob):
    print(fob)
    farmer_ob = FarmerProfile.objects.get(user=fob)
    print(farmer_ob)
    account = Account.objects.get(id=farmer_ob)
    print(account)
    acc_id = account.id
    print(acc_id)

    
    
    return redirect('view_profile', acc_id)



    return render(request,"accounts/otp_verify.html")





def farmers(request):

    all_farmers = FarmerProfile.objects.all()

    data = {
        'all_farmers' : all_farmers
    }

    return render(request , 'accounts/farmers.html', data)



def merchants(request):
    
    all_merchants = UserProfile.objects.all()

    data = {
        'all_merchants' : all_merchants
    }

    return render(request , 'accounts/merchants.html' , data)
