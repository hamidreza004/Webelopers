# -*- coding: utf-8 -*-

from suds.client import Client

from .config import WEBSERVICE_WSDL


def payment_request(payment, email=None, mobile=None):
    client = Client(WEBSERVICE_WSDL)
    result = client.service.PaymentRequest(payment.merchant_id,
                                           payment.amount,
                                           payment.description,
                                           email,
                                           mobile,
                                           payment.callback_url)
    if result.Status == 100:
        return result.Authority
    else:
        raise Exception("Can't send request to zarinpal")


def verify(team):
    client = Client(WEBSERVICE_WSDL)
    result = client.service.PaymentVerification(team.payment.merchant_id,
                                                team.transaction,
                                                team.payment.amount)
    if result.Status == 100:
        return 1
    elif result.Status == 101:
        return 0
    else:
        return -1
