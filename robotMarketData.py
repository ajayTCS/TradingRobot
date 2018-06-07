from __future__ import print_function
from ib.ext.Contract import Contract
from ib.opt import ibConnection, message
from time import sleep

# print all messages from TWS
def watcher(msg):
    print(msg)
    print("inside watcher")

# show Bid and Ask quotes
def my_BidAsk(msg):
    print("inside bid ask")
    print(msg.field)
    if msg.field == 66:
        print ('%s:%s: bid: %s' % (contractTuple[0],
                       contractTuple[6], msg.price))

    elif msg.field == 67:
        print ('%s:%s: ask: %s' % (contractTuple[0], contractTuple[6],msg.price))



def makeStkContract(contractTuple):
    newContract = Contract()
    newContract.m_symbol = contractTuple[0]
    newContract.m_secType = contractTuple[1]
    newContract.m_exchange = contractTuple[2]
    newContract.m_currency = contractTuple[3]
    newContract.m_expiry = contractTuple[4]
    newContract.m_strike = contractTuple[5]
    newContract.m_right = contractTuple[6]
    print ('Contract Values:%s,%s,%s,%s,%s,%s,%s:' % contractTuple)
    return newContract

if __name__ == '__main__':
    con = ibConnection(port = 7497, clientId = 9615)
    con.registerAll(watcher)
    showBidAskOnly = False  # set False to see the raw messages
    if showBidAskOnly:
        con.unregister(watcher, message.tickSize, message.tickPrice,
                   message.tickString, message.tickOptionComputation)
        con.register(my_BidAsk, message.tickPrice)
    con.connect()
    sleep(1)
    tickId = 1221
    # MarketDataTypeEnum = Enum("N/A", "REALTIME", "FROZEN", "DELAYED", "DELAYED_FROZEN")
    # Note: Option quotes will give an error if they aren't shown in TWS
    contractTuple = ('IBDE30', 'CFD', 'SMART', 'EUR', '', 0.0, 'False')
    # contractTuple = ('QQQQ', 'OPT', 'SMART', 'USD', '20070921', 47.0, 'CALL')
    # contractTuple = ('ES', 'FUT', 'GLOBEX', 'USD', '200709', 0.0, '')
    # contractTuple = ('ES', 'FOP', 'GLOBEX', 'USD', '20070920', 1460.0, 'CALL')
    # contractTuple = ('EUR', 'CASH', 'IDEALPRO', 'USD', '', 0.0, '')
    stkContract = makeStkContract(contractTuple)
    print ('* * * * REQUESTING MARKET DATA * * * *')
    #con.reqMktData(tickId, stkContract, '', False)
    con.reqMarketDataType( 3 )
    # requesting the market data in a infinite timer
    con.reqMktData(tickId, stkContract, '', False)
    # for grouped data like a baar
    # request is highly throttled
    # keep in mind that 
    # con.reqMktData(tickId, stkContract, '', True)
    # for real time bars
    # request is throttled
    # please keep in mind that
    # con.reqRealTimeBars(3001, stkContract, 5, "MIDPOINT", True)
    sleep(30)
    print ('* * * * CANCELING MARKET DATA * * * *')
    con.cancelMktData(tickId)
    sleep(1)
    con.disconnect()

