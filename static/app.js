"use strict";


/* =========================================================
  Travel Life
  app.js
========================================================= */




/* =========================================================
  0. 国データ
========================================================= */


const rawCountries = [
  ["CA","カナダ","Canada","🇨🇦","CAD","カナダドル","Toronto",43.6532,-79.3832,"+1","911","911","911"],
  ["NZ","ニュージーランド","New Zealand","🇳🇿","NZD","ニュージーランドドル","Wellington",-41.2866,174.7756,"+64","111","111","111"],
  ["AU","オーストラリア","Australia","🇦🇺","AUD","オーストラリアドル","Sydney",-33.8688,151.2093,"+61","000","000","000"],
  ["JP","日本","Japan","🇯🇵","JPY","円","Tokyo",35.6762,139.6503,"+81","119","110","119"],
  ["US","アメリカ","United States","🇺🇸","USD","米ドル","New York",40.7128,-74.0060,"+1","911","911","911"],
  ["GB","イギリス","United Kingdom","🇬🇧","GBP","英ポンド","London",51.5072,-0.1276,"+44","999","999","999"],
  ["IE","アイルランド","Ireland","🇮🇪","EUR","ユーロ","Dublin",53.3498,-6.2603,"+353","112","112","112"],
  ["FR","フランス","France","🇫🇷","EUR","ユーロ","Paris",48.8566,2.3522,"+33","112","112","112"],
  ["DE","ドイツ","Germany","🇩🇪","EUR","ユーロ","Berlin",52.5200,13.4050,"+49","112","110","112"],
  ["IT","イタリア","Italy","🇮🇹","EUR","ユーロ","Rome",41.9028,12.4964,"+39","112","112","112"],
  ["ES","スペイン","Spain","🇪🇸","EUR","ユーロ","Madrid",40.4168,-3.7038,"+34","112","112","112"],
  ["PT","ポルトガル","Portugal","🇵🇹","EUR","ユーロ","Lisbon",38.7223,-9.1393,"+351","112","112","112"],
  ["NL","オランダ","Netherlands","🇳🇱","EUR","ユーロ","Amsterdam",52.3676,4.9041,"+31","112","112","112"],
  ["BE","ベルギー","Belgium","🇧🇪","EUR","ユーロ","Brussels",50.8503,4.3517,"+32","112","112","112"],
  ["CH","スイス","Switzerland","🇨🇭","CHF","スイスフラン","Zurich",47.3769,8.5417,"+41","144","117","118"],
  ["AT","オーストリア","Austria","🇦🇹","EUR","ユーロ","Vienna",48.2082,16.3738,"+43","144","133","122"],
  ["SE","スウェーデン","Sweden","🇸🇪","SEK","スウェーデンクローナ","Stockholm",59.3293,18.0686,"+46","112","112","112"],
  ["NO","ノルウェー","Norway","🇳🇴","NOK","ノルウェークローネ","Oslo",59.9139,10.7522,"+47","113","112","110"],
  ["DK","デンマーク","Denmark","🇩🇰","DKK","デンマーククローネ","Copenhagen",55.6761,12.5683,"+45","112","112","112"],
  ["FI","フィンランド","Finland","🇫🇮","EUR","ユーロ","Helsinki",60.1699,24.9384,"+358","112","112","112"],
  ["IS","アイスランド","Iceland","🇮🇸","ISK","アイスランドクローナ","Reykjavik",64.1466,-21.9426,"+354","112","112","112"],
  ["PL","ポーランド","Poland","🇵🇱","PLN","ズウォティ","Warsaw",52.2297,21.0122,"+48","112","112","112"],
  ["CZ","チェコ","Czech Republic","🇨🇿","CZK","チェココルナ","Prague",50.0755,14.4378,"+420","112","112","112"],
  ["HU","ハンガリー","Hungary","🇭🇺","HUF","フォリント","Budapest",47.4979,19.0402,"+36","112","112","112"],
  ["GR","ギリシャ","Greece","🇬🇷","EUR","ユーロ","Athens",37.9838,23.7275,"+30","112","112","112"],
  ["HR","クロアチア","Croatia","🇭🇷","EUR","ユーロ","Zagreb",45.8150,15.9819,"+385","112","112","112"],
  ["EE","エストニア","Estonia","🇪🇪","EUR","ユーロ","Tallinn",59.4370,24.7536,"+372","112","112","112"],
  ["LV","ラトビア","Latvia","🇱🇻","EUR","ユーロ","Riga",56.9496,24.1052,"+371","112","112","112"],
  ["LT","リトアニア","Lithuania","🇱🇹","EUR","ユーロ","Vilnius",54.6872,25.2797,"+370","112","112","112"],
  ["SG","シンガポール","Singapore","🇸🇬","SGD","シンガポールドル","Singapore",1.3521,103.8198,"+65","995","999","995"],
  ["MY","マレーシア","Malaysia","🇲🇾","MYR","マレーシアリンギット","Kuala Lumpur",3.1390,101.6869,"+60","999","999","999"],
  ["TH","タイ","Thailand","🇹🇭","THB","タイバーツ","Bangkok",13.7563,100.5018,"+66","1669","191","199"],
  ["VN","ベトナム","Vietnam","🇻🇳","VND","ベトナムドン","Ho Chi Minh City",10.8231,106.6297,"+84","115","113","114"],
  ["PH","フィリピン","Philippines","🇵🇭","PHP","フィリピンペソ","Manila",14.5995,120.9842,"+63","911","911","911"],
  ["ID","インドネシア","Indonesia","🇮🇩","IDR","インドネシアルピア","Jakarta",-6.2088,106.8456,"+62","119","110","113"],
  ["KR","韓国","South Korea","🇰🇷","KRW","韓国ウォン","Seoul",37.5665,126.9780,"+82","119","112","119"],
  ["TW","台湾","Taiwan","🇹🇼","TWD","台湾ドル","Taipei",25.0330,121.5654,"+886","119","110","119"],
  ["HK","香港","Hong Kong","🇭🇰","HKD","香港ドル","Hong Kong",22.3193,114.1694,"+852","999","999","999"],
  ["IN","インド","India","🇮🇳","INR","インドルピー","New Delhi",28.6139,77.2090,"+91","112","112","112"],
  ["AE","UAE","United Arab Emirates","🇦🇪","AED","UAEディルハム","Dubai",25.2048,55.2708,"+971","998","999","997"],
  ["QA","カタール","Qatar","🇶🇦","QAR","カタールリヤル","Doha",25.2854,51.5310,"+974","999","999","999"],
  ["SA","サウジアラビア","Saudi Arabia","🇸🇦","SAR","サウジリヤル","Riyadh",24.7136,46.6753,"+966","997","999","998"],
  ["TR","トルコ","Turkey","🇹🇷","TRY","トルコリラ","Istanbul",41.0082,28.9784,"+90","112","112","112"],
  ["MX","メキシコ","Mexico","🇲🇽","MXN","メキシコペソ","Mexico City",19.4326,-99.1332,"+52","911","911","911"],
  ["BR","ブラジル","Brazil","🇧🇷","BRL","ブラジルレアル","São Paulo",-23.5505,-46.6333,"+55","192","190","193"],
  ["AR","アルゼンチン","Argentina","🇦🇷","ARS","アルゼンチンペソ","Buenos Aires",-34.6037,-58.3816,"+54","107","911","100"],
  ["CL","チリ","Chile","🇨🇱","CLP","チリペソ","Santiago",-33.4489,-70.6693,"+56","131","133","132"],
  ["ZA","南アフリカ","South Africa","🇿🇦","ZAR","南アフリカランド","Cape Town",-33.9249,18.4241,"+27","112","10111","112"],
  ["MT","マルタ","Malta","🇲🇹","EUR","ユーロ","Valletta",35.8989,14.5146,"+356","112","112","112"],
  ["CY","キプロス","Cyprus","🇨🇾","EUR","ユーロ","Nicosia",35.1856,33.3823,"+357","112","112","112"],
  ["IL","イスラエル","Israel","🇮🇱","ILS","イスラエル新シェケル","Tel Aviv",32.0853,34.7818,"+972","101","100","102"]
];




const countries = rawCountries.map(row => ({
  code: row[0],
  name: row[1],
  searchName: row[2],
  flag: row[3],
  currency: row[4],
  currencyName: row[5],
  city: row[6],
  lat: row[7],
  lon: row[8],
  callingCode: row[9],
  ambulance: row[10],
  police: row[11],
  fire: row[12]
}));




/* =========================================================
  1. 共通
========================================================= */


const $ = id => document.getElementById(id);


const MINUTE = 60 * 1000;


const HOUR = 60 * MINUTE;


const DAY = 24 * HOUR;




function setText(
  id,
  value
) {


  const element = $(
    id
  );


  if (!element) {
    return;
  }


  element.textContent =
    value === null ||
    value === undefined
      ? "--"
      : String(
        value
      );
}




function numberValue(
  value
) {


  const number = Number(
    value
  );


  if (!Number.isFinite(
    number
  )) {


    return null;
  }


  return number;
}




function formatNumber(
  value,
  digits = 0
) {


  const number = numberValue(
    value
  );


  if (number === null) {
    return "--";
  }


  return number.toLocaleString(
    "ja-JP",
    {
      maximumFractionDigits:
        digits
    }
  );
}




function formatCoins(
  value
) {


  const number = numberValue(
    value
  );


  if (number === null) {
    return "--";
  }


  return (
    Math.round(
      number
    ).toLocaleString(
      "ja-JP"
    )
    +
    " coin"
  );
}




function formatDistance(
  meters
) {


  const value = numberValue(
    meters
  );


  if (value === null) {
    return "--";
  }


  if (value >= 1000) {


    return (
      (
        value
        /
        1000
      ).toFixed(
        2
      )
      +
      " km"
    );
  }


  return (
    Math.round(
      value
    )
    +
    " m"
  );
}




function formatDuration(
  seconds
) {


  const value = numberValue(
    seconds
  );


  if (value === null) {
    return "--";
  }


  const minutes =
    Math.max(
      0,
      Math.round(
        value
        /
        60
      )
    );


  if (minutes < 60) {


    return (
      minutes
      +
      "分"
    );
  }


  const hours =
    Math.floor(
      minutes
      /
      60
    );


  const remaining =
    minutes
    %
    60;


  return (
    hours
    +
    "時間"
    +
    remaining
    +
    "分"
  );
}




function formatDate(
  unixTime
) {


  const number = numberValue(
    unixTime
  );


  if (number === null) {
    return "--";
  }


  return new Date(
    number
    *
    1000
  ).toLocaleString(
    "ja-JP"
  );
}




function escapeText(
  value
) {


  return String(
    value ?? ""
  );
}




function createElement(
  tag,
  className = "",
  text = ""
) {


  const element =
    document.createElement(
      tag
    );


  if (className) {


    element.className =
      className;
  }


  if (
    text !== null &&
    text !== undefined &&
    text !== ""
  ) {


    element.textContent =
      String(
        text
      );
  }


  return element;
}




function createButton(
  text,
  click,
  className = "route-button"
) {


  const element =
    createElement(
      "button",
      className,
      text
    );


  element.type =
    "button";


  element.addEventListener(
    "click",
    click
  );


  return element;
}




function showStatus(
  id,
  message,
  isError = false
) {


  const element = $(
    id
  );


  if (!element) {
    return;
  }


  element.textContent =
    message || "";


  element.classList.toggle(
    "error",
    Boolean(
      isError
    )
  );
}




async function requestJSON(
  url,
  options = {},
  timeout = 20000
) {


  const controller =
    new AbortController();


  const timer =
    setTimeout(
      () => {
        controller.abort();
      },
      timeout
    );


  try {


    const response =
      await fetch(
        url,
        {
          ...options,


          signal:
            controller.signal,


          credentials:
            "same-origin",


          cache:
            "no-store"
        }
      );


    let data = {};


    try {


      data =
        await response.json();


    } catch {


      throw new Error(
        "サーバーから正しいデータが返されませんでした"
      );
    }


    if (
      !response.ok ||
      data?.error
    ) {


      throw new Error(
        data?.error
        ||
        `通信エラー ${response.status}`
      );
    }


    return data;


  } catch (
    error
  ) {


    if (
      error.name
      ===
      "AbortError"
    ) {


      throw new Error(
        "通信がタイムアウトしました"
      );
    }


    throw error;


  } finally {


    clearTimeout(
      timer
    );
  }
}




function getCurrentPosition() {


  return new Promise(
    (
      resolve,
      reject
    ) => {


      if (
        !navigator.geolocation
      ) {


        reject(
          new Error(
            "この端末では位置情報を利用できません"
          )
        );


        return;
      }


      navigator.geolocation.getCurrentPosition(
        resolve,


        () => {


          reject(
            new Error(
              "位置情報を取得できませんでした"
            )
          );
        },


        {
          enableHighAccuracy:
            true,


          timeout:
            15000,


          maximumAge:
            10000
        }
      );
    }
  );
}




function normalizeSearch(
  value
) {


  return String(
    value ?? ""
  )
    .normalize(
      "NFKC"
    )
    .toLowerCase()
    .trim();
}




/* =========================================================
  2. 状態
========================================================= */


let currentCountry =
  countries.find(
    country =>
      country.code
      ===
      "NZ"
  )
  ||
  countries[0];




let currentPeriod =
  "1m";




let latestRate =
  null;




let currencyChart =
  null;




let dangerMap =
  null;




let radarMap =
  null;




let historyMap =
  null;




let historyRouteLayer =
  null;




let conquestMap =
  null;


let conquestMoveTimer =
  null;


let conquestLayers =
  [];




let selectedLand =
  null;




let currentGamePlayer =
  null;




let currentGamePosition =
  null;




let currentTrip =
  null;




let tripWatchId =
  null;




let routeOrigin =
  null;




let routeDestination =
  null;




const selectedCities =
  new Map();




/* =========================================================
  3. LocalStorage
========================================================= */


function loadLocalSettings() {


  try {


    const saved =
      JSON.parse(
        localStorage.getItem(
          "travel-life-settings"
        )
        ||
        "{}"
      );


    if (
      saved.country
    ) {


      const found =
        countries.find(
          country =>
            country.code
            ===
            saved.country
        );


      if (found) {


        currentCountry =
          found;
      }
    }


    if (
      Array.isArray(
        saved.cities
      )
    ) {


      for (
        const [
          code,
          city
        ]
        of
        saved.cities
      ) {


        selectedCities.set(
          code,
          city
        );
      }
    }


  } catch (
    error
  ) {


    console.warn(
      "SETTINGS LOAD ERROR:",
      error
    );
  }
}




function saveLocalSettings() {


  try {


    localStorage.setItem(
      "travel-life-settings",


      JSON.stringify({
        country:
          currentCountry.code,


        cities:
          [
            ...selectedCities
          ]
      })
    );


  } catch (
    error
  ) {


    console.warn(
      "SETTINGS SAVE ERROR:",
      error
    );
  }
}




/* =========================================================
  4. 画面切り替え
========================================================= */


function openScreen(
  screenId
) {


  document
    .querySelectorAll(
      ".screen"
    )
    .forEach(
      screen => {


        screen.classList.toggle(
          "active",
          screen.id
          ===
          screenId
        );
      }
    );




  document
    .querySelectorAll(
      ".nav-button"
    )
    .forEach(
      button => {


        button.classList.toggle(
          "active",


          button.dataset.screen
          ===
          screenId
        );
      }
    );




  window.scrollTo(
    0,
    0
  );




  if (
    screenId
    ===
    "currency-screen"
  ) {


    loadRates();
  }




  if (
    screenId
    ===
    "news-screen"
  ) {


    loadNews();
  }




  if (
    screenId
    ===
    "danger-screen"
  ) {


    loadDanger();
  }




  if (
    screenId
    ===
    "life-screen"
  ) {


    loadWeather();
  }




  if (
    screenId
    ===
    "history-screen"
  ) {


    loadTrips();
  }




  if (
    screenId
    ===
    "conquest-screen"
  ) {


    loadGame();
  }




  setTimeout(
    () => {


      dangerMap?.invalidateSize();


      radarMap?.invalidateSize();


      historyMap?.invalidateSize();


      conquestMap?.invalidateSize();
    },
    100
  );
}




function setupNavigation() {


  document
    .querySelectorAll(
      ".nav-button"
    )
    .forEach(
      button => {


        button.addEventListener(
          "click",
          () => {


            openScreen(
              button.dataset.screen
            );
          }
        );
      }
    );
}




/* =========================================================
  5. 国カード
========================================================= */


function renderCountryCards() {


  const area = $(
    "country-scroll"
  );


  if (!area) {
    return;
  }


  area.replaceChildren();




  for (
    const country
    of
    countries
  ) {


    const button =
      createButton(
        "",
        () => {


          changeCountry(
            country
          );
        },
        "country-card"
      );




    if (
      country.code
      ===
      currentCountry.code
    ) {


      button.classList.add(
        "active"
      );
    }




    const flag =
      createElement(
        "span",
        "country-flag",
        country.flag
      );




    const name =
      createElement(
        "span",
        "country-name",
        country.name
      );




    button.append(
      flag,
      name
    );




    area.append(
      button
    );
  }
}




function updateCountryDisplay() {
  renderCountryCards();

  setText(
    "news-flag",
    currentCountry.flag
  );
  setText(
    "news-country",
    currentCountry.name
  );

  setText(
    "danger-flag",
    currentCountry.flag
  );
  setText(
    "danger-country",
    currentCountry.name
  );

  setText(
    "life-flag",
    currentCountry.flag
  );
  setText(
    "life-country",
    currentCountry.name
  );

  const city =
    selectedCities.get(
      currentCountry.code
    );

  setText(
    "weather-city",
    city?.name
    ||
    currentCountry.city
  );

  setText(
    "calling-code",
    currentCountry.callingCode
  );
  setText(
    "ambulance",
    currentCountry.ambulance
  );
  setText(
    "police",
    currentCountry.police
  );
  setText(
    "fire",
    currentCountry.fire
  );

  const emergencyLinks = [
    [
      "ambulance-link",
      currentCountry.ambulance
    ],
    [
      "police-link",
      currentCountry.police
    ],
    [
      "fire-link",
      currentCountry.fire
    ]
  ];

  for (
    const [
      id,
      number
    ]
    of emergencyLinks
  ) {
    const link = $(
      id
    );

    if (link) {
      link.href =
        `tel:${String(
          number || ""
        ).replace(
          /[^0-9+]/g,
          ""
        )}`;
    }
  }

  document
    .querySelectorAll(
      ".country-search"
    )
    .forEach(
      input => {
        input.value =
          "";
      }
    );

  document
    .querySelectorAll(
      ".country-results"
    )
    .forEach(
      area => {
        area.hidden =
          true;
        area.replaceChildren();
      }
    );

  if (
    $("city-search")
  ) {
    $("city-search").value =
      "";
  }

  if (
    $("city-results")
  ) {
    $("city-results").hidden =
      true;
  }

  showStatus(
    "city-hint",
    `${currentCountry.name}の街を検索します。`
  );
}





function changeCountry(
  country
) {


  currentCountry =
    country;


  latestRate =
    null;




  routeOrigin =
    null;


  routeDestination =
    null;




  saveLocalSettings();


  updateCountryDisplay();




  const active =
    document.querySelector(
      ".screen.active"
    );




  if (!active) {
    return;
  }




  if (
    active.id
    ===
    "currency-screen"
  ) {


    loadRates();
  }




  if (
    active.id
    ===
    "news-screen"
  ) {


    loadNews();
  }




  if (
    active.id
    ===
    "danger-screen"
  ) {


    loadDanger();
  }




  if (
    active.id
    ===
    "life-screen"
  ) {


    loadWeather();
  }
}




/* =========================================================
  6. 国検索
========================================================= */


function setupCountrySearch() {


  document
    .querySelectorAll(
      ".country-search"
    )
    .forEach(
      input => {


        const box =
          input.closest(
            ".country-search-box"
          );




        const results =
          box?.querySelector(
            ".country-results"
          );




        if (!results) {
          return;
        }




        input.addEventListener(
          "input",
          () => {


            const query =
              normalizeSearch(
                input.value
              );




            results.replaceChildren();




            if (!query) {


              results.hidden =
                true;


              return;
            }




            const found =
              countries.filter(
                country => {


                  const text =
                    normalizeSearch(
                      [
                        country.name,
                        country.searchName,
                        country.code
                      ].join(
                        " "
                      )
                    );




                  return text.includes(
                    query
                  );
                }
              );




            if (!found.length) {


              results.hidden =
                false;


              results.append(
                createElement(
                  "p",
                  "",
                  "国が見つかりません"
                )
              );


              return;
            }




            for (
              const country
              of
              found
            ) {


              const button =
                createButton(
                  `${country.flag} ${country.name}`,


                  () => {


                    input.value =
                      "";


                    results.hidden =
                      true;


                    changeCountry(
                      country
                    );
                  },
                  ""
                );




              results.append(
                button
              );
            }




            results.hidden =
              false;
          }
        );
      }
    );
}




/* =========================================================
  7. 為替
========================================================= */


async function loadRates() {


  setText(
    "rate-number",
    "--"
  );


  setText(
    "rate-date",
    "取得中..."
  );


  setText(
    "rate-label",
    `1${currentCountry.currencyName} は`
  );


  setText(
    "converter-currency",
    currentCountry.currency
  );




  try {


    const data =
      await requestJSON(
        `/api/rates/${encodeURIComponent(
          currentCountry.currency
        )}?period=${encodeURIComponent(
          currentPeriod
        )}`
      );




    latestRate =
      numberValue(
        data.latest_rate
      );




    setText(
      "rate-number",


      latestRate === null
        ?
        "--"
        :
        formatNumber(
          latestRate,
          4
        )
    );




    setText(
      "rate-date",
      data.latest_date
      ||
      "--"
    );




    renderRateChart(
      data.data
      ||
      []
    );




    updateConverter();


  } catch (
    error
  ) {


    latestRate =
      null;


    setText(
      "rate-date",
      error.message
    );




    updateConverter();
  }
}




function renderRateChart(
  rows
) {


  if (
    !Array.isArray(
      rows
    )
    ||
    !rows.length
  ) {


    return;
  }




  const canvas = $(
    "currency-chart"
  );




  if (
    !canvas
    ||
    typeof Chart
    ===
    "undefined"
  ) {


    return;
  }




  currencyChart?.destroy();




  setText(
    "chart-date",
    rows.at(-1)?.date
    ||
    "--"
  );




  setText(
    "chart-value",
    `${
      formatNumber(
        rows.at(-1)?.rate,
        4
      )
    } 円`
  );




  currencyChart =
    new Chart(
      canvas,
      {
        type:
          "line",


        data: {


          labels:
            rows.map(
              row =>
                row.date
            ),


          datasets: [
            {
              data:
                rows.map(
                  row =>
                    row.rate
                ),


              borderColor:
                "#66d69e",


              backgroundColor:
                "rgba(102,214,158,.12)",


              fill:
                true,


              pointRadius:
                0,


              pointHoverRadius:
                4,


              tension:
                0.15,


              borderWidth:
                2
            }
          ]
        },


        options: {


          responsive:
            true,


          maintainAspectRatio:
            false,


          animation:
            false,


          interaction: {
            mode:
              "index",


            intersect:
              false
          },


          plugins: {


            legend: {
              display:
                false
            },


            tooltip: {


              callbacks: {


                label:
                  context =>
                    `${formatNumber(
                      context.parsed.y,
                      4
                    )} 円`
              }
            }
          },


          scales: {


            x: {
              display:
                false
            },


            y: {


              ticks: {
                color:
                  "#9ba8b8"
              },


              grid: {
                color:
                  "rgba(255,255,255,.08)"
              }
            }
          },


          onHover:
            (
              event,
              elements
            ) => {


              if (
                !elements.length
              ) {


                return;
              }




              const row =
                rows[
                  elements[0].index
                ];




              setText(
                "chart-date",
                row.date
              );




              setText(
                "chart-value",
                `${formatNumber(
                  row.rate,
                  4
                )} 円`
              );
            }
        }
      }
    );
}




function updateConverter() {


  const input = $(
    "converter-input"
  );




  if (!input) {
    return;
  }




  const amount =
    numberValue(
      input.value
    );




  if (
    amount === null
    ||
    latestRate === null
  ) {


    setText(
      "converter-result",
      "--"
    );


    return;
  }




  setText(
    "converter-result",


    formatNumber(
      amount
      *
      latestRate,
      2
    )
  );
}
function setupCurrency() {


  document
    .querySelectorAll(
      ".period-row button"
    )
    .forEach(
      button => {


        button.addEventListener(
          "click",
          () => {


            currentPeriod =
              button.dataset.period
              ||
              "1m";




            document
              .querySelectorAll(
                ".period-row button"
              )
              .forEach(
                item => {


                  item.classList.toggle(
                    "active",
                    item
                    ===
                    button
                  );
                }
              );




            loadRates();
          }
        );
      }
    );




  $("converter-input")
    ?.addEventListener(
      "input",
      updateConverter
    );
}




/* =========================================================
  8. ニュース
========================================================= */


async function loadNews() {


  const area = $(
    "news-list"
  );




  if (!area) {
    return;
  }




  area.replaceChildren(
    createElement(
      "div",
      "loading",
      "ニュースを取得しています..."
    )
  );




  showStatus(
    "news-status",
    "取得中..."
  );




  try {


    const data =
      await requestJSON(
        `/api/news?country=${encodeURIComponent(
          currentCountry.searchName
        )}`,
        {},
        45000
      );




    area.replaceChildren();




    if (
      !Array.isArray(
        data
      )
      ||
      !data.length
    ) {


      area.append(
        createElement(
          "div",
          "empty-state",
          "ニュースが見つかりませんでした"
        )
      );


      showStatus(
        "news-status",
        ""
      );


      return;
    }




    for (
      const article
      of
      data
    ) {


      let url;


      try {


        url =
          new URL(
            article.url
          );


      } catch {


        continue;
      }




      if (
        ![
          "http:",
          "https:"
        ].includes(
          url.protocol
        )
      ) {


        continue;
      }




      const card =
        createElement(
          "a",
          "news-card"
        );




      card.href =
        url.href;


      card.target =
        "_blank";


      card.rel =
        "noopener noreferrer";




      card.append(
        createElement(
          "div",
          "news-source",
          article.domain
          ||
          url.hostname
        ),


        createElement(
          "div",
          "news-title",
          article.title
          ||
          "記事"
        ),


        createElement(
          "div",
          "news-arrow",
          "→"
        )
      );




      area.append(
        card
      );
    }




    showStatus(
      "news-status",
      ""
    );


  } catch (
    error
  ) {


    area.replaceChildren(
      createElement(
        "div",
        "empty-state",
        "ニュースを取得できませんでした"
      )
    );




    showStatus(
      "news-status",
      error.message,
      true
    );
  }
}




/* =========================================================
  9. Leaflet 共通
========================================================= */


function createLeafletMap(
  id,
  center,
  zoom
) {


  if (
    typeof L
    ===
    "undefined"
  ) {


    throw new Error(
      "地図ライブラリを読み込めませんでした"
    );
  }




  const map =
    L.map(
      id,
      {
        zoomControl:
          true
      }
    ).setView(
      center,
      zoom
    );




  L.tileLayer(
    "https://tile.openstreetmap.org/{z}/{x}/{y}.png",
    {
      maxZoom:
        19,


      attribution:
        '&copy; OpenStreetMap contributors'
    }
  ).addTo(
    map
  );




  return map;
}




/* =========================================================
  10. 安全
========================================================= */


async function loadDanger() {


 try {


  if (!dangerMap) {


   dangerMap =
    createLeafletMap(
     "danger-map",
     [
      currentCountry.lat,
      currentCountry.lon
     ],
     5
    );


  } else {


   dangerMap.eachLayer(
    layer => {


     if (
      layer instanceof L.Marker
      ||
      layer instanceof L.CircleMarker
     ) {
      dangerMap.removeLayer(
       layer
      );
     }
    }
   );


   dangerMap.setView(
    [
     currentCountry.lat,
     currentCountry.lon
    ],
    5
   );
  }




  dangerMap.invalidateSize();




  const data =
   await requestJSON(
    `/api/danger?country=${encodeURIComponent(
     currentCountry.code
    )}`
   );




  const events =
   Array.isArray(
    data.events
   )
    ?
    data.events
    :
    [];




  if (
   events.length === 0
  ) {


   L.popup()
    .setLatLng(
     [
      currentCountry.lat,
      currentCountry.lon
     ]
    )
    .setContent(
     `${escapeText(
      currentCountry.name
     )}<br>現在取得できるGDACS災害情報はありません`
    )
    .openOn(
     dangerMap
    );


   return;
  }




  const bounds = [];




  for (
   const event of events
  ) {


   const latitude =
    Number(
     event.latitude
    );


   const longitude =
    Number(
     event.longitude
    );




   if (
    !Number.isFinite(
     latitude
    )
    ||
    !Number.isFinite(
     longitude
    )
   ) {
    continue;
   }




   const alertLevel =
    String(
     event.alert_level
     ||
     "Green"
    );




   let color =
    "#65d99a";




   if (
    alertLevel
    ===
    "Red"
   ) {


    color =
     "#ff4d62";


   } else if (
    alertLevel
    ===
    "Orange"
   ) {


    color =
     "#ff8d42";


   } else if (
    alertLevel
    ===
    "Green"
   ) {


    color =
     "#65d99a";
   }




   const eventName =
    event.name
    ||
    event.type
    ||
    "災害情報";




   const marker =
    L.circleMarker(
     [
      latitude,
      longitude
     ],
     {
      radius:
       9,


      color:
       color,


      fillColor:
       color,


      fillOpacity:
       0.72,


      weight:
       2
     }
    );




   marker.bindPopup(
    [
     `<strong>${escapeText(
      eventName
     )}</strong>`,


     `警戒レベル: ${escapeText(
      alertLevel
     )}`,


     event.type
      ?
      `種類: ${escapeText(
       event.type
      )}`
      :
      "",


     event.from_date
      ?
      `開始: ${escapeText(
       event.from_date
      )}`
      :
      ""
    ]
     .filter(
      Boolean
     )
     .join(
      "<br>"
     )
   );




   marker.addTo(
    dangerMap
   );




   bounds.push(
    [
     latitude,
     longitude
    ]
   );
  }




  if (
   bounds.length > 1
  ) {


   dangerMap.fitBounds(
    bounds,
    {
     padding:
      [
       30,
       30
      ],


     maxZoom:
      7
    }
   );


  } else if (
   bounds.length === 1
  ) {


   dangerMap.setView(
    bounds[0],
    6
   );
  }




 } catch (
  error
 ) {


  console.error(
   "DANGER ERROR:",
   error
  );




  if (
   dangerMap
  ) {


   L.popup()
    .setLatLng(
     [
      currentCountry.lat,
      currentCountry.lon
     ]
    )
    .setContent(
     "災害情報を取得できませんでした"
    )
    .openOn(
     dangerMap
    );
  }
 }
}








/* =========================================================
  11. 街検索
========================================================= */


let citySearchTimer =
  null;




function setupCitySearch() {


  const input = $(
    "city-search"
  );




  const area = $(
    "city-results"
  );




  if (
    !input
    ||
    !area
  ) {


    return;
  }




  input.addEventListener(
    "input",
    () => {


      clearTimeout(
        citySearchTimer
      );




      const query =
        input.value.trim();




      if (
        query.length
        <
        2
      ) {


        area.hidden =
          true;


        area.replaceChildren();


        return;
      }




      citySearchTimer =
        setTimeout(
          () => {


            searchCities(
              query
            );
          },
          500
        );
    }
  );
}




async function searchCities(
  query
) {


  const area = $(
    "city-results"
  );




  if (!area) {
    return;
  }




  area.hidden =
    false;




  area.replaceChildren(
    createElement(
      "p",
      "",
      "検索中..."
    )
  );




  try {


    const data =
      await requestJSON(
        `/api/cities?country=${encodeURIComponent(
          currentCountry.code
        )}&q=${encodeURIComponent(
          query
        )}`
      );




    area.replaceChildren();




    const rows =
      Array.isArray(
        data.results
      )
        ?
        data.results
        :
        [];




    if (!rows.length) {


      area.append(
        createElement(
          "p",
          "",
          "候補がありません"
        )
      );


      return;
    }




    for (
      const city
      of
      rows
    ) {


      const button =
        createButton(
          "",
          () => {


            selectedCities.set(
              currentCountry.code,
              city
            );




            saveLocalSettings();




            $("city-search").value =
              city.name;




            area.hidden =
              true;




            setText(
              "weather-city",
              city.name
            );




            loadWeather();
          },
          ""
        );




      button.append(
        createElement(
          "strong",
          "",
          city.name
        ),


        createElement(
          "small",
          "",
          city.detail
          ||
          city.admin1
          ||
          ""
        )
      );




      area.append(
        button
      );
    }


  } catch (
    error
  ) {


    area.replaceChildren(
      createElement(
        "p",
        "",
        error.message
      )
    );
  }
}




/* =========================================================
  12. 天気
========================================================= */


function weatherIcon(
  code
) {


  const value =
    Number(
      code
    );




  if (
    value === 0
  ) {


    return "☀️";
  }




  if (
    value <= 2
  ) {


    return "🌤️";
  }




  if (
    value === 3
  ) {


    return "☁️";
  }




  if (
    value <= 48
  ) {


    return "🌫️";
  }




  if (
    value <= 67
  ) {


    return "🌧️";
  }




  if (
    value <= 77
  ) {


    return "🌨️";
  }




  if (
    value <= 82
  ) {


    return "🌧️";
  }




  if (
    value <= 86
  ) {


    return "🌨️";
  }




  if (
    value >= 95
  ) {


    return "⛈️";
  }




  return "☁️";
}




function getWeatherPoint() {


  const saved =
    selectedCities.get(
      currentCountry.code
    );




  if (saved) {


    return {
      name:
        saved.name,


      latitude:
        Number(
          saved.latitude
        ),


      longitude:
        Number(
          saved.longitude
        )
    };
  }




  return {
    name:
      currentCountry.city,


    latitude:
      currentCountry.lat,


    longitude:
      currentCountry.lon
  };
}




async function loadWeather() {


  const point =
    getWeatherPoint();




  setText(
    "weather-city",
    point.name
  );




  showStatus(
    "weather-status",
    "天気を取得しています..."
  );




  try {


    const data =
      await requestJSON(
        `/api/weather?lat=${encodeURIComponent(
          point.latitude
        )}&lon=${encodeURIComponent(
          point.longitude
        )}`
      );




    renderWeather(
      data
    );




    renderRadar(
      point
    );




    showStatus(
      "weather-status",
      ""
    );


  } catch (
    error
  ) {


    showStatus(
      "weather-status",
      error.message,
      true
    );
  }
}




function renderWeather(
  data
) {
  const current =
    data.current
    ||
    {};

  const hourly =
    data.hourly
    ||
    {};

  const daily =
    data.daily
    ||
    {};

  setText(
    "weather-description",
    current.description
    ||
    "--"
  );

  setText(
    "weather-temperature",
    formatNumber(
      current.temperature_2m,
      0
    )
  );

  setText(
    "weather-feels",
    `${formatNumber(
      current.apparent_temperature,
      0
    )}°C`
  );

  setText(
    "weather-rain",
    `${formatNumber(
      current.precipitation,
      1
    )} mm`
  );

  setText(
    "weather-wind",
    `${formatNumber(
      current.wind_speed_10m,
      0
    )} km/h`
  );

  setText(
    "weather-icon",
    weatherIcon(
      current.weather_code
    )
  );

  const precipitation =
    numberValue(
      current.precipitation
    )
    ||
    0;

  const rain =
    numberValue(
      current.rain
    )
    ||
    0;

  const code =
    Number(
      current.weather_code
    );

  const rainy =
    precipitation > 0.05
    ||
    rain > 0.05
    ||
    (
      Number.isFinite(code)
      &&
      (
        (
          code >= 51
          &&
          code <= 67
        )
        ||
        (
          code >= 80
          &&
          code <= 82
        )
        ||
        (
          code >= 95
          &&
          code <= 99
        )
      )
    );

  setText(
    "advice-icon",
    rainy
      ? "☔"
      : "☀️"
  );

  setText(
    "advice-title",
    rainy
      ? "傘を持っていくのがおすすめ"
      : "大きな雨の可能性は低め"
  );

  setText(
    "advice-text",
    rainy
      ? `現在の降水量は${formatNumber(
          Math.max(
            precipitation,
            rain
          ),
          1
        )} mmです。`
      : "現在の予報では目立った降水は確認されていません。"
  );

  const uvValue =
    numberValue(
      daily
        .uv_index_max
        ?.[0]
    );

  setText(
    "uv-index",
    uvValue === null
      ? "--"
      : formatNumber(
          uvValue,
          1
        )
  );

  let uvAdvice =
    "UV情報を取得できませんでした。";

  if (
    uvValue !== null
  ) {
    if (
      uvValue < 3
    ) {
      uvAdvice =
        "UVは低めです。長時間の屋外活動では通常の紫外線対策をしてください。";
    } else if (
      uvValue < 6
    ) {
      uvAdvice =
        "UVは中程度です。日焼け止めや帽子の使用がおすすめです。";
    } else if (
      uvValue < 8
    ) {
      uvAdvice =
        "UVは強めです。日焼け止め・帽子・日陰を活用してください。";
    } else {
      uvAdvice =
        "UVは非常に強い水準です。できるだけ直射日光を避けてください。";
    }
  }

  setText(
    "uv-advice",
    uvAdvice
  );

  setText(
    "uv-time",
    Array.isArray(
      daily.time
    )
    &&
    daily.time[0]
      ? `対象日: ${daily.time[0]}`
      : ""
  );

  renderHourlyWeather(
    hourly
  );

  renderWeeklyWeather(
    daily
  );
}





function renderHourlyWeather(
  hourly
) {


  const area = $(
    "hourly-forecast"
  );




  if (!area) {
    return;
  }




  area.replaceChildren();




  const times =
    hourly.time
    ||
    [];




  const now =
    Date.now();




  let startIndex =
    times.findIndex(
      value => {


        const parsed =
          Date.parse(
            value
          );




        return Number.isFinite(
          parsed
        )
        &&
        parsed >=
        now
        -
        60
        *
        60
        *
        1000;
      }
    );




  if (
    startIndex < 0
  ) {


    startIndex =
      0;
  }




  const endIndex =
    Math.min(
      times.length,
      startIndex
      +
      24
    );




  for (
    let kinako =
      startIndex;


    kinako <
    endIndex;


    kinako++
  ) {


    const card =
      createElement(
        "div",
        "hourly-card"
      );




    const time =
      String(
        times[
          kinako
        ]
        ||
        ""
      );




    const probability =
      hourly
        .precipitation_probability
        ?.[kinako];




    card.append(
      createElement(
        "div",
        "hourly-time",
        time.slice(
          11,
          16
        )
        ||
        "--"
      ),


      createElement(
        "div",
        "hourly-icon",
        weatherIcon(
          hourly
            .weather_code
            ?.[kinako]
        )
      ),


      createElement(
        "strong",
        "",
        `${formatNumber(
          hourly
            .temperature_2m
            ?.[kinako],
          0
        )}°`
      ),


      createElement(
        "small",
        "",
        `${formatNumber(
          probability,
          0
        )}%`
      )
    );




    area.append(
      card
    );
  }
}




function renderWeeklyWeather(
  daily
) {


  const area = $(
    "weekly-forecast"
  );




  if (!area) {
    return;
  }




  area.replaceChildren();




  const times =
    daily.time
    ||
    [];




  for (
    let kinako =
      0;


    kinako <
    times.length;


    kinako++
  ) {


    const card =
      createElement(
        "div",
        "weekly-row"
      );




    const date =
      new Date(
        `${times[kinako]}T12:00:00`
      );




    const day =
      Number.isNaN(
        date.getTime()
      )
        ?
        times[kinako]
        :
        date.toLocaleDateString(
          "ja-JP",
          {
            month:
              "numeric",


            day:
              "numeric",


            weekday:
              "short"
          }
        );




    card.append(
      createElement(
        "span",
        "weekly-date",
        day
      ),


      createElement(
        "span",
        "weekly-icon",
        weatherIcon(
          daily
            .weather_code
            ?.[kinako]
        )
      ),


      createElement(
        "span",
        "weekly-temp",
        `${formatNumber(
          daily
            .temperature_2m_min
            ?.[kinako],
          0
        )}° / ${formatNumber(
          daily
            .temperature_2m_max
            ?.[kinako],
          0
        )}°`
      ),


      createElement(
        "span",
        "weekly-rain",
        `${formatNumber(
          daily
            .precipitation_probability_max
            ?.[kinako],
          0
        )}%`
      )
    );




    area.append(
      card
    );
  }
}




let radarLayer = null;
let radarFrames = [];
let radarTimer = null;
let radarHost = "";
let radarLastLoadedAt = 0;
let radarLoadPromise = null;


function stopRadar() {
 if (radarTimer) {
  clearInterval(radarTimer);
  radarTimer = null;
 }


 setText(
  "radar-play",
  "▶ 再生"
 );
}


function radarFrameTime(frame) {
 if (!frame?.time) {
  return "--";
 }


 return new Intl.DateTimeFormat(
  "ja-JP",
  {
   month: "numeric",
   day: "numeric",
   hour: "2-digit",
   minute: "2-digit"
  }
 ).format(
  new Date(
   Number(frame.time) * 1000
  )
 );
}


function showRadar() {
 if (
  !radarMap
  ||
  !radarFrames.length
  ||
  !radarHost
 ) {
  return;
 }


 const slider = $(
  "radar-slider"
 );


 const rawIndex = Number(
  slider?.value ?? 0
 );


 const index = Math.min(
  Math.max(
   Number.isFinite(rawIndex)
    ? rawIndex
    : 0,
   0
  ),
  radarFrames.length - 1
 );


 const frame =
  radarFrames[index];


 if (radarLayer) {
  radarMap.removeLayer(
   radarLayer
  );
 }


 radarLayer = L.tileLayer(
  `${radarHost}${frame.path}/256/{z}/{x}/{y}/2/1_1.png`,
  {
   opacity: 0.72,
   maxNativeZoom: 7,
   maxZoom: 18,
   tileSize: 256,
   attribution: "Weather data © RainViewer"
  }
 );


 radarLayer.addTo(
  radarMap
 );


 setText(
  "radar-time",
  radarFrameTime(frame)
 );
}


async function loadRadar(
 force = false
) {
 if (
  typeof L === "undefined"
 ) {
  return;
 }


 const point =
  getWeatherPoint();


 renderRadar(
  point,
  false
 );


 const now = Date.now();


 if (
  !force
  &&
  radarFrames.length
  &&
  now - radarLastLoadedAt < 60_000
 ) {
  showRadar();
  return;
 }


 if (radarLoadPromise) {
  await radarLoadPromise;
  showRadar();
  return;
 }


 radarLoadPromise = (
  async () => {
   const response = await fetch(
    "https://api.rainviewer.com/public/weather-maps.json",
    {
     cache: "no-store"
    }
   );


   if (!response.ok) {
    throw new Error(
     `RainViewer取得失敗: ${response.status}`
    );
   }


   const data =
    await response.json();


   const frames =
    data?.radar?.past;


   if (
    !data?.host
    ||
    !Array.isArray(frames)
    ||
    frames.length === 0
   ) {
    throw new Error(
     "雨雲レーダーのデータがありません"
    );
   }


   radarHost =
    data.host;


   radarFrames =
    frames;


   radarLastLoadedAt =
    Date.now();


   const slider = $(
    "radar-slider"
   );


   if (slider) {
    slider.min = "0";
    slider.max = String(
     radarFrames.length - 1
    );
    slider.step = "1";
    slider.value = String(
     radarFrames.length - 1
    );
   }
  }
 )();


 try {
  await radarLoadPromise;
  showRadar();
 } catch (error) {
  console.error(
   "loadRadar:",
   error
  );


  stopRadar();


  setText(
   "radar-time",
   "取得失敗"
  );
 } finally {
  radarLoadPromise = null;
 }
}


function renderRadar(
 point,
 shouldLoad = true
) {
 if (
  typeof L === "undefined"
 ) {
  return;
 }


 if (!radarMap) {
  radarMap =
   createLeafletMap(
    "radar-map",
    [
     point.latitude,
     point.longitude
    ],
    8
   );
 } else {
  radarMap.setView(
   [
    point.latitude,
    point.longitude
   ],
   8
  );
 }


 radarMap.invalidateSize();


 if (shouldLoad) {
  loadRadar().catch(
   error => {
    console.error(
     "loadRadar:",
     error
    );
   }
  );
 }
}


/* =========================================================
  13. 経路
========================================================= */


function setupRoute() {


  const origin = $(
    "route-origin"
  );




  const destination = $(
    "route-destination"
  );




  origin?.addEventListener(
    "input",
    () => {


      routeOrigin =
        null;


      setupRouteSearchTimer(
        "origin"
      );
    }
  );




  destination?.addEventListener(
    "input",
    () => {


      routeDestination =
        null;


      setupRouteSearchTimer(
        "destination"
      );
    }
  );




  $("route-current-location")
    ?.addEventListener(
      "click",
      useCurrentRouteLocation
    );




  $("route-search")
    ?.addEventListener(
      "click",
      loadRoute
    );




  const now =
    new Date();




  const local =
    new Date(
      now.getTime()
      -
      now.getTimezoneOffset()
      *
      60000
    )
    .toISOString()
    .slice(
      0,
      16
    );




  if (
    $("route-departure")
  ) {


    $("route-departure").value =
      local;
  }
}




const routeSearchTimers = {
  origin:
    null,


  destination:
    null
};




function setupRouteSearchTimer(
  type
) {
  clearTimeout(
    routeSearchTimers[
      type
    ]
  );

  routeSearchTimers[
    type
  ] =
    setTimeout(
      () => {
        searchRoutePlace(
          type
        );
      },
      350
    );
}


async function searchRoutePlace(
  type
) {
  const inputId =
    type === "origin"
      ? "route-origin"
      : "route-destination";

  const resultsId =
    type === "origin"
      ? "route-origin-results"
      : "route-destination-results";

  const input = $(
    inputId
  );

  const area = $(
    resultsId
  );

  if (
    !input
    ||
    !area
  ) {
    return;
  }

  const cleanQuery =
    String(
      input.value
      ||
      ""
    )
    .trim();

  area.replaceChildren();

  if (
    cleanQuery.length < 2
  ) {
    area.hidden =
      true;
    return;
  }

  try {
    const data =
      await requestJSON(
        `/api/cities?country=${encodeURIComponent(
          currentCountry.code
        )}&q=${encodeURIComponent(
          cleanQuery
        )}`
      );

    const results =
      Array.isArray(
        data?.results
      )
        ? data.results
        : [];

    if (
      !results.length
    ) {
      area.hidden =
        false;

      area.append(
        createElement(
          "div",
          "empty-state",
          "候補が見つかりませんでした"
        )
      );

      return;
    }

    for (
      const place
      of results
    ) {
      const latitude =
        Number(
          place.latitude
        );
      const longitude =
        Number(
          place.longitude
        );

      if (
        !Number.isFinite(
          latitude
        )
        ||
        !Number.isFinite(
          longitude
        )
      ) {
        continue;
      }

      const button =
        createElement(
          "button",
          "search-result"
        );

      button.type =
        "button";

      const name =
        String(
          place.name
          ||
          ""
        );

      const detail =
        String(
          place.detail
          ||
          [
            place.admin1,
            place.admin2
          ]
          .filter(
            Boolean
          )
          .join(
            "・"
          )
        );

      button.append(
        createElement(
          "strong",
          "",
          name
          ||
          "場所"
        )
      );

      if (
        detail
      ) {
        button.append(
          createElement(
            "small",
            "",
            detail
          )
        );
      }

      button.addEventListener(
        "click",
        () => {
          const selected = {
            name:
              name
              ||
              cleanQuery,
            detail:
              detail,
            latitude:
              latitude,
            longitude:
              longitude
          };

          if (
            type === "origin"
          ) {
            routeOrigin =
              selected;
          } else {
            routeDestination =
              selected;
          }

          input.value =
            selected.name;

          area.replaceChildren();
          area.hidden =
            true;

          setText(
            "route-timezone",
            `${currentCountry.name}の現地時刻を基準に検索します。`
          );

          showStatus(
            "route-status",
            ""
          );
        }
      );

      area.append(
        button
      );
    }

    area.hidden =
      area.childElementCount === 0;

  } catch (
    error
  ) {
    area.hidden =
      false;

    area.replaceChildren(
      createElement(
        "div",
        "empty-state",
        error.message
        ||
        "場所を検索できませんでした"
      )
    );
  }
}



async function useCurrentRouteLocation() {
  showStatus(
    "route-status",
    "現在地を取得しています..."
  );

  try {
    const position =
      await getCurrentPosition();

    routeOrigin = {
      name:
        "現在地",
      detail:
        "",
      latitude:
        position.coords.latitude,
      longitude:
        position.coords.longitude
    };

    if (
      $("route-origin")
    ) {
      $("route-origin").value =
        "現在地";
    }

    if (
      $("route-origin-results")
    ) {
      $("route-origin-results").hidden =
        true;
      $("route-origin-results").replaceChildren();
    }

    showStatus(
      "route-status",
      "現在地を出発地に設定しました。"
    );

  } catch (
    error
  ) {
    showStatus(
      "route-status",
      error.message
      ||
      "現在地を取得できませんでした。",
      true
    );
  }
}


function routeModeForBackend(
  value
) {
  if (
    value === "bicycle"
  ) {
    return "cycling";
  }

  if (
    value === "drive"
  ) {
    return "driving";
  }

  if (
    value === "walk"
  ) {
    return "walking";
  }

  return null;
}





async function loadRoute() {
  if (
    !routeOrigin
    ||
    !routeDestination
  ) {
    showStatus(
      "route-status",
      "出発地と目的地を候補から選択してください",
      true
    );

    return;
  }

  const mode =
    $("route-mode")?.value
    ||
    "walk";

  const searchButton =
    $("route-search");

  showStatus(
    "route-status",
    "経路を取得しています..."
  );

  if (
    searchButton
  ) {
    searchButton.disabled =
      true;
  }

  try {
    if (
      mode === "transit"
    ) {
      const googleParams =
        new URLSearchParams({
          api:
            "1",
          origin:
            `${routeOrigin.latitude},${routeOrigin.longitude}`,
          destination:
            `${routeDestination.latitude},${routeDestination.longitude}`,
          travelmode:
            "transit"
        });

      const link = $(
        "route-google-link"
      );

      if (
        link
      ) {
        link.href =
          `https://www.google.com/maps/dir/?${googleParams.toString()}`;
        link.hidden =
          false;
      }

      setText(
        "route-umbrella-icon",
        "🚆"
      );
      setText(
        "route-umbrella-title",
        "公共交通の経路"
      );
      setText(
        "route-umbrella-text",
        "公共交通の時刻・乗換案内はGoogle Mapsで確認してください。"
      );
      setText(
        "route-distance",
        "--"
      );
      setText(
        "route-duration",
        "--"
      );
      setText(
        "route-outdoor-time",
        "--"
      );
      setText(
        "route-wet-time",
        "--"
      );
      setText(
        "route-precipitation",
        "--"
      );
      setText(
        "route-rain-time",
        "公共交通は外部経路案内で確認"
      );
      setText(
        "route-data-note",
        "公共交通は無料の経路APIで正確な時刻表を保証できないため、Google Mapsへ接続します。"
      );

      if (
        $("route-result")
      ) {
        $("route-result").hidden =
          false;
      }

      showStatus(
        "route-status",
        "公共交通の経路リンクを作成しました。"
      );

      return;
    }

    const backendMode =
      routeModeForBackend(
        mode
      );

    if (
      !backendMode
    ) {
      throw new Error(
        "対応していない移動方法です"
      );
    }

    const params =
      new URLSearchParams({
        start_lat:
          String(
            routeOrigin.latitude
          ),
        start_lon:
          String(
            routeOrigin.longitude
          ),
        end_lat:
          String(
            routeDestination.latitude
          ),
        end_lon:
          String(
            routeDestination.longitude
          ),
        mode:
          backendMode
      });

    const route =
      await requestJSON(
        `/api/route?${params.toString()}`,
        {},
        30000
      );

    if (
      !route
      ||
      !Number.isFinite(
        Number(
          route.distance
        )
      )
      ||
      !Number.isFinite(
        Number(
          route.duration
        )
      )
    ) {
      throw new Error(
        "経路データを正しく取得できませんでした"
      );
    }

    const midpoint = {
      latitude:
        (
          Number(
            routeOrigin.latitude
          )
          +
          Number(
            routeDestination.latitude
          )
        )
        /
        2,
      longitude:
        (
          Number(
            routeOrigin.longitude
          )
          +
          Number(
            routeDestination.longitude
          )
        )
        /
        2
    };

    let weather =
      null;

    try {
      weather =
        await requestJSON(
          `/api/weather?lat=${encodeURIComponent(
            midpoint.latitude
          )}&lon=${encodeURIComponent(
            midpoint.longitude
          )}`
        );
    } catch (
      error
    ) {
      console.warn(
        "ROUTE WEATHER ERROR:",
        error
      );
    }

    renderRouteResult(
      route,
      weather,
      mode
    );

    showStatus(
      "route-status",
      "経路を取得しました"
    );

  } catch (
    error
  ) {
    console.error(
      "ROUTE LOAD ERROR:",
      error
    );

    showStatus(
      "route-status",
      error?.message
      ||
      "経路を取得できませんでした",
      true
    );

  } finally {
    if (
      searchButton
    ) {
      searchButton.disabled =
        false;
    }
  }
}
function renderRouteResult(
  route,
  weather,
  mode
) {


  const distance =
    numberValue(
      route.distance
    )
    ||
    0;




  const duration =
    numberValue(
      route.duration
    )
    ||
    0;




  let outdoor =
    duration;




  if (
    mode
    ===
    "drive"
  ) {


    outdoor =
      Math.min(
        300,
        duration
      );
  }




  if (
    mode
    ===
    "transit"
  ) {


    outdoor =
      Math.min(
        1200,
        duration
        *
        0.25
      );
  }




  const current =
    weather?.current
    ||
    {};




  const precipitation =
    numberValue(
      current.precipitation
    )
    ||
    0;




  const rain =
    numberValue(
      current.rain
    )
    ||
    0;




  const isRain =
    precipitation > 0.05
    ||
    rain > 0.05;




  let title =
    "傘不要の目安";




  let icon =
    "☀️";




  let text =
    "現在の予報では大きな雨は確認されていません。";




  if (isRain) {


    title =
      mode
      ===
      "bicycle"
        ?
        "レインウェア推奨"
        :
        "傘を持っていくことを推奨";




    icon =
      "☔";




    text =
      `経路周辺で${formatNumber(
        Math.max(
          precipitation,
          rain
        ),
        1
      )} mm程度の降水が確認されています。`;
  }




  setText(
    "route-umbrella-icon",
    icon
  );




  setText(
    "route-umbrella-title",
    title
  );




  setText(
    "route-umbrella-text",
    text
  );




  setText(
    "route-distance",
    formatDistance(
      distance
    )
  );




  setText(
    "route-duration",
    formatDuration(
      duration
    )
  );




  setText(
    "route-outdoor-time",
    formatDuration(
      outdoor
    )
  );




  setText(
    "route-wet-time",
    isRain
      ?
      formatDuration(
        outdoor
      )
      :
      "0分"
  );




  setText(
    "route-precipitation",
    `${formatNumber(
      Math.max(
        precipitation,
        rain
      ),
      1
    )} mm`
  );




  setText(
    "route-rain-time",
    isRain
      ?
      "移動時間帯に雨の可能性あり"
      :
      "目立った雨なし"
  );




  setText(
    "route-data-note",


    "経路と周辺の天気予報から算出した目安です。"
  );




  const travelMode = {
    walk:
      "walking",


    bicycle:
      "bicycling",


    drive:
      "driving",


    transit:
      "transit"
  }[
    mode
  ]
  ||
  "walking";




  const googleParams =
    new URLSearchParams({
      api:
        "1",


      origin:
        `${routeOrigin.latitude},${routeOrigin.longitude}`,


      destination:
        `${routeDestination.latitude},${routeDestination.longitude}`,


      travelmode:
        travelMode
    });




  const link = $(
    "route-google-link"
  );




  if (link) {


    link.href =
      `https://www.google.com/maps/dir/?${googleParams.toString()}`;


    link.hidden =
      false;
  }




  $("route-result").hidden =
    false;
}




/* =========================================================
  14. 移動履歴
========================================================= */


function initializeHistoryMap() {


  if (
    historyMap
    ||
    typeof L
    ===
    "undefined"
  ) {


    return;
  }




  historyMap =
    createLeafletMap(
      "history-map",
      [
        35.6762,
        139.6503
      ],
      12
    );
}




async function loadTrips() {
  initializeHistoryMap();

  try {
    const data =
      await requestJSON(
        "/api/game/trips"
      );

    renderTripHistory(
      data.trips
      ||
      []
    );

    await loadCurrentTrip();

    showStatus(
      "history-status",
      ""
    );

  } catch (
    error
  ) {
    showStatus(
      "history-status",
      error.message,
      true
    );
  }
}


async function loadCurrentTrip() {
  try {
    const data =
      await requestJSON(
        "/api/game/trip/current"
      );

    currentTrip =
      data.trip
      ||
      null;

    if (
      data.player
    ) {
      gamePlayer =
        data.player;

      setText(
        "history-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );

      if (
        gamePlayer.name
      ) {
        setText(
          "history-player-name",
          gamePlayer.name
        );
      }
    }

    updateTripButtons();

    if (
      currentTrip
    ) {
      startTripLocationWatch();
    }

  } catch (
    error
  ) {
    console.error(
      "CURRENT TRIP ERROR:",
      error
    );
  }
}


function updateTripButtons() {
  const active =
    Boolean(
      currentTrip
    );

  setText(
    "trip-mode",
    active
      ? "記録中"
      : "停止中"
  );

  setText(
    "trip-distance",
    active
      ? formatDistance(
          currentTrip.distance
        )
      : "0 m"
  );

  setText(
    "trip-coins",
    active
      ? formatNumber(
          currentTrip.coins
          ||
          0,
          0
        )
      : "0"
  );

  if (
    $("trip-start")
  ) {
    $("trip-start").disabled =
      active;
  }

  if (
    $("trip-stop")
  ) {
    $("trip-stop").disabled =
      !active;
  }

  showStatus(
    "trip-status",
    active
      ? "移動記録中・GPSを取得しています。"
      : "記録停止中"
  );
}


let gamePlayer =
  null;


function setGameText(
  id,
  value
) {
  const element =
    document.getElementById(
      id
    );

  if (
    element
  ) {
    element.textContent =
      String(
        value
      );
  }
}


async function loadGameSession() {
  const data =
    await requestJSON(
      "/api/game/bootstrap",
      {},
      20000
    );

  gamePlayer =
    data.player
    ||
    {};

  setGameText(
    "conquest-coins",
    Number(
      gamePlayer.coins
      ||
      0
    ).toLocaleString(
      "ja-JP"
    )
  );

  setGameText(
    "conquest-land-count",
    gamePlayer.land_count
    ??
    0
  );

  setGameText(
    "conquest-daily-income",
    `${Number(
      gamePlayer.daily_income
      ||
      0
    ).toLocaleString(
      "ja-JP"
    )} coin`
  );

  setGameText(
    "history-coins",
    Number(
      gamePlayer.coins
      ||
      0
    ).toLocaleString(
      "ja-JP"
    )
  );

  if (
    gamePlayer.name
  ) {

    setGameText(
      "history-player-name",
      gamePlayer.name
    );

    setGameText(
      "conquest-player-name",
      gamePlayer.name
    );
  }

  currentTrip =
    data.active_trip
    ||
    currentTrip
    ||
    null;

  updateTripButtons();

  return data;
}


async function startTrip() {
  showStatus(
    "trip-status",
    "移動記録を開始しています..."
  );

  try {
    const data =
      await requestJSON(
        "/api/game/trip/start",
        {
          method:
            "POST",
          headers: {
            "Content-Type":
              "application/json"
          },
          body:
            JSON.stringify({})
        },
        20000
      );

    currentTrip =
      data.trip
      ||
      null;

    if (
      data.player
    ) {
      gamePlayer =
        data.player;

      setText(
        "history-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );
    }

    updateTripButtons();

    startTripLocationWatch();

    showStatus(
      "trip-status",
      "移動記録を開始しました。"
    );

  } catch (
    error
  ) {
    console.error(
      "START TRIP ERROR:",
      error
    );

    showStatus(
      "trip-status",
      error.message
      ||
      "移動記録を開始できませんでした。",
      true
    );
  }
}


function startTripLocationWatch() {
  if (
    !currentTrip
    ||
    !navigator.geolocation
  ) {
    return;
  }

  if (
    tripWatchId !== null
  ) {
    navigator.geolocation.clearWatch(
      tripWatchId
    );
  }

  tripWatchId =
    navigator.geolocation.watchPosition(
      position => {
        setText(
          "trip-accuracy",
          `${Math.round(
            position.coords.accuracy
            ||
            0
          )} m`
        );

        sendTripPoint(
          position
        );
      },
      error => {
        if (
          error.code === 1
        ) {
          showStatus(
            "trip-status",
            "位置情報が許可されていません。",
            true
          );
        } else if (
          error.code === 3
        ) {
          showStatus(
            "trip-status",
            "GPSを取得中です。"
          );
        } else {
          showStatus(
            "trip-status",
            "現在地を取得できません。",
            true
          );
        }
      },
      {
        enableHighAccuracy:
          true,
        maximumAge:
          5000,
        timeout:
          20000
      }
    );
}


async function sendTripPoint(
  position
) {
  if (
    !currentTrip
  ) {
    return;
  }

  try {
    const data =
      await requestJSON(
        "/api/game/trip/point",
        {
          method:
            "POST",
          headers: {
            "Content-Type":
              "application/json"
          },
          body:
            JSON.stringify({
              lat:
                position.coords.latitude,
              lon:
                position.coords.longitude,
              accuracy:
                position.coords.accuracy
                ||
                0
            })
        }
      );

    if (
      data.trip
    ) {
      currentTrip =
        data.trip;
    }

    if (
      data.player
    ) {
      gamePlayer =
        data.player;

      setText(
        "history-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );

      setText(
        "conquest-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );
    }

    if (
      data.accepted === false
    ) {
      showStatus(
        "trip-status",
        data.reason
        ||
        "この位置情報は記録しませんでした。"
      );

      return;
    }

    updateTripButtons();

    showStatus(
      "trip-status",
      data.earned
        ? `移動記録中・${data.earned} coin獲得`
        : "移動記録中"
    );

  } catch (
    error
  ) {
    console.error(
      "TRIP POINT ERROR:",
      error
    );
  }
}


async function stopTrip() {
  showStatus(
    "trip-status",
    "移動記録を終了しています..."
  );

  try {
    const data =
      await requestJSON(
        "/api/game/trip/stop",
        {
          method:
            "POST",
          headers: {
            "Content-Type":
              "application/json"
          },
          body:
            JSON.stringify({})
        },
        20000
      );

    if (
      tripWatchId !== null
    ) {
      navigator.geolocation.clearWatch(
        tripWatchId
      );

      tripWatchId =
        null;
    }

    currentTrip =
      null;

    if (
      data.player
    ) {
      gamePlayer =
        data.player;

      setText(
        "history-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );

      setText(
        "conquest-coins",
        formatNumber(
          gamePlayer.coins,
          0
        )
      );
    }

    updateTripButtons();

    showStatus(
      "trip-status",
      `移動記録を終了しました。獲得 ${formatNumber(
        data.trip?.coins
        ||
        0,
        0
      )} coin`
    );

    await loadTrips();

  } catch (
    error
  ) {
    console.error(
      "STOP TRIP ERROR:",
      error
    );

    showStatus(
      "trip-status",
      error.message
      ||
      "移動記録を終了できませんでした。",
      true
    );
  }
}


function renderTripHistory(
  trips
) {
  const area = $(
    "trip-list"
  );

  if (
    !area
  ) {
    return;
  }

  area.replaceChildren();

  if (
    !Array.isArray(
      trips
    )
    ||
    !trips.length
  ) {
    area.append(
      createElement(
        "div",
        "empty-state",
        "まだ移動履歴がありません"
      )
    );

    return;
  }

  for (
    const trip
    of trips
  ) {
    const card =
      createElement(
        "button",
        "news-card"
      );

    card.type =
      "button";

    card.append(
      createElement(
        "div",
        "news-source",
        trip.active
          ? "記録中"
          : formatDate(
              trip.started_at
            )
      ),
      createElement(
        "div",
        "news-title",
        `移動距離 ${formatDistance(
          trip.distance
        )}`
      ),
      createElement(
        "div",
        "ranking-detail",
        `獲得 ${formatNumber(
          trip.coins
          ||
          0,
          0
        )} coin`
      ),
      createElement(
        "div",
        "news-arrow",
        "→"
      )
    );

    card.addEventListener(
      "click",
      () => {
        loadTripDetail(
          trip.id
        );
      }
    );

    area.append(
      card
    );
  }
}


async function loadTripDetail(
  tripId
) {
  initializeHistoryMap();

  try {
    const data =
      await requestJSON(
        `/api/game/trips/${encodeURIComponent(
          tripId
        )}`
      );

    const points =
      data.points
      ||
      [];

    historyRouteLayer?.remove();

    if (
      !points.length
    ) {
      showStatus(
        "history-status",
        "この移動には位置データがありません"
      );

      return;
    }

    const latlngs =
      points.map(
        point => [
          point.lat,
          point.lon
        ]
      );

    historyRouteLayer =
      L.polyline(
        latlngs,
        {
          weight:
            5
        }
      )
      .addTo(
        historyMap
      );

    historyMap.fitBounds(
      historyRouteLayer.getBounds(),
      {
        padding: [
          30,
          30
        ]
      }
    );

    showStatus(
      "history-status",
      `移動距離 ${formatDistance(
        data.trip.distance
      )}`
    );

  } catch (
    error
  ) {
    showStatus(
      "history-status",
      error.message,
      true
    );
  }
}


/* =========================================================
  15. ゲーム初期化
========================================================= */


async function loadGame() {


  showStatus(
    "conquest-status",
    "ゲームデータを取得しています..."
  );




  try {


    const data =
      await requestJSON(
        "/api/game/bootstrap"
      );




    currentGamePlayer =
      data.player;




    renderGamePlayer(
      data.player,
      data.stats
    );




    await Promise.all([
      loadRanking(),
      loadNotifications(),
      loadBuyouts()
    ]);




    if (
      currentGamePosition
    ) {


      await loadGameMap(
        currentGamePosition.latitude,
        currentGamePosition.longitude
      );


    } else {


      showStatus(
        "conquest-status",
        "現在地ボタンを押すと周辺の土地を表示します。"
      );
    }


  } catch (
    error
  ) {


    showStatus(
      "conquest-status",
      error.message,
      true
    );
  }
}
function renderGamePlayer(
  player,
  stats = {}
) {


  if (!player) {
    return;
  }




  currentGamePlayer =
    player;




  setText(
    "conquest-player-name",
    player.name
    ||
    "Traveler"
  );




  setText(
    "conquest-coins",
    formatNumber(
      player.coins,
      0
    )
  );




  setText(
    "conquest-land-count",
    stats.land_count
    ??
    player.land_count
    ??
    0
  );




  setText(
    "conquest-daily-income",
    `${formatNumber(
      stats.daily_income
      ??
      player.daily_income
      ??
      0,
      0
    )} coin`
  );




  setText(
    "history-player-name",
    player.name
    ||
    "Traveler"
  );




  setText(
    "history-coins",
    formatNumber(
      player.coins,
      0
    )
  );




  const input = $(
    "game-player-name-input"
  );




  if (
    input
    &&
    document.activeElement
    !==
    input
  ) {


    input.value =
      player.name
      ||
      "";
  }
}




async function saveGamePlayerName() {


  const input = $(
    "game-player-name-input"
  );




  if (!input) {
    return;
  }




  const name =
    input.value.trim();




  if (
    !name
  ) {


    showStatus(
      "conquest-status",
      "プレイヤー名を入力してください。",
      true
    );


    return;
  }




  showStatus(
    "conquest-status",
    "プレイヤー名を保存しています..."
  );




  try {


    const data =
      await requestJSON(
        "/api/game/profile",
        {
          method:
            "POST",


          headers: {
            "Content-Type":
              "application/json"
          },


          body:
            JSON.stringify({
              name:
                name
            })
        }
      );




    if (
      data.player
    ) {


      currentGamePlayer =
        data.player;


      renderGamePlayer(
        data.player,
        data.stats
        ||
        {}
      );
    }




    showStatus(
      "conquest-status",
      "プレイヤー名を保存しました。"
    );


  } catch (
    error
  ) {


    showStatus(
      "conquest-status",
      error.message
      ||
      "プレイヤー名を保存できませんでした。",
      true
    );
  }
}




async function locateGame() {


  showStatus(
    "conquest-status",
    "現在地を取得しています..."
  );




  try {


    const position =
      await getCurrentPosition();




    currentGamePosition = {
      latitude:
        position.coords.latitude,


      longitude:
        position.coords.longitude,


      accuracy:
        position.coords.accuracy
    };




    setText(
      "conquest-location-accuracy",
      `${Math.round(
        currentGamePosition.accuracy
        ||
        0
      )} m`
    );




    await loadGameMap(
      currentGamePosition.latitude,
      currentGamePosition.longitude
    );




    showStatus(
      "conquest-status",
      "現在地周辺の土地を表示しました。"
    );


  } catch (
    error
  ) {


    showStatus(
      "conquest-status",
      error.message
      ||
      "現在地を取得できませんでした。",
      true
    );
  }
}




/* =========================================================
  16. 旧 Leaflet 土地マップ
========================================================= */


async function loadGameMapLegacy(
  latitude,
  longitude
) {


  if (
    typeof L
    ===
    "undefined"
  ) {


    showStatus(
      "conquest-status",
      "地図ライブラリを読み込めませんでした。",
      true
    );


    return;
  }




  if (
    !conquestMap
  ) {


    conquestMap =
      createLeafletMap(
        "conquest-map",
        [
          latitude,
          longitude
        ],
        17
      );


  } else {


    conquestMap.setView(
      [
        latitude,
        longitude
      ],
      17
    );
  }




  conquestMap.invalidateSize();




  try {


    const params =
      new URLSearchParams({
        lat:
          String(
            latitude
          ),


        lon:
          String(
            longitude
          )
      });




    const data =
      await requestJSON(
        `/api/game/map?${params.toString()}`,
        {},
        30000
      );




    renderGameParcels(
      data.lands
      ||
      data.parcels
      ||
      []
    );


  } catch (
    error
  ) {


    console.error(
      "GAME MAP LEGACY ERROR:",
      error
    );




    showStatus(
      "conquest-status",
      error.message
      ||
      "土地情報を取得できませんでした。",
      true
    );
  }
}




function countLocalPlayers(
  lands
) {


  const owners =
    new Set();




  for (
    const land
    of
    lands
    ||
    []
  ) {


    if (
      land.owner_id
    ) {


      owners.add(
        String(
          land.owner_id
        )
      );
    }
  }




  return owners.size;
}




function clearConquestLayers() {


  for (
    const layer
    of
    conquestLayers
  ) {


    try {


      layer.remove();


    } catch (
      error
    ) {


      console.warn(
        "LAYER REMOVE ERROR:",
        error
      );
    }
  }




  conquestLayers =
    [];
}




function gameLandColor(
  land
) {


  if (
    !land.owner_id
  ) {


    return "#353b46";
  }




  const myId =
    currentGamePlayer?.id
    ??
    currentGamePlayer?.player_id;




  if (
    myId !== null
    &&
    myId !== undefined
    &&
    String(
      land.owner_id
    )
    ===
    String(
      myId
    )
  ) {


    return "#3488ff";
  }




  const source =
    String(
      land.owner_id
    );




  let hash =
    0;




  for (
    let kinako =
      0;


    kinako <
    source.length;


    kinako++
  ) {


    hash =
      (
        hash
        *
        31
        +
        source.charCodeAt(
          kinako
        )
      )
      >>>
      0;
  }




  const hue =
    hash
    %
    360;




  return `hsl(${hue} 70% 55%)`;
}




function renderGameParcels(
  lands
) {


  if (
    !conquestMap
  ) {


    return;
  }




  clearConquestLayers();




  const rows =
    Array.isArray(
      lands
    )
      ?
      lands
      :
      [];




  for (
    const land
    of
    rows
  ) {


    let polygon =
      land.polygon
      ||
      land.polygon_json;




    if (
      typeof polygon
      ===
      "string"
    ) {


      try {


        polygon =
          JSON.parse(
            polygon
          );


      } catch {


        polygon =
          null;
      }
    }




    if (
      !Array.isArray(
        polygon
      )
      ||
      !polygon.length
    ) {


      continue;
    }




    let latlngs =
      polygon;




    if (
      Array.isArray(
        polygon[0]
      )
      &&
      Array.isArray(
        polygon[0][0]
      )
    ) {


      latlngs =
        polygon[0];
    }




    const converted =
      latlngs
        .map(
          point => {


            if (
              !Array.isArray(
                point
              )
              ||
              point.length
              <
              2
            ) {


              return null;
            }




            const first =
              Number(
                point[0]
              );




            const second =
              Number(
                point[1]
              );




            if (
              !Number.isFinite(
                first
              )
              ||
              !Number.isFinite(
                second
              )
            ) {


              return null;
            }




            if (
              Math.abs(
                first
              )
              >
              90
            ) {


              return [
                second,
                first
              ];
            }




            return [
              first,
              second
            ];
          }
        )
        .filter(
          Boolean
        );




    if (
      converted.length
      <
      3
    ) {


      continue;
    }




    const color =
      gameLandColor(
        land
      );




    const layer =
      L.polygon(
        converted,
        {
          color:
            color,


          fillColor:
            color,


          fillOpacity:
            land.owner_id
              ?
              0.42
              :
              0.22,


          weight:
            land.owner_id
              ?
              2
              :
              1
        }
      );




    layer.addTo(
      conquestMap
    );




    layer.on(
      "click",
      () => {


        openLandPanel(
          land
        );
      }
    );




    conquestLayers.push(
      layer
    );
  }




  setText(
    "local-conquerors",
    countLocalPlayers(
      rows
    )
  );
}




function landTypeName(
  value
) {


  const names = {
    building:
      "建物",


    commercial:
      "商業施設",


    retail:
      "店舗",


    station:
      "駅",


    railway:
      "鉄道施設",


    park:
      "公園",


    school:
      "学校",


    university:
      "大学",


    hospital:
      "病院",


    hotel:
      "ホテル",


    restaurant:
      "飲食店",


    residential:
      "住宅",


    office:
      "オフィス",


    industrial:
      "工業施設",


    land:
      "土地"
  };




  return names[
    value
  ]
  ||
  value
  ||
  "土地";
}




function openLandPanel(
  land
) {


  selectedLand =
    land;




  const panel = $(
    "land-panel"
  );




  if (
    panel
  ) {


    panel.hidden =
      false;
  }




  const name =
    land.name
    ||
    land.land_name
    ||
    "名称未設定";




  const type =
    landTypeName(
      land.land_type
    );




  const price =
    numberValue(
      land.price
      ??
      land.purchase_price
    )
    ??
    0;




  const income =
    numberValue(
      land.daily_income
    )
    ??
    0;




  const area =
    numberValue(
      land.area_m2
    );




  const stationDistance =
    numberValue(
      land.station_distance
    );




  setText(
    "land-name",
    name
  );




  setText(
    "land-type",
    type
  );




  setText(
    "land-price",
    formatCoins(
      price
    )
  );




  setText(
    "land-income",
    `${formatNumber(
      income,
      0
    )} coin / 日`
  );




  setText(
    "land-area",
    area === null
      ?
      "--"
      :
      `${formatNumber(
        area,
        0
      )} m²`
  );




  setText(
    "land-station-distance",
    stationDistance === null
      ?
      "--"
      :
      formatDistance(
        stationDistance
      )
  );




  const ownerName =
    land.owner_name
    ||
    (
      land.owner_id
        ?
        `Player ${land.owner_id}`
        :
        "未購入"
    );




  setText(
    "land-owner",
    ownerName
  );




  const myId =
    currentGamePlayer?.id
    ??
    currentGamePlayer?.player_id;




  const ownedByMe =
    land.owner_id
    &&
    myId !== null
    &&
    myId !== undefined
    &&
    String(
      land.owner_id
    )
    ===
    String(
      myId
    );




  const buyButton = $(
    "land-buy"
  );




  if (
    buyButton
  ) {


    if (
      !land.owner_id
    ) {


      buyButton.hidden =
        false;


      buyButton.disabled =
        false;


      buyButton.textContent =
        `${formatCoins(
          price
        )} で購入`;


    } else if (
      ownedByMe
    ) {


      buyButton.hidden =
        true;


    } else {


      buyButton.hidden =
        false;


      buyButton.disabled =
        false;


      buyButton.textContent =
        `${formatCoins(
          price
          *
          2
        )} で買収申請`;
    }
  }




  const defendButton = $(
    "land-defend-button"
  );




  if (
    defendButton
  ) {


    defendButton.hidden =
      true;
  }
}




async function buySelectedLand() {


  if (
    !selectedLand
  ) {


    showStatus(
      "conquest-status",
      "購入する土地を選択してください。",
      true
    );


    return;
  }




  const myId =
    currentGamePlayer?.id
    ??
    currentGamePlayer?.player_id;




  if (
    selectedLand.owner_id
    &&
    myId !== null
    &&
    myId !== undefined
    &&
    String(
      selectedLand.owner_id
    )
    ===
    String(
      myId
    )
  ) {


    showStatus(
      "conquest-status",
      "この土地はすでに所有しています。",
      true
    );


    return;
  }




  const isBuyout =
    Boolean(
      selectedLand.owner_id
    );




  const endpoint =
    isBuyout
      ?
      "/api/game/cell/buyout"
      :
      "/api/game/cell/buy";




  const button = $(
    "land-buy"
  );




  if (
    button
  ) {


    button.disabled =
      true;
  }




  showStatus(
    "conquest-status",
    isBuyout
      ?
      "買収申請を送信しています..."
      :
      "土地を購入しています..."
  );




  try {


    let payload;




    if (
      isBuyout
    ) {


      payload = {
        cell_id:
          selectedLand.cell_id
      };


    } else {


      let polygon =
        selectedLand.polygon
        ||
        selectedLand.polygon_json
        ||
        [];




      if (
        typeof polygon
        ===
        "string"
      ) {


        try {


          polygon =
            JSON.parse(
              polygon
            );


        } catch {


          polygon =
            [];
        }
      }




      payload = {
        cell_id:
          selectedLand.cell_id,


        name:
          selectedLand.name
          ||
          selectedLand.land_name
          ||
          "名称未設定",


        land_type:
          selectedLand.land_type
          ||
          "land",


        osm_type:
          selectedLand.osm_type
          ||
          null,


        osm_id:
          selectedLand.osm_id
          ||
          null,


        polygon:
          polygon,


        area_m2:
          numberValue(
            selectedLand.area_m2
          ),


        station_distance:
          numberValue(
            selectedLand.station_distance
          ),


        daily_income:
          numberValue(
            selectedLand.daily_income
          ),


        price:
          numberValue(
            selectedLand.price
            ??
            selectedLand.purchase_price
          ),


        latitude:
          numberValue(
            selectedLand.latitude
            ??
            selectedLand.center_lat
          ),


        longitude:
          numberValue(
            selectedLand.longitude
            ??
            selectedLand.center_lon
          )
      };
    }




    const data =
      await requestJSON(
        endpoint,
        {
          method:
            "POST",


          headers: {
            "Content-Type":
              "application/json"
          },


          body:
            JSON.stringify(
              payload
            )
        },
        30000
      );




    if (
      data.player
    ) {


      currentGamePlayer =
        data.player;
    }




    if (
      isBuyout
    ) {


      showStatus(
        "conquest-status",
        "買収申請を送りました。所有者は24時間以内に防衛できます。"
      );


    } else {


      showStatus(
        "conquest-status",
        "土地を購入しました。"
      );
    }




    await refreshGameAfterAction();


  } catch (
    error
  ) {


    showStatus(
      "conquest-status",
      error.message
      ||
      (
        isBuyout
          ?
          "買収申請に失敗しました。"
          :
          "土地を購入できませんでした。"
      ),
      true
    );


  } finally {


    if (
      button
    ) {


      button.disabled =
        false;
    }
  }
}




async function refreshGameMe() {


  try {


    const data =
      await requestJSON(
        "/api/game/me"
      );




    if (
      data.player
    ) {


      currentGamePlayer =
        data.player;


      renderGamePlayer(
        data.player,
        data.stats
        ||
        {}
      );
    }




    return data;


  } catch (
    error
  ) {


    console.error(
      "GAME ME ERROR:",
      error
    );


    return null;
  }
}




async function refreshGameAfterAction() {


  await refreshGameMe();




  await Promise.all([
    loadRanking(),
    loadNotifications(),
    loadBuyouts()
  ]);




  if (
    currentGamePosition
  ) {


    await loadGameMap(
      currentGamePosition.latitude,
      currentGamePosition.longitude
    );
  }
}




/* =========================================================
  17. 買収
========================================================= */


async function loadBuyouts() {


  const area = $(
    "buyout-list"
  );




  if (!area) {
    return;
  }




  try {


    const data =
      await requestJSON(
        "/api/game/buyouts"
      );




    renderBuyouts(
      data.buyouts
      ||
      []
    );


  } catch (
    error
  ) {


    area.replaceChildren(
      createElement(
        "div",
        "empty-state",
        "買収情報を取得できませんでした"
      )
    );
  }
}




function buyoutStatusName(
  status
) {


  const names = {
    pending:
      "防衛待ち",


    defended:
      "防衛済み",


    completed:
      "買収成立",


    cancelled:
      "キャンセル"
  };




  return names[
    status
  ]
  ||
  status
  ||
  "--";
}




function remainingTimeText(
  expiresAt
) {


  const timestamp =
    numberValue(
      expiresAt
    );




  if (
    timestamp === null
  ) {


    return "--";
  }




  const remaining =
    timestamp
    *
    1000
    -
    Date.now();




  if (
    remaining <= 0
  ) {


    return "期限切れ";
  }




  const hours =
    Math.floor(
      remaining
      /
      HOUR
    );




  const minutes =
    Math.floor(
      (
        remaining
        %
        HOUR
      )
      /
      MINUTE
    );




  return `${hours}時間${minutes}分`;
}




function renderBuyouts(
  buyouts
) {


  const area = $(
    "buyout-list"
  );




  if (!area) {
    return;
  }




  area.replaceChildren();




  if (
    !Array.isArray(
      buyouts
    )
    ||
    !buyouts.length
  ) {


    area.append(
      createElement(
        "div",
        "empty-state",
        "現在の買収申請はありません"
      )
    );


    return;
  }




  const myId =
    currentGamePlayer?.id
    ??
    currentGamePlayer?.player_id;




  for (
    const buyout
    of
    buyouts
  ) {


    const card =
      createElement(
        "div",
        "buyout-card"
      );




    card.append(
      createElement(
        "strong",
        "",
        buyout.land_name
        ||
        buyout.name
        ||
        "土地"
      ),


      createElement(
        "div",
        "",
        `状態: ${buyoutStatusName(
          buyout.status
        )}`
      ),


      createElement(
        "div",
        "",
        `提示額: ${formatCoins(
          buyout.offer_price
        )}`
      )
    );




    if (
      buyout.status
      ===
      "pending"
    ) {


      card.append(
        createElement(
          "div",
          "",
          `残り: ${remainingTimeText(
            buyout.expires_at
          )}`
        )
      );
    }




    const ownerId =
      buyout.owner_id
      ??
      buyout.seller_id;




    if (
      buyout.status
      ===
      "pending"
      &&
      myId !== null
      &&
      myId !== undefined
      &&
      String(
        ownerId
      )
      ===
      String(
        myId
      )
    ) {


      const defend =
        createButton(
          "買い戻して防衛",


          () => {


            defendBuyout(
              buyout.id
            );
          },


          "route-button"
        );




      card.append(
        defend
      );
    }




    area.append(
      card
    );
  }
}




async function defendBuyout(
  buyoutId
) {


  if (
    buyoutId === null
    ||
    buyoutId === undefined
  ) {


    return;
  }




  showStatus(
    "conquest-status",
    "土地を防衛しています..."
  );




  try {


    const data =
      await requestJSON(
        `/api/game/buyout/${encodeURIComponent(
          buyoutId
        )}/defend`,
        {
          method:
            "POST",


          headers: {
            "Content-Type":
              "application/json"
          },


          body:
            JSON.stringify({})
        }
      );




    if (
      data.player
    ) {


      currentGamePlayer =
        data.player;
    }




    showStatus(
      "conquest-status",
      "土地を防衛しました。"
    );




    await refreshGameAfterAction();


  } catch (
    error
  ) {


    showStatus(
      "conquest-status",
      error.message
      ||
      "土地を防衛できませんでした。",
      true
    );
  }
}




/* =========================================================
  18. 通知
========================================================= */


async function loadNotifications() {


  const area = $(
    "game-notifications"
  );




  if (!area) {
    return;
  }




  try {


    const data =
      await requestJSON(
        "/api/game/notifications"
      );




    renderNotifications(
      data.notifications
      ||
      []
    );




    setText(
      "notification-count",
      data.unread_count
      ??
      0
    );


  } catch (
    error
  ) {


    area.replaceChildren(
      createElement(
        "div",
        "empty-state",
        "通知を取得できませんでした"
      )
    );
  }
}




function renderNotifications(
  notifications
) {


  const area = $(
    "game-notification"
  );




  if (!area) {
    return;
  }




  area.replaceChildren();




  if (
    !Array.isArray(
      notifications
    )
    ||
    !notifications.length
  ) {


    area.append(
      createElement(
        "div",
        "empty-state",
        "通知はありません"
      )
    );


    return;
  }




  for (
    const notification
    of
    notifications
  ) {


    const card =
      createElement(
        "div",
        "notification-card"
      );




    if (
      !notification.read
      &&
      !notification.is_read
    ) {


      card.classList.add(
        "unread"
      );
    }




    card.append(
      createElement(
        "strong",
        "",
        notification.title
        ||
        "通知"
      ),


      createElement(
        "div",
        "",
        notification.message
        ||
        ""
      )
    );




    if (
      notification.created_at
    ) {


      card.append(
        createElement(
          "small",
          "",
          formatDate(
            notification.created_at
          )
        )
      );
    }




    area.append(
      card
    );
  }
}




async function markNotificationsRead() {


  try {


    await requestJSON(
      "/api/game/notifications/read",
      {
        method:
          "POST",


        headers: {
          "Content-Type":
            "application/json"
        },


        body:
          JSON.stringify({})
      }
    );




    await loadNotifications();


  } catch (
    error
  ) {


    console.error(
      "NOTIFICATION READ ERROR:",
      error
    );
  }
}




/* =========================================================
  19. ランキング
========================================================= */


async function loadRanking() {


  const area = $(
    "land-ranking"
  );




  if (!area) {
    return;
  }




  try {


    const data =
      await requestJSON(
        "/api/game/ranking"
      );




    renderRanking(
      data.ranking
      ||
      data.players
      ||
      []
    );


  } catch (
    error
  ) {


    area.replaceChildren(
      createElement(
        "div",
        "empty-state",
        "ランキングを取得できませんでした"
      )
    );
  }
}




function renderRanking(
  ranking
) {


  const area = $(
    "land-ranking"
  );




  if (!area) {
    return;
  }




  area.replaceChildren();




  if (
    !Array.isArray(
      ranking
    )
    ||
    !ranking.length
  ) {


    area.append(
      createElement(
        "div",
        "empty-state",
        "ランキングデータがありません"
      )
    );


    return;
  }




  ranking.forEach(
    (
      player,
      index
    ) => {


      const row =
        createElement(
          "div",
          "ranking-row"
        );




      row.append(
        createElement(
          "strong",
          "ranking-position",
          `${index + 1}`
        ),


        createElement(
          "span",
          "ranking-name",
          player.name
          ||
          "Traveler"
        ),


        createElement(
          "span",
          "ranking-detail",
          `${formatNumber(
            player.land_count
            ||
            0,
            0
          )} 土地`
        ),


        createElement(
          "span",
          "ranking-coins",
          formatCoins(
            player.coins
          )
        )
      );




      area.append(
        row
      );
    }
  );
}




/* =========================================================
  20. ゲームイベント
========================================================= */


function setupGame() {


  $("conquest-locate")
    ?.addEventListener(
      "click",
      locateGame
    );




  $("conquest-refresh")
    ?.addEventListener(
      "click",
      async () => {


        if (
          currentGamePosition
        ) {


          await loadGameMap(
            currentGamePosition.latitude,
            currentGamePosition.longitude
          );


        } else {


          await locateGame();
        }
      }
    );




  $("game-player-name-save")
    ?.addEventListener(
      "click",
      saveGamePlayerName
    );




  $("land-buy")
    ?.addEventListener(
      "click",
      buySelectedLand
    );




  $("notification-read")
    ?.addEventListener(
      "click",
      markNotificationsRead
    );
}




function setupTrips() {
  $("trip-start")
    ?.addEventListener(
      "click",
      startTrip
    );

  $("trip-stop")
    ?.addEventListener(
      "click",
      stopTrip
    );

  $("location-permission")
    ?.addEventListener(
      "click",
      async () => {
        showStatus(
          "history-status",
          "位置情報を確認しています..."
        );

        try {
          const position =
            await getCurrentPosition();

          setText(
            "trip-accuracy",
            `${Math.round(
              position.coords.accuracy
              ||
              0
            )} m`
          );

          initializeHistoryMap();

          historyMap?.setView(
            [
              position.coords.latitude,
              position.coords.longitude
            ],
            16
          );

          showStatus(
            "history-status",
            "位置情報を取得できました。"
          );

        } catch (
          error
        ) {
          showStatus(
            "history-status",
            error.message
            ||
            "位置情報を取得できませんでした。",
            true
          );
        }
      }
    );

  $("history-locate")
    ?.addEventListener(
      "click",
      async () => {
        try {
          const position =
            await getCurrentPosition();

          initializeHistoryMap();

          historyMap?.setView(
            [
              position.coords.latitude,
              position.coords.longitude
            ],
            16
          );

          setText(
            "trip-accuracy",
            `${Math.round(
              position.coords.accuracy
              ||
              0
            )} m`
          );

        } catch (
          error
        ) {
          showStatus(
            "history-status",
            error.message,
            true
          );
        }
      }
    );

  $("history-refresh")
    ?.addEventListener(
      "click",
      loadTrips
    );
}
function gameHash(
  text
) {


  let hash =
    2166136261;




  const value =
    String(
      text
    );




  for (
    let kinako = 0;
    kinako < value.length;
    kinako++
  ) {


    hash ^=
      value.charCodeAt(
        kinako
      );




    hash =
      Math.imul(
        hash,
        16777619
      );
  }




  return (
    hash
    >>>
    0
  );
}




/* =========================================================
  GeoJSON座標を全部取得
========================================================= */


function flattenCoordinates(
  coordinates,
  result = []
) {


  if (
    !Array.isArray(
      coordinates
    )
  ) {


    return result;
  }




  if (
    coordinates.length >= 2
    &&
    typeof coordinates[0] === "number"
    &&
    typeof coordinates[1] === "number"
  ) {


    result.push([
      coordinates[0],
      coordinates[1]
    ]);


    return result;
  }




  for (
    const item
    of
    coordinates
  ) {


    flattenCoordinates(
      item,
      result
    );
  }




  return result;
}




/* =========================================================
  建物固定ID
========================================================= */


function buildingCellId(
  feature
) {


  if (
    feature?.id !== undefined
    &&
    feature?.id !== null
  ) {


    const numericId =
      Number(
        feature.id
      );




    if (
      Number.isFinite(
        numericId
      )
    ) {


      return (
        "osm:way:"
        +
        Math.abs(
          Math.trunc(
            numericId
          )
        )
      );
    }
  }




  const points =
    flattenCoordinates(
      feature?.geometry?.coordinates
    );




  if (!points.length) {


    return (
      "osm:way:"
      +
      gameHash(
        JSON.stringify(
          feature?.geometry
          ||
          {}
        )
      )
    );
  }




  let minLon =
    Infinity;


  let maxLon =
    -Infinity;


  let minLat =
    Infinity;


  let maxLat =
    -Infinity;




  for (
    const point
    of
    points
  ) {


    minLon =
      Math.min(
        minLon,
        point[0]
      );


    maxLon =
      Math.max(
        maxLon,
        point[0]
      );


    minLat =
      Math.min(
        minLat,
        point[1]
      );


    maxLat =
      Math.max(
        maxLat,
        point[1]
      );
  }




  const key = [
    minLat.toFixed(
      6
    ),
    minLon.toFixed(
      6
    ),
    maxLat.toFixed(
      6
    ),
    maxLon.toFixed(
      6
    )
  ].join(
    ":"
  );




  return (
    "osm:way:"
    +
    gameHash(
      key
    )
  );
}




/* =========================================================
  グリッド土地
========================================================= */


function gridLandFromPoint(
  latitude,
  longitude
) {


  const row =
    Math.floor(
      (
        Number(
          latitude
        )
        +
        90
      )
      /
      GAME_GRID_DEGREES
    );




  const col =
    Math.floor(
      (
        Number(
          longitude
        )
        +
        180
      )
      /
      GAME_GRID_DEGREES
    );




  const south =
    (
      row
      *
      GAME_GRID_DEGREES
    )
    -
    90;




  const north =
    south
    +
    GAME_GRID_DEGREES;




  const west =
    (
      col
      *
      GAME_GRID_DEGREES
    )
    -
    180;




  const east =
    west
    +
    GAME_GRID_DEGREES;




  return {


    cell_id:
      `grid:${row}:${col}`,


    latitude:
      (
        south
        +
        north
      )
      /
      2,


    longitude:
      (
        west
        +
        east
      )
      /
      2,


    south:
      south,


    north:
      north,


    west:
      west,


    east:
      east,


    polygon: [
      [
        south,
        west
      ],
      [
        south,
        east
      ],
      [
        north,
        east
      ],
      [
        north,
        west
      ],
      [
        south,
        west
      ]
    ]
  };
}




/* =========================================================
  距離
========================================================= */


function conquestDistanceMeters(
  lat1,
  lon1,
  lat2,
  lon2
) {


  const earth =
    6371000;




  const p1 =
    lat1
    *
    Math.PI
    /
    180;




  const p2 =
    lat2
    *
    Math.PI
    /
    180;




  const dp =
    (
      lat2
      -
      lat1
    )
    *
    Math.PI
    /
    180;




  const dl =
    (
      lon2
      -
      lon1
    )
    *
    Math.PI
    /
    180;




  const kinako =
    Math.sin(
      dp / 2
    )
    ** 2
    +
    Math.cos(
      p1
    )
    *
    Math.cos(
      p2
    )
    *
    Math.sin(
      dl / 2
    )
    ** 2;




  return (
    earth
    *
    2
    *
    Math.atan2(
      Math.sqrt(
        kinako
      ),
      Math.sqrt(
        1
        -
        kinako
      )
    )
  );
}




/* =========================================================
  土地価格
========================================================= */


function conquestLandPrice(
  type
) {


  const table = {


    station_major:
      5000,


    station:
      3500,


    mall:
      4000,


    supermarket:
      2500,


    hotel:
      3000,


    hospital:
      3000,


    restaurant:
      1500,


    commercial:
      1800,


    office:
      1500,


    residential:
      1000,


    park:
      1200,


    normal:
      800
  };




  return (
    table[
      type
    ]
    ??
    1000
  );
}




/* =========================================================
  1日収益
========================================================= */


function conquestLandIncome(
  distance,
  type
) {


  let income;




  if (
    distance <= 100
  ) {


    income =
      40;


  } else if (
    distance <= 300
  ) {


    income =
      30;


  } else if (
    distance <= 500
  ) {


    income =
      22;


  } else if (
    distance <= 1000
  ) {


    income =
      15;


  } else if (
    distance <= 2000
  ) {


    income =
      10;


  } else {


    income =
      6;
  }




  if (
    type === "mall"
  ) {


    income =
      Math.max(
        40,
        income
      );
  }




  return income;
}




/* =========================================================
  POI分類


  静岡駅・駅
  アピタ・イオン・ららぽーと等
========================================================= */


function classifyConquestPoi(
  feature
) {


  const properties =
    feature?.properties
    ||
    {};




  const name =
    String(
      properties[
        "name:ja"
      ]
      ||
      properties.name
      ||
      properties.name_en
      ||
      ""
    );




  const lower =
    name.toLowerCase();




  const className =
    String(
      properties.class
      ||
      ""
    ).toLowerCase();




  const subclass =
    String(
      properties.subclass
      ||
      ""
    ).toLowerCase();




  if (
    className === "railway"
    ||
    subclass.includes(
      "station"
    )
    ||
    lower.endsWith(
      "駅"
    )
  ) {


    return {
      name:
        name || "駅",


      type:
        "station"
    };
  }




  const mallWords = [
    "アピタ",
    "apita",
    "イオン",
    "aeon",
    "ららぽーと",
    "lalaport",
    "アウトレット",
    "outlet",
    "parco",
    "パルコ",
    "伊勢丹",
    "isetan",
    "高島屋",
    "takashimaya",
    "松坂屋",
    "matsuzakaya"
  ];




  if (
    mallWords.some(
      word =>
        lower.includes(
          word.toLowerCase()
        )
    )
    ||
    subclass === "mall"
    ||
    subclass === "department_store"
  ) {


    return {
      name:
        name || "大型商業施設",


      type:
        "mall"
    };
  }




  if (
    subclass === "supermarket"
    ||
    className === "grocery"
  ) {


    return {
      name:
        name || "スーパーマーケット",


      type:
        "supermarket"
    };
  }




  if (
    className === "hospital"
    ||
    subclass === "hospital"
  ) {


    return {
      name:
        name || "病院",


      type:
        "hospital"
    };
  }




  if (
    className === "lodging"
    ||
    subclass === "hotel"
  ) {


    return {
      name:
        name || "ホテル",


      type:
        "hotel"
    };
  }




  if (
    [
      "restaurant",
      "cafe",
      "fast_food"
    ].includes(
      subclass
    )
  ) {


    return {
      name:
        name || "飲食店",


      type:
        "restaurant"
    };
  }




  if (
    className === "shop"
    ||
    className === "grocery"
  ) {


    return {
      name:
        name || "商業施設",


      type:
        "commercial"
    };
  }




  return {
    name:
      name || "建物",


    type:
      "normal"
  };
}




/* =========================================================
  近くのPOI
========================================================= */


function nearestConquestPoi(
  point
) {


  if (
    !conquestVectorReady
    ||
    !conquestVectorMap
    ||
    !conquestVectorMap.getLayer(
      "travel-game-poi-hit"
    )
  ) {


    return null;
  }




  try {


    const range =
      55;




    const features =
      conquestVectorMap
        .queryRenderedFeatures(
          [
            [
              point.x
              -
              range,
              point.y
              -
              range
            ],
            [
              point.x
              +
              range,
              point.y
              +
              range
            ]
          ],
          {
            layers: [
              "travel-game-poi-hit"
            ]
          }
        );




    const named =
      features.filter(
        feature => {


          const properties =
            feature.properties
            ||
            {};




          return Boolean(
            properties[
              "name:ja"
            ]
            ||
            properties.name
            ||
            properties.name_en
          );
        }
      );




    return (
      named[0]
      ||
      null
    );


  } catch {


    return null;
  }
}




/* =========================================================
  最寄り駅距離
========================================================= */


function nearestStationDistance(
  latitude,
  longitude
) {


  if (
    !conquestVectorReady
    ||
    !conquestVectorMap
    ||
    !conquestVectorMap.getLayer(
      "travel-game-poi-hit"
    )
  ) {


    return 2500;
  }




  try {


    const canvas =
      conquestVectorMap.getCanvas();




    const features =
      conquestVectorMap
        .queryRenderedFeatures(
          [
            [
              0,
              0
            ],
            [
              canvas.clientWidth,
              canvas.clientHeight
            ]
          ],
          {
            layers: [
              "travel-game-poi-hit"
            ]
          }
        );




    let answer =
      Infinity;




    for (
      const feature
      of
      features
    ) {


      const info =
        classifyConquestPoi(
          feature
        );




      if (
        info.type
        !==
        "station"
      ) {


        continue;
      }




      const coordinates =
        feature?.geometry?.coordinates;




      if (
        !Array.isArray(
          coordinates
        )
        ||
        typeof coordinates[0]
        !==
        "number"
      ) {


        continue;
      }




      const distance =
        conquestDistanceMeters(
          latitude,
          longitude,
          coordinates[1],
          coordinates[0]
        );




      answer =
        Math.min(
          answer,
          distance
        );
    }




    return (
      Number.isFinite(
        answer
      )
        ?
        answer
        :
        2500
    );


  } catch {


    return 2500;
  }
}




/* =========================================================
  世界グリッド表示
========================================================= */
function renderConquestWorldGrid() {


  if (
    !conquestMap
  ) {


    return;
  }




  if (
    !conquestGridLayer
  ) {


    conquestGridLayer =
      L.layerGroup()
        .addTo(
          conquestMap
        );


  } else {


    conquestGridLayer
      .clearLayers();
  }




  const zoom =
    conquestMap.getZoom();




  /*
    遠くまでズームアウトした時に
    線が数万本になるのを防ぐ。
    土地購入は詳細表示時に行う。
  */


  if (
    zoom < 14
  ) {


    return;
  }




  const bounds =
    conquestMap.getBounds();




  const south =
    bounds.getSouth();




  const north =
    bounds.getNorth();




  const west =
    bounds.getWest();




  const east =
    bounds.getEast();




  const firstLat =
    Math.floor(
      south
      /
      GAME_GRID_DEGREES
    )
    *
    GAME_GRID_DEGREES;




  const firstLon =
    Math.floor(
      west
      /
      GAME_GRID_DEGREES
    )
    *
    GAME_GRID_DEGREES;




  const lineOptions = {


    color:
      "#66788b",


    weight:
      1,


    opacity:
      0.38,


    interactive:
      false
  };




  let lineCount =
    0;




  for (
    let latitude =
      firstLat;


    latitude <=
    north
    +
    GAME_GRID_DEGREES;


    latitude +=
    GAME_GRID_DEGREES
  ) {


    if (
      lineCount
      >
      900
    ) {


      break;
    }




    L.polyline(
      [
        [
          latitude,
          west
        ],
        [
          latitude,
          east
        ]
      ],
      lineOptions
    ).addTo(
      conquestGridLayer
    );




    lineCount++;
  }




  for (
    let longitude =
      firstLon;


    longitude <=
    east
    +
    GAME_GRID_DEGREES;


    longitude +=
    GAME_GRID_DEGREES
  ) {


    if (
      lineCount
      >
      1800
    ) {


      break;
    }




    L.polyline(
      [
        [
          south,
          longitude
        ],
        [
          north,
          longitude
        ]
      ],
      lineOptions
    ).addTo(
      conquestGridLayer
    );
}    
}
/* =========================================================
  購入済み通常区画を塗る
========================================================= */


function renderConquestOwnedGrid() {


  if (
    !conquestMap
  ) {


    return;
  }




  if (
    !conquestGridOwnershipLayer
  ) {


    conquestGridOwnershipLayer =
      L.layerGroup()
        .addTo(
          conquestMap
        );


  } else {


    conquestGridOwnershipLayer
      .clearLayers();
  }




  for (
    const land
    of
    conquestOwnership.values()
  ) {


    if (
      !String(
        land.cell_id
      ).startsWith(
        "grid:"
      )
    ) {


      continue;
    }




    const parts =
      String(
        land.cell_id
      ).split(
        ":"
      );




    if (
      parts.length
      !==
      3
    ) {


      continue;
    }




    const row =
      Number(
        parts[1]
      );




    const col =
      Number(
        parts[2]
      );




    if (
      !Number.isFinite(
        row
      )
      ||
      !Number.isFinite(
        col
      )
    ) {


      continue;
    }




    const south =
      (
        row
        *
        GAME_GRID_DEGREES
      )
      -
      90;




    const north =
      south
      +
      GAME_GRID_DEGREES;




    const west =
      (
        col
        *
        GAME_GRID_DEGREES
      )
      -
      180;




    const east =
      west
      +
      GAME_GRID_DEGREES;




    const mine =
      Boolean(
        land.mine
      );




    const color =
      mine
        ?
        "#3388ff"
        :
        "#ef5368";




    L.rectangle(
      [
        [
          south,
          west
        ],
        [
          north,
          east
        ]
      ],
      {
        color:
          color,


        fillColor:
          color,


        fillOpacity:
          0.42,


        weight:
          2,


        interactive:
          false
      }
    ).addTo(
      conquestGridOwnershipLayer
    );
  }
}




/* =========================================================
  購入済み建物の色
========================================================= */







/* =========================================================
  MapLibre建物レイヤー
========================================================= */
/* =========================================================
  所有済み土地を現在の地物と照合
========================================================= */


function conquestPointInRing(
  longitude,
  latitude,
  ring
) {


  if (
    !Array.isArray(ring)
    ||
    ring.length < 3
  ) {
    return false;
  }


  let inside =
    false;


  for (
    let kinako = 0,
      kenako = ring.length - 1;
    kinako < ring.length;
    kenako = kinako++
  ) {


    const x1 =
      Number(
        ring[kinako]?.[0]
      );


    const y1 =
      Number(
        ring[kinako]?.[1]
      );


    const x2 =
      Number(
        ring[kenako]?.[0]
      );


    const y2 =
      Number(
        ring[kenako]?.[1]
      );


    if (
      !Number.isFinite(x1)
      ||
      !Number.isFinite(y1)
      ||
      !Number.isFinite(x2)
      ||
      !Number.isFinite(y2)
    ) {
      continue;
    }


    const intersect =
      (
        (y1 > latitude)
        !==
        (y2 > latitude)
      )
      &&
      (
        longitude
        <
        (
          (x2 - x1)
          *
          (latitude - y1)
          /
          (
            (y2 - y1)
            ||
            0.0000000001
          )
          +
          x1
        )
      );


    if (
      intersect
    ) {
      inside =
        !inside;
    }
  }


  return inside;
}




function conquestFeatureContainsPoint(
  feature,
  latitude,
  longitude
) {


  const geometry =
    feature?.geometry;


  if (!geometry) {
    return false;
  }


  if (
    geometry.type ===
    "Polygon"
  ) {


    return (
      geometry.coordinates
        ?.some(
          ring =>
            conquestPointInRing(
              longitude,
              latitude,
              ring
            )
        )
      ||
      false
    );
  }


  if (
    geometry.type ===
    "MultiPolygon"
  ) {


    for (
      const polygon
      of geometry.coordinates
      ||
      []
    ) {


      for (
        const ring
        of polygon
        ||
        []
      ) {


        if (
          conquestPointInRing(
            longitude,
            latitude,
            ring
          )
        ) {
          return true;
        }
      }
    }
  }


  return false;
}




/* =========================================================
  DB上の所有地を探す


  1. cell_id完全一致
  2. 以前のOSM IDでも、保存座標が現在の建物内なら同じ土地
  3. POIの場合は近距離照合
========================================================= */


function findConquestOwnedLand(
  cellId,
  feature,
  latitude,
  longitude
) {


  if (
    !(conquestOwnership instanceof Map)
  ) {
    return null;
  }


  const exact =
    conquestOwnership.get(
      cellId
    );


  if (
    exact
  ) {
    return exact;
  }


  let nearest =
    null;


  let nearestDistance =
    Infinity;


  for (
    const land
    of conquestOwnership.values()
  ) {


    const landLatitude =
      Number(
        land.latitude
        ??
        land.lat
      );


    const landLongitude =
      Number(
        land.longitude
        ??
        land.lon
      );


    if (
      !Number.isFinite(
        landLatitude
      )
      ||
      !Number.isFinite(
        landLongitude
      )
    ) {
      continue;
    }


    /*
     * 建物・公園・大学などなら
     * DBに保存された座標が現在のポリゴン内か確認
     */


    if (
      feature
      &&
      conquestFeatureContainsPoint(
        feature,
        landLatitude,
        landLongitude
      )
    ) {


      const distance =
        conquestMeters(
          latitude,
          longitude,
          landLatitude,
          landLongitude
        );


      if (
        distance <
        nearestDistance
      ) {


        nearest =
          land;


        nearestDistance =
          distance;
      }


      continue;
    }


    /*
     * 駅POIなどポイント地物
     */


    if (
      feature?.geometry?.type
      ===
      "Point"
    ) {


      const distance =
        conquestMeters(
          latitude,
          longitude,
          landLatitude,
          landLongitude
        );


      if (
        distance <= 35
        &&
        distance <
        nearestDistance
      ) {


        nearest =
          land;


        nearestDistance =
          distance;
      }
    }
  }


  return nearest;
}




/* =========================================================
  所有土地の色


  自分 = 青
  他人 = 赤
========================================================= */
function refreshConquestOwnedBuildings() {


  if (
    !conquestVectorReady
    ||
    !conquestVectorMap
  ) {
    return;
  }


  const layerIds = [
    "travel-game-facility-fill",
    "travel-game-park-fill",
    "travel-game-building-fill"
  ].filter(
    kinako =>
      conquestVectorMap.getLayer(
        kinako
      )
  );


  if (
    !layerIds.length
  ) {
    return;
  }


  const visibleFeatures =
    conquestVectorMap
      .queryRenderedFeatures(
        undefined,
        {
          layers:
            layerIds
        }
      )
    ||
    [];


  const ownedFeatures =
    [];


  const used =
    new Set();


  for (
    const feature
    of visibleFeatures
  ) {


    if (
      !feature?.geometry
    ) {
      continue;
    }


    /*
     * 地物中心の目安
     */


    let latitude =
      null;


    let longitude =
      null;


    const coordinates =
      feature.geometry
        .coordinates;


    function findCoordinate(
      value
    ) {


      if (
        latitude !== null
      ) {
        return;
      }


      if (
        Array.isArray(value)
        &&
        value.length >= 2
        &&
        Number.isFinite(
          Number(
            value[0]
          )
        )
        &&
        Number.isFinite(
          Number(
            value[1]
          )
        )
      ) {


        longitude =
          Number(
            value[0]
          );


        latitude =
          Number(
            value[1]
          );


        return;
      }


      if (
        Array.isArray(value)
      ) {


        for (
          const kinako
          of value
        ) {


          findCoordinate(
            kinako
          );


          if (
            latitude !== null
          ) {
            break;
          }
        }
      }
    }


    findCoordinate(
      coordinates
    );


    if (
      latitude === null
      ||
      longitude === null
    ) {
      continue;
    }


    const landType =
      conquestFeatureType(
        feature
      );


    const cellId =
      conquestFeatureCellId(
        feature,
        landType,
        latitude,
        longitude
      );


    const owned =
      findConquestOwnedLand(
        cellId,
        feature,
        latitude,
        longitude
      );


    if (
      !owned
    ) {
      continue;
    }


    const key =
      owned.cell_id
      ||
      owned.cell
      ||
      cellId;


    if (
      used.has(key)
    ) {
      continue;
    }


    used.add(
      key
    );


    ownedFeatures.push({
      type:
        "Feature",


      properties: {
        mine:
          Boolean(
            owned.mine
          )
      },


      geometry:
        feature.geometry
    });
  }




  const geojson = {
    type:
      "FeatureCollection",


    features:
      ownedFeatures
  };




  const sourceId =
    "travel-game-owned-source";




  if (
    conquestVectorMap.getSource(
      sourceId
    )
  ) {


    conquestVectorMap
      .getSource(
        sourceId
      )
      .setData(
        geojson
      );


    return;
  }




  conquestVectorMap.addSource(
    sourceId,
    {
      type:
        "geojson",


      data:
        geojson
    }
  );




  conquestVectorMap.addLayer({
    id:
      "travel-game-owned-fill",


    type:
      "fill",


    source:
      sourceId,


    paint: {


      "fill-color": [
        "case",


        [
          "==",
          [
            "get",
            "mine"
          ],
          true
        ],


        "#3388ff",


        "#ef5368"
      ],


      "fill-opacity":
        0.48
    }
  });




  conquestVectorMap.addLayer({
    id:
      "travel-game-owned-line",


    type:
      "line",


    source:
      sourceId,


    paint: {


      "line-color": [
        "case",


        [
          "==",
          [
            "get",
            "mine"
          ],
          true
        ],


        "#1769ff",


        "#ff334f"
      ],


      "line-width":
        2.5
    }
  });
}
function setupConquestVectorMap() {


  if (
    conquestVectorLayer
    ||
    !conquestMap
  ) {
    return;
  }


  if (
    !window.maplibregl
    ||
    !L.maplibreGL
  ) {
    console.warn(
      "MapLibreを読み込めませんでした。"
    );
    return;
  }


  conquestVectorReady =
    false;


  conquestVectorLayer =
    L.maplibreGL({
      style:
        "https://tiles.openfreemap.org/styles/liberty",
      interactive:
        false
    });


  conquestVectorLayer.addTo(
    conquestMap
  );


  conquestVectorMap =
    conquestVectorLayer
      .getMaplibreMap();


  conquestVectorMap.on(
    "load",
    () => {


      const style =
        conquestVectorMap.getStyle();


      /*
       * 元のMapLibre表示は隠す。
       * Leafletの地図を背景として残す。
       */
      for (
        const layer
        of style.layers || []
      ) {


        try {


          if (
            layer.type ===
            "background"
          ) {


            conquestVectorMap
              .setPaintProperty(
                layer.id,
                "background-opacity",
                0
              );


          } else {


            conquestVectorMap
              .setLayoutProperty(
                layer.id,
                "visibility",
                "none"
              );
          }


        } catch (
          error
        ) {


          console.debug(
            error
          );
        }
      }


      /*
       * =========================================
       * OpenStreetMapベクターレイヤーを探す
       * =========================================
       */


      const findLayer =
        sourceLayerName => {


          return (
            style.layers || []
          ).find(
            layer =>
              layer[
                "source-layer"
              ] ===
              sourceLayerName
          );
        };




      /*
       * =========================================
       * 1. 建物
       * 1棟 = 1土地
       * =========================================
       */


      const building =
        findLayer(
          "building"
        );


      if (
        building
        &&
        building.source
      ) {


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-building-fill",


            type:
              "fill",


            source:
              building.source,


            "source-layer":
              "building",


            paint: {
              "fill-color":
                "#7d8b99",


              "fill-opacity":
                0.20
            }
          });


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-building-line",


            type:
              "line",


            source:
              building.source,


            "source-layer":
              "building",


            paint: {
              "line-color":
                "#aebac6",


              "line-width":
                1.2,


              "line-opacity":
                0.9
            }
          });
      }




      /*
       * =========================================
       * 2. 大学・学校・病院・商業施設
       * 敷地全体 = 1土地
       * =========================================
       */


      const landuse =
        findLayer(
          "landuse"
        );


      if (
        landuse
        &&
        landuse.source
      ) {


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-facility-fill",


            type:
              "fill",


            source:
              landuse.source,


            "source-layer":
              "landuse",


            filter: [
              "match",
              [
                "get",
                "class"
              ],
              [
                "university",
                "college",
                "school",
                "hospital",
                "commercial",
                "retail"
              ],
              true,
              false
            ],


            paint: {
              "fill-color": [
                "match",


                [
                  "get",
                  "class"
                ],


                "university",
                "#22c55e",


                "college",
                "#22c55e",


                "school",
                "#34d399",


                "hospital",
                "#ef4444",


                "commercial",
                "#f59e0b",


                "retail",
                "#f59e0b",


                "#7d8b99"
              ],


              "fill-opacity":
                0.28
            }
          });


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-facility-line",


            type:
              "line",


            source:
              landuse.source,


            "source-layer":
              "landuse",


            filter: [
              "match",
              [
                "get",
                "class"
              ],
              [
                "university",
                "college",
                "school",
                "hospital",
                "commercial",
                "retail"
              ],
              true,
              false
            ],


            paint: {
              "line-color":
                "#dbeafe",


              "line-width":
                1.6
            }
          });
      }




      /*
       * =========================================
       * 3. 公園
       * 公園全体 = 1土地
       * =========================================
       */


      const park =
        findLayer(
          "park"
        );


      if (
        park
        &&
        park.source
      ) {


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-park-fill",


            type:
              "fill",


            source:
              park.source,


            "source-layer":
              "park",


            paint: {
              "fill-color":
                "#22c55e",


              "fill-opacity":
                0.25
            }
          });


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-park-line",


            type:
              "line",


            source:
              park.source,


            "source-layer":
              "park",


            paint: {
              "line-color":
                "#4ade80",


              "line-width":
                1.5
            }
          });
      }




      /*
       * =========================================
       * 4. POI
       * 駅・ショッピングモール等の判定用
       * 画面には表示しない
       * =========================================
       */


      const poi =
        findLayer(
          "poi"
        );


      if (
        poi
        &&
        poi.source
      ) {


        conquestVectorMap
          .addLayer({
            id:
              "travel-game-poi-hit",


            type:
              "circle",


            source:
              poi.source,


            "source-layer":
              "poi",


            paint: {
              "circle-radius":
                18,


              "circle-opacity":
                0
            }
          });
      }




      conquestVectorReady =
        true;


      /*
       * 所有済み建物の色を反映
       */
      refreshConquestOwnedBuildings();


      console.log(
        "Travel Life world land map ready"
      );
    }
  );
}






/* =========================================================
  地図を押した時
========================================================= */


function conquestSetStatus(
  message,
  error = false
) {
  if (
    typeof showStatus ===
    "function"
  ) {
    showStatus(
      "conquest-status",
      message,
      error
    );
    return;
  }


  if (
    typeof status ===
    "function"
  ) {
    status(
      "conquest-status",
      message,
      error
    );
  }
}




/* =========================================================
  地物の文字情報
========================================================= */
function conquestFeatureText(
  feature
) {


  const properties =
    feature?.properties
    ||
    {};


  return String(
    properties[
      "name:ja"
    ]
    ||
    properties.name
    ||
    properties.name_en
    ||
    properties.ref
    ||
    ""
  ).trim();
}




/* =========================================================
  地物タイプ判定
========================================================= */


function conquestFeatureType(
  feature
) {


  const properties =
    feature?.properties
    ||
    {};


  const sourceLayer =
    String(
      feature?.sourceLayer
      ||
      feature?.layer?.[
        "source-layer"
      ]
      ||
      ""
    ).toLowerCase();


  const className =
    String(
      properties.class
      ||
      ""
    ).toLowerCase();


  const subclass =
    String(
      properties.subclass
      ||
      ""
    ).toLowerCase();


  const name =
    conquestFeatureText(
      feature
    ).toLowerCase();


  if (
    sourceLayer ===
    "park"
  ) {


    return "park";
  }


  if (
    className ===
    "university"
    ||
    subclass ===
    "university"
  ) {


    return "university";
  }


  if (
    className ===
    "college"
    ||
    subclass ===
    "college"
  ) {


    return "university";
  }


  if (
    className ===
    "school"
    ||
    subclass ===
    "school"
  ) {


    return "school";
  }


  if (
    className ===
    "hospital"
    ||
    subclass ===
    "hospital"
  ) {


    return "hospital";
  }


  if (
    className ===
    "commercial"
    ||
    className ===
    "retail"
  ) {


    return "commercial";
  }


  if (
    subclass ===
    "mall"
    ||
    subclass ===
    "department_store"
  ) {


    return "mall";
  }


  if (
    subclass ===
    "supermarket"
  ) {


    return "supermarket";
  }


  if (
    subclass ===
    "hotel"
  ) {


    return "hotel";
  }


  if (
    [
      "restaurant",
      "cafe",
      "fast_food"
    ].includes(
      subclass
    )
  ) {


    return "restaurant";
  }


  if (
    sourceLayer ===
    "building"
  ) {


    return "building";
  }


  if (
    name.endsWith(
      "駅"
    )
    ||
    subclass.includes(
      "station"
    )
  ) {


    return "station";
  }


  return "normal";
}




function conquestTypeName(
  type
) {


  const names = {


    building:
      "建物",


    park:
      "公園",


    university:
      "大学",


    school:
      "学校",


    hospital:
      "病院",


    commercial:
      "商業施設",


    mall:
      "大型商業施設",


    supermarket:
      "スーパーマーケット",


    hotel:
      "ホテル",


    restaurant:
      "飲食店",


    station:
      "駅",


    normal:
      "土地"
  };


  return (
    names[
      type
    ]
    ||
    "土地"
  );
}




/* =========================================================
  安定した地物ハッシュ
========================================================= */


function conquestStableHash(
  value
) {


  const text =
    String(
      value
    );


  let hash =
    2166136261;


  for (
    let kinako = 0;
    kinako < text.length;
    kinako++
  ) {


    hash ^=
      text.charCodeAt(
        kinako
      );


    hash =
      Math.imul(
        hash,
        16777619
      );
  }


  return (
    hash
    >>>
    0
  );
}




/* =========================================================
  地物を購入保存用polygonへ変換
========================================================= */


function conquestFeaturePolygon(
  feature
) {


  const geometry =
    feature?.geometry;


  if (
    !geometry
  ) {


    return [];
  }


  if (
    geometry.type ===
    "Polygon"
  ) {


    const ring =
      geometry.coordinates
        ?.[0]
      ||
      [];


    return ring
      .map(
        point => {


          if (
            !Array.isArray(
              point
            )
            ||
            point.length < 2
          ) {


            return null;
          }


          return [
            Number(
              point[1]
            ),
            Number(
              point[0]
            )
          ];
        }
      )
      .filter(
        point =>
          Number.isFinite(
            point?.[0]
          )
          &&
          Number.isFinite(
            point?.[1]
          )
      );
  }


  if (
    geometry.type ===
    "MultiPolygon"
  ) {


    const ring =
      geometry.coordinates
        ?.[0]
        ?.[0]
      ||
      [];


    return ring
      .map(
        point => {


          if (
            !Array.isArray(
              point
            )
            ||
            point.length < 2
          ) {


            return null;
          }


          return [
            Number(
              point[1]
            ),
            Number(
              point[0]
            )
          ];
        }
      )
      .filter(
        point =>
          Number.isFinite(
            point?.[0]
          )
          &&
          Number.isFinite(
            point?.[1]
          )
      );
  }


  return [];
}




/* =========================================================
  地物cell_id
========================================================= */


function conquestFeatureCellId(
  feature,
  type,
  latitude,
  longitude
) {


  const properties =
    feature?.properties
    ||
    {};


  const sourceLayer =
    String(
      feature?.sourceLayer
      ||
      feature?.layer?.[
        "source-layer"
      ]
      ||
      "land"
    );


  const rawId =
    feature?.id
    ??
    properties.osm_id
    ??
    properties.id;


  if (
    rawId !== null
    &&
    rawId !== undefined
    &&
    String(
      rawId
    ).trim()
  ) {


    return [
      "osm",
      sourceLayer,
      String(
        rawId
      )
    ].join(
      ":"
    );
  }


  const polygon =
    conquestFeaturePolygon(
      feature
    );


  if (
    polygon.length
  ) {


    const key =
      polygon
        .map(
          point =>
            `${Number(
              point[0]
            ).toFixed(
              6
            )},${Number(
              point[1]
            ).toFixed(
              6
            )}`
        )
        .join(
          "|"
        );


    return [
      "osm",
      sourceLayer,
      conquestStableHash(
        key
      )
    ].join(
      ":"
    );
  }


  return [
    "poi",
    type,
    Number(
      latitude
    ).toFixed(
      5
    ),
    Number(
      longitude
    ).toFixed(
      5
    )
  ].join(
    ":"
  );
}




/* =========================================================
  2地点間距離
========================================================= */


function conquestMeters(
  lat1,
  lon1,
  lat2,
  lon2
) {


  const earthRadius =
    6371000;


  const phi1 =
    Number(
      lat1
    )
    *
    Math.PI
    /
    180;


  const phi2 =
    Number(
      lat2
    )
    *
    Math.PI
    /
    180;


  const deltaPhi =
    (
      Number(
        lat2
      )
      -
      Number(
        lat1
      )
    )
    *
    Math.PI
    /
    180;


  const deltaLambda =
    (
      Number(
        lon2
      )
      -
      Number(
        lon1
      )
    )
    *
    Math.PI
    /
    180;


  const kinako =
    Math.sin(
      deltaPhi
      /
      2
    )
    **
    2
    +
    Math.cos(
      phi1
    )
    *
    Math.cos(
      phi2
    )
    *
    Math.sin(
      deltaLambda
      /
      2
    )
    **
    2;


  const kenako =
    2
    *
    Math.atan2(
      Math.sqrt(
        kinako
      ),
      Math.sqrt(
        1
        -
        kinako
      )
    );


  return (
    earthRadius
    *
    kenako
  );
}




/* =========================================================
  駅距離
========================================================= */


function conquestStationDistance(
  latitude,
  longitude
) {


  if (
    !conquestVectorReady
    ||
    !conquestVectorMap
  ) {


    return 2500;
  }


  const layer =
    "travel-game-poi-hit";


  if (
    !conquestVectorMap.getLayer(
      layer
    )
  ) {


    return 2500;
  }


  let features;


  try {


    features =
      conquestVectorMap
        .queryRenderedFeatures(
          undefined,
          {
            layers: [
              layer
            ]
          }
        );


  } catch {


    return 2500;
  }


  let nearest =
    Infinity;


  for (
    const feature
    of features
    ||
    []
  ) {


    const type =
      conquestFeatureType(
        feature
      );


    if (
      type !==
      "station"
    ) {


      continue;
    }


    const coordinates =
      feature?.geometry
        ?.coordinates;


    if (
      !Array.isArray(
        coordinates
      )
      ||
      !Number.isFinite(
        Number(
          coordinates[0]
        )
      )
      ||
      !Number.isFinite(
        Number(
          coordinates[1]
        )
      )
    ) {


      continue;
    }


    const distance =
      conquestMeters(
        latitude,
        longitude,
        Number(
          coordinates[1]
        ),
        Number(
          coordinates[0]
        )
      );


    nearest =
      Math.min(
        nearest,
        distance
      );
  }


  return (
    Number.isFinite(
      nearest
    )
      ?
      nearest
      :
      2500
  );
}




/* =========================================================
  土地価格
========================================================= */


function conquestPrice(
  type,
  stationDistance
) {


  const basePrices = {


    building:
      1000,


    park:
      1200,


    university:
      2600,


    school:
      1800,


    hospital:
      2800,


    commercial:
      2200,


    mall:
      4000,


    supermarket:
      2500,


    hotel:
      3000,


    restaurant:
      1500,


    station:
      3500,


    normal:
      1000
  };


  let price =
    basePrices[
      type
    ]
    ??
    1000;


  if (
    stationDistance <= 100
  ) {


    price +=
      1500;


  } else if (
    stationDistance <= 300
  ) {


    price +=
      1000;


  } else if (
    stationDistance <= 500
  ) {


    price +=
      700;


  } else if (
    stationDistance <= 1000
  ) {


    price +=
      400;
  }


  return Math.round(
    price
  );
}




/* =========================================================
  土地収益
========================================================= */


function conquestIncome(
  stationDistance,
  type
) {


  let income;


  if (
    stationDistance <= 100
  ) {


    income =
      40;


  } else if (
    stationDistance <= 300
  ) {


    income =
      30;


  } else if (
    stationDistance <= 500
  ) {


    income =
      22;


  } else if (
    stationDistance <= 1000
  ) {


    income =
      15;


  } else if (
    stationDistance <= 2000
  ) {


    income =
      10;


  } else {


    income =
      6;
  }


  const minimums = {


    mall:
      40,


    supermarket:
      25,


    university:
      25,


    hospital:
      25,


    commercial:
      20,


    hotel:
      20,


    restaurant:
      15,


    station:
      40
  };


  if (
    minimums[
      type
    ] !==
    undefined
  ) {


    income =
      Math.max(
        income,
        minimums[
          type
        ]
      );
  }


  return income;
}




/* =========================================================
  地図クリック処理
========================================================= */


function handleConquestWorldClick(
  event
) {


  if (
    !event
    ||
    !event.latlng
  ) {


    return;
  }


  const latitude =
    Number(
      event.latlng.lat
    );


  const longitude =
    Number(
      event.latlng.lng
    );


  if (
    !Number.isFinite(
      latitude
    )
    ||
    !Number.isFinite(
      longitude
    )
  ) {


    return;
  }


  if (
    !conquestVectorReady
    ||
    !conquestVectorMap
  ) {


    const gridLand =
      gridLandFromPoint(
        latitude,
        longitude
      );


    const stationDistance =
      2500;


    const type =
      "normal";


    const price =
      conquestPrice(
        type,
        stationDistance
      );


    const dailyIncome =
      conquestIncome(
        stationDistance,
        type
      );


    const owned =
      conquestOwnership.get(
        gridLand.cell_id
      );


    openLandPanel({
      ...gridLand,


      name:
        "通常区画",


      land_name:
        "通常区画",


      land_type:
        type,


      price:
        price,


      purchase_price:
        price,


      station_distance:
        stationDistance,


      daily_income:
        dailyIncome,


      owner_id:
        owned?.owner_id
        ??
        null,


      owner_name:
        owned?.owner_name
        ??
        null,


      mine:
        Boolean(
          owned?.mine
        )
    });


    return;
  }


  let point;


  try {


    point =
      conquestVectorMap.project([
        longitude,
        latitude
      ]);


  } catch {


    return;
  }


  const layerIds = [
    "travel-game-facility-fill",
    "travel-game-park-fill",
    "travel-game-building-fill",
    "travel-game-poi-hit"
  ].filter(
    layerId =>
      conquestVectorMap.getLayer(
        layerId
      )
  );


  let features = [];


  try {


    features =
      conquestVectorMap
        .queryRenderedFeatures(
          [
            [
              point.x - 5,
              point.y - 5
            ],
            [
              point.x + 5,
              point.y + 5
            ]
          ],
          {
            layers:
              layerIds
          }
        );


  } catch (
    error
  ) {


    console.error(
      "CONQUEST FEATURE ERROR:",
      error
    );
  }


  const priority = {


    "travel-game-facility-fill":
      1,


    "travel-game-park-fill":
      2,


    "travel-game-building-fill":
      3,


    "travel-game-poi-hit":
      4
  };


  features.sort(
    (
      kinako,
      kenako
    ) => {


      const first =
        priority[
          kinako.layer?.id
        ]
        ??
        99;


      const second =
        priority[
          kenako.layer?.id
        ]
        ??
        99;


      return (
        first
        -
        second
      );
    }
  );


  const feature =
    features[0]
    ||
    null;


  if (
    !feature
  ) {


    const gridLand =
      gridLandFromPoint(
        latitude,
        longitude
      );


    const stationDistance =
      conquestStationDistance(
        latitude,
        longitude
      );


    const type =
      "normal";


    const price =
      conquestPrice(
        type,
        stationDistance
      );


    const dailyIncome =
      conquestIncome(
        stationDistance,
        type
      );


    const owned =
      conquestOwnership.get(
        gridLand.cell_id
      );


    openLandPanel({
      ...gridLand,


      name:
        "通常区画",


      land_name:
        "通常区画",


      land_type:
        type,


      price:
        price,


      purchase_price:
        price,


      station_distance:
        stationDistance,


      daily_income:
        dailyIncome,


      owner_id:
        owned?.owner_id
        ??
        null,


      owner_name:
        owned?.owner_name
        ??
        null,


      mine:
        Boolean(
          owned?.mine
        )
    });


    return;
  }


  const type =
    conquestFeatureType(
      feature
    );


  const name =
    conquestFeatureText(
      feature
    )
    ||
    conquestTypeName(
      type
    );


  let featureLatitude =
    latitude;


  let featureLongitude =
    longitude;


  if (
    feature.geometry?.type ===
    "Point"
    &&
    Array.isArray(
      feature.geometry.coordinates
    )
  ) {


    featureLongitude =
      Number(
        feature.geometry.coordinates[0]
      );


    featureLatitude =
      Number(
        feature.geometry.coordinates[1]
      );
  }


  const cellId =
    conquestFeatureCellId(
      feature,
      type,
      featureLatitude,
      featureLongitude
    );


  const stationDistance =
    conquestStationDistance(
      featureLatitude,
      featureLongitude
    );


  const price =
    conquestPrice(
      type,
      stationDistance
    );


  const dailyIncome =
    conquestIncome(
      stationDistance,
      type
    );


  const polygon =
    conquestFeaturePolygon(
      feature
    );


  const owned =
    findConquestOwnedLand(
      cellId,
      feature,
      featureLatitude,
      featureLongitude
    );


  const properties =
    feature.properties
    ||
    {};


  const osmId =
    feature.id
    ??
    properties.osm_id
    ??
    properties.id
    ??
    null;


  const sourceLayer =
    feature.sourceLayer
    ||
    feature.layer?.[
      "source-layer"
    ]
    ||
    null;


  openLandPanel({
    cell_id:
      cellId,


    name:
      name,


    land_name:
      name,


    land_type:
      type,


    osm_type:
      sourceLayer,


    osm_id:
      osmId,


    polygon:
      polygon,


    polygon_json:
      polygon,


    latitude:
      featureLatitude,


    longitude:
      featureLongitude,


    center_lat:
      featureLatitude,


    center_lon:
      featureLongitude,


    station_distance:
      stationDistance,


    daily_income:
      dailyIncome,


    price:
      price,


    purchase_price:
      price,


    owner_id:
      owned?.owner_id
      ??
      null,


    owner_name:
      owned?.owner_name
      ??
      null,


    mine:
      Boolean(
        owned?.mine
      )
  });
}
async function loadGameMap(
  latitude,
  longitude
) {
  if (
    !conquestMap
  ) {
    return;
  }

  showStatus(
    "conquest-status",
    "周辺の土地を取得しています..."
  );

  try {
    const center =
      conquestMap.getCenter();

    let radius =
      500;

    try {
      const bounds =
        conquestMap.getBounds();

      radius =
        center.distanceTo(
          bounds.getNorthEast()
        );
    } catch (
      error
    ) {
      radius =
        500;
    }

    radius =
      Math.max(
        250,
        Math.min(
          radius,
          1200
        )
      );

    const params =
      new URLSearchParams({
        lat:
          Number.isFinite(
            Number(
              latitude
            )
          )
            ? String(
                latitude
              )
            : String(
                center.lat
              ),

        lon:
          Number.isFinite(
            Number(
              longitude
            )
          )
            ? String(
                longitude
              )
            : String(
                center.lng
              ),

        radius:
          String(
            Math.round(
              radius
            )
          )
      });

    const data =
      await requestJSON(
        `/api/game/map?${params.toString()}`,
        {},
        45000
      );

    const parcels =
      data.parcels
      ||
      data.lands
      ||
      [];

    currentGamePlayer =
      data.player
      ||
      currentGamePlayer;

    if (
      data.player
    ) {
      renderGamePlayer(
        data.player
      );
    }

    renderGameParcels(
      parcels
    );

    setText(
      "local-conquerors",
      countLocalPlayers(
        parcels
      )
    );

    showStatus(
      "conquest-status",
      parcels.length
        ? `${parcels.length}件の実在土地・施設を表示しています`
        : "この範囲では購入候補の土地が見つかりませんでした"
    );

  } catch (
    error
  ) {
    console.error(
      "GAME MAP ERROR:",
      error
    );

    showStatus(
      "conquest-status",
      error.message,
      true
    );
  }
}


/* =========================================================
  画面切り替え・初期化
========================================================= */

function activeScreen() {

 const element =
  document.querySelector(
   ".screen.active"
  );

 return element
  ? element.id
  : "";
}
function loadScreen() {
  const screen =
    activeScreen();

  switch (
    screen
  ) {
    case "currency-screen":
      loadRates();
      break;

    case "news-screen":
      loadNews();
      break;

    case "danger-screen":
      setTimeout(
        () => {
          loadDanger();
        },
        100
      );
      break;

    case "route-screen":
      break;

    case "life-screen":
      loadWeather();

      setTimeout(
        () => {
          loadRadar();
        },
        100
      );
      break;

    case "history-screen":
      loadGameSession()
        .catch(
          error => {
            console.error(
              "GAME SESSION:",
              error
            );
          }
        );

      loadTrips();
      break;

    case "conquest-screen":
      loadGame();
      break;
  }
}


function initialize() {


 console.log(
  "Travel Life initialize start"
 );




 // ==========================================
 // 1. 保存設定
 // ==========================================


 try {


  if (
   typeof loadLocalSettings ===
   "function"
  ) {


   loadLocalSettings();
  }


 } catch (error) {


  console.error(
   "LOCAL SETTINGS:",
   error
  );
 }




 // ==========================================
 // 2. 国検索
 // ==========================================


 try {


  if (
   typeof setupCountrySearch ===
   "function"
  ) {


   setupCountrySearch();
  }


 } catch (error) {


  console.error(
   "COUNTRY SEARCH:",
   error
  );
 }




 // ==========================================
 // 3. 街検索
 // ==========================================


 try {


  if (
   typeof setupCitySearch ===
   "function"
  ) {


   setupCitySearch();
  }


 } catch (error) {


  console.error(
   "CITY SEARCH:",
   error
  );
 }




 // ==========================================
 // 4. 国表示
 // ==========================================


 try {


  if (
   typeof updateCountryDisplay ===
   "function"
  ) {


   updateCountryDisplay();
  }


 } catch (error) {


  console.error(
   "COUNTRY DISPLAY:",
   error
  );
 }




 // ==========================================
 // 5. 為替
 // ==========================================


 try {


  if (
   typeof setupCurrency ===
   "function"
  ) {


   setupCurrency();
  }


 } catch (error) {


  console.error(
   "CURRENCY SETUP:",
   error
  );
 }




 // ==========================================
 // 6. 経路検索
 // ==========================================


 try {


  if (
   typeof setupRoute ===
   "function"
  ) {


   setupRoute();
  }


 } catch (error) {


  console.error(
   "ROUTE SETUP:",
   error
  );
 }




 // ==========================================
 // 7. ゲーム
 // ==========================================


 try {


  if (
   typeof setupGame ===
   "function"
  ) {


   setupGame();
  }


 } catch (error) {


  console.error(
   "GAME SETUP:",
   error
  );
 }




 try {


  if (
   typeof setupTrips ===
   "function"
  ) {


   setupTrips();
  }


 } catch (error) {


  console.error(
   "TRIP SETUP:",
   error
  );
 }




 // ==========================================
 // 8. 下部ナビ
 // ==========================================


 document
  .querySelectorAll(
   ".nav-button"
  )
  .forEach(
   button => {


    button.onclick =
     () => {


      const screenId =
       button.dataset.screen;


      const screen =
       document.getElementById(
        screenId
       );




      if (!screen) {


       console.error(
        "画面がありません:",
        screenId
       );


       return;
      }




      try {


       if (
        typeof stopRadar ===
        "function"
       ) {


        stopRadar();
       }


      } catch (error) {


       console.error(
        "RADAR STOP:",
        error
       );
      }




      document
       .querySelectorAll(
        ".screen"
       )
       .forEach(
        kinako => {


         kinako.classList.toggle(
          "active",
          kinako === screen
         );
        }
       );




      document
       .querySelectorAll(
        ".nav-button"
       )
       .forEach(
        kinako => {


         kinako.classList.toggle(
          "active",
          kinako === button
         );
        }
       );




      requestAnimationFrame(
       () => {


        try {


         if (
          typeof loadScreen ===
          "function"
         ) {


          loadScreen();
         }


        } catch (error) {


         console.error(
          "SCREEN LOAD:",
          error
         );
        }




        try {


         if (
          typeof dangerMap !==
          "undefined"
          &&
          dangerMap
         ) {


          dangerMap.invalidateSize();
         }


        } catch (error) {


         console.error(
          "DANGER MAP SIZE:",
          error
         );
        }




        try {


         if (
          typeof radarMap !==
          "undefined"
          &&
          radarMap
         ) {


          radarMap.invalidateSize();
         }


        } catch (error) {


         console.error(
          "RADAR MAP SIZE:",
          error
         );
        }




        try {


         if (
          typeof historyMap !==
          "undefined"
          &&
          historyMap
         ) {


          historyMap.invalidateSize();
         }


        } catch (error) {


         console.error(
          "HISTORY MAP SIZE:",
          error
         );
        }




        try {


         if (
          typeof conquestMap !==
          "undefined"
          &&
          conquestMap
         ) {


          conquestMap.invalidateSize();
         }


        } catch (error) {


         console.error(
          "CONQUEST MAP SIZE:",
          error
         );
        }
       }
      );
     };
   }
  );




 // ==========================================
 // 9. 雨雲レーダー
 // ==========================================


 const radarSlider =
  document.getElementById(
   "radar-slider"
  );




 if (
  radarSlider
  &&
  typeof showRadar ===
  "function"
 ) {


  radarSlider.oninput =
   showRadar;
 }




 const radarPlay =
  document.getElementById(
   "radar-play"
  );




 if (radarPlay) {


  radarPlay.onclick =
   async () => {


    try {


     if (
      typeof radarTimer !==
      "undefined"
      &&
      radarTimer
     ) {


      stopRadar();


      return;
     }




     if (
      !Array.isArray(
       radarFrames
      )
      ||
      radarFrames.length === 0
     ) {


      if (
       typeof loadRadar ===
       "function"
      ) {


       await loadRadar(
        true
       );
      }
     }




     if (
      !Array.isArray(
       radarFrames
      )
      ||
      radarFrames.length === 0
     ) {


      return;
     }




     radarPlay.textContent =
      "■ 停止";




     radarTimer =
      setInterval(
       () => {


        if (
         !radarSlider
        ) {


         return;
        }




        radarSlider.value =
         (
          Number(
           radarSlider.value
          )
          +
          1
         )
         %
         radarFrames.length;




        if (
         typeof showRadar ===
         "function"
        ) {


         showRadar();
        }


       },
       1000
      );


    } catch (error) {


     console.error(
      "RADAR PLAY:",
      error
     );
    }
   };
 }




 // ==========================================
 // 10. ゲームセッション
 // ==========================================


 try {


  if (
   typeof loadGameSession ===
   "function"
  ) {


   Promise
    .resolve(
     loadGameSession()
    )
    .catch(
     error => {


      console.error(
       "GAME SESSION:",
       error
      );
     }
    );
  }


 } catch (error) {


  console.error(
   "GAME SESSION START:",
   error
  );
 }




 // ==========================================
 // 11. 最初の画面
 // ==========================================


 requestAnimationFrame(
  () => {


   try {


    if (
     typeof loadScreen ===
     "function"
    ) {


     loadScreen();
    }


   } catch (error) {


    console.error(
     "FIRST SCREEN:",
     error
    );
   }
  }
 );




 console.log(
  "Travel Life initialize complete"
 );
}


initialize();
