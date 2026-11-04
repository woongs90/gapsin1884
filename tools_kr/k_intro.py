"""갑신년 그날 밤, 우정총국 인트로 영상 (movies/Kr_Intro.webm · .mp4, 1280x720, 약 44초, 건너뛸 수 없음)
 0~6   검은 화면 글씨: 1893년 섣달 그믐, 김옥균의 편지
 6~14  동아시아 지도: 임오군란 뒤 한성의 청군 · 일본 경비병, 도쿄로 가는 수신사
 14~21 윤재의 서재
 21~35 편지 묶음 속 장면들 (긴자 · 박문국 · 운종가 · 우정총국 축하연 · 경우궁 · 거문도)
 35~44 제목
"""
import os, sys, math, subprocess, shutil
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps, ImageEnhance
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
from k_common import F
import k_music as MU
import k_geo as GEO

W, H, FPS, DUR = 1280, 720, 30, 44.0
def ease(x): return 0 if x <= 0 else 1 if x >= 1 else x * x * (3 - 2 * x)
def seg(t, a, b): return 0 if t < a else 1 if t > b else (t - a) / (b - a)
def fio(t, a, b, f=0.6): return ease(seg(t, a, a + f)) * (1 - ease(seg(t, b - f, b)))

def sepia(im):
    g = ImageOps.grayscale(im.convert('RGB'))
    return ImageOps.colorize(g, (36, 24, 14), (250, 236, 206)).convert('RGBA')

def text(frame, s, y, size, a, col=(250, 236, 206), kind='serif'):
    if a <= 0: return
    lay = Image.new('RGBA', frame.size, (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
    d.text((W / 2, y), s, font=F(size, kind), fill=col + (int(255 * a),), anchor='mm', stroke_width=3, stroke_fill=(20, 12, 6, int(200 * a)))
    frame.alpha_composite(lay)

def compose(root, mid, par, keep):
    """지도 원경 위에 그 장면의 인물들을 세운 그림 (가운데 17칸)"""
    import json
    mp = json.load(open(os.path.join(root, 'data', 'Map%03d.json' % mid), encoding='utf-8'))
    im = Image.open(os.path.join(root, 'img/parallaxes', par + '.png')).convert('RGBA')
    DIR = {2: 0, 4: 1, 6: 2, 8: 3}
    for e in sorted([e for e in mp['events'] if e], key=lambda e: e['y']):
        if e['name'] not in keep: continue
        pg = e['pages'][0]; img = pg['image']['characterName']
        if not img: continue
        sh_ = Image.open(os.path.join(root, 'img/characters', img + '.png')).convert('RGBA')
        fw, fh = sh_.width // 3, sh_.height // 4
        r = DIR[pg['image']['direction']]
        im.alpha_composite(sh_.crop((fw, r * fh, fw * 2, r * fh + fh)), (e['x'] * 48 + 24 - fw // 2, e['y'] * 48 + 48 - fh))
    top = os.path.join(root, 'img/parallaxes', par + '_top.png')
    if os.path.exists(top): im.alpha_composite(Image.open(top).convert('RGBA'))
    return im.crop((288, 0, 1104, 624))

SHOT_KEEP = {
    '!k_ginza': (2, {'gaslamp', 'postbox', 'newsboy', 'kimokgyun', 'minyoungik', 'parkyounghyo', 'seogwangbeom', 'fukuzawa', 'rickshaw', 'jp_police'}),
    '!k_bakmun': (3, {'kimokgyun', 'parkyounghyo', 'hongyoungsik', 'kimyunsik', 'eoyunjung'}),
    '!k_market84': (4, {'yunhee', 'qmerchant', 'peddler', 'market_w', 'qing1', 'qing2', 'silk', 'jpshop', 'coinboard', 'hyesang'}),
    '!k_ujeong_night': (5, {'hongyoungsik', 'minyoungik', 'foote', 'chenshutang', 'aston', 'mollendorff', 'shimamura', 'parkyounghyo', 'kimokgyun', 'empty_seat', 'table1', 'table2', 'mailbox'}),
    '!k_gyeongu': (6, {'gojong', 'kimokgyun', 'parkyounghyo', 'seojaepil', 'takezoe', 'jpsol1', 'jpsol2', 'cadet'}),
    '!k_geomundo': (8, {'boat', 'treaties', 'seamap', 'cemetery', 'islander', 'islander_w', 'brsailor', 'ding'}),
}
def tone(im, dark=(14, 20, 34), light=(214, 230, 244)):
    g = ImageOps.grayscale(im.convert('RGB'))
    return ImageOps.colorize(g, dark, light).convert('RGBA')

def build(root):
    pars = os.path.join(root, 'img', 'parallaxes')
    lib = Image.open(os.path.join(pars, '!k_seojae.png')).convert('RGBA').crop((288, 0, 1104, 624))
    st_big = lib.resize((int(816 * 1.7), int(624 * 1.7)), Image.NEAREST)
    hero = Image.open(os.path.join(root, 'img/characters/$k_yunjae37.png')).convert('RGBA')
    fw, fh = hero.width // 3, hero.height // 4
    hero = hero.crop((fw, 0, fw * 2, fh)).resize((fw * 4, fh * 4), Image.NEAREST)
    shots = [('!k_ginza', '1882  도쿄 긴자 · 수신사 일행'), ('!k_bakmun', '1883  박문국 · 갈라지는 개화'), ('!k_market84', '1884  운종가 · 청 상인과 당오전'),
             ('!k_ujeong_night', '1884년 12월 4일  우정총국 축하연'), ('!k_gyeongu', '그날 밤  경우궁'), ('!k_geomundo', '1885  거문도 · 영국 함대')]
    shot_imgs = []
    for n, cap in shots:
        mid, keep = SHOT_KEEP[n]
        im = compose(root, mid, n, keep).resize((780, 596), Image.LANCZOS)
        shot_imgs.append((tone(im, (40, 26, 16), (250, 236, 206)), cap))
    ARROWS = [((118.0, 37.5), (126.6, 37.4), '청군 3,000명 (1882)', (250, 210, 120)), ((131.0, 34.0), (126.8, 37.3), '일본 공사관 경비병', (250, 200, 200)),
              ((126.4, 37.3), (138.8, 35.4), '수신사 일행 → 도쿄', (200, 230, 250))]
    base = GEO.render(1880, (112, 146, 26, 46), (W, H), colors=lambda p, o: (176, 160, 120) if 'Korea' in (p.get('NAME') or '') else (100, 92, 84),
                      line_w=0.6, seed=1880, paper=False, sea=(18, 30, 50), line=(40, 34, 30))
    world, pj = base[0].convert('RGBA'), base[1]
    grain = [Image.effect_noise((W // 2, H // 2), 40).resize((W, H)).convert('L') for _ in range(4)]
    tmp = os.path.join(root, '_intro_frames'); os.makedirs(tmp, exist_ok=True)
    N_ = int(DUR * FPS)
    for i in range(N_):
        t = i / FPS
        fr = Image.new('RGBA', (W, H), (8, 6, 4, 255))
        if t < 6.2:
            text(fr, '1893년 섣달 그믐, 한양.', H / 2 - 40, 34, fio(t, 0.6, 6.0))
            text(fr, '역관 윤재에게 바다 건너 편지 한 통이 왔다.', H / 2 + 20, 26, fio(t, 2.0, 6.0), col=(230, 214, 180))
            text(fr, '보낸 사람은 아홉 해 전 \'사흘의 나라\'를 세웠던 김옥균.', H / 2 + 62, 24, fio(t, 3.0, 6.0), col=(210, 196, 166))
        elif t < 14.2:
            fr.alpha_composite(world)
            d = ImageDraw.Draw(fr)
            x, y = pj(127.0, 37.0); d.text((x - 20, y + 40), '조선', font=F(30, 'serif'), fill=(250, 236, 200), stroke_width=3, stroke_fill=(30, 20, 10), anchor='mm')
            for j, (a0, a1, lb, col) in enumerate(ARROWS):
                kj = seg(t, 6.8 + j * 2.0, 8.8 + j * 2.0)
                if kj <= 0: continue
                x0, y0 = pj(*a0); x1, y1 = pj(*a1); xx = x0 + (x1 - x0) * ease(kj) * 0.9; yy = y0 + (y1 - y0) * ease(kj) * 0.9
                d.line([(x0, y0), (xx, yy)], fill=col, width=4); d.ellipse([xx - 7, yy - 7, xx + 7, yy + 7], fill=col)
                d.text((x0 + 10, y0 + 14), lb, font=F(20), fill=col, stroke_width=2, stroke_fill=(10, 10, 20))
            text(fr, '임오군란 뒤, 청과 일본의 군대가 한성에 머물렀다', 70, 34, fio(t, 6.6, 14.0))
            text(fr, '개화를 꿈꾸던 젊은이들은 두 갈래로 나뉜다.', H - 70, 24, fio(t, 8.0, 14.0), col=(230, 214, 180), kind='sans')
            a = fio(t, 6.2, 14.2, 0.6)
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - a)))))
        elif t < 21.2:
            k = seg(t, 14.2, 21.2)
            x = int(-60 - k * 260); y = int(-180 + k * 40)
            fr.alpha_composite(st_big, (x, y))
            fr.alpha_composite(Image.new('RGBA', (W, H), (20, 14, 30, int(90 * (1 - k * 0.5)))))
            fr.alpha_composite(hero, (W // 2 - 90, 330))
            a = fio(t, 14.2, 21.2, 0.6)
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * (1 - a)))))
            text(fr, '서른일곱 살 역관 윤재, 편지 묶음 여섯을 풀다', 90, 32, fio(t, 14.6, 20.8))
        elif t < 35.2:
            k = (t - 21.2) / (14.0 / 6)
            idx = min(5, int(k)); kk = k - idx
            im, cap = shot_imgs[idx]
            sc = 0.82 + kk * 0.05
            im2 = im.resize((int(780 * sc), int(596 * sc)), Image.LANCZOS)
            frame = Image.new('RGBA', (im2.width + 24, im2.height + 64), (240, 228, 200, 255)); frame.alpha_composite(im2, (12, 12))
            d = ImageDraw.Draw(frame); d.text((frame.width / 2, im2.height + 38), cap, font=F(24, 'serif'), fill=(60, 40, 24), anchor='mm')
            rot = frame.rotate(-2 + idx * 0.9, expand=True, resample=Image.BICUBIC)
            a = min(1, kk / 0.18) * (1 if kk < 0.85 else (1 - (kk - 0.85) / 0.15))
            rot.putalpha(rot.split()[3].point(lambda v: int(v * a)))
            fr.alpha_composite(rot, ((W - rot.width) // 2, (H - rot.height) // 2))
        else:
            text(fr, '편지 한 묶음을 풀 때마다,', H / 2 - 150, 30, fio(t, 35.4, 39.4))
            text(fr, '그날 밤의 한양이 되살아난다.', H / 2 - 104, 30, fio(t, 36.2, 39.4))
            a = ease(seg(t, 39.0, 40.5))
            text(fr, '갑신년 그날 밤, 우정총국', H / 2 + 10, 66, a, col=(250, 236, 200))
            text(fr, '개화파의 분화에서 갑신정변, 그 뒤 10년까지 · 1882 – 1893', H / 2 + 88, 28, a, col=(220, 196, 150))
            fr.alpha_composite(Image.new('RGBA', (W, H), (0, 0, 0, int(255 * ease(seg(t, 42.6, 44.0))))))
        g = grain[i % 4]
        fr.paste(Image.new('RGBA', (W, H), (140, 110, 80, 255)), (0, 0), g.point(lambda v: max(0, v - 128) // 7))
        fr.convert('RGB').save(os.path.join(tmp, 'f%05d.png' % i))
    trk = MU.Track(DUR)
    music = MU.kr_title()
    fade = np.clip(np.minimum(np.arange(len(music)) / (MU.SR * 3), 1), 0, 1)
    m = music[:int(MU.SR * DUR)] * 0.85
    m[:len(fade)] *= fade[:len(m)]
    trk.add(m, 0.0)
    for k in range(6): trk.add(MU.se_paper() * 0.5, 21.2 + k * 14.0 / 6)
    out = trk.render(0.2, loop=False)
    end = int(MU.SR * (DUR - 1.5)); out[end:] *= np.linspace(1, 0, len(out) - end)
    wav = os.path.join(tmp, 'a.wav'); MU.save(wav, out)
    md = os.path.join(root, 'movies'); os.makedirs(md, exist_ok=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%05d.png'), '-i', wav,
                    '-c:v', 'libvpx', '-b:v', '2.2M', '-crf', '10', '-c:a', 'libvorbis', '-q:a', '4', '-shortest', os.path.join(md, 'Kr_Intro.webm')], check=True)
    subprocess.run(['ffmpeg', '-loglevel', 'error', '-y', '-framerate', str(FPS), '-i', os.path.join(tmp, 'f%05d.png'), '-i', wav,
                    '-c:v', 'libx264', '-preset', 'veryfast', '-crf', '23', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '128k', '-movflags', '+faststart', '-shortest',
                    os.path.join(md, 'Kr_Intro.mp4')], check=True)
    shutil.rmtree(tmp)
    print('intro ok')

if __name__ == '__main__':
    build(sys.argv[1])
