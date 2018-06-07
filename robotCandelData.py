from __future__ import print_function
from time import sleep, strftime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message

def allDataHandler(msg):
    print(msg)


def make_contract():
    cont = Contract()
    cont.m_secType = "CFD"
    cont.m_symbol = "IBDE30"
    cont.m_currency = "EUR"
    cont.m_exchange = "SMART"
    #cont.m_expiry = ''
    #cont.m_strike = 0.0
    #cont.m_right = True
    return cont

if __name__ == '__main__':
    conn = ibConnection(host='127.0.0.1', port=7497, clientId=999)
    conn.registerAll(allDataHandler)
    conn.connect()
    sleep(1)
    contMe = make_contract()
    conn.reqMarketDataType( 4 )
    conn.reqRealTimeBars(3101, contMe, 5, "TRADES", True)
    sleep(5)
    conn.disconnect()
