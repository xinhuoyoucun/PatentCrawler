# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from logbook import Logger
from requests.utils import dict_from_cookiejar
from scrapy.downloadermiddlewares.retry import RetryMiddleware

import controller as ctrl
from service.account import login, update_cookies

logger = Logger(__name__)


class PatentMiddleware(RetryMiddleware):

    def process_request(self, request, spider):
        if ctrl.PROXIES is not None:
            request.meta['proxy'] = "http://%s" % (ctrl.PROXIES.get('http'))
        if ctrl.COOKIES is not None:
            request.cookies = dict_from_cookiejar(ctrl.COOKIES)

    def process_response(self, request, response, spider):
        body = response.body_as_unicode()
        if body.find(
                'window.location.href = contextPath +"/portal/uilogin-forwardLogin.shtml";') != -1 or response.status == 404:
            logger.info('未登录，登陆中，请稍后···')
            if login():
                return self._retry(request, 'unlogin', spider)
        return response

    def process_exception(self, request, exception, spider):
        logger.error(exception)