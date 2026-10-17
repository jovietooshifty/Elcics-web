import numpy as np, potrace, sys
from PIL import Image, ImageFilter
S=8; TH=150; VT=int(sys.argv[1]) if len(sys.argv)>1 else 75
g=Image.open('logo_hi_gray.png').convert('L')
big=g.resize((319*S,212*S),Image.LANCZOS).filter(ImageFilter.GaussianBlur(S*0.4))
a=np.array(big)
mask=a>=TH
# carve faint leaf veins: inside leaf region, mid-gray pixels that sit inside dark fill
g0=np.array(Image.open('logo_hi_gray.png').resize((319*S,212*S),Image.BICUBIC).filter(ImageFilter.GaussianBlur(S*0.25))).astype(float)
reg=np.zeros_like(mask); reg[0:66*S,105*S:200*S]=True
vein=reg&(g0>=VT)
from PIL import ImageDraw
vm=Image.new('L',(319*S,212*S),0); dr=ImageDraw.Draw(vm)
VEINS=[((133.3,17.5),(140,23),(145.8,31.7)),((153.3,7.5),(155.5,14),(156.7,21.7)),((161.7,27.5),(168,25),(175,24.2)),((123.3,37.5),(131,41),(139.2,46.7)),((156.7,44.2),(166,41.5),(176.7,40.8))]
for p0,p1,p2 in VEINS:
    pts=[((1-t)**2*p0[0]+2*(1-t)*t*p1[0]+t*t*p2[0], (1-t)**2*p0[1]+2*(1-t)*t*p1[1]+t*t*p2[1]) for t in [i/20 for i in range(21)]]
    dr.line([(x*S,y*S) for x,y in pts],fill=255,width=max(1,int(S*0.5)))
mask=mask|(np.array(vm)>0)
bmp=potrace.Bitmap(mask)
path=bmp.trace(turdsize=30, turnpolicy=potrace.POTRACE_TURNPOLICY_MINORITY, alphamax=1.0, opticurve=True, opttolerance=0.2)
def build(sc,dx,dy,prec=3):
    def P(p): return f"{round(p.x/S*sc+dx,prec):g} {round(p.y/S*sc+dy,prec):g}"
    out=[]
    for c in path:
        s="M"+P(c.start_point)
        for seg in c.segments:
            s+= ("L"+P(seg.c)+"L"+P(seg.end_point)) if seg.is_corner else ("C"+P(seg.c1)+" "+P(seg.c2)+" "+P(seg.end_point))
        out.append(s+"Z")
    return ''.join(out)
import json
json.dump({'native':build(1,0,0,2)},open('paths.json','w'))
SC,DX,DY=0.526,-13.4,11.4
GREEN='#1D5F2F'
d140=build(SC,DX,DY)
hdr=lambda w,h,vb,body,bg: f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="{vb}">\n  <title>ELCICS Ltd. logo</title>\n'+(f'  <rect x="{vb.split()[0]}" y="{vb.split()[1]}" width="{vb.split()[2]}" height="{vb.split()[3]}" fill="#FFFFFF"/>\n' if bg else '')+f'  <path fill="{GREEN}" fill-rule="evenodd" d="{body}"/>\n</svg>\n'
open('ELCICS-logo.svg','w').write(hdr(140,140,'0 0 140 140',d140,False))
open('ELCICS-logo-white-bg.svg','w').write(hdr(140,140,'0 0 140 140',d140,True))
dn=build(1,0,0,2)
open('ELCICS-logo-full-artwork.svg','w').write(hdr(319,212,'0 0 319 212',dn,False))
print(len(path))
