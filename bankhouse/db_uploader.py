import os
import django
import csv
import sys

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bankhouse.settings') 
django.setup() 

from posts.models import * 



CSV_PATH_PRODUCTS = './CSV/posts.csv'  # 가지고있는 CSV경로도 변수화 해서 저장
with open(CSV_PATH_PRODUCTS) as in_file: # CSV_PATH_PRODUCTS 경로에서 in_file 이란 이름으로 파일열기
    data_reader = csv.reader(in_file)  # 데이터 한줄 씩 읽기
    next(data_reader, None) # 첫줄을 스킵하기위해 추가
    for row in data_reader:  
        if row[0]:
            menu_name = row[0]
            update, create = Menu.objects.update_or_create(name=menu_name)
    update.save()

CSV_PATH_PRODUCTS= './CSV/category.csv'
with open(CSV_PATH_PRODUCTS) as in_file: 
    data_reader = csv.reader(in_file) 
    next(data_reader, None)
    for row in data_reader:  
        print(row)
    #     if row[0]:
    #         menu_name = row[0]
    #     category_name = row[1]
    #     menu_id=Menu.objects.get(name=menu_name)
    #     update, create = Category.objects.update_or_create(menu=menu_id, name=category_name)
    # update.save()