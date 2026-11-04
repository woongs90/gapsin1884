"""갑신년 그날 밤, 우정총국 · 확대 그림(카드) 만들기 -> img/pictures
 python k_cards.py <프로젝트 폴더>
 지도: historical-basemaps (Ourednik, GPL-3.0) 1880년 국경 자료
 '실제 사진 자리' 그림(kc_photo_*)은 tools_kr/photos/<이름>.png 가 있으면 그 사진으로, 없으면 예시 그림으로 만든다.
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import k_cards_base as B
from k_cards_base import paper, wrap, text_block, title, tag, footnote, card, CW, CH, INK, RED, BLUE, F, sh, mix, outline
import k_geo as GEO

def S(im, name): B.S(im, name)
HANJI = (240, 230, 206)

# ==================================================================== 안내
def cards_intro():
    card('kc_rules', '『갑신년 그날 밤, 우정총국』을 시작하기 전에', [
        '윤재와 아버지(역관) · 누이 윤희 · 식자공 돌쇠, 장터와 섬 사람들은 이야기를 위해 꾸민 인물이에요. 박문국 모임과 경우궁 통역 장면도 꾸민 장면이에요.',
        '김옥균 · 박영효 · 홍영식 · 서광범 · 서재필 · 김윤식 · 어윤중 · 민영익 · 고종 · 위안스카이 · 다케조에 · 묄렌도르프 · 알렌 등은 실존 인물이고, 말은 기록을 바탕으로 쉽게 풀었어요.',
        '1893년의 윤재가 지난 편지 묶음 여섯을 차례로 읽어요. 3~5장은 갑신정변의 사흘(12월 4일~6일)이에요.',
        '같은 일을 여러 사람의 눈으로 보여 줘요. 다치거나 목숨을 잃는 장면은 짧은 글로만 다뤘어요.'], label='알림', size=16)
    card('kc_controls', '이렇게 해요', [
        '방향키 · 화면 누르기: 걷기    Enter · Space · 클릭: 앞에 있는 사람 · 물건 조사',
        '머리 위 노란 \'!\': 지금 가야 할 곳    흰 \'?\': 아직 살펴보지 않은 물건 (가까이 가면 보여요)',
        '화면 위 시계 (3~5장): 갑신정변 사흘 동안의 시각',
        '오른쪽 위 [가방]: 모은 사료 카드 다시 보기    [힌트]: 막힐 때',
        '퍼즐 창: 틀려도 괜찮아요. 두 번 틀리면 힌트, 세 번 틀리면 정답을 알려 줘요. Esc 로 나중에 하기',
        '처음 시작할 때 1장~6장 가운데 골라 그 장부터 할 수도 있어요 (2차시는 4장부터).'], label='조작', size=16)

# ==================================================================== 프롤로그
def kog_letter():
    B.letter('kc_kog_letter', '윤 역관 보시게', ['해가 저무니 그날 밤 우정총국의 불빛이 다시 떠오르네. 그 사흘 동안 자네가 옮긴 말들을 나는 잊지 못하네.',
                                            '해가 바뀌면 나는 상하이에 가 보려 하네. 청의 이홍장을 만나 조선의 앞날을 논해 볼 생각이네.',
                                            '자네는 그날 밤을 어떻게 기억하는가. 보태지도 빼지도 말고 들려주게.'], '고균(김옥균)', '계사년(1893) 섣달 · 도쿄에서')

STAMPS = [('5', '문', (214, 90, 100), True), ('10', '문', (60, 90, 170), True), ('25', '문', (220, 140, 50), False), ('50', '문', (60, 140, 90), False), ('100', '문', (150, 80, 120), False)]
def stamp(w, h, val, col):
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    for x in range(0, w, 8): d.ellipse([x - 3, -3, x + 3, 3], fill=(250, 246, 234)); d.ellipse([x - 3, h - 3, x + 3, h + 3], fill=(250, 246, 234))
    d.rectangle([3, 3, w - 4, h - 4], fill=(250, 246, 234)); d.rectangle([8, 8, w - 9, h - 9], fill=col)
    d.rectangle([14, 14, w - 15, h - 15], outline=(250, 246, 234), width=2)
    cx, cy = w / 2, h / 2 - 4
    d.ellipse([cx - 16, cy - 16, cx + 16, cy + 16], fill=(250, 246, 234))
    d.pieslice([cx - 12, cy - 12, cx + 12, cy + 12], 180, 360, fill=sh(col, 0.6)); d.pieslice([cx - 12, cy - 12, cx + 12, cy + 12], 0, 180, fill=sh(col, 1.3))
    d.text((cx, 26), '大朝鮮國', font=F(11, 'serif'), fill=(250, 246, 234), anchor='mm')
    d.text((cx, h - 30), val + '文', font=F(16, 'serif'), fill=(250, 246, 234), anchor='mm')
    return im

def stamps():
    im = paper(seed=21); d = ImageDraw.Draw(im)
    title(d, '우리나라 첫 우표 · 문위우표 (1884)', sub='우정총국이 문을 열 때 일본에 맡겨 찍은 다섯 가지')
    for k, (v, u, col, sold) in enumerate(STAMPS):
        x = 62 + k * 140; y = 120
        st = stamp(104, 136, v, col); im.alpha_composite(st, (x, y)); d = ImageDraw.Draw(im)
        d.text((x + 52, y + 156), v + u, font=F(20), fill=INK, anchor='mm')
        if sold: d.text((x + 52, y + 186), '팔았음', font=F(15), fill=(40, 110, 60), anchor='mm')
        else:
            d.line([(x - 4, y - 4), (x + 108, y + 140)], fill=(190, 40, 40), width=3)
            for j, ln in enumerate(['늦게 도착해', '한 장도 팔지 못함']): d.text((x + 52, y + 184 + j * 18), ln, font=F(13), fill=RED, anchor='mm')
    footnote(d, '윤재의 메모: 정변으로 우정총국이 20일 만에 문을 닫아, 늦게 온 세 가지는 쓰이지 못했다')
    S(im, 'kc_stamps')

BUNDLES = [('一', '1882 겨울', '도쿄'), ('二', '1884', '장터 · 우정총국'), ('三', '12월 4일', '첫째 날'), ('四', '12월 5일', '둘째 날'), ('五', '12월 6일', '셋째 날'), ('六', '1885~93', '그 뒤')]
def bundles():
    im = paper(seed=23); d = ImageDraw.Draw(im)
    title(d, '편지와 신문 스크랩 여섯 묶음', sub='1882 ~ 1893')
    for k, (n, yr, wh) in enumerate(BUNDLES):
        x = 46 + k * 120; y = 118
        for j in range(4): d.rectangle([x + j * 2, y + 14 - j * 4, x + 100 + j * 2, y + 210 - j * 4], fill=[(244, 238, 222), (236, 228, 206), (246, 242, 230), (230, 222, 200)][j], outline=(170, 150, 120))
        d.line([(x + 50, y - 4), (x + 50, y + 214)], fill=(150, 90, 50), width=3); d.line([(x, y + 110), (x + 106, y + 110)], fill=(150, 90, 50), width=3)
        d.rectangle([x + 18, y + 26, x + 84, y + 90], fill=(250, 246, 234), outline=(140, 110, 70))
        d.text((x + 51, y + 58), n, font=F(30, 'serif'), fill=INK, anchor='mm')
        d.rectangle([x + 6, y + 132, x + 98, y + 184], fill=(250, 246, 234), outline=(170, 150, 120))
        d.text((x + 52, y + 146), yr, font=F(14), fill=RED, anchor='mm'); d.text((x + 52, y + 170), wh, font=F(12), fill=INK, anchor='mm')
    footnote(d, '묶음 하나 = 한 장')
    S(im, 'kc_bundles')

# ==================================================================== 1장
def kyunmun():
    im = paper(seed=25, kind='letter'); d = ImageDraw.Draw(im)
    for yy in range(80, CH - 30, 36): d.line([(60, yy), (CW - 60, yy)], fill=(206, 196, 176))
    d.text((70, 34), '견문록 · 임오년(1882) 겨울 · 도쿄 긴자', font=F(22, 'serif'), fill=(60, 50, 80))
    rows = [('가스등', '밤에도 낮처럼 밝은 거리'), ('벽돌 거리', '불에 타지 않는 벽돌집, 2층 건물'), ('철도 마차', '말이 쇠길(레일) 위로 수레를 끈다'),
            ('우체통', '편지를 나라가 전해 준다 (우편)'), ('신문', '백성이 나랏일과 세상일을 신문으로 읽는다')]
    for k, (a, b_) in enumerate(rows):
        y = 86 + k * 66
        d.ellipse([70, y + 6, 92, y + 28], fill=(190, 60, 50)); d.text((81, y + 17), str(k + 1), font=F(14), fill=(255, 250, 240), anchor='mm')
        d.text((106, y + 4), a, font=F(22, 'serif'), fill=(40, 34, 60)); d.text((260, y + 8), b_, font=F(19, 'serif'), fill=(60, 50, 80))
    d.text((CW - 70, CH - 30), '→ 모두 메이지 유신(1868) 뒤에 생긴 것', font=F(16), fill=RED, anchor='rm')
    S(im, 'kc_kyunmun')

def sunbo_page(w=800, h=450, aged=True):
    im = paper(w, h, kind='news', seed=27); d = ImageDraw.Draw(im)
    d.rectangle([24, 20, w - 24, h - 20], outline=(60, 50, 40), width=3)
    d.rectangle([w - 120, 30, w - 34, h - 30], outline=(60, 50, 40), width=2)
    for k, ch in enumerate('漢城旬報'): d.text((w - 77, 70 + k * 78), ch, font=F(52, 'serif'), fill=(30, 24, 20), anchor='mm')
    d.text((w - 150, 50), '第一號', font=F(16, 'serif'), fill=(30, 24, 20), anchor='mm')
    rnd = random.Random(1883)
    hanja = '國內官報各國近事論說朝鮮淸日本英國美國俄羅斯大洋鐵道電信郵便學校兵制商務物價年月日開港通商條約政府人民'
    f = F(15, 'serif')
    for col in range(30):
        x = w - 152 - col * 21
        if x < 40: break
        y = 70
        if col in (0, 11, 22): d.rectangle([x - 9, 66, x + 9, 94], fill=(60, 50, 40)); y = 104
        while y < h - 40:
            d.text((x, y), rnd.choice(hanja), font=f, fill=(50, 42, 36), anchor='mm'); y += 18
    d.line([(40, 60), (w - 140, 60)], fill=(60, 50, 40), width=2)
    d.text((300, 40), '朝鮮開國四百九十二年 十月 初一日 · 博文局', font=F(15, 'serif'), fill=(40, 34, 30), anchor='mm')
    return im

def sunbo():
    im = sunbo_page()
    d = ImageDraw.Draw(im)
    d.rounded_rectangle([40, CH - 70, 420, CH - 30], 8, fill=(40, 34, 30))
    d.text((230, CH - 50), '『한성순보』 첫 호 · 1883년 10월 31일 (양력)', font=F(15), fill=(250, 240, 220), anchor='mm')
    S(im, 'kc_sunbo')

def burnt_type():
    im = Image.new('RGB', (CW, CH), (30, 26, 24)); d = ImageDraw.Draw(im)
    for k in range(60):
        r = random.Random(k); x, y = r.randint(0, CW), r.randint(0, CH); d.ellipse([x, y, x + r.randint(20, 80), y + r.randint(8, 30)], fill=(40 + r.randint(0, 20),) * 3)
    d.rounded_rectangle([290, 90, 510, 330], 14, fill=(120, 116, 112), outline=(70, 66, 62), width=6)
    d.rounded_rectangle([310, 110, 490, 310], 10, fill=(150, 146, 140))
    gl = Image.new('RGBA', (180, 180), (0, 0, 0, 0)); gd = ImageDraw.Draw(gl)
    gd.text((90, 90), '報', font=F(140, 'serif'), fill=(60, 56, 52), anchor='mm')
    im.paste(gl.transpose(Image.FLIP_LEFT_RIGHT), (310, 120), gl.transpose(Image.FLIP_LEFT_RIGHT))
    d = ImageDraw.Draw(im)
    for k in range(14):
        r = random.Random(100 + k); x, y = 290 + r.randint(0, 200), 90 + r.randint(0, 220); d.ellipse([x, y, x + r.randint(10, 30), y + r.randint(6, 16)], fill=(36, 32, 30))
    d.text((CW / 2, 380), '타다 남은 활자 · \'報(보)\' 자가 거울처럼 거꾸로 새겨져 있다', font=F(18), fill=(236, 226, 206), anchor='mm')
    S(im, 'kc_burnt_type')

# ==================================================================== 3장 · 축하연 좌석표
SEATS = [('홍영식', '우정총국 총판 · 주인'), ('민영익', '우영사'), ('푸트', '미국 공사'), ('윤치호', '미국 공사 통역'), ('애스턴', '영국 총영사'),
         ('진수당', '청 상무총판'), ('묄렌도르프', '외교 고문'), ('시마무라', '일본 공사관 서기관'), ('김옥균', ''), ('박영효', ''), ('?', '')]
def banquet():
    im = paper(seed=31); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '축하연 좌석표')
    d.text((300, 36), '우정총국 개국 축하연 · 갑신년 10월 17일', font=F(19, 'serif'), fill=INK, anchor='mm')
    d.rounded_rectangle([90, 150, 510, 290], 40, fill=(160, 50, 46), outline=(110, 30, 26), width=3)
    pos = [(300, 112), (150, 112), (220, 112), (380, 112), (450, 112), (150, 330), (220, 330), (300, 330), (380, 330), (450, 330), (56, 220)]
    order = [0, 1, 2, 3, 4, 5, 6, 10, 7, 8, 9]
    for k, (x, y) in enumerate(pos):
        nm, role = SEATS[order[k]]
        empty = nm == '?'
        d.rounded_rectangle([x - 34, y - 26, x + 34, y + 26], 8, fill=(250, 246, 234) if not empty else (255, 236, 190), outline=(140, 110, 70) if not empty else RED, width=2 if not empty else 3)
        d.text((x, y - 6), nm if not empty else '빈자리', font=F(14 if len(nm) < 5 else 12), fill=INK if not empty else RED, anchor='mm')
        if role: d.text((x, y + 13), role[:8], font=F(9, 'reg'), fill=(110, 90, 70), anchor='mm')
    d.rounded_rectangle([540, 70, 780, 420], 10, fill=(250, 246, 234), outline=(150, 120, 80), width=2)
    d.text((660, 92), '초대한 외국 손님', font=F(17), fill=RED, anchor='mm')
    guests = ['미국 공사 푸트', '영국 총영사 애스턴', '청 상무총판 진수당', '일본 공사 다케조에', '외교 고문 묄렌도르프']
    for k, g in enumerate(guests): d.text((560, 124 + k * 34), '· ' + g, font=F(16), fill=INK)
    text_block(d, 556, 304, 210, '좌석표의 이름과 견주어 오지 않은 사람을 찾아요.', size=14, col=(110, 90, 70))
    S(im, 'kc_banquet')

# ==================================================================== 4장 · 명단 · 정강
def roster():
    im = paper(seed=33, kind='letter'); d = ImageDraw.Draw(im)
    tag(d, 24, 18, '명단 쪽지 (12월 5일 아침)')
    rows = [('영의정', '이재원 (왕실 어른)'), ('좌의정', '홍 ○○'), ('호조참판 (재정)', '김 ○○'), ('전후영사 · 좌포장 (군사 · 경찰)', '박 ○○'),
            ('좌우영사 · 외교 사무', '서광○'), ('병조참판 · 정령관 (생도)', '서 ○○')]
    for k, (a, b_) in enumerate(rows):
        y = 80 + k * 54
        d.text((70, y + 12), a, font=F(19, 'serif'), fill=(40, 34, 60)); d.text((470, y + 12), b_, font=F(19, 'serif'), fill=(60, 50, 80))
        d.line([(60, y + 44), (CW - 60, y + 44)], fill=(206, 196, 176))
    footnote(d, '급히 적느라 이름이 몇 자 지워졌다 · 사람들의 말을 떠올려 채워 보자')
    S(im, 'kc_roster')

def plan14():
    im = paper(seed=35); d = ImageDraw.Draw(im)
    title(d, '갑신정변 14개조 정강 (요약)', sub='김옥균 『갑신일록』 · 1884년 12월 6일 발표')
    groups = [('청과의 관계', ['대원군을 곧 돌아오게 함', '청에 대한 조공 허례 폐지'], (190, 70, 60)),
              ('신분 · 인재', ['문벌 폐지 · 인민 평등권', '능력에 따른 인재 등용'], (60, 110, 170)),
              ('나라 살림 (재정)', ['지조법 개혁', '재정은 호조로 일원화', '혜상공국 · 환곡 폐지'], (60, 140, 90)),
              ('정치 · 기관', ['의정부 회의로 정령 결정', '내시부 · 규장각 등 폐지', '순사 설치 (근대 경찰)'], (150, 110, 50))]
    for k, (h, items, col) in enumerate(groups):
        x = 40 + (k % 2) * 370; y = 100 + (k // 2) * 160
        d.rounded_rectangle([x, y, x + 350, y + 146], 10, fill=(250, 246, 234), outline=col, width=3)
        d.rectangle([x, y, x + 350, y + 32], fill=col); d.text((x + 175, y + 16), h, font=F(18), fill=(255, 250, 240), anchor='mm')
        text_block(d, x + 16, y + 42, 320, items, size=16, bullet='·', gap=4)
    footnote(d, '청에서 벗어난 자주 국가 · 신분 차별 없는 사회 · 근대 재정과 정치 (토지 문제는 빠짐)')
    S(im, 'kc_14')

# ==================================================================== 5장 · 창덕궁 지도 (턴제 방어)
CD_GATES = [('돈화문', 0.30, 0.90), ('단봉문', 0.50, 0.92), ('선인문', 0.86, 0.66), ('금호문', 0.09, 0.62), ('요금문', 0.12, 0.22)]
def changdeok():
    W_, H_ = 760, 520
    im = Image.new('RGBA', (W_, H_), (214, 204, 172, 255)); d = ImageDraw.Draw(im)
    rnd = random.Random(1884)
    for _ in range(2500):
        x, y = rnd.randint(0, W_ - 1), rnd.randint(0, H_ - 1); d.point((x, y), fill=sh((214, 204, 172), 0.93 + rnd.random() * 0.1))
    wall = [(0.09, 0.14), (0.40, 0.08), (0.70, 0.12), (0.86, 0.30), (0.86, 0.80), (0.70, 0.92), (0.30, 0.92), (0.09, 0.80)]
    P = [(x * W_, y * H_) for x, y in wall]
    d.polygon(P, fill=(196, 206, 170)); d.line(P + [P[0]], fill=(120, 80, 60), width=7)
    for (cx, cy) in ((0.3, 0.2), (0.5, 0.18), (0.62, 0.24), (0.42, 0.28), (0.72, 0.36)):
        for k in range(3): d.ellipse([cx * W_ - 26 + k * 16, cy * H_ - 16, cx * W_ + k * 16, cy * H_ + 12], fill=(110, 150, 100))
    d.text((0.5 * W_, 0.25 * H_), '후원', font=F(18), fill=(60, 90, 60), anchor='mm')
    def bld(x, y, w, h, nm, col=(170, 60, 50)):
        X, Y = x * W_, y * H_
        d.rectangle([X - w / 2, Y - h / 2, X + w / 2, Y + h / 2], fill=col, outline=(80, 40, 30), width=2)
        d.rectangle([X - w / 2 - 6, Y - h / 2 - 8, X + w / 2 + 6, Y - h / 2 + 4], fill=(80, 86, 96))
        d.text((X, Y + h / 2 + 14), nm, font=F(14), fill=(50, 40, 30), anchor='mm')
    bld(0.40, 0.66, 110, 40, '인정전'); bld(0.58, 0.52, 80, 30, '희정당'); bld(0.66, 0.68, 70, 28, '관물헌 (개화당)', col=(60, 90, 150))
    bld(0.30, 0.45, 60, 24, '선원전'); bld(0.74, 0.46, 60, 24, '대조전')
    # 바깥: 청군 진영 (동쪽 창경궁 쪽 · 남쪽)
    d.text((0.96 * W_, 0.50 * H_), '창경궁 →', font=F(14), fill=(90, 70, 50), anchor='mm')
    for (x, y) in ((0.95, 0.72), (0.40, 0.99), (0.20, 0.99), (0.98, 0.86)):
        X, Y = x * W_, y * H_
        d.line([(X, Y - 2), (X, Y - 26)], fill=(60, 40, 20), width=2); d.polygon([(X, Y - 26), (X + 18, Y - 20), (X, Y - 13)], fill=(240, 190, 40))
    for (nm, x, y) in CD_GATES:
        X, Y = x * W_, y * H_
        d.rectangle([X - 22, Y - 14, X + 22, Y + 10], fill=(170, 60, 50), outline=(80, 40, 30), width=2); d.rectangle([X - 26, Y - 20, X + 26, Y - 12], fill=(80, 86, 96))
    d.rounded_rectangle([10, 10, 300, 40], 8, fill=(250, 246, 234), outline=(150, 120, 80))
    d.text((155, 25), '창덕궁 (간략한 그림) · 1884년 12월 6일', font=F(14), fill=INK, anchor='mm')
    S(im, 'kc_changdeok')

# ==================================================================== 6장 · 조약 · 동아시아 바다 · 정동
TREATY2 = [
    ('한성 조약 (1885.1 · 조선 ↔ 일본)', None, (0.27, 0.22)), ('톈진 조약 (1885.4 · 청 ↔ 일본)', None, (0.73, 0.22)),
    ('제2조', '조선은 일본에 11만 원을 물어 준다. (정변 때 해를 입은 일본인 · 불탄 공사관)', (0.27, 0.45)),
    ('제4조', '불탄 일본 공사관을 새로 지을 땅을 내주고, 짓는 비용 2만 원을 낸다.', (0.27, 0.74)),
    ('제1조', '청과 일본은 넉 달 안에 조선에 둔 군대를 모두 물린다.', (0.73, 0.45)),
    ('제3조', '앞으로 조선에 일이 생겨 군대를 보낼 때는 서로 미리 문서로 알린다(行文知照).', (0.73, 0.74)),
]
def treaty2():
    im = paper(seed=37, kind='letter'); d = ImageDraw.Draw(im)
    d.line([(CW / 2, 40), (CW / 2, CH - 30)], fill=(150, 120, 80), width=2)
    for (h, t, (cx, cy)) in TREATY2:
        if t is None:
            d.text((cx * CW, cy * CH - 40), h, font=F(19, 'serif'), fill=INK, anchor='mm'); continue
        bw, bh = 340, 112; x0 = cx * CW - bw / 2; y0 = cy * CH - bh / 2
        d.rectangle([x0, y0, x0 + bw, y0 + bh], fill=(250, 246, 234), outline=(140, 110, 80), width=2)
        d.text((x0 + 12, y0 + 8), h, font=F(17, 'serif'), fill=RED)
        text_block(d, x0 + 12, y0 + 32, bw - 24, t, size=16, gap=3)
    d.text((CW - 46, CH - 20), '(쉽게 풀어 옮김)', font=F(13, 'reg'), fill=(120, 100, 80), anchor='rm')
    S(im, 'kc_treaty2')

EA_MARKS = None
def eastasia():
    global EA_MARKS
    W_, H_ = 760, 520
    box = (108, 142, 19, 47)
    def col(p, o):
        n = (p.get('NAME') or '')
        if o == 'ru': return (200, 200, 208)
        if o == 'jp': return (236, 214, 190)
        if o == 'qing': return (236, 222, 170)
        if 'Korea' in n: return (210, 236, 200)
        if o == 'gb': return (236, 196, 196)
        return (226, 220, 206)
    mp, pj = GEO.render(1880, box, (W_, H_), colors=col, line_w=0.6, seed=7, paper=False)
    mp = mp.convert('RGBA'); d = ImageDraw.Draw(mp)
    for (lo, la, t, sz) in ((127.5, 38.6, '조선', 18), (114, 33, '청', 22), (139.5, 37.2, '일본', 18), (134, 46, '러시아', 18)):
        x, y = pj(lo, la); d.text((x, y), t, font=F(sz), fill=(40, 30, 24), anchor='mm', stroke_width=3, stroke_fill=(250, 244, 226))
    places = {'블라디보스토크': (131.9, 43.1), '홍콩': (114.17, 22.3), '거문도': (127.31, 34.03), '웨이하이': (122.12, 37.5)}
    marks = {}
    for k, (lo, la) in places.items():
        x, y = pj(lo, la); marks[k] = (round(x / W_, 3), round(y / H_, 3))
        d.ellipse([x - 6, y - 6, x + 6, y + 6], fill=(190, 50, 40), outline=(255, 250, 240), width=2)
    # 러시아 남하 길 (점선)
    a = pj(131.9, 43.1); b_ = pj(129.5, 36.0); c_ = pj(127.4, 33.4)
    for (p, q) in ((a, b_), (b_, c_)):
        n = 12
        for i in range(n):
            if i % 2: continue
            t0, t1 = i / n, (i + 1) / n
            d.line([(p[0] + (q[0] - p[0]) * t0, p[1] + (q[1] - p[1]) * t0), (p[0] + (q[0] - p[0]) * t1, p[1] + (q[1] - p[1]) * t1)], fill=(120, 120, 140), width=3)
    d.text((20, H_ - 20), '1885년 동아시아 바다 (러시아 함대가 남쪽으로 나오는 길: 점선)', font=F(13), fill=(60, 50, 40), stroke_width=2, stroke_fill=(250, 244, 226))
    EA_MARKS = marks
    S(mp, 'kc_eastasia')
    print('  동아시아 지도 표시 자리:', marks)

JD_SPOTS = [('구리개 병원', 0.80, 0.30), ('붉은 벽돌 학교', 0.30, 0.42), ('언덕 위 한옥 학교', 0.16, 0.72), ('나라에서 세운 학교', 0.52, 0.78)]
def jeongdong_map():
    W_, H_ = 760, 520
    im = Image.new('RGBA', (W_, H_), (232, 222, 190, 255)); d = ImageDraw.Draw(im)
    rnd = random.Random(1888)
    for _ in range(2500):
        x, y = rnd.randint(0, W_ - 1), rnd.randint(0, H_ - 1); d.point((x, y), fill=sh((232, 222, 190), 0.93 + rnd.random() * 0.1))
    d.line([(0, 0.58 * H_), (W_, 0.50 * H_)], fill=(200, 180, 140), width=14); d.text((0.62 * W_, 0.47 * H_), '큰길', font=F(13), fill=(110, 90, 60), anchor='mm')
    d.line([(0.40 * W_, 0), (0.42 * W_, H_)], fill=(200, 180, 140), width=10)
    d.line([(0.02 * W_, 0.05 * H_), (0.06 * W_, 0.95 * H_)], fill=(140, 130, 116), width=6); d.text((0.07 * W_, 0.08 * H_), '도성', font=F(12), fill=(90, 80, 70), anchor='lm')
    # 공사관 (깃발) — 길잡이
    for (x, y, nm, c) in ((0.26, 0.20, '미국 공사관', (60, 80, 150)), (0.60, 0.20, '영국 공사관', (150, 50, 50)), (0.18, 0.36, '러시아 공사관', (90, 90, 120))):
        X, Y = x * W_, y * H_
        d.rectangle([X - 30, Y - 14, X + 30, Y + 14], fill=(220, 214, 200), outline=(120, 110, 100)); d.line([(X + 20, Y - 14), (X + 20, Y - 34)], fill=(80, 80, 80), width=2)
        d.rectangle([X + 21, Y - 34, X + 38, Y - 24], fill=c); d.text((X, Y + 24), nm, font=F(12), fill=(80, 70, 60), anchor='mm')
    # 네 자리 (그림만)
    def brick(X, Y):
        d.rectangle([X - 34, Y - 26, X + 34, Y + 18], fill=(170, 80, 60), outline=(90, 40, 30), width=2)
        for k in range(4): d.rectangle([X - 26 + k * 16, Y - 18, X - 18 + k * 16, Y - 6], fill=(230, 226, 214)); d.rectangle([X - 26 + k * 16, Y, X - 18 + k * 16, Y + 10], fill=(230, 226, 214))
        d.polygon([(X - 38, Y - 26), (X + 38, Y - 26), (X + 26, Y - 40), (X - 26, Y - 40)], fill=(80, 86, 96))
    def hanok(X, Y, hill=False):
        if hill: d.ellipse([X - 70, Y - 10, X + 70, Y + 40], fill=(170, 190, 140))
        d.rectangle([X - 30, Y - 14, X + 30, Y + 12], fill=(236, 228, 210), outline=(120, 90, 60), width=2)
        d.polygon([(X - 40, Y - 14), (X + 40, Y - 14), (X + 30, Y - 32), (X - 30, Y - 32)], fill=(70, 74, 82))
    def hospital(X, Y):
        hanok(X, Y); d.rectangle([X - 6, Y - 6, X + 6, Y + 8], fill=(255, 255, 255)); d.rectangle([X - 2, Y - 4, X + 2, Y + 6], fill=(40, 120, 70)); d.rectangle([X - 5, Y - 1, X + 5, Y + 2], fill=(40, 120, 70))
    def gov(X, Y):
        hanok(X, Y); d.rectangle([X - 36, Y + 14, X + 36, Y + 22], fill=(170, 60, 50))
    hospital(0.80 * W_, 0.30 * H_ - 20); brick(0.30 * W_, 0.42 * H_ - 20); hanok(0.16 * W_, 0.72 * H_ - 20, True); gov(0.52 * W_, 0.78 * H_ - 20)
    for (nm, x, y) in JD_SPOTS: d.ellipse([x * W_ - 5, y * H_ - 5, x * W_ + 5, y * H_ + 5], fill=(190, 50, 40))
    d.rounded_rectangle([W_ - 250, H_ - 40, W_ - 10, H_ - 10], 8, fill=(250, 246, 234), outline=(150, 120, 80))
    d.text((W_ - 130, H_ - 25), '1880년대 정동 둘레 (간략한 그림)', font=F(13), fill=INK, anchor='mm')
    S(im, 'kc_jeongdong')
# ==================================================================== 사진 자리
def photo_slot(name, head, what, draw, desc=None):
    ph = os.path.join(HERE, 'photos', name.replace('kc_photo_', '') + '.png')
    if os.path.exists(ph):
        src = Image.open(ph).convert('RGB'); AH = CH - 40
        if src.height > src.width * 1.1:          # 세로로 긴 사진: 왼쪽에 크게, 오른쪽에 설명
            im = Image.new('RGB', (CW, CH), (30, 26, 24))
            bg = ImageEnhance.Brightness(ImageOps.fit(src, (CW, CH)).filter(ImageFilter.GaussianBlur(22))).enhance(0.3); im.paste(bg, (0, 0))
            k = (CH - 20) / src.height; fg = src.resize((max(1, int(src.width * k)), CH - 20), Image.LANCZOS)
            px = 40; im.paste(fg, (px, 10))
            d = ImageDraw.Draw(im); x0 = px + fg.width + 30; tw = CW - x0 - 30
            d.rectangle([x0 - 12, 0, CW, CH], fill=(30, 26, 24))
            lines, cur = [], ''
            for w in head.replace(' (', '\n(').split('\n'):
                lines.append(w)
            fs = 26
            while fs > 14 and max(d.textlength(l, font=F(fs)) for l in lines) > tw: fs -= 1
            y = (60 if desc else CH / 2 - (len(lines) * (fs + 12)) / 2)
            for i, l in enumerate(lines):
                d.text((x0, y), l, font=F(fs if i == 0 else max(14, fs - 6)), fill=(250, 240, 220) if i == 0 else (214, 200, 176)); y += fs + 14
            if desc:
                y += 10; d.line([(x0, y), (x0 + 60, y)], fill=(200, 160, 90), width=2); y += 18
                for para in desc:
                    cur = ''
                    for wd in para.split(' '):
                        t_ = (cur + ' ' + wd) if cur else wd
                        if cur and d.textlength(t_, font=F(17)) > tw: d.text((x0, y), cur, font=F(17), fill=(232, 222, 204)); y += 26; cur = wd
                        else: cur = t_
                    if cur: d.text((x0, y), cur, font=F(17), fill=(232, 222, 204)); y += 26
                    y += 8
            S(im, name); return
        bg = ImageEnhance.Brightness(ImageOps.fit(src, (CW, AH)).filter(ImageFilter.GaussianBlur(18))).enhance(0.35)
        im = Image.new('RGB', (CW, CH), (24, 20, 18)); im.paste(bg, (0, 0))
        k = min((CW - 16) / src.width, (AH - 12) / src.height); fg = src.resize((max(1, int(src.width * k)), max(1, int(src.height * k))), Image.LANCZOS)
        im.paste(fg, ((CW - fg.width) // 2, (AH - fg.height) // 2))
        d = ImageDraw.Draw(im); d.rectangle([0, AH, CW, CH], fill=(30, 26, 24))
        d.text((CW / 2, AH + 20), head, font=F(20), fill=(250, 240, 220), anchor='mm')
        S(im, name); return
    im = Image.new('RGB', (CW, CH), (60, 56, 52)); d = ImageDraw.Draw(im)
    draw(im, d)
    d.rectangle([0, CH - 52, CW, CH], fill=(30, 26, 24))
    d.text((CW / 2, CH - 36), head, font=F(18), fill=(250, 240, 220), anchor='mm')
    d.text((CW / 2, CH - 14), '예시 그림 · 실제 사진을 img/pictures/%s.png 로 넣으면 바뀌어요 (%s)' % (name, what), font=F(12), fill=(200, 190, 170), anchor='mm')
    S(im, name)


def _sepia_people(im, d, n, y_base, gat=True, seed=1, x0=80, x1=720, cols=None):
    """옛 사진 느낌의 사람 줄 (얼굴은 그리지 않고 옷차림만)"""
    rnd = random.Random(seed)
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        c = (cols[k % len(cols)] if cols else (rnd.randint(200, 230),) * 3)
        d.polygon([(x - 34, y_base), (x - 26, y_base - 120), (x + 26, y_base - 120), (x + 34, y_base)], fill=c)
        d.ellipse([x - 17, y_base - 160, x + 17, y_base - 118], fill=(196, 180, 150))
        if gat:
            d.ellipse([x - 40, y_base - 160, x + 40, y_base - 146], fill=(40, 36, 32)); d.rectangle([x - 15, y_base - 186, x + 15, y_base - 152], fill=(40, 36, 32))
        d.line([(x, y_base - 116), (x, y_base - 40)], fill=sh(c, 0.8), width=2)

def photos():
    def sunbo_d(im, d):
        im.paste(sunbo_page(CW, CH - 52).convert('RGB'), (0, 0))
    def bobingsa_d(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(186, 170, 140))
        for y in range(0, CH - 52, 3): d.line([(0, y), (CW, y)], fill=(180 + (y % 7), 164 + (y % 5), 134))
        d.rectangle([40, 300, CW - 40, CH - 60], fill=(150, 130, 100))
        _sepia_people(im, d, 8, 330, True, seed=1883, cols=[(70, 60, 50), (210, 200, 180), (90, 80, 70), (220, 210, 190)])
        d.rectangle([30, 20, CW - 30, CH - 62], outline=(110, 90, 66), width=6)
    def ujeong_d(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(200, 196, 186))
        d.rectangle([0, 300, CW, CH - 52], fill=(170, 160, 140))
        d.rectangle([150, 190, 650, 300], fill=(150, 60, 50)); d.rectangle([140, 296, 660, 312], fill=(150, 146, 136))
        for x in range(160, 650, 50): d.rectangle([x, 200, x + 40, 290], fill=(226, 218, 196))
        d.polygon([(110, 196), (690, 196), (620, 110), (180, 110)], fill=(70, 74, 82)); d.rectangle([180, 100, 620, 112], fill=(50, 52, 58))
        d.rectangle([340, 150, 460, 178], fill=(40, 34, 30)); d.text((400, 164), '郵征總局', font=F(18, 'serif'), fill=(240, 220, 160), anchor='mm')
        for x in (60, 720): d.ellipse([x - 40, 140, x + 40, 260], fill=(90, 120, 80)); d.rectangle([x - 4, 250, x + 4, 300], fill=(90, 70, 50))
    def four_d(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(176, 162, 136))
        for y in range(0, CH - 52, 4): d.line([(0, y), (CW, y)], fill=(170 + (y % 9), 156 + (y % 6), 130))
        _sepia_people(im, d, 4, 360, True, seed=1884, x0=180, x1=620, cols=[(220, 212, 196), (60, 56, 50), (210, 200, 184), (70, 64, 56)])
        d.rectangle([30, 20, CW - 30, CH - 62], outline=(110, 90, 66), width=6)
    def cemetery_d(im, d):
        d.rectangle([0, 0, CW, 160], fill=(170, 200, 220)); d.rectangle([0, 150, CW, 230], fill=(90, 140, 170))
        d.polygon([(0, 260), (300, 200), (620, 230), (CW, 210), (CW, CH - 52), (0, CH - 52)], fill=(110, 140, 90))
        d.rectangle([250, 250, 560, 360], outline=(200, 196, 186), width=4)
        for k, x in enumerate((300, 380, 460, 520)):
            d.rectangle([x - 4, 260 + (k % 2) * 8, x + 4, 340], fill=(236, 232, 222)); d.rectangle([x - 18, 280 + (k % 2) * 8, x + 18, 288 + (k % 2) * 8], fill=(236, 232, 222))
    def light_d(im, d):
        d.rectangle([0, 0, CW, CH - 52], fill=(30, 34, 54))
        d.rectangle([0, 280, CW, CH - 52], fill=(60, 60, 70))
        d.rectangle([160, 170, 640, 280], fill=(140, 60, 50))
        for x in range(180, 640, 56): d.rectangle([x, 182, x + 44, 270], fill=(250, 226, 160))
        d.polygon([(120, 176), (680, 176), (610, 96), (190, 96)], fill=(60, 62, 70))
        for x in (120, 680):
            d.line([(x, 280), (x, 120)], fill=(80, 70, 60), width=4); d.ellipse([x - 12, 108, x + 12, 132], fill=(255, 240, 180))
            g = Image.new('L', (CW, CH), 0); ImageDraw.Draw(g).ellipse([x - 80, 40, x + 80, 200], fill=90); g = g.filter(ImageFilter.GaussianBlur(30)); im.paste((255, 230, 150), (0, 0), g)
        d.text((400, 60), '乾淸宮', font=F(16, 'serif'), fill=(230, 220, 190), anchor='mm')
    photo_slot('kc_photo_sunbo', '『한성순보』 제6호 (1883년 12월)', '한성순보 사진', sunbo_d,
               ['박문국에서 열흘마다 펴낸 우리나라 첫 근대 신문.', '나라의 소식(국내관보)과 외국 소식을 한문으로 실었다.',
                '오른쪽 위 큰 제목 漢城旬報, 그 아래 博文局이 보인다.'])
    photo_slot('kc_photo_bobingsa', '보빙사 일행 (1883 · 앞줄 오른쪽 서양인은 안내를 맡은 로웰)', '보빙사 사진', bobingsa_d)
    photo_slot('kc_photo_ujeong', '우정총국 건물 (지금도 서울 종로에 남아 있음)', '우정총국 사진', ujeong_d)
    photo_slot('kc_photo_four', '갑신정변을 이끈 사람들 (일본 망명 시절)', '개화파 사진', four_d)
    photo_slot('kc_photo_cemetery', '거문도 영국군 묘지', '영국군 묘지 사진', cemetery_d)
    photo_slot('kc_photo_light', '경복궁 건청궁 전등 (1887)', '전등 · 건청궁 사진', light_d)

# ==================================================================== 사료 카드 · 정리
def cards_src():
    card('kc_src_split', '개화파의 분화 (1882 ~ 1883)', [
        '배경: 임오군란 뒤 청군 주둔 · 조청 상민 수륙 무역 장정 · 청의 내정 간섭(마젠창 · 묄렌도르프)',
        '온건 개화파: 김홍집 · 김윤식 · 어윤중 → 청과 관계 유지, 청의 양무운동 본보기, 동도서기, 점진적 개혁',
        '급진 개화파(개화당): 김옥균 · 박영효 · 홍영식 · 서광범 · 서재필 → 청에서 벗어나기, 일본 메이지 유신 본보기, 급진적 개혁',
        '박문국 설치 · 『한성순보』(1883, 열흘마다 · 한문) · 태극기를 국기로 정함(1883)'], label='사료 카드', size=16)
    card('kc_src_eve', '정변 전야 · 청의 간섭과 개화 정책 (1883 ~ 1884)', [
        '청: 군대 주둔 · 위안스카이 · 청 상인이 한성 안까지 장사 / 정부: 당오전 발행(1883) → 물가 상승',
        '개화 정책: 보빙사(1883, 미국) · 박문국 · 전환국 · 기기창 · 우정총국(1884, 총판 홍영식)',
        '김옥균의 일본 차관 실패 · 청프 전쟁(1884)으로 청군 절반 철수 · 일본 공사 다케조에의 지원 약속',
        '→ 급진 개화파가 정변을 준비함'], label='사료 카드', size=16)
    card('kc_src_day1', '갑신정변 첫째 날 (1884.12.4)', [
        '우정총국 개국 축하연 (일본 공사 다케조에는 오지 않음) → 근처에 불을 질러 신호',
        '민영익이 크게 다침 (미국 의사 알렌이 치료 → 제중원의 계기)',
        '국왕을 경우궁으로 옮기고 일본 공사관 군대(약 150명)에 호위를 청함',
        '민씨 정권의 대신들(민태호 · 민영목 · 조영하 등)이 목숨을 잃음'], label='사료 카드', size=16)
    card('kc_src_day2', '갑신정변 둘째 날 · 14개조 정강 (1884.12.5 ~ 6)', [
        '새 정부: 홍영식(좌의정) · 김옥균(호조참판, 재정) · 박영효 · 서광범(군사) · 서재필(사관생도)',
        '정강: 대원군 귀국 · 조공 허례 폐지 / 문벌 폐지 · 인민 평등권 / 지조법 개혁 · 호조로 재정 일원화 · 혜상공국 폐지 / 의정부 회의 · 순사 설치',
        '의의: 우리나라 첫 근대 국가 개혁안 (입헌 군주제를 지향한 정치 개혁)',
        '한계: 토지 문제 빠짐 · 백성의 뜻을 모으지 못함 · 국왕은 넓은 창덕궁으로 돌아감'], label='사료 카드', size=16)
    card('kc_src_day3', '삼일천하 (1884.12.6)', [
        '위안스카이의 청군 1,500여 명이 창덕궁 공격 · 일본군은 본국 훈령을 핑계로 철수',
        '홍영식 · 박영교 피살 · 김옥균 · 박영효 · 서광범 · 서재필은 일본으로 망명',
        '성난 백성이 일본 공사관 · 개화당 집 · 박문국에 불을 지름 (『한성순보』 중단 → 1886 『한성주보』)',
        '실패 까닭: 외세(일본) 의존 · 백성의 지지 부족 · 준비 부족 · 청군과 병력 차이'], label='사료 카드', size=16)
    card('kc_src_after', '갑신정변 그 뒤 10년 (1885 ~ 1893)', [
        '한성 조약(1885, 조선 ↔ 일본): 배상금 · 공사관 신축비 / 톈진 조약(1885, 청 ↔ 일본): 군대 철수 · 파병 때 서로 미리 알림',
        '거문도 사건(1885 ~ 1887): 영국이 러시아를 막는다며 거문도 점령 · 조선 중립화론(부들러 · 유길준)',
        '근대 시설: 제중원(1885) · 배재학당(1885) · 이화학당(1886) · 육영공원(1886) · 전신(1885) · 경복궁 전등(1887)',
        '방곡령(1889 함경도, 1890 황해도) → 배상금 · 동학 교조신원운동 · 보은 집회(1893)'], label='사료 카드', size=15)

def summaries():
    data = [
        ('kc_sum1', '1장 정리 · 갈라지는 개화', ['임오군란 뒤 청의 간섭 → 개화파가 둘로 나뉨', '온건(김홍집 · 김윤식 · 어윤중): 청과 함께 · 동도서기 · 천천히', '급진(김옥균 · 박영효 · 홍영식 · 서광범 · 서재필): 청에서 벗어나 · 메이지 유신처럼 · 빠르게', '박문국 · 『한성순보』(1883)']),
        ('kc_sum2', '2장 정리 · 정변 전야', ['청군 · 청 상인 · 위안스카이 / 당오전과 물가', '보빙사(1883) · 우정총국(1884)', '청프 전쟁으로 청군 절반 철수 · 일본의 지원 약속']),
        ('kc_sum3', '3장 정리 · 첫째 날 (12.4)', ['우정총국 축하연에서 정변 (일본 공사는 불참)', '국왕을 경우궁으로 · 일본군 약 150명이 호위', '민씨 정권 대신들 제거']),
        ('kc_sum4', '4장 정리 · 둘째 날 (12.5)', ['새 정부 구성 (홍영식 · 김옥균 · 박영효 · 서광범 · 서재필)', '14개조 정강: 자주 · 평등 · 재정 · 정치 개혁', '국왕은 창덕궁으로 · 장터의 민심은 차가움']),
        ('kc_sum5', '5장 정리 · 셋째 날 (12.6)', ['청군 1,500여 명 공격 · 일본군 철수 → 삼일천하', '홍영식 피살 · 김옥균 등 일본 망명 · 박문국 불탐', '실패 까닭: 외세 의존 · 민중 지지 부족 · 준비 부족']),
        ('kc_sum6', '6장 정리 · 그 뒤 10년', ['한성 조약 · 톈진 조약(1885: 파병 때 미리 알림)', '거문도 사건(1885 ~ 1887) · 중립화론', '제중원 · 배재 · 이화 · 육영공원 · 전신 · 전등 · 방곡령(1889) · 보은 집회(1893)']),
    ]
    for (n, h, ls) in data: card(n, h, ls, label='정리', size=19)
    im = paper(seed=93); d = ImageDraw.Draw(im)
    title(d, '갑신년 그날 밤, 우정총국 한눈에 보기')
    steps = [('1882 ~ 83', '개화파의 분화 · 한성순보'), ('1883 ~ 84', '보빙사 · 당오전 · 우정총국'), ('1884.12.4', '첫째 날 · 우정총국 축하연'),
             ('1884.12.5', '둘째 날 · 새 정부 · 14개조 정강'), ('1884.12.6', '셋째 날 · 청군 공격 · 삼일천하'), ('1885', '한성 조약 · 톈진 조약'),
             ('1885 ~ 87', '거문도 사건 · 중립화론'), ('1885 ~ 87', '제중원 · 배재 · 이화 · 육영공원 · 전등'), ('1889 ~ 93', '방곡령 · 보은 집회')]
    for k, (yr, ev) in enumerate(steps):
        x = 60 + (k % 3) * 236; y = 96 + (k // 3) * 102
        d.rounded_rectangle([x, y, x + 214, y + 80], 10, fill=(250, 244, 228), outline=(150, 120, 80), width=2)
        d.text((x + 14, y + 18), yr, font=F(17), fill=RED, anchor='lm')
        text_block(d, x + 14, y + 34, 190, ev, size=14)
    footnote(d, '→ 3편 「동학농민운동과 갑오개혁」 (1894)으로 이어집니다')
    S(im, 'kc_summary')

def icons():
    def ic(name, fn):
        im = Image.new('RGBA', (64, 64), (0, 0, 0, 0)); d = ImageDraw.Draw(im); fn(d, im); S(outline(im, 0.5), name)
    def letters(d, im):
        for k in range(3): d.rectangle([10 + k * 3, 14 + k * 6, 50 + k * 3, 44 + k * 6], fill=[(244, 238, 222), (236, 228, 206), (246, 242, 230)][k], outline=(150, 130, 100))
        d.line([(32, 10), (32, 60)], fill=(150, 90, 50), width=3)
    def sunbo_i(d, im):
        d.rectangle([10, 8, 54, 56], fill=(236, 230, 214), outline=(100, 90, 80)); d.rectangle([40, 12, 50, 52], outline=(60, 50, 40))
        for x in range(14, 38, 5): d.line([(x, 14), (x, 50)], fill=(120, 110, 100))
    def type_i(d, im):
        d.rounded_rectangle([16, 12, 48, 52], 4, fill=(120, 116, 112), outline=(60, 56, 52), width=2); d.rectangle([22, 18, 42, 46], fill=(150, 146, 140))
        d.text((32, 32), '報', font=F(20, 'serif'), fill=(50, 46, 42), anchor='mm')
    def cardi(d, im):
        d.rectangle([10, 12, 54, 52], fill=(240, 230, 204)); d.rectangle([10, 12, 54, 20], fill=(150, 40, 40))
        for yy in range(26, 48, 6): d.line([(16, yy), (48, yy)], fill=(100, 80, 60))
    for n, fn in (('ki_letters', letters), ('ki_sunbo', sunbo_i), ('ki_type', type_i), ('ki_card', cardi)): ic(n, fn)

def build(root):
    B.ROOT = root; B.OUT = os.path.join(root, 'img', 'pictures'); os.makedirs(B.OUT, exist_ok=True)
    cards_intro(); kog_letter(); stamps(); bundles(); kyunmun(); sunbo(); burnt_type(); banquet(); roster(); plan14()
    changdeok(); treaty2(); eastasia(); jeongdong_map(); photos(); cards_src(); summaries(); icons()
    B.review_card(name='kc_review')
    print('cards', len([f for f in os.listdir(B.OUT) if f.startswith(('kc_', 'ki_'))]))

if __name__ == '__main__':
    build(sys.argv[1])
