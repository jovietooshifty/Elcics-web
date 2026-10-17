import json
from PIL import Image, ImageDraw
from PIL import ImageFont
P=[(p['group'],p['name'],p['hex'],p['use'],p['source']) for p in json.load(open('out/ELCICS-brand-colours.json'))]
F='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'; FB='/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
W,H=1800,1480
im=Image.new('RGB',(W,H),'white'); d=ImageDraw.Draw(im)
t=lambda s,b=False: ImageFont.truetype(FB if b else F,s)
logo=Image.open('out/ELCICS-logo-1120x1120-transparent.png').resize((220,220))
im.paste(logo,(60,30),logo)
d.text((300,80),'ELCICS Ltd. - Brand Colours',font=t(52,True),fill='#33343F')
d.text((300,150),'Logo green measured from the logo artwork; neutrals and gold from the current site theme.',font=t(24),fill='#5F6176')
y=290
def lumi(h):
    r,g,b=[int(h[i:i+2],16)/255 for i in (1,3,5)]; return 0.2126*r+0.7152*g+0.0722*b
for grp in ['Primary','Accent','Neutral']:
    items=[p for p in P if p[0]==grp]
    d.text((60,y),grp.upper(),font=t(22,True),fill='#5F6176'); y+=36
    x=60; cw=(W-120-20*4)//5
    for i,(g,n,h,u,s) in enumerate(items):
        if i==5: x=60; y+=250
        d.rounded_rectangle((x,y,x+cw,y+150),radius=14,fill=h,outline='#C8C9D3' if h in('#FFFFFF','#F7F7F7','#F1F5F3') else h,width=2)
        tc='#FFFFFF' if lumi(h)<0.45 else '#33343F'
        d.text((x+18,y+108),h,font=t(24,True),fill=tc)
        d.text((x,y+162),n,font=t(24,True),fill='#33343F')
        d.text((x,y+194),s,font=t(15),fill='#5F6176')
        x+=cw+20
    y+=250
im=im.crop((0,0,W,y+10)); im.save('out/ELCICS-brand-colours.png'); print(im.size)
