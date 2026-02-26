// Wall Street Research Cards - sourced via X #privatecredit
// Auto-injected after main script loads

var WS_CARDS = [
  {
    id: "ws001", ti: "Morgan Stanley: Private Credit 2026 Outlook",
    sr: "Morgan Stanley IM", ty: "article", dt: "2025-12-16",
    dm: "CreditMarkets", sg: "Monitor", ag: "A1",
    tg: ["#privatecredit", "#directlending", "#macrorates", "#xsource"],
    su: "Refi wave to overtake supply; DL yields trough 8-8.5%. Semi-liquid vehicles now ~1/3 of $1T US DL market.",
    url: "https://www.morganstanley.com/im/en-us/institutional-investor/insights/outlooks/private-credit-2026-outlook.html",
    xs: true
  },
  {
    id: "ws003", ti: "Blue Owl OBDC II: Redemption Gate Triggers Contagion",
    sr: "Bloomberg / Reuters", ty: "market_data", dt: "2026-02-18",
    dm: "CreditMarkets", sg: "Alert", ag: "A2",
    tg: ["#privatecredit", "#bdc", "#liquidityrisk", "#distresseddebt", "#xsource"],
    su: "Blue Owl halts quarterly redemptions OBDC II; $1.4B DL sold. Requests exceeded 5% cap. Contagion to APO/BX/KKR.",
    url: "https://www.reuters.com/business/blue-owl-sells-14-bln-debt-funds-pension-insurance-investors-2026-02-18/",
    xs: true
  },
  {
    id: "ws004", ti: "BlackRock: Private Credit to Double by Decade End",
    sr: "BlackRock", ty: "article", dt: "2025-10-06",
    dm: "CreditMarkets", sg: "Confirmed", ag: "A1",
    tg: ["#privatecredit", "#directlending", "#generalaccount", "#xsource"],
    su: "$41T revenue pool. 10% PC allocation improves 60/40 risk-return. Market share grew 3% to 10% since 2014.",
    url: "https://www.blackrock.com/corporate/insights/global-insights/todays-private-credit-opportunity",
    xs: true
  },
  {
    id: "ws005", ti: "JPMorgan AM: Private Credit Core to Portfolio Construction",
    sr: "JPMorgan Asset Management", ty: "article", dt: "2025-11-19",
    dm: "CreditMarkets", sg: "Confirmed", ag: "A3",
    tg: ["#privatecredit", "#directlending", "#macrorates", "#xsource"],
    su: "JPMAM: PC essential ballast for 60/40. Senior-secured DL yields ~200bps above LL, ~300bps above HY.",
    url: "https://am.jpmorgan.com/us/en/asset-management/adv/insights/portfolio-insights/alternatives/alternatives-outlook/",
    xs: true
  },
  {
    id: "ws006", ti: "Moody's: Private Credit AUM to Exceed $2T in 2026",
    sr: "Moody's Ratings", ty: "regulatory", dt: "2026-01-21",
    dm: "CreditMarkets", sg: "Monitor", ag: "A4",
    tg: ["#privatecredit", "#abf", "#liquidityrisk", "#xsource"],
    su: "AUM approaching $4T by 2030. ABF leading growth. Increasing complexity and liquidity risks as mix shifts.",
    url: "https://www.moodys.com/web/en/us/insights/credit-risk/outlooks/private-credit-2026.html",
    xs: true
  },
  {
    id: "ws007", ti: "Moody's/WSJ: US Insurers Park 50%+ FI in Private Credit",
    sr: "Moody's / WSJ", ty: "regulatory", dt: "2025-11-12",
    dm: "Regulatory", sg: "Alert", ag: "A4",
    tg: ["#privatecredit", "#lifeannuity", "#generalaccount", "#liquidityrisk", "#xsource"],
    su: "Some US life insurers park 50%+ FI in PC. Illiquid at $685B/18% of $3.8T fixed-income assets.",
    url: "https://www.wsj.com/finance/investing/u-s-insurers-are-binging-on-private-credit-moodys-says-ee10a41e",
    xs: true
  },
  {
    id: "ws008", ti: "NY Fed: Private Credit Market Nears $1.3 Trillion",
    sr: "NY Federal Reserve", ty: "regulatory", dt: "2025-11-03",
    dm: "Macro", sg: "Confirmed", ag: "A3",
    tg: ["#privatecredit", "#macrorates", "#directlending", "#xsource"],
    su: "Fed maps $1.3T PC market. Growth driven by structure, policy, and volatility displacement from banks.",
    url: "https://nyfed.org/4qleICc",
    xs: true
  }
];
// Inject cards into main C array and re-render
if (typeof C !== 'undefined') {
  WS_CARDS.forEach(function(card) { C.push(card); });
  if (typeof render === 'function') render();
}
