# -*- coding: utf-8 -*-
"""
Created on Fri Dec  8 14:35:57 2017

@author: sonng
"""
import pandas as pd
from finance_util import get_data, fill_missing_values, optimize_portfolio, compute_portfolio, \
                         get_data_from_cophieu68_openwebsite, get_data_from_SSI_website, analysis_alpha_beta,get_info_stock
from strategy import ninja_trading, hedgefund_trading, bollinger_bands, short_selling, hung_canslim, mean_reversion, get_statistic_index
from plot_strategy import plot_hedgefund_trading, plot_ninja_trading, plot_trading_weekly,plot_shortselling_trading, plot_canslim_trading
from machine_learning import price_predictions, ML_strategy

def portfolio_management():
    df = pd.DataFrame()
    tickers = ['ANV','PHC','HLD','GEX', 'TVN']
    # chu y xu ly cac CP nhu PVS (co kha nang thoat hang), ACB, MBS, NVB(ngam lau dai doi thoi),  (HAR, DVN, VIX): sieu lo
    buy_price = [23.7, 19.5, 18.6, 38.8, 10.65]
    shares_number = [400, 500, 500, 260, 1900]
    
    low_candle = [22.3, 18.9, 15.9, 37, 10]
    
    df['Ticker'] = tickers
    df = df.set_index('Ticker')    
    df['Buy'] = buy_price
    df['Cut_loss'] = df['Buy']*0.97
    df['Target'] = df['Buy']*1.2
    df['Shares'] = shares_number
    df['Values'] = df['Buy']*df['Shares']
    df['Low'] = low_candle
    df['MinPort'] = df['Low']*df['Shares']
    df['MaxLoss'] = df['MinPort'] - df['Buy']*df['Shares']
    #df['']
    actual_price = []
    for ticker in tickers:        
        print(ticker)
        try:
            df_temp = get_info_stock(ticker)
            actual_price.append(df_temp['Close'].iloc[-1]) 
    #        print(df_temp['Close'].iloc[-1])
    #        print(df['Target'][ticker])
            if (df_temp['Close'].iloc[-1] >= df['Target'][ticker]):
                print(' SELL TARGET signal : actual price:' , df_temp['Close'].iloc[-1], 'target:', df['Target'][ticker])
            else:
                if (df_temp['Close'].iloc[-1] <= df['Cut_loss'][ticker]):
                    print(' CUT_LOSS signal : actual price:' , df_temp['Close'].iloc[-1], 'cut loss: ', df['Cut_loss'][ticker])
                else:
                    print(' Continue HOLDING : actual price:', df_temp['Close'].iloc[-1], ' actual/buy ratio: ' , round(df_temp['Close'].iloc[-1]/df['Buy'][ticker],3))
        except Exception as e:
            print(" Error in symbol : ", ticker) 
            print(e)
            pass
    
    df['Current'] = actual_price
    df['Port_val'] = df['Current']*df['Shares']
    df['Diff_val'] = df['Port_val'] - df['Values']
    portfolio_diff =  df['Diff_val'].sum(axis = 0)
    
    print(' Porfolio value :', df['Diff_val'].values, ' Sum: ', portfolio_diff)
    print(' Max loss:', df['MaxLoss'].sum(axis=0))
#    return df
    




def getliststocks(typestock = "^VNINDEX"):
    benchmark = ["^VNINDEX", "^HASTC", "^UPCOM"]
    
    nganhang = ['ACB','CTG','VPB','VCB','NVB', 'LPB', 'VIB', 'BID','HDB', 'EIB', 'MBB', 'SHB', 'STB']
    
    thuysan = ['VHC', 'ANV']
    daukhi = ['PVS','PVD','PVB','PLX', 'BSR', 'POW','TDG','GAS']
    batdongsan =['HAR', 'HLD', 'DXG', 'NVL', 'KDH', 'CEO', 'VIC','NDN','PDR','VPI', 'VRE','ASM','EVG','NBB' ]
    chungkhoan = ['HCM', 'SSI', 'VND', 'TVB','TVS', 'BVS','MBS','FTS', 'HCM', 'VIX', 'ART','SHS', 'VCI']
    baohiem = ['BVH', 'BMI']
    xaydung = ['CTD', 'HBC', 'PHC','ROS','FLC','VMC']
    duocpham = ['DVN', 'DHG']
    hangkhong = ['HVN','VJC']
    thep = ['TVN', 'HPG']
    cntt = ['MWG', 'FPT']
    nhua = ['BMP']
    vatlieuxd = ['VCS']
    caosu = ['PHR', 'DRC']
    anuong = ['VNM', 'SAB']
    
    
    symbolsHNX = [ 'ALV',  'TNG', 'BVS',  'NVB',   "VE9", 
                  'ACB', 'BCC', 'CVN', 'CEO', 'DBC',  'DST', 'HUT', 'SD9', 'HLD', 'HHG', 'NSH', 'DS3',
                  'LAS',  'MBS', 'NDN', 'PGS', 'PVC', 'PVI',   'PHC', 'PVE', 'PVG', 'PVB',
                  'PVS', 'SHB', 'SHS', 'TTB','VC3', 'VCG','VCS', 'VGC','VMC','VIX', 'TVC', 'SPP',
                 'VKC', 'VPI', 'NBC', 'VGS']
    
    symbolsVNI = [ 'ASP', 'APG', 'APC', 'ANV', "ASM", "BSI", "BWE", 'CEE',
                  'BCG', "BFC", "BID", "BMI", "BMP", "BVH",  'CTS', 'CTI', "CII", "CTD", "CAV", "CMG", "CSM", "CSV", "CTG", 'CHP', 'C47', 
               "DCM","DHG", "DIG",  "DPM","DPR", "DRH",  "DQC", "DRC", "DXG", 'DGW', 'DHA', 'DHC', 'DAH',
               "ELC", "EVE", 'EVG', "FCN","FIT","FLC", 'FMC', 'FTS', "FPT", "GAS", "GMD", "GTN", 
                'HAX', "HAG", "HHS", "HNG",  "HT1",  'HAR', 'HII', 'HCD',
               "HSG", "HDG", "HCM", "HPG", "HBC", 'LDG', 'LCG', 'LGL', 'LHG', 'HDC',
               'IDI', "IJC",  "KBC", "KSB",  "KDH", "KDC", 
               "MBB", "MSN", "MWG", "NKG", "NLG", "NT2", "NVL", "NBB", 'NAF',
                "PVT","PVD","PHR","PGI","PDR","PTB", "PNJ",  "PC1",   "PLX", "PXS",
                "PPC", "PAC", 'QBS', "QCG", "REE",  
                'SHI',"SAM","SJD","SJS","STB","STG","SKG",  "SSI", "SBT", "SAB", 'TLD', 'PMG',
                "VSH","VNM", "VHC", "VIC", "VCB", "VSC", "VJC", "VNS" , 'TVS', 'VDS', 'TNI','TLH',
                'ITC','LSS',  'PME', 'PAN','TCH', 'TDH',  'GEX','VCI', 'VIS',
                'TDC','TCM', 'VNE', 'SHN', 'AAA','SCR',  'TDG', 'VRC',  'SRC',
                'EIB','VPB','VRE','ROS',"VND", "HDB",  "SMC", "C32","CVT",'VPH','VNG','VIP',
                'NTL','PET','VPD','VTO','SHA','DCL', 'GIL', 'TEG', 'AST','DAG', 'HAH']
    
    symbolsUPCOM = ['TBD', 'LPB', 'QNS',   'ART',  'ACV',  "SWC", "NTC","DVN", 'HVN', 'HPI','IDC',  'MSR', 
                    'VGT','TVN','TVB','TIS','VIB','DRI', 'POW', 'BSR','MVC','MCH']
    
    if typestock == "ALL":
        symbols = benchmark + symbolsVNI + symbolsHNX + symbolsUPCOM 
    if typestock == "^VNINDEX":
        symbols = symbolsVNI
    if typestock == "^HASTC":
        symbols = symbolsHNX
    if typestock == "^UPCOM":
        symbols = symbolsUPCOM
    if typestock == "TICKER":
        symbols = symbolsVNI + symbolsHNX + symbolsUPCOM 
    if typestock == "BENCHMARK":
        symbols = benchmark
#    symbols =  high_cpm
    symbols = pd.unique(symbols).tolist()
    symbols = sorted(symbols)
    
    
    
    return symbols
    
    
    

def get_stocks_highcpm(download = True, source = "ssi"):

    data = pd.read_csv('fundemental_stocks_all.csv', parse_dates=True, index_col=0)
    df = data.query("MeanVol_10W > 100000")
    df = df.query("FVQ > 0")
    df = df.query("CPM > 1.4")
    df = df.query("EPS > 0")
    tickers  = df.index
    
    if download:
        if source == "cp68":
            get_data_from_cophieu68_openwebsite(tickers)
        else:
           get_data_from_SSI_website(tickers) 
    
    
    return tickers
    
    
def analysis_trading(tickers, start, end, update = False, source = "cp68"):
    
    if tickers == None:
        tickers = getliststocks(typestock = "TICKER")
        
#    data = pd.read_csv('fundemental_stocks_all.csv', parse_dates=True, index_col=0)
#    data['Diff_Price'] = data['Close'] - data['EPS']*data['PE']/1000
#    data['EPS_Price'] = data['EPS']/data['Close']/1000
#    df = data.query("MeanVol_10W > 80000")
#    df = data.query("MeanVol_13W > 80000")
#    df = df.query("EPS > 1000")
#    df = df.query("ROE > 15")
#       
#    canslim_symbol = df.index.tolist()
#    
#    tickers = canslim_symbol
    
    for ticker in tickers:
#        print(" Analysing ..." , ticker)
        try:
#            ninja_trading(ticker, start, end, realtime = update, source = source)
#            hedgefund_trading(ticker, start, end, realtime = update, source = source)
            hung_canslim(ticker, start, end, realtime = update, source = source)
#            mean_reversion(ticker, start, end, realtime = update, source = source)
#            bollinger_bands(ticker, start, end, realtime = update, source = source)
#            short_selling(ticker, start, end, realtime = update, source = source)
        except Exception as e:
            print (e)
            print("Error in reading symbol: ", ticker)
            pass
    
    


def get_csv_data(source = "cp68"):

    symbols = getliststocks(typestock = "ALL")
     
    if source == "cp68":
        get_data_from_cophieu68_openwebsite(symbols)
    else:
       get_data_from_SSI_website(symbols) 
    return symbols
 

            
def predict_stocks(tickers, start, end):
    for ticker in tickers:
        print('Prediction of ticker .................' , ticker)
        price_predictions(ticker, start, end, forecast_out = 5)
        print(' End of prediction ticker ...................', ticker)

def passive_strategy(start_date, end_date, market = "^VNINDEX"):

    symbols = getliststocks(typestock = market)
    
    dates = pd.date_range(start_date, end_date)  # date range as index
    df_data = get_data(symbols, dates, benchmark = market)  # get data for each symbol
    
    df_volume = get_data(symbols, dates, benchmark = None, colname = '<Volume>')  # get data for each symbol
    df_high = get_data(symbols, dates, benchmark = None, colname = '<High>')
    df_low = get_data(symbols, dates, benchmark = None, colname = '<Low>')
    
#    covariance = numpy.cov(asset , SPY)[0][1]  
#    variance = numpy.var(asset)
#    
#    beta = covariance / variance 
    
    
    vol_mean = pd.Series(df_volume.mean(),name = 'Volume')
    max_high = pd.Series(df_high.max(), name = 'MaxHigh')
    min_low = pd.Series(df_low.min(), name = 'MinLow')
    cpm = pd.Series(max_high/min_low, name = 'CPM')
    # Fill missing values
    fill_missing_values(df_data)

    
    # Assess the portfolio
    
    allocations, cr, adr, sddr, sr  = optimize_portfolio(sd = start_date, ed = end_date,
        syms = symbols,  benchmark = market, gen_plot = True)

     # Print statistics
    print ("Start Date:", start_date)
    print ("End Date:", end_date)
    print ("Symbols:", symbols)
    print ("Optimal allocations:", allocations)
    print ("Sharpe Ratio:", sr)
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)
    
    investment = 50000000
    df_result = pd.DataFrame(index = symbols)    
    df_result['Opt allocs'] = allocations
    df_result['Cash'] = allocations * investment
    df_result['Volume'] = vol_mean
    df_result['Close'] = df_data[symbols].iloc[-1,:].values
    #    df_result['MaxH'] = max_high
#    df_result['MinL'] = min_low
    df_result['CPM'] = cpm
    df_result['Shares'] = round(df_result['Cash']/df_result['Close'].values/1000,0)
    df_result ['Volatility'] = df_data[symbols].pct_change().std() 
    
    alpha_beta = analysis_alpha_beta(df_data, symbols, market)
    df_result['Alpha'] = alpha_beta['Alpha']
    df_result['Beta'] = alpha_beta['Beta']
    
    relative_strength = 40*df_data[symbols].pct_change(periods = 65).fillna(0) \
             + 30*df_data[symbols].pct_change(periods = 130).fillna(0) \
             + 30*df_data[symbols].pct_change(periods = 260).fillna(0)     
    
    df_result ['RSW'] = relative_strength.iloc[-1,:].values

    return df_result, df_data


def active_strategy(start_date, end_date, update = False, source = "cp68", market = "^VNINDEX"):

    symbols = getliststocks(typestock = market)
    
    for ticker in symbols:
        try:
#            ninja_trading(ticker, start, end, realtime = update, source = source)
#            hedgefund_trading(ticker, start, end, realtime = update, source = source)
            hung_canslim(ticker, start = start_date, end = end_date, realtime = update, source = source, market = market)
#            mean_reversion(ticker, start, end, realtime = update, source = source)
#            bollinger_bands(ticker, start, end, realtime = update, source = source)
#            short_selling(ticker, start, end, realtime = update, source = source)
        except Exception as e:
            print (e)
            print("Error in reading symbol: ", ticker)
            pass

def rebalancing_porfolio(symbols = None, bench = '^VNINDEX'):

   
    start0 = "2015-1-2"
    end0 = "2017-1-2"
    allocations, cr, adr, sddr, sr  = optimize_portfolio(sd = start0, ed = end0,
            syms = symbols,  benchmark = bench, gen_plot = True)
    print ("Optimize start Date:", start0)
    print ("Optimize end Date:", end0) 
    print ("Optimize volatility (stdev of daily returns):", sddr)
    print ("Optimize average Daily Return:", adr)
    print ("Optimize cumulative Return:", cr)
    print(" -----------------------------------------------------")
    start_date_list = ["2017-1-3", "2017-7-3"]
    end_date_list = ["2017-7-2",  "2018-4-1"]
    for start, end in zip(start_date_list, end_date_list):    
        
        cr, adr, sddr, sr  = compute_portfolio(sd = start, ed = end,
            syms = symbols, allocs = allocations, benchmark = bench, gen_plot = True)
        print ("Start Date:", start)
        print ("End Date:", end) 
        print ("Volatility (stdev of daily returns):", sddr)
        print ("Average Daily Return:", adr)
        print ("Cumulative Return:", cr)  
        print(" -----------------------------------------------------")
        allocations, cr, adr, sddr, sr  = optimize_portfolio(sd = start, ed = end,
            syms = symbols,  benchmark = bench, gen_plot = False)
        print ("Optimize volatility (stdev of daily returns):", sddr)
        print ("Optimize average Daily Return:", adr)
        print ("Optimize cumulative Return:", cr)
        print(" -----------------------------------------------------")
        
    
    
    
    
    # Out of sample testing optimisation algorithm
    
    end_date = "2018-5-21"
    start_date = "2018-4-2"
    
    cr, adr, sddr, sr  = compute_portfolio(sd = start_date, ed = end_date,
            syms = symbols, allocs = allocations, benchmark = bench, gen_plot = True)
    print("....................... Out of sample performance .................")
    print ("Start Date:", start_date)
    print ("End Date:", end_date) 
    print ("Volatility (stdev of daily returns):", sddr)
    print ("Average Daily Return:", adr)
    print ("Cumulative Return:", cr)  
    # Assess the portfolio
    investment = 60000000
    df_result = pd.DataFrame(index = symbols)    
    df_result['Opt allocs'] = allocations
    df_result['Cash'] = allocations * investment

    dates = pd.date_range(start_date, end_date)  # date range as index
    df_data = get_data(symbols, dates, benchmark = bench)  # get data for each symbol
    
   
    df_high = get_data(symbols, dates, benchmark = None, colname = '<High>')
    df_low = get_data(symbols, dates, benchmark = None, colname = '<Low>')
    
    max_high = pd.Series(df_high.max(), name = 'MaxHigh')
    min_low = pd.Series(df_low.min(), name = 'MinLow')
    cpm = pd.Series(max_high/min_low, name = 'CPM')
    volatility = df_data[symbols].pct_change().std()  
    
    # Fill missing values
            
    df_result['Close'] = df_data[symbols].iloc[-1,:].values    
    df_result['CPM'] = cpm
    df_result['Shares'] = round(df_result['Cash']/df_result['Close'].values/1000,0)
    df_result ['Volatility'] = volatility
    
    alpha_beta = analysis_alpha_beta(df_data, symbols, market = bench)
    df_result['Alpha'] = alpha_beta['Alpha']
    df_result['Beta'] = alpha_beta['Beta']
    
    relative_strength = 40*df_data[symbols].pct_change(periods = 65).fillna(0) \
             + 30*df_data[symbols].pct_change(periods = 130).fillna(0) \
             + 30*df_data[symbols].pct_change(periods = 260).fillna(0)     
    
    df_result ['RSW'] = relative_strength.iloc[-1,:].values
   
    return df_result
    

    
if __name__ == "__main__":
#    symbols = get_csv_data(source = "cp68")
#    symbols = get_csv_data()
#    symbols = get_stocks_highcpm(download = False, source ="cp68")
    
#    symbols =  ['FTS', 'PVI', 'VNE']

#    analysis_trading(symbols, start = "2017-3-1" , end = "2018-4-11", update = False, source = "cp68")


    
#    VNI_result, VNI_data  = passive_strategy(start_date = "2017-3-26" , end_date = "2018-4-24", market= "^VNINDEX")
    

    ticker = 'DGW'    
#
    end_date = "2018-5-18"
    start_date = "2017-1-2"
#####    bollingerbands = bollinger_bands(ticker, start_date, end_date, realtime = False, source = "cp68")
####    
#    hedgefund = hedgefund_trading(ticker, start_date, end_date, realtime = False, source ="cp68")    
#    plot_hedgefund_trading(ticker, hedgefund)
#####    
#####    shortsell = short_selling(ticker, start_date, end_date, realtime = False, source ="ssi")    
#####    plot_shortselling_trading(ticker, shortsell)
#####    
#####
#####    
#    ninja = ninja_trading(ticker, start_date, end_date, realtime = False,  source ="cp68")    
#    plot_ninja_trading(ticker, ninja)
    
##    plot_trading_weekly(ticker, hedgefund)
##    
##    investment_stocks = ['CII', 'HPG', 'NBB', 'STB', 'PAN', 'VND' ]
##    
#    canslim = hung_canslim(ticker, start_date, end_date, realtime = False,  source ="cp68", market = "^HASTC") 
#    meanrevert = mean_reversion(ticker, start_date, end_date, realtime = False,  source ="cp68") 
###    plot_canslim_trading(ticker, canslim)

    RSWlist= ['NVB','VGS','PHC','ACB', 'HLD', 'MBS', 'TTB', 'NDN', 
              'HPG', 'CTG', 'GEX','VCI', 'CTG', 'GEX', 'DIG', 'MBB', 'DGW', 
              'BVH', 'VND', 'BID', 'HCM',
              'VJC', 'PAN', 'MSN', 'GAS', 'TCH', 'DXG', 'PNJ', 'IDI', 'VIC', 'ANV']
    analysis_trading(tickers = None, start = "2017-1-2" , end = "2018-5-23", update = False,  source ="cp68")
#    
#    
    
    
    symbolsVNI = getliststocks(typestock = "^VNINDEX")
    symbolsHNX = getliststocks(typestock = "^HASTC")
#    ALLOC_opt = rebalancing_porfolio(symbols = symbolsVNI, bench = '^VNINDEX')
#    stock_alloc, stock_data = passive_strategy(start_date = start_date, end_date = end_date, market = "^VNINDEX")
#    active_strategy(start_date = start_date, end_date = end_date, update = True, source = "cp68", market = "^VNINDEX")
#    dates = pd.date_range(start_date, end_date)  # date range as index
#    df_data = get_data(symbolsVNI, dates, benchmark = "^VNINDEX")  # get data for each symbol
#    fill_missing_values(df_data)
#    df_alphabeta = analysis_alpha_beta(df_data, symbols = symbolsVNI, market =  "^VNINDEX" )
#    port = portfolio_management()
    
#    get_statistic_index(days = 1, start = "2017-1-2" , end = "2018-5-14", update = True,  source ="cp68")
    
#    investing = ['NVB', 'MBS', 'FPT', 'TVN', 'VIX']
#    predict_stocks(investing, start ="2010-3-18", end = "2018-4-13")
   
#    ML_strategy('ACB', start ="2008-1-2", end = "2018-4-26")
#    tickers = pd.Series(symbols)
    