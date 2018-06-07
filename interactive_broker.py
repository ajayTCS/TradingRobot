from __future__ import print_function
from ib.opt import Connection, message
from ib.ext.Contract import Contract
from ib.ext.Order import Order
from random import randint
from time import sleep, strftime

def all_message_handler(msg):
    print("hi")
    print(msg)

def my_next_valid_id_handler(msg):
    print("inside robot next id validation")
    print(msg)

def make_contract(symbol, sec_type, exch, prim_exch, curr):
    Contract.m_symbol=symbol
    Contract.m_secType=sec_type
    Contract.m_exchange=exch
    Contract.m_primaryExch=prim_exch
    Contract.m_currency=curr
    return Contract

def make_order(action, quantity, price=None):
    if price is not None:
        order=Order()
        order.m_orderType='LMT'
        order.m_totalQuantity= quantity
        order.m_action= action
        order.m_lmtPrice= price
    else:
        order=Order()
        order.m_orderType='MKT'
        order.m_totalQuantity= quantity
        order.m_action= action
    return order

def my_account_handler(msg):
    print("account data")
    print(msg)

def my_tick_handler(msg):
    print("tic data")
    print(msg)

def my_hist_data_handler(msg):
    print("historic data")
    print(msg)

def historiDataWrapper():
    con = Connection.create(port=7497,clientId=999)
    con.register(my_account_handler, 'UpdateAccountValue')
    con.register(my_tick_handler, message.tickSize, message.tickPrice)
    con.register(my_hist_data_handler, message.historicalData)
    con.register(my_next_valid_id_handler, message.nextValidId)
    con.registerAll(all_message_handler)
    con.connect()
    print(con.isConnected())
    qqqq1 = Contract()
    qqqq1.m_secType = "STK" 
    qqqq1.m_symbol = "GE"
    qqqq1.m_currency = "USD"
    qqqq1.m_exchange = "SMART"
    qqqq1.m_primaryExch = "SMART"
    endtime = strftime('%Y%m%d %H:%M:%S')
    print(endtime)
    print(con.reqHistoricalData(1,qqqq1,endtime,"1 W","10 secs","BID",1,1))
    con.reqHistoricalData(1,qqqq1,endtime,"1 W","1 day","BID",1,2)
    #con.reqHistoricalData(0, "CSCO", "STK", "", 0, "", "", "NASDAQ", "USD", 0, "20101015 17:05:00", "1 W", "1 min", "TRADES", 1, 1);
    con.disconnect()


def main():
    conn=Connection.create(port=7497, clientId=999)
    conn.registerAll(all_message_handler)
    conn.connect()
    oid= 1000233495
    print(oid)
    cont= make_contract('GE', 'STK', 'SMART', 'SMART', 'USD')
    offer= make_order('SELL', 1)
    conn.placeOrder(oid, cont, offer)
    sleep(5)
    conn.disconnect()
    historiDataWrapper()


if __name__ == '__main__':
    main()
    

