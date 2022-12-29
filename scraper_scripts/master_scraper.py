import news_scraper as ns
import index_scraper as ids


def main():
    ns.moneycontrol()
    ns.grow()
    ns.upstox_fo()
    ns.upstox_mo()
    ns.capital()
    ids.eqsis()
    ids.mc_cash()
    ids.mc_fno()

if __name__ == "__main__":
    main()
