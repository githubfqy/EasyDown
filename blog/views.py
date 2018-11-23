from django.shortcuts import render,render_to_response,get_object_or_404
from django.http import HttpResponse,HttpResponseRedirect
from django.template import RequestContext
from blog.models import User,Article,Tag,ArticleComment,Category,Message
from django.contrib.auth.hashers import make_password,check_password
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import Http404
from django.conf import settings
from blog.forms import ArticleCommentForm
from django.utils.timezone import now

# Create your views here.
def home(request):  # 主页
    is_login = request.session.get('IS_LOGIN',False)
    if is_login:
        posts = Article.objects.all()  # 获取全部的Article对象
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
        page = request.GET.get('page')  # 获取URL中page参数的值
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        nickname = request.session['nickname']
        return render(request, 'home.html', {'post_list': post_list, 'nickname': nickname})
    return render_to_response('Home_unlog.html')

def detail(request, id):  # 查看文章详情
    try:
        post = Article.objects.get(article_id=str(id))
        post.viewed()   # 更新浏览次数
        tags = post.tags.all()  # 获取文章对应所有标签
    except Article.DoesNotExist:
        raise Http404
    comments = ArticleComment.objects.filter(article = str(id))
    paginator = Paginator(comments, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        comment = ArticleCommentForm(request.POST)
        if comment.is_valid():
            message = comment.cleaned_data['body']
            user_name = request.session['username']
            nick_name = request.session['nickname']
            article = Article.objects.get(article_id = str(id))
            newrecord = ArticleComment()
            #newrecord.username = user_name
            newrecord.body = message
            newrecord.article = id
            newrecord.username = user_name
            newrecord.nickname = nick_name
            newrecord.title = post.title
            newrecord.save()
            user = User.objects.get(username = user_name)
            user.comment()
            return render(request,'com_return.html',{'article':id})
    else:
        comment = ArticleCommentForm()
    previous_post = Article.objects.filter(article_id=str(id-1))
    if previous_post and id!=0:
        previous_post = Article.objects.get(article_id=str(id-1))
    next_post = Article.objects.filter(article_id=str(id+1))
    if next_post:
        next_post = Article.objects.get(article_id=str(id+1))
    return render(request, 'post.html', {'post': post, 'tags': tags,'comment':comment,'comment_list':comment_list,'previouspost':previous_post,'nextpost':next_post})

def register(request):
    if request.method =='POST':
        user_name = request.POST.get('username','')
        pass_word_1 = request.POST.get('password_1','')
        pass_word_2 = request.POST.get('password_2','')
        nick_name = request.POST.get('nickname','')
        email = request.POST.get('email','')
        if User.objects.filter(username = user_name):
            return render(request,'register.html',{'error':'用户已存在'})
            #将表单写入数据库
        if(pass_word_1 != pass_word_2):
            return render(request, 'register.html', {'error': '两次密码请输入一致'})
        user = User()
        user.username = user_name
        user.password = make_password(pass_word_1)
        user.email = email
        user.nickname = nick_name
        user.save()
            #返回注册成功页面
        return render_to_response('home_unlog.html')
    else:
        return render(request,'register.html')



def login(request):
    if request.method == 'POST':
        user_name = request.POST.get('username','')
        pass_word = request.POST.get('password','')
            #pass_word = make_password(pass_word)
        user = User.objects.filter(username=user_name)
        if user:
            user = User.objects.get(username = user_name)
               #if check_password(pass_word,user[0]['password']):

            if check_password(pass_word,user.password):
                request.session['IS_LOGIN'] = True
                request.session['nickname'] = user.nickname
                request.session['username'] = user_name
                return render(request,'Home_log.html',{'user':user})
            else:
                return render(request,'login.html',{'error': '密码错误!'})
        else:
            return render(request, 'login.html', {'error': '用户名不存在!'})
    else:
        return render(request,'login.html')





def reset_password(request):
    if request.method == 'POST':
        pass_word = request.POST.get('password','')
        pass_word1 = request.POST.get('password1','')
        pass_word2 = request.POST.get('password2','')
        user_name = request.session['username']
        user = User.objects.get(username = user_name)
        if check_password(pass_word,user.password):
            if pass_word1 == pass_word2:
                user.password = make_password(pass_word1)
                user.save()
                return render_to_response('user_info.html')
        else:
            return render(request,'reset.html', {'error': '密码错误'})
    else:
        return render(request,'reset.html')


def forget_password(request):
    if request.method == 'POST':
        user_name = request.POST.get('username','')
        email = request.POST.get('email','')
        user = User.objects.filter(username = user_name)
        if user:
            user = User.objects.get(username = user_name)
            if(user.email == email):
                return render(request,'for_setpass.html')
            else:
                return render(request,'forget.html',{'error':'您的用户名和邮箱不匹配！'})
        else:
            return render(request,'forget.html',{'error':'请输入正确的用户名'})
    else:
        return  render(request,'forget.html')

#def for_resetpass(request):
def forget_set(request):
    if request.method == 'POST':
        pass_word1 = request.POST.get('password1','')
        pass_word2 = request.POST.get('password2','')
        user_name = request.session['user_name']
        user = User.objects.get(username = user_name)
        if pass_word1 == pass_word2:
            user.password = make_password(pass_word1)
            user.save()
            return render_to_response('login.html')
        else:
            return render(request,'for_setpass.html', {'error': '两次密码输入不一致！'})
    else:
        return render(request,'for_setpass.html')

def home_unlog(request):  # 主页
    return render(request, 'Home_unlog.html')
'''
def category(request):
    try:
        catetories = Article.objects.category.all()
    except Article.DoesNotExist:
        raise Http404
    return render_to_response('category.html',{'cate_list':catetories})
'''


def tags(request):
    nickname = request.session['nickname']
    tags = Tag.objects.all()
    paginator = Paginator(tags, settings.TAG_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        tags = paginator.page(page)
    except PageNotAnInteger:
        tags = paginator.page(1)
    except EmptyPage:
        tags = paginator.page(paginator.num_pages)
    return render_to_response('tags.html', {'tag_list': tags,'nickname':nickname})

def tag_detail(request,id):
    posts =Article.objects.filter(tags = id)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'tags_detail.html', {'post_list': post_list})

def user_info(request):
    user_name = request.session['username']
    user = User.objects.get(username = user_name)
    comments = ArticleComment.objects.filter(username = user_name)
    paginator = Paginator(comments, settings.COMMENT_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)
    return render_to_response('user_info.html',{'user':user,'comment_list':comment_list})

def log_out(request):
    del request.session['IS_LOGIN']
    del request.session['username']
    del request.session['nickname']
    return render_to_response('Home_unlog.html')

def comment_del(request,comment_id):
    user_name = request.session['username']
    user = User.objects.get(username = user_name)
    ArticleComment.objects.filter(id=str(comment_id)).delete()
    user.comment_del()
    comments = ArticleComment.objects.filter(username = user_name)
    paginator = Paginator(comments, settings.COMMENT_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        comment_list = paginator.page(page)
    except PageNotAnInteger:
        comment_list = paginator.page(1)
    except EmptyPage:
        comment_list = paginator.page(paginator.num_pages)
    return render_to_response('user_info.html',{'user':user,'comment_list':comment_list,'msg':'删除成功'})

def category(request,id):
    posts =Article.objects.filter(category_id = str(id))
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'category.html', {'post_list': post_list})

def app(request):
    app = Category.objects.get(name = '软件')
    posts =Article.objects.filter(category_id = app.id)
    paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
    page = request.GET.get('page')  # 获取URL中page参数的值
    try:
        post_list = paginator.page(page)
    except PageNotAnInteger:
        post_list = paginator.page(1)
    except EmptyPage:
        post_list = paginator.page(paginator.num_pages)
    return render(request, 'app.html', {'post_list': post_list})

def contact(request):
    if request.method =='POST':
        username = request.POST.get('username','')
        email = request.POST.get('email','')
        message = request.POST.get('message','')
        mes = Message()
        mes.username = username
        mes.email = email
        mes.content = message
        mes.save()
        return render(request,'contact.html',{'msg':'留言成功'})
    return render(request,'contact.html')

def search(request):
    if request.method =='POST':
        search_info = request.POST.get('info','')
        posts = Article.objects.filter(title__icontains = search_info)
        paginator = Paginator(posts, settings.PAGE_NUM)  # 每页显示数量，对应settings.py中的PAGE_NUM
        page = request.GET.get('page')  # 获取URL中page参数的值
        try:
            post_list = paginator.page(page)
        except PageNotAnInteger:
            post_list = paginator.page(1)
        except EmptyPage:
            post_list = paginator.page(paginator.num_pages)
        return render(request, 'search.html', {'post_list': post_list})
    return render(request,'home.html')