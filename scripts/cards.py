#!/usr/bin/env python3
import argparse,json,html,urllib.request
from pathlib import Path
def get(url,token=""):
    h={"Accept":"application/vnd.github+json","User-Agent":"Surya-Profile-Generator/1.0"}
    if token:h["Authorization"]="Bearer "+token
    req=urllib.request.Request(url,headers=h)
    with urllib.request.urlopen(req,timeout=30) as r:return json.load(r)
def card(title,sub,rows,dark):
    bg="#0d1117" if dark else "#fff"; fg="#f0f6fc" if dark else "#24292f"; muted="#8b949e" if dark else "#57606a"; line="#30363d" if dark else "#d0d7de"
    o=[f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="260"><rect width="520" height="260" rx="16" fill="{bg}" stroke="{line}"/><text x="28" y="42" font-family="monospace" font-size="17" font-weight="700" fill="{fg}">{html.escape(title)}</text><text x="28" y="62" font-family="monospace" font-size="10" fill="{muted}">{html.escape(sub)}</text>']; y=95
    for k,v in rows:
        o.append(f'<text x="30" y="{y}" font-family="monospace" font-size="12" fill="{muted}">{html.escape(k)}</text><text x="485" y="{y}" text-anchor="end" font-family="monospace" font-size="14" font-weight="700" fill="#58A6FF">{html.escape(str(v))}</text><line x1="30" y1="{y+9}" x2="490" y2="{y+9}" stroke="{line}"/>'); y+=34
    o.append(f'<text x="30" y="238" font-family="monospace" font-size="9" fill="{muted}">Live data • refreshed by GitHub Actions</text></svg>'); return ''.join(o)
def main():
    p=argparse.ArgumentParser(); p.add_argument("--user",required=True); p.add_argument("--out",required=True); p.add_argument("--token",default=""); a=p.parse_args(); out=Path(a.out); out.mkdir(parents=True,exist_ok=True)
    user=get(f"https://api.github.com/users/{a.user}",a.token); repos=[r for r in get(f"https://api.github.com/users/{a.user}/repos?per_page=100&type=owner&sort=updated",a.token) if not r.get("fork")]
    stats=[("Public repositories",user.get("public_repos",len(repos))),("Followers",user.get("followers",0)),("Following",user.get("following",0)),("Stars received",sum(r.get("stargazers_count",0) for r in repos)),("Forks received",sum(r.get("forks_count",0) for r in repos))]
    langs={}
    for r in repos:
        try:
            for k,v in get(r["languages_url"],a.token).items():langs[k]=langs.get(k,0)+v
        except Exception:pass
    items=sorted(langs.items(),key=lambda x:x[1],reverse=True); total=sum(v for _,v in items) or 1; rows=[(k,f"{v/total*100:.1f}%") for k,v in items[:5]]
    if not rows:rows=[("No language data","yet")]
    for dark in (True,False):
        suf="dark" if dark else "light"; (out/f"stats-{suf}.svg").write_text(card("GitHub signal",a.user,stats,dark),encoding="utf-8"); (out/f"languages-{suf}.svg").write_text(card("Repository language mix","top measured languages",rows,dark),encoding="utf-8")
    cfg=out/"projects.json"
    if cfg.exists():
        for pr in json.loads(cfg.read_text()).get("projects",[]):
            repo=pr["repo"]; r=next((x for x in repos if x["name"]==repo),None); lang=(r or {}).get("language") or "GitHub"; stars=(r or {}).get("stargazers_count",0); forks=(r or {}).get("forks_count",0); safe=repo.replace("/","-")
            for dark in (True,False):
                bg="#0d1117" if dark else "#fff"; fg="#f0f6fc" if dark else "#24292f"; muted="#8b949e" if dark else "#57606a"; line="#30363d" if dark else "#d0d7de"; desc=html.escape(pr.get("description",""))
                s=f'<svg xmlns="http://www.w3.org/2000/svg" width="520" height="205"><rect width="520" height="205" rx="16" fill="{bg}" stroke="{line}"/><text x="26" y="38" font-family="monospace" font-size="15" font-weight="700" fill="#58A6FF">{html.escape(repo)}</text><text x="26" y="70" font-family="monospace" font-size="11" fill="{fg}">{desc[:72]}</text><text x="26" y="94" font-family="monospace" font-size="11" fill="{fg}">{desc[72:144]}</text><text x="26" y="146" font-family="monospace" font-size="10" fill="{muted}">LANGUAGE</text><text x="26" y="169" font-family="monospace" font-size="12" font-weight="700" fill="{fg}">{html.escape(str(lang))}</text><text x="490" y="169" text-anchor="end" font-family="monospace" font-size="9" fill="{muted}">★ {stars}   ⑂ {forks}</text></svg>'
                (out/("card-"+safe+"-"+("dark" if dark else "light")+".svg")).write_text(s,encoding="utf-8")
if __name__=="__main__":main()
