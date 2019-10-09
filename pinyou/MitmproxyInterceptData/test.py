# -*- coding: utf-8 -*-

import mitmproxy.http
from mitmproxy import ctx
import time
import xlwt


class Counter:
    def __init__(self):
        self.num = 0
        self.requestNum = 0
        self.responseOrErrorNum = 0
        self.aa = 0
        self.all_arr = [['请求路径', '请求域名', '请求path', '请求大小(b)', '响应大小', '响应类型', '请求响应时间差(s)', '请求开始时间', '请求响应结束时间']]

    def http_connect(self, flow: mitmproxy.http.HTTPFlow):
        flow.customField = []

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        self.requestNum = self.requestNum + 1
        flow.start_time = time.time()
        flow.customField = [flow.request.url, flow.request.host, flow.request.path]
        self.all_arr.append(flow.customField)
        # print('----------',len(self.all_arr))

    def error(self, flow):
        self.aa = self.aa + 1
        self.responseOrErrorNum = self.responseOrErrorNum + 1
        flow.customField.append("Error response")

    def response(self, flow):
        self.aa = self.aa + 1
        self.responseOrErrorNum = self.responseOrErrorNum + 1
        flow.end_time = time.time()

        try:
            flow.customField.append(flow.request.headers['Content-Length'])
        except:
            flow.customField.append("")
        try:
            flow.customField.append(flow.response.headers['Content-Length'])
        except:
            flow.customField.append("")
        try:
            flow.customField.append(flow.response.headers['Content-Type'])
        except Exception:
            flow.customField.append("")
        try:
            time_gap = flow.end_time - flow.start_time
            flow.customField.append(time_gap)

        except Exception:
            flow.customField.append("")

        self.formatoutput(flow)
        self.save_excel(self.all_arr, 'toutiao-content-10.xls')

    def formatoutput(self, flow):
        ctx.log.info("We've seen %d flows" % self.num)
        try:
            flow.customField.append(flow.start_time)
        except:
            flow.customField.append("")
        try:
            flow.customField.append(flow.end_time)
        except:
            flow.customField.append("")

    def save_excel(self, array, filename):
        workbook = xlwt.Workbook()
        worksheet = workbook.add_sheet('test')
        for x in range(len(array)):
            for y in range(len(array[x])):
                worksheet.write(x, y, array[x][y])
        workbook.save(filename)


addons = [
    Counter()
]
