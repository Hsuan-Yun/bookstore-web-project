from django.shortcuts import render, redirect
from .models import Member, Product, Images, Author, Publisher, Comment, Order_product, Order_data
from datetime import date, datetime
from django.contrib.auth import logout, login, authenticate
from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User

#首頁
def index_view(request):
    #會員
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount=auth_user.username)
            username = member.memberName[:2]
        except Member.DoesNotExist:
            username = None
    
        context = {'username': username, 'isMember': True}
        return render(request, 'index.html', context)
    
    #訪客
    else:
        return render(request, 'index.html', {'isMember': False})

#會員註冊
@csrf_exempt
def member_register_view(request):
    #會員，重新導向會員中心
    if request.user.is_authenticated:
        return redirect('member_centre')
    
    #訪客，接收註冊資料
    else:
        #接收註冊資料
        if request.method == 'POST':
            name = request.POST['name']
            account = request.POST['account']
            password = request.POST['password']
            passwordcheck = request.POST['passwordcheck']
            birthday = request.POST['birthday']
            email = request.POST['email']

            #確認密碼錯誤
            if password != passwordcheck:
                alert_script = "<script>window.alert('確認密碼錯誤！');</script>"
                return render(request, 'member_register.html', {'alert_script': alert_script})

            #帳號已被註冊
            if Member.objects.filter(memberAccount=account).exists():
                alert_script = "<script>window.alert('帳號已被註冊！');</script>"
                return render(request, 'member_register.html', {'alert_script': alert_script})
            
            #計算當前年齡
            birthday = datetime.strptime(birthday, '%Y-%m-%d').date()

            today = date.today()
            age = today.year - birthday.year
            if today.month < birthday.month or (today.month == birthday.month and today.day < birthday.day):
                age -= 1

            #新建會員資料
            new_member = Member(memberName=name, memberAccount=account, memberPassword=password, memberBirthday=birthday, memberAge=age, memberEmail=email)
            new_member.save()

            #會員資料存入auth_user
            username = new_member.memberAccount
            password = new_member.memberPassword
            user = User.objects.create_user(username=username, password=password)
            user.save()

            #登入
            login(request, user)

            #發送註冊成功信
            email_template = render_to_string(
                'register_success.html',
                {'username': new_member.memberName}
            )
            email = EmailMessage(
                '感謝您的註冊',
                email_template,
                settings.EMAIL_HOST_USER,
                [new_member.memberEmail]
            )
            email.fail_silently = False
            email.send()

            #註冊，導向信箱確認
            return redirect('member_email')

        #資料傳輸錯誤
        elif request.method == 'GET':
            return render(request, 'member_register.html')

#信箱確認
@csrf_exempt
def member_email_view(request):
    #會員
    if request.user.is_authenticated:

        #接收信箱確認資料
        if request.method == 'POST':
            emailcheck = request.POST.get('emailcheck')

            auth_user = request.user

            try:
                member = Member.objects.get(memberAccount=auth_user.username)
            except Member.DoesNotExist:
                member = None

            #收到信件，導向首頁
            if emailcheck == 'receive':
                return redirect('index')

            #未收信件
            elif emailcheck == 'notreceive':
                if member:
                    email = request.POST.get('email')
                    member.memberEmail = email
                    member.save()

                    #發送註冊成功信
                    email_template = render_to_string(
                        'register_success.html',
                        {'username': member.memberName}
                    )
                    email = EmailMessage(
                        '感謝您的註冊',
                        email_template,
                        settings.EMAIL_HOST_USER,
                        [member.memberEmail]
                    )
                    email.fail_silently = False
                    email.send()

            #重新導向信箱確認
            return redirect('member_email')

        #資料傳輸錯誤
        elif request.method == 'GET':
            return render(request, 'member_email.html')

    #訪客，重新導向會員登入
    else:
        return redirect('member_login')

#會員登入
@csrf_exempt
def member_login_view(request):
    #會員，重新導向會員中心
    if request.user.is_authenticated:
        return redirect('member_centre')
    
    #訪客
    else:
        if request.method == 'POST':
            account = request.POST['account']
            password = request.POST['password']

            user = authenticate(request, username=account, password=password)

            #驗證成功
            if user is not None:
                login(request, user)
                return redirect('index')
            else:
                alert_script = "<script>window.alert('帳號或者密碼錯誤！');</script>"
                return render(request, 'member_login.html', {'alert_script': alert_script})

        return render(request, 'member_login.html')

#會員中心
def member_centre_view(request):
    #會員
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount = auth_user.username)
            context = {'member': member}
        except Member.DoesNotExist:
            context = {'member': None}

        return render(request, 'member_centre.html', context)
    
    #訪客，重新導向會員登入
    else:
        return redirect('member_login')

#更改資料
@csrf_exempt
def member_profile_view(request):
    #會員
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount = auth_user.username)
            context = {'member': member}
        except Member.DoesNotExist:
            context = {'member': None}

        if request.method == 'POST':
            name = request.POST['name']
            birthday = request.POST['birthday']
            phone = request.POST['phone']
            address = request.POST['address']

            if name:
                member.memberName = name
            
            if birthday:
                member.memberBirthday = birthday

            if phone:
                member.memberPhone = phone
            
            if address:
                member.memberAddress = address

            member.save()

            return redirect('member_centre')

        return render(request, 'member_profile.html', context)
    
    #訪客，重新導向會員登入
    else:
        return render(request, 'member_profile.html', {'isMember': False})

#點數查詢
def member_point_view(request):
    #會員
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount = auth_user.username)
            context = {'member': member}
        except Member.DoesNotExist:
            context = {'member': None}

        return render(request, 'member_point.html', context)
    
    #訪客，重新導向會員登入
    else:
        return redirect('member_login')

#書籍資訊
def book_detail_view(request, id):
    #會員
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount = auth_user.username)
            username = member.memberName[:2]
        except Member.DoesNotExist:
            username = None

        try:
            book = Product.objects.get(product_id = id)
            cover = Images.objects.get(product_id = book.product_id)
            author = Author.objects.get(author_id = book.author_id)
            publisher = Publisher.objects.get(publisher_id = book.publisher_id)
            comment = Comment.objects.filter(product_id = book.product_id)
            context = {
                'username': username,
                'isMember': True,
                'book': book,
                'cover': cover,
                'author': author,
                'publisher': publisher,
                'comment': comment
            }
        except Member.DoesNotExist:
            context = {
                'username': username,
                'isMember': True,
                'book': None,
                'cover': None,
                'author': None,
                'publisher': None,
                'comment': None
            }
        return render(request, 'book_detail.html', context)
    
    #訪客，重新導向會員登入
    else:
        return render(request, 'book_detail.html', {'isMember': False})

def checkout_page_view(request):
    #會員
    if request.user.is_authenticated:
        return render(request, 'checkout_page.html', {'isMember': True})
    
    #訪客，重新導向會員登入
    else:
        return redirect('member_login')

def search_results_view(request):
    if request.user.is_authenticated:

        auth_user = request.user
        
        try:
            member = Member.objects.get(memberAccount=auth_user.username)
            username = member.memberName[:2]
        except Member.DoesNotExist:
            username = None
    
        context = {'username': username, 'isMember': True}
        return render(request, 'search_results.html', context)
    
    else:
        return render(request, 'search_results.html', {'isMember': False})

def shopping_cart_view(request):
    if request.user.is_authenticated:
        return render(request, 'shopping_cart.html', {'isMember': True})
    else:
        return render(request, 'shopping_cart.html', {'isMember': False})
    
def logout_view(request):
    logout(request)
    return redirect('index')