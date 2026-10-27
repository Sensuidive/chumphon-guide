"""Every 3 h: TMD Weather Forecast API (NWP, Bearer token from repo secret TMD_TOKEN, Michael's account) -> wx_tmd.json.
The app uses it when it is fresh (credit: Thai Meteorological Department) and falls back to MET Norway otherwise."""
import json, os, sys, urllib.request, urllib.parse
from datetime import datetime, timedelta, timezone
tok = os.environ.get('TMD_TOKEN')
if not tok: print('no TMD_TOKEN yet'); sys.exit(0)
BKK = timezone(timedelta(hours=7)); now = datetime.now(BKK)
TOWN, SEA = (10.50, 99.18), (10.60, 99.33)
def get(kind, la, lo, fields, **q):
    url = 'https://data.tmd.go.th/nwpapi/v1/forecast/location/%s/at?%s' % (kind, urllib.parse.urlencode(dict(lat=la, lon=lo, fields=fields, **q)))
    r = urllib.request.Request(url, headers={'accept': 'application/json', 'authorization': 'Bearer ' + tok, 'User-Agent': 'ChumphonGuide/1.0 (info@sensuidive.com)'})
    d = json.load(urllib.request.urlopen(r, timeout=60))
    return [(f['time'][:13], f['data']) for f in d['WeatherForecasts'][0]['forecasts']]
today = now.strftime('%Y-%m-%d')
daily = get('daily', *TOWN, 'tc_max,tc_min,rain,cond', date=today, duration=3)
seaD = dict(get('daily', *SEA, 'ws10m,wd10m', date=today, duration=3))
seaH = get('hourly', *SEA, 'ws10m,wd10m', date=today, hour=0, duration=48)
days = []
for t, x in daily:
    d = t[:10]; h = [v for k, v in seaH if k[:10] == d and 8 <= int(k[11:13]) <= 14]
    ws = [v['ws10m'] * 3.6 for v in h] or [seaD.get(t, {}).get('ws10m', 0) * 3.6]
    wd = (h[len(h) // 2]['wd10m'] if h else seaD.get(t, {}).get('wd10m', 0))
    days.append(dict(d=d, hi=round(x['tc_max']), lo=round(x['tc_min']), rain=round(x['rain'], 1), cond=int(x['cond']),
                     wlo=round(min(ws)), whi=round(max(ws)), wd=round(wd)))
json.dump(dict(at=now.strftime('%Y-%m-%dT%H:%M:%S+07:00'), src='Thai Meteorological Department (TMD) Weather Forecast API', days=days), open('wx_tmd.json', 'w'), indent=1)
print('ok', days)
