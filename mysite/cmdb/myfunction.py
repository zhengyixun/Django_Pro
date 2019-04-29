#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time : 2019/4/15 15:45 
# @Author : xx
# @File : myfunction.py
from cmdb import models
import random
from django.core import serializers
# from django.core import serializers
from django.shortcuts import HttpResponse
from django.http import JsonResponse
def to_mysql(data):
    a = data['data']
    x = 0
    if data['code'] != '200':
        return JsonResponse({'error': '表格格式异常'}, content_type='application/json')
    else:
        for key in a:
            arrs = a[key]
            if models.CmdbUserinfo.objects.filter(user=arrs['user']).exists():
                x = x + 1
            else:
                models.CmdbUserinfo.objects.create(user=arrs['user'], pwd=arrs['pwd'], ages=arrs['ages'], sex=arrs['sex'])
        # user_list = models.UserInfo.objects.all()
        # ajax_testvalue = serializers.serialize("json", user_list)
        datas = {
            'msg': '导入成功, %x 条重复数据' %(x) ,
            'code': '200'
        }
        return JsonResponse(datas, content_type='application/json')
# 转成json
def to_json(data):
    return serializers.serialize("json", data)
# 随机生成token   ##########-##########-##########
def get_token():
    # 设置随机字符串
    str_seed = 'ahf0ur21o2132354pqawfWlakwf[1iAFDASFADc0=3rd[lsdqEd30RIqQ3LF-[SEG*L/M068413157q803R4kva3944e596f253sasdwdafae09sakl'
    # 设置随机数的范围---设置取第几位字符串
    # 生成字符串
    str_arr = []
    # 循环三次
    for i in range(3):
        str = '-'
        a = []
        # 从字符串随机选择字符
        for i in range(10):
            num = random.randint(1, 110)
            a.append(str_seed[num])
        arr = ''
        arr = arr.join(a)
        # 存到str_arr 中
        str_arr.append(arr)
    # 拼接str_arr
    strings = '-'
    strings = strings.join(str_arr)
    # 返回
    return strings


