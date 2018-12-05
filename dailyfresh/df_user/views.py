# encoding=utf-8
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect,JsonResponse
from models import *
from hashlib import sha1
# Create your views here.


def register(request):  # 登录页面显示视图
    return render(request,'df_user/register.html')


def register_handle(request): # 登录页面提交处理视图
    # 接收用户输入

    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')

    # 判断两次密码
    if upwd != upwd2:
        return redirect('/user/register/')
    # 密码加密
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    # 创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功转到登录页面
    return redirect('/user/login/')


def register_exist(request):  # 判断注册用户是否存在的ajax请求视图
    uname = request.GET.get('uname')
    print(uname)
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count':count})


def login(request):  # 登录页面显示视图
    uname = request.COOKIES.get('uname','')
    context = {'title':'登录','error_name':0,'error_pwd':0,'uname':uname}
    return render(request,'df_user/login.html',context)


def login_handle(request):  # 登录页面提交处理视图
    # 接收请求信息
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu',0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # 判断 如果未查到用户名错,用户名正确判断密码,密码正确转到用户中心
    if len(users) == 1: # 如果用户名正确
        s1 = sha1()
        s1.update(upwd)
        if s1.hexdigest() == users[0].upwd : #如果密码正确
            red = HttpResponseRedirect('/user/info/')
            if jizhu!=0 : # 如果记住被勾选
                red.set_cookie('uname',uname,max_age=3600*24) # 注意如果不设置max_age cooie在浏览器关闭后过期
            else:
                red.set_cookie('uname',max_age=-1) # 清空cookie 立刻过期
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red # 用户密码正确,重定向到/user/info/ 用户中心
        else: #密码错误
            context = {'titlle': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'titlle':'用户登录','error_name':1,'error_pwd':0,'uname':uname,'upwd':upwd}
        return render(request,'df_user/login.html',context)


def info(request): # 用户中心信息页面
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_name = request.session['user_name']
    context={'title': '用户中心','user_email':user_email,'user_name':user_name}
    return render(request, 'df_user/user_center_info.html', context)


def order(request): # 用户中心订单页面
    return render(request,'df_user/user_center_order.html',context={'title':'用户中心'})


def site(request): # 用户中心地址管理页面 包括修改提交的处理
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method=="POST":
        post=request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title':'用户中心','user':user}
    return render(request,'df_user/user_center_site.html',context)



