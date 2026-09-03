#!/usr/bin/env python3
import argparse
from pathlib import Path
from PIL import Image, ImageEnhance

def main():
    p=argparse.ArgumentParser()
    p.add_argument("image")
    p.add_argument("-o","--output",required=True)
    p.add_argument("--cols",type=int,default=72)
    a=p.parse_args()
    im=Image.open(a.image).convert("RGB")
    w,h=im.size; target=.62
    if w/h>target:
        nw=int(h*target); left=(w-nw)//2; im=im.crop((left,0,left+nw,h))
    else:
        nh=int(w/target); top=max(0,(h-nh)//3); im=im.crop((0,top,w,top+nh))
    rows=max(90,min(round(a.cols*im.height/im.width*.48),150))
    im=ImageEnhance.Contrast(im.resize((a.cols,rows),Image.Resampling.LANCZOS)).enhance(1.15)
    px=im.load(); W,H=a.cols*7+40,rows*7+40
    out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}"><rect width="100%" height="100%" rx="20" fill="#0d1117"/><g>']
    for y in range(rows):
        for x in range(a.cols):
            r,g,b=px[x,y]; lum=(.2126*r+.7152*g+.0722*b)/255; rad=.65+2.65*lum
            if rad<.7: continue
            out.append(f'<circle cx="{20+x*7}" cy="{20+y*7}" r="{rad:.2f}" fill="#{r:02x}{g:02x}{b:02x}" opacity=".92"/>')
    out.append('</g></svg>')
    Path(a.output).write_text(''.join(out),encoding='utf-8')
if __name__=="__main__": main()
