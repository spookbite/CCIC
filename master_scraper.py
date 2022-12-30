import news_scraper as ns
import index_scraper as ids


def main():
    ns.grow()
    ns.upstox_fo()
    ns.upstox_mo()
    ns.capital()
    ids.eqsis()
    ids.mc_cash()
    ids.mc_fno()
    ids.nse_india()
    ids.investing()
    ns.moneycontrol()

if __name__ == "__main__":
    main()
