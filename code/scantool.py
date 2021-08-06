import openpyxl
import requests
import json
import time
import re
import ast
import spacy
import os
from spacy import displacy


baseURL = 'xxxxx'


def writelog(content):
    with open('mattermostLog', 'a+') as f:
        f.write(content+'\n')
def loadData(filePath):
    workbook = openpyxl.load_workbook(filePath)
    worksheet = workbook.worksheets[0]
    keys = []
    datas = {}
    i = 0
    for row in worksheet.rows:
        if i == 0:
            for cell in row:
                if cell.value == "Arguments":
                    i = i + 1
                    keys.append(cell.value + str(i))
                elif cell.value == "(Arg_Req)" or cell.value == "Arg_Example" or cell.value == "api_dep":
                    keys.append(cell.value + str(i))
                else:
                    keys.append(cell.value)
        else:
            j = 0
            obj = ''
            data = {}
            for cell in row:
                v = cell.value
                if v is not None:
                    if isinstance(v, str):
                        v = v.replace('\n', ' ')
                        v = v.strip()
                if keys[j] == 'OBJECT':
                    obj = v
                data[keys[j]] = v
                j = j + 1

            ds = []
            if obj in datas:
                ds = datas[obj]
            ds.append(data)
            datas[obj] = ds
    for obj, dataList in datas.items():
        newDataList = []
        try:
            for data in dataList:
                url = data['Method URL']
                if url is None:
                    break
                if 'https://discord.com/api/guilds/{guild.id}/prune' in url:
                    print('ddd')
                elif 'https://discord.com/api/guilds/{guild.id}/invites' in url:
                    print('d')
                url = url.replace('https://', '')
                url = url.replace('http://', '')
                if ':' in url:
                    items = url.split('/')
                    for item in items:
                        if ':' in item and 'https:' not in item and 'http:' not in item:
                            replaceStr = '{' + item.replace(':', '') + '}'
                            if ':_id' == item:
                                replaceStr = '{id}'
                            elif ':rid' == item:
                                replaceStr = '{room_id}'
                            url = data['Method URL']
                            url = url.replace(item, replaceStr)
                            data['Method URL'] = url
                if 'args' in data and data['args'] is not None:
                    args = json.loads(data['args'])
                    for i in range(1, 14):
                        arg = data['Arguments' + str(i)]
                        if arg in args:
                            data['Arg_Example' + str(i)] = args[arg]
                        else:
                            data['Arg_Example' + str(i)] = None
                else:
                    items = []
                    if '{' in data['Method URL'] and '}' in data['Method URL']:
                        items = re.findall("{(.*?)}", data['Method URL'])
                    if '{id}' in data['Method URL']:
                        url = data['Method URL']
                        urlItems = url.split('/')
                        for i in range(1, len(urlItems)):
                            if urlItems[i] == '{id}':
                                preItem = urlItems[i-1]
                                replaceStr = preItem + '/{' + preItem + '_id}'
                                if 's' == preItem[-1]:
                                    replaceStr = preItem + '/{' + preItem[:-1] + '_id}'

                                url = url.replace(preItem + '/{id}',replaceStr)

                        data['Method URL'] = url

                    for i in range(1, 14):
                        #if data['(Arg_Req)'+str(i)] is not None:
                        #    data['(Arg_Req)' + str(i)] = 'Required'
                        for item in items:
                            if data['Arguments' + str(i)] is not None and data['Arguments' + str(i)] == item:
                                data['(Arg_Req)' + str(i)] = 'Optional'
                        if data['(Arg_Req)'+str(i)] != 'Required' and data['(Arg_Req)'+str(i)] is not None:
                            data['(Arg_Req)' + str(i)] = 'Optional'

                        if data['Arg_Example'+str(i)] is None:
                            break

                newDataList.append(data)
            datas[obj] = newDataList
        except:
            print(data['Method URL']+' error loadData')


    return datas


def getResponse(allArgList, allResponsDict, datas, preDatas, depRes, token, u):
    deps = datas[1]
    datas = datas[0]
    if 'requset example' in datas and datas['requset example'] is not None:
        print('dd')
    url = datas['Method URL']
    if ' ' in url:
        items = url.split(' ')
        url = items[0]
    headers = {}
    headers['Content-type'] = 'application/json'
    headers['Authorization'] = 'Bearer ' + token[0]
    i = 1
    data = {}
    argstr = ''
    arghasList = []
    sendData = {}
    k = datas['Method URL'].replace(baseURL, '') + '---' + datas['OBJECT'] + '---' + datas[' HTTP method']
    trueArgs = allArgList[k]
    finishedUrlArgs = []
    if '###' in url:
        ius = url.split('###')
        url = ius[0]
    oldurl = url
    for i in range(1, 14):
        k = '(Arg_Req)' + str(i)
        if k in datas:
            if datas[k] == 'Optional':
                continue
            trueArg = datas['Arguments' + str(i)]
            if trueArg is None:
                if '{' in oldurl and '}' in oldurl:
                    urlArgs = re.findall("{(.*?)}", oldurl)
                    for urlArg in urlArgs:
                        if urlArg in finishedUrlArgs:
                            continue
                        else:
                            trueArg = urlArg
                            finishedUrlArgs.append(urlArg)
                            break
                if trueArg is None:
                    break
            arg = None
            for k, v in trueArgs.items():
                if v == trueArg:
                    arg = k
                    break
            if arg is None:
                continue
            elif arg in preDatas:
                preData = preDatas[arg]
                if isinstance(preData, list) and len(preData) > 0 and arg != 'groupTypes' and arg != 'roles' and arg != 'members':
                    argstr = argstr + trueArg + '=' + str(preData[0]) + '&'
                    sendData[trueArg] = preData
                    argTrue = []
                    argTrue.append(trueArg)
                    argTrue.append(arg)
                    if argTrue not in arghasList:
                        arghasList.append(argTrue)
                else:
                    argstr = argstr + trueArg + '=' + str(preData) + '&'
                    sendData[trueArg] = preData

            elif arg in deps and len(deps[arg]) > 0:
                items = deps[arg].split('---')
                m = items[0]
                if m == url:
                    if arg in preDatas:
                        preData = preDatas[arg]
                        if isinstance(preData, list) and len(preData) > 0:
                            argstr = argstr + trueArg + '=' + str(preData) + '&'
                            sendData[trueArg] = preData
                            argTrue = []
                            argTrue.append(trueArg)
                            argTrue.append(arg)
                            if argTrue not in arghasList:
                                arghasList.append(argTrue)
                        else:
                            argstr = argstr + trueArg + '=' + str(preData) + '&'
                            sendData[trueArg] = preData

                    elif arg != 'token' and datas['Arg_Example' + str(i)] is not None:
                        argstr = argstr + trueArg + '=' + str(datas['Arg_Example' + str(i)]) + '&'
                        argdata = datas['Arg_Example' + str(i)]
                        if isinstance(argdata, str) and '[' in argdata and ']' in argdata:
                            sendData[trueArg] = ast.literal_eval(argdata)
                        elif isinstance(argdata, str) and '{' in argdata and '}' in argdata:
                            sendData[trueArg] = json.loads(argdata)
                        else:
                            sendData[trueArg] = argdata
                elif m in depRes:
                    result = depRes[m]
                    if len(items) == 2:
                        argstr = argstr + trueArg + '=' + str(result[items[1]]) + '&'
                        sendData[trueArg] = result[items[1]]
                    elif len(items) == 4:
                        ta = trueArgs
                        t = ''
                        trueRess = allResponsDict[items[0]+'---'+items[1]+'---'+items[2]]
                        trueRes = trueRess[items[3]]
                        if '---' in trueRes:
                            resItems = trueRes.split('---')
                            if resItems[0] not in result and datas['Arg_Example' + str(i)] is not None:
                                argstr = argstr + trueArg + '=' + str(datas['Arg_Example' + str(i)]) + '&'
                                argdata = datas['Arg_Example' + str(i)]
                                if isinstance(argdata, str) and '[' in argdata and ']' in argdata:
                                    sendData[trueArg] = ast.literal_eval(argdata)
                                elif isinstance(argdata, str) and '{' in argdata and '}' in argdata:
                                    sendData[trueArg] = json.loads(argdata)
                                else:
                                    sendData[trueArg] = argdata
                            else:
                                getRes = True
                                temResult = result.copy()
                                for kRes in resItems:
                                    if kRes in temResult:
                                        temResult = temResult[kRes]
                                        if isinstance(temResult, list):
                                            temResult = temResult[0]
                                    else:
                                        getRes = False
                                if getRes:
                                    argstr = argstr + trueArg + '=' + str(temResult) + '&'
                                    sendData[trueArg] = temResult
                        else:
                            #不嵌套，直接获取value
                            if result is None or (trueRes not in result and datas['Arg_Example' + str(i)] is not None):
                                argstr = argstr + trueArg + '=' + str(datas['Arg_Example' + str(i)]) + '&'
                                argdata = datas['Arg_Example' + str(i)]
                                if isinstance(argdata, str) and '[' in argdata and ']' in argdata:
                                    sendData[trueArg] = ast.literal_eval(argdata)
                                elif isinstance(argdata, str) and '{' in argdata and '}' in argdata:
                                    sendData[trueArg] = json.loads(argdata)
                                else:
                                    sendData[trueArg] = argdata
                            elif trueRes in result:
                                argstr = argstr + trueArg + '=' + str(result[trueRes]) + '&'
                                sendData[trueArg] = result[trueRes]
                else:
                    return None


            elif arg != 'token' and datas['Arg_Example' + str(i)] is not None:
                argstr = argstr + trueArg + '=' + str(datas['Arg_Example' + str(i)]) + '&'
                argdata = datas['Arg_Example' + str(i)]
                if isinstance(argdata, str) and '[' in argdata and ']' in argdata:
                    sendData[trueArg] = ast.literal_eval(argdata)
                elif isinstance(argdata, str) and '{' in argdata and '}' in argdata:
                    sendData[trueArg] = json.loads(argdata)
                else:
                    sendData[trueArg] = argdata
                # data[arg] = datas['Arg_Example'+str(i)]
        else:
            break
    oldurl = url
    if '{' and '}' in oldurl:
        urlArgs = re.findall("{(.*?)}",oldurl)
        for urlArg in urlArgs:
            if urlArg in sendData:
                replaceData = sendData[urlArg]
                if isinstance(replaceData, list):
                    replaceData = replaceData[0]
                oldurl = oldurl.replace('{'+urlArg+'}',replaceData)
                if 'api/v4/teams/{team_id}/members' not in url:
                    sendData.pop(urlArg)
            elif 'https://mytest-2.cloud.mattermost.com/api/v4/teams/{team_id}' == url:
                replaceData = sendData['id']
                oldurl = oldurl.replace('{' + urlArg + '}', replaceData)
            elif 'https://mytest-2.cloud.mattermost.com/api/v4/oauth/apps/{app_id}' == url:
                replaceData = sendData['id']
                oldurl = oldurl.replace('{' + urlArg + '}', replaceData)
    url = url + '?' + argstr[:-1]
    if len(url) <10000:
        print(url)
    if len(url) < 10000:
        print(oldurl)
    response = None


    httpMethod = datas[' HTTP method'].upper()
    response = None
    if ('pic_file' in sendData or 'file' in sendData or 'files' in sendData or 'image' in sendData or 'certificate' in sendData) and len(
            sendData) == 1:
        headers['Content-type'] = 'multipart/form-data'
        if httpMethod == 'POST':
            response = requests.post(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'GET':
            response = requests.get(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'PATCH':
            response = requests.patch(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'DELETE':
            response = requests.delete(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'PUT':
            response = requests.put(oldurl, headers=headers, files=sendData)

    elif 'image' in sendData:
        if httpMethod == 'POST':
            response = requests.post(oldurl, headers=headers, data=sendData)
        elif httpMethod == 'GET':
            response = requests.get(oldurl, headers=headers, data=sendData)
        elif httpMethod == 'PATCH':
            response = requests.patch(oldurl, headers=headers, data=sendData)
        elif httpMethod == 'DELETE':
            response = requests.delete(oldurl, headers=headers, data=sendData)
        elif httpMethod == 'PUT':
            response = requests.put(oldurl, headers=headers, data=sendData)

    elif 'emoji' in sendData:
        if httpMethod == 'POST':
            response = requests.post(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'GET':
            response = requests.get(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'PATCH':
            response = requests.patch(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'DELETE':
            response = requests.delete(oldurl, headers=headers, files=sendData)
        elif httpMethod == 'PUT':
            response = requests.put(oldurl, headers=headers, files=sendData)

    else:
        if 'Array' in sendData:
            sendData = sendData['Array']
        if httpMethod == 'POST':
            response = requests.post(oldurl, headers=headers, data=json.dumps(sendData))
        if httpMethod == 'POST':
            response = requests.post(oldurl, headers=headers, data=json.dumps(sendData))
        elif httpMethod == 'GET':
            response = requests.get(oldurl, headers=headers, data=json.dumps(sendData))
        elif httpMethod == 'PATCH':
            response = requests.patch(oldurl, headers=headers, data=json.dumps(sendData))
        elif httpMethod == 'DELETE':
            response = requests.delete(oldurl, headers=headers, data=json.dumps(sendData))
        elif httpMethod == 'PUT':
            response = requests.put(oldurl, headers=headers, data=json.dumps(sendData))
    time.sleep(1)
    if response.status_code == 204 or response.status_code == 202 or response.status_code == 201:
        return {"OK": True}
    r = {}
    try:
        r = response.json()
    except Exception:
        r = {}
    if 'trackingId' in response.text or 'detailed_error' in response.text or 'error' in response.text or 'Invalid' in response.text:
        if len(token) > 1:
            for i in range(1, len(token)):
                if ('error' in r and r['error'] == 'not_allowed_token_type') or 'Invalid' in response.text:
                    headers['Authorization'] = 'Bearer ' + token[i]
                    if 'Array' in sendData:
                        sendData = sendData['Array']
                    if httpMethod == 'POST':
                        response = requests.post(oldurl, headers=headers, data=json.dumps(sendData))
                    elif httpMethod == 'GET':
                        response = requests.get(oldurl, headers=headers, data=json.dumps(sendData))
                    elif httpMethod == 'PATCH':
                        response = requests.patch(oldurl, headers=headers, data=json.dumps(sendData))
                    elif httpMethod == 'DELETE':
                        response = requests.delete(oldurl, headers=headers, data=json.dumps(sendData))
                    elif httpMethod == 'PUT':
                        response = requests.put(oldurl, headers=headers, data=json.dumps(sendData))
                    if response is not None and 'errors' in response.text:
                        if httpMethod == 'POST':
                            response = requests.post(url, headers=headers)
                    r = {}
                    try:
                        r = response.json()
                    except Exception:
                        r = {}
                    time.sleep(1)
        if ('trackingId' in r or 'detailed_error' in r or 'error' in r or 'Invalid' in response.text) and len(arghasList) > 0:
            url1 = oldurl
            for a in arghasList:

                preData = preDatas[a[1]]

                replaceStr = a[0] + '=' + str(preData[0]) + '&'
                if 'detailed_error' in r or 'error' in r or 'Invalid' in response.text:
                    for i in range(0, len(preData)):
                        if '{' + a[0] + '}' in url:
                            url1 = oldurl.replace(preData[0], preData[i])
                        # url1 = oldurl.replace(replaceStr, a + '=' + str(preData[i]) + '&')
                        if isinstance(sendData, list):
                            sendData = preData[i]
                        else:
                            sendData[a[0]] = preData[i]
                        if 'Array' in sendData:
                            sendData = sendData['Array']
                        if httpMethod == 'POST':
                            response = requests.post(url1, headers=headers, data=json.dumps(sendData))
                        elif httpMethod == 'GET':
                            response = requests.get(url1, headers=headers, data=json.dumps(sendData))
                        elif httpMethod == 'PATCH':
                            response = requests.patch(url1, headers=headers, data=json.dumps(sendData))
                        elif httpMethod == 'DELETE':
                            response = requests.delete(url1, headers=headers, data=json.dumps(sendData))
                        elif httpMethod == 'PUT':
                            response = requests.put(url1, headers=headers, data=json.dumps(sendData))
                        if response is not None and (
                                'errors' in response.text or 'detailed_error' in response.text):
                            if httpMethod == 'POST':
                                requests.post(url1, headers=headers)
                        r = response.json()
                        if 'trackingId' in r or 'detailed_error' in r or 'error' in r:
                            continue
                        elif 'detailed_error' not in r and 'error' not in r:
                            break


   
    r = None
    try:
        if response is None:
            return response
        r = response.json()
        if 'trackingId' in r:
            if len(url) < 10000:
                print(url)
    except:
        if len(response.content) < 10000:
            print(response.content)
        return {}


    return r


def getDataFromResult(key, result):
    if key in result:
        return result[key]
    else:
        for k, v in result.items():
            if isinstance(v, dict) and key in v:
                return v[key]
    return None


# get all APIs' all arguments
def getAllArguments(datas):
    allObjList = {}
    # get all arg
    argList = []
    allArgList = {}
    for key in datas.keys():
        data = datas[key]
        for d in data:
            linkArgRes = {}
            if d['Method URL'] is None:
                continue
            # get args
            argList = []
            lenR = 1
            while 'Arguments' + str(lenR) in d:
                lenR = lenR + 1

            for i in range(1, lenR):
                arg = d['Arguments' + str(i)]
                if arg is not None and arg not in argList:
                    argList.append(arg)
            u = d['Method URL'].replace(baseURL, '')
            argDict = {}
            obj = d['OBJECT']
            allObjList[obj] = 1
            for arg in argList:
                if arg == 'id' or arg == '.id' or arg == '.Id' or arg == 'ID' or arg == 'Id' or arg == '_id':
                    argDict[d['OBJECT']+'_id'] = 'id'
                elif arg == 'msgId':
                    argDict['message_id'] = 'msgId'
                elif 'X-User-Id' == arg:
                    argDict['user_id'] = 'X-User-Id'
                elif arg == obj[0]+'id':
                    argDict[obj +'_id'] = arg
                elif arg == 'msg':
                    argDict['message'] = 'msg'
                elif arg.endswith('Id') :
                    argDict[arg.replace('Id','_id')] = arg
                elif arg.endswith('ID'):
                    argDict[arg.replace('ID', '_id')] = arg
                elif arg.endswith('-id'):
                    argDict[arg.replace('-id', '_id')] = arg
                elif arg.endswith('._id'):
                    argDict[arg.replace('._id', '_id')] = arg
                elif arg.endswith('_id'):
                    argDict[arg] = arg
                elif arg.endswith('id'):
                    argDict[arg.replace('id', '_id')] = arg
                else:
                    argDict[arg] = arg

            if "{" in u and "}" in u:
                urlItems = u.split('/')
                for i in range(0, len(urlItems)):
                    item = urlItems[i]
                    if '|' in item:
                        its = item.split('|')
                        item = its[0].strip() + '}'
                    if item == '{id}' or item == '{ID}' or item == '{Id}':
                        headStr = urlItems[i - 1]
                        if headStr.endswith('s'):
                            headStr = headStr[:-1]
                        u = u.replace(urlItems[i - 1] + '/' + urlItems[i], urlItems[i - 1] + '/{' + headStr + '_id}')
                items = re.findall('{(.*?)}', u)
                for item in items:
                    newItem = item.lower()
                    if item in argList:
                        continue

                    if '-id' in item:
                        newItem = item.replace('-id', '_id')
                    elif '.id' in item:
                        newItem = item.replace('.id', '_id')
                    elif item.endswith('Id'):
                        newItem = item.replace('Id', '_id')
                    elif 'ID' in item and '_ID' not in item and item != 'ID':
                        newItem = item.replace('ID', '_id')
                    elif 'id' in item and '_id' not in item and item != 'id':
                        newItem = item.replace('id', '_id')
                    if newItem not in argDict:
                        argDict[newItem] = item



            allArgList[d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = argDict
    return allArgList, allObjList


# For each object's methods, split them into three groups: insert, select and update
def getObjectCRU(data, allObjList):
    # get insert, select, update data
    insertDatas = {}
    selectDatas = {}
    updateDatas = {}

    for d in data:
        if d['Method URL'] is None:
            continue
        if 'https://graph.microsoft.com/v1.0/chats/{chat_id}/tabs' in d['Method URL']:
            print('dd')
        # 1. for each object list, get their insert methods' list, select methods' list and update methods' list
        response = d['api response']
        if response is not None and len(response) > 2:
            newRes = {}
            try:
                response = re.sub(' +', '', response)
                response = response.replace(',{...}','')
                response = response.replace(',}','}')
                response = response.replace('}"', '},"')
                response = response.replace('},]','}]')
                response = response.replace('//...','')
                if '..."' not in response:
                    response = response.replace('...','""')
                response = response.replace('xxxxxxxxxxxxxx','""')
                response = response.replace('xxxxxxxxxx','""')
                response = response.replace(';',',')
                response = response.replace('“','"')
                response = response.replace('”','"')
                response = response.replace(']"', '],"')
                response = response.replace('false', '""')
                response = response.replace('"null"', '""')
                response = response.replace('null', '""')
                response = response.replace('None','""')

                res = json.loads(response)
                if isinstance(res, list) and len(res) > 0:
                    res = res[0]
                # 判断response是否为dict
                if isinstance(res, dict):
                    for k, v in res.items():
                        newK = k
                        if k == 'id' or k == '-id' or k == 'ID' or k == 'Id' or k == '_id':
                            newRes[d['OBJECT']+'_id'] = k
                            continue
                        elif isinstance(v, list) and len(v) > 0:
                            if k[-1] == 's':
                                newK = k[:-1].lower()
                            v = v[0]
                        if isinstance(v, dict):
                            for k1, v1 in v.items():
                                newK1 = k1
                                if k1 == 'id' or k1 == '-id' or k1 == 'ID' or k1 == 'Id' or k1 == '_id':
                                    if newK in allObjList:
                                        newRes[newK + '_id'] = k+'---'+k1
                                    elif newK == 'u':
                                        newRes['user_id'] = k + '---' + k1
                                    elif d['OBJECT'] + '_id' in newRes:
                                        newRes[newK + '_id'] = k + '---' + k1
                                    else:
                                        newRes[d['OBJECT'] + '_id'] = k + '---' + k1
                                    continue
                                elif isinstance(v1, list) and len(v1) > 0:
                                    if k1[-1] == 's':
                                        newK1 = k1[:-1].lower()
                                    v1 = v1[0]
                                if isinstance(v1, dict):
                                    for k2, v2 in v1.items():
                                        if k2 == 'id' or k2 == '-id' or k2 == 'ID' or k2 == 'Id' or k2 == '_id':
                                            if newK1 in allObjList:
                                                newRes[newK1 + '_id'] = k + '---' + k1 + '---' + k2
                                            elif newK1 == 'u':
                                                newRes['user_id'] = k + '---' + k1 + '---' + k2
                                            elif newK1 + '_id' in newRes:
                                                newRes[newK1 + '_id'] = k + '---' + k1 + '---' + k2
                                            else:
                                                newRes[newK1 + '_id'] = k + '---' + k1 + '---' + k2
                                        elif newK1.endswith('id'):
                                            newRes[newK1.replace('id', '_id')]
                                        else:
                                            newRes[k2] = k + '---' + k1 + '---' + k2
                                elif newK.endswith('id'):
                                    newRes[newK.replace('id','_id')] = k+'---'+k1
                                elif k1 in newRes:
                                    newRes[newK+'---'+k1] = k + '---' + k1
                                else:
                                    newRes[k1] = k+'---'+k1
                        else:
                            newRes[k] = k

                if 'api/v4/bots' in d['Method URL'] and 'user_id' in newRes:
                    newRes['bot_user_id'] = 'user_id'
                    newRes.pop('user_id')

                if d['CRUD'] == 'INSERT':
                    insertDatas[
                        d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = newRes
                elif d['CRUD'] == 'SELECT':
                    selectDatas[
                        d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = newRes
                elif d['CRUD'] == 'UPDATE':
                    updateDatas[
                        d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = newRes
            except:
                print(d['Method URL']+' error with response')
                updateDatas[d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = []

        else:
            if d['CRUD'] == 'INSERT':
                insertDatas[
                    d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = []
            elif d['CRUD'] == 'SELECT':
                selectDatas[
                    d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = []
            elif d['CRUD'] == 'UPDATE':
                updateDatas[
                    d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']] = []
    return insertDatas, selectDatas, updateDatas


#
def buildLinkForArg(crud, oldArg, arg, datas, allArgList, resList, newArgs):
    for m, res in datas.items():
        if m in allArgList and crud != 'INSERT':
            mArgList = allArgList[m]
            if arg in mArgList:
                continue

        if isinstance(res, list) and len(res) > 0:
            res = res[0]
        if isinstance(res, dict):
            if arg in res:
                resList.append(m + '---' + arg)
                if isinstance(res[arg], dict):
                    if 'id' in res[arg]:
                        resList.append(m + '---id')
                    elif '_id' in res[arg]:
                        resList.append(m + '---_id')

                else:
                    print(str(res[arg]))
                newArgs.pop(oldArg)
                break
            else:
                for k1, v1 in res.items():
                    if isinstance(v1, list) and len(v1) > 0:
                        v1 = v1[0]
                    if isinstance(v1, dict):
                        if arg in v1:
                            resList.append(m + '---' + k1)
                            resList.append(m + '---' + arg)
                            newArgs.pop(oldArg)
                            break
                        else:
                            for k2, v2 in v1.items():
                                if isinstance(v2, list) and len(v2) > 0:
                                    v2 = v2[0]
                                if isinstance(v2, dict):
                                    if arg in v2:
                                        resList.append(m + '---' + k1)
                                        resList.append(m + '---' + k2)
                                        resList.append(m + '---' + arg)
                                        newArgs.pop(oldArg)
                                        break
                if len(resList) > 0:
                    break


def buildLinkBetweenArgsAndRes(crud, d, args, k, datas, allArgList, allLinkArgRes):
    trueGo = True
    newArgs = args.copy()

    if len(datas) > 0:
        trueGo = False
        linkArgRes = {}
        if k in allLinkArgRes:
            linkArgRes = allLinkArgRes[k]
        oldDatas = datas.copy()
        if k in datas:
            datas.pop(k)
        for arg in args:
            resList = []
            buildLinkForArg(crud, arg, arg, datas, allArgList, resList, newArgs)
            if len(resList) == 0 and ((arg.lower()).startswith(d['OBJECT'].lower() + '_') or (arg.lower()).startswith(
                    d['OBJECT'].lower()) or (arg.lower()).endswith('s')):
                oldarg = arg
                obj = d['OBJECT'].lower()
                if (arg.lower()).startswith(obj + '_'):
                    arg = (arg.lower()).replace(obj + '_', '')
                elif (arg.lower()).startswith(obj):
                    arg = (arg.lower()).replace(obj, '')
                else:
                    arg = arg[:len(arg) - 1]
                buildLinkForArg(crud, oldarg, arg, datas, allArgList, resList, newArgs)
                arg = oldarg

            linkArgRes[arg] = resList
        allLinkArgRes[k] = linkArgRes
        datas = oldDatas.copy()
    args = newArgs.copy()
    return trueGo, args, newArgs, datas, allArgList, allLinkArgRes

def getLinksBetweenArgsAndRes(data, allArgList, insertDatas, selectDatas, updateDatas, allLinkArgRes, sameArgList):
    for d in data:
        if d['Method URL'] is None:
            continue
        insertGo = True
        selectGo = True
        updateGo = True

        k = d['Method URL'].replace(baseURL, '') + '---' + d['OBJECT'] + '---' + d[' HTTP method']

        if k in allArgList:
            # k is a method, get k's args
            args = allArgList[k]
            # get same arg list for all method, will be used in 4
            for arg in args:
                if '_id' not in arg:
                    continue
                sameArgs = []
                if arg.lower() in sameArgList:
                    sameArgs = sameArgList[arg.lower()]
                sameArgs.append(k)
                sameArgList[arg.lower()] = sameArgs



            # start to build links between insert, select, update method and arg
            insertGo, args, newArgs, insertDatas, allArgList, allLinkArgRes = buildLinkBetweenArgsAndRes("INSERT", d, args, k,
                                                                                                   insertDatas,
                                                                                                   allArgList,
                                                                                                   allLinkArgRes)

            if d['CRUD'] != 'INSERT':
                selectGo, args, newArgs, selectDatas, allArgList, allLinkArgRes = buildLinkBetweenArgsAndRes("SELECT",d, args, k,
                                                                                                             selectDatas,
                                                                                                             allArgList,
                                                                                                             allLinkArgRes)
                updateGo, args, newArgs, updateDatas, allArgList, allLinkArgRes = buildLinkBetweenArgsAndRes("UPDATE",d, args, k,
                                                                                                             updateDatas,
                                                                                                             allArgList,
                                                                                                             allLinkArgRes)

            # when insert, select, update method can not build links with arg
            if insertGo and selectGo and updateGo:
                linkArgRes = {}
                for arg in args:
                    linkArgRes[arg] = []
                allLinkArgRes[k] = linkArgRes
    return allArgList, insertDatas, allLinkArgRes, sameArgList
	
	
	

# load data
allDatas = loadData('cliq_api_list.xlsx')
for obj, dataList in allDatas.items():
    if 'Arg_Example1' not in dataList[0] and 'requset example' in dataList[0]:
        newDataList = []
        for data in dataList:
            request = data['requset example']
            try:
                if request is not None:
                    request = json.loads(request)
                else:
                    request = {}
                i = 1
                while 'Arguments' + str(i) in data:
                    arg = data['Arguments' + str(i)]
                    if arg in request:
                        data['Arg_Example' + str(i)] = request[arg]
                    else:
                        data['Arg_Example' + str(i)] = None
                    i = i + 1
                newDataList.append(data)
            except:
                print(request)
        allDatas[obj] = newDataList

allArgs = {}
objs = {}
allArgList, allObjList = getAllArguments(allDatas)

# updata the allLinkArgRes, get the most right one.
allInsertDatas = {}
allSelectDatas = {}
allUpdateDatas = {}
allLinkArgRes = {}
# 0. build
sameArgList = {}
tempAllDatas = {}
for key in allDatas.keys():
    data = allDatas[key]
    insertDatas, selectDatas, updateDatas = getObjectCRU(data, allObjList)
    allInsertDatas.update(insertDatas)
    allSelectDatas.update(selectDatas)
    allUpdateDatas.update(updateDatas)
    allDataList = []
    allDataList.append(data)
    allDataList.append(insertDatas)
    allDataList.append(selectDatas)
    allDataList.append(updateDatas)
    tempAllDatas[key] = allDataList
for key in tempAllDatas.keys():
    allDataList = tempAllDatas[key]
    # 3. first, insert, second, select, last, update

    allArgList, allInsertDatas, allLinkArgRes,sameArgList = getLinksBetweenArgsAndRes(allDataList[0], allArgList, allInsertDatas, allDataList[2], allDataList[3], allLinkArgRes, sameArgList)
    #getLinksBetweenArgsAndRes(data, allArgList, insertDatas, selectDatas, updateDatas, allLinkArgRes)

for arg, methods in sameArgList.items():
    link = []
    for m in methods:
        linkArgRes = allLinkArgRes[m]
        data = []
        if arg in linkArgRes:
            data = linkArgRes[arg]
        else:
            for karg in linkArgRes.keys():
                if karg.lower() == arg:
                    data = linkArgRes[karg]
                    break
        if len(data) > len(link):
            link = data.copy()
    if len(link) > 0:
        for m in methods:
            linkArgRes = allLinkArgRes[m]
            data = []
            if arg in linkArgRes:
                data = linkArgRes[arg]
                if len(data) < len(link):
                    linkArgRes[arg] = link
            else:
                for karg in linkArgRes.keys():
                    if karg.lower() == arg:
                        data = linkArgRes[karg]
                        if len(data) < len(link):
                            linkArgRes[karg] = link
                        break
        allLinkArgRes[m] = linkArgRes

for k in allArgs:
    items = k.split('----')
    arg = items[1]
    methods = allArgs[k]
    link = []
    for m in methods:
        items = m.split('***')
        m = items[0]
        linkArgRes = allLinkArgRes[m]
        data = linkArgRes[arg]
        if len(data) > len(link):
            link = data
    if len(link) > 0:
        for m in methods:
            items = m.split('***')
            m = items[0]
            linkArgRes = allLinkArgRes[m]
            data = linkArgRes[arg]
            if len(data) < len(link):
                linkArgRes[arg] = link
        allLinkArgRes[m] = linkArgRes


allResult = {}
# V and A1 are in the same channel, while A2 is in another channel
tokenV = []
tokenA1 = []
tokenA2 = []

hasCreate = False
runOrder = ['SELECT', 'UPDATE', 'DELETE']
allResult1 = {}
allResult2 = {}
result3 = {}
result4 = {}
allOtherDatas = {}
preDatas = {}

depRes = {}
todoList = []
idatas = {}
for k in allInsertDatas.keys():
    trueArgs = allArgList[k]
    items = k.split('---')
    if len(items) == 3:
        datas = allDatas[items[1]]
        for data in datas:
            if data['Method URL'].replace(baseURL, '') == items[0] and data[' HTTP method'] == items[2]:
                insertData = []
                insertData.append(data)
                newone = {}
                linkArgRes = allLinkArgRes[k]

                for arg,d in linkArgRes.items():
                    trueArg = trueArgs[arg]
                    if len(d) == 0:
                        newone[arg] = ''
                    else:
                        for i in range(1, 17):
                            if 'Arguments' + str(i) not in data:
                                print('dd')
                            if data['Arguments' + str(i)] == trueArg:
                                if data['(Arg_Req)' + str(i)] == 'Optional':
                                    ddddd= '1'
                                    #newone[arg] = ''
                                else:
                                    newone[arg] = d[0]
                                break
                        if arg not in newone and '{' in data['Method URL']:
                            newone[arg] = d[0]

                insertData.append(newone)
                idatas[items[0]] = insertData
allOtherDatas = {}
otherDatas = {}
otherDatas.update(allSelectDatas)
otherDatas.update(allUpdateDatas)

for k in otherDatas.keys():
    trueArgs = allArgList[k]
    items = k.split('---')
    if len(items) == 3:
        datas = allDatas[items[1]]
        for data in datas:
            if data['Method URL'].replace(baseURL, '') == items[0] and data[' HTTP method'] == items[2]:
                otherData = []
                otherData.append(data)
                newone = {}
                linkArgRes = allLinkArgRes[k]

                for arg,d in linkArgRes.items():
                    trueArg = trueArgs[arg]
                    if len(d) == 0:
                        newone[arg] = ''
                    else:
                        for i in range(1, 14):
                            if data['Arguments' + str(i)] == trueArg:
                                if data['(Arg_Req)' + str(i)] == 'Optional' and '{'+arg+'}' not in data['Method URL'] :
                                    newone[arg] = ''
                                else:
                                    newone[arg] = d[0]
                                break
                        if i == 13 and arg not in newone:
                            newone[arg] = d[0]
                otherData.append(newone)
                allOtherDatas[items[0]] = otherData
allResponsDict = {}
allResponsDict.update(allInsertDatas)
allResponsDict.update(allSelectDatas)
allResponsDict.update(allUpdateDatas)

for m, ds in idatas.items():
    newDs = ds.copy()
    if len(newDs[1]) == 0:
        result1 = getResponse(allArgList, allResponsDict, newDs, preDatas, depRes, tokenV, 'initialuser')
        print(m)
        print(result1)
    else:
        go = True
        if go:
            newDs[1] = {}
            result1 = getResponse(allArgList, allResponsDict, newDs, preDatas, depRes, tokenV, 'initialuser')
            if 'trackingId' not in str(result1) and 'detailed_error' not in str(result1): #result1['ok']:
                depRes[m] = result1
            else:
                todoList.append(m)
            print(m)
            print(result1)
        else:
            todoList.append(m)

i = 0
while len(todoList) != i:
    m = todoList[i]
    print(m)
    ds = idatas[m]
    result1 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenV, 'initialuser')
    i = i + 1
    if 'detailed_error' in str(result1) and 'api/v4/channels/{channel_id}/members' in m:
        todoList.append(m)
    else:
        if 'trackingId' not in str(result1) and 'detailed_error' not in str(result1): #result1['ok']:
            depRes[m] = result1
        print(m)
        print(result1)


newAllOtherDatas = {}
print('********************************************************')
for k, v in allOtherDatas.items():
    data = v[0]
    obj = data['OBJECT']
    dataList = []
    if obj in newAllOtherDatas:
        dataList = newAllOtherDatas[obj]
    dataList.append(v)
    newAllOtherDatas[obj] = dataList

deleteList = []
for obj, data in newAllOtherDatas.items():
    if obj == 'workspace':
        continue
    for func in runOrder:
        for ds in data:
            d = ds[0]
            try:
                if d['CRUD'] == func:
                    if d['CRUD'] == 'DELETE':
                        deleteList.append(ds)
                        continue
                    if len(ds[1]) == 0:
                        result4 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA2, 'xxxx')
                        result3 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA1, 'xxxx')
                    else:
                        result4 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA2, 'xxxx')
                        result3 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA1, 'xxxx')
                    if result3 is not None and 'trackingId' not in str(result3) and 'detailed_error' not in str(
                            result3) and 'error' not in str(result3) and func != 'SELECT' and 'code' not in str(result3):
                        print(d['Method URL'].replace(baseURL, '') + ' has vulnerability1!')
                    if result4 is not None and 'trackingId' not in str(result4) and 'detailed_error' not in str(
                            result4) and 'error' not in str(result4)  and 'code' not in str(result4):
                        print(d['Method URL'].replace(baseURL, '') + ' has vulnerability2!')
                    if result3 is not None and 'trackingId' not in str(result3) and 'detailed_error' not in str(
                            result3) and 'error' not in str(result3)  and 'code' not in str(result3):
                        depRes[d['Method URL']] = result3
                        allResult1[d['Method URL'].replace(baseURL, '')] = result3
                    if result4 is not None and 'trackingId' not in str(result4) and 'detailed_error' not in str(
                            result4) and 'error' not in str(result4) and 'code' not in str(result4):
                        depRes[d['Method URL']] = result4
                        allResult2[d['Method URL'].replace(baseURL, '')] = result4
            except Exception:
                print(d['Method URL']+' error newAllOtherData')

for ds in deleteList:
    try:
        if len(ds[1]) == 0:
            result4 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA2, 'xxxx')
            result3 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA1, 'xxxx')
        else:
            result4 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA2, 'xxxx')
            result3 = getResponse(allArgList, allResponsDict, ds, preDatas, depRes, tokenA1, 'xxxx')

        if result3 is not None and 'trackingId' not in str(result3) and 'detailed_error' not in str(
                result3) and 'error' not in str(result3) and func != 'SELECT' and 'code' not in str(result3):
            print(d['Method URL'].replace(baseURL, '') + ' has vulnerability1!')
        if result4 is not None and 'trackingId' not in str(result4) and 'detailed_error' not in str(
                result4) and 'error' not in str(result4) and 'code' not in str(result4):
            print(d['Method URL'].replace(baseURL, '') + ' has vulnerability2!')
        if result3 is not None and 'trackingId' not in str(result3) and 'detailed_error' not in str(
                result3) and 'error' not in str(result3) and 'code' not in str(result3):
            depRes[d['Method URL']] = result3
            allResult1[d['Method URL'].replace(baseURL, '')] = result3
        if result4 is not None and 'trackingId' not in str(result4) and 'detailed_error' not in str(
                result4) and 'error' not in str(result4) and 'code' not in str(result4):
            depRes[d['Method URL']] = result4
            allResult2[d['Method URL'].replace(baseURL, '')] = result4
