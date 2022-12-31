import news_scraper as ns
import index_scraper as ids


def main():
    try:
        ns.grow()
    except:
        print("Groww failed")
    try:
        ns.upstox_fo()
    except:
        print("Upstox F&O Failed")
    try:
        ns.upstox_mo()
    except:
        print("Upstox morning failed")
    try:
        ns.capital()
    except:
        print("Capital Market failed")
    try:
        ids.eqsis()
    except:
        print("Eqsis failed")
    try:
        ids.mc_cash()
    except:
        print("moneycontrol cash failed")
    try:
        ids.mc_fno()
    except:
        print("moneycontrol F&O failed")
    try:
        ids.nse_india()
    except:
        print("Nse India failed")
    try:
        ids.investing()
    except:
        print("Investing.com failed")
    try:
        ns.moneycontrol()
    except:
        print("moneycontrol news failed")

if __name__ == "__main__":
    main()
