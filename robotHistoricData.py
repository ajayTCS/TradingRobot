from __future__ import print_function
from time import sleep, strftime
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message


def all_message_handler(msg):
    print(msg)

def historical_data_handler(msg):
    # The response data callback function
    # print (msg.reqId, msg.date, msg.open, msg.close, msg.high, msg.low)
    print(msg)


if __name__ == '__main__':
    # Establish IB connection, make sure you have the correct port, clientId
    conn = ibConnection(host='127.0.0.1', port=7497, clientId=999)

    # Register the response callback function and type of data to be returned
    conn.register(historical_data_handler, message.historicalData)
    conn.registerAll(all_message_handler)
    conn.connect()

    # Establish a Contract object and the params for the request
    req = Contract()
    req.m_secType = "CFD" 
    req.m_symbol = "IBDE30"
    req.m_currency = "EUR"
    req.m_exchange = "SMART"
    req.m_primaryExch= "SMART"
    endtime = strftime('%Y%m%d %H:%M:%S')
    conn.reqHistoricalData(1,req,endtime,"14 D","1 min","BID",1,1)

    # Make sure the connection don't get disconnected prior the response data return
    sleep(5)
    conn.disconnect()
