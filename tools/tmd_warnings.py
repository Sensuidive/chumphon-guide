"""Hourly: TMD weather warning news -> warnings.json for the Chumphon Guide red bar (Michael 27 Oct 2026).
Keys come from repo secrets TMD_UID / TMD_UKEY (Michael's own TMD account). Shows only warnings from the last 36 h
that mention Chumphon, the Gulf of Thailand or the upper south."""
import json, os, re, sys, urllib.request
from datetime import datetime, timedelta, timezone
uid, key = os.environ.get('TMD_UID'), os.environ.get('TMD_UKEY')
if not uid or not key: sys.exit('no TMD keys yet')
url = 'https://data.tmd.go.th/api/WeatherWarningNews/v1/?uid=%s&ukey=%s&format=json' % (uid, key)
d = json.load(urllib.request.urlopen(url, timeout=60))
w = d.get('WarningNews') or []
w = w if isinstance(w, list) else [w]
now = datetime.now(timezone(timedelta(hours=7)))
AREA = re.compile(r'ชุมพร|อ่าวไทย|ภาคใต้ตอนบน|ภาคใต้ฝั่งตะวันออก|Chumphon|Gulf of Thailand|upper south', re.I)
out = []
for x in w:
    try: t = datetime.strptime(x['AnnounceDateTime'][:19], '%Y-%m-%d %H:%M:%S').replace(tzinfo=now.tzinfo)
    except Exception: continue
    text = ' '.join(str(x.get(k) or '') for k in ('TitleThai', 'TitleEnglish', 'DescriptionThai', 'DescriptionEnglish'))
    if now - t <= timedelta(hours=36) and AREA.search(text):
        out.append(dict(at=x['AnnounceDateTime'][:16], th=x.get('TitleThai') or '', en=x.get('TitleEnglish') or x.get('TitleThai') or '',
                        pdf=(x.get('DocumentFile') or '').replace('\\', '/').replace('http://', 'https://')))
new = json.dumps(dict(checked=now.strftime('%Y-%m-%d %H:%M'), warnings=out), ensure_ascii=False, indent=1)
old = open('warnings.json').read() if os.path.exists('warnings.json') else ''
if json.loads(old or '{"warnings":null}').get('warnings') != out or not old:
    open('warnings.json', 'w').write(new); print('updated', len(out))
else: print('no change', len(out))
