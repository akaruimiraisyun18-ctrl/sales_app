from flask import (
 Flask,
 render_template,
 jsonify,
 request,
 session
)
from datetime import date, timedelta
from pathlib import Path
import requests
import sqlite3
import math
import os
import re
import time
import uuid
import json
# ============================================================
# Flask
# ============================================================
app = Flask(__name__)
app.secret_key = os.environ.get(
 "SECRET_KEY",
 "travel-life-development-secret-key"
)
# ============================================================
# 国
# ============================================================
COUNTRY_NAMES = {
 "Canada",
 "New Zealand",
 "Australia",
 "Japan",
 "United States",
 "United Kingdom",
 "Ireland",
 "France",
 "Germany",
 "Italy",
 "Spain",
 "Portugal",
 "Netherlands",
 "Belgium",
 "Switzerland",
 "Austria",
 "Sweden",
 "Norway",
 "Denmark",
 "Finland",
 "Iceland",
 "Poland",
 "Czech Republic",
 "Hungary",
 "Greece",
 "Croatia",
 "Estonia",
 "Latvia",
 "Lithuania",
 "Singapore",
 "Malaysia",
 "Thailand",
 "Vietnam",
 "Philippines",
 "Indonesia",
 "South Korea",
 "Taiwan",
 "Hong Kong",
 "India",
 "United Arab Emirates",
 "Qatar",
 "Saudi Arabia",
 "Turkey",
 "Mexico",
 "Brazil",
 "Argentina",
 "Chile",
 "South Africa",
 "Malta",
 "Cyprus",
 "Israel"
}
COUNTRY_CODES = {
 "CA", "NZ", "AU", "JP", "US", "GB", "IE",
 "FR", "DE", "IT", "ES", "PT", "NL", "BE",
 "CH", "AT", "SE", "NO", "DK", "FI", "IS",
 "PL", "CZ", "HU", "GR", "HR", "EE", "LV",
 "LT", "SG", "MY", "TH", "VN", "PH", "ID",
 "KR", "TW", "HK", "IN", "AE", "QA", "SA",
 "TR", "MX", "BR", "AR", "CL", "ZA", "MT",
 "CY", "IL"
}
# ============================================================
# 共通キャッシュ
# ============================================================
CACHE = {}
CACHE_LIMIT = 300
def get_cache(key, seconds):
 saved = CACHE.get(key)
 if saved is None:
  return None
 if (
  time.time()
  -
  saved["time"]
  >
  seconds
 ):
  return None
 return saved["data"]
def save_cache(key, data):
 CACHE[key] = {
  "time": time.time(),
  "data": data
 }
 while len(CACHE) > CACHE_LIMIT:
  first = next(
   iter(CACHE)
  )
  CACHE.pop(
   first,
   None
  )
def json_with_cache_headers(
 data,
 fetched_at=None,
 stale=False
):
 response = jsonify(
  data
 )
 response.headers[
  "X-Fetched-At"
 ] = str(
  fetched_at
  or
  time.time()
 )
 response.headers[
  "X-Data-Stale"
 ] = (
  "1"
  if stale
  else "0"
 )
 response.headers[
  "Cache-Control"
 ] = "no-store"
 return response
# ============================================================
# トップページ
# ============================================================
@app.route("/")
def index():
 return render_template(
  "index.html"
 )
# ============================================================
# 1. 為替
# ============================================================
@app.route(
 "/api/rates/<currency>"
)
def get_rates(currency):
 currency = (
  currency
  .upper()
  .strip()
 )
 period = request.args.get(
  "period",
  "1m"
 )
 days_table = {
  "1d": 7,
  "5d": 14,
  "1m": 35,
  "1y": 370,
  "5y": 1830,
  "max": 3650
 }
 days = days_table.get(
  period,
  35
 )
 today = date.today()
 start_date = (
  today
  -
  timedelta(
   days=days
  )
 )
 if currency == "JPY":
  rows = []
  for kinako in range(
   days + 1
  ):
   target = (
    start_date
    +
    timedelta(
     days=kinako
    )
   )
   rows.append({
    "date":
     target.isoformat(),
    "rate":
     1
   })
  if period == "1d":
   rows = rows[-2:]
  elif period == "5d":
   rows = rows[-5:]
  return json_with_cache_headers({
   "currency":
    "JPY",
   "latest_rate":
    1,
   "latest_date":
    today.isoformat(),
   "data":
    rows
  })
 cache_key = (
  f"rates:{currency}:{period}"
 )
 saved = get_cache(
  cache_key,
  600
 )
 if saved is not None:
  return json_with_cache_headers(
   saved
  )
 try:
  url = (
   "https://api.frankfurter.dev/v1/"
   +
   start_date.isoformat()
   +
   ".."
   +
   today.isoformat()
  )
  response = requests.get(
   url,
   params={
    "base":
     currency,
    "symbols":
     "JPY"
   },
   timeout=15
  )
  response.raise_for_status()
  source = response.json()
  rows = []
  for kinako in sorted(
   source.get(
    "rates",
    {}
   )
  ):
   rate = (
    source[
     "rates"
    ][kinako]
    .get(
     "JPY"
    )
   )
   if rate is None:
    continue
   rows.append({
    "date":
     kinako,
    "rate":
     rate
   })
  if period == "1d":
   rows = rows[-2:]
  elif period == "5d":
   rows = rows[-5:]
  if not rows:
   return jsonify({
    "error":
     "為替データがありません"
   }), 404
  answer = {
   "currency":
    currency,
   "latest_rate":
    rows[-1][
     "rate"
    ],
   "latest_date":
    rows[-1][
     "date"
    ],
   "data":
    rows
  }
  save_cache(
   cache_key,
   answer
  )
  return json_with_cache_headers(
   answer
  )
 except Exception as error:
  print(
   "RATE ERROR:",
   error
  )
  return jsonify({
   "error":
    "為替データを取得できませんでした"
  }), 500
# ============================================================
# 2. ニュース
# ============================================================
@app.route(
 "/api/news"
)
def get_news():
 country = (
  request.args
  .get(
   "country",
   "New Zealand"
  )
  .strip()
 )
 if country not in COUNTRY_NAMES:
  return jsonify({
   "error":
    "対応する国を選択してください"
  }), 400
 cache_key = (
  "news:"
  +
  country
 )
 saved = get_cache(
  cache_key,
  1800
 )
 if saved is not None:
  return json_with_cache_headers(
   saved
  )
 try:
  response = requests.get(
   "https://api.gdeltproject.org/api/v2/doc/doc",
   params={
    "query":
     f'"{country}" sourcelang:english',
    "mode":
     "artlist",
    "maxrecords":
     15,
    "format":
     "json",
    "sort":
     "datedesc",
    "timespan":
     "7d"
   },
   headers={
    "User-Agent":
     "TravelLife/2.0"
   },
   timeout=12
  )
  response.raise_for_status()
  source = response.json()
  articles = []
  for article in source.get(
   "articles",
   []
  ):
   title = article.get(
    "title"
   )
   url = article.get(
    "url"
   )
   if not title:
    continue
   if not str(url).startswith(
    (
     "https://",
     "http://"
    )
   ):
    continue
   articles.append({
    "title":
     title,
    "url":
     url,
    "domain":
     article.get(
      "domain",
      ""
     ),
    "date":
     article.get(
      "seendate",
      ""
     )
   })
  save_cache(
   cache_key,
   articles
  )
  return json_with_cache_headers(
   articles
  )
 except Exception as error:
  print(
   "NEWS ERROR:",
   error
  )
  old = CACHE.get(
   cache_key
  )
  if old:
   return json_with_cache_headers(
    old["data"],
    old["time"],
    True
   )
  return jsonify({
   "error":
    "ニュースを取得できませんでした"
  }), 503
# ============================================================
# 街検索
# ============================================================
def search_places(
 query,
 country
):
 response = requests.get(
  "https://geocoding-api.open-meteo.com/v1/search",
  params={
   "name":
    query,
   "countryCode":
    country,
   "count":
    15,
   "language":
    "ja",
   "format":
    "json"
  },
  headers={
   "User-Agent":
    "TravelLife/2.0"
  },
  timeout=10
 )
 response.raise_for_status()
 data = response.json()
 results = []
 for item in data.get(
  "results",
  []
 ):
  latitude = item.get(
   "latitude"
  )
  longitude = item.get(
   "longitude"
  )
  if (
   latitude is None
   or
   longitude is None
  ):
   continue
  results.append({
   "id":
    item.get(
     "id"
    ),
   "name":
    item.get(
     "name",
     ""
    ),
   "admin1":
    item.get(
     "admin1",
     ""
    ),
   "admin2":
    item.get(
     "admin2",
     ""
    ),
   "detail":
    "・".join(
     [
      str(value)
      for value in [
       item.get(
        "admin1"
       ),
       item.get(
        "country"
       )
      ]
      if value
     ]
    ),
   "latitude":
    latitude,
   "longitude":
    longitude
  })
 return results
@app.route(
 "/api/cities"
)
def get_cities():
 country = (
  request.args
  .get(
   "country",
   ""
  )
  .upper()
 )
 query = (
  request.args
  .get(
   "q",
   ""
  )
  .strip()
 )
 if country not in COUNTRY_CODES:
  return jsonify({
   "error":
    "国を確認してください"
  }), 400
 if len(query) < 2:
  return jsonify({
   "results": []
  })
 cache_key = (
  f"city:{country}:{query.casefold()}"
 )
 saved = get_cache(
  cache_key,
  86400
 )
 if saved is not None:
  return json_with_cache_headers({
   "results":
    saved
  })
 try:
  results = search_places(
   query,
   country
  )
  save_cache(
   cache_key,
   results
  )
  return json_with_cache_headers({
   "results":
    results
  })
 except Exception as error:
  print(
   "CITY ERROR:",
   error
  )
  return jsonify({
   "error":
    "街を検索できませんでした"
  }), 503
# ============================================================
# 天気
# ============================================================
def valid_coordinate(
 latitude,
 longitude
):
 try:
  latitude = float(
   latitude
  )
  longitude = float(
   longitude
  )
 except (
  TypeError,
  ValueError
 ):
  return False
 return (
  -90
  <= latitude
  <= 90
  and
  -180
  <= longitude
  <= 180
 )
def weather_description(code):
 table = {
  0: "快晴",
  1: "晴れ",
  2: "一部曇り",
  3: "曇り",
  45: "霧",
  48: "霧",
  51: "弱い霧雨",
  53: "霧雨",
  55: "強い霧雨",
  56: "着氷性の霧雨",
  57: "強い着氷性の霧雨",
  61: "弱い雨",
  63: "雨",
  65: "強い雨",
  66: "着氷性の雨",
  67: "強い着氷性の雨",
  71: "弱い雪",
  73: "雪",
  75: "強い雪",
  77: "雪粒",
  80: "弱いにわか雨",
  81: "にわか雨",
  82: "激しいにわか雨",
  85: "弱いにわか雪",
  86: "強いにわか雪",
  95: "雷雨",
  96: "ひょうを伴う雷雨",
  99: "激しいひょうを伴う雷雨"
 }
 try:
  return table.get(
   int(code),
   "不明"
  )
 except (
  TypeError,
  ValueError
 ):
  return "不明"
@app.route(
 "/api/weather"
)
def get_weather():
 latitude = request.args.get(
  "lat"
 )
 longitude = request.args.get(
  "lon"
 )
 if not valid_coordinate(
  latitude,
  longitude
 ):
  return jsonify({
   "error":
    "位置情報を確認してください"
  }), 400
 latitude = float(
  latitude
 )
 longitude = float(
  longitude
 )
 cache_key = (
  f"weather:{latitude:.3f}:{longitude:.3f}"
 )
 saved = get_cache(
  cache_key,
  600
 )
 if saved is not None:
  return json_with_cache_headers(
   saved
  )
 try:
  response = requests.get(
   "https://api.open-meteo.com/v1/forecast",
   params={
    "latitude":
     latitude,
    "longitude":
     longitude,
    "current":
     ",".join([
      "temperature_2m",
      "apparent_temperature",
      "relative_humidity_2m",
      "precipitation",
      "rain",
      "weather_code",
      "cloud_cover",
      "wind_speed_10m",
      "wind_direction_10m",
      "wind_gusts_10m"
     ]),
    "hourly":
     ",".join([
      "temperature_2m",
      "apparent_temperature",
      "precipitation_probability",
      "precipitation",
      "rain",
      "weather_code",
      "cloud_cover",
      "visibility",
      "wind_speed_10m",
      "wind_gusts_10m"
     ]),
    "daily":
     ",".join([
      "weather_code",
      "temperature_2m_max",
      "temperature_2m_min",
      "apparent_temperature_max",
      "apparent_temperature_min",
      "sunrise",
      "sunset",
      "precipitation_sum",
      "rain_sum",
      "precipitation_probability_max",
      "wind_speed_10m_max",
      "wind_gusts_10m_max",
      "uv_index_max"
     ]),
    "timezone":
     "auto",
    "forecast_days":
     7
   },
   timeout=12
  )
  response.raise_for_status()
  source = response.json()
  current = source.get(
   "current",
   {}
  )
  hourly = source.get(
   "hourly",
   {}
  )
  daily = source.get(
   "daily",
   {}
  )
  current_code = current.get(
   "weather_code"
  )
  answer = {
   "latitude":
    latitude,
   "longitude":
    longitude,
   "timezone":
    source.get(
     "timezone",
     ""
    ),
   "current": {
    **current,
    "description":
     weather_description(
      current_code
     )
   },
   "hourly":
    hourly,
   "daily":
    daily
  }
  save_cache(
   cache_key,
   answer
  )
  return json_with_cache_headers(
   answer
  )
 except Exception as error:
  print(
   "WEATHER ERROR:",
   error
  )
  old = CACHE.get(
   cache_key
  )
  if old:
   return json_with_cache_headers(
    old["data"],
    old["time"],
    True
   )
  return jsonify({
   "error":
    "天気情報を取得できませんでした"
  }), 503
# ============================================================
# 危険情報
# ============================================================
@app.route(
 "/api/danger"
)
@app.route(
  "/api/danger",
  methods=["GET"]
)
def get_danger():


  country = (
    request.args.get(
      "country",
      ""
    )
    .strip()
    .upper()
  )


  if not country:
    return jsonify({
      "error":
        "country が必要です"
    }), 400


  try:
    response = requests.get(
      "https://www.gdacs.org/gdacsapi/api/events/geteventlist/search",
      params={
        "country":
          country
      },
      timeout=15
    )


    response.raise_for_status()


    source = response.json()


    features = source.get(
      "features",
      []
    )


    events = []


    for feature in features:


      properties = feature.get(
        "properties",
        {}
      )


      geometry = feature.get(
        "geometry",
        {}
      )


      coordinates = geometry.get(
        "coordinates",
        []
      )


      event = {
        "id":
          properties.get(
            "eventid"
          ),


        "type":
          properties.get(
            "eventtype",
            ""
          ),


        "name":
          properties.get(
            "name",
            ""
          ),


        "alert_level":
          properties.get(
            "alertlevel",
            "Green"
          ),


        "severity":
          properties.get(
            "severitydata",
            {}
          ),


        "from_date":
          properties.get(
            "fromdate"
          ),


        "to_date":
          properties.get(
            "todate"
          ),


        "country":
          properties.get(
            "country",
            ""
          ),


        "latitude":
          (
            coordinates[1]
            if (
              isinstance(
                coordinates,
                list
              )
              and
              len(coordinates) >= 2
            )
            else None
          ),


        "longitude":
          (
            coordinates[0]
            if (
              isinstance(
                coordinates,
                list
              )
              and
              len(coordinates) >= 2
            )
            else None
          )
      }


      events.append(
        event
      )


    alert_order = {
      "Red":
        3,
      "Orange":
        2,
      "Green":
        1
    }


    events.sort(
      key=lambda kinako:
        alert_order.get(
          kinako.get(
            "alert_level",
            "Green"
          ),
          0
        ),
      reverse=True
    )


    return jsonify({
      "ok":
        True,


      "country":
        country,


      "source":
        "GDACS",


      "count":
        len(
          events
        ),


      "events":
        events
    })


  except requests.RequestException as error:


    print(
      "GDACS ERROR:",
      error
    )


    return jsonify({
      "error":
        "災害情報を取得できませんでした"
    }), 503


  except Exception as error:


    print(
      "DANGER ERROR:",
      error
    )


    return jsonify({
      "error":
        "災害情報の処理に失敗しました"
    }), 500
# ============================================================
# 経路
# ============================================================
ROUTE_PROFILES = {
 "walking":
  "foot-walking",
 "cycling":
  "cycling-regular",
 "driving":
  "driving-car"
}
@app.route(
 "/api/route"
)
@app.route(
  "/api/route",
  methods=["GET"]
)
def get_route():
  start_lat = request.args.get("start_lat", "").strip()
  start_lon = request.args.get("start_lon", "").strip()
  end_lat = request.args.get("end_lat", "").strip()
  end_lon = request.args.get("end_lon", "").strip()
  mode = request.args.get("mode", "walking").strip().lower()


  if mode not in ROUTE_PROFILES:
    return jsonify({
      "error": "対応していない移動方法です"
    }), 400


  try:
    start_lat = float(start_lat)
    start_lon = float(start_lon)
    end_lat = float(end_lat)
    end_lon = float(end_lon)
  except (TypeError, ValueError):
    return jsonify({
      "error": "位置情報が正しくありません"
    }), 400


  if not (-90 <= start_lat <= 90):
    return jsonify({
      "error": "出発地点の緯度が正しくありません"
    }), 400


  if not (-180 <= start_lon <= 180):
    return jsonify({
      "error": "出発地点の経度が正しくありません"
    }), 400


  if not (-90 <= end_lat <= 90):
    return jsonify({
      "error": "到着地点の緯度が正しくありません"
    }), 400


  if not (-180 <= end_lon <= 180):
    return jsonify({
      "error": "到着地点の経度が正しくありません"
    }), 400


  cache_key = (
    f"route:"
    f"{start_lat:.5f}:"
    f"{start_lon:.5f}:"
    f"{end_lat:.5f}:"
    f"{end_lon:.5f}:"
    f"{mode}"
  )


  cached = get_cache(
    cache_key,
    300
  )


  if cached is not None:
    return json_with_cache_headers(
      cached
    )


  api_key = (
    os.environ.get(
      "ORS_API_KEY",
      ""
    )
    or os.environ.get(
      "OPENROUTESERVICE_API_KEY",
      ""
    )
  ).strip()


  if not api_key:
    osrm_servers = {
      "walking": "routed-foot",
      "cycling": "routed-bike",
      "driving": "routed-car"
    }


    osrm_server = osrm_servers.get(
      mode
    )


    if not osrm_server:
      return jsonify({
        "error": "この移動方法には対応していません"
      }), 400


    try:
      response = requests.get(
        (
          "https://routing.openstreetmap.de/"
          f"{osrm_server}/route/v1/driving/"
          f"{start_lon},{start_lat};"
          f"{end_lon},{end_lat}"
        ),
        params={
          "overview": "full",
          "geometries": "geojson",
          "steps": "true"
        },
        headers={
          "User-Agent": "TravelLife/2.0"
        },
        timeout=20
      )


      response.raise_for_status()
      source = response.json()


      routes = source.get(
        "routes",
        []
      )


      if not routes:
        return jsonify({
          "error": "経路が見つかりませんでした"
        }), 404


      route = routes[0]


      answer = {
        "distance": route.get(
          "distance",
          0
        ),
        "duration": route.get(
          "duration",
          0
        ),
        "geometry": route.get(
          "geometry",
          {}
        ),
        "mode": mode,
        "provider": "OSRM"
      }


      save_cache(
        cache_key,
        answer
      )


      return json_with_cache_headers(
        answer
      )


    except requests.RequestException as error:
      print(
        "OSRM ROUTE ERROR:",
        error
      )


      return jsonify({
        "error": "経路を取得できませんでした"
      }), 503


    except (
      KeyError,
      TypeError,
      ValueError
    ) as error:
      print(
        "OSRM DATA ERROR:",
        error
      )


      return jsonify({
        "error": "経路データを処理できませんでした"
      }), 502


  try:
    profile = ROUTE_PROFILES[
      mode
    ]


    ors_url = (
      "https://api.heigit.org/"
      "openrouteservice/v2/directions/"
      f"{profile}/geojson"
    )


    response = requests.post(
      ors_url,
      headers={
        "Authorization": api_key,
        "Content-Type": "application/json",
        "Accept": "application/json"
      },
      json={
        "coordinates": [
          [
            start_lon,
            start_lat
          ],
          [
            end_lon,
            end_lat
          ]
        ]
      },
      timeout=20
    )


    response.raise_for_status()
    source = response.json()


    features = source.get(
      "features",
      []
    )


    if not features:
      return jsonify({
        "error": "経路が見つかりませんでした"
      }), 404


    feature = features[0]


    properties = feature.get(
      "properties",
      {}
    )


    summary = properties.get(
      "summary",
      {}
    )


    geometry = feature.get(
      "geometry",
      {}
    )


    answer = {
      "distance": summary.get(
        "distance",
        0
      ),
      "duration": summary.get(
        "duration",
        0
      ),
      "geometry": geometry,
      "mode": mode,
      "provider": "OpenRouteService"
    }


    save_cache(
      cache_key,
      answer
    )


    return json_with_cache_headers(
      answer
    )


  except requests.RequestException as error:
    print(
      "ORS ROUTE ERROR:",
      error
    )


    return jsonify({
      "error": "経路を取得できませんでした"
    }), 503


  except (
    KeyError,
    TypeError,
    ValueError
  ) as error:
    print(
      "ORS DATA ERROR:",
      error
    )


    return jsonify({
      "error": "経路データを処理できませんでした"
    }), 502


  # --------------------------------------------------------
  # OpenRouteService
  # --------------------------------------------------------


  try:
    profile = ROUTE_PROFILES[
      mode
    ]


    response = requests.post(
      (
        "https://api.heigit.org/openrouteservice/"
        f"v2/directions/{profile}/geojson"
      ),
      json={
        "coordinates": [
          [
            start_lon,
            start_lat
          ],
          [
            end_lon,
            end_lat
          ]
        ]
      },
      headers={
        "Authorization":
          api_key,
        "Content-Type":
          "application/json"
      },
      timeout=15
    )


    response.raise_for_status()


    source = response.json()


    features = source.get(
      "features",
      []
    )


    if not features:
      return jsonify({
        "error":
          "経路が見つかりませんでした"
      }), 404


    feature = features[0]


    properties = feature.get(
      "properties",
      {}
    )


    summary = properties.get(
      "summary",
      {}
    )


    answer = {
      "distance":
        summary.get(
          "distance",
          0
        ),
      "duration":
        summary.get(
          "duration",
          0
        ),
      "geometry":
        feature.get(
          "geometry",
          {}
        ),
      "mode":
        mode,
      "provider":
        "OpenRouteService"
    }


    save_cache(
      cache_key,
      answer
    )


    return json_with_cache_headers(
      answer
    )


  except requests.RequestException as error:
    print(
      "ORS REQUEST ERROR:",
      error
    )


    return jsonify({
      "error":
        "経路サービスとの通信に失敗しました"
    }), 503


  except Exception as error:
    print(
      "ORS ROUTE ERROR:",
      error
    )


    return jsonify({
      "error":
        "経路を取得できませんでした"
    }), 503


   
# ============================================================
# GAME / DATABASE
# ============================================================
GAME_DB_PATH = os.environ.get(
  "GAME_DB_PATH",
  "/tmp/travellife_game.sqlite3"
)
GAME_NORMAL_START_COINS = int(
  os.environ.get(
    "GAME_NORMAL_START_COINS",
    "1500"
  )
)
GAME_MASTER_START_COINS = int(
  os.environ.get(
    "GAME_MASTER_START_COINS",
    "100000"
  )
)
GAME_BASE_PRICE = int(
  os.environ.get(
    "GAME_BASE_PRICE",
    "1000"
  )
)
GAME_BUYOUT_MULTIPLIER = 2.0
GAME_DEFENSE_MULTIPLIER = 2.0
GAME_BUYOUT_HOURS = 24
LAND_TYPE_MULTIPLIERS = {
  "station_major": 5.0,
  "station": 3.5,
  "mall": 4.0,
  "supermarket": 2.5,
  "hotel": 3.0,
  "hospital": 3.0,
  "restaurant": 1.5,
  "commercial": 1.8,
  "office": 1.5,
  "residential": 1.0,
  "normal": 0.8
}
def game_connect():
  db = sqlite3.connect(
    GAME_DB_PATH,
    timeout=15
  )
  db.row_factory = sqlite3.Row
  return db
def game_now():
  return int(
    time.time()
  )
def game_player_id():
  player_id = session.get(
    "game_player_id"
  )
  if not player_id:
    player_id = str(
      uuid.uuid4()
    )
    session[
      "game_player_id"
    ] = player_id
  return player_id
def add_column(db, table, definition):
  column_name = definition.split()[0]


  existing_columns = {
    row[1]
    for row in db.execute(
      f"PRAGMA table_info({table})"
    ).fetchall()
  }


  if column_name not in existing_columns:
    db.execute(
      f"""
      ALTER TABLE {table}
      ADD COLUMN {definition}
      """
    )




def init_game_db():
  with game_connect() as db:
    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_players (
        id TEXT PRIMARY KEY,
        player_id TEXT,
        name TEXT,
        coins INTEGER NOT NULL DEFAULT 1500,
        is_game_master INTEGER NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL,
        updated_at INTEGER NOT NULL
      )
      """
    )

    add_column(
      db,
      "game_players",
      "player_id TEXT"
    )

    db.execute(
      """
      UPDATE game_players
      SET player_id = id
      WHERE
        player_id IS NULL
        OR player_id = ''
      """
    )

    db.execute(
      """
      CREATE UNIQUE INDEX IF NOT EXISTS
      game_players_player_id_index
      ON game_players(player_id)
      """
    )

    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_lands (
        cell_id TEXT PRIMARY KEY,
        owner_id TEXT NOT NULL,
        center_lat REAL NOT NULL DEFAULT 0,
        center_lon REAL NOT NULL DEFAULT 0,
        purchase_price INTEGER NOT NULL DEFAULT 0,
        acquired_at INTEGER NOT NULL DEFAULT 0,
        name TEXT NOT NULL DEFAULT '',
        land_type TEXT NOT NULL DEFAULT 'normal',
        osm_type TEXT NOT NULL DEFAULT '',
        osm_id TEXT NOT NULL DEFAULT '',
        polygon_json TEXT NOT NULL DEFAULT '',
        area_m2 REAL NOT NULL DEFAULT 0,
        station_distance REAL NOT NULL DEFAULT 999999,
        daily_income INTEGER NOT NULL DEFAULT 6,
        last_income_at INTEGER NOT NULL DEFAULT 0,
        land_name TEXT NOT NULL DEFAULT '',
        price INTEGER NOT NULL DEFAULT 0,
        latitude REAL NOT NULL DEFAULT 0,
        longitude REAL NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL DEFAULT 0,
        updated_at INTEGER NOT NULL DEFAULT 0
      )
      """
    )

    land_columns = [
      "center_lat REAL NOT NULL DEFAULT 0",
      "center_lon REAL NOT NULL DEFAULT 0",
      "purchase_price INTEGER NOT NULL DEFAULT 0",
      "acquired_at INTEGER NOT NULL DEFAULT 0",
      "name TEXT NOT NULL DEFAULT ''",
      "land_type TEXT NOT NULL DEFAULT 'normal'",
      "osm_type TEXT NOT NULL DEFAULT ''",
      "osm_id TEXT NOT NULL DEFAULT ''",
      "polygon_json TEXT NOT NULL DEFAULT ''",
      "area_m2 REAL NOT NULL DEFAULT 0",
      "station_distance REAL NOT NULL DEFAULT 999999",
      "daily_income INTEGER NOT NULL DEFAULT 6",
      "last_income_at INTEGER NOT NULL DEFAULT 0",
      "land_name TEXT NOT NULL DEFAULT ''",
      "price INTEGER NOT NULL DEFAULT 0",
      "latitude REAL NOT NULL DEFAULT 0",
      "longitude REAL NOT NULL DEFAULT 0",
      "created_at INTEGER NOT NULL DEFAULT 0",
      "updated_at INTEGER NOT NULL DEFAULT 0"
    ]

    for kinako in land_columns:
      add_column(
        db,
        "game_lands",
        kinako
      )

    now = game_now()

    db.execute(
      """
      UPDATE game_lands
      SET
        land_name = CASE
          WHEN land_name = '' THEN name
          ELSE land_name
        END,
        name = CASE
          WHEN name = '' THEN land_name
          ELSE name
        END,
        price = CASE
          WHEN price = 0 THEN purchase_price
          ELSE price
        END,
        purchase_price = CASE
          WHEN purchase_price = 0 THEN price
          ELSE purchase_price
        END,
        latitude = CASE
          WHEN latitude = 0 AND center_lat != 0 THEN center_lat
          ELSE latitude
        END,
        center_lat = CASE
          WHEN center_lat = 0 AND latitude != 0 THEN latitude
          ELSE center_lat
        END,
        longitude = CASE
          WHEN longitude = 0 AND center_lon != 0 THEN center_lon
          ELSE longitude
        END,
        center_lon = CASE
          WHEN center_lon = 0 AND longitude != 0 THEN longitude
          ELSE center_lon
        END,
        created_at = CASE
          WHEN created_at = 0 THEN acquired_at
          ELSE created_at
        END,
        acquired_at = CASE
          WHEN acquired_at = 0 THEN created_at
          ELSE acquired_at
        END,
        updated_at = CASE
          WHEN updated_at = 0 THEN
            CASE
              WHEN acquired_at > 0 THEN acquired_at
              ELSE ?
            END
          ELSE updated_at
        END,
        last_income_at = CASE
          WHEN last_income_at = 0 THEN
            CASE
              WHEN acquired_at > 0 THEN acquired_at
              ELSE ?
            END
          ELSE last_income_at
        END
      """,
      (
        now,
        now
      )
    )

    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_buyouts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        cell_id TEXT NOT NULL,
        challenger_id TEXT NOT NULL,
        owner_id TEXT NOT NULL,
        offer_price INTEGER NOT NULL,
        defense_price INTEGER NOT NULL,
        status TEXT NOT NULL DEFAULT 'pending',
        created_at INTEGER NOT NULL,
        expires_at INTEGER NOT NULL,
        resolved_at INTEGER
      )
      """
    )

    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_notifications (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id TEXT NOT NULL,
        type TEXT NOT NULL,
        message TEXT NOT NULL,
        cell_id TEXT,
        buyout_id INTEGER,
        is_read INTEGER NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL
      )
      """
    )

    # 旧版の移動テーブルが残っている場合は、現在の列構成へ移行する。
    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_trips (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        player_id TEXT NOT NULL,
        started_at INTEGER NOT NULL,
        ended_at INTEGER,
        distance REAL NOT NULL DEFAULT 0,
        coins INTEGER NOT NULL DEFAULT 0
      )
      """
    )

    trip_columns = {
      row[1]
      for row in db.execute(
        "PRAGMA table_info(game_trips)"
      ).fetchall()
    }

    if not {
      "id",
      "player_id",
      "started_at",
      "ended_at",
      "distance"
    }.issubset(
      trip_columns
    ):
      db.execute(
        "ALTER TABLE game_trips RENAME TO game_trips_legacy"
      )

      db.execute(
        """
        CREATE TABLE game_trips (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          player_id TEXT NOT NULL,
          started_at INTEGER NOT NULL,
          ended_at INTEGER,
          distance REAL NOT NULL DEFAULT 0,
          coins INTEGER NOT NULL DEFAULT 0
        )
        """
      )

      legacy_columns = {
        row[1]
        for row in db.execute(
          "PRAGMA table_info(game_trips_legacy)"
        ).fetchall()
      }

      if "player_id" in legacy_columns:
        id_expr = (
          "trip_id"
          if "trip_id" in legacy_columns
          else "NULL"
        )
        started_expr = (
          "started_at"
          if "started_at" in legacy_columns
          else (
            "started"
            if "started" in legacy_columns
            else str(now)
          )
        )
        ended_expr = (
          "ended_at"
          if "ended_at" in legacy_columns
          else (
            "ended"
            if "ended" in legacy_columns
            else "NULL"
          )
        )
        distance_expr = (
          "distance"
          if "distance" in legacy_columns
          else "0"
        )
        coins_expr = (
          "coins"
          if "coins" in legacy_columns
          else "0"
        )

        db.execute(
          f"""
          INSERT OR IGNORE INTO game_trips (
            id,
            player_id,
            started_at,
            ended_at,
            distance,
            coins
          )
          SELECT
            {id_expr},
            player_id,
            {started_expr},
            {ended_expr},
            {distance_expr},
            {coins_expr}
          FROM game_trips_legacy
          """
        )

      db.execute(
        "DROP TABLE game_trips_legacy"
      )
    else:
      add_column(
        db,
        "game_trips",
        "coins INTEGER NOT NULL DEFAULT 0"
      )

    db.execute(
      """
      CREATE TABLE IF NOT EXISTS game_trip_points (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        trip_id INTEGER NOT NULL,
        latitude REAL NOT NULL,
        longitude REAL NOT NULL,
        accuracy REAL NOT NULL DEFAULT 0,
        created_at INTEGER NOT NULL
      )
      """
    )

    point_columns = {
      row[1]
      for row in db.execute(
        "PRAGMA table_info(game_trip_points)"
      ).fetchall()
    }

    if not {
      "id",
      "trip_id",
      "latitude",
      "longitude",
      "created_at"
    }.issubset(
      point_columns
    ):
      db.execute(
        "ALTER TABLE game_trip_points RENAME TO game_trip_points_legacy"
      )

      db.execute(
        """
        CREATE TABLE game_trip_points (
          id INTEGER PRIMARY KEY AUTOINCREMENT,
          trip_id INTEGER NOT NULL,
          latitude REAL NOT NULL,
          longitude REAL NOT NULL,
          accuracy REAL NOT NULL DEFAULT 0,
          created_at INTEGER NOT NULL
        )
        """
      )

      legacy_columns = {
        row[1]
        for row in db.execute(
          "PRAGMA table_info(game_trip_points_legacy)"
        ).fetchall()
      }

      if "trip_id" in legacy_columns:
        id_expr = (
          "point_id"
          if "point_id" in legacy_columns
          else "NULL"
        )
        lat_expr = (
          "latitude"
          if "latitude" in legacy_columns
          else (
            "lat"
            if "lat" in legacy_columns
            else "NULL"
          )
        )
        lon_expr = (
          "longitude"
          if "longitude" in legacy_columns
          else (
            "lon"
            if "lon" in legacy_columns
            else "NULL"
          )
        )
        accuracy_expr = (
          "accuracy"
          if "accuracy" in legacy_columns
          else "0"
        )
        created_expr = (
          "created_at"
          if "created_at" in legacy_columns
          else str(now)
        )

        if (
          lat_expr != "NULL"
          and
          lon_expr != "NULL"
        ):
          db.execute(
            f"""
            INSERT OR IGNORE INTO game_trip_points (
              id,
              trip_id,
              latitude,
              longitude,
              accuracy,
              created_at
            )
            SELECT
              {id_expr},
              trip_id,
              {lat_expr},
              {lon_expr},
              {accuracy_expr},
              {created_expr}
            FROM game_trip_points_legacy
            """
          )

      db.execute(
        "DROP TABLE game_trip_points_legacy"
      )
    else:
      add_column(
        db,
        "game_trip_points",
        "accuracy REAL NOT NULL DEFAULT 0"
      )

    db.commit()
def ensure_game_player(
  db,
  player_id
):
  player = db.execute(
    """
    SELECT *
    FROM game_players
    WHERE id = ?
    """,
    (
      player_id,
    )
  ).fetchone()

  if player:
    if (
      not player["player_id"]
      or
      player["player_id"] != player_id
    ):
      db.execute(
        """
        UPDATE game_players
        SET player_id = ?
        WHERE id = ?
        """,
        (
          player_id,
          player_id
        )
      )
      db.commit()

    return db.execute(
      """
      SELECT *
      FROM game_players
      WHERE id = ?
      """,
      (
        player_id,
      )
    ).fetchone()

  now = game_now()

  start_coins = GAME_NORMAL_START_COINS

  if session.get(
    "game_is_master"
  ) is True:
    start_coins = GAME_MASTER_START_COINS

  db.execute(
    """
    INSERT INTO game_players (
      id,
      player_id,
      name,
      coins,
      is_game_master,
      created_at,
      updated_at
    )
    VALUES (?, ?, ?, ?, ?, ?, ?)
    """,
    (
      player_id,
      player_id,
      None,
      start_coins,
      1
      if session.get(
        "game_is_master"
      ) is True
      else 0,
      now,
      now
    )
  )

  db.commit()

  return db.execute(
    """
    SELECT *
    FROM game_players
    WHERE id = ?
    """,
    (
      player_id,
    )
  ).fetchone()
def game_player_name(
  db,
  player_id
):
  row = db.execute(
    """
    SELECT name
    FROM game_players
    WHERE id = ?
    """,
    (
      player_id,
    )
  ).fetchone()
  if not row:
    return "不明"
  return (
    row["name"]
    or
    "名前未設定"
  )
def calculate_station_income(
  distance
):
  if distance is None:
    return 6
  distance = float(
    distance
  )
  if distance <= 100:
    return 40
  if distance <= 300:
    return 30
  if distance <= 500:
    return 22
  if distance <= 1000:
    return 15
  if distance <= 2000:
    return 10
  return 6
def is_large_commercial(
  name,
  land_type
):
  text = (
    str(name or "")
    .casefold()
  )
  keywords = [
    "apita",
    "アピタ",
    "aeon",
    "イオン",
    "lalaport",
    "ららぽーと",
    "outlet",
    "アウトレット",
    "mall",
    "モール"
  ]
  if land_type == "mall":
    return True
  return any(
    word.casefold() in text
    for word in keywords
  )
def calculate_land_income(
  station_distance,
  land_name="",
  land_type="normal"
):
  income = calculate_station_income(
    station_distance
  )
  if is_large_commercial(
    land_name,
    land_type
  ):
    income = max(
      40,
      income
    )
  return int(
    income
  )
def calculate_land_price(
  land_type="normal"
):
  multiplier = (
    LAND_TYPE_MULTIPLIERS
    .get(
      land_type,
      LAND_TYPE_MULTIPLIERS[
        "normal"
      ]
    )
  )
  return max(
    100,
    int(
      round(
        GAME_BASE_PRICE
        *
        multiplier
      )
    )
  )
def settle_land_income(
  db,
  player_id=None
):
  now = game_now()
  if player_id:
    lands = db.execute(
      """
      SELECT *
      FROM game_lands
      WHERE owner_id = ?
      """,
      (
        player_id,
      )
    ).fetchall()
  else:
    lands = db.execute(
      """
      SELECT *
      FROM game_lands
      WHERE owner_id IS NOT NULL
      """
    ).fetchall()
  player_income = {}
  for land in lands:
    last_income_at = (
      land[
        "last_income_at"
      ]
      or
      land[
        "updated_at"
      ]
      or
      now
    )
    elapsed = (
      now
      -
      int(
        last_income_at
      )
    )
    whole_days = (
      elapsed
      //
      86400
    )
    if whole_days <= 0:
      continue
    income = (
      int(
        land[
          "daily_income"
        ]
        or
        0
      )
      *
      whole_days
    )
    owner_id = land[
      "owner_id"
    ]
    if (
      not owner_id
      or
      income <= 0
    ):
      continue
    player_income[
      owner_id
    ] = (
      player_income.get(
        owner_id,
        0
      )
      +
      income
    )
    db.execute(
      """
      UPDATE game_lands
      SET last_income_at = ?
      WHERE cell_id = ?
      """,
      (
        int(
          last_income_at
          +
          whole_days
          *
          86400
        ),
        land[
          "cell_id"
        ]
      )
    )
  for (
    owner_id,
    amount
  ) in player_income.items():
    db.execute(
      """
      UPDATE game_players
      SET
        coins = coins + ?,
        updated_at = ?
      WHERE id = ?
      """,
      (
        amount,
        now,
        owner_id
      )
    )
  db.commit()
def create_game_notification(
  db,
  player_id,
  notification_type,
  message,
  cell_id=None,
  buyout_id=None
):
  db.execute(
    """
    INSERT INTO game_notifications (
      player_id,
      type,
      message,
      cell_id,
      buyout_id,
      is_read,
      created_at
    )
    VALUES (?, ?, ?, ?, ?, 0, ?)
    """,
    (
      player_id,
      notification_type,
      message,
      cell_id,
      buyout_id,
      game_now()
    )
  )
def settle_expired_buyouts(
  db
):
  now = game_now()
  buyouts = db.execute(
    """
    SELECT *
    FROM game_buyouts
    WHERE
      status = 'pending'
      AND expires_at <= ?
    """,
    (
      now,
    )
  ).fetchall()
  for buyout in buyouts:
    land = db.execute(
      """
      SELECT *
      FROM game_lands
      WHERE cell_id = ?
      """,
      (
        buyout[
          "cell_id"
        ],
      )
    ).fetchone()
    if not land:
      db.execute(
        """
        UPDATE game_buyouts
        SET
          status = 'cancelled',
          resolved_at = ?
        WHERE id = ?
        """,
        (
          now,
          buyout[
            "id"
          ]
        )
      )
      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins + ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          buyout[
            "offer_price"
          ],
          now,
          buyout[
            "challenger_id"
          ]
        )
      )
      continue
    if (
      land[
        "owner_id"
      ]
      !=
      buyout[
        "owner_id"
      ]
    ):
      db.execute(
        """
        UPDATE game_buyouts
        SET
          status = 'cancelled',
          resolved_at = ?
        WHERE id = ?
        """,
        (
          now,
          buyout[
            "id"
          ]
        )
      )
      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins + ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          buyout[
            "offer_price"
          ],
          now,
          buyout[
            "challenger_id"
          ]
        )
      )
      continue
    db.execute(
      """
      UPDATE game_lands
      SET
        owner_id = ?,
        price = ?,
        last_income_at = ?,
        updated_at = ?
      WHERE cell_id = ?
      """,
      (
        buyout[
          "challenger_id"
        ],
        buyout[
          "offer_price"
        ],
        now,
        now,
        buyout[
          "cell_id"
        ]
      )
    )
    db.execute(
      """
      UPDATE game_players
      SET
        coins = coins + ?,
        updated_at = ?
      WHERE id = ?
      """,
      (
        buyout[
          "offer_price"
        ],
        now,
        buyout[
          "owner_id"
        ]
      )
    )
    db.execute(
      """
      UPDATE game_buyouts
      SET
        status = 'completed',
        resolved_at = ?
      WHERE id = ?
      """,
      (
        now,
        buyout[
          "id"
        ]
      )
    )
    challenger_name = game_player_name(
      db,
      buyout[
        "challenger_id"
      ]
    )
    create_game_notification(
      db,
      buyout[
        "owner_id"
      ],
      "buyout_completed",
      (
        f"{land['land_name'] or '土地'}の買収が完了し、"
        f"{challenger_name}さんへ所有権が移りました。"
      ),
      buyout[
        "cell_id"
      ],
      buyout[
        "id"
      ]
    )
    create_game_notification(
      db,
      buyout[
        "challenger_id"
      ],
      "buyout_completed",
      (
        f"{land['land_name'] or '土地'}の買収が完了しました。"
      ),
      buyout[
        "cell_id"
      ],
      buyout[
        "id"
      ]
    )
  db.commit()
# ============================================================
# GAME / PROFILE
# ============================================================
@app.route(
  "/api/game/profile",
  methods=[
    "POST"
  ]
)
def game_profile():
  player_id = game_player_id()
  try:
    data = (
      request.get_json(
        silent=True
      )
      or
      {}
    )
    name = str(
      data.get(
        "name",
        ""
      )
    ).strip()
    if (
      len(name) < 2
      or
      len(name) > 20
    ):
      return jsonify({
        "error":
          "ユーザー名は2〜20文字で入力してください"
      }), 400
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      duplicate = db.execute(
        """
        SELECT id
        FROM game_players
        WHERE
          name = ?
          AND id != ?
        """,
        (
          name,
          player_id
        )
      ).fetchone()
      if duplicate:
        return jsonify({
          "error":
            "そのユーザー名は既に使用されています"
        }), 409
      db.execute(
        """
        UPDATE game_players
        SET
          name = ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          name,
          game_now(),
          player_id
        )
      )
      db.commit()
      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()
      return jsonify({
        "ok":
          True,
        "player": {
          "id":
            player[
              "id"
            ],
          "name":
            player[
              "name"
            ],
          "coins":
            player[
              "coins"
            ]
        }
      })
  except Exception as error:
    print(
      "GAME PROFILE ERROR:",
      error
    )
    return jsonify({
      "error":
        "ユーザー名を保存できませんでした"
    }), 500
# ============================================================
# GAME / ME
# ============================================================
@app.route(
  "/api/game/me",
  methods=[
    "GET"
  ]
)
def game_me():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      settle_land_income(
        db,
        player_id
      )
      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()
      land_count = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM game_lands
        WHERE owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()[
        "count"
      ]
      daily_income = db.execute(
        """
        SELECT
          COALESCE(
            SUM(daily_income),
            0
          ) AS total
        FROM game_lands
        WHERE owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()[
        "total"
      ]
      return jsonify({
        "ok":
          True,
        "player": {
          "id":
            player[
              "id"
            ],
          "name":
            player[
              "name"
            ],
          "coins":
            player[
              "coins"
            ],
          "is_game_master":
            bool(
              player[
                "is_game_master"
              ]
            ),
          "land_count":
            land_count,
          "daily_income":
            daily_income
        }
      })
  except Exception as error:
    print(
      "GAME ME ERROR:",
      error
    )
    return jsonify({
      "error":
        "プレイヤー情報を取得できませんでした"
    }), 500
# ============================================================
# GAME / BOOTSTRAP
# ============================================================
@app.route(
  "/api/game/bootstrap",
  methods=[
    "GET"
  ]
)
def game_bootstrap():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      settle_land_income(
        db,
        player_id
      )
      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()
      land_count = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM game_lands
        WHERE owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()[
        "count"
      ]
      total_lands = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM game_lands
        WHERE owner_id IS NOT NULL
        """
      ).fetchone()[
        "count"
      ]
      total_players = db.execute(
        """
        SELECT COUNT(*) AS count
        FROM game_players
        """
      ).fetchone()[
        "count"
      ]
      daily_income = db.execute(
        """
        SELECT
          COALESCE(
            SUM(daily_income),
            0
          ) AS total
        FROM game_lands
        WHERE owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()[
        "total"
      ]
      return jsonify({
        "ok":
          True,
        "player": {
          "id":
            player[
              "id"
            ],
          "name":
            player[
              "name"
            ],
          "coins":
            player[
              "coins"
            ],
          "land_count":
            land_count,
          "daily_income":
            daily_income
        },
        "stats": {
          "players":
            total_players,
          "lands":
            total_lands
        },
        "settings": {
          "base_price":
            GAME_BASE_PRICE,
          "buyout_multiplier":
            GAME_BUYOUT_MULTIPLIER,
          "buyout_hours":
            GAME_BUYOUT_HOURS
        }
      })
  except Exception as error:
    print(
      "GAME BOOTSTRAP ERROR:",
      error
    )
    return jsonify({
      "error":
        "ゲームデータを読み込めませんでした"
    }), 500
# ============================================================
# GAME / LAND
# ============================================================
def normalize_cell_id(value):


  value = str(
    value
    or ""
  ).strip()


  # ================================================
  # 対応する土地ID
  #
  # 旧形式
  # 123:456
  # grid:123:456
  #
  # OSM由来
  # osm:node:123
  # osm:way:123
  # osm:relation:123
  # osm:building:123
  # ================================================


  if re.fullmatch(
    r"(?:"
    r"-?\d+:-?\d+"
    r"|grid:-?\d+:-?\d+"
    r"|osm:(?:node|way|relation|building):\d+"
    r")",
    value
  ):
    return value


  raise ValueError(
    "土地IDが正しくありません"
  )
@app.route(
  "/api/game/cell",
  methods=[
    "GET"
  ]
)
def game_cell():
  player_id = game_player_id()
  cell_id = normalize_cell_id(
    request.args.get(
      "cell_id"
    )
  )
  if not cell_id:
    return jsonify({
      "error":
        "土地IDが正しくありません"
    }), 400
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      land = db.execute(
        """
        SELECT *
        FROM game_lands
        WHERE cell_id = ?
        """,
        (
          cell_id,
        )
      ).fetchone()
      if not land:
        return jsonify({
          "ok":
            True,
          "land": {
            "cell_id":
              cell_id,
            "owner_id":
              None,
            "owner_name":
              None,
            "price":
              GAME_BASE_PRICE,
            "daily_income":
              6,
            "land_type":
              "normal"
          }
        })
      owner_name = None
      if land[
        "owner_id"
      ]:
        owner_name = game_player_name(
          db,
          land[
            "owner_id"
          ]
        )
      pending = db.execute(
        """
        SELECT *
        FROM game_buyouts
        WHERE
          cell_id = ?
          AND status = 'pending'
        ORDER BY id DESC
        LIMIT 1
        """,
        (
          cell_id,
        )
      ).fetchone()
      return jsonify({
        "ok":
          True,
        "land": {
          "cell_id":
            land[
              "cell_id"
            ],
          "land_name":
            land[
              "land_name"
            ],
          "land_type":
            land[
              "land_type"
            ],
          "owner_id":
            land[
              "owner_id"
            ],
          "owner_name":
            owner_name,
          "price":
            land[
              "price"
            ],
          "latitude":
            land[
              "latitude"
            ],
          "longitude":
            land[
              "longitude"
            ],
          "station_distance":
            land[
              "station_distance"
            ],
          "daily_income":
            land[
              "daily_income"
            ],
          "mine":
            (
              land[
                "owner_id"
              ]
              ==
              player_id
            ),
          "buyout_pending":
            bool(
              pending
            )
        }
      })
  except Exception as error:
    print(
      "GAME CELL ERROR:",
      error
    )
    return jsonify({
      "error":
        "土地情報を取得できませんでした"
    }), 500
# ============================================================
# GAME / LAND BUY
# ============================================================
@app.route(
  "/api/game/cell/buy",
  methods=[
    "POST"
  ]
)
def game_cell_buy():
  player_id = game_player_id()

  try:
    data = (
      request.get_json(
        silent=True
      )
      or
      {}
    )

    cell_id = normalize_cell_id(
      data.get(
        "cell_id"
      )
    )

    if not cell_id:
      return jsonify({
        "error":
          "土地IDが正しくありません"
      }), 400

    land_name = str(
      data.get(
        "land_name"
      )
      or
      data.get(
        "name"
      )
      or
      "土地"
    )[:100]

    land_type = str(
      data.get(
        "land_type"
      )
      or
      "normal"
    )

    if land_type not in LAND_TYPE_MULTIPLIERS:
      land_type = "normal"

    try:
      latitude = float(
        data.get(
          "latitude"
        )
      )
      longitude = float(
        data.get(
          "longitude"
        )
      )
    except (
      TypeError,
      ValueError
    ):
      return jsonify({
        "error":
          "土地の位置情報が正しくありません"
      }), 400

    if not (
      -90 <= latitude <= 90
      and
      -180 <= longitude <= 180
    ):
      return jsonify({
        "error":
          "土地の位置情報が正しくありません"
      }), 400

    station_distance = data.get(
      "station_distance"
    )

    try:
      station_distance = float(
        station_distance
      )
    except (
      TypeError,
      ValueError
    ):
      station_distance = 999999.0

    try:
      area_m2 = max(
        0.0,
        float(
          data.get(
            "area_m2",
            0
          )
          or
          0
        )
      )
    except (
      TypeError,
      ValueError
    ):
      area_m2 = 0.0

    polygon = data.get(
      "polygon"
    )

    if isinstance(
      polygon,
      str
    ):
      try:
        polygon = json.loads(
          polygon
        )
      except Exception:
        polygon = []

    if not isinstance(
      polygon,
      list
    ):
      polygon = []

    polygon_json = json.dumps(
      polygon,
      ensure_ascii=False,
      separators=(
        ",",
        ":"
      )
    )

    osm_type = ""
    osm_id = ""

    cell_parts = cell_id.split(
      ":",
      2
    )

    if (
      len(
        cell_parts
      )
      ==
      3
      and
      cell_parts[0]
      ==
      "osm"
    ):
      osm_type = cell_parts[1]
      osm_id = cell_parts[2]

    price = calculate_land_price(
      land_type
    )

    daily_income = calculate_land_income(
      station_distance,
      land_name,
      land_type
    )

    init_game_db()

    with game_connect() as db:
      player = ensure_game_player(
        db,
        player_id
      )

      if not player["name"]:
        return jsonify({
          "error":
            "先にユーザー名を設定してください"
        }), 400

      settle_expired_buyouts(
        db
      )

      existing = db.execute(
        """
        SELECT *
        FROM game_lands
        WHERE cell_id = ?
        """,
        (
          cell_id,
        )
      ).fetchone()

      if (
        existing
        and
        existing["owner_id"]
      ):
        return jsonify({
          "error":
            "この土地には既に所有者がいます"
        }), 409

      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()

      if int(
        player["coins"]
      ) < price:
        return jsonify({
          "error":
            "コインが足りません"
        }), 400

      now = game_now()

      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins - ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          price,
          now,
          player_id
        )
      )

      values = (
        player_id,
        latitude,
        longitude,
        price,
        now,
        land_name,
        land_type,
        osm_type,
        osm_id,
        polygon_json,
        area_m2,
        station_distance,
        daily_income,
        now,
        land_name,
        price,
        latitude,
        longitude,
        now,
        now
      )

      if existing:
        db.execute(
          """
          UPDATE game_lands
          SET
            owner_id = ?,
            center_lat = ?,
            center_lon = ?,
            purchase_price = ?,
            acquired_at = ?,
            name = ?,
            land_type = ?,
            osm_type = ?,
            osm_id = ?,
            polygon_json = ?,
            area_m2 = ?,
            station_distance = ?,
            daily_income = ?,
            last_income_at = ?,
            land_name = ?,
            price = ?,
            latitude = ?,
            longitude = ?,
            created_at = ?,
            updated_at = ?
          WHERE cell_id = ?
          """,
          values
          +
          (
            cell_id,
          )
        )
      else:
        db.execute(
          """
          INSERT INTO game_lands (
            cell_id,
            owner_id,
            center_lat,
            center_lon,
            purchase_price,
            acquired_at,
            name,
            land_type,
            osm_type,
            osm_id,
            polygon_json,
            area_m2,
            station_distance,
            daily_income,
            last_income_at,
            land_name,
            price,
            latitude,
            longitude,
            created_at,
            updated_at
          )
          VALUES (
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?,
            ?
          )
          """,
          (
            cell_id,
          )
          +
          values
        )

      db.commit()

      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()

      return jsonify({
        "ok":
          True,
        "message":
          f"{land_name}を購入しました",
        "cell_id":
          cell_id,
        "price":
          price,
        "daily_income":
          daily_income,
        "player": {
          "id":
            player["id"],
          "name":
            player["name"],
          "coins":
            int(
              player["coins"]
            )
        }
      })

  except Exception as error:
    print(
      "GAME BUY ERROR:",
      error
    )

    return jsonify({
      "error":
        "土地を購入できませんでした"
    }), 500
@app.route(
  "/api/game/dev/make-me-gm",
  methods=["GET"]
)
def game_dev_make_me_gm():


  # ローカル環境だけ許可
  if request.remote_addr not in (
    "127.0.0.1",
    "::1"
  ):
    return jsonify({
      "error": "ローカル開発専用です"
    }), 403


  player_id = game_player_id()


  init_game_db()


  with game_connect() as db:


    ensure_game_player(
      db,
      player_id
    )


    db.execute(
      """
      UPDATE game_players
      SET
        coins = 1000000,
        is_game_master = 1
      WHERE player_id = ?
      """,
      (
        player_id,
      )
    )


    db.commit()


    player = db.execute(
      """
      SELECT
        coins,
        is_game_master
      FROM game_players
      WHERE player_id = ?
      """,
      (
        player_id,
      )
    ).fetchone()


    return jsonify({
      "ok": True,
      "coins": int(
        player["coins"]
      ),
      "is_game_master": bool(
        player["is_game_master"]
      )
    })
  
# ============================================================
# GAME / BUYOUT
# ============================================================
@app.route(
  "/api/game/cell/buyout",
  methods=["POST"]
)
def game_cell_buyout():
  player_id = game_player_id()
  try:
    data = (
      request.get_json(
        silent=True
      )
      or
      {}
    )
    cell_id = normalize_cell_id(
      data.get(
        "cell_id"
      )
    )
    if not cell_id:
      return jsonify({
        "error":
          "土地IDが正しくありません"
      }), 400
    init_game_db()
    with game_connect() as db:
      player = ensure_game_player(
        db,
        player_id
      )
      if not player["name"]:
        return jsonify({
          "error":
            "先にユーザー名を設定してください"
        }), 400
      settle_expired_buyouts(
        db
      )
      land = db.execute(
        """
        SELECT *
        FROM game_lands
        WHERE cell_id = ?
        """,
        (
          cell_id,
        )
      ).fetchone()
      if not land:
        return jsonify({
          "error":
            "土地が見つかりません"
        }), 404
      if not land["owner_id"]:
        return jsonify({
          "error":
            "未所有の土地は通常購入してください"
        }), 400
      if land["owner_id"] == player_id:
        return jsonify({
          "error":
            "自分の土地は買収できません"
        }), 400
      pending = db.execute(
        """
        SELECT *
        FROM game_buyouts
        WHERE
          cell_id = ?
          AND status = 'pending'
        LIMIT 1
        """,
        (
          cell_id,
        )
      ).fetchone()
      if pending:
        return jsonify({
          "error":
            "この土地は現在買収手続き中です"
        }), 409
      current_price = int(
        land["price"]
        or
        GAME_BASE_PRICE
      )
      offer_price = int(
        round(
          current_price
          *
          GAME_BUYOUT_MULTIPLIER
        )
      )
      defense_price = int(
        round(
          offer_price
          *
          GAME_DEFENSE_MULTIPLIER
        )
      )
      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()
      if player["coins"] < offer_price:
        return jsonify({
          "error":
            f"買収には{offer_price} coin必要です"
        }), 400
      now = game_now()
      expires_at = (
        now
        +
        GAME_BUYOUT_HOURS
        *
        3600
      )
      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins - ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          offer_price,
          now,
          player_id
        )
      )
      cursor = db.execute(
        """
        INSERT INTO game_buyouts (
          cell_id,
          challenger_id,
          owner_id,
          offer_price,
          defense_price,
          status,
          created_at,
          expires_at
        )
        VALUES (?, ?, ?, ?, ?, 'pending', ?, ?)
        """,
        (
          cell_id,
          player_id,
          land["owner_id"],
          offer_price,
          defense_price,
          now,
          expires_at
        )
      )
      buyout_id = cursor.lastrowid
      challenger_name = (
        player["name"]
        or
        "他のユーザー"
      )
      land_name = (
        land["land_name"]
        or
        "土地"
      )
      create_game_notification(
        db,
        land["owner_id"],
        "buyout_started",
        (
          f"{challenger_name}さんが"
          f"{land_name}を"
          f"{offer_price} coinで買収申請しました。"
          f"24時間以内に{defense_price} coinで"
          f"防衛できます。"
        ),
        cell_id,
        buyout_id
      )
      db.commit()
      return jsonify({
        "ok":
          True,
        "message":
          "買収申請を開始しました",
        "buyout": {
          "id":
            buyout_id,
          "cell_id":
            cell_id,
          "offer_price":
            offer_price,
          "defense_price":
            defense_price,
          "expires_at":
            expires_at,
          "status":
            "pending"
        }
      })
  except Exception as error:
    print(
      "GAME BUYOUT ERROR:",
      error
    )
    return jsonify({
      "error":
        "買収申請を開始できませんでした"
    }), 500
# ============================================================
# GAME / BUYOUT DEFENSE
# ============================================================
@app.route(
  "/api/game/buyout/<int:buyout_id>/defend",
  methods=["POST"]
)
def game_buyout_defend(
  buyout_id
):
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      buyout = db.execute(
        """
        SELECT *
        FROM game_buyouts
        WHERE id = ?
        """,
        (
          buyout_id,
        )
      ).fetchone()
      if not buyout:
        return jsonify({
          "error":
            "買収申請が見つかりません"
        }), 404
      if buyout["status"] != "pending":
        return jsonify({
          "error":
            "この買収申請は既に終了しています"
        }), 409
      if buyout["owner_id"] != player_id:
        return jsonify({
          "error":
            "この土地を防衛する権限がありません"
        }), 403
      now = game_now()
      if now >= buyout["expires_at"]:
        settle_expired_buyouts(
          db
        )
        return jsonify({
          "error":
            "24時間の防衛期限を過ぎています"
        }), 409
      owner = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()
      defense_price = int(
        buyout["defense_price"]
      )
      if owner["coins"] < defense_price:
        return jsonify({
          "error":
            f"防衛には{defense_price} coin必要です"
        }), 400
      land = db.execute(
        """
        SELECT *
        FROM game_lands
        WHERE cell_id = ?
        """,
        (
          buyout["cell_id"],
        )
      ).fetchone()
      if (
        not land
        or
        land["owner_id"] != player_id
      ):
        return jsonify({
          "error":
            "土地の所有状態が変更されています"
        }), 409
      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins - ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          defense_price,
          now,
          player_id
        )
      )
      # 買収申請時に預かった挑戦者のコインを返却します。
      db.execute(
        """
        UPDATE game_players
        SET
          coins = coins + ?,
          updated_at = ?
        WHERE id = ?
        """,
        (
          buyout["offer_price"],
          now,
          buyout["challenger_id"]
        )
      )
      # 防衛後の土地価格は防衛価格まで上昇します。
      db.execute(
        """
        UPDATE game_lands
        SET
          price = ?,
          updated_at = ?
        WHERE cell_id = ?
        """,
        (
          defense_price,
          now,
          buyout["cell_id"]
        )
      )
      db.execute(
        """
        UPDATE game_buyouts
        SET
          status = 'defended',
          resolved_at = ?
        WHERE id = ?
        """,
        (
          now,
          buyout_id
        )
      )
      owner_name = game_player_name(
        db,
        player_id
      )
      land_name = (
        land["land_name"]
        or
        "土地"
      )
      create_game_notification(
        db,
        buyout["challenger_id"],
        "buyout_defended",
        (
          f"{owner_name}さんが"
          f"{land_name}を防衛しました。"
          f"{buyout['offer_price']} coinは返金されました。"
        ),
        buyout["cell_id"],
        buyout_id
      )
      create_game_notification(
        db,
        player_id,
        "buyout_defended",
        (
          f"{land_name}の防衛に成功しました。"
        ),
        buyout["cell_id"],
        buyout_id
      )
      db.commit()
      return jsonify({
        "ok":
          True,
        "message":
          f"{land_name}を防衛しました",
        "price":
          defense_price
      })
  except Exception as error:
    print(
      "GAME DEFEND ERROR:",
      error
    )
    return jsonify({
      "error":
        "土地を防衛できませんでした"
    }), 500
# ============================================================
# GAME / BUYOUT LIST
# ============================================================
@app.route(
  "/api/game/buyouts",
  methods=["GET"]
)
def game_buyouts():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      rows = db.execute(
        """
        SELECT
          b.*,
          l.land_name,
          l.land_type,
          challenger.name AS challenger_name,
          owner.name AS owner_name
        FROM game_buyouts b
        LEFT JOIN game_lands l
          ON l.cell_id = b.cell_id
        LEFT JOIN game_players challenger
          ON challenger.id = b.challenger_id
        LEFT JOIN game_players owner
          ON owner.id = b.owner_id
        WHERE
          b.owner_id = ?
          OR
          b.challenger_id = ?
        ORDER BY
          b.created_at DESC
        LIMIT 100
        """,
        (
          player_id,
          player_id
        )
      ).fetchall()
      answer = []
      now = game_now()
      for row in rows:
        remaining_seconds = max(
          0,
          int(
            row["expires_at"]
            -
            now
          )
        )
        answer.append({
          "id":
            row["id"],
          "cell_id":
            row["cell_id"],
          "land_name":
            row["land_name"],
          "land_type":
            row["land_type"],
          "challenger_id":
            row["challenger_id"],
          "challenger_name":
            row["challenger_name"],
          "owner_id":
            row["owner_id"],
          "owner_name":
            row["owner_name"],
          "offer_price":
            row["offer_price"],
          "defense_price":
            row["defense_price"],
          "status":
            row["status"],
          "created_at":
            row["created_at"],
          "expires_at":
            row["expires_at"],
          "remaining_seconds":
            remaining_seconds,
          "can_defend":
            (
              row["status"]
              ==
              "pending"
              and
              row["owner_id"]
              ==
              player_id
              and
              remaining_seconds
              >
              0
            )
        })
      return jsonify({
        "ok":
          True,
        "buyouts":
          answer
      })
  except Exception as error:
    print(
      "GAME BUYOUT LIST ERROR:",
      error
    )
    return jsonify({
      "error":
        "買収情報を取得できませんでした"
    }), 500
# ============================================================
# GAME / NOTIFICATIONS
# ============================================================
@app.route(
  "/api/game/notifications",
  methods=["GET"]
)
def game_notifications():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      rows = db.execute(
        """
        SELECT *
        FROM game_notifications
        WHERE player_id = ?
        ORDER BY created_at DESC
        LIMIT 100
        """,
        (
          player_id,
        )
      ).fetchall()
      notifications = []
      for row in rows:
        notifications.append({
          "id":
            row["id"],
          "type":
            row["type"],
          "message":
            row["message"],
          "cell_id":
            row["cell_id"],
          "buyout_id":
            row["buyout_id"],
          "is_read":
            bool(
              row["is_read"]
            ),
          "created_at":
            row["created_at"]
        })
      unread_count = sum(
        1
        for kinako in notifications
        if not kinako["is_read"]
      )
      return jsonify({
        "ok":
          True,
        "notifications":
          notifications,
        "unread_count":
          unread_count
      })
  except Exception as error:
    print(
      "GAME NOTIFICATION ERROR:",
      error
    )
    return jsonify({
      "error":
        "通知を取得できませんでした"
    }), 500
@app.route(
  "/api/game/notifications/read",
  methods=["POST"]
)
def game_notifications_read():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      db.execute(
        """
        UPDATE game_notifications
        SET is_read = 1
        WHERE player_id = ?
        """,
        (
          player_id,
        )
      )
      db.commit()
      return jsonify({
        "ok":
          True
      })
  except Exception as error:
    print(
      "GAME NOTIFICATION READ ERROR:",
      error
    )
    return jsonify({
      "error":
        "通知を既読にできませんでした"
    }), 500
# ============================================================
# GAME / RANKING
# ============================================================
@app.route(
  "/api/game/ranking",
  methods=["GET"]
)
def game_ranking():
  player_id = game_player_id()
  try:
    init_game_db()
    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )
      settle_expired_buyouts(
        db
      )
      settle_land_income(
        db
      )
      rows = db.execute(
        """
        SELECT
          p.id,
          p.name,
          p.coins,
          COUNT(l.cell_id)
            AS land_count,
          COALESCE(
            SUM(l.price),
            0
          )
            AS total_land_value,
          COALESCE(
            SUM(l.daily_income),
            0
          )
            AS daily_income
        FROM game_players p
        LEFT JOIN game_lands l
          ON l.owner_id = p.id
        WHERE
          p.name IS NOT NULL
          AND
          TRIM(p.name) != ''
        GROUP BY
          p.id,
          p.name,
          p.coins
        ORDER BY
          land_count DESC,
          total_land_value DESC,
          p.coins DESC,
          p.name ASC
        """
      ).fetchall()
      ranking = []
      my_rank = None
      for (
        kinako,
        row
      ) in enumerate(
        rows,
        start=1
      ):
        item = {
          "rank":
            kinako,
          "player_id":
            row["id"],
          "name":
            row["name"],
          "coins":
            row["coins"],
          "land_count":
            row["land_count"],
          "total_land_value":
            row["total_land_value"],
          "daily_income":
            row["daily_income"],
          "mine":
            (
              row["id"]
              ==
              player_id
            )
        }
        if item["mine"]:
          my_rank = item
        if kinako <= 50:
          ranking.append(
            item
          )
      return jsonify({
        "ok":
          True,
        "ranking":
          ranking,
        "my_rank":
          my_rank,
        "total_players":
          len(
            rows
          )
      })
  except Exception as error:
    print(
      "GAME RANKING ERROR:",
      error
    )
    return jsonify({
      "error":
        "ランキングを取得できませんでした"
    }), 500
# ============================================================
# GAME / MAP UTILITIES
# ============================================================


EARTH_RADIUS_METERS = 6371000


OVERPASS_URL = os.environ.get(
  "OVERPASS_URL",
  "https://overpass-api.de/api/interpreter"
)


GAME_MAP_RADIUS = int(
  os.environ.get(
    "GAME_MAP_RADIUS",
    "700"
  )
)


GAME_MAP_MAX_FEATURES = int(
  os.environ.get(
    "GAME_MAP_MAX_FEATURES",
    "250"
  )
)




def distance_meters(
  lat1,
  lon1,
  lat2,
  lon2
):


  try:


    lat1 = float(
      lat1
    )


    lon1 = float(
      lon1
    )


    lat2 = float(
      lat2
    )


    lon2 = float(
      lon2
    )


  except (
    TypeError,
    ValueError
  ):


    return 999999.0


  phi1 = math.radians(
    lat1
  )


  phi2 = math.radians(
    lat2
  )


  delta_phi = math.radians(
    lat2
    -
    lat1
  )


  delta_lambda = math.radians(
    lon2
    -
    lon1
  )


  kinako = (
    math.sin(
      delta_phi / 2
    )
    **
    2
    +
    math.cos(
      phi1
    )
    *
    math.cos(
      phi2
    )
    *
    math.sin(
      delta_lambda / 2
    )
    **
    2
  )


  kinako = min(
    1.0,
    max(
      0.0,
      kinako
    )
  )


  return (
    EARTH_RADIUS_METERS
    *
    2
    *
    math.asin(
      math.sqrt(
        kinako
      )
    )
  )




def polygon_center(
  geometry
):


  if not geometry:


    return (
      None,
      None
    )


  latitudes = []


  longitudes = []


  for point in geometry:


    try:


      latitude = float(
        point.get(
          "lat"
        )
      )


      longitude = float(
        point.get(
          "lon"
        )
      )


    except (
      TypeError,
      ValueError,
      AttributeError
    ):


      continue


    latitudes.append(
      latitude
    )


    longitudes.append(
      longitude
    )


  if not latitudes:


    return (
      None,
      None
    )


  return (
    sum(
      latitudes
    )
    /
    len(
      latitudes
    ),


    sum(
      longitudes
    )
    /
    len(
      longitudes
    )
  )




def polygon_area_rough(
  geometry
):


  if (
    not geometry
    or
    len(
      geometry
    )
    <
    3
  ):


    return 0.0


  center_lat, center_lon = polygon_center(
    geometry
  )


  if (
    center_lat is None
    or
    center_lon is None
  ):


    return 0.0


  meter_per_lat = 111320.0


  meter_per_lon = (
    111320.0
    *
    math.cos(
      math.radians(
        center_lat
      )
    )
  )


  points = []


  for point in geometry:


    try:


      x = (
        float(
          point[
            "lon"
          ]
        )
        -
        center_lon
      ) * meter_per_lon


      y = (
        float(
          point[
            "lat"
          ]
        )
        -
        center_lat
      ) * meter_per_lat


    except (
      KeyError,
      TypeError,
      ValueError
    ):


      continue


    points.append(
      (
        x,
        y
      )
    )


  if len(
    points
  ) < 3:


    return 0.0


  area = 0.0


  for kinako in range(
    len(
      points
    )
  ):


    x1, y1 = points[
      kinako
    ]


    x2, y2 = points[
      (
        kinako
        +
        1
      )
      %
      len(
        points
      )
    ]


    area += (
      x1
      *
      y2
      -
      x2
      *
      y1
    )


  return abs(
    area
  ) / 2




def classify_osm_land(
  tags
):


  tags = (
    tags
    or
    {}
  )


  railway = str(
    tags.get(
      "railway",
      ""
    )
  ).casefold()


  public_transport = str(
    tags.get(
      "public_transport",
      ""
    )
  ).casefold()


  building = str(
    tags.get(
      "building",
      ""
    )
  ).casefold()


  shop = str(
    tags.get(
      "shop",
      ""
    )
  ).casefold()


  amenity = str(
    tags.get(
      "amenity",
      ""
    )
  ).casefold()


  tourism = str(
    tags.get(
      "tourism",
      ""
    )
  ).casefold()


  landuse = str(
    tags.get(
      "landuse",
      ""
    )
  ).casefold()


  leisure = str(
    tags.get(
      "leisure",
      ""
    )
  ).casefold()


  name = str(
    tags.get(
      "name",
      ""
    )
  ).casefold()


  if (
    railway
    ==
    "station"
    or
    public_transport
    ==
    "station"
    or
    building
    ==
    "train_station"
  ):


    if any(
      keyword
      in
      name
      for keyword in [
        "tokyo",
        "東京",
        "shinjuku",
        "新宿",
        "shibuya",
        "渋谷",
        "nagoya",
        "名古屋",
        "osaka",
        "大阪",
        "kyoto",
        "京都",
        "shizuoka",
        "静岡"
      ]
    ):


      return "station_major"


    return "station"


  if (
    shop
    ==
    "mall"
    or
    building
    ==
    "mall"
  ):


    return "mall"


  if shop == "supermarket":


    return "supermarket"


  if tourism == "hotel":


    return "hotel"


  if amenity == "hospital":


    return "hospital"


  if amenity in {
    "restaurant",
    "fast_food",
    "cafe"
  }:


    return "restaurant"


  if (
    building
    in {
      "retail",
      "commercial"
    }
    or
    landuse
    ==
    "commercial"
  ):


    return "commercial"


  if (
    building
    ==
    "office"
    or
    landuse
    ==
    "office"
  ):


    return "office"


  if (
    building
    in {
      "residential",
      "apartments",
      "house",
      "detached"
    }
    or
    landuse
    ==
    "residential"
  ):


    return "residential"


  if leisure in {
    "park",
    "garden"
  }:


    return "normal"


  if shop:


    return "commercial"


  if amenity:


    return "commercial"


  if building:


    return "normal"


  return "normal"




def osm_land_name(
  tags,
  land_type
):


  tags = (
    tags
    or
    {}
  )


  name = str(
    tags.get(
      "name"
    )
    or
    tags.get(
      "name:ja"
    )
    or
    ""
  ).strip()


  if name:


    return name[:100]


  default_names = {
    "station_major":
      "主要駅",


    "station":
      "駅",


    "mall":
      "大型商業施設",


    "supermarket":
      "スーパーマーケット",


    "hotel":
      "ホテル",


    "hospital":
      "病院",


    "restaurant":
      "飲食店",


    "commercial":
      "商業施設",


    "office":
      "オフィス",


    "residential":
      "住宅",


    "normal":
      "土地"
  }


  return default_names.get(
    land_type,
    "土地"
  )




def serialize_land(row, player_id):
  if row is None:
    return None


  pending = None


  try:
    pending = row["buyout_id"]
  except Exception:
    pass


  price = int(row["purchase_price"])


  # ==========================================
  # 保存済み土地ポリゴンをJSONから復元
  # ==========================================


  polygon = []


  try:
    raw_polygon = row["polygon_json"]


    if raw_polygon:
      polygon = json.loads(raw_polygon)


      if not isinstance(polygon, list):
        polygon = []


  except Exception:
    polygon = []


  return {
    "cell": row["cell_id"],
    "id": row["cell_id"],


    "owner": row["owner_id"],
    "owner_id": row["owner_id"],


    "owner_name":
      row["owner_name"]
      if "owner_name" in row.keys()
      else "",


    "lat": float(row["center_lat"]),
    "lon": float(row["center_lon"]),


    "price": price,
    "purchase_price": price,


    "takeover_price":
      int(
        math.ceil(
          price
          * 2.0
        )
      ),


    "mine":
      row["owner_id"]
      == player_id,


    "owned":
      True,


    "name":
      row["name"],


    "land_type":
      row["land_type"],


    "station_distance":
      float(
        row["station_distance"]
      ),


    "daily_income":
      int(
        row["daily_income"]
      ),


    # ★重要
    # JSON文字列ではなくJSがそのまま使える配列で返す
    "polygon":
      polygon,


    "area_m2":
      float(
        row["area_m2"] or 0
      ),


    "pending_buyout":
      bool(pending),


    "buyout_id":
      pending,
  }


def nearest_station_distance(
  latitude,
  longitude,
  stations
):


  if (
    latitude is None
    or
    longitude is None
    or
    not stations
  ):


    return 999999.0


  best = 999999.0


  for station in stations:


    distance = distance_meters(
      latitude,
      longitude,
      station[
        "lat"
      ],
      station[
        "lon"
      ]
    )


    if distance < best:


      best = distance


  return best




def osm_feature_id(
  element
):


  element_type = str(
    element.get(
      "type",
      ""
    )
  )


  element_id = element.get(
    "id"
  )


  if (
    element_type
    not in {
      "node",
      "way",
      "relation"
    }
    or
    element_id is None
  ):


    return None


  return (
    f"osm:{element_type}:{element_id}"
  )






def overpass_query(
  latitude,
  longitude,
  radius
):


  # 最大250mまでに制限して高速化
  radius = min(
    int(float(radius)),
    250
  )


  return f"""
  [out:json][timeout:6];


  (
    way["building"]
      (around:{radius},{latitude},{longitude});


    way["railway"="station"]
      (around:{radius},{latitude},{longitude});


    way["building"="train_station"]
      (around:{radius},{latitude},{longitude});


    way["public_transport"="station"]
      (around:{radius},{latitude},{longitude});


    way["shop"="mall"]
      (around:{radius},{latitude},{longitude});


    way["shop"="supermarket"]
      (around:{radius},{latitude},{longitude});


    way["building"="retail"]
      (around:{radius},{latitude},{longitude});


    way["amenity"="hospital"]
      (around:{radius},{latitude},{longitude});


    way["tourism"="hotel"]
      (around:{radius},{latitude},{longitude});


    way["leisure"="park"]
      (around:{radius},{latitude},{longitude});
  );


  out tags center geom;
  """






def fetch_osm_elements(
  latitude,
  longitude,
  radius
):


  cache_key = (
    f"osm:"
    f"{float(latitude):.3f}:"
    f"{float(longitude):.3f}:"
    f"{int(radius)}"
  )


  cached = get_cache(
    cache_key,
    3600
  )


  if cached is not None:


    return cached


  query = overpass_query(
    latitude,
    longitude,
    radius
  )


  response = requests.post(
    OVERPASS_URL,
    data={
      "data":
        query
    },
    headers={
      "User-Agent":
        "TravelLife/2.0"
    },
    timeout=25
  )


  response.raise_for_status()


  source = response.json()


  elements = source.get(
    "elements",
    []
  )


  save_cache(
    cache_key,
    elements
  )


  return elements




def build_osm_parcels(
  elements
):


  stations = []


  for element in elements:


    tags = (
      element.get(
        "tags"
      )
      or
      {}
    )


    railway = tags.get(
      "railway"
    )


    public_transport = tags.get(
      "public_transport"
    )


    if (
      railway
      !=
      "station"
      and
      public_transport
      !=
      "station"
    ):


      continue


    latitude = element.get(
      "lat"
    )


    longitude = element.get(
      "lon"
    )


    if (
      latitude is None
      or
      longitude is None
    ):


      center = (
        element.get(
          "center"
        )
        or
        {}
      )


      latitude = center.get(
        "lat"
      )


      longitude = center.get(
        "lon"
      )


    if (
      latitude is None
      or
      longitude is None
    ):


      geometry = element.get(
        "geometry",
        []
      )


      latitude, longitude = polygon_center(
        geometry
      )


    if (
      latitude is None
      or
      longitude is None
    ):


      continue


    stations.append({
      "lat":
        float(
          latitude
        ),


      "lon":
        float(
          longitude
        )
    })


  parcels = []


  used_ids = set()


  for element in elements:


    cell_id = osm_feature_id(
      element
    )


    if (
      not cell_id
      or
      cell_id in used_ids
    ):


      continue


    tags = (
      element.get(
        "tags"
      )
      or
      {}
    )


    land_type = classify_osm_land(
      tags
    )


    geometry = element.get(
      "geometry",
      []
    )


    latitude = element.get(
      "lat"
    )


    longitude = element.get(
      "lon"
    )


    if (
      latitude is None
      or
      longitude is None
    ):


      center = (
        element.get(
          "center"
        )
        or
        {}
      )


      latitude = center.get(
        "lat"
      )


      longitude = center.get(
        "lon"
      )


    if (
      latitude is None
      or
      longitude is None
    ):


      latitude, longitude = polygon_center(
        geometry
      )


    if (
      latitude is None
      or
      longitude is None
    ):


      continue


    latitude = float(
      latitude
    )


    longitude = float(
      longitude
    )


    station_distance = nearest_station_distance(
      latitude,
      longitude,
      stations
    )


    name = osm_land_name(
      tags,
      land_type
    )


    area_m2 = polygon_area_rough(
      geometry
    )


    base_price = calculate_land_price(
      land_type
    )


    area_multiplier = 1.0


    if area_m2 >= 10000:


      area_multiplier = 1.8


    elif area_m2 >= 5000:


      area_multiplier = 1.5


    elif area_m2 >= 2000:


      area_multiplier = 1.3


    elif area_m2 >= 500:


      area_multiplier = 1.15


    station_multiplier = 1.0


    if station_distance <= 100:


      station_multiplier = 1.4


    elif station_distance <= 300:


      station_multiplier = 1.25


    elif station_distance <= 500:


      station_multiplier = 1.15


    price = int(
      round(
        base_price
        *
        area_multiplier
        *
        station_multiplier
      )
    )


    price = max(
      300,
      price
    )


    daily_income = calculate_land_income(
      station_distance,
      name,
      land_type
    )


    parcel = {
      "cell_id":
        cell_id,


      "land_name":
        name,


      "land_type":
        land_type,


      "latitude":
        latitude,


      "longitude":
        longitude,


      "station_distance":
        round(
          station_distance,
          1
        ),


      "daily_income":
        daily_income,


      "price":
        price,


      "area_m2":
        round(
          area_m2,
          1
        ),


      "polygon":
        __import__("json").dumps(
          geometry
        ),


      "osm_tags":
        {
          key:
            value
          for (
            key,
            value
          ) in tags.items()
          if key in {
            "name",
            "name:ja",
            "building",
            "railway",
            "public_transport",
            "shop",
            "amenity",
            "tourism",
            "landuse"
          }
        }
    }


    parcels.append(
      parcel
    )


    used_ids.add(
      cell_id
    )


    if (
      len(
        parcels
      )
      >=
      GAME_MAP_MAX_FEATURES
    ):


      break


  return parcels




# ============================================================
# GAME / FALLBACK GRID
# ============================================================


def grid_cell_size():


  return 0.001




def make_grid_cell_id(
  latitude,
  longitude
):


  size = grid_cell_size()


  row = math.floor(
    float(
      latitude
    )
    /
    size
  )


  col = math.floor(
    float(
      longitude
    )
    /
    size
  )


  return (
    f"grid:{row}:{col}"
  )




def grid_cell_polygon(
  latitude,
  longitude
):


  size = grid_cell_size()


  row = math.floor(
    float(
      latitude
    )
    /
    size
  )


  col = math.floor(
    float(
      longitude
    )
    /
    size
  )


  south = row * size


  north = (
    row
    +
    1
  ) * size


  west = col * size


  east = (
    col
    +
    1
  ) * size


  return [
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




def build_grid_parcels(
  latitude,
  longitude,
  radius_cells=4
):


  size = grid_cell_size()


  center_row = math.floor(
    float(
      latitude
    )
    /
    size
  )


  center_col = math.floor(
    float(
      longitude
    )
    /
    size
  )


  parcels = []


  for kinako in range(
    center_row
    -
    radius_cells,
    center_row
    +
    radius_cells
    +
    1
  ):


    for kenako in range(
      center_col
      -
      radius_cells,
      center_col
      +
      radius_cells
      +
      1
    ):


      south = kinako * size


      north = (
        kinako
        +
        1
      ) * size


      west = kenako * size


      east = (
        kenako
        +
        1
      ) * size


      center_lat = (
        south
        +
        north
      ) / 2


      center_lon = (
        west
        +
        east
      ) / 2


      cell_id = (
        f"grid:{kinako}:{kenako}"
      )


      parcels.append({
        "cell_id":
          cell_id,


        "land_name":
          "通常区画",


        "land_type":
          "normal",


        "latitude":
          center_lat,


        "longitude":
          center_lon,


        "station_distance":
          999999,


        "daily_income":
          6,


        "price":
          GAME_BASE_PRICE,


        "area_m2":
          10000,


        "polygon": [
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
      })


  return parcels




# ============================================================
# GAME / MAP
# ============================================================
# ============================================================
# GAME / OWNERSHIP MAP
# ============================================================


@app.route(
  "/api/game/ownership/map",
  methods=["GET"]
)
def game_ownership_map():


  player_id = game_player_id()


  # ==========================================
  # 位置情報
  # ==========================================


  try:


    latitude = float(
      request.args.get(
        "latitude",
        ""
      )
    )


    longitude = float(
      request.args.get(
        "longitude",
        ""
      )
    )


    radius = float(
      request.args.get(
        "radius",
        3000
      )
    )


  except Exception:


    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400




  if not (
    -90 <= latitude <= 90
    and
    -180 <= longitude <= 180
  ):


    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400




  # 最大10km
  radius = max(
    500,
    min(
      radius,
      10000
    )
  )




  # ==========================================
  # 緯度経度の検索範囲
  # ==========================================


  lat_margin = (
    radius /
    111000
  )


  cos_lat = max(
    0.2,
    math.cos(
      math.radians(
        latitude
      )
    )
  )


  lon_margin = (
    radius /
    (
      111000 *
      cos_lat
    )
  )




  south = (
    latitude -
    lat_margin
  )


  north = (
    latitude +
    lat_margin
  )


  west = (
    longitude -
    lon_margin
  )


  east = (
    longitude +
    lon_margin
  )




  try:


    init_game_db()


    with game_connect() as db:


      # ==================================
      # 期限切れ買収を確定
      # ==================================


      settle_expired_buyouts(
        db
      )


      db.commit()




      # ==================================
      # 周辺の購入済み土地を取得
      # ==================================


      rows = db.execute(
        """
        SELECT
          l.*,
          p.name AS owner_name,
          b.id AS buyout_id


        FROM game_lands l


        LEFT JOIN game_players p
          ON p.player_id =
            l.owner_id


        LEFT JOIN game_buyouts b
          ON b.cell_id =
            l.cell_id
          AND b.status =
            'pending'


        WHERE
          l.center_lat
          BETWEEN ? AND ?


          AND


          l.center_lon
          BETWEEN ? AND ?


        LIMIT 2000
        """,


        (
          south,
          north,
          west,
          east
        )


      ).fetchall()




      lands = []




      # ==================================
      # 本当にradius内か確認
      # ==================================


      for row in rows:


        land_lat = float(
          row[
            "center_lat"
          ]
        )


        land_lon = float(
          row[
            "center_lon"
          ]
        )




        # ------------------------------
        # Haversine距離
        # ------------------------------


        radius_earth = 6371000


        lat1 = math.radians(
          latitude
        )


        lat2 = math.radians(
          land_lat
        )


        delta_lat = (
          lat2 -
          lat1
        )


        delta_lon = math.radians(
          land_lon -
          longitude
        )


        value = (
          math.sin(
            delta_lat / 2
          ) ** 2
          +
          math.cos(
            lat1
          )
          *
          math.cos(
            lat2
          )
          *
          math.sin(
            delta_lon / 2
          ) ** 2
        )


        distance = (
          radius_earth
          *
          2
          *
          math.asin(
            math.sqrt(
              min(
                1,
                max(
                  0,
                  value
                )
              )
            )
          )
        )




        if distance > radius:


          continue




        # ==================================
        # serialize_landで土地情報作成
        # ==================================


        land = serialize_land(
          row,
          player_id
        )




        if land is None:


          continue




        land[
          "distance"
        ] = round(
          distance,
          1
        )




        lands.append(
          land
        )




      # ==================================
      # 所有者数
      # ==================================


      owner_ids = {
        land.get(
          "owner_id"
        )
        for land in lands


        if land.get(
          "owner_id"
        )
      }




      return jsonify({


        "ok":
          True,


        "lands":
          lands,


        "count":
          len(
            lands
          ),


        "conquerors":
          len(
            owner_ids
          ),


        "latitude":
          latitude,


        "longitude":
          longitude,


        "radius":
          radius


      })




  except Exception as error:


    print(
      "GAME OWNERSHIP MAP ERROR:",
      error
    )


    return jsonify({
      "error":
        "土地情報を取得できませんでした"
    }), 500




  if not (
    -90 <= latitude <= 90
    and
    -180 <= longitude <= 180
  ):


    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400




  # 最大10km
  radius = max(
    500,
    min(
      radius,
      10000
    )
  )




  # ========================================================
  # 表示範囲を緯度経度へ変換
  # ========================================================


  lat_delta = (
    radius
    /
    111320.0
  )




  lon_scale = max(
    0.20,
    math.cos(
      math.radians(
        latitude
      )
    )
  )




  lon_delta = (
    radius
    /
    (
      111320.0
      *
      lon_scale
    )
  )




  south = (
    latitude
    -
    lat_delta
  )


  north = (
    latitude
    +
    lat_delta
  )


  west = (
    longitude
    -
    lon_delta
  )


  east = (
    longitude
    +
    lon_delta
  )




  try:


    init_game_db()




    with game_connect() as db:


      ensure_game_player(
        db,
        player_id
      )




      # ================================================
      # 期限切れ買収を処理
      # ================================================


      try:


        settle_expired_buyouts(
          db
        )


      except Exception:


        pass




      db.commit()




      # ================================================
      # この範囲に存在する購入済み土地だけ取得
      #
      # 建物形状そのものはブラウザ側で表示するため、
      # Overpass APIはここでは一切使用しない
      # ================================================


      rows = db.execute(
        """
        SELECT
          l.cell_id,
          l.owner_id,
          l.land_name,
          l.land_type,
          l.price,
          l.latitude,
          l.longitude,
          l.station_distance,
          l.daily_income,
          p.name AS owner_name


        FROM game_lands l


        LEFT JOIN game_players p
          ON p.id = l.owner_id


        WHERE
          l.latitude BETWEEN ? AND ?
          AND
          l.longitude BETWEEN ? AND ?
        """,
        (
          south,
          north,
          west,
          east
        )
      ).fetchall()




      # ================================================
      # 買収申請中の土地
      # ================================================


      pending_cells = set()




      try:


        pending_rows = db.execute(
          """
          SELECT
            cell_id


          FROM game_buyouts


          WHERE
            status = 'pending'
          """
        ).fetchall()




        for row in pending_rows:


          pending_cells.add(
            row[
              "cell_id"
            ]
          )


      except Exception:


        pass




      lands = []




      for row in rows:


        owner_id = row[
          "owner_id"
        ]




        lands.append({


          "cell_id":
            row[
              "cell_id"
            ],


          "owner_id":
            owner_id,


          "owner_name":
            (
              row[
                "owner_name"
              ]
              or
              "プレイヤー"
            ),


          "land_name":
            (
              row[
                "land_name"
              ]
              or
              "土地"
            ),


          "land_type":
            (
              row[
                "land_type"
              ]
              or
              "normal"
            ),


          "price":
            int(
              row[
                "price"
              ]
              or
              GAME_BASE_PRICE
            ),


          "latitude":
            float(
              row[
                "latitude"
              ]
              or
              0
            ),


          "longitude":
            float(
              row[
                "longitude"
              ]
              or
              0
            ),


          "station_distance":
            float(
              row[
                "station_distance"
              ]
              or
              999999
            ),


          "daily_income":
            int(
              row[
                "daily_income"
              ]
              or
              0
            ),


          "mine":
            (
              owner_id
              ==
              player_id
            ),


          "buyout_pending":
            (
              row[
                "cell_id"
              ]
              in
              pending_cells
            )
        })




      # ================================================
      # 現在プレイヤー
      # ================================================


      player = db.execute(
        """
        SELECT
          id,
          name,
          coins


        FROM game_players


        WHERE
          id = ?
        """,
        (
          player_id,
        )
      ).fetchone()




      # ================================================
      # 自分の所有土地数・1日収益
      # ================================================


      player_stats = db.execute(
        """
        SELECT
          COUNT(*) AS land_count,


          COALESCE(
            SUM(
              daily_income
            ),
            0
          ) AS daily_income


        FROM game_lands


        WHERE
          owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()




      # ================================================
      # 全プレイヤー数
      # ================================================


      total_player_row = db.execute(
        """
        SELECT
          COUNT(*) AS count


        FROM game_players
        """
      ).fetchone()




      # ================================================
      # 全購入済み土地数
      # ================================================


      total_land_row = db.execute(
        """
        SELECT
          COUNT(*) AS count


        FROM game_lands
        """
      ).fetchone()




      # ================================================
      # 現在表示範囲の所有者数
      # ================================================


      local_owner_ids = set()




      for row in rows:


        if row[
          "owner_id"
        ]:


          local_owner_ids.add(
            row[
              "owner_id"
            ]
          )




      # ================================================
      # プレイヤー情報
      # ================================================


      player_data = {


        "id":
          player_id,


        "name":
          (
            player[
              "name"
            ]
            if player
            else None
          ),


        "coins":
          int(
            player[
              "coins"
            ]
            if player
            else GAME_NORMAL_START_COINS
          ),


        "land_count":
          int(
            player_stats[
              "land_count"
            ]
            if player_stats
            else 0
          ),


        "daily_income":
          int(
            player_stats[
              "daily_income"
            ]
            if player_stats
            else 0
          )
      }




      # ================================================
      # JSON返却
      # ================================================


      return jsonify({


        "ok":
          True,


        "player":
          player_data,


        "lands":
          lands,


        "parcels":
          lands,


        "local_conquerors":
          len(
            local_owner_ids
          ),


        "total_conquerors":
          int(
            total_player_row[
              "count"
            ]
          ),


        "total_lands":
          int(
            total_land_row[
              "count"
            ]
          )
      })




  except Exception as error:


    print(
      "GAME OWNERSHIP MAP ERROR:",
      error
    )




    return jsonify({
      "error":
        "土地所有情報を取得できませんでした"
    }), 500
@app.route(
  "/api/game/land-candidates",
  methods=["GET"]
)
def game_land_candidates():


  try:
    latitude = float(
      request.args.get("latitude", "")
    )
    longitude = float(
      request.args.get("longitude", "")
    )
    radius = float(
      request.args.get("radius", 1500)
    )


  except (TypeError, ValueError):
    return jsonify({
      "error": "位置情報が正しくありません"
    }), 400


  if not (
    -90 <= latitude <= 90
    and -180 <= longitude <= 180
  ):
    return jsonify({
      "error": "位置情報が正しくありません"
    }), 400


  radius = max(
    300,
    min(radius, 2500)
  )


  lat_margin = radius / 111000


  cos_lat = max(
    0.2,
    math.cos(
      math.radians(latitude)
    )
  )


  lon_margin = (
    radius /
    (111000 * cos_lat)
  )


  south = latitude - lat_margin
  north = latitude + lat_margin
  west = longitude - lon_margin
  east = longitude + lon_margin


  query = f"""
  [out:json][timeout:20];
  (
    way["building"]({south},{west},{north},{east});
    way["railway"="station"]({south},{west},{north},{east});
    way["shop"="mall"]({south},{west},{north},{east});
    way["shop"="supermarket"]({south},{west},{north},{east});
    way["landuse"="retail"]({south},{west},{north},{east});
    way["landuse"="commercial"]({south},{west},{north},{east});
    way["tourism"="hotel"]({south},{west},{north},{east});
    way["amenity"="hospital"]({south},{west},{north},{east});
  );
  out geom tags;
  """


  try:
    response = requests.post(
      "https://overpass-api.de/api/interpreter",
      data={
        "data": query
      },
      headers={
        "User-Agent": "TravelLife/3.0"
      },
      timeout=25
    )


    response.raise_for_status()
    source = response.json()


  except Exception as error:
    print(
      "LAND CANDIDATES ERROR:",
      error
    )


    return jsonify({
      "ok": True,
      "lands": [],
      "count": 0
    })


  def distance_meters(
    lat1,
    lon1,
    lat2,
    lon2
  ):
    earth = 6371000


    p1 = math.radians(lat1)
    p2 = math.radians(lat2)


    delta_lat = math.radians(
      lat2 - lat1
    )


    delta_lon = math.radians(
      lon2 - lon1
    )


    value = (
      math.sin(delta_lat / 2) ** 2
      +
      math.cos(p1)
      *
      math.cos(p2)
      *
      math.sin(delta_lon / 2) ** 2
    )


    return (
      earth
      *
      2
      *
      math.asin(
        math.sqrt(
          min(
            1,
            max(0, value)
          )
        )
      )
    )


  def polygon_area_m2(polygon):


    if len(polygon) < 3:
      return 100


    center_lat = (
      sum(
        point[0]
        for point in polygon
      )
      / len(polygon)
    )


    cos_center = max(
      0.2,
      math.cos(
        math.radians(
          center_lat
        )
      )
    )


    points = []


    for point in polygon:
      points.append((
        point[1]
        * 111000
        * cos_center,


        point[0]
        * 111000
      ))


    area = 0


    for kinako in range(
      len(points)
    ):
      kenako = (
        kinako + 1
      ) % len(points)


      area += (
        points[kinako][0]
        *
        points[kenako][1]
      )


      area -= (
        points[kenako][0]
        *
        points[kinako][1]
      )


    return max(
      20,
      abs(area) / 2
    )


  price_table = {
    "station": 3.5,
    "mall": 4.0,
    "supermarket": 2.5,
    "commercial": 1.8,
    "hotel": 3.0,
    "hospital": 3.0,
    "office": 1.5,
    "residential": 1.0,
    "normal": 0.8
  }


  lands = []
  used_cells = set()


  for element in source.get(
    "elements",
    []
  ):


    geometry = (
      element.get("geometry")
      or []
    )


    polygon = []


    for point in geometry:


      try:
        polygon.append([
          float(point["lat"]),
          float(point["lon"])
        ])


      except (
        KeyError,
        TypeError,
        ValueError
      ):
        continue


    if len(polygon) < 3:
      continue


    center_lat = (
      sum(
        point[0]
        for point in polygon
      )
      / len(polygon)
    )


    center_lon = (
      sum(
        point[1]
        for point in polygon
      )
      / len(polygon)
    )


    distance = distance_meters(
      latitude,
      longitude,
      center_lat,
      center_lon
    )


    if distance > radius:
      continue


    tags = (
      element.get("tags")
      or {}
    )


    osm_id = str(
      element.get("id", "")
    )


    cell = (
      f"osm:way:{osm_id}"
    )


    if cell in used_cells:
      continue


    used_cells.add(cell)


    name = (
      tags.get("name")
      or tags.get("brand")
      or tags.get("operator")
      or "建物"
    )


    building = tags.get(
      "building",
      ""
    )


    shop = tags.get(
      "shop",
      ""
    )


    railway = tags.get(
      "railway",
      ""
    )


    landuse = tags.get(
      "landuse",
      ""
    )


    tourism = tags.get(
      "tourism",
      ""
    )


    amenity = tags.get(
      "amenity",
      ""
    )


    if railway == "station":
      land_type = "station"


    elif shop == "mall":
      land_type = "mall"


    elif shop == "supermarket":
      land_type = "supermarket"


    elif (
      landuse == "retail"
      or
      landuse == "commercial"
    ):
      land_type = "commercial"


    elif tourism == "hotel":
      land_type = "hotel"


    elif amenity == "hospital":
      land_type = "hospital"


    elif building == "office":
      land_type = "office"


    elif building in {
      "apartments",
      "residential",
      "house",
      "detached"
    }:
      land_type = "residential"


    else:
      land_type = "normal"


    area_m2 = polygon_area_m2(
      polygon
    )


    multiplier = price_table.get(
      land_type,
      1.0
    )


    price = max(
      300,
      int(
        GAME_BASE_PRICE
        *
        multiplier
      )
    )


    lands.append({
      "cell": cell,
      "cell_id": cell,
      "name": name,
      "land_type": land_type,
      "osm_type": "way",
      "osm_id": osm_id,
      "lat": center_lat,
      "lon": center_lon,
      "latitude": center_lat,
      "longitude": center_lon,
      "polygon": polygon,
      "area_m2": round(
        area_m2,
        1
      ),
      "distance": round(
        distance,
        1
      ),
      "price": price
    })


  lands.sort(
    key=lambda kinako:
      kinako["area_m2"],
    reverse=True
  )


  return jsonify({
    "ok": True,
    "lands": lands[:700],
    "count": min(
      len(lands),
      700
    )
  })


@app.route(
  "/api/game/map",
  methods=["GET"]
)
def game_map():


  player_id = game_player_id()


  latitude = request.args.get(
    "lat"
  )


  longitude = request.args.get(
    "lon"
  )


  radius = request.args.get(
    "radius",
    GAME_MAP_RADIUS
  )


  if not valid_coordinate(
    latitude,
    longitude
  ):


    return jsonify({
      "error":
        "現在地を確認できませんでした"
    }), 400


  try:


    latitude = float(
      latitude
    )


    longitude = float(
      longitude
    )


    radius = int(
      float(
        radius
      )
    )


  except Exception:


    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400




  radius = max(
    200,
    min(
      radius,
      1200
    )
  )




  # ======================================================
  # 距離計算
  # ======================================================


  def distance_meters(
    lat1,
    lon1,
    lat2,
    lon2
  ):


    earth_radius = 6371000.0


    phi1 = math.radians(
      lat1
    )


    phi2 = math.radians(
      lat2
    )


    delta_phi = math.radians(
      lat2 - lat1
    )


    delta_lambda = math.radians(
      lon2 - lon1
    )


    kinako = (
      math.sin(
        delta_phi / 2
      ) ** 2
      +
      math.cos(
        phi1
      )
      *
      math.cos(
        phi2
      )
      *
      math.sin(
        delta_lambda / 2
      ) ** 2
    )


    kenako = (
      2
      *
      math.atan2(
        math.sqrt(
          kinako
        ),
        math.sqrt(
          1 - kinako
        )
      )
    )


    return (
      earth_radius
      *
      kenako
    )




  # ======================================================
  # 土地タイプ判定
  # ======================================================


  def detect_land_type(
    tags
  ):


    tags = tags or {}


    name = str(
      tags.get(
        "name",
        ""
      )
    ).lower()


    building = str(
      tags.get(
        "building",
        ""
      )
    ).lower()


    shop = str(
      tags.get(
        "shop",
        ""
      )
    ).lower()


    amenity = str(
      tags.get(
        "amenity",
        ""
      )
    ).lower()


    railway = str(
      tags.get(
        "railway",
        ""
      )
    ).lower()


    public_transport = str(
      tags.get(
        "public_transport",
        ""
      )
    ).lower()


    tourism = str(
      tags.get(
        "tourism",
        ""
      )
    ).lower()


    leisure = str(
      tags.get(
        "leisure",
        ""
      )
    ).lower()




    # --------------------------------------------------
    # 駅
    # --------------------------------------------------


    if (
      railway == "station"
      or
      public_transport == "station"
      or
      building == "train_station"
    ):


      if (
        "新幹線" in name
        or
        "shinkansen" in name
      ):


        return "station_major"


      return "station"




    # --------------------------------------------------
    # 大型商業施設
    # --------------------------------------------------


    large_commercial_words = [
      "アピタ",
      "apita",
      "イオン",
      "aeon",
      "ららぽーと",
      "lalaport",
      "lalaport",
      "アウトレット",
      "outlet",
      "パルコ",
      "parco",
      "マークイズ",
      "mark is",
      "高島屋",
      "takashimaya",
      "伊勢丹",
      "isetan",
      "松坂屋",
      "matsuzakaya",
      "そごう",
      "sogo"
    ]


    if any(
      word in name
      for word
      in large_commercial_words
    ):


      return "mall"




    if (
      shop == "mall"
      or
      building == "retail"
      or
      tags.get(
        "landuse"
      )
      ==
      "retail"
    ):


      return "mall"




    # --------------------------------------------------
    # スーパー
    # --------------------------------------------------


    if shop in [
      "supermarket",
      "department_store"
    ]:


      return "supermarket"




    # --------------------------------------------------
    # ホテル
    # --------------------------------------------------


    if (
      tourism == "hotel"
      or
      building == "hotel"
    ):


      return "hotel"




    # --------------------------------------------------
    # 病院
    # --------------------------------------------------


    if (
      amenity == "hospital"
      or
      building == "hospital"
    ):


      return "hospital"




    # --------------------------------------------------
    # 飲食店
    # --------------------------------------------------


    if amenity in [
      "restaurant",
      "cafe",
      "fast_food",
      "food_court"
    ]:


      return "restaurant"




    # --------------------------------------------------
    # 商業
    # --------------------------------------------------


    if (
      shop
      or
      amenity in [
        "bank",
        "cinema",
        "marketplace"
      ]
    ):


      return "commercial"




    # --------------------------------------------------
    # オフィス
    # --------------------------------------------------


    if (
      tags.get(
        "office"
      )
      or
      building == "office"
    ):


      return "office"




    # --------------------------------------------------
    # 公園
    # --------------------------------------------------


    if leisure in [
      "park",
      "garden",
      "playground"
    ]:


      return "park"




    # --------------------------------------------------
    # 住宅
    # --------------------------------------------------


    if building in [
      "house",
      "residential",
      "apartments",
      "detached",
      "semidetached_house",
      "terrace"
    ]:


      return "residential"




    if building:


      return "normal"




    return "normal"




  # ======================================================
  # 土地価格
  # ======================================================


  def land_price_for_type(
    land_type
  ):


    multipliers = {


      "station_major":
        5.0,


      "station":
        3.5,


      "mall":
        4.0,


      "supermarket":
        2.5,


      "hotel":
        3.0,


      "hospital":
        3.0,


      "restaurant":
        1.5,


      "commercial":
        1.8,


      "office":
        1.5,


      "residential":
        1.0,


      "park":
        1.2,


      "normal":
        0.8
    }


    multiplier = multipliers.get(
      land_type,
      1.0
    )


    return int(
      round(
        GAME_BASE_PRICE
        *
        multiplier
      )
    )




  # ======================================================
  # 1日収益
  # ======================================================


  def daily_income_from_station(
    station_distance,
    land_type
  ):


    if station_distance <= 100:


      income = 40


    elif station_distance <= 300:


      income = 30


    elif station_distance <= 500:


      income = 22


    elif station_distance <= 1000:


      income = 15


    elif station_distance <= 2000:


      income = 10


    else:


      income = 6




    # 大型商業施設は最低40coin
    if land_type == "mall":


      income = max(
        40,
        income
      )




    return income




  # ======================================================
  # OSM geometry → polygon
  # ======================================================


  def geometry_to_polygon(
    geometry
  ):


    polygon = []


    if not isinstance(
      geometry,
      list
    ):


      return polygon




    for point in geometry:


      if not isinstance(
        point,
        dict
      ):


        continue




      lat = point.get(
        "lat"
      )


      lon = point.get(
        "lon"
      )




      try:


        lat = float(
          lat
        )


        lon = float(
          lon
        )


      except Exception:


        continue




      polygon.append([
        lat,
        lon
      ])




    return polygon




  # ======================================================
  # polygon 中心
  # ======================================================


  def polygon_center(
    polygon
  ):


    if not polygon:


      return (
        latitude,
        longitude
      )




    lat_sum = 0.0


    lon_sum = 0.0




    for point in polygon:


      lat_sum += point[0]


      lon_sum += point[1]




    count = len(
      polygon
    )




    return (
      lat_sum / count,
      lon_sum / count
    )




  # ======================================================
  # 六角形の補助土地
  # ======================================================


  def make_hexagon(
    center_lat,
    center_lon,
    size_meters
  ):


    points = []




    latitude_degree = (
      size_meters
      /
      111320.0
    )




    longitude_degree = (
      size_meters
      /
      (
        111320.0
        *
        max(
          0.20,
          math.cos(
            math.radians(
              center_lat
            )
          )
        )
      )
    )




    for kinako in range(
      6
    ):


      angle = math.radians(
        60
        *
        kinako
        -
        30
      )




      point_lat = (
        center_lat
        +
        latitude_degree
        *
        math.sin(
          angle
        )
      )




      point_lon = (
        center_lon
        +
        longitude_degree
        *
        math.cos(
          angle
        )
      )




      points.append([
        point_lat,
        point_lon
      ])




    return points




  try:


    init_game_db()




    with game_connect() as db:


      ensure_game_player(
        db,
        player_id
      )




      # ==================================================
      # 所有済み土地を取得
      # ==================================================


      owned_rows = db.execute(
        """
        SELECT
          cell_id,
          owner_id,
          land_name,
          land_type,
          price,
          latitude,
          longitude,
          station_distance,
          daily_income
        FROM game_lands
        """
      ).fetchall()




      owned_by_cell = {}




      for row in owned_rows:


        owned_by_cell[
          row["cell_id"]
        ] = row




      # ==================================================
      # プレイヤー名一覧
      # ==================================================


      player_rows = db.execute(
        """
        SELECT
          id,
          name
        FROM game_players
        """
      ).fetchall()




      player_names = {}




      for row in player_rows:


        player_names[
          row["id"]
        ] = (
          row["name"]
          or
          "プレイヤー"
        )




      # ==================================================
      # 買収中土地
      # ==================================================


      pending_cells = set()




      try:


        pending_rows = db.execute(
          """
          SELECT
            cell_id
          FROM game_buyouts
          WHERE status = 'pending'
          """
        ).fetchall()




        for row in pending_rows:


          pending_cells.add(
            row["cell_id"]
          )


      except Exception:


        pass




      # ==================================================
      # Overpass API
      # ==================================================


      overpass_query = f"""
      [out:json][timeout:8];


      (
        way["building"](around:{radius},{latitude},{longitude});


        way["railway"="station"](around:{radius},{latitude},{longitude});


        way["public_transport"="station"](around:{radius},{latitude},{longitude});


        way["shop"="mall"](around:{radius},{latitude},{longitude});


        way["shop"="supermarket"](around:{radius},{latitude},{longitude});


        way["amenity"="hospital"](around:{radius},{latitude},{longitude});


        way["tourism"="hotel"](around:{radius},{latitude},{longitude});


        way["leisure"="park"](around:{radius},{latitude},{longitude});
      );


      out tags center geom;
      """








      osm_elements = []




      try:


        response = requests.post(
          "https://overpass-api.de/api/interpreter",


          data={
            "data":
              overpass_query
          },


          headers={
            "User-Agent":
              "TravelLife/1.0"
          },


          timeout=
            10
        )




        response.raise_for_status()




        osm_data = response.json()




        osm_elements = (
          osm_data.get(
            "elements"
          )
          or
          []
        )




      except Exception as error:


        print(
          "OVERPASS ERROR:",
          error
        )


        osm_elements = []




      # ==================================================
      # 駅位置を先に取得
      # ==================================================


      station_points = []




      for element in osm_elements:


        tags = (
          element.get(
            "tags"
          )
          or
          {}
        )




        railway = tags.get(
          "railway"
        )




        public_transport = tags.get(
          "public_transport"
        )




        building = tags.get(
          "building"
        )




        if not (
          railway == "station"
          or
          public_transport == "station"
          or
          building == "train_station"
        ):


          continue




        geometry = geometry_to_polygon(
          element.get(
            "geometry"
          )
        )




        if geometry:


          station_lat, station_lon = polygon_center(
            geometry
          )


        else:


          center = (
            element.get(
              "center"
            )
            or
            {}
          )




          try:


            station_lat = float(
              center.get(
                "lat"
              )
            )


            station_lon = float(
              center.get(
                "lon"
              )
            )


          except Exception:


            continue




        station_points.append(
          (
            station_lat,
            station_lon
          )
        )




      # ==================================================
      # OSM土地生成
      # ==================================================


      parcels = []


      used_cells = set()




      for element in osm_elements:


        osm_type = element.get(
          "type"
        )




        osm_id = element.get(
          "id"
        )




        if (
          osm_type not in [
            "way",
            "relation"
          ]
          or
          not osm_id
        ):


          continue




        cell_id = (
          f"osm:{osm_type}:{osm_id}"
        )




        if cell_id in used_cells:


          continue




        geometry = geometry_to_polygon(
          element.get(
            "geometry"
          )
        )




        if len(
          geometry
        ) < 3:


          continue




        tags = (
          element.get(
            "tags"
          )
          or
          {}
        )




        land_type = detect_land_type(
          tags
        )




        center_lat, center_lon = polygon_center(
          geometry
        )




        # ----------------------------------------------
        # 表示名
        # ----------------------------------------------


        land_name = (
          tags.get(
            "name"
          )
          or
          tags.get(
            "brand"
          )
          or
          tags.get(
            "operator"
          )
        )




        if not land_name:


          default_names = {


            "station_major":
              "駅",


            "station":
              "駅",


            "mall":
              "商業施設",


            "supermarket":
              "スーパーマーケット",


            "hotel":
              "ホテル",


            "hospital":
              "病院",


            "restaurant":
              "飲食店",


            "commercial":
              "商業施設",


            "office":
              "オフィス",


            "park":
              "公園",


            "residential":
              "住宅",


            "normal":
              "建物"
          }




          land_name = default_names.get(
            land_type,
            "土地"
          )




        # ----------------------------------------------
        # 最寄り駅
        # ----------------------------------------------


        if land_type in [
          "station",
          "station_major"
        ]:


          station_distance = 0.0


        elif station_points:


          station_distance = min(


            distance_meters(
              center_lat,
              center_lon,
              station_lat,
              station_lon
            )


            for (
              station_lat,
              station_lon
            )
            in
            station_points
          )


        else:


          station_distance = 2500.0




        # ----------------------------------------------
        # 価格・収益
        # ----------------------------------------------


        price = land_price_for_type(
          land_type
        )




        daily_income = daily_income_from_station(
          station_distance,
          land_type
        )




        # ----------------------------------------------
        # DB所有状況
        # ----------------------------------------------


        owned = owned_by_cell.get(
          cell_id
        )




        if owned:


          owner_id = owned[
            "owner_id"
          ]


          price = owned[
            "price"
          ]


          land_name = (
            owned[
              "land_name"
            ]
            or
            land_name
          )


          land_type = (
            owned[
              "land_type"
            ]
            or
            land_type
          )


          station_distance = (
            owned[
              "station_distance"
            ]
            if
            owned[
              "station_distance"
            ]
            is not None
            else
            station_distance
          )


          daily_income = (
            owned[
              "daily_income"
            ]
            if
            owned[
              "daily_income"
            ]
            is not None
            else
            daily_income
          )


        else:


          owner_id = None




        owner_name = None




        if owner_id:


          owner_name = player_names.get(
            owner_id,
            "プレイヤー"
          )




        parcels.append({


          "cell_id":
            cell_id,


          "land_name":
            land_name,


          "land_type":
            land_type,


          "latitude":
            center_lat,


          "longitude":
            center_lon,


          "polygon":
            geometry,


          "price":
            int(
              price
            ),


          "station_distance":
            round(
              float(
                station_distance
              ),
              1
            ),


          "daily_income":
            int(
              daily_income
            ),


          "owner_id":
            owner_id,


          "owner_name":
            owner_name,


          "mine":
            (
              owner_id
              ==
              player_id
            ),


          "buyout_pending":
            (
              cell_id
              in
              pending_cells
            )
        })




        used_cells.add(
          cell_id
        )




      # ==================================================
      # 補助土地
      #
      # OSMの建物が少ない場所でもゲームできるように
      # 四角形ではなく六角形で補完
      # ==================================================


      if False and len(
        parcels
      ) < 25:


        hex_size = 38.0


        lat_step = (
          hex_size
          *
          1.5
          /
          111320.0
        )




        lon_step = (
          hex_size
          *
          math.sqrt(
            3
          )
          /
          (
            111320.0
            *
            max(
              0.20,
              math.cos(
                math.radians(
                  latitude
                )
              )
            )
          )
        )




        for kinako in range(
          -5,
          6
        ):


          for kenako in range(
            -5,
            6
          ):


            center_lat = (
              latitude
              +
              kinako
              *
              lat_step
            )




            center_lon = (
              longitude
              +
              kenako
              *
              lon_step
            )




            if kinako % 2:


              center_lon += (
                lon_step
                /
                2
              )




            distance_from_user = distance_meters(
              latitude,
              longitude,
              center_lat,
              center_lon
            )




            if distance_from_user > radius:


              continue




            # --------------------------------------
            # 既存OSM土地の中心に近すぎる場所は
            # 補助土地を置かない
            # --------------------------------------


            too_close = False




            for parcel in parcels:


              parcel_lat = parcel.get(
                "latitude"
              )


              parcel_lon = parcel.get(
                "longitude"
              )




              if (
                parcel_lat is None
                or
                parcel_lon is None
              ):


                continue




              if distance_meters(
                center_lat,
                center_lon,
                float(
                  parcel_lat
                ),
                float(
                  parcel_lon
                )
              ) < 32:


                too_close = True


                break




            if too_close:


              continue




            cell_id = (
              f"grid:{kinako}:{kenako}"
            )




            polygon = make_hexagon(
              center_lat,
              center_lon,
              hex_size
            )




            if station_points:


              station_distance = min(


                distance_meters(
                  center_lat,
                  center_lon,
                  station_lat,
                  station_lon
                )


                for (
                  station_lat,
                  station_lon
                )
                in
                station_points
              )


            else:


              station_distance = 2500.0




            land_type = "normal"




            price = land_price_for_type(
              land_type
            )




            daily_income = daily_income_from_station(
              station_distance,
              land_type
            )




            owned = owned_by_cell.get(
              cell_id
            )




            if owned:


              owner_id = owned[
                "owner_id"
              ]


              price = owned[
                "price"
              ]


              land_name = (
                owned[
                  "land_name"
                ]
                or
                "通常土地"
              )


              station_distance = (
                owned[
                  "station_distance"
                ]
                if
                owned[
                  "station_distance"
                ]
                is not None
                else
                station_distance
              )


              daily_income = (
                owned[
                  "daily_income"
                ]
                if
                owned[
                  "daily_income"
                ]
                is not None
                else
                daily_income
              )


            else:


              owner_id = None


              land_name = "通常土地"




            owner_name = None




            if owner_id:


              owner_name = player_names.get(
                owner_id,
                "プレイヤー"
              )




            parcels.append({


              "cell_id":
                cell_id,


              "land_name":
                land_name,


              "land_type":
                land_type,


              "latitude":
                center_lat,


              "longitude":
                center_lon,


              "polygon":
                polygon,


              "price":
                int(
                  price
                ),


              "station_distance":
                round(
                  float(
                    station_distance
                  ),
                  1
                ),


              "daily_income":
                int(
                  daily_income
                ),


              "owner_id":
                owner_id,


              "owner_name":
                owner_name,


              "mine":
                (
                  owner_id
                  ==
                  player_id
                ),


              "buyout_pending":
                (
                  cell_id
                  in
                  pending_cells
                )
            })




      # ==================================================
      # プレイヤー情報
      # ==================================================


      player_row = db.execute(
        """
        SELECT
          id,
          name,
          coins
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()




      land_stats = db.execute(
        """
        SELECT
          COUNT(*) AS land_count,
          COALESCE(
            SUM(daily_income),
            0
          ) AS daily_income
        FROM game_lands
        WHERE owner_id = ?
        """,
        (
          player_id,
        )
      ).fetchone()




      player = {


        "id":
          player_id,


        "name":
          (
            player_row[
              "name"
            ]
            if player_row
            else
            None
          ),


        "coins":
          (
            player_row[
              "coins"
            ]
            if player_row
            else
            GAME_NORMAL_START_COINS
          ),


        "land_count":
          int(
            land_stats[
              "land_count"
            ]
            if land_stats
            else
            0
          ),


        "daily_income":
          int(
            land_stats[
              "daily_income"
            ]
            if land_stats
            else
            0
          )
      }




      return jsonify({


        "ok":
          True,


        "player":
          player,


        "parcels":
          parcels,


        "lands":
          parcels,


        "count":
          len(
            parcels
          ),


        "center": {
          "lat":
            latitude,


          "lon":
            longitude
        }
      })




  except Exception as error:


    print(
      "GAME MAP ERROR:",
      error
    )




    return jsonify({
      "error":
        "土地マップを取得できませんでした"
    }), 500




# ============================================================
# GAME / OWNED LANDS
# ============================================================


@app.route(
  "/api/game/lands",
  methods=["GET"]
)
def game_lands():


  player_id = game_player_id()


  try:


    init_game_db()


    with game_connect() as db:


      ensure_game_player(
        db,
        player_id
      )


      settle_expired_buyouts(
        db
      )


      settle_land_income(
        db,
        player_id
      )


      rows = db.execute(
        """
        SELECT
          l.*,
          p.name AS owner_name
        FROM game_lands l


        LEFT JOIN game_players p
          ON p.id = l.owner_id


        WHERE
          l.owner_id = ?


        ORDER BY
          l.daily_income DESC,
          l.price DESC
        """,
        (
          player_id,
        )
      ).fetchall()


      lands = []


      for row in rows:


        lands.append({
          "cell_id":
            row[
              "cell_id"
            ],


          "land_name":
            row[
              "land_name"
            ],


          "land_type":
            row[
              "land_type"
            ],


          "owner_id":
            row[
              "owner_id"
            ],


          "owner_name":
            row[
              "owner_name"
            ],


          "price":
            row[
              "price"
            ],


          "latitude":
            row[
              "latitude"
            ],


          "longitude":
            row[
              "longitude"
            ],


          "station_distance":
            row[
              "station_distance"
            ],


          "daily_income":
            row[
              "daily_income"
            ]
        })


      return jsonify({
        "ok":
          True,


        "lands":
          lands,


        "count":
          len(
            lands
          ),


        "daily_income":
          sum(
            int(
              land[
                "daily_income"
              ]
              or
              0
            )
            for land in lands
          )
      })


  except Exception as error:


    print(
      "GAME LANDS ERROR:",
      error
    )


    return jsonify({
      "error":
        "所有土地を取得できませんでした"
    }), 500




# ============================================================
# GAME / TRIP UTILITIES
# ============================================================


def game_active_trip(
  db,
  player_id
):


  row = db.execute(
    """
    SELECT *
    FROM game_trips
    WHERE
      player_id = ?
      AND ended_at IS NULL
    ORDER BY id DESC
    LIMIT 1
    """,
    (
      player_id,
    )
  ).fetchone()


  return row




def trip_distance_between(
  lat1,
  lon1,
  lat2,
  lon2
):


  return distance_meters(
    lat1,
    lon1,
    lat2,
    lon2
  )




# ============================================================
# GAME / TRIP START
# ============================================================


@app.route(
  "/api/game/trip/start",
  methods=["POST"]
)
def game_trip_start():
  player_id = game_player_id()

  try:
    init_game_db()

    with game_connect() as db:
      player = ensure_game_player(
        db,
        player_id
      )

      if not player["name"]:
        return jsonify({
          "error":
            "先にユーザー名を設定してください"
        }), 400

      existing = game_active_trip(
        db,
        player_id
      )

      if existing:
        return jsonify({
          "ok":
            True,
          "trip": {
            "id":
              existing["id"],
            "started_at":
              existing["started_at"],
            "distance":
              float(
                existing["distance"]
              ),
            "coins":
              int(
                existing["coins"]
                or
                0
              ),
            "active":
              True
          },
          "player": {
            "id":
              player["id"],
            "name":
              player["name"],
            "coins":
              int(
                player["coins"]
              )
          }
        })

      now = game_now()

      cursor = db.execute(
        """
        INSERT INTO game_trips (
          player_id,
          started_at,
          ended_at,
          distance,
          coins
        )
        VALUES (?, ?, NULL, 0, 0)
        """,
        (
          player_id,
          now
        )
      )

      trip_id = cursor.lastrowid

      db.commit()

      return jsonify({
        "ok":
          True,
        "message":
          "移動記録を開始しました",
        "trip": {
          "id":
            trip_id,
          "started_at":
            now,
          "distance":
            0.0,
          "coins":
            0,
          "active":
            True
        },
        "player": {
          "id":
            player["id"],
          "name":
            player["name"],
          "coins":
            int(
              player["coins"]
            )
        }
      })

  except Exception as error:
    print(
      "GAME TRIP START ERROR:",
      error
    )

    return jsonify({
      "error":
        "移動記録を開始できませんでした"
    }), 500
@app.route(
  "/api/game/trip/point",
  methods=["POST"]
)


def game_trip_point():
  player_id = game_player_id()

  try:
    data = (
      request.get_json(
        silent=True
      )
      or
      {}
    )

    latitude = float(
      data["lat"]
    )
    longitude = float(
      data["lon"]
    )
    accuracy = float(
      data.get(
        "accuracy",
        0
      )
      or
      0
    )

  except (
    KeyError,
    TypeError,
    ValueError
  ):
    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400

  if not (
    -90 <= latitude <= 90
    and
    -180 <= longitude <= 180
  ):
    return jsonify({
      "error":
        "位置情報が正しくありません"
    }), 400

  try:
    init_game_db()

    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )

      trip = game_active_trip(
        db,
        player_id
      )

      if not trip:
        return jsonify({
          "error":
            "移動記録が開始されていません"
        }), 409

      trip_id = int(
        trip["id"]
      )

      if accuracy > 120:
        return jsonify({
          "ok":
            True,
          "accepted":
            False,
          "reason":
            "GPS精度が低いため記録しませんでした",
          "trip": {
            "id":
              trip_id,
            "distance":
              float(
                trip["distance"]
              ),
            "coins":
              int(
                trip["coins"]
                or
                0
              )
          }
        })

      previous = db.execute(
        """
        SELECT
          latitude,
          longitude,
          created_at
        FROM game_trip_points
        WHERE trip_id = ?
        ORDER BY id DESC
        LIMIT 1
        """,
        (
          trip_id,
        )
      ).fetchone()

      moved = 0.0

      if previous:
        lat1 = math.radians(
          float(
            previous["latitude"]
          )
        )
        lat2 = math.radians(
          latitude
        )
        delta_lat = math.radians(
          latitude
          -
          float(
            previous["latitude"]
          )
        )
        delta_lon = math.radians(
          longitude
          -
          float(
            previous["longitude"]
          )
        )

        value = (
          math.sin(
            delta_lat / 2
          ) ** 2
          +
          math.cos(
            lat1
          )
          *
          math.cos(
            lat2
          )
          *
          math.sin(
            delta_lon / 2
          ) ** 2
        )

        moved = (
          6371000
          *
          2
          *
          math.asin(
            math.sqrt(
              min(
                1,
                value
              )
            )
          )
        )

        elapsed = max(
          1,
          game_now()
          -
          int(
            previous["created_at"]
          )
        )

        speed_mps = (
          moved
          /
          elapsed
        )

        if (
          moved > 1000
          or
          speed_mps > 60
        ):
          return jsonify({
            "ok":
              True,
            "accepted":
              False,
            "reason":
              "位置情報が大きく飛んだため記録しませんでした",
            "trip": {
              "id":
                trip_id,
              "distance":
                float(
                  trip["distance"]
                ),
              "coins":
                int(
                  trip["coins"]
                  or
                  0
                )
            }
          })

      now = game_now()

      db.execute(
        """
        INSERT INTO game_trip_points (
          trip_id,
          latitude,
          longitude,
          accuracy,
          created_at
        )
        VALUES (?, ?, ?, ?, ?)
        """,
        (
          trip_id,
          latitude,
          longitude,
          accuracy,
          now
        )
      )

      # 10 m = 1 coin。1回のGPS更新では最大100 coin。
      earned = min(
        int(
          moved / 10
        ),
        100
      )

      if moved > 0:
        db.execute(
          """
          UPDATE game_trips
          SET
            distance = distance + ?,
            coins = coins + ?
          WHERE id = ?
          """,
          (
            moved,
            earned,
            trip_id
          )
        )

      if earned > 0:
        db.execute(
          """
          UPDATE game_players
          SET
            coins = coins + ?,
            updated_at = ?
          WHERE id = ?
          """,
          (
            earned,
            now,
            player_id
          )
        )

      db.commit()

      updated = db.execute(
        """
        SELECT *
        FROM game_trips
        WHERE id = ?
        """,
        (
          trip_id,
        )
      ).fetchone()

      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()

      return jsonify({
        "ok":
          True,
        "accepted":
          True,
        "earned":
          earned,
        "trip": {
          "id":
            updated["id"],
          "started_at":
            updated["started_at"],
          "distance":
            float(
              updated["distance"]
            ),
          "coins":
            int(
              updated["coins"]
              or
              0
            ),
          "active":
            True
        },
        "player": {
          "id":
            player["id"],
          "name":
            player["name"],
          "coins":
            int(
              player["coins"]
            )
        }
      })

  except Exception as error:
    print(
      "GAME TRIP POINT ERROR:",
      error
    )

    return jsonify({
      "error":
        "位置情報を記録できませんでした"
    }), 500
@app.route(
  "/api/game/trip/stop",
  methods=["POST"]
)
def game_trip_stop():
  player_id = game_player_id()

  try:
    init_game_db()

    with game_connect() as db:
      player = ensure_game_player(
        db,
        player_id
      )

      trip = game_active_trip(
        db,
        player_id
      )

      if not trip:
        return jsonify({
          "error":
            "終了する移動記録がありません"
        }), 409

      now = game_now()

      db.execute(
        """
        UPDATE game_trips
        SET ended_at = ?
        WHERE id = ?
        """,
        (
          now,
          trip["id"]
        )
      )

      db.commit()

      updated = db.execute(
        """
        SELECT *
        FROM game_trips
        WHERE id = ?
        """,
        (
          trip["id"],
        )
      ).fetchone()

      player = db.execute(
        """
        SELECT *
        FROM game_players
        WHERE id = ?
        """,
        (
          player_id,
        )
      ).fetchone()

      return jsonify({
        "ok":
          True,
        "message":
          "移動記録を終了しました",
        "trip": {
          "id":
            updated["id"],
          "started_at":
            updated["started_at"],
          "ended_at":
            updated["ended_at"],
          "distance":
            float(
              updated["distance"]
            ),
          "coins":
            int(
              updated["coins"]
              or
              0
            ),
          "active":
            False
        },
        "player": {
          "id":
            player["id"],
          "name":
            player["name"],
          "coins":
            int(
              player["coins"]
            )
        }
      })

  except Exception as error:
    print(
      "GAME TRIP STOP ERROR:",
      error
    )

    return jsonify({
      "error":
        "移動記録を終了できませんでした"
    }), 500
@app.route(
  "/api/game/trips",
  methods=["GET"]
)
def game_trips():
  player_id = game_player_id()

  try:
    init_game_db()

    with game_connect() as db:
      ensure_game_player(
        db,
        player_id
      )

      rows = db.execute(
        """
        SELECT *
        FROM game_trips
        WHERE player_id = ?
        ORDER BY id DESC
        LIMIT 100
        """,
        (
          player_id,
        )
      ).fetchall()

      trips = []

      for row in rows:
        trips.append({
          "id":
            row["id"],
          "started_at":
            row["started_at"],
          "ended_at":
            row["ended_at"],
          "distance":
            float(
              row["distance"]
            ),
          "coins":
            int(
              row["coins"]
              or
              0
            ),
          "active":
            row["ended_at"]
            is
            None
        })

      return jsonify({
        "ok":
          True,
        "trips":
          trips,
        "count":
          len(
            trips
          )
      })

  except Exception as error:
    print(
      "GAME TRIPS ERROR:",
      error
    )

    return jsonify({
      "error":
        "移動履歴を取得できませんでした"
    }), 500
@app.route(
  "/api/game/trips/<int:trip_id>",
  methods=["GET"]
)
def game_trip_detail(
  trip_id
):


  player_id = game_player_id()


  try:


    init_game_db()


    with game_connect() as db:


      ensure_game_player(
        db,
        player_id
      )


      trip = db.execute(
        """
        SELECT *
        FROM game_trips
        WHERE
          id = ?
          AND
          player_id = ?
        """,
        (
          trip_id,
          player_id
        )
      ).fetchone()


      if not trip:


        return jsonify({
          "error":
            "移動履歴が見つかりません"
        }), 404


      rows = db.execute(
        """
        SELECT *
        FROM game_trip_points
        WHERE trip_id = ?
        ORDER BY id ASC
        LIMIT 5000
        """,
        (
          trip_id,
        )
      ).fetchall()


      points = []


      for row in rows:


        points.append({
          "id":
            row[
              "id"
            ],


          "lat":
            row[
              "latitude"
            ],


          "lon":
            row[
              "longitude"
            ],


          "created_at":
            row[
              "created_at"
            ]
        })


      return jsonify({
        "ok":
          True,


        "trip": {
          "id":
            trip[
              "id"
            ],


          "started_at":
            trip[
              "started_at"
            ],


          "ended_at":
            trip[
              "ended_at"
            ],


          "distance":
            trip[
              "distance"
            ]
        },


        "points":
          points
      })


  except Exception as error:


    print(
      "GAME TRIP DETAIL ERROR:",
      error
    )


    return jsonify({
      "error":
        "移動履歴を取得できませんでした"
    }), 500




# ============================================================
# GAME / CURRENT TRIP
# ============================================================


@app.route(
  "/api/game/trip/current",
  methods=["GET"]
)
def game_trip_current():
  player_id = game_player_id()

  try:
    init_game_db()

    with game_connect() as db:
      player = ensure_game_player(
        db,
        player_id
      )

      trip = game_active_trip(
        db,
        player_id
      )

      if not trip:
        return jsonify({
          "ok":
            True,
          "trip":
            None,
          "player": {
            "id":
              player["id"],
            "name":
              player["name"],
            "coins":
              int(
                player["coins"]
              )
          }
        })

      return jsonify({
        "ok":
          True,
        "trip": {
          "id":
            trip["id"],
          "started_at":
            trip["started_at"],
          "distance":
            float(
              trip["distance"]
            ),
          "coins":
            int(
              trip["coins"]
              or
              0
            ),
          "active":
            True
        },
        "player": {
          "id":
            player["id"],
          "name":
            player["name"],
          "coins":
            int(
              player["coins"]
            )
        }
      })

  except Exception as error:
    print(
      "GAME CURRENT TRIP ERROR:",
      error
    )

    return jsonify({
      "error":
        "移動状態を取得できませんでした"
    }), 500
@app.route(
  "/health"
)
def health():


  return jsonify({
    "ok":
      True,


    "service":
      "Travel Life",


    "time":
      game_now()
  })




# ============================================================
# ERROR HANDLERS
# ============================================================


@app.errorhandler(
  404
)
def not_found(
  error
):


  if request.path.startswith(
    "/api/"
  ):


    return jsonify({
      "error":
        "APIが見つかりません"
    }), 404


  return (
    "ページが見つかりません",
    404
  )




@app.errorhandler(
  405
)
def method_not_allowed(
  error
):


  if request.path.startswith(
    "/api/"
  ):


    return jsonify({
      "error":
        "この操作には対応していません"
    }), 405


  return (
    "Method Not Allowed",
    405
  )




@app.errorhandler(
  500
)
def internal_server_error(
  error
):


  print(
    "INTERNAL SERVER ERROR:",
    error
  )


  if request.path.startswith(
    "/api/"
  ):


    return jsonify({
      "error":
        "サーバー内部でエラーが発生しました"
    }), 500


  return (
    "サーバー内部でエラーが発生しました",
    500
  )




# ============================================================
# 初期化
# ============================================================


def initialize_app():


  try:


    init_game_db()


    print(
      "Travel Life game database initialized."
    )


  except Exception as error:


    print(
      "GAME DATABASE INITIALIZE ERROR:",
      error
    )




initialize_app()




# ============================================================
# 起動
# ============================================================


if __name__ == "__main__":


  app.run(
    host="0.0.0.0",
    port=int(
      os.environ.get(
        "PORT",
        "5000"
      )
    ),
    debug=True
  )
