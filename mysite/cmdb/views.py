# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from cmdb import models
from django.shortcuts import HttpResponse
from django.http import JsonResponse
from django.forms.models import model_to_dict
import json
from django.core import serializers
# Create your views here.
from django.views.decorators.cache import cache_page
# 引入自定义模块
from cmdb.myfunction import to_mysql
from cmdb.myfunction import to_json
from cmdb.myfunction import get_token
# 导入excel
import xlrd
import uuid
import random
from .models import Image

@cache_page(60 * 15)  # 秒数，这里指缓存 15 分钟，不直接写900是为了提高可读性
# 数据库中读取数据
def index(request):
    if request.method == "POST":
        # 获取 session：禁止同样的信息添加两次
        aaa = request.session.get("username", default=None)
        username = request.POST.get("username", None)
        password = request.POST.get("password", None)
        ages = request.POST.get("ages", None)
        # 使用缓存
        if aaa == username:
            return HttpResponse("You've already commented.")
        else:
            # 创建或修改 session：
            request.session["username"] = username
            models.Userinfo.objects.create(user=username, pwd=password, ages=ages,)

    user_list = models.Userinfo.objects.all()
    return render(request, "index.html", {"data": user_list})
# 在地址栏上做加减法
def adds(request):
    # 获取 session：禁止同样的信息添加两次
    aaa = request.session.get("username", default=None)
    a = request.GET.get('a', 0)
    b = request.GET.get('b', 0)
    # int() 转成 整型 str()  转成字符串类型
    c = int(a) + int(b)
    # 输出字符串必须用HttpResponse
    return render(request, "adds.html", {"data": aaa})
# 跳转到logins 页面
def logins(request):
    return render(request, "logins.html")
# 传递一个数组或字典 到 网页，在显示出来
def get_list(request):
    # 创建整列函数 ，从0 - 100as
    token = request.POST.get("token", None)
    if token == "123":
        name_dict = {
            'resCode': "200",
            'resMsg': "成功",
            'resData': {
               'twz': 'Love python and Django', 'zqxt': 'I am teaching Django'
            },
        }
    else:
        name_dict = {
            'resCode': "500",
            'resMsg': "token为空",
            'resData': {},
        }
    data_list = {
        'code': "200",
        'list': serializers.serialize("json", models.Userinfo.objects.all())
    }

    return JsonResponse(data_list, content_type='application/json')

# 导入excel表格到数据库
def excel_import(request):
    # 读取传递的参数
    file_excel = request.POST.get('file_url')
    by_name = request.POST.get('table_name')
    # 用户未传入表名，则 默认 sheet1
    if by_name == None:
        by_name = 'Sheet1'
    # # 本地 excel 的地址
    # file_excel = 'C:/Users/Administrator/Desktop/data.xls'
    # # 代表第几张表
    # by_name = 'Sheet1'
    data = xlrd.open_workbook(file_excel)
    table = data.sheet_by_name(by_name)
    n_rows = table.nrows  # 行数
    row_dict = {}
    for row_num in range(1, n_rows):
        row = table.row_values(row_num)
        seq = {'user': row[0], 'pwd': row[1], 'ages': row[2], 'sex': row[3]}
        row_dict[row_num] = seq

    da = {
        'code': '200',
        'msg': '成功',
        'data': row_dict
    }
    # 调用方法 ---自定义模板函数 这里必须要return
    return to_mysql(da)
    # return JsonResponse(da, content_type='application/json')

# 登陆的方法
def login(request):
    name = (request.POST.get('name') if request.POST.get('name') != None else "")
    # 三元表达式
    pwd = (request.POST.get('pwd') if request.POST.get('pwd') != None else "")
    # 从数据库中获取一列，并将queryset转成dist格式
    pwd_d = model_to_dict(models.Userinfo.objects.get(user=name))
    print pwd_d
    if name == "" or pwd == "":
        data_list = {
            'code': "500",
            'result': False,
            'data': {'msg': "账号或密码为空", 'token': ''}
        }
    else:
        if pwd != pwd_d[u'pwd']:
            data_list = {
                'code': "200",
                'result': True,
                'data': {'msg': "密码错误", 'token': ''}
            }
        else:
            # 登陆成功，数据库中存入token
            to = get_token()
            # 生成随机数
            token = models.Userinfo.objects.get(id=pwd_d[u'id'])
            # 更新
            token.token = to
            # 保存
            token.save()
            data_list = {
                'code': "200",
                'result': True,
                'data': {'msg': "验证通过", 'token': to}
            }

    return JsonResponse(data_list, content_type='application/json')

import os
# 子进程
import multiprocessing
import time
def upload_file(request):
    if request.method == "POST":    # 请求方法为POST时，进行处理
        myFile =request.FILES.get("myfile", None)    # 获取上传的文件，如果没有文件，则默认为None
        if not myFile:
            return HttpResponse("no files for upload!")

        destination = open(os.path.join("F:\django\mysite\static\media", myFile.name), 'wb+')    # 打开特定的文件进行二进制的写操作
        for chunk in myFile.chunks():      # 分块写入文件
            destination.write(chunk)
        destination.close()

        p = multiprocessing.Process()
        p.start()
        n = 1
        if n < 10:
            n = n + 1
            return JsonResponse({'time': n}, content_type='application/json')
            p.terminate()
        else:
            return JsonResponse({'time': "upload over"}, content_type='application/json')




