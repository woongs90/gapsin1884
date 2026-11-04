"""갑신년 그날 밤, 우정총국 타이틀 화면 (img/titles1/Kr_Title.png, 1392x624 + 화면 너비에 맞춰 놓는 조각들)
 별 뜬 한양의 밤, 지평선의 불빛, 청사초롱을 단 우정총국, 가운데 제목 판, 왼쪽 편지 봉투 · 오른쪽 초롱과 활자, 아래 그 시대 사람들
"""
import os, sys, math, random
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from k_common import F
from hd_art import sh, mix
import k_mg as MG

def outlined(d, xy, text, font, fill, ol=(30, 18, 8), w=5, anchor='mm'):
    d.text(xy, text, font=font, fill=fill, anchor=anchor, stroke_width=w, stroke_fill=ol)

def title_image(root, W=1392, H=624):
    bg = Image.new('RGBA', (W, H), (0, 0, 0, 255)); d = ImageDraw.Draw(bg)
    for y in range(H):
        t = y / H
        d.line([(0, y), (W, y)], fill=mix((14, 18, 40), (60, 40, 64), min(1, t * 1.3)) if t < 0.62 else mix((150, 60, 40), (40, 20, 24), (t - 0.62) / 0.38))
    rnd = random.Random(1884)
    for _ in range(140): x, y = rnd.randint(0, W), rnd.randint(0, int(H * 0.5)); d.point((x, y), fill=(230, 230, 250))
    d.ellipse([W * 0.12, H * 0.10, W * 0.12 + 60, H * 0.10 + 60], fill=(250, 240, 200)); d.ellipse([W * 0.12 + 14, H * 0.10 - 6, W * 0.12 + 74, H * 0.10 + 54], fill=(18, 22, 44))
    # 지평선의 불빛 (그날 밤)
    glow = Image.new('L', (W, H), 0); ImageDraw.Draw(glow).ellipse([W * 0.55, H * 0.42, W * 0.95, H * 0.82], fill=200)
    glow = glow.filter(ImageFilter.GaussianBlur(70)); bg.paste((240, 120, 50, 255), (0, 0), glow.point(lambda v: int(v * 0.6)))
    pts = [(0, int(H * 0.68))]
    for x in range(0, W + 40, 40):
        h_ = 40 + 30 * math.sin(x / 90.0) + 110 * max(0, 1 - abs(x - W * 0.3) / (W * 0.18)) + 70 * max(0, 1 - abs(x - W * 0.72) / (W * 0.14))
        pts.append((x, int(H * 0.68 - h_)))
    pts.append((W, int(H * 0.68)))
    ImageDraw.Draw(bg).polygon(pts, fill=(34, 28, 42))
    d = ImageDraw.Draw(bg)
    for k in range(10):                      # 기와지붕 실루엣
        x0 = -40 + k * 150 + rnd.randint(-20, 20); w_ = rnd.randint(140, 210); yb = int(H * 0.88) + rnd.randint(-10, 20)
        dd = ImageDraw.Draw(bg)
        dd.rectangle([x0 + 10, yb - 10, x0 + w_ - 10, H], fill=(30, 20, 26))
        MG.giwa_roof(dd, x0 + 10, x0 + w_ - 10, yb - 58, yb - 14, (26, 18, 24))
        if k % 3 == 1:
            for j in range(3): dd.rectangle([x0 + 30 + j * 30, yb - 2, x0 + 46 + j * 30, yb + 14], fill=(250, 200, 120))
    # 우정총국 (가운데 아래) + 청사초롱
    cx = W // 2; yb = int(H * 0.92)
    d.rectangle([cx - 200, yb - 60, cx + 200, yb + 10], fill=(70, 34, 30))
    for x in range(cx - 190, cx + 190, 38): d.rectangle([x, yb - 52, x + 30, yb], fill=(250, 214, 140))
    MG.giwa_roof(d, cx - 200, cx + 200, yb - 120, yb - 58, (24, 18, 22))
    for x in range(cx - 180, cx + 200, 60):
        d.line([(x, yb - 60), (x, yb - 50)], fill=(40, 30, 20)); d.rounded_rectangle([x - 7, yb - 50, x + 7, yb - 32], 4, fill=(230, 60, 50)); d.rectangle([x - 7, yb - 44, x + 7, yb - 38], fill=(60, 80, 170))
    vig = Image.new('L', (W, H), 0); ImageDraw.Draw(vig).ellipse([-200, -160, W + 200, H + 220], fill=255)
    vig = ImageOps.invert(vig.filter(ImageFilter.GaussianBlur(120)))
    bg.paste(Image.new('RGBA', (W, H), (6, 6, 10, 255)), (0, 0), vig.point(lambda v: int(v * 0.8)))
    d = ImageDraw.Draw(bg)
    # 제목 판
    d.rounded_rectangle([W / 2 - 370, 50, W / 2 + 370, 300], 18, fill=(24, 18, 22, 225), outline=(222, 190, 120), width=3)
    for k, x in enumerate(range(int(W / 2 - 350), int(W / 2 + 350), 20)):
        for y0 in (60, 284):
            d.rectangle([x, y0, x + 9, y0 + 6], fill=(60, 130, 110)); d.rectangle([x + 10, y0, x + 19, y0 + 6], fill=(170, 60, 50) if k % 2 else (60, 90, 150))
    t1, t2 = '갑신년 그날 밤,', '우정총국'
    tsz = 64
    while d.textlength(t1, font=F(tsz, 'serif')) + 12 > 620: tsz -= 2
    outlined(d, (W / 2, 112), t1, F(tsz - 14, 'serif'), (236, 214, 170), w=5)
    tz2 = 78
    while d.textlength(t2, font=F(tz2, 'serif')) + 12 > 620: tz2 -= 2
    outlined(d, (W / 2, 184), t2, F(tz2, 'serif'), (252, 240, 214), w=6)
    outlined(d, (W / 2, 238), '개화파의 분화 · 갑신정변 · 그 뒤 10년 · 1882 – 1893', F(23, 'serif'), (230, 200, 140), w=4)
    outlined(d, (W / 2, 268), '역관 윤재의 편지 묶음 · 개항기 2편', F(17), (240, 232, 214), w=3)
    os.makedirs(os.path.join(root, 'img/titles1'), exist_ok=True)
    # ---- 화면 너비에 맞춰 놓는 조각들
    lt = Image.new('RGBA', (170, 220), (0, 0, 0, 0)); ld = ImageDraw.Draw(lt)        # 편지 봉투 + 우표
    ld.polygon([(10, 60), (160, 40), (166, 190), (16, 210)], fill=(236, 226, 200), outline=(120, 100, 70))
    ld.line([(10, 60), (88, 130), (160, 40)], fill=(150, 130, 100), width=2)
    ld.rectangle([110, 54, 150, 100], fill=(250, 246, 234)); ld.rectangle([114, 58, 146, 96], fill=(214, 90, 100))
    ld.ellipse([122, 68, 138, 84], fill=(250, 246, 234)); ld.text((130, 90), '5文', font=F(9, 'serif'), fill=(250, 246, 234), anchor='mm')
    ld.text((70, 160), '윤 역관께', font=F(16, 'serif'), fill=(60, 50, 80), anchor='mm')
    lt.save(os.path.join(root, 'img/titles1/Kr_TitleLeft.png'))
    rt = Image.new('RGBA', (150, 220), (0, 0, 0, 0)); rd = ImageDraw.Draw(rt)       # 청사초롱 + 활자
    rd.line([(75, 0), (75, 30)], fill=(60, 50, 40), width=3)
    rd.rounded_rectangle([40, 30, 110, 130], 18, fill=(220, 60, 50)); rd.rectangle([40, 62, 110, 98], fill=(60, 80, 170))
    g = Image.new('L', (150, 220), 0); ImageDraw.Draw(g).ellipse([20, 20, 130, 140], fill=110); g = g.filter(ImageFilter.GaussianBlur(14))
    rt.paste((255, 200, 120, 255), (0, 0), g); rd = ImageDraw.Draw(rt)
    rd.rounded_rectangle([40, 30, 110, 130], 18, fill=(220, 60, 50)); rd.rectangle([40, 62, 110, 98], fill=(60, 80, 170))
    rd.line([(75, 130), (75, 150)], fill=(220, 60, 50), width=3)
    rd.rounded_rectangle([46, 160, 104, 214], 6, fill=(130, 126, 120), outline=(70, 66, 62), width=3)
    gl = Image.new('RGBA', (58, 54), (0, 0, 0, 0)); ImageDraw.Draw(gl).text((29, 27), '報', font=F(34, 'serif'), fill=(50, 46, 42), anchor='mm')
    rt.alpha_composite(gl.transpose(Image.FLIP_LEFT_RIGHT), (46, 160))
    rt.save(os.path.join(root, 'img/titles1/Kr_TitleRight.png'))
    people = ['$k_dolsoe', '$k_yunhee23', '$k_hongyoungsik', '$k_seojaepil', '$k_seogwangbeom', '$k_parkyounghyo', '$k_kimokgyun', '$k_yunjae26',
              '$k_minyoungik', '$k_takezoe', '$k_yuan', '$k_mollendorff', '$k_foote', '$k_allen', '$k_father93']
    n = len(people); gap = 76
    strip = Image.new('RGBA', (gap * n + 66, 58 * 3), (0, 0, 0, 0))
    for k, p in enumerate(people):
        sh_ = Image.open(os.path.join(root, 'img/characters', p + '.png')).convert('RGBA')
        fw, fh = sh_.width // 3, sh_.height // 4
        fr = sh_.crop((fw, 0, fw * 2, fh)).resize((fw * 3, fh * 3), Image.NEAREST)
        strip.alpha_composite(fr, (int(33 + gap * k + gap / 2 - fw * 1.5), 0))
    strip = strip.crop(strip.getbbox())
    strip.save(os.path.join(root, 'img/titles1/Kr_TitlePeople.png'))
    bg.convert('RGB').save(os.path.join(root, 'img/titles1/Kr_Title.png'))

if __name__ == '__main__':
    title_image(sys.argv[1]); print('title ok')
