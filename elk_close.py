#!/usr/bin/python

import os,re,datetime

#检索ES所有打开的索引
#提取出来的格式为（项目名-2018.10.10）
elk_index = os.popen("curl -XGET http://172.16.41.115:9200/_cat/indices?v |grep open |awk '{print $3}'").read().split()


for index in elk_index:
        #正则匹配出日期(2018.10.10)
        index_date_str = re.findall(r'(\d*\.\d*\.\d*)',index)
        if index_date_str:
                #转换日期格式
                index_date = datetime.datetime.strptime(index_date_str[0],'%Y.%m.%d')
                date_now = datetime.datetime.now()
                #距离当前为几天
                delta = date_now - index_date
                if delta.days > 6:
                        #关闭7天前打开的索引
                        index_close = 'http://172.16.41.115:9200/%s/_close' %(index)
                        os.popen("curl -XPOST %s" %(index_close))

 
