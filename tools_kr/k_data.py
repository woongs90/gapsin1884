"""갑신년 그날 밤, 우정총국 데이터 모으기 -> data/EscapeData.json  (+ 지도 이벤트 · 그림 파일 맞춰 보기)
 python k_data.py <프로젝트 폴더>"""
import json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
ROOT = sys.argv[1]
import k_story as S
import k_portraits as PT

PORTRAIT_FILES = ['kp_%s_%s' % (who, e) for who, exprs in PT.SETS.items() for e in exprs]

# 이어하기 단위: 장을 시작할 때마다 저장 (번호 4자리). 단위 k = 'k장을 시작할 수 있음' (그 앞 장까지의 깃발과 사료 카드)
UNITS = [
    ("c1", ["c0", "p_letter", "p_dad", "p_stamp", "p_box", "p_desk"], ["letters"]),
    ("c2", ["a_in", "a_1", "a_2", "a_3", "a_4", "a_5", "a_obs", "a_q", "a_bk", "a_b1", "a_b2", "a_b3", "a_b4", "a_b5", "a_sort", "a_oct", "a_type", "r1", "dev1", "quiz1"], ["sunbo", "src_split"]),
    ("c3", ["b_in", "b_1", "b_2", "b_3", "b_pick", "b_uj", "b_4", "b_5", "b_6", "b_order", "b_drill", "r2", "dev2", "quiz2"], ["src_eve"]),
    ("c4", ["c_in", "c_1", "c_2", "c_3", "c_4", "c_seat", "c_st", "c_sneak", "c_gy", "c_5", "c_6", "c_7", "c_nego", "r3", "dev3", "quiz3"], ["src_day1"]),
    ("c5", ["d_in", "d_match", "d_mk", "d_1", "d_2", "d_3", "d_4", "d_cd", "d_sort", "r4", "dev4", "quiz4"], ["src_day2"]),
    ("c6", ["e_in", "e_1", "e_2", "e_3", "e_talk", "e_def", "e_scale", "e_bk", "e_4", "e_5", "r5", "dev5", "quiz5"], ["src_day3", "burnt_type"]),
    ("c7", ["f_in", "f_spot", "f_1", "f_2", "f_3", "f_4", "f_map", "f_jd", "f_5", "f_6", "f_7", "f_8", "f_jdmap", "f_q", "r6", "dev6", "quiz6"], ["src_after"]),
]
NCH = 7

def body(k):
    """k장 처음부터 (저장 표시 단계는 빼고)"""
    st = S.CHAPTER_START[k]()
    return [{"flag": "c%d" % k}] + st[1:]

def resume_steps():
    s = None
    for k in range(1, NCH + 1):
        s = [{"if": {"flag": "c%d" % k}, "then": body(k), "else": s or []}] if s is not None else [{"if": {"flag": "c%d" % k}, "then": body(k)}]
    return s

def code_entry():
    return [{"lock": {"progress": True, "digits": 4, "question": "장을 시작할 때 받은 이어하기 번호 4자리를 입력하세요."},
             "success": [{"text": "번호를 확인했어요. 그 장부터 이어서 합니다."}] + resume_steps(),
             "fail": [{"text": "번호가 맞지 않아요. 처음부터 시작합니다."}]}]

def part(k, label):
    """k장부터 시작 (그 앞 장의 깃발 · 사료 카드를 알림 없이 채움)"""
    flags, items = [], []
    for f, fl, it in UNITS:
        if int(f[1:]) <= k:
            if int(f[1:]) < k: flags.append(f)
            flags += fl; items += it
    return [{"flag": flags, "grant": items}, {"text": label + "부터 시작합니다. 앞 장에서 모을 사료 카드는 가방에 넣어 두었어요.", "speaker": "시작"},
            PREV[k]] + body(k)

PREV = {
    1: {"picture": "kc_bundles", "speaker": "지난 이야기", "text": "1893년 섣달 그믐, 역관 윤재는 김옥균의 편지를 받고 지난 11년의 편지 묶음을 꺼냈다."},
    2: {"picture": "kc_sum1", "speaker": "지난 이야기", "text": "1장: 임오군란 뒤 개화파는 온건 개화파와 급진 개화파로 갈라졌다. 1883년 박문국에서 『한성순보』가 나왔다."},
    3: {"picture": "kc_sum2", "speaker": "지난 이야기", "text": "1~2장: 청의 간섭이 심해지는 가운데 보빙사가 미국에 다녀오고 우정총국이 세워졌다. 청군 절반이 빠져나가자 급진 개화파는 정변을 준비했다."},
    4: {"picture": "kc_sum3", "speaker": "지난 이야기", "text": "1~3장: 1884년 12월 4일 우정총국 축하연에서 정변이 일어났다. 국왕은 경우궁으로 옮겼고 일본군이 그곳을 지켰다."},
    5: {"picture": "kc_sum4", "speaker": "지난 이야기", "text": "1~4장: 12월 5일 새 정부가 서고 14개조 정강이 마련되었다. 그러나 국왕은 넓은 창덕궁으로 돌아갔고, 장터의 민심은 차가웠다."},
    6: {"picture": "kc_sum5", "speaker": "지난 이야기", "text": "1~5장: 12월 6일 청군이 쳐들어오고 일본군이 물러나 정변은 사흘 만에 끝났다(삼일천하)."},
}
PART_CHOICES = ["처음부터 하기 (프롤로그부터)", "1장 · 갈라지는 개화", "2장 · 정변 전야", "3장 · 첫째 날 (12월 4일)",
                "4장 · 둘째 날 (12월 5일)", "5장 · 셋째 날 (12월 6일)", "6장 · 그 뒤 10년", "이어하기 번호 입력 (다른 기기)"]
def part_menu():
    return {"speaker": "시작", "question": "어디서부터 할까요? (1부 1~3장 · 2부 4~6장)", "choice": PART_CHOICES, "shuffle": False,
            "on2": part(1, "1장"), "on3": part(2, "2장"), "on4": part(3, "3장"), "on5": part(4, "4장"), "on6": part(5, "5장"), "on7": part(6, "6장"), "on8": code_entry()}

START = [
    {"if": {"progressSaved": True},
     "then": [{"speaker": "이어하기", "question": "이 기기에 저장된 기록이 있어요. 어떻게 할까요?", "choice": ["새로 시작하기 (장 고르기)", "이 기기에서 이어서 하기"],
               "on2": [{"progressLoad": True, "text": "저장한 곳부터 이어서 합니다."}] + resume_steps(), "on1": [part_menu()], "shuffle": False}],
     "else": [part_menu()]},
]
def add_code_notice(o):
    if isinstance(o, list):
        out = []
        for x in o:
            x = add_code_notice(x); out.append(x)
            if isinstance(x, dict) and x.get("progressSave"):
                out.append({"speaker": "이어하기", "text": "여기까지 이 기기에 저장했어요. 다른 기기에서 이어 하려면 번호 {code} 를 기억하세요."})
        return out
    if isinstance(o, dict): return {k: add_code_notice(v) for k, v in o.items()}
    return o

ROOMS = add_code_notice(S.ROOMS)

PORTRAITS = {"{name}": "kp_{pid}", "통역 · 윤재": "kp_{pid}", "윤재의 마음": "kp_{pid}", "윤희": "kp_{hpid}", "아버지": "kp_{fpid}",
             "김옥균": "kp_kimokgyun", "박영효": "kp_parkyounghyo", "홍영식": "kp_hongyoungsik", "서광범": "kp_seogwangbeom", "서재필": "kp_seojaepil",
             "김윤식": "kp_kimyunsik", "어윤중": "kp_eoyunjung", "김홍집": "kp_kimhongjip", "민영익": "kp_minyoungik", "윤치호": "kp_yunchiho", "고종": "kp_gojong",
             "위안스카이": "kp_yuan", "진수당": "kp_chenshutang", "다케조에": "kp_takezoe", "시마무라": "kp_shimamura", "묄렌도르프": "kp_mollendorff",
             "푸트": "kp_foote", "애스턴": "kp_aston", "후쿠자와": "kp_fukuzawa", "이노우에": "kp_inoue", "정여창": "kp_ding",
             "알렌": "kp_allen", "아펜젤러": "kp_appenzeller", "스크랜턴 부인": "kp_scranton", "헐버트": "kp_hulbert",
             "돌쇠": "kp_dolsoe", "신문팔이 소년": "kp_newsboy", "인력거꾼": "kp_rickshaw", "일본 순사": "kp_jp_police",
             "청 상인": "kp_qing_merchant", "청 군사": "kp_qing_soldier", "보부상": "kp_peddler", "장터 아낙": "kp_market_w", "상민": "kp_commoner", "도시 빈민": "kp_poor_m",
             "우체부": "kp_postman", "목수": "kp_carpenter", "순라군": "kp_patrol", "일본 군인": "kp_jp_soldier", "사관생도": "kp_cadet",
             "거문도 주민": "kp_islander", "섬 아낙": "kp_islander_w", "영국 수병": "kp_br_sailor", "육영공원 학생": "kp_student_y", "전보국 관리": "kp_telegraph_off"}

data = {
    "title": "갑신년 그날 밤, 우정총국", "gameTitle": "갑신년 그날 밤, 우정총국",
    "titleImage": "Kr_Title", "titleText": False, "titlePromptY": 0.64,
    "titleLayers": [{"image": "Kr_TitleLeft", "side": "left", "margin": 22, "y": 70, "clear": 370},
                    {"image": "Kr_TitleRight", "side": "right", "margin": 24, "y": 70, "clear": 370},
                    {"image": "Kr_TitlePeople", "x": "center", "bottom": 6, "fit": 8}], "titleBgm": "Kr_Title",
    "bgm": "Kr_Home", "timeLimit": 0, "hints": 10, "hp": 3, "wrongPenalty": 0,
    "startRoom": "seojae", "recordTitle": "여섯 묶음을 모두 읽고, 김옥균에게 답장을 썼다!",
    "shuffleChoices": True, "roomCards": False, "endingBgm": "Kr_Ending",
    "vars": {"name": "윤재", "pid": "yunjae37", "hpid": "yunhee35", "fpid": "father93", "code": "----", "tension": "", "clock": "", "held": "4", "yjc": "1", "last": ""},
    "gauge": {"var": "tension", "label": "경우궁 긴장", "min": 0, "max": 10, "style": "level"},
    "clock": {"var": "clock"},
    "archives": S.ARCHIVES,
    "characters": [{"label": "윤재", "image": "$k_yunjae37", "index": 0, "vars": {"name": "윤재"}}],
    "portraits": PORTRAITS,
    "portraitFiles": PORTRAIT_FILES,
    "intro": S.INTRO + START,
    "progress": {"key": "ujeong_1884", "mult": 337, "add": 613, "base": {"flags": []},
                 "keepItems": S.ARCHIVES + ["letters", "sunbo", "burnt_type"],
                 "units": [{"flag": f, "flags": fl, "items": it} for f, fl, it in UNITS]},
    "review": {"url": "https://forms.gle/9PfM9UU7hb5RcCwd6", "picture": "kc_review", "title": "갑신년 그날 밤, 우정총국 · 후기를 남겨 주세요",
               "text": "끝까지 함께해 줘서 고마워요! [후기 남기기]를 누르면 새 창이 열려요. 휴대폰으로 QR 코드를 찍어도 돼요."},
    "items": S.ITEMS, "hintQuizzes": S.HINTQ, "puzzles": S.PUZZLES, "rooms": ROOMS,
    "ending": {"success": [{"text": "갑신년 그날 밤, 우정총국 완료!", "speaker": "기록"}],
               "fail": [{"text": "시간이 다 되었다."}],
               "summary": [{"picture": "kc_summary", "speaker": "정리",
                            "text": "개화파의 분화 → 정변 전야 → 갑신정변 사흘(12.4~12.6) → 한성 · 톈진 조약, 거문도, 근대 시설, 방곡령 → (3편) 동학농민운동"}]},
}

out = os.path.join(ROOT, 'data', 'EscapeData.json')
os.makedirs(os.path.dirname(out), exist_ok=True)
open(out, 'w', encoding='utf-8').write(json.dumps(data, ensure_ascii=False, indent=1))

# ---- 검사
pics = set()
def walk(o):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ('picture', 'closeup', 'image', 'image2') and isinstance(v, str) and not v.startswith(('$', '!')) and k != 'image' or (k == 'image' and isinstance(v, str) and v.startswith(('kc_', 'ki_'))): pics.add(v)
            walk(v)
    elif isinstance(o, list):
        for x in o: walk(x)
walk(data)
for k, it in S.ITEMS.items(): pics.add(it['image'])
for f in PORTRAIT_FILES: pics.add(f)
bad = 0
for r in ROOMS:
    mp = json.load(open(os.path.join(ROOT, 'data', 'Map%03d.json' % r['map']), encoding='utf-8'))
    names = {e['name'] for e in mp['events'] if e}
    ids = {h['id'] for h in r['hotspots']}
    for w in r.get('watchers', []): ids.add(w['event'])
    miss = ids - names; extra = names - ids
    if miss or extra: print(r['id'], 'MISSING', sorted(miss), 'EXTRA', sorted(extra)); bad += 1
pd = os.path.join(ROOT, 'img', 'pictures')
have = {f[:-4] for f in os.listdir(pd)} if os.path.isdir(pd) else set()
need = sorted(p for p in pics if p not in have)
print('rooms', len(ROOMS), 'hotspots', sum(len(r['hotspots']) for r in ROOMS), 'pictures', len(pics), 'missing', len(need), need[:30])
items = set(S.ITEMS)
def walk3(o):
    if isinstance(o, dict):
        for k in ('give', 'take', 'grant'):
            if k in o:
                for it in (o[k] if isinstance(o[k], list) else [o[k]]):
                    if it not in items: print('  ? unknown item', it)
        for v in o.values(): walk3(v)
    elif isinstance(o, list):
        for x in o: walk3(x)
walk3(data)
all_ids = {(r['id'], h['id']) for r in ROOMS for h in r['hotspots']}
any_ids = {h for _, h in all_ids}
nogoal = []
def walk4(o, where):
    if isinstance(o, dict):
        if isinstance(o.get('goal'), str):
            t = o.get('targets') or []
            if not t: nogoal.append((where, o['goal'][:30]))
            for x in t:
                if ':' in x:
                    if tuple(x.split(':', 1)) not in all_ids: print('  ? bad target', x)
                elif x not in any_ids: print('  ? bad target', x, 'in', where)
        for v in o.values(): walk4(v, where)
    elif isinstance(o, list):
        for x in o: walk4(x, where)
for r in ROOMS: walk4(r, r['id'])
walk4(data['intro'], 'intro')
print('goals without targets:', len(nogoal), nogoal[:8])
setf = set()
def walk5(o):
    if isinstance(o, dict):
        if 'flag' in o and not any(k in o for k in ('if', 'noFlag', 'flags', 'noFlags')) and len(o) <= 3:
            for f in (o['flag'] if isinstance(o['flag'], list) else [o['flag']]): setf.add(f)
        for v in o.values(): walk5(v)
    elif isinstance(o, list):
        for x in o: walk5(x)
walk5(S.ROOMS)
unit_flags = set(f for f, fl, it in UNITS) | set(x for f, fl, it in UNITS for x in fl)
late = {'h_in', 'h_dad', 'h_reply', 'epi'}
print('flags not in units:', sorted(setf - unit_flags - late))
sp = {r['id']: r for r in ROOMS}
for f, fl, it in UNITS:
    print(f, 'code', '%04d' % ((sum(1 << i for i in range(int(f[1:]))) * 337 + 613) % 10000))

# ---- 한자 글꼴 (fonts/EscHanja.ttf): 데이터에 나오는 한자만 골라 작은 글꼴로 (Noto Serif CJK KR, OFL)
import subprocess, re as _re
han = sorted(set(_re.findall(r'[㐀-鿿豈-﫿]', json.dumps(data, ensure_ascii=False))))
fd = os.path.join(ROOT, 'fonts'); os.makedirs(fd, exist_ok=True)
txt = os.path.join(fd, '_hanja.txt'); open(txt, 'w', encoding='utf-8').write(''.join(han))
subprocess.run(['pyftsubset', '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc', '--font-number=1', '--text-file=' + txt,
                '--output-file=' + os.path.join(fd, 'EscHanja.ttf'), '--layout-features=*', '--no-hinting'], check=True)
os.remove(txt)
print('hanja glyphs', len(han), os.path.getsize(os.path.join(fd, 'EscHanja.ttf')))
