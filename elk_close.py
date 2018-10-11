#!/usr/bin/python
#author:hong
#update:2018.10.10
#description: elk日志处理，7天以上的关闭索引，30天以上的删除索引


import os,re,datetime,requests,time
#elasticsearch ip地址
es_ip = "172.16.41.115"
#关闭索引天数
close_day = 7
#删除索引天数
delete_day = 30
#获取当前时间
date_now = datetime.datetime.now()

def elk_close(es_ip,close_day):
    elk_open_index = os.popen("curl -XGET http://%s:9200/_cat/indices?v |grep open |awk '{print $3}'" %(es_ip)).read().split()
    for index in elk_open_index:
        #正则匹配出日期(2018.10.10)
        index_date_str = re.findall(r'(\d*\.\d*\.\d*)',index)
        if index_date_str:
            index_date = datetime.datetime.strptime(index_date_str[0], '%Y.%m.%d')
            #与现在相差天数
            delta = (date_now - index_date).days
            if delta > close_day:
                index_close = 'http://%s:9200/%s/_close' % (es_ip,index)
                os.popen("curl -XPOST %s" % (index_close))

def elk_delete(es_ip,delete_day):
    elk_all_index = os.popen("curl -XGET http://%s:9200/_cat/indices?v |awk '{print $3}'" %(es_ip)).read().split()
    for index in elk_all_index:
        #正则匹配出日期(2018.10.10)
        index_date_str = re.findall(r'(\d*\.\d*\.\d*)',index)
        if index_date_str:
            index_date = datetime.datetime.strptime(index_date_str[0], '%Y.%m.%d')
            #与现在相差天数
            delta = (date_now - index_date).days
            if delta > delete_day:
                index_delete = 'http://%s:9200/%s' % (es_ip,index)
                os.popen("curl -XDELETE %s" % (index_delete))


elk_close(es_ip,close_day)
elk_delete(es_ip,delete_day)
