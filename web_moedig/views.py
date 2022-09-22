from ast import If
from lib2to3.pgen2.token import NAME
from logging import exception
from sqlite3 import paramstyle
from django.shortcuts import render, redirect
from django.http import HttpResponse

from moedig.settings import RAZORPAY_API_KEY, RAZORPAY_SECRET_API_KEY
from . models import Contact, Newsletter, Profile, Product, Order , Coupon , Employee
from django.contrib import messages , admin
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout 
from django.contrib.auth.decorators import login_required
import uuid
from django.contrib.sites.shortcuts import get_current_site
from django.conf import settings
from django.core.mail import send_mail
import json, ast , os
import razorpay
from django.views.decorators.csrf import csrf_exempt


from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes


# Create your views here.


def home(request):
    if request.user.is_authenticated:
        products = Product.objects.filter(
            user=request.user, order_id=None).all()

        json_dict = {}
        sum = 0
        for product in products:

            json_items = product.items_json
            json_list = json.loads(json_items)
            json_dict.update(json_list)

            sum += float(product.price)

        params = {'products': products, 'json_list': json_dict, 'sum': sum}
        return render(request, 'web_moedig/index.html', params)

    return render(request, 'web_moedig/index.html')


@login_required(login_url="/loginSignup/")
def checkout(request):

    if request.method == 'GET':
        try:
            products = Product.objects.filter(
                user=request.user, order_id=None).all()
            if not products:
                return HttpResponse('Please add some product before getting into checkout')
        except:
            pass

        json_dict = {}
        sum = 0
        for product in products:

            json_items = product.items_json
            json_list = json.loads(json_items)
            json_dict.update(json_list)

            sum += float(product.price)

        params = {'products': products, 'json_list': json_dict, 'sum': sum}
        return render(request, 'web_moedig/checkoutPage.html', params)

    if request.method == 'POST':
        order_id = str(uuid.uuid4())
        user = request.user
        delivery = request.POST.get('delivery')
        delivery = delivery.split(' ')[0]
        slot = request.POST.get('hslot')
        coupon = request.POST.get('coupon')
        phone = request.POST.get('phone')
        

        products = Product.objects.filter(
            user=request.user, order_id=None).all()
        product_json = []
        sum = 0

        for product in products:
            json_str = json.loads(product.items_json)
            product_json.append(json_str)
            sum += float(product.price)
        if not(coupon == ''):
            try:
                real_coupon = Coupon.objects.filter(coupon=coupon).first()
                if real_coupon:
                    sum = round((sum - (sum*real_coupon.discount*0.01)),2)
                    messages.success(request,'Your Coupon Is Applied')
                else:
                    messages.error(request,'Invalid Coupon')
            except:
                sum = sum
        json_product = json.dumps(product_json)
        pickup = 'pickupp'
        # sum = int(sum)
        client = razorpay.Client(
            auth=(RAZORPAY_API_KEY, RAZORPAY_SECRET_API_KEY))
        payment = client.order.create(
            {"amount": sum*100, "currency": "INR", "payment_capture": "1"})
        print(payment)

        order = Order(order_id=order_id, user=user, delivery=delivery, tslot=slot,
                      product_json=json_product, bill=sum, pickup=pickup, payment_id=payment['id'],phone=phone)
        order.save()

        call_back_url = 'http://' + \
            str(get_current_site(request))+"/success/"

        return render(request, 'web_moedig/checkoutPage.html', {'payment': payment, 'order': order, 'callback_url': call_back_url, 'products': products, 'sum': sum})

        messages.success(request, 'saved order')

    return render(request, 'web_moedig/checkoutPage.html')


@csrf_exempt
def success(request):
    
    if request.method == 'POST':
        a = request.POST
        try:
            for key, val in a.items():
                if key == "razorpay_order_id":
                    order_id = val
                    break
            print(order_id)

            order = Order.objects.filter(payment_id=order_id).first()
            order.payment_status = True
            order.save()

            print(order.payment_status)

            if order.payment_status:
                try:
                    user = order.user
                    login(request, user)
                    products = Product.objects.filter(user=request.user,order_id=None).all()
                    for product in products:
                        product.order_id = order
                        product.save()
                except:
                    print('This part isn"t working')

            return render(request, 'web_moedig/success.html', {'a': a, 'order_id': order_id})
        except:
            b = request.POST
            return render(request, 'web_moedig/success.html', {'b': b})
    
    else:
        return redirect('home')
        
    if not (request.user.is_authenticated):
        return redirect('home')

    return render(request, 'web_moedig/success.html')


@login_required(login_url='/loginSignup/')
def order(request):
    orders = Order.objects.filter(user=request.user, payment_status=True).all()
    return render(request, 'web_moedig/order.html', {'orders': orders})


def pricing(request):
    if request.method == 'POST':
        email = request.POST.get('news_email')
        newsletter = Newsletter(email=email)
        newsletter.save()
        messages.success(request, 'You are now added to our Newsletter!')
        return redirect('/')
    return render(request, 'web_moedig/pricing.html')


def about(request):
    return render(request, 'web_moedig/aboutus.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name', default='')
        email = request.POST.get('email', default='')
        phone = request.POST.get('phone', default='')
        message = request.POST.get('message', default='')

        if len(name) < 1 or len(email) < 5 or len(phone) < 10:
            messages.error(request, 'Please fill your form correctly!')
        else:
            contact = Contact(name=name, email=email,
                              phone=phone, message=message)
            contact.save()
            messages.success(
                request, f'Your form has been submitted, We will contact you soon!')
    return render(request, 'web_moedig/contact.html')


def send_mail_after_registration(email, token):
    subject = 'Your accounts need to be verified'
    message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


def loginSignup(request):

    if request.method == 'POST':
        if 'signup_submit' in request.POST:
            username = request.POST.get('username')
            name = request.POST.get('sname')
            email = request.POST.get('email')
            email = email.lower()
            pass1 = request.POST.get('pswd1')
            pass2 = request.POST.get('pswd2')

            # checking the errors in form fillup

            if User.objects.filter(username=username).first():
                messages.error(
                    request, 'This username already exists, please choose a different username!')
                return redirect('loginSignup')

            if User.objects.filter(email=email).first():
                messages.error(
                    request, 'This email already exists, please choose a different email!')
                return redirect('loginSignup')

            if len(username) > 16:
                messages.error(
                    request, 'username can not be greater than 15 characters')
                return redirect('loginSignup')

            # if name.isalnum():
            #     messages.error(request, 'Please write the name correctly!')
            #     return redirect('loginSignup')

            if not username.isalnum():
                messages.error(
                    request, 'username should only contain letters and numbers')
                return redirect('loginSignup')

            if pass1 != pass2:
                messages.error(request, 'Passwords do not match')
                return redirect('loginSignup')

            # creating user
            my_user = User.objects.create_user(username, email, pass1)
            my_user.first_name = name
            my_user.save()
            messages.success(request, 'Your Account has been Created!')

            auth_token = str(uuid.uuid4())
            profile_obj = Profile.objects.create(
                user=my_user, auth_token=auth_token)
            profile_obj.save()
            send_mail_after_registration(email, auth_token)
            messages.success(request, 'Email has been send!')

            return redirect('home')

        if 'login_submit' in request.POST:
            username = request.POST.get('login_username')
            password = request.POST.get('login_pswd')

            user_obj = User.objects.filter(username=username).first()

            profile_obj = Profile.objects.filter(user=user_obj).first()

            print(user_obj)

            if not (username == 'Moedig_Technologies'):
                if not profile_obj.is_verified:
                    messages.error(
                        request, 'Profile is not verified check your mail.')
                    return redirect('loginSignup')

            user = authenticate(username=username, password=password)

            if user is not None:
                login(request, user)
                next = request.POST.get('next')
                if next:
                    return redirect(next)
                messages.success(request, 'You are now logged In!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid Credentials!')
                return redirect('home')

        else:
            return render(request, 'web_moedig/loginSignup.html')

    return render(request, 'web_moedig/loginSignup.html')


@login_required(login_url="/")
def handleLogout(request):
    logout(request)
    messages.success(request, 'You are logged out successfully!')
    return redirect('home')


def verify(request, auth_token):
    try:
        profile_obj = Profile.objects.filter(auth_token=auth_token).first()

        if profile_obj:
            if profile_obj.is_verified:
                messages.success(request, 'Your account is already verified.')
                return redirect('home')
            profile_obj.is_verified = True
            profile_obj.save()
            messages.success(request, 'Your account has been verified.')
            return redirect('home')
        else:
            return HttpResponse('invalid token')
    except Exception as e:
        print(e)
        return redirect('/')


def upload(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            uploaded_file = request.FILES['uploadFile']
            info_json = request.POST.get('info_json')
            total_price = request.POST.get('total_price')
            product = Product(uploaded_file=uploaded_file,
                              user=request.user, items_json=info_json, price=total_price)
            product.save()
            messages.success(request, 'image uploaded!')

            return redirect('home')
    else:
        messages.error(request, 'Please Login First')
        return redirect('/')

    return render(request, 'web_moedig/index.html')


@login_required(login_url='/loginSignup/')
def delete(request, slug):
    product = Product.objects.filter(id=slug).first()
    os.remove(os.path.join(settings.MEDIA_ROOT,product.uploaded_file.name))
    product.delete()
    messages.success(request, f'{product.uploaded_file} is deleted ')
    return redirect('home')


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            data = data.lower()
            associated_users = User.objects.filter(Q(email=data))
            if associated_users.exists():
                for user in associated_users:
                    subject = "Password Reset Requested"
                    email_template_name = "web_moedig/password_reset/password_reset_email.txt"
                    c = {
                        "email": user.email,
                        'domain': '127.0.0.1:8000',
                        'site_name': 'Moedig_Technologies',
                        "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                        "user": user,
                        'token': default_token_generator.make_token(user),
                        'protocol': 'http',
                    }
                    email = render_to_string(email_template_name, c)
                    try:
                        send_mail(subject, email, 'himmu1144@gmail.com',
                                  [user.email], fail_silently=False)
                    except BadHeaderError:
                        return HttpResponse('Invalid header found.')
                    return redirect("/reset_password_done/")
            else:
                messages.error(request,"User Doesn't Exist")
                return redirect('/password_reset_request/')
        
    password_reset_form = PasswordResetForm()
    return render(request=request, template_name="web_moedig/password_reset/password_reset_view.html", context={"password_reset_form": password_reset_form})




def adminDashboard(request):

    if request.user.is_authenticated:
        user = request.user
        if not(user.username == "Moedig_Technologies"):
            return redirect('home')
        else:
            orders = Order.objects.filter(payment_status=True).all()
            profiles = Profile.objects.all()
            employee_names = []
            for profile in profiles:
                if profile.is_employee:
                    employee_names.append(profile.user.username)
            params = {'orders':orders,'enames':employee_names}
            return render(request,'web_moedig/adminDashboard.html',params)
    else:
        messages.error(request,'please log in first')
    return render(request,'web_moedig/adminDashboard.html')

def adminview(request,id):
    order = Order.objects.filter(order_id=id).first()
    products = Product.objects.filter(order_id=order).all()
    params = {'products':products}

    if request.method == 'GET': 
        status = request.GET.get('stats')
        if status:
            order.delivery_status = status
            order.save()
    return render(request,'web_moedig/adminview.html',params)

def employee(request):
    if request.method=='POST':
        name = request.POST.get('employee')
        id_order = request.POST.get('id_order')
        try:
            employee = Employee.objects.filter(order_id=id_order).first()
            if employee:
                return redirect('home')
        except:
            pass
        
        if name:
            user = User.objects.filter(username=name).first()
        else:
            print('not name')

        employee = Employee(user=user,order_id=id_order)
        employee.save()
        messages.success(request,'Forwarded To '+name)
    else:
        return HttpResponse('None')
    return redirect('adminDashboard')

def employeeDashboard(request):
    if request.user.is_authenticated:
        profile_obj = Profile.objects.filter(user=request.user).first()
        if profile_obj.is_employee == True:
            try:
                employees = Employee.objects.filter(user=request.user).all()
            except exception as e:
                error = e
            if employees:
                employees = {'employees':employees}
                return render(request,'web_moedig/employeeDashboard.html',employees)
        else:
            return HttpResponse('You are not suthorized!')
    else:
        return redirect('home')
    return render(request,'web_moedig/employeeDashboard.html')


def employeeview(request,id):
    order = Order.objects.filter(order_id=id).first()
    products = Product.objects.filter(order_id=order).all()
    params = {'products':products}
    if request.method == 'GET': 
        statuus = request.GET.get('statss')
    if statuus:
        order.delivery_status = statuus
        order.save()
    return render(request,'web_moedig/employeeview.html',params)