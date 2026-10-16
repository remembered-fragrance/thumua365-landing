# Vẽ các dải cảnh làng quê (SVG) ở đáy từng mục rồi chèn thẳng vào index.html.
# Chạy lại bao nhiêu lần cũng được: cảnh cũ bị xoá trước khi chèn cảnh mới.
#   python tools/ve-canh.py index.html
import random, re, sys

P = sys.argv[1]
s = open(P, encoding='utf-8').read()
s = re.sub(r'    <svg class="(scene|sky)".*?</svg>\n', '', s, flags=re.S).replace(' class="sc" ', ' ')

def svg(body, cls='scene'):
    return (f'    <svg class="{cls}" viewBox="0 0 1440 200" preserveAspectRatio="xMidYMax slice" aria-hidden="true">'
            + body + '</svg>\n')

def tree(x, y, r, c1, c2, trunk):
    return (f'<rect x="{x-4}" y="{y}" width="8" height="{170-y}" fill="{trunk}"/>'
            f'<circle cx="{x}" cy="{y-r*.4:.0f}" r="{r}" fill="{c1}"/><circle cx="{x+r*.6:.0f}" cy="{y-r*.1:.0f}" r="{r*.7:.0f}" fill="{c2}"/>'
            f'<circle cx="{x-r*.6:.0f}" cy="{y:.0f}" r="{r*.6:.0f}" fill="{c2}"/>')

def sack(x, y, w=34, h=24, fill='#e3c189', st='#b8894e'):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{fill}" stroke="{st}" stroke-width="1.5"/>'

def ground(back, front):
    return (f'<path fill="{back}" d="M0 140C180 108 340 130 520 114S860 98 1040 122 1300 102 1440 120V200H0Z"/>',
            f'<path fill="{front}" d="M0 172C320 160 640 182 960 168S1300 166 1440 174V200H0Z"/>')

sc = {}

# 1. Vì sao — xe hàng chạy vào vựa, cân bàn, bao chất trước cửa
b, f = ground('#ece3cf', '#e6dcc6')
sc['vi-sao'] = svg(b + tree(130, 120, 40, '#a9cc96', '#8fbf7c', '#8a5a34') + tree(1310, 118, 42, '#a9cc96', '#8fbf7c', '#8a5a34')
    + '<rect x="790" y="112" width="200" height="60" fill="#f1d7a8"/><path fill="#8a5a34" d="M768 118 880 76 1012 118Z"/>'
    + '<path d="M800 112l80-30M840 112l40-15M920 112l-40-15M960 112l-80-30" stroke="#a87348" stroke-width="2" opacity=".6"/>'
    + '<rect x="838" y="124" width="104" height="48" fill="#6b4a2e"/>' + sack(848, 150, 28, 22) + sack(878, 150, 28, 22) + sack(863, 130, 28, 22)
    + '<rect x="853" y="100" width="74" height="12" rx="3" fill="#14663c"/>'
    + sack(1006, 148) + sack(1042, 148) + sack(1024, 124)
    + '<rect x="688" y="164" width="84" height="8" rx="2" fill="#7b7468"/><rect x="760" y="124" width="5" height="42" fill="#7b7468"/>'
    + '<circle cx="762" cy="118" r="12" fill="#fff" stroke="#7b7468" stroke-width="3"/><path d="M762 118l6-7" stroke="#d4462a" stroke-width="2"/>'
    + '<g class="truck"><rect x="420" y="118" width="160" height="42" rx="4" fill="#2f7d4f"/>'
    + sack(430, 96) + sack(468, 96) + sack(506, 96) + sack(544, 96, 30) + sack(449, 74, 36, 22) + sack(487, 74, 36, 22)
    + '<path fill="#e6a817" d="M582 122h40l22 22v18h-62z"/><path fill="#d7ecf5" d="M592 128h26l16 16h-42z"/>'
    + '<g fill="#33241a"><circle cx="462" cy="162" r="13"/><circle cx="612" cy="162" r="13"/></g>'
    + '<g fill="#cfc6b6"><circle cx="462" cy="162" r="5"/><circle cx="612" cy="162" r="5"/></g></g>' + f)

# 2. Chuyện của vựa — xóm đêm sáng đèn, cây cau, khói bếp; trời sao ở trên
def house(x, w, h, roof, wall, win):
    top = 170 - h
    return (f'<rect x="{x}" y="{top}" width="{w}" height="{h}" fill="{wall}"/><path d="M{x-10} {top+2} {x+w/2:.0f} {top-34} {x+w+10} {top+2}Z" fill="{roof}"/>'
            f'<circle cx="{x+w*.3:.0f}" cy="{top+h*.45:.0f}" r="18" fill="#f2b53a" opacity=".18"/>'
            f'<rect x="{x+w*.3-9:.0f}" y="{top+h*.45-8:.0f}" width="18" height="16" rx="2" fill="{win}"/>'
            f'<rect x="{x+w*.62:.0f}" y="{top+h-30}" width="16" height="30" fill="#140d08"/>')
def areca(x, h):
    t = 170 - h
    return (f'<path d="M{x} 170q4 {-h/2:.0f} 0 {-h}" stroke="#20150d" stroke-width="5" fill="none"/>'
            f'<path d="M{x} {t}c-22-6-36 2-44 14M{x} {t}c22-6 36 2 44 14M{x} {t}c-8-18-24-24-38-22M{x} {t}c8-18 24-24 38-22M{x} {t}c-2-16 2-26 6-30" stroke="#20150d" stroke-width="4" fill="none" stroke-linecap="round"/>')
smoke = ''.join(f'<circle class="puff" style="animation-delay:-{i*1.3:.1f}s" cx="742" cy="74" r="{6+i}" fill="#cbb79c"/>' for i in range(3))
sc['van-de'] = svg('<path fill="#2a1c13" d="M0 150C200 128 420 150 640 136S1100 122 1440 140V200H0Z"/>'
    + areca(250, 120) + areca(300, 96) + areca(1190, 118) + areca(1240, 92)
    + '<rect x="736" y="78" width="12" height="26" fill="#1c130c"/>' + smoke
    + house(500, 110, 56, '#1c130c', '#24180f', '#f6c453') + house(680, 130, 66, '#1c130c', '#24180f', '#f6c453')
    + house(880, 100, 50, '#1c130c', '#24180f', '#f6c453')
    + '<path fill="#22170f" d="M0 176C320 166 640 184 960 172S1300 170 1440 178V200H0Z"/>')
random.seed(7)
stars = ''
for i in range(34):
    x = random.choice([random.uniform(20, 380), random.uniform(1060, 1420), random.uniform(380, 1060)])
    y = random.uniform(16, 190)
    r = random.choice([1.2, 1.6, 2, 2.4])
    tw = ' class="tw" style="animation-delay:-%.1fs"' % random.uniform(0, 4) if i % 3 == 0 else ''
    stars += f'<circle{tw} cx="{x:.0f}" cy="{y:.0f}" r="{r}"/>'
sky = ('    <svg class="sky" viewBox="0 0 1440 220" preserveAspectRatio="xMidYMin slice" aria-hidden="true">'
       f'<g fill="#f8e6b0">{stars}</g><circle cx="1250" cy="70" r="40" fill="#f8e6b0" opacity=".08"/>'
       '<path d="M1244 44a28 28 0 1 0 26 44 22 22 0 1 1-26-44z" fill="#f8e6b0"/></svg>\n')
sc['van-de'] = sky + sc['van-de']

# 3. Lợi ích — rẫy cao su có chén hứng mủ, người cạo mủ
rows = ''
for i, x in enumerate(range(40, 1440, 112)):
    h = 112 + (i % 3) * 6
    rows += (f'<rect x="{x}" y="{170-h}" width="14" height="{h}" fill="#b7c3a3"/>'
             f'<path d="M{x} {128-(i%2)*6}l14-9" stroke="#8a9479" stroke-width="2"/><rect x="{x+3}" y="{132-(i%2)*6}" width="9" height="7" rx="2" fill="#fff"/>')
canopy = ''.join(f'<circle cx="{x}" cy="{50+(i%3)*8}" r="{36+(i%4)*5}" fill="{"#a9d199" if i%2 else "#95c585"}"/>' for i, x in enumerate(range(0, 1500, 70)))
sc['loi-ich'] = svg('<path fill="#d3e6ca" d="M0 150C300 140 700 158 1000 146S1300 144 1440 150V200H0Z"/>' + canopy + rows
    + '<path fill="#c6ddb9" d="M0 174C320 164 640 182 960 170S1300 168 1440 176V200H0Z"/>')

# 4. Tính năng — cây điều trĩu trái, xe đạp chở giỏ điều
def cashew_tree(x, r):
    fr = ''
    for k, (dx, dy) in enumerate([(-.5, .3), (.1, .5), (.5, .2), (-.2, -.1), (.35, -.25)]):
        cx, cy = x + dx * r, 92 + dy * r
        col = '#e0573b' if k % 2 else '#f2b53a'
        fr += f'<path d="M{cx-5:.0f} {cy:.0f}q5-10 10 0l-2 10h-6z" fill="{col}"/><path d="M{cx-3:.0f} {cy+10:.0f}q3 6 7 1" stroke="#8a6a4a" stroke-width="3" fill="none"/>'
    return (f'<rect x="{x-5}" y="96" width="10" height="74" fill="#7a5638"/><ellipse cx="{x}" cy="84" rx="{r}" ry="{r*.62:.0f}" fill="#6fa35c"/>'
            f'<ellipse cx="{x+r*.35:.0f}" cy="74" rx="{r*.55:.0f}" ry="{r*.35:.0f}" fill="#83b56f"/>' + fr)
nuts = ''.join(f'<path d="M{x} 113q6-8 12 0q-2 7-6 4q-4 3-6-4z" fill="#e3c189" stroke="#b8894e" stroke-width="1"/>' for x in range(624, 672, 10))
bike = ('<g transform="translate(660 122)" stroke="#33241a" stroke-width="4" fill="none" stroke-linecap="round" stroke-linejoin="round">'
        '<circle cx="0" cy="38" r="20"/><circle cx="92" cy="38" r="20"/>'
        '<path d="M0 38 30 8 45 38ZM30 8h42L45 38M72 8l20 30M72 8l4-12M68-4h16M24 4h12"/></g>')
sc['tinh-nang'] = svg('<path fill="#f3ead6" d="M0 150C300 136 700 156 1000 144S1300 140 1440 148V200H0Z"/>'
    + cashew_tree(110, 70) + cashew_tree(300, 54) + cashew_tree(1150, 58) + cashew_tree(1340, 72)
    + '<rect x="618" y="112" width="60" height="26" rx="6" fill="#c58a4a"/><path d="M618 120h60M618 128h60" stroke="#a46f39" stroke-width="2"/>' + nuts + bike
    + '<path fill="#efe3c8" d="M0 174C320 164 640 182 960 170S1300 168 1440 176V200H0Z"/>')

# 6. Ai dùng được — nhà nông dân, vựa, công ty nối nhau bằng một con đường
win = ''.join(f'<rect x="{x}" y="{y}" width="12" height="12" fill="#8ea4e0"/>' for x in range(944, 1010, 20) for y in range(66, 150, 22))
sc['ai-dung'] = svg('<path fill="#ece3cf" d="M0 140C180 108 340 130 520 114S860 98 1040 122 1300 102 1440 120V200H0Z"/>'
    + tree(120, 118, 38, '#a9cc96', '#8fbf7c', '#8a5a34') + tree(1330, 116, 40, '#a9cc96', '#8fbf7c', '#8a5a34')
    + '<path d="M300 150l60-6M300 160l70-6M300 140l50-6" stroke="#8fbf7c" stroke-width="6" stroke-linecap="round"/>'
    + '<rect x="420" y="124" width="96" height="46" fill="#ecd6a6"/><path d="M406 128 468 92 530 128Z" fill="#d9a85a"/><rect x="458" y="140" width="18" height="30" fill="#8a5a34"/>'
    + '<rect x="660" y="118" width="130" height="52" fill="#f1d7a8"/><path fill="#8a5a34" d="M646 122 725 90 804 122Z"/><rect x="692" y="132" width="66" height="38" fill="#6b4a2e"/><rect x="700" y="106" width="50" height="10" rx="3" fill="#14663c"/>'
    + '<rect x="930" y="56" width="92" height="114" fill="#d7def3"/><rect x="924" y="50" width="104" height="8" fill="#1e40af"/>' + win
    + '<path d="M300 178C460 168 560 182 725 176S940 170 1100 180" stroke="#d4c19c" stroke-width="10" fill="none" stroke-linecap="round"/>'
    + '<path d="M300 178C460 168 560 182 725 176S940 170 1100 180" stroke="#fff" stroke-width="2" stroke-dasharray="10 12" fill="none"/>'
    + '<path fill="#e6dcc6" d="M0 186C320 180 640 194 960 186S1300 184 1440 188V200H0Z"/>')

# 7. Gói — mặt trời lên trên đồi cà phê chín
rays = ''.join(f'<path d="M720 150 L{720+190*__import__("math").cos(a):.0f} {150-190*__import__("math").sin(a):.0f}" />' for a in [i*3.1416/9 for i in range(1, 9)])
sc['goi'] = svg('<g class="sunup"><g stroke="#f6d77a" stroke-width="10" stroke-linecap="round" opacity=".35">' + rays + '</g>'
    + '<circle cx="720" cy="150" r="80" fill="#f6d77a"/><circle cx="720" cy="150" r="62" fill="#f2c14e"/></g>'
    + '<path fill="#ead9ad" d="M0 150C300 118 560 150 720 140S1140 112 1440 140V200H0Z"/>'
    + '<path fill="#e6d3a2" d="M0 166C260 146 520 170 760 158S1180 144 1440 160V200H0Z"/>'
    + '<path fill="#e3cf9e" d="M0 176C320 166 640 184 960 172S1300 170 1440 178V200H0Z"/>')

# 8. Hỏi đáp — gốc cây, võng đung đưa, nón lá, ấm trà
sc['hoi-dap'] = svg('<path fill="#ece3cf" d="M0 150C300 138 700 158 1000 146S1300 142 1440 150V200H0Z"/>'
    + tree(150, 120, 40, '#a9cc96', '#8fbf7c', '#8a5a34') + tree(1320, 118, 44, '#a9cc96', '#8fbf7c', '#8a5a34')
    + '<rect x="1004" y="60" width="16" height="112" fill="#8a5a34"/><circle cx="1012" cy="64" r="50" fill="#95c585"/><circle cx="1054" cy="80" r="36" fill="#a9d199"/><circle cx="968" cy="82" r="34" fill="#a9d199"/>'
    + '<rect x="768" y="96" width="8" height="76" fill="#8a5a34"/>'
    + '<g class="sway"><path d="M772 104C820 150 950 150 1006 104" stroke="#b8894e" stroke-width="2" fill="none"/>'
    + '<path d="M780 110C826 160 948 160 998 110C946 142 830 142 780 110Z" fill="#e6a817"/><path d="M800 124C850 150 930 150 980 124" stroke="#d4462a" stroke-width="3" fill="none"/></g>'
    + '<path d="M612 170 640 154 668 170Z" fill="#ead39a"/><path d="M612 170h56" stroke="#c9a85e" stroke-width="2"/>'
    + '<rect x="450" y="146" width="110" height="8" rx="2" fill="#8a5a34"/><rect x="460" y="154" width="8" height="18" fill="#8a5a34"/><rect x="542" y="154" width="8" height="18" fill="#8a5a34"/>'
    + '<ellipse cx="498" cy="134" rx="18" ry="13" fill="#5f8f43"/><rect x="491" y="118" width="14" height="5" rx="2" fill="#4a7334"/><path d="M515 132l12-8" stroke="#5f8f43" stroke-width="5" stroke-linecap="round"/>'
    + '<path d="M482 128c-10 0-10 12 0 12" stroke="#4a7334" stroke-width="3" fill="none"/>'
    + '<rect x="528" y="136" width="10" height="10" rx="2" fill="#fff" stroke="#b9ad98"/><rect x="544" y="136" width="10" height="10" rx="2" fill="#fff" stroke="#b9ad98"/>'
    + '<path fill="#e6dcc6" d="M0 174C320 164 640 182 960 170S1300 168 1440 176V200H0Z"/>')

for sid, markup in sc.items():
    a = s.index(f'<section id="{sid}"')
    b = s.index('  </section>', a)
    s = s[:b] + markup + s[b:]
    # gắn class để chừa chỗ cho cảnh ở đáy
    s = s.replace(f'<section id="{sid}" ', f'<section id="{sid}" class="sc" ', 1)
open(P, 'w', encoding='utf-8').write(s)
print({k: len(v) for k, v in sc.items()}, sum(len(v) for v in sc.values()))
