#coding=utf-8
import json
import urllib2
import time
import string

class Zabbix:

    # based url and required header
    url = "http://192.167.7.123/zabbix/api_jsonrpc.php"
    header = {"Content-Type": "application/json"}
    
#私有接口

    #登录
    def _login(self,url,header):
        # logindata json
        logindata = json.dumps(
            {
        	   "jsonrpc": "2.0",
                "method": "user.login",
                "params": {
                "user": "Admin",
                "password": "zabbix",
                "userData": "true"
            },
            "id": 1
            })
        # create request object login
        logindatarequest = urllib2.Request(url,logindata)
        for key in header:
            logindatarequest.add_header(key,header[key])
        # login
        try:
            logindataresult = urllib2.urlopen(logindatarequest)
        except URLError as e:
            print "Login Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(logindataresult.read())
            logindataresult.close()
            print "Login Successful. The Login Sessionid ID Is:",response['result']['sessionid']
            return response

    #退出
    def _logout(self,response,url,header):
        # logoutdata json
        logoutdata = json.dumps(
            {
                "jsonrpc": "2.0",
                "method": "user.logout",
                "params": [],
                "auth": response['result']['sessionid'],
                "id": 1
            })
        # create request object logout
        logoutdatarequest = urllib2.Request(url,logoutdata)
        for key in header:
            logoutdatarequest.add_header(key,header[key])
        # logout
        try:
            logoutdataresult = urllib2.urlopen(logoutdatarequest)
        except URLError as e:
            print "Logout Failed, Please Check Your Name And Password:",e.code
        else:
            response = json.loads(logoutdataresult.read())
            logoutdataresult.close()
            print "Logout Successful. The Logout Status Is:",response['result']

    #增加监控主机
    def _hostadd(self,addhostname,addhostip,response,url,header):
        # hostadddata json
        hostadddata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"host.create",
                "params":{
                    "host": addhostname,
                    "interfaces": [
                        {
                            "type": 1,
                            "main": 1,
                            "useip": 1,
                            "ip": addhostip,
                            "dns": "",
                            "port": "10050"
                        }
                    ],
                    "groups": [
                        {
                            "groupid": "2"
                        }
                    ],
                    "templates": [
                        {
                            "templateid": "10001"
                        }
                    ],
                    #"inventory_mode": 0
                    #"inventory": {
                    #    "macaddress_a": "01234",
                    #    "macaddress_b": "56768"
                    #}
                },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object hostadd
        hostadddatarequest = urllib2.Request(url,hostadddata)
        for key in header:
            hostadddatarequest.add_header(key,header[key])
        # hostadd
        try:
            hostadddataresult = urllib2.urlopen(hostadddatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(hostadddataresult.read())
            hostadddataresult.close()

    #删除监控主机
    def _hostdel(self,hostid,response,url,header):
        # hostdeldata json
        hostdeldata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"host.delete",
                "params":[hostid],
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object hostdeldata
        hostdeldatarequest = urllib2.Request(url,hostdeldata)
        for key in header:
            hostdeldatarequest.add_header(key,header[key])
        # hostdeldata
        try:
            hostdeldataresult = urllib2.urlopen(hostdeldatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(hostdeldataresult.read())
            hostdeldataresult.close()
            #print response

    #查询监控主机
    def _hostget(self,hostname,response,url,header):
        # hostgetdata json
        hostgetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"host.get",
                "params":{
                    "output":["hostid","name"],
                    "filter":{"host":hostname}
                    },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object hostget
        hostgetdatarequest = urllib2.Request(url,hostgetdata)
        for key in header:
            hostgetdatarequest.add_header(key,header[key])
        # get host list
        try:
            hostgetdataresult = urllib2.urlopen(hostgetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(hostgetdataresult.read())
            print response
            hostgetdataresult.close()
            print "Number Of Hosts: ", len(response['result'])
            for host in response['result']:
                print "Host ID:",host['hostid'],"Host Name:",host['name']
            return host['hostid']
    
    #查询主机组信息
    def _groupget(self,groupname,response,url,header):
        # groupgetdata json
        hostgroupgetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"hostgroup.get",
                "params":{
                    "output":["extend"],
                    "filter":{"name":groupname}
                    },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object groupget
        hostgroupgetdatarequest = urllib2.Request(url,hostgroupgetdata)
        for key in header:
            hostgroupgetdatarequest.add_header(key,header[key])
        # get group list
        try:
            hostgroupgetdataresult = urllib2.urlopen(hostgroupgetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(hostgroupgetdataresult.read())
            hostgroupgetdataresult.close()
            print response

    #查询模板信息
    def _templateget(self,response,url,header):
        # templategetdata json
        templategetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"template.get",
                "params":{
                    "output":["extend"],
                    "filter":{"host":"Template OS Linux"}
                    },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object templateget
        templategetdatarequest = urllib2.Request(url,templategetdata)
        for key in header:
            templategetdatarequest.add_header(key,header[key])
        # get template list
        try:
            templategetdataresult = urllib2.urlopen(templategetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(templategetdataresult.read())
            templategetdataresult.close()
            print response  

    #查询指定主机图表信息
    def _hostgraphget(self,hostid,response,url,header):
        # hostgraphgetdata json
        hostgraphgetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"graph.get",
                "params":{
                    "output":["extend"],
                    "hostids": hostid,
                    "sortfield": "name",
                    },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object hostget
        hostgraphgetdatarequest = urllib2.Request(url,hostgraphgetdata)
        for key in header:
            hostgraphgetdatarequest.add_header(key,header[key])
        # get host list
        try:
            hostgraphgetdataresult = urllib2.urlopen(hostgraphgetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(hostgraphgetdataresult.read())
            hostgraphgetdataresult.close()   
            print response

    #获取历史数据信息
    def _historyget(self,historyvalue,hostids,itemids,response,url,header):
        # historygetdata json
        statusgetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"history.get",
                "params":{
                    "history": historyvalue,
                    "hostids":hostids,
                    "itemids": itemids,
                    "sortfield": "clock",
                    "sortorder": "DESC",
                    "limit": 60    #选取最新数据60条记录,以分钟为单位,统计1小时的信息
                },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object historygetdata
        statusgetdatarequest = urllib2.Request(url,statusgetdata)
        for key in header:
            statusgetdatarequest.add_header(key,header[key])
        # get status
        try:
            statusgetdataresult = urllib2.urlopen(statusgetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            historyresponse = json.loads(statusgetdataresult.read())
            statusgetdataresult.close()   
            print "----*****************MSG OF _historyget Return Json*********************---"
            print historyresponse
            print "Msg Of Hosts: ", len(historyresponse['result'])
            for historyvalue in historyresponse['result']:
                print "Host Msg Clock:",historyvalue['clock'],"Host Msg Value:",historyvalue['value']
                timeswap = string.atof(historyvalue['clock'])
                timevalue = time.localtime(timeswap)
                #print historyvalue['clock']
                #print "Host Msg Clock:",time.strftime('%Y-%m-%d %H:%M:%S',timevalue)"Host Msg Value:",historyvalue['value']
                #print "Host Msg Clock:",time.strftime('%H:%M',timevalue),"Host Msg Value:",historyvalue['value']
                #return historyvalue['hostid']

    #获取查询项
    def _itemget(self,hostid,key,response,url,header):
        # itemgetdata json
        statusgetdata = json.dumps(
            {
                "jsonrpc":"2.0",
                "method":"item.get",
                "params":{
                    "output": "extend",
                    "hostids": hostid,
                    "search": {
                        "key_": key #parameter:'sys' or 'net' or 'mem' or 'system.cpu.load'
                        },
                    "sortfield": "name",
                    "limit": 22
                },
                "auth":response['result']['sessionid'], 
                "id":1,
            })
        # create request object itemgetdata
        statusgetdatarequest = urllib2.Request(url,statusgetdata)
        for key in header:
            statusgetdatarequest.add_header(key,header[key])
        # get status
        try:
            statusgetdataresult = urllib2.urlopen(statusgetdatarequest)
        except URLError as e:
            if hasattr(e, 'reason'):
                print 'We failed to reach a server.'
                print 'Reason: ', e.reason
            elif hasattr(e, 'code'):
                print 'The server could not fulfill the request.'
                print 'Error code: ', e.code
        else:
            response = json.loads(statusgetdataresult.read())
            statusgetdataresult.close()   
            print "----*****************MSG OF _itemget Return Json*********************---"
            print response  #此处将会打印数据信息 
            print "Number Of Items: ", len(response['result'])
            items=[]
            for item in response['result']:
                print "item ID:",item['itemid'],"item Name:",item['key_']
                items.append(item['itemid'])
                #return item['itemid']  #调试专用
            print items
            return items    #返回id列表
             

#公共接口
    #增加解控主机
    def hostadd(self,addhostname,addhostip):
        addresponse = self._login(self.url,self.header)
        self._hostadd(addhostname,addhostip,addresponse,self.url,self.header)
        self._logout(addresponse,self.url,self.header)     
    
    #删除监控主机
    def hostdelete(self,hostname):
        queryresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,queryresponse,self.url,self.header)        
        self._hostdel(hostid,queryresponse,self.url,self.header)
        self._logout(queryresponse,self.url,self.header)    
    
    #查询监控主机
    def hostquery(self,host=''):
        queryresponse = self._login(self.url,self.header)
        self._hostget(host,queryresponse,self.url,self.header)
        self._logout(queryresponse,self.url,self.header)

    #查询监控主机组信息
    def querygroup(self,groupname=''):
        querygroupresponse = self._login(self.url,self.header)
        self._groupget(groupname,querygroupresponse,self.url,self.header)
        self._logout(querygroupresponse,self.url,self.header)

    #查询指定模板信息
    def querytemplate(self):
        querytemplateresponse = self._login(self.url,self.header)
        self._templateget(querytemplateresponse,self.url,self.header)
        self._logout(querytemplateresponse,self.url,self.header) 

    #查询指定主机图表
    def queryhostgraph(self,hostname=''):
        queryhostgraphresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,queryhostgraphresponse,self.url,self.header)  
        self._hostgraphget(hostid,queryhostgraphresponse,self.url,self.header)
        self._logout(queryhostgraphresponse,self.url,self.header)

    #获取cpu相关历史信息
    def historyofcpu(self,hostname='',key='system.cpu.load[percpu,avg1]'):
        historyresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,historyresponse,self.url,self.header)
        itemids = self._itemget(hostid,key,historyresponse,self.url,self.header)
        self._historyget(0,hostid,itemids,historyresponse,self.url,self.header)
        self._logout(historyresponse,self.url,self.header)  

    #获取网卡流量相关历史信息
    def historyofnet(self,hostname='',key='net.if.in[eth0]'):
        historyresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,historyresponse,self.url,self.header)
        itemids = self._itemget(hostid,key,historyresponse,self.url,self.header)
        self._historyget(3,hostid,itemids,historyresponse,self.url,self.header)
        self._logout(historyresponse,self.url,self.header)  

    #获取内存相关历史信息
    def historyofmem(self,hostname='',key='vm.memory.size[available]'):
        historyresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,historyresponse,self.url,self.header)
        itemids = self._itemget(hostid,key,historyresponse,self.url,self.header)
        self._historyget(3,hostid,itemids,historyresponse,self.url,self.header)
        self._logout(historyresponse,self.url,self.header) 

    #获取查询项
    def item(self,hostname='',key=''):
        itemresponse = self._login(self.url,self.header)
        hostid = self._hostget(hostname,itemresponse,self.url,self.header)  
        itemid = self._itemget(hostid,key,itemresponse,self.url,self.header)
        self._logout(itemresponse,self.url,self.header)         


if __name__ == '__main__':
    # based url and required header
    #za = Zabbix()
    #za.hostquery() #查询主机,默认all
    #za.hostdelete("215") #删除主机,参数为主机名称,默认null
    #za.querygroup('Linux servers') #查询主机组,调试专用,参数为组名,默认all
    #za.querytemplate() #查询模板信息,调试专用,暂不支持传参
    #za.hostadd('215','172.21.4.215')   #添加主机,参数为主机名称和ip地址
    #za.queryhostgraph()    #查询指定主机图表,参数为主机名称,默认逻辑第一个
    #za.historyofcpu('windowsagent1','system.cpu.load[percpu,avg1]')  #查询历史数据,参数为主机名称和查询内容,默认逻辑第一个
        ##第二参数:cpu:'system.cpu.load[percpu,avg1]'、'system.cpu.load[percpu,avg5]'、'system.cpu.load[percpu,avg15]'
    #za.historyofnet('windowsagent1','net.if.out[eth0]')  #查询历史数据,参数为主机名称和查询内容,默认逻辑第一个
        #第二参数:net:'net.if.in[eth0]'、'net.if.in[eth1]'、'net.if.out[eth0]'、'net.if.out[eth1]'
    #za.historyofmem('zabbixagent2','vm.memory.size[total]')  #查询历史数据,参数为主机名称和查询内容,默认逻辑第一个
        #第二参数:mem:'vm.memory.size[available]'、'vm.memory.size[total]'
    #za.item('windowsagent1','net')    #查询监控项,调试专用,参数为主机名称,默认逻辑第一个