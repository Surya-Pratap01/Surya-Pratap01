#!/usr/bin/env python3
import argparse,json,math,urllib.request
from pathlib import Path

def fetch(url):
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json","User-Agent":"Surya-Profile-Generator"})
    with urllib.request.urlopen(req,timeout=20) as r:return json.load(r)

def draw(data,title,subtitle,dark):
    bg='#0d1117' if dark else '#fff'; fg='#f0f6fc' if dark else '#24292f'; muted='#8b949e' if dark else '#57606a'; grid='#30363d' if dark else '#d0d7de'
    cx,cy,R,n=260,175,112,len(data); pts=[]; out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="360"><rect width="520" height="360" rx="16" fill="{bg}" stroke="{grid}"/><text x="28" y="36" font-family="monospace" font-size="16" font-weight="700" fill="{fg}">{title}</text><text x="28" y="56" font-family="monospace" font-size="9" fill="{muted}">{subtitle}</text>']
    for f in (.25,.5,.75,1):out.append(f'<circle cx="{cx}" cy="{cy}" r="{R*f}" fill="none" stroke="{grid}"/>')
    for i,(lab,val) in enumerate(data):
        ang=-math.pi/2+2*math.pi*i/n; tx=cx+(R+24)*math.cos(ang); ty=cy+(R+24)*math.sin(ang); anchor='start' if math.cos(ang)>.3 else ('end' if math.cos(ang)<-.3 else 'middle')
        pts.append((cx+R*val/100*math.cos(ang),cy+R*val/100*math.sin(ang)))
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+R*math.cos(ang):.1f}" y2="{cy+R*math.sin(ang):.1f}" stroke="{grid}"/><text x="{tx:.1f}" y="{ty:.1f}" text-anchor="{anchor}" dominant-baseline="middle" font-family="monospace" font-size="10" fill="{muted}">{lab}</text><text x="{tx:.1f}" y="{ty+12:.1f}" text-anchor="{anchor}" font-family="monospace" font-size="9" fill="#58A6FF">{val}</text>')
    out.append(f'<polygon points="{" ".join(f"{x:.1f},{y:.1f}" for x,y in pts)}" fill="#58A6FF" fill-opacity=".16" stroke="#58A6FF" stroke-width="2"/></svg>')
    return ''.join(out)

def main():
    p=argparse.ArgumentParser(); p.add_argument("--data"); p.add_argument("--github"); p.add_argument("-o","--out",required=True); a=p.parse_args()
    if a.data:
        d=json.loads(Path(a.data).read_text()); vals=[(x["label"],x["value"]) for x in d["axes"]]; title=d.get("title","Skill Radar"); sub="self-assessed"
    else:
        repos=fetch(f"https://api.github.com/users/{a.github}/repos?per_page=100&type=owner"); totals={}
        for r in repos:
            if r.get("fork"):continue
            try:
                for k,v in fetch(r["languages_url"]).items():totals[k]=totals.get(k,0)+v
            except Exception:pass
        ignored={"HTML","CSS","Shell","Makefile","Dockerfile"}; items=sorted([(k,v) for k,v in totals.items() if k not in ignored],key=lambda x:x[1],reverse=True)[:7] or [("TypeScript",50),("JavaScript",40),("Python",30)]
        mx=max(v for _,v in items); vals=[(k,round(100*(v/mx)**.4)) for k,v in items]; title="Repository language radar"; sub="generated from current repository data"
    for dark in (True,False):
        suf="dark" if dark else "light"; Path(a.out+"-"+suf+".svg").write_text(draw(vals,title,sub,dark),encoding="utf-8")
if __name__=="__main__":main()
