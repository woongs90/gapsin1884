"""갑신년 그날 밤, 우정총국 · 지도 9장 (29 x 13칸, 가운데 7~21칸을 걷는다)
 01 윤재의 서재 (1893 밤)   02 도쿄 긴자 (1882)      03 박문국 (1883 · 불탄 뒤)
 04 운종가 (1884)           05 우정총국 (낮 · 축하연 밤)  06 경우궁 (밤) · 창덕궁 (낮)
 07 창덕궁 가는 밤골목 (잠행)  08 거문도 (1885)         09 정동 (1888)
 시대가 갈수록 기와집 사이로 벽돌 건물 · 전신주 · 가스등 · 서양 공사관이 섞여 든다.
"""
import math
from k_mapbase import *
import k_mapbase as MB
from k_m1 import side_walls

MAP_NAMES = ['01 윤재의 서재', '02 도쿄 긴자', '03 박문국', '04 운종가 1884', '05 우정총국', '06 경우궁 · 창덕궁', '07 창덕궁 가는 밤골목', '08 거문도', '09 정동']
GIWA = (70, 74, 82); GIWA_L = (110, 116, 126); WOOD = (128, 86, 54); WOOD_D = (90, 58, 36); WALL_W = (238, 232, 216); STONE_K = (176, 170, 158)
DAN_G = (60, 130, 110); DAN_R = (170, 60, 50); DAN_B = (60, 90, 150)
SKY_T, SKY_B = (132, 176, 214), (220, 228, 228)

def grid_open(ground='.', top=3, x0=7, x1=21):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(top, 12):
        for x in range(x0, x1 + 1): g[y][x] = ground
    g[12][14] = ground; g[11][14] = ground
    return g

def skyk(b, h, top=SKY_T, bot=SKY_B):
    d = ImageDraw.Draw(b)
    for y in range(h): d.line([(0, y), (b.width, y)], fill=mix(top, bot, y / max(1, h - 1)))

def granite_mts(b, base_y, seed=3, col=(150, 150, 140), height=110, peaks=((0.3, 1.0), (0.62, 0.8))):
    """화강암 바위산 (북악산 · 인왕산 느낌)"""
    d = ImageDraw.Draw(b); rnd = random.Random(seed); W_ = b.width
    pts = [(0, base_y)]
    for x in range(0, W_ + 30, 30):
        h_ = 26 + rnd.randint(0, 16)
        for px_, ph in peaks:
            dx = abs(x - px_ * W_) / (W_ * 0.16)
            if dx < 1: h_ += height * ph * (1 - dx * dx)
        pts.append((x, base_y - h_))
    pts.append((W_, base_y))
    d.polygon(pts, fill=mix(col, (120, 150, 120), 0.35))
    for i in range(1, len(pts) - 2):
        x, y = pts[i]
        if rnd.random() < 0.5 and base_y - y > 50:
            d.polygon([(x, y + 4), (x + 18, y + 10), (x + 8, y + 36)], fill=sh(col, 1.18))
    for _ in range(int(W_ / 8)):
        x = rnd.randint(0, W_); y = base_y - rnd.randint(4, 40)
        d.ellipse([x, y, x + 9, y + 6], fill=rnd.choice([(70, 110, 80), (84, 124, 88), (60, 96, 72)]))

def giwa_roof(d, x0, x1, y_ridge, y_eave, col=GIWA, flare=16, ridge=True):
    """처마 끝이 살짝 들린 기와지붕 (정면)"""
    mid = (x0 + x1) / 2
    eave = [(x0 - flare, y_eave - 10)]
    for k in range(1, 20):
        t = k / 20; x = x0 - flare + (x1 - x0 + 2 * flare) * t
        eave.append((x, y_eave + 2 - 12 * (2 * t - 1) ** 4))
    eave.append((x1 + flare, y_eave - 10))
    top = [(x1 - (x1 - x0) * 0.08, y_ridge), (x0 + (x1 - x0) * 0.08, y_ridge)]
    d.polygon(eave + top, fill=col)
    for k in range(0, 40):
        t = k / 39; xa = x0 + (x1 - x0) * 0.08 + (x1 - x0) * 0.84 * t; xb = x0 - flare + (x1 - x0 + 2 * flare) * t
        d.line([(xa, y_ridge + 2), (xb, y_eave - 12 * (2 * t - 1) ** 4)], fill=sh(col, 0.8))
    for (x, y) in eave[1:-1:1]: d.ellipse([x - 2, y - 2, x + 2, y + 2], fill=sh(col, 1.5))
    if ridge:
        d.rectangle([x0 + (x1 - x0) * 0.06, y_ridge - 6, x1 - (x1 - x0) * 0.06, y_ridge + 2], fill=sh(col, 0.55))
        for sx in (x0 + (x1 - x0) * 0.06, x1 - (x1 - x0) * 0.06):
            d.polygon([(sx - 6, y_ridge + 2), (sx + 6, y_ridge + 2), (sx + (8 if sx > mid else -8), y_ridge - 12)], fill=sh(col, 0.5))

def hall(b, x0, x1, y_base, wall_h=58, roof_h=46, wall=WALL_W, wood=WOOD, doors='changho', dan=False, roof=GIWA, sign=None, sign_c=(40, 34, 30)):
    """기와 건물 정면 (기단 · 기둥 · 창호/가게 · 지붕 · 현판)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0 - 8, y_base - 8, x1 + 8, y_base], fill=STONE_K); d.line([(x0 - 8, y_base - 8), (x1 + 8, y_base - 8)], fill=sh(STONE_K, 1.15))
    yt = y_base - 8 - wall_h
    d.rectangle([x0, yt, x1, y_base - 8], fill=wall)
    n = max(2, int((x1 - x0) / 48))
    for k in range(n + 1):
        x = x0 + (x1 - x0) * k / n
        d.rectangle([x - 3, yt, x + 3, y_base - 8], fill=wood)
    for k in range(n):
        xa = x0 + (x1 - x0) * k / n + 5; xb = x0 + (x1 - x0) * (k + 1) / n - 5
        if doors == 'changho':
            d.rectangle([xa, yt + 8, xb, y_base - 12], fill=(236, 228, 204))
            for x in range(int(xa) + 4, int(xb), 6): d.line([(x, yt + 8), (x, y_base - 12)], fill=sh(wood, 1.15))
            for y in range(int(yt) + 12, y_base - 12, 7): d.line([(xa, y), (xb, y)], fill=sh(wood, 1.15))
        elif doors == 'shop':
            d.rectangle([xa, yt + 6, xb, y_base - 10], fill=(70, 50, 38))
        elif doors == 'wall':
            d.rectangle([xa, yt + 30, xb, y_base - 12], fill=sh(wall, 0.9))
        elif doors == 'store':      # 곳간 판자문
            d.rectangle([xa, yt + 6, xb, y_base - 10], fill=sh(wood, 1.1))
            for x in range(int(xa) + 6, int(xb), 8): d.line([(x, yt + 6), (x, y_base - 10)], fill=sh(wood, 0.8))
            d.rectangle([(xa + xb) / 2 - 3, (yt + y_base) / 2 - 3, (xa + xb) / 2 + 3, (yt + y_base) / 2 + 3], fill=(60, 60, 60))
    d.rectangle([x0 - 4, yt - 8, x1 + 4, yt], fill=wood)
    if dan:
        for x in range(int(x0), int(x1), 16):
            d.rectangle([x, yt - 8, x + 7, yt - 1], fill=DAN_G); d.rectangle([x + 8, yt - 8, x + 15, yt - 1], fill=DAN_R if (x // 16) % 2 else DAN_B)
    giwa_roof(d, x0, x1, yt - 8 - roof_h, yt - 6, roof)
    if sign:
        f = F(14, 'serif'); tw = d.textlength(sign, font=f)
        sx = (x0 + x1) / 2
        d.rectangle([sx - tw / 2 - 8, yt - 30, sx + tw / 2 + 8, yt - 10], fill=sign_c, outline=(200, 170, 100))
        d.text((sx, yt - 20), sign, font=f, fill=(240, 220, 160), anchor='mm')

def gwanghwamun(b, cx, base_y, scaffold=True):
    """광화문 (석축 홍예문 셋 + 2층 문루) · 공사 중이면 비계"""
    d = ImageDraw.Draw(b)
    W_, H_ = 420, 74
    d.rectangle([cx - W_ / 2, base_y - H_, cx + W_ / 2, base_y], fill=(196, 188, 170))
    for y in range(int(base_y - H_) + 8, int(base_y), 12):
        off = 0 if (y // 12) % 2 else 18
        for x in range(int(cx - W_ / 2) + off, int(cx + W_ / 2), 36): d.line([(x, y - 12), (x, y)], fill=(170, 162, 146))
        d.line([(cx - W_ / 2, y), (cx + W_ / 2, y)], fill=(170, 162, 146))
    for k, w_ in ((-1, 44), (0, 54), (1, 44)):
        ax = cx + k * 120
        d.chord([ax - w_ / 2, base_y - H_ + 14, ax + w_ / 2, base_y - H_ + 14 + w_], 180, 360, fill=(40, 34, 30))
        d.rectangle([ax - w_ / 2, base_y - H_ + 14 + w_ / 2, ax + w_ / 2, base_y], fill=(40, 34, 30))
    y1 = base_y - H_
    hall(b, cx - 150, cx + 150, y1, wall_h=40, roof_h=30, doors='wall', dan=True, wall=(170, 60, 50))
    giwa_roof(d, cx - 120, cx + 120, y1 - 128, y1 - 92, GIWA)
    d.rectangle([cx - 110, y1 - 92, cx + 110, y1 - 80], fill=(170, 60, 50))
    if scaffold:
        for x in range(int(cx - 170), int(cx + 180), 26): d.line([(x, y1 + 4), (x, y1 - 150)], fill=(150, 110, 70), width=3)
        for y in range(int(y1 - 140), int(y1), 24): d.line([(cx - 170, y), (cx + 170, y)], fill=(150, 110, 70), width=2)
        for x in range(int(cx - 170), int(cx + 150), 52): d.line([(x, y1), (x + 26, y1 - 24)], fill=(130, 96, 60), width=2)

def note_label(b, text, x=9 * TS + 10, y=12 * TS + 12):
    label(b, text, x, y, 12, back=(40, 30, 24, 230))

def sea(b, y0, y1, col=(58, 120, 168), deep=(34, 86, 140), seed=3):
    d = ImageDraw.Draw(b); rnd = random.Random(seed)
    for y in range(int(y0), int(y1)): d.line([(0, y), (b.width, y)], fill=mix(deep, col, (y - y0) / max(1, y1 - y0)))
    for _ in range(int(b.width * (y1 - y0) / 900)):
        x, y = rnd.randint(0, b.width), rnd.randint(int(y0) + 2, int(y1) - 2); d.line([(x, y), (x + rnd.randint(6, 16), y)], fill=sh(col, 1.25))

def fortress(b, x0, x1, y_top, h=52, col=(178, 172, 158), crenel=True):
    """성벽 (돌 쌓기 + 여장)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0, y_top, x1, y_top + h], fill=col)
    rnd = random.Random(x0 + y_top)
    for y in range(int(y_top) + 4, int(y_top + h), 10):
        off = rnd.randint(0, 16)
        for x in range(int(x0) - off, int(x1), 22): d.rectangle([max(x, x0), y, min(x + 20, x1), y + 9], outline=sh(col, 0.8))
    if crenel:
        for x in range(int(x0), int(x1), 30):
            d.rectangle([x, y_top - 16, x + 24, y_top], fill=sh(col, 1.05)); d.rectangle([x + 9, y_top - 10, x + 14, y_top - 5], fill=(50, 46, 42))
            d.line([(x, y_top - 16), (x + 24, y_top - 16)], fill=sh(col, 1.2))

def us_ship(b, x, y, s=1.0, smoke=True, col=(40, 40, 46)):
    """19세기 증기 군함 (옆모습: 돛대 셋 + 굴뚝)"""
    d = ImageDraw.Draw(b)
    d.polygon([(x - 90 * s, y), (x + 100 * s, y), (x + 80 * s, y + 22 * s), (x - 76 * s, y + 22 * s)], fill=col)
    d.line([(x - 86 * s, y + 6 * s), (x + 96 * s, y + 6 * s)], fill=(220, 220, 220), width=max(1, int(2 * s)))
    for k in range(6): d.rectangle([x - 60 * s + k * 26 * s, y + 9 * s, x - 55 * s + k * 26 * s, y + 13 * s], fill=(20, 20, 24))
    for mx in (-56, 6, 64):
        d.line([(x + mx * s, y), (x + mx * s, y - 70 * s)], fill=(60, 50, 40), width=max(1, int(2 * s)))
        for yy in (-58, -40, -22): d.line([(x + (mx - 16) * s, y + yy * s), (x + (mx + 16) * s, y + yy * s)], fill=(60, 50, 40))
    d.rectangle([x - 18 * s, y - 34 * s, x - 6 * s, y], fill=(30, 30, 30))
    if smoke:
        for k in range(5): d.ellipse([x - 26 * s - k * 14 * s, y - 52 * s - k * 6 * s, x - 2 * s - k * 12 * s, y - 36 * s - k * 6 * s], fill=(90 + k * 12, 90 + k * 12, 96 + k * 12))

def steamship(b, x, y, s=1.0, name=None):
    """여객 증기선 (제물포 · 메이지마루)"""
    d = ImageDraw.Draw(b)
    d.polygon([(x - 150 * s, y - 6 * s), (x + 160 * s, y - 6 * s), (x + 130 * s, y + 34 * s), (x - 130 * s, y + 34 * s)], fill=(36, 36, 42))
    d.rectangle([x - 140 * s, y - 6 * s, x + 150 * s, y + 2 * s], fill=(160, 40, 36))
    d.rectangle([x - 90 * s, y - 34 * s, x + 90 * s, y - 6 * s], fill=(236, 232, 220))
    for k in range(10): d.ellipse([x - 82 * s + k * 17 * s, y - 26 * s, x - 74 * s + k * 17 * s, y - 18 * s], fill=(60, 70, 90))
    d.rectangle([x - 14 * s, y - 80 * s, x + 6 * s, y - 34 * s], fill=(30, 30, 30)); d.rectangle([x - 14 * s, y - 70 * s, x + 6 * s, y - 62 * s], fill=(200, 200, 200))
    for mx in (-110, 110): d.line([(x + mx * s, y - 6 * s), (x + mx * s, y - 96 * s)], fill=(70, 56, 40), width=max(2, int(3 * s)))
    for k in range(6): d.ellipse([x - 20 * s - k * 22 * s, y - 104 * s - k * 8 * s, x + 6 * s - k * 18 * s, y - 84 * s - k * 8 * s], fill=(110 + k * 14, 110 + k * 14, 116 + k * 14))
    if name: d.text((x + 100 * s, y + 18 * s), name, font=F(int(11 * s) + 4), fill=(236, 230, 210), anchor='mm')

def jangpan(b, x0, y0, x1, y1, col=(214, 170, 96)):
    """장판 (기름 먹인 종이 바닥)"""
    d = ImageDraw.Draw(b)
    d.rectangle([x0, y0, x1, y1], fill=col)
    for y in range(int(y0), int(y1), 48):
        for x in range(int(x0) + ((y // 48) % 2) * 32, int(x1), 64):
            d.rectangle([x, y, x + 63, y + 47], outline=sh(col, 0.9))
            d.line([(x + 4, y + 3), (x + 30, y + 3)], fill=sh(col, 1.08))

def goods(d, x, y, kind):
    """가게 앞 물건"""
    if kind == 'rice':
        for k in range(3): d.rounded_rectangle([x + k * 16, y - 18, x + k * 16 + 15, y], 5, fill=(214, 190, 130), outline=(160, 130, 80))
        d.rounded_rectangle([x + 8, y - 32, x + 23, y - 16], 5, fill=(214, 190, 130), outline=(160, 130, 80))
    elif kind == 'cloth':
        for k in range(4): d.rectangle([x + k * 12, y - 26 + (k % 2) * 4, x + k * 12 + 10, y], fill=[(240, 236, 226), (200, 70, 60), (60, 90, 150), (226, 214, 180)][k], outline=(120, 110, 90))
    elif kind == 'pot':
        for k in range(3): d.ellipse([x + k * 15, y - 20, x + k * 15 + 14, y], fill=(110, 70, 44)); d.ellipse([x + k * 15 + 3, y - 22, x + k * 15 + 11, y - 17], fill=(80, 50, 32))
    elif kind == 'fish':
        d.rectangle([x, y - 10, x + 48, y], fill=(150, 110, 70))
        for k in range(5): d.ellipse([x + 2 + k * 9, y - 16, x + 10 + k * 9, y - 10], fill=(170, 180, 186))
    elif kind == 'paper':
        for k in range(5): d.rectangle([x + k * 3, y - 20 - k * 2, x + 34 + k * 3, y - 16 - k * 2], fill=(246, 242, 228), outline=(200, 190, 170))
    elif kind == 'kerosene':
        for k in range(3): d.rectangle([x + k * 15, y - 22, x + k * 15 + 12, y], fill=(170, 60, 50)); d.rectangle([x + k * 15 + 3, y - 26, x + k * 15 + 8, y - 22], fill=(150, 150, 156))
    elif kind == 'matches':
        for k in range(3):
            for j in range(2): d.rectangle([x + k * 14, y - 10 - j * 10, x + k * 14 + 12, y - j * 10], fill=(230, 200, 120), outline=(150, 110, 60))
    elif kind == 'calico':      # 옥양목 (하얀 면직물 두루마리)
        for k in range(4): d.rounded_rectangle([x + k * 4, y - 12 - k * 7, x + 46 + k * 4, y - k * 7], 3, fill=(250, 250, 246), outline=(180, 180, 176))

def shop_row(b, x0, x1, y_base, signs, era='1867'):
    """시전 행랑: 기와 가게들이 길게 이어진 정면 + 간판 + 물건"""
    d = ImageDraw.Draw(b)
    n = len(signs); w = (x1 - x0) / n
    for k, (sg, kind) in enumerate(signs):
        a = x0 + k * w + 4; c = x0 + (k + 1) * w - 4
        hall(b, a, c, y_base, wall_h=54, roof_h=34, doors='shop', wall=(230, 222, 200))
        d = ImageDraw.Draw(b)
        if sg:
            jp = sg.startswith('日')
            f = F(13, 'serif'); tw = d.textlength(sg, font=f)
            sx = (a + c) / 2; sy = y_base - 70
            bc = (240, 236, 226) if jp else (40, 34, 30)
            d.rectangle([sx - tw / 2 - 6, sy - 10, sx + tw / 2 + 6, sy + 10], fill=bc, outline=(160, 130, 80))
            d.text((sx, sy), sg, font=f, fill=(30, 30, 40) if jp else (240, 220, 160), anchor='mm')
            if jp:      # 노렌 (가게 앞 천)
                for j in range(4): d.rectangle([a + 6 + j * (c - a - 12) / 4, y_base - 58, a + 4 + (j + 1) * (c - a - 12) / 4, y_base - 36], fill=(50, 60, 100))
        if kind: goods(d, int(a + 8), y_base - 12, kind)

def straw_mat(d, x0, y0, x1, y1):
    d.rectangle([x0, y0, x1, y1], fill=(206, 184, 130))
    for x in range(int(x0), int(x1), 4): d.line([(x, y0), (x, y1)], fill=(186, 160, 106))

# ==================================================================== 2편 공통 그림
BRICK = (168, 80, 60); TRIM = (238, 230, 212); SLATE = (66, 70, 80)
def brick_bldg(b, x0, x1, y_base, floors=2, col=BRICK, trim=TRIM, roof=SLATE, sign=None, sign_c=(30, 40, 60), veranda=False, flag=None, arch=True):
    """서양식 벽돌 건물 정면 (층마다 아치 창 · 처마 장식 · 슬레이트 지붕)"""
    d = ImageDraw.Draw(b)
    fh = 54; top = y_base - fh * floors
    d.rectangle([x0, top, x1, y_base], fill=col)
    rnd = random.Random(x0 + y_base)
    for y in range(int(top) + 4, int(y_base), 6):
        off = 0 if (y // 6) % 2 else 6
        for x in range(int(x0) + off, int(x1), 12): d.line([(x, y), (x, y + 5)], fill=sh(col, 0.86))
        d.line([(x0, y), (x1, y)], fill=sh(col, 0.9))
    for f in range(floors):
        yb = y_base - f * fh
        d.rectangle([x0 - 3, yb - fh - 2, x1 + 3, yb - fh + 3], fill=trim)
        n = max(2, int((x1 - x0) / 34))
        for k in range(n):
            wx = x0 + (x1 - x0) * (k + 0.5) / n
            w2, h2 = 9, 20
            d.rectangle([wx - w2 - 3, yb - fh + 13, wx + w2 + 3, yb - 8], fill=trim)
            if arch: d.chord([wx - w2 - 3, yb - fh + 7, wx + w2 + 3, yb - fh + 25], 180, 360, fill=trim)
            d.rectangle([wx - w2, yb - fh + 16, wx + w2, yb - 10], fill=(60, 76, 96))
            if arch: d.chord([wx - w2, yb - fh + 10, wx + w2, yb - fh + 22], 180, 360, fill=(60, 76, 96))
            d.line([(wx, yb - fh + 12), (wx, yb - 10)], fill=trim); d.line([(wx - w2, yb - 26), (wx + w2, yb - 26)], fill=trim)
    d.rectangle([x0 - 6, top - 6, x1 + 6, top], fill=trim)
    d.polygon([(x0 - 4, top - 6), (x1 + 4, top - 6), (x1 - 18, top - 34), (x0 + 18, top - 34)], fill=roof)
    for x in range(int(x0) + 10, int(x1) - 10, 10): d.line([(x, top - 8), (x + (x - (x0 + x1) / 2) * -0.1, top - 32)], fill=sh(roof, 1.15))
    if veranda:
        for k in range(int((x1 - x0) / 30) + 1):
            cx = x0 + k * 30; d.rectangle([cx - 3, y_base - fh + 4, cx + 3, y_base], fill=trim)
        d.rectangle([x0 - 4, y_base - fh - 2, x1 + 4, y_base - fh + 6], fill=trim)
        for x in range(int(x0), int(x1), 8): d.line([(x, y_base - fh - 12), (x, y_base - fh - 2)], fill=trim)
        d.line([(x0, y_base - fh - 12), (x1, y_base - fh - 12)], fill=trim, width=2)
    if sign:
        f = F(13, 'serif'); tw = d.textlength(sign, font=f); sx = (x0 + x1) / 2
        d.rectangle([sx - tw / 2 - 8, top + 6, sx + tw / 2 + 8, top + 24], fill=sign_c, outline=trim)
        d.text((sx, top + 15), sign, font=f, fill=(250, 240, 210), anchor='mm')
    if flag:
        fx = x1 - 20
        d.line([(fx, top - 34), (fx, top - 84)], fill=(80, 80, 80), width=2)
        flag(d, fx + 1, top - 84)

def us_flag(d, x, y):
    for k in range(7): d.rectangle([x, y + k * 3, x + 30, y + k * 3 + 1], fill=(200, 40, 40) if k % 2 == 0 else (250, 250, 250))
    d.rectangle([x, y, x + 12, y + 10], fill=(40, 50, 120))
def uk_flag(d, x, y):
    d.rectangle([x, y, x + 30, y + 18], fill=(40, 50, 120))
    d.line([(x, y), (x + 30, y + 18)], fill=(250, 250, 250), width=3); d.line([(x, y + 18), (x + 30, y)], fill=(250, 250, 250), width=3)
    d.rectangle([x + 12, y, x + 18, y + 18], fill=(250, 250, 250)); d.rectangle([x, y + 7, x + 30, y + 11], fill=(250, 250, 250))
    d.rectangle([x + 13, y, x + 17, y + 18], fill=(200, 40, 40)); d.rectangle([x, y + 8, x + 30, y + 10], fill=(200, 40, 40))
def ru_flag(d, x, y):
    for k, c in enumerate(((250, 250, 250), (40, 70, 160), (200, 40, 40))): d.rectangle([x, y + k * 6, x + 30, y + k * 6 + 5], fill=c)
def kr_flag(d, x, y):
    d.rectangle([x, y, x + 30, y + 20], fill=(250, 250, 248))
    d.pieslice([x + 9, y + 4, x + 21, y + 16], 180, 360, fill=(200, 40, 50)); d.pieslice([x + 9, y + 4, x + 21, y + 16], 0, 180, fill=(40, 70, 160))
    for (ax, ay) in ((x + 3, y + 3), (x + 24, y + 3), (x + 3, y + 14), (x + 24, y + 14)):
        for j in range(3): d.line([(ax, ay + j * 1.4), (ax + 3, ay + j * 1.4)], fill=(30, 30, 30))

def gas_lamp(d, x, yb, lit=True):
    d.rectangle([x - 2, yb - 86, x + 2, yb], fill=(40, 46, 50)); d.rectangle([x - 6, yb - 4, x + 6, yb], fill=(40, 46, 50)); d.line([(x - 9, yb - 80), (x + 9, yb - 80)], fill=(40, 46, 50), width=2)
    d.polygon([(x - 7, yb - 104), (x + 7, yb - 104), (x + 10, yb - 86), (x - 10, yb - 86)], fill=(252, 238, 170) if lit else (200, 200, 190), outline=(40, 46, 50))
    d.polygon([(x - 9, yb - 104), (x + 9, yb - 104), (x, yb - 112)], fill=(40, 46, 50))

def horse_tram(b, x, y):
    """철도 마차 (1882 도쿄) : 말 + 2층 없는 객차 + 레일"""
    d = ImageDraw.Draw(b)
    d.rectangle([x - 70, y - 54, x + 60, y - 12], fill=(60, 110, 80)); d.rectangle([x - 74, y - 60, x + 64, y - 52], fill=(200, 180, 120))
    for k in range(5): d.rectangle([x - 62 + k * 24, y - 48, x - 46 + k * 24, y - 30], fill=(220, 230, 236))
    d.rectangle([x - 70, y - 24, x + 60, y - 20], fill=(200, 180, 120))
    for wx in (x - 50, x + 40): d.ellipse([wx - 10, y - 18, wx + 10, y + 2], fill=(40, 40, 44)); d.ellipse([wx - 4, y - 12, wx + 4, y - 4], fill=(150, 150, 150))
    hx = x + 84
    d.ellipse([hx - 16, y - 40, hx + 22, y - 18], fill=(120, 80, 50)); d.polygon([(hx + 18, y - 38), (hx + 30, y - 52), (hx + 36, y - 46), (hx + 24, y - 30)], fill=(120, 80, 50))
    for lx in (hx - 12, hx - 4, hx + 10, hx + 18): d.line([(lx, y - 22), (lx, y)], fill=(100, 66, 40), width=3)
    d.line([(x + 60, y - 30), (hx - 14, y - 30)], fill=(60, 40, 30), width=2)

def lanterns(d, x0, x1, y, n=5):
    for k in range(n):
        x = x0 + (x1 - x0) * (k + 0.5) / n
        d.line([(x, y - 14), (x, y - 6)], fill=(60, 50, 40))
        d.rounded_rectangle([x - 7, y - 6, x + 7, y + 12], 4, fill=(220, 60, 50)); d.rectangle([x - 7, y - 1, x + 7, y + 6], fill=(60, 80, 160))
        d.line([(x, y + 12), (x, y + 18)], fill=(220, 60, 50))

def hanok_wall(d, x0, x1, y_top, h=40, col=(206, 196, 176)):
    """돌담 + 기와 담장"""
    d.rectangle([x0, y_top, x1, y_top + h], fill=col)
    rnd = random.Random(x0 * 3 + y_top)
    for _ in range(int((x1 - x0) * h / 120)):
        x, y = rnd.randint(int(x0), int(x1) - 8), rnd.randint(int(y_top) + 8, int(y_top + h) - 6)
        d.ellipse([x, y, x + rnd.randint(8, 16), y + rnd.randint(5, 9)], fill=sh(col, rnd.choice([0.86, 0.92, 1.06])))
    giwa_roof(d, x0 - 6, x1 + 6, y_top - 12, y_top + 2, GIWA, flare=0, ridge=False)

# ==================================================================== 01 윤재의 서재 (1893 밤)
def seojae(root):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(3, 12):
        for x in range(8, 21): g[y][x] = 'o'
    g[12][14] = 'o'
    g[3][19] = 'x'; g[3][20] = 'x'                     # 책장
    g[4][9] = 'x'                                     # 편지함
    g[5][14] = 'x'                                    # 책상
    g[3][12] = 'x'; g[3][11] = 'x'                     # 문갑 + 우표첩
    g[5][18] = 'x'                                    # 신문 더미
    g[5][16] = 'x'                                    # 남포등
    g[9][11] = 'x'                                    # 화로
    m = Map('seojae', 1, [''.join(r) for r in g], 'seoul', 1893)
    b = m.big; d = ImageDraw.Draw(b)
    dark_out(b, 0, 8, col=(26, 22, 20)); dark_out(b, 21, 29, col=(26, 22, 20))
    jangpan(b, 8 * TS, 3 * TS, 21 * TS - 1, 12 * TS - 1)
    d.rectangle([14 * TS, 12 * TS, 15 * TS - 1, 13 * TS - 1], fill=(120, 90, 60))
    d.rectangle([8 * TS, 0, 21 * TS - 1, 3 * TS - 1], fill=(232, 224, 204))
    for x in (8 * TS, 12 * TS + 20, 17 * TS + 30, 21 * TS - 8): d.rectangle([x, 0, x + 8, 3 * TS], fill=WOOD)
    d.rectangle([8 * TS, 3 * TS - 10, 21 * TS - 1, 3 * TS - 1], fill=WOOD_D)
    d.rectangle([8 * TS, 0, 21 * TS - 1, 12], fill=WOOD_D)
    # 왼쪽 벽: 태극기 족자 + 지도
    d.rectangle([8 * TS + 20, 22, 10 * TS + 30, 3 * TS - 22], fill=(236, 228, 206), outline=(140, 110, 70), width=2)
    granite = ImageDraw.Draw(b)
    kr_flag(d, 9 * TS + 2, 40)
    d.text((9 * TS + 18, 3 * TS - 40), '大朝鮮國', font=F(12, 'serif'), fill=(60, 40, 30), anchor='mm')
    # 가운데 족자 (글씨)
    d.rectangle([13 * TS + 6, 18, 15 * TS + 40, 3 * TS - 20], fill=(244, 238, 222), outline=(140, 110, 70), width=2)
    d.text((14 * TS + 24, 72), '不增不減', font=F(20, 'serif'), fill=(40, 30, 26), anchor='mm')
    d.text((14 * TS + 24, 100), '(보태지도 빼지도 말라)', font=F(10), fill=(110, 90, 70), anchor='mm')
    # 벽시계 (16칸)
    cx, cy = 16 * TS + 24, 2 * TS + 4
    d.rounded_rectangle([cx - 18, cy - 44, cx + 18, cy + 34], 6, fill=(110, 70, 40), outline=(70, 44, 26), width=2)
    d.ellipse([cx - 14, cy - 40, cx + 14, cy - 12], fill=(246, 240, 224), outline=(70, 44, 26))
    for k in range(12):
        a = k / 12 * 2 * math.pi; d.point((cx + 11 * math.sin(a), cy - 26 - 11 * math.cos(a)), fill=(40, 30, 26))
    d.line([(cx, cy - 26), (cx, cy - 37)], fill=(30, 26, 22), width=2); d.line([(cx, cy - 26), (cx - 2, cy - 33)], fill=(30, 26, 22), width=2)
    d.line([(cx, cy - 10), (cx, cy + 20)], fill=(206, 170, 90)); d.ellipse([cx - 5, cy + 18, cx + 5, cy + 28], fill=(206, 170, 90))
    # 창 (오른쪽 · 달빛)
    wx = 18 * TS + 10
    d.rectangle([wx, 20, wx + 130, 3 * TS - 18], fill=(60, 76, 116))
    d.ellipse([wx + 86, 30, wx + 114, 58], fill=(250, 240, 200))
    d.rectangle([wx, 20, wx + 130, 3 * TS - 18], outline=WOOD_D, width=4)
    for x in range(wx + 13, wx + 130, 13): d.line([(x, 20), (x, 3 * TS - 18)], fill=(220, 210, 180))
    for y in range(33, 3 * TS - 18, 13): d.line([(wx, y), (wx + 130, y)], fill=(220, 210, 180))
    d.rectangle([8 * TS - 10, 0, 8 * TS, 12 * TS], fill=WOOD_D); d.rectangle([21 * TS, 0, 21 * TS + 10, 12 * TS], fill=WOOD_D)
    # 보료 · 방석 · 문지방
    d.rounded_rectangle([12 * TS + 4, 6 * TS + 6, 17 * TS - 4, 6 * TS + 40], 6, fill=(150, 60, 60), outline=(110, 40, 40))
    for x in (13 * TS, 15 * TS): d.rounded_rectangle([x + 8, 7 * TS + 8, x + 40, 7 * TS + 36], 8, fill=(80, 100, 150))
    d.rectangle([8 * TS, 12 * TS - 6, 21 * TS - 1, 12 * TS + 2], fill=WOOD)
    # 문갑 (낮은 장) 왼쪽 칸
    with Prop(b, 11 * TS, 3 * TS - 4, TS, 44) as dd:
        dd.rectangle([2, 8, TS - 2, 40], fill=(120, 80, 48)); dd.rectangle([2, 4, TS - 2, 10], fill=(150, 104, 64))
        for k in range(2): dd.rectangle([6 + k * 20, 14, 22 + k * 20, 34], outline=(206, 170, 90)); dd.ellipse([12 + k * 20, 22, 16 + k * 20, 26], fill=(206, 170, 90))
    glow(b, 16 * TS + 24, 5 * TS + 14, 130, (255, 220, 150), 60)
    glow(b, 11 * TS + 24, 9 * TS + 24, 70, (255, 140, 60), 50)
    m.ev('door', 14, 12, trigger=1)
    m.ev('desk', 14, 5, '!$k_desk_w')
    m.ev('letterbox', 9, 4, '!$k_letterbox')
    m.ev('stamps', 12, 3, '!$k_stampbook')
    m.ev('bookcase', 19, 3, '!$k_bookcase')
    m.ev('lamp', 16, 5, '!$k_lamp_oil', anime=True)
    m.ev('papers', 18, 5, '!$k_papers')
    m.ev('hwaro', 11, 9, '!$k_hwaro', anime=True)
    m.ev('father', 10, 8, '$k_father93', dir='right')
    m.ev('yunhee', 18, 8, '$k_yunhee35', dir='left')
    m.ev('wallclock', 16, 2)
    m.ev('window', 19, 2)
    G.finish(b, m.grid, vignette=0.2, ao=0.25, warm=0.1)
    d = ImageDraw.Draw(b)
    d.rectangle([0, 0, 8 * TS - 11, b.height], fill=(26, 22, 20)); d.rectangle([21 * TS + 11, 0, b.width, b.height], fill=(26, 22, 20))
    d.rectangle([0, 12 * TS, 14 * TS - 1, b.height], fill=(26, 22, 20)); d.rectangle([15 * TS, 12 * TS, b.width, b.height], fill=(26, 22, 20))
    note_label(b, '윤재의 서재 · 1893년 섣달 그믐')
    m.save(root, parallax_name='!k_seojae', finish=False)

# ==================================================================== 02 도쿄 긴자 (1882)
def ginza(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for x in (17, 18, 19): g[6][x] = 'x'                       # 철도 마차
    g[10][21] = 'x'                                           # 인력거
    m = Map('ginza', 2, [''.join(r) for r in g], 'seoul', 1882)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (176, 196, 214), (226, 226, 220))
    # 벽돌 거리 (2층 · 베란다)
    signs = ['洋服', '時計', '新聞社', '銀座 煉瓦街', '書肆', '洋品']
    xs = [0, 4 * TS, 8 * TS, 12 * TS, 17 * TS, 21 * TS, 25 * TS, 29 * TS]
    for k in range(7):
        x0, x1 = xs[k] + 6, xs[k + 1] - 6
        brick_bldg(b, x0, x1, 4 * TS - 2, 2, col=[(168, 80, 60), (186, 96, 70), (160, 74, 56)][k % 3], veranda=True, sign=signs[k % len(signs)] if k not in (0, 6) else None)
    d = ImageDraw.Draw(b)
    # 보도 (벽돌) · 차도 · 레일
    d.rectangle([0, 4 * TS - 2, b.width, 4 * TS + 30], fill=(170, 110, 90))
    for x in range(0, b.width, 16): d.line([(x, 4 * TS - 2), (x, 4 * TS + 30)], fill=(150, 96, 78))
    d.line([(0, 4 * TS + 30), (b.width, 4 * TS + 30)], fill=(120, 110, 100), width=3)
    for y in (6 * TS + 40, 6 * TS + 46): d.line([(0, y), (b.width, y)], fill=(90, 90, 96), width=3)
    for x in range(0, b.width, 22): d.rectangle([x, 6 * TS + 37, x + 8, 6 * TS + 50], fill=(110, 90, 70))
    d.line([(0, 6 * TS + 40), (b.width, 6 * TS + 40)], fill=(150, 150, 156), width=2); d.line([(0, 6 * TS + 46), (b.width, 6 * TS + 46)], fill=(150, 150, 156), width=2)
    horse_tram(b, 18 * TS + 4, 6 * TS + 44)
    d = ImageDraw.Draw(b)
    for gx in (2, 6, 20, 24, 27): gas_lamp(d, gx * TS + 24, 4 * TS + 26)
    # 전신줄
    for x in (1, 13, 26): d.rectangle([x * TS + 22, 0, x * TS + 26, 4 * TS + 26], fill=(110, 80, 54)); d.rectangle([x * TS + 12, 8, x * TS + 36, 11], fill=(110, 80, 54))
    d.line([(0, 9), (b.width, 12)], fill=(30, 30, 34)); d.line([(0, 14), (b.width, 17)], fill=(30, 30, 34))
    # 인력거 (21,10)
    with Prop(b, 21 * TS - 10, 10 * TS - 6, 70, 54) as dd:
        dd.ellipse([22, 18, 58, 54], outline=(40, 30, 26), width=3); dd.line([(40, 36), (40, 18)], fill=(40, 30, 26))
        dd.rectangle([18, 10, 50, 30], fill=(40, 40, 50)); dd.chord([16, 0, 52, 24], 180, 360, fill=(30, 30, 40)); dd.line([(18, 30), (0, 42)], fill=(110, 80, 50), width=3)
    for tx in (1, 3, 25, 27): G.tree(b, tx, 9, 'willow', 0.9)
    exit_path(b, 14, 14, 11 * TS + 30, '숙소로')
    note_label(b, '도쿄 긴자 거리 · 1882년 11월')
    m.ev('exit', 14, 12, trigger=1)
    m.ev('gaslamp', 9, 5, '!$k_gaslamp')
    m.ev('brick', 11, 4)
    m.ev('tram', 18, 6)
    m.ev('postbox', 15, 5, '!$k_postbox_jp')
    m.ev('newsboy', 11, 8, '$k_newsboy', dir='right')
    m.ev('kimokgyun', 16, 9, '$k_kimokgyun', dir='down')
    m.ev('minyoungik', 17, 9, '$k_minyoungik', dir='left')
    m.ev('parkyounghyo', 13, 7, '$k_parkyounghyo', dir='down')
    m.ev('seogwangbeom', 10, 6, '$k_seogwangbeom', dir='right')
    m.ev('fukuzawa', 20, 8, '$k_fukuzawa', dir='left')
    m.ev('rickshaw', 20, 10, '$k_rickshaw', dir='left')
    m.ev('jp_police', 8, 10, '$k_jp_police', dir='right')
    g2 = m.grid; g2[5][9] = 'x'; g2[5][15] = 'x'; g2[4][11] = 'x'
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.04)
    m.save(root, parallax_name='!k_ginza', finish=False)

# ==================================================================== 03 박문국 (1883 · 불탄 뒤)
def bakmun(root):
    g = [list('B' * 29) for _ in range(13)]
    for y in range(4, 12):
        for x in range(8, 21): g[y][x] = 'H'
    g[12][14] = 'H'
    for (x, y) in ((10, 4), (11, 4), (12, 4), (16, 4), (19, 4), (14, 6), (17, 5)): g[y][x] = 'x'
    m = Map('bakmun', 3, [''.join(r) for r in g], 'seoul', 1883)
    base = m.big.copy()
    def draw(b, burnt):
        d = ImageDraw.Draw(b)
        dark_out(b, 0, 8, col=(30, 26, 24)); dark_out(b, 21, 29, col=(30, 26, 24))
        wall = (226, 218, 200) if not burnt else (90, 80, 72)
        d.rectangle([8 * TS, 0, 21 * TS - 1, 4 * TS - 1], fill=wall)
        for x in (8 * TS, 11 * TS + 24, 15 * TS + 24, 21 * TS - 8): d.rectangle([x, 0, x + 8, 4 * TS], fill=WOOD if not burnt else (50, 40, 34))
        d.rectangle([8 * TS, 4 * TS - 10, 21 * TS - 1, 4 * TS - 1], fill=WOOD_D)
        # 창 (유리창 · 1883 새 관청)
        for wx in (9 * TS + 10, 13 * TS, 17 * TS + 10):
            d.rectangle([wx, 26, wx + 90, 2 * TS + 20], fill=(150, 176, 196) if not burnt else (30, 26, 24), outline=WOOD_D, width=3)
            d.line([(wx + 45, 26), (wx + 45, 2 * TS + 20)], fill=WOOD_D, width=2); d.line([(wx, 26 + 40), (wx + 90, 26 + 40)], fill=WOOD_D, width=2)
        # 현판
        d.rectangle([12 * TS + 30, 3 * TS - 4, 16 * TS + 18, 3 * TS + 24], fill=(40, 34, 30), outline=(200, 170, 100))
        d.text((14 * TS + 24, 3 * TS + 10), '博文局', font=F(17, 'serif'), fill=(240, 220, 160) if not burnt else (150, 130, 100), anchor='mm')
        # 종이 선반 (오른쪽 벽)
        for y in (2 * TS + 34, 3 * TS + 14):
            d.rectangle([18 * TS + 40, y, 20 * TS + 40, y + 6], fill=WOOD_D)
            for k in range(6): d.rectangle([18 * TS + 44 + k * 15, y - 16, 18 * TS + 56 + k * 15, y], fill=(240, 236, 220) if not burnt else (60, 54, 48))
        d.rectangle([8 * TS - 10, 0, 8 * TS, 12 * TS], fill=WOOD_D); d.rectangle([21 * TS, 0, 21 * TS + 10, 12 * TS], fill=WOOD_D)
        d.rectangle([8 * TS, 12 * TS - 6, 21 * TS - 1, 12 * TS + 2], fill=WOOD)
        # 인쇄기 (10~12, 4)
        with Prop(b, 10 * TS, 4 * TS - 30, 3 * TS, 76) as dd:
            if not burnt:
                dd.rectangle([14, 44, 130, 70], fill=(50, 52, 58)); dd.rectangle([18, 70, 26, 75], fill=(40, 40, 44)); dd.rectangle([118, 70, 126, 75], fill=(40, 40, 44))
                dd.rectangle([26, 34, 118, 44], fill=(230, 226, 214)); dd.rectangle([46, 8, 100, 34], fill=(70, 72, 80)); dd.rectangle([66, 0, 78, 10], fill=(60, 60, 66))
                dd.line([(100, 18), (136, 4)], fill=(80, 80, 86), width=4); dd.ellipse([2, 40, 22, 60], outline=(80, 80, 86), width=3)
            else:
                dd.polygon([(14, 50), (130, 46), (126, 72), (18, 74)], fill=(34, 32, 32)); dd.polygon([(46, 20), (100, 14), (96, 46), (52, 46)], fill=(40, 38, 40))
                dd.line([(100, 30), (126, 50)], fill=(50, 48, 50), width=4)
        # 활자 상자 (16,4) · 교정지 (19,4) · 조판대 (17,5) · 탁자 (14,6)
        with Prop(b, 16 * TS, 4 * TS - 8, TS, 56) as dd:
            if not burnt:
                dd.rectangle([4, 4, 44, 54], fill=(110, 76, 46))
                for y in range(7, 52, 7):
                    for x in range(7, 42, 8): dd.rectangle([x, y, x + 6, y + 5], fill=(60, 54, 50)); dd.point((x + 2, y + 2), fill=(180, 180, 180))
            else:
                dd.rectangle([4, 20, 44, 54], fill=(46, 36, 30)); dd.polygon([(4, 20), (16, 8), (30, 16), (44, 10), (44, 20)], fill=(36, 28, 24))
                for k in range(12): dd.point((8 + k * 3, 44 + (k % 3) * 3), fill=(200, 200, 196))
        with Prop(b, 19 * TS, 4 * TS - 10, TS, 56) as dd:
            dd.line([(2, 8), (46, 10)], fill=(120, 90, 60), width=2)
            for k in range(3):
                if burnt and k == 1: continue
                dd.rectangle([5 + k * 14, 10, 16 + k * 14, 34], fill=(244, 240, 228) if not burnt else (110, 96, 80), outline=(170, 160, 140))
        with Prop(b, 17 * TS, 5 * TS - 4, TS, 52) as dd:
            dd.polygon([(4, 30), (44, 22), (44, 30), (4, 38)], fill=(130, 92, 58) if not burnt else (50, 40, 34)); dd.rectangle([6, 38, 9, 50], fill=WOOD_D); dd.rectangle([39, 30, 42, 50], fill=WOOD_D)
            dd.polygon([(12, 26), (36, 21), (36, 27), (12, 32)], fill=(70, 70, 76))
        with Prop(b, 14 * TS - 6, 6 * TS - 2, TS + 12, 52) as dd:
            dd.rectangle([2, 22, 58, 30], fill=(140, 96, 60) if not burnt else (54, 44, 36)); dd.rectangle([4, 30, 8, 50], fill=WOOD_D); dd.rectangle([52, 30, 56, 50], fill=WOOD_D)
            if not burnt:
                for (x, y) in ((8, 14), (22, 12), (36, 15)): dd.rectangle([x, y, x + 12, y + 8], fill=(244, 240, 228), outline=(170, 160, 140))
        if burnt:
            rnd = random.Random(84)
            soot = Image.new('L', b.size, 0); sd = ImageDraw.Draw(soot)
            for _ in range(16):
                x, y = rnd.randint(8 * TS, 21 * TS), rnd.randint(4 * TS, 11 * TS)
                sd.ellipse([x, y, x + rnd.randint(40, 90), y + rnd.randint(16, 34)], fill=150)
            soot = soot.filter(ImageFilter.GaussianBlur(10)); b.paste((30, 26, 24), (0, 0), soot); d = ImageDraw.Draw(b)
            d.polygon([(9 * TS, 0), (11 * TS, 0), (10 * TS + 20, 60)], fill=(20, 18, 18)); d.polygon([(18 * TS, 0), (20 * TS, 0), (19 * TS, 80)], fill=(20, 18, 18))
        G.finish(b, m.grid, vignette=0.2 if not burnt else 0.32, ao=0.25, warm=0.08)
        d = ImageDraw.Draw(b)
        d.rectangle([0, 0, 8 * TS - 11, b.height], fill=(30, 26, 24)); d.rectangle([21 * TS + 11, 0, b.width, b.height], fill=(30, 26, 24))
        d.rectangle([0, 12 * TS, 14 * TS - 1, b.height], fill=(30, 26, 24)); d.rectangle([15 * TS, 12 * TS, b.width, b.height], fill=(30, 26, 24))
        note_label(b, '박문국 · 1883년' if not burnt else '불탄 박문국 · 1884년 12월')
    for burnt, nm in ((False, '!k_bakmun'), (True, '!k_bakmun_burnt')):
        bb = base.copy(); draw(bb, burnt); save_variant(root, nm, bb)
        if not burnt: m.big = bb
    m.ev('exit', 14, 12, trigger=1)
    m.ev('press', 11, 4)
    m.ev('typecase', 16, 4)
    m.ev('proofs', 19, 4)
    m.ev('composing', 17, 5)
    m.ev('memo', 14, 6)
    m.ev('kimokgyun', 10, 7, '$k_kimokgyun', dir='right')
    m.ev('parkyounghyo', 9, 9, '$k_parkyounghyo', dir='right')
    m.ev('hongyoungsik', 11, 9, '$k_hongyoungsik', dir='up')
    m.ev('kimyunsik', 18, 8, '$k_kimyunsik', dir='left')
    m.ev('eoyunjung', 19, 10, '$k_eoyunjung', dir='left')
    m.ev('dolsoe', 16, 6, '$k_dolsoe', dir='left')
    m.ev('inoue', 12, 6, '$k_inoue', dir='right')
    m.save(root, parallax_name='!k_bakmun', finish=False, image=False)

# ==================================================================== 04 운종가 (1884)
def market(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    m = Map('market', 4, [''.join(r) for r in g], 'seoul', 1884)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 3 * TS)
    granite_mts(b, 2 * TS + 10, seed=11, height=100, peaks=((0.4, 1.0), (0.75, 0.7)))
    d = ImageDraw.Draw(b)
    signs = [('米廛', 'rice'), ('華商 綢緞', 'cloth'), ('洋布 · 玉洋木', 'calico'), ('紙廛', 'paper'), ('日本商會', 'matches'), ('石油', 'kerosene')]
    shop_row(b, 6 * TS - 20, 19 * TS, 4 * TS - 4, signs, '1884')
    hall(b, 19 * TS + 10, 22 * TS + 30, 4 * TS - 4, wall_h=70, roof_h=40, doors='wall', dan=True, wall=(170, 60, 50), sign='普信閣')
    d = ImageDraw.Draw(b)
    for tx in (0, 25):
        d.rectangle([tx * TS, 2 * TS, (tx + 4) * TS, 4 * TS], fill=(214, 196, 160))
        giwa_roof(d, tx * TS + 10, (tx + 4) * TS - 10, 2 * TS - 30, 2 * TS + 6)
    # 청 상점 등롱 · 전신주 (1884)
    for x in (8 * TS + 30, 9 * TS + 20):
        d.line([(x, 3 * TS + 10), (x, 3 * TS + 18)], fill=(60, 50, 40)); d.ellipse([x - 8, 3 * TS + 18, x + 8, 3 * TS + 36], fill=(220, 50, 40)); d.rectangle([x - 6, 3 * TS + 22, x + 6, 3 * TS + 24], fill=(240, 200, 80))
    d.line([(6 * TS, 4 * TS + 6), (23 * TS, 4 * TS + 6)], fill=(110, 100, 90), width=2)
    for (tx, ty, kind) in ((22, 7, 'fish'), (22, 10, 'pot'), (6, 6, 'rice')):
        straw_mat(d, tx * TS - 30, ty * TS + 14, tx * TS + 40, ty * TS + 44); goods(d, tx * TS - 22, ty * TS + 38, kind)
    straw_mat(d, 10 * TS - 20, 6 * TS + 18, 11 * TS - 6, 6 * TS + 46); goods(d, 10 * TS - 14, 6 * TS + 42, 'cloth')     # 윤희네 포목 좌판
    note_label(b, '운종가 장터 · 1884년')
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.06)
    exit_path(b, 14, 14, 11 * TS + 30, '큰길')
    m.ev('exit', 14, 12, trigger=1)
    m.ev('yunhee', 11, 6, '$k_yunhee23', dir='down')
    m.ev('qmerchant', 8, 5, '$k_qing_merchant', dir='down')
    m.ev('peddler', 10, 8, '$k_peddler', dir='right')
    m.ev('market_w', 19, 9, '$k_market_w', dir='left')
    m.ev('commoner', 16, 7, '$k_commoner', dir='left')
    m.ev('poor_m', 13, 8, '$k_poor_m', dir='down')
    m.ev('yuan', 7, 7, '$k_yuan', dir='right')
    m.ev('qing1', 7, 10, '$k_qing_soldier', dir='right')
    m.ev('qing2', 21, 10, '$k_qing_soldier', dir='left')
    m.ev('silk', 9, 4, '!$k_silk')
    m.ev('jpshop', 15, 4, '!$k_jpsign')
    m.ev('coinboard', 12, 4, '!$k_notice')
    m.ev('hyesang', 18, 4, '!$k_flag_hs', anime=True)
    m.ev('bell', 20, 2)
    m.save(root, parallax_name='!k_market84', finish=False)

# ==================================================================== 05 우정총국 (1884 가을 낮 · 12월 4일 밤)
def ujeong(root):
    g = grid_open('#', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for (x, y) in ((20, 5),): g[y][x] = 'x'          # 잔칫상 · 빈자리 · 액자 · 지도판은 장마다 보였다 숨으므로 칸을 막지 않음 (이벤트가 보일 때만 막힘)
    m = Map('ujeong', 5, [''.join(r) for r in g], 'seoul', 1884)
    base = m.big.copy()
    def draw(b, night):
        d = ImageDraw.Draw(b)
        skyk(b, 2 * TS, (190, 200, 210) if not night else (24, 28, 52), (230, 226, 214) if not night else (50, 50, 76))
        if night:
            rnd = random.Random(1884)
            for _ in range(40): d.point((rnd.randint(0, b.width), rnd.randint(0, 2 * TS)), fill=(220, 220, 240))
        granite_mts(b, 2 * TS, seed=5, height=70, col=(150, 150, 140) if not night else (70, 74, 90), peaks=((0.3, 1.0), (0.7, 0.6)))
        d = ImageDraw.Draw(b)
        # 담장 + 우정총국 (한옥 · 현판)
        hanok_wall(d, 0, b.width, 3 * TS - 10, 40)
        hall(b, 9 * TS, 20 * TS, 4 * TS - 4, wall_h=70, roof_h=44, doors='changho', dan=True, sign='郵征總局', sign_c=(40, 34, 30))
        d = ImageDraw.Draw(b)
        if not night:      # 고치는 중: 비계 · 목재
            for x in range(17 * TS, 20 * TS + 10, 24): d.line([(x, 4 * TS - 4), (x, 1 * TS - 10)], fill=(150, 110, 70), width=3)
            for y in range(1 * TS, 4 * TS - 10, 22): d.line([(17 * TS, y), (20 * TS + 10, y)], fill=(150, 110, 70), width=2)
            for k in range(4): d.rounded_rectangle([22 * TS - 10, 8 * TS + 26 - k * 8, 24 * TS, 8 * TS + 34 - k * 8], 3, fill=(170, 120, 74) if k % 2 else (150, 104, 62))
        else:              # 잔치: 청사초롱 · 밝은 창
            lanterns(d, 9 * TS, 20 * TS, 2 * TS + 28, 7)
            for x in range(9 * TS + 10, 20 * TS - 10, 66): glow(b, x + 20, 3 * TS + 20, 60, (255, 210, 130), 70)
            d = ImageDraw.Draw(b)
            d.rectangle([10 * TS, 6 * TS + 10, 19 * TS, 8 * TS + 30], fill=(140, 50, 46)); d.rectangle([10 * TS, 6 * TS + 10, 19 * TS, 8 * TS + 30], outline=(220, 180, 100), width=3)
        for tx in (2, 4, 24, 26): G.tree(b, tx, 7, 'pine' if tx in (2, 26) else 'autumn' if not night else 'pine', 1.0)
        note_label(b, '우정총국 · 1884년 가을' if not night else '우정총국 개국 축하연 · 1884년 12월 4일 밤')
        G.finish(b, m.grid, vignette=0.12 if not night else 0.26, ao=0.25, warm=0.06)
        exit_path(b, 14, 14, 11 * TS + 30, '큰길')
    for night, nm in ((False, '!k_ujeong_day'), (True, '!k_ujeong_night')):
        bb = base.copy(); draw(bb, night); save_variant(root, nm, bb)
        if not night: m.big = bb
    m.ev('exit', 14, 12, trigger=1)
    m.ev('hongyoungsik', 14, 5, '$k_hongyoungsik', dir='down')
    m.ev('postman', 9, 7, '$k_postman', dir='right')
    m.ev('carpenter', 19, 8, '$k_carpenter', dir='left')
    m.ev('frame', 11, 4, '!$k_frame')
    m.ev('postmap', 17, 4, '!$k_hmap')
    m.ev('mailbox', 20, 5, '!$k_postbox_k')
    m.ev('kimokgyun', 20, 9, '$k_kimokgyun', dir='left')
    m.ev('minyoungik', 10, 6, '$k_minyoungik', dir='down')
    m.ev('foote', 12, 6, '$k_foote', dir='down')
    m.ev('chenshutang', 16, 6, '$k_chenshutang', dir='down')
    m.ev('aston', 18, 6, '$k_aston', dir='down')
    m.ev('mollendorff', 10, 8, '$k_mollendorff', dir='up')
    m.ev('shimamura', 18, 8, '$k_shimamura', dir='up')
    m.ev('parkyounghyo', 8, 9, '$k_parkyounghyo', dir='right')
    m.ev('empty_seat', 14, 6, '!$k_emptyseat')
    m.ev('table1', 11, 7, '!$k_btable')
    m.ev('table2', 17, 7, '!$k_btable')
    m.ev('sign', 14, 2)
    m.save(root, parallax_name='!k_ujeong_day', finish=False, image=False)

# ==================================================================== 06 경우궁 (밤) · 창덕궁 (낮)
def palace(root):
    g = grid_open('P', 4)
    for x in range(7, 22): g[3][x] = 'B'
    # 명단 탁자 · 정강 초안 · 관물헌 지도는 장마다 보였다 숨으므로 칸을 막지 않음 (이벤트가 보일 때만 막힘)
    m = Map('palace', 6, [''.join(r) for r in g], 'seoul', 1884)
    base = m.big.copy()
    def draw(b, big):
        d = ImageDraw.Draw(b)
        if big: skyk(b, 2 * TS, (150, 186, 214), (226, 228, 222)); granite_mts(b, 2 * TS + 10, seed=31, height=110, peaks=((0.5, 1.0), (0.15, 0.6)))
        else: skyk(b, 2 * TS, (40, 44, 70), (70, 70, 96)); granite_mts(b, 2 * TS, seed=37, height=70, col=(90, 94, 110), peaks=((0.6, 1.0),))
        d = ImageDraw.Draw(b)
        if big:            # 창덕궁: 2층 지붕 · 단청 · 월대
            d.rectangle([0, 3 * TS - 6, b.width, 4 * TS], fill=(214, 150, 110)); giwa_roof(d, -10, b.width + 10, 3 * TS - 18, 3 * TS - 2, GIWA, flare=0, ridge=False)
            d.rectangle([9 * TS - 10, 3 * TS + 20, 20 * TS + 10, 4 * TS - 2], fill=STONE_K)
            for k in range(4): d.line([(9 * TS - 10, 3 * TS + 20 + k * 7), (20 * TS + 10, 3 * TS + 20 + k * 7)], fill=sh(STONE_K, 0.9))
            hall(b, 10 * TS, 19 * TS, 3 * TS + 20, wall_h=56, roof_h=34, doors='changho', dan=True, wall=(170, 60, 50), sign='熙政堂')
            d = ImageDraw.Draw(b); giwa_roof(d, 11 * TS, 18 * TS, 0 - 4, 1 * TS - 6)
            d.rectangle([11 * TS + 10, 1 * TS - 8, 18 * TS - 10, 1 * TS + 4], fill=(170, 60, 50))
        else:              # 경우궁: 작은 사당 궁 · 밤 · 횃불
            hanok_wall(d, 0, b.width, 3 * TS - 4, 40, col=(150, 140, 126))
            hall(b, 11 * TS, 18 * TS, 4 * TS - 4, wall_h=60, roof_h=36, doors='changho', dan=True, wall=(150, 56, 46), sign='景祐宮')
            d = ImageDraw.Draw(b)
            for x in (10 * TS, 19 * TS + 40):
                d.line([(x, 4 * TS - 4), (x, 2 * TS + 30)], fill=WOOD_D, width=3); d.polygon([(x - 8, 2 * TS + 30), (x + 8, 2 * TS + 30), (x, 2 * TS + 12)], fill=(250, 160, 50))
                glow(b, x, 2 * TS + 24, 90, (255, 170, 80), 80)
            d = ImageDraw.Draw(b)
        for tx in (2, 4, 24, 26): G.tree(b, tx, 7, 'pine', 1.0)
        note_label(b, '창덕궁 · 1884년 12월' if big else '경우궁 · 1884년 12월 4일 밤')
        G.finish(b, m.grid, vignette=0.12 if big else 0.25, ao=0.25, warm=0.05)
        exit_path(b, 14, 14, 11 * TS + 30, '궁 밖으로', col=(170, 166, 156), edge=(130, 126, 116))
    for big, nm in ((False, '!k_gyeongu'), (True, '!k_changdeok')):
        bb = base.copy(); draw(bb, big); save_variant(root, nm, bb)
        if not big: m.big = bb
    m.ev('exit', 14, 12, trigger=1)
    m.ev('gojong', 14, 4, '$k_gojong', dir='down')
    m.ev('roster', 11, 4, '!$k_ledger')
    m.ev('draft', 17, 4, '!$k_seoan')
    m.ev('palmap', 14, 6, '!$k_hmap')
    m.ev('kimokgyun', 12, 6, '$k_kimokgyun', dir='right')
    m.ev('parkyounghyo', 16, 6, '$k_parkyounghyo', dir='left')
    m.ev('seojaepil', 10, 8, '$k_seojaepil', dir='right')
    m.ev('hongyoungsik', 18, 9, '$k_hongyoungsik', dir='left')
    m.ev('takezoe', 18, 7, '$k_takezoe', dir='left')
    m.ev('jpsol1', 20, 8, '$k_jp_soldier', dir='left')
    m.ev('jpsol2', 20, 10, '$k_jp_soldier', dir='left')
    m.ev('cadet', 8, 10, '$k_cadet', dir='right')
    m.ev('hall', 14, 2)
    m.save(root, parallax_name='!k_gyeongu', finish=False, image=False)

# ==================================================================== 07 창덕궁 가는 밤골목 (잠행)
STREET_OBS = [(9, 10), (19, 10), (11, 8), (16, 8), (8, 6), (13, 6), (20, 6), (10, 4), (17, 4)]
def street(root):
    g = grid_open('q', 3)
    for (x, y) in STREET_OBS: g[y][x] = 'k'
    for x in range(7, 22):
        if x != 14: g[3][x] = 'B'
    m = Map('street', 7, [''.join(r) for r in g], 'seoul', 1884)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (20, 24, 46), (44, 46, 70))
    rnd = random.Random(7)
    for _ in range(50): d.point((rnd.randint(0, b.width), rnd.randint(0, 2 * TS)), fill=(220, 220, 240))
    # 창덕궁 담 + 금호문
    d.rectangle([0, 2 * TS - 4, b.width, 4 * TS], fill=(150, 104, 80))
    giwa_roof(d, -10, b.width + 10, 2 * TS - 18, 2 * TS - 2, (60, 62, 70), flare=0, ridge=False)
    X = 14 * TS
    hall(b, X - 50, X + TS + 50, 4 * TS - 2, wall_h=56, roof_h=30, doors='wall', dan=True, wall=(130, 50, 44), sign='金虎門')
    d = ImageDraw.Draw(b)
    d.rectangle([X + 2, 3 * TS + 6, X + TS - 2, 4 * TS - 2], fill=(26, 22, 20))
    # 양옆 초가 · 기와집 담
    for tx in (0, 3, 23, 26):
        d.rectangle([tx * TS, 4 * TS + 6, (tx + 3) * TS - 6, 6 * TS], fill=(170, 160, 140))
        d.polygon([(tx * TS - 6, 4 * TS + 10), ((tx + 3) * TS, 4 * TS + 10), ((tx + 2.5) * TS, 3 * TS + 20), (tx * TS + 20, 3 * TS + 20)], fill=(150, 130, 90))
    # 숨을 곳: 장독대 · 수레 · 짚더미
    for i, (tx, ty) in enumerate(STREET_OBS):
        with Prop(b, tx * TS - 6, ty * TS + 2, 60, 48) as dd:
            k = i % 3
            if k == 0:      # 장독대
                for j, (x, s_) in enumerate(((4, 1.0), (22, 0.85), (36, 0.9))):
                    w = int(18 * s_); h = int(32 * s_)
                    dd.ellipse([x, 46 - h, x + w, 46], fill=(100, 64, 40)); dd.ellipse([x + 3, 46 - h - 2, x + w - 3, 46 - h + 4], fill=(80, 50, 32))
            elif k == 1:    # 짐수레
                dd.rectangle([4, 16, 56, 30], fill=(120, 86, 54)); dd.ellipse([8, 26, 28, 46], outline=(80, 56, 36), width=3); dd.ellipse([34, 26, 54, 46], outline=(80, 56, 36), width=3)
                dd.rectangle([10, 6, 50, 16], fill=(180, 160, 110))
            else:           # 짚더미
                dd.ellipse([4, 12, 56, 46], fill=(190, 160, 96)); dd.ellipse([10, 4, 46, 30], fill=(206, 176, 110))
                for x in range(10, 52, 6): dd.line([(x, 20), (x - 3, 40)], fill=(160, 130, 80))
    for (tx, ty) in ((7, 9), (21, 9), (7, 5), (21, 4)): G.tree(b, tx, ty, 'willow', 0.8)
    note_label(b, '창덕궁 가는 밤골목 · 1884년 12월 4일')
    m.ev('gate', 14, 3, trigger=1)
    m.ev('patrol1', 8, 9, '$k_patrol', dir='left')
    m.ev('patrol2', 20, 7, '$k_patrol', dir='left')
    m.ev('patrol3', 10, 5, '$k_patrol', dir='right')
    m.ev('jar', 16, 8)
    G.finish(b, m.grid, vignette=0.25, ao=0.25, warm=0.0)
    m.save(root, parallax_name='!k_street', finish=False)

# ==================================================================== 08 거문도 (1885)
def geomundo(root):
    g = grid_open(',', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for x in range(7, 22):
        if x != 14: g[11][x] = 'W'
    g[11][14] = 'x'                                          # 나룻배
    for (x, y) in ((12, 5), (16, 4), (8, 4)): g[y][x] = 'x'
    m = Map('geomundo', 8, [''.join(r) for r in g], 'seoul', 1885)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (150, 190, 220), (226, 232, 230))
    sea(b, 1 * TS, 4 * TS, (80, 140, 176), (50, 104, 150))
    d = ImageDraw.Draw(b)
    d.polygon([(0, 1 * TS + 20), (5 * TS, 1 * TS - 10), (9 * TS, 1 * TS + 10), (9 * TS, 1 * TS + 30), (0, 1 * TS + 40)], fill=(96, 130, 90))      # 건너편 섬
    us_ship(b, 18 * TS, 2 * TS + 20, 0.6, col=(40, 40, 46)); us_ship(b, 23 * TS, 2 * TS + 4, 0.5, col=(50, 50, 56))
    d = ImageDraw.Draw(b)
    # 영국 국기 언덕 (오른쪽)
    d.polygon([(21 * TS, 4 * TS), (24 * TS, 2 * TS + 30), (29 * TS, 2 * TS + 10), (29 * TS, 4 * TS)], fill=(110, 140, 90))
    d.line([(25 * TS, 2 * TS + 26), (25 * TS, 1 * TS - 10)], fill=(90, 80, 70), width=3); uk_flag(d, 25 * TS + 2, 1 * TS - 10)
    d.rectangle([22 * TS + 10, 3 * TS + 6, 23 * TS + 30, 3 * TS + 40], fill=(214, 206, 186)); d.polygon([(22 * TS, 3 * TS + 8), (23 * TS + 40, 3 * TS + 8), (22 * TS + 44, 2 * TS + 40)], fill=(120, 110, 100))
    # 해안선 · 마을 (초가)
    d.rectangle([0, 4 * TS - 6, b.width, 4 * TS + 6], fill=(214, 200, 160))
    for tx in (1, 4, 24, 26):
        d.rectangle([tx * TS, 5 * TS, (tx + 2) * TS, 6 * TS + 20], fill=(206, 196, 176))
        d.ellipse([tx * TS - 10, 4 * TS + 20, (tx + 2) * TS + 10, 5 * TS + 20], fill=(190, 160, 96))
    # 미역 말리는 줄
    d.line([(3 * TS, 8 * TS), (6 * TS, 8 * TS + 6)], fill=(110, 80, 50), width=2)
    for x in range(3 * TS + 6, 6 * TS, 10): d.line([(x, 8 * TS + 3), (x, 8 * TS + 24)], fill=(40, 70, 50), width=3)
    sea(b, 11 * TS, 13 * TS, (70, 126, 160), (50, 104, 140), seed=9)
    d = ImageDraw.Draw(b)
    d.rectangle([13 * TS, 10 * TS + 30, 16 * TS, 11 * TS + 10], fill=(150, 110, 70))
    for x in range(13 * TS, 16 * TS, 9): d.line([(x, 10 * TS + 30), (x, 11 * TS + 10)], fill=(120, 86, 52))
    label(b, '거문도 (영국은 포트 해밀턴이라 불렀다)', 14 * TS + 24, 1 * TS + 4, 11, back=(40, 60, 80, 220))
    note_label(b, '전라도 거문도 · 1885년 5월', x=5 * TS, y=10 * TS + 26)
    m.ev('boat', 14, 11, '!$k_boat')
    m.ev('treaties', 12, 5, '!$k_crate')
    m.ev('seamap', 16, 4, '!$k_chart')
    m.ev('cemetery', 8, 4, '!$k_cross')
    m.ev('islander', 9, 8, '$k_islander', dir='right')
    m.ev('islander_w', 11, 9, '$k_islander_w', dir='up')
    m.ev('brsailor', 18, 7, '$k_br_sailor', dir='left')
    m.ev('ding', 16, 9, '$k_ding', dir='left')
    m.ev('mollendorff', 19, 9, '$k_mollendorff', dir='left')
    m.ev('ships', 19, 2)
    G.finish(b, m.grid, vignette=0.12, ao=0.2, warm=0.04)
    m.save(root, parallax_name='!k_geomundo', finish=False)

# ==================================================================== 09 정동 (1888)
def jeongdong(root):
    g = grid_open('.', 4)
    for x in range(7, 22): g[3][x] = 'B'
    for (x, y) in ((14, 4), (21, 4), (20, 5)): g[y][x] = 'x'
    g[5][20] = '.'
    m = Map('jeongdong', 9, [''.join(r) for r in g], 'seoul', 1888)
    b = m.big; d = ImageDraw.Draw(b)
    skyk(b, 2 * TS, (160, 196, 222), (230, 230, 224))
    granite_mts(b, 2 * TS - 10, seed=19, height=80, peaks=((0.2, 1.0), (0.8, 0.7)))
    d = ImageDraw.Draw(b)
    hanok_wall(d, 0, b.width, 3 * TS + 6, 34)
    brick_bldg(b, 1 * TS, 7 * TS, 4 * TS - 2, 2, sign='美國公使館', flag=us_flag, col=(200, 196, 186), trim=(250, 248, 240))
    brick_bldg(b, 8 * TS, 13 * TS - 10, 4 * TS - 2, 2, sign='培材學堂', col=(170, 80, 60))
    hall(b, 15 * TS + 10, 19 * TS + 30, 4 * TS - 2, wall_h=50, roof_h=30, doors='changho', sign='梨花學堂')
    brick_bldg(b, 22 * TS, 28 * TS, 4 * TS - 2, 2, sign='英國公使館', flag=uk_flag, col=(186, 100, 76))
    d = ImageDraw.Draw(b)
    d.line([(0, 30), (b.width, 36)], fill=(30, 30, 34)); d.line([(0, 40), (b.width, 46)], fill=(30, 30, 34))
    for (tx, ty) in ((7, 9), (21, 10)): G.tree(b, tx, ty, 'poplar', 0.9)
    for tx in (1, 3, 25, 27): G.tree(b, tx, 8, 'poplar', 1.0)
    note_label(b, '한양 정동 · 1888년 봄')
    exit_path(b, 14, 14, 11 * TS + 30, '큰길')
    G.finish(b, m.grid, vignette=0.12, ao=0.25, warm=0.05)
    m.ev('exit', 14, 12, trigger=1)
    m.ev('jdmap', 14, 4, '!$k_jdsign')
    m.ev('telpole', 21, 4, '!$k_telpole')
    m.ev('allen', 9, 7, '$k_allen', dir='right')
    m.ev('appenzeller', 12, 6, '$k_appenzeller', dir='down')
    m.ev('scranton', 17, 6, '$k_scranton', dir='down')
    m.ev('hulbert', 19, 8, '$k_hulbert', dir='left')
    m.ev('student', 15, 8, '$k_student_y', dir='left')
    m.ev('telegraph_off', 20, 5, '$k_telegraph_off', dir='left')
    m.ev('peddler2', 8, 10, '$k_peddler', dir='right')
    m.ev('legation', 19, 2)
    m.save(root, parallax_name='!k_jeongdong', finish=False)

def build(root, only=None):
    fns = [seojae, ginza, bakmun, market, ujeong, palace, street, geomundo, jeongdong]
    for f in fns:
        if only and f.__name__ not in only: continue
        f(root); print('map', f.__name__)
    write_mapinfos(root, MAP_NAMES)

if __name__ == '__main__':
    build(sys.argv[1], sys.argv[2:] or None)
