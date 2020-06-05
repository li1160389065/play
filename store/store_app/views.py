import os
import pymysql
import redis
from django.conf import settings
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from decimal import Decimal
def con_mysql():
    return pymysql.connect(host='127.0.0.1',port=3306,user='root',passwd='root',db='store',charset='utf8')
# 读取表的数据
def read(table_name,num):
    conn = con_mysql()
    cur=conn.cursor()
    cur.execute("select * from %s" % table_name)
    r=list(cur.fetchall())
    d={}
    for i in range(len(r)):
        d[r[i][num]]=[r[i][j] for j in range(len(r[i]))]
    conn.commit()
    # 关闭游标
    cur.close()
    # 关闭连接
    conn.close()
    return d
def read_order(table_name,who,key,num):
    conn = con_mysql()
    cur=conn.cursor()
    cur.execute("select * from %s where %s=%s" % (table_name,who,key))
    r=list(cur.fetchall())
    d={}
    for i in range(len(r)):
        d[r[i][num]]=[r[i][j] for j in range(len(r[i]))]
    conn.commit()
    cur.close()
    conn.close()
    return d
def find(a,b,c):
    r=read(a,b)
    d={}
    for keys,values in r.items():
        if keys==c:
            for i in range(len(values)):
                d['a'+str(i)]=values[i]
    return d
def show(a,b):
    r=read(a,b)
    lists=[]
    for keys,values in r.items():
        d = {}
        for i in range(len(values)):
            d['a'+str(i)]=values[i]
        lists.append(d)
    return lists
#判断
def  decide_login(user_account,pass_word):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select * from user where account='%s'"%user_account)
    a=cursor.fetchall()
    conn.commit()
    cursor.close()
    if len(a)>0:
        if user_account==a[0][1] and pass_word==a[0][3]:
            return True
        else:
            return False
    else:
        return False
def  decide(user_account):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select account from user where account='%s'"%user_account)
    a=cursor.fetchall()
    conn.commit()
    cursor.close()
    if len(a)>0:
        return  True
    else:
        return  False
#查找权限
def permission(cook):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("select power from user where account='%s'" % cook)
    a = cursor.fetchall()
    conn.commit()
    cursor.close()
    return a[0][0]
#添加
def insert_type(type_id,table_name,):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into goods_type values('%s','%s')"%(type_id,table_name))
    conn.commit()
    cursor.close()
def insert_into(user_account,user_name,pass_word,user_phone):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into user(account,username,password,phone) values('%s','%s','%s','%s')"%(user_account,user_name,
                                                                                pass_word,user_phone))
    conn.commit()
    cursor.close()
def insert_member(user_account,user_name,pass_word,user_phone,user_power,user_photos):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into user(account,username,password,phone,power,picture) values('%s','%s','%s','%s','%s',"
                   "'%s')"%(user_account,user_name,pass_word,user_phone,user_power,user_photos))
    conn.commit()
    cursor.close()
def insert_goods(goods_id,name,goods_type,price,number,unit,picture,intr):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into goods values('%s','%s','%s','%s','%s','%s','%s','%s')"%(goods_id,
                                                        name,goods_type,price,number,unit,picture,intr))
    conn.commit()
    cursor.close()
def insert_order(goods_id,name,price,number,picture,user):
    conn=con_mysql()
    cursor=conn.cursor()
    cursor.execute("insert into car values('%s','%s','%s','%s','%s','%s')"%(goods_id,
                                                        name,price,number,picture,user))
    conn.commit()
    cursor.close()
#修改
def change_goods(goods_cook,new_id,new_name,new_title,new_price,new_num,new_unit,new_photos,new_intr):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update goods set goods_id='%s',goods_name='%s',title='%s',price='%s',num='%s',unit='%s ',goods_picture='%s',"
                   "intr='%s'where goods_id='%s' " % (new_id,new_name,new_title,new_price,new_num,new_unit,new_photos,new_intr,goods_cook))
    conn.commit()
    cursor.close()
def change_member(goods_cook,new_name,new_password,new_phone,new_power,new_photos):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set username='%s',password='%s',phone='%s',power='%s',"
                   "picture='%s 'where account='%s' " % (new_name,new_password,new_phone,new_power,new_photos,goods_cook))
    conn.commit()
    cursor.close()
def change_personal(goods_cook,new_name,new_password,new_phone,new_photos):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set username='%s',password='%s',phone='%s',"
                   "picture='%s 'where account='%s' " % (new_name,new_password,new_phone,new_photos,goods_cook))
    conn.commit()
    cursor.close()
def change_money(user,new_money):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("update user set  money='%s' where account='%s' " % (new_money,user))
    conn.commit()
    cursor.close()

#删除
def delete(table,who,key):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from %s where %s=%s"%(table,who,key))
    conn.commit()
    cursor.close()
def delete_big(big):
    conn = con_mysql()
    cursor = conn.cursor()
    cursor.execute("delete from %s " % (big))
    conn.commit()
    cursor.close()
# Create your views here.

# 登录
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    else:
        user = request.POST.get('Account')
        password = request.POST.get('PassWord')

        if user is '':
            return render(request,'login.html',context={'err':"请输入用户名()"})
        elif user == 'root' and password == 'root':
            cook = redirect("index", permanent=False)
            cook.set_cookie(key="cook", value=user, max_age=1200)
            return cook
        else:
            if not user.isdigit():
                return render(request,'login.html',context={'err':'用户名格式错误，请重新输入(仅数字)'})
            elif not password.isalnum():
                return render(request,'login.html',context={'err':'密码格式错误，请重新输入(仅数字或字母)'})
            else:
                if decide_login(user,password) is False:

                    return render(request,'login.html',context={'err':'用户或者密码错误'})
                else:
                    cook = redirect("index", permanent=False)
                    cook.set_cookie(key="cook", value=user,max_age=1200)
                    return cook


# 注册
def register(request):
    if request.method=='GET':
        return render(request,'register.html')
    else:
        new_account = request.POST.get('account')
        new_password = request.POST.get('password')
        again_password = request.POST.get('again_password')
        new_phone=request.POST.get('phone')
        new_name=request.POST.get('username')

        if  '' in [new_account,new_name,new_password,again_password,new_phone]:
            return render(request,'register.html',context={'err':'均必填，请写全'})
        elif not new_account.isdigit():
            return render(request, 'register.html', context={'err': '用户名格式错误，请重新输入(仅数字)'})
        elif new_password!=again_password:
            return render(request, 'register.html', context={'err': '前后密码不一致'})
        elif decide(new_account) is True:
            return render(request, 'register.html', context={'err': '该用户已存在'})
        else:
            insert_into(new_account,new_name,new_password,new_phone)
            return redirect('login')
# 退出
def login_out(request):
    response = redirect('index')
    response.delete_cookie('cook')
    return response
#验证cookie
def cook(func):
    def get_cook_from(request,*args):
        get_cook=request.COOKIES.get('cook')
        if  get_cook is None:
            return redirect('login')
        return func(request,*args)
    return get_cook_from
#主页面
def index(request):
    get_cook=request.COOKIES.get('cook')
    print(request.COOKIES.get('12'))
    f=show('goods', 0)
    goods_type = read('goods_type', 0)
    goods = read('goods', 0)
    paginator = Paginator(f,8)
    try:
        # GET请求方式  get()获取指定Key值所对应的Value值
        # 获取index的值 如果没有 则设置使用默认值1
        num = request.GET.get('index', '1')
        # number 表示某一页的内容
        number = paginator.page(num)
    except PageNotAnInteger:
        # 如果输入的页码数不是是整数  那么显示第一页数据
        number = paginator.page(1)
    except EmptyPage:
        # 如果页码数不在当前页码范围内 则显示最后一页
        # paginator.num_pages 获取当前总页数
        # paginator.page()获取指定的某一页
        number = paginator.page(paginator.num_pages)
        # number代表一页的内容， paginator代表所有页的内容
        #  return render(request, 'index.html', {'page': number, 'paginator': paginator})
    if get_cook is None:
        condition = {'a1':'登录','a2': '注册'}
        return render(request, 'index.html', context={'power': condition,'goods':goods,'page': number, 'paginator': paginator,'types':goods_type})
    elif get_cook=='root':
        condition = {'a3': '注销',  'a6': '后台管理中心'}
        return render(request, 'index.html', context={'user':get_cook,'power': condition,'goods':goods,'page': number, 'paginator': paginator,'types':goods_type})
    elif permission(get_cook)==2:
        condition = {'a1': '', 'a2': '', 'a3': '注销', 'a4': '个人中心', 'a5': '购物车', 'a6': '后台管理中心'}
        return render(request, 'index.html', context={'user':get_cook,'power': condition,'goods':goods,'page': number, 'paginator': paginator,'types':goods_type})
    else:
        condition = {'a1': '', 'a2': '', 'a3': '退出', 'a4': '个人中心', 'a5': '购物车', 'a6': ''}
        return render(request,'index.html',context={'user':get_cook,'power':condition,'goods':goods,'page': number, 'paginator': paginator,'types':goods_type})

#后台管理
@cook
def management(request):
    goods = read('goods', 0)
    get_cook = request.COOKIES.get('cook')
    return render(request, 'management.html', context={'user': get_cook, 'goods':goods})
#后台管理  人员
@cook
def manage_member(request):
    number = read('user',1)
    get_cook = request.COOKIES.get('cook')
    if get_cook=='root':
        return render(request, 'manage_member.html', context={'user': get_cook, 'number': number})
    else:
        return render(request, 'management_two.html', context={'user': get_cook, 'number': number})
#修改人员信息
@cook
def member_change(request,key):
    get_id=find('user',1,key)

    if request.method == "GET":
        return render(request, 'member_change.html',context={'member': get_id,'user':key})
    else:

        new_member_username= request.POST.get('new_member_username')
        new_member_password= request.POST.get('new_member_password')
        new_member_phone=request.POST.get('new_member_phone')
        new_member_power= request.POST.get('new_member_power')
        new_member_picture= request.FILES.get('new_member_picture')
        new_picture="%s.jpg"%key
        if new_member_password=='':
            return render(request, 'member_change.html', context={'member':get_id,'users':key,'err': '密码不能为空'})
        elif not new_member_picture:
            change_member(key, new_member_username, new_member_password,
                          new_member_phone, new_member_power, new_picture)
            get_id = find('user',1, key)
            return render(request, 'member_change.html', context={'member': get_id, 'users':key,'err':"修改成功已保存"})
        else:

            img = os.path.join(settings.MEDIA_ROOT,new_picture)
            with open(img, 'wb') as f:
                for i in new_member_picture.chunks():
                    f.write(i)
            change_member(key,new_member_username,new_member_password,
                          new_member_phone,new_member_power,new_picture)
            get_id = find('user',1,key)
            return render(request,'member_change.html',context={'member':get_id,'users':key,'err':"修改成功已保存"})
#添加人员
@cook
def member_add(request):
    if request.method == "GET":
        return render(request, 'member_add.html')
    else:
        member_account = request.POST.get('member_account')
        member_username = request.POST.get('member_username')
        member_password = request.POST.get('member_password')
        member_phone = request.POST.get('member_phone')
        member_power = request.POST.get('member_power')
        member_picture = request.FILES.get('member_picture')
        pictures = "%s.jpg" % member_username

        if member_account == '':
            return render(request, 'member_add.html',{'err':'成员账号不能为空'})
        elif not member_picture:
            insert_member(member_account, member_username, member_password, member_phone, member_power, pictures)
            return render(request, 'member_add.html',{'err':'添加成功'})
        else:

            img = os.path.join(settings.MEDIA_ROOT,pictures)
            with open(img, 'wb') as f:
                for i in member_picture.chunks():
                    f.write(i)
            insert_member(member_account,member_username,member_password,member_phone,member_power,pictures)
            return render(request, 'member_add.html',{'err':'添加成功'})
#删除人员
@cook
def member_delete(request,key):
    delete('user', 'account', key)
    return redirect('/store_app/manage_member/')
# 添加分类
@cook
def goods_type_add(request):
    goods_type = read('goods_type', 0)
    if request.method=='GET':
        return render(request,'goods_type.html',context={'types':goods_type})
    else:
        new_id = request.POST.get("new_id")
        new_type=request.POST.get("new_type")

        insert_type(new_id,new_type)
        goods_type=read('goods_type',0)
        return render(request, 'goods_type.html',context={'types':goods_type,'err':'添加成功'})
#商品分类查找
def goods_list(request,key):
    goods_type = read('goods_type', 0)
    f=show('goods where title=(select sort from goods_type where type_id=%s)'%key,0)
    paginator = Paginator(f,10)
    try:
        num = request.GET.get('index', '1')
        number = paginator.page(num)
    except PageNotAnInteger:
        number = paginator.page(1)
    except EmptyPage:
        number = paginator.page(paginator.num_pages)

    if request.method=='GET':
        return render(request,'goods_list.html',context={'types':goods_type,'page': number, 'paginator': paginator})
    else:
        goods_find=request.POST.get('goods_find')
        finds=show("goods where locate('%s',title)>0 or locate('%s',goods_name)>0"%(goods_find,goods_find),0)
        paginator = Paginator(finds, 5)
        try:
            num = request.GET.get('index', '1')
            number = paginator.page(num)
        except PageNotAnInteger:
            number = paginator.page(1)
        except EmptyPage:
            number = paginator.page(paginator.num_pages)
        return render(request, 'goods_list.html',context={'types':goods_type,'page': number, 'paginator': paginator})



#添加商品
@cook
def goods_add(request):
    if request.method == "GET":
        return render(request, 'goods_add.html')
    else:
        goods_id= request.POST.get('goods_id')
        goods_name= request.POST.get('goods_name')
        goods_type= request.POST.get('goods_type')
        goods_price=request.POST.get('goods_price')
        goods_num = request.POST.get('goods_num')
        goods_unit = request.POST.get('goods_unit')
        goods_picture= request.FILES.get('goods_picture')
        goods_intr = request.POST.get('goods_intr')
        pictures = "%s.jpg" % goods_name

        if goods_id == '':
            return render(request, 'goods_add.html',{'err':'商品编号不能为空'})
        elif not goods_picture:
            insert_goods(goods_id, goods_name, goods_type, goods_price, goods_num, goods_unit, pictures, goods_intr)
            return render(request, 'goods_add.html', {'err': '添加成功'})
        else:

            img = os.path.join(settings.MEDIA_ROOT,pictures)
            with open(img, 'wb') as f:
                for i in goods_picture.chunks():
                    f.write(i)
            insert_goods(goods_id,goods_name,goods_type,goods_price,goods_num,goods_unit,pictures,goods_intr)
            return render(request, 'goods_add.html',{'err':'添加成功'})
#修改商品
@cook
def goods_change(request,key):
    get_id=find('goods',0,key)
    if request.method == "GET":
        return render(request, 'goods_change.html',context={'goods': get_id,'key':key})
    else:
        new_goods_id= request.POST.get('new_goods_id')
        new_goods_name= request.POST.get('new_goods_name')
        new_goods_type= request.POST.get('new_goods_type')
        new_goods_price=request.POST.get('new_goods_price')
        new_goods_num= request.POST.get('new_goods_num')
        new_goods_unit = request.POST.get('new_goods_unit')
        new_goods_picture= request.FILES.get('new_goods_picture')
        new_goods_intr = request.POST.get('new_goods_intr')
        new_picture= "%s.jpg" % new_goods_name
        if new_goods_id=='':
            return render(request, 'goods_change.html', context={'goods':get_id,'users':key,'err': '商品编号'})
        elif not new_goods_picture:
            change_goods(key, new_goods_id, new_goods_name, new_goods_type, new_goods_price,new_goods_num,new_goods_unit,
                         new_picture, new_goods_intr)
            get_id = find('goods', 0, key)
            return render(request, 'goods_change.html', context={'goods': get_id, 'users':key,'err':"修改成功已保存"})
        else:

            img = os.path.join(settings.MEDIA_ROOT,new_picture)
            with open(img, 'wb') as f:
                for i in new_goods_picture.chunks():
                    f.write(i)
            change_goods(key, new_goods_id, new_goods_name, new_goods_type, new_goods_price, new_goods_num,
                         new_goods_unit,new_picture, new_goods_intr)
            get_id = find('goods', 0, key)
            return render(request,'goods_change.html',context={'goods':get_id,'users':key,'err':"修改成功已保存"})
#删除商品
@cook
def goods_delete(request,key):
    delete('goods','goods_id',key)
    return redirect('/store_app/management/')
#商品详情
@cook
def goods_date(request,key):
    get_cook = request.COOKIES.get('cook')
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    r.lrem('%s'%get_cook,0,key)
    r.lpush('%s'%get_cook,key)
    r.ltrim('%s'%get_cook,0,9)
    goods=find('goods',0,key)
    return render(request, 'goods.html', context={'goods':goods})
#个人中心
@cook
def personal(request):
    get_cook = request.COOKIES.get('cook')
    get_id = find('user', 1, get_cook)
    return render(request, 'personal.html',context={'user':get_id})

#修改个人信息
@cook
def personal_change(request,key):
    get_id=find('user',1,key)
    if request.method == "GET":
        return render(request, 'personal_change.html',context={'member': get_id,'user':key})
    else:
        new_username= request.POST.get('new_username')
        new_password= request.POST.get('new_password')
        new_phone=request.POST.get('new_phone')
        new_member_picture= request.FILES.get('new_picture')
        new_picture="%s.jpg"%key
        if new_password=='':
            return render(request, 'personal_change.html', context={'member':get_id,'users':key,'err': '密码不能为空'})
        elif not new_member_picture:
            change_personal(key, new_username, new_password,new_phone, new_picture)
            get_id = find('user',1, key)
            return render(request, 'personal_change.html', context={'member': get_id, 'users':key,'err':"修改成功已保存"})
        else:
            img = os.path.join(settings.MEDIA_ROOT,new_picture)
            with open(img, 'wb') as f:
                for i in new_member_picture.chunks():
                    f.write(i)
            change_personal(key, new_username, new_password, new_phone, new_picture)
            get_id = find('user',1,key)
            return render(request,'personal_change.html',context={'member':get_id,'users':key,'err':"修改成功已保存"})
#充值中心
@cook
def add_money(request):
    get_cook = request.COOKIES.get('cook')
    user_date= read_order('user', 'account', get_cook, 0)

    for key, value in user_date.items():
        money=value[7]
    if request.method == 'GET':
        return render(request, 'add_money.html')
    else:
        money_add= request.POST.get('money_add')
        if money_add<='0':
            return render(request, 'add_money.html',context={'err':'请输入大于等于0的数(小数最多2位)'})
        else:
            money+=Decimal(money_add)
            change_money(get_cook,money)
            return render(request,'add_money.html',context={'err':'充值成功'})

#下单
@cook
def order(request,key):
    get_cook = request.COOKIES.get('cook')
    get_id = find('goods', 0, key)
    if request.method == "GET":
        return render(request, 'order.html')
    else:
        num=request.POST.get('num')
        if num<'0':
            return render(request, 'order.html',context={'err':'请输入正整数'})
        else:
            insert_order(get_id['a0'],get_id['a1'],get_id['a3'],num,get_id['a6'],get_cook)
            return render(request, 'order.html',context={'err':'下单成功','user':get_cook})
#购物车
@cook
def order_list(request,key):
    get_cook = request.COOKIES.get('cook')
    a=Decimal(0.00)
    lists=read_order('car','user_name',get_cook ,0)
    user_power=permission(get_cook)
    user_date = read_order('user', 'account', get_cook, 0)
    for key, value in user_date.items():
        money = value[7]
    for key, value in lists.items():
        a+=value[2]*value[3]
    end_price=a*(10-user_power)/10
    new_money=money-end_price
    print(new_money)
    if request.method == "GET":
        return render(request, 'order_list.html',context={'lists':lists,'a':a,'end_price':end_price})
    else:
        if new_money<0.00:
            return render(request, 'order_list.html',context={'lists':lists,'a':a,'end_price':end_price,'err':'余额不足请充值','err1':'前往充值'})
        else:
            delete_big('car where user_name=%s'%get_cook)
            change_money(get_cook, new_money)
            return render(request, 'order_list.html',context={'lists':lists,'a':a,'end_price':end_price,'err':'支付成功'})
#删除购物车
@cook
def order_delete(request,key):
    get_cook = request.COOKIES.get('cook')
    delete_big("car where goods_id=%s and user_name=%s"%(key,get_cook))
    return redirect('/store_app/order_list/%s/'%get_cook)

#最近浏览记录
@cook
def recent(request):
    get_cook = request.COOKIES.get('cook')
    pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
    r = redis.Redis(connection_pool=pool)
    recent_goods=r.lrange('%s'%get_cook,0,9)
    goods_li=[]
    for i in recent_goods:
        good=show("goods where goods_id=%s"%i,0)

        goods_li.append(good)
    return  render(request,'recent_browse.html',context={'goods_li':goods_li})



