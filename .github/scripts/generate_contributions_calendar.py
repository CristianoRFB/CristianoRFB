#!/usr/bin/env python3
"""Renderiza calendário real de contribuições do GitHub em PNG, com paleta do perfil."""
from __future__ import annotations
import html
import json
import os
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path
import cairosvg

USER = "CristianoRFB"
ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets/contribution-calendar.png"
TODAY = datetime.now(timezone.utc).date()
FROM = TODAY - timedelta(days=370)
START = TODAY - timedelta(days=364)
START -= timedelta(days=(START.weekday()+1)%7)
C = ["#1F2028", "#4A0A1D", "#8A1132", "#CB1348", "#FF1744"]
SHORTMONTH = ["Jan","Fev","Mar","Abr","Mai","Jun","Jul","Ago","Set","Out","Nov","Dez"]

def request_json(url, payload=None, token=None):
    headers = {"User-Agent": "CristianoRFB-ProfileReadme/1.0", "Accept": "application/json"}
    if token:
        headers["Authorization"] = "Bearer " + token
    data = json.dumps(payload).encode("utf-8") if payload else None
    if payload:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers)
    with urllib.request.urlopen(req, timeout=25) as response:
        return json.load(response)

def get_counts():
    token = os.getenv("GITHUB_TOKEN", "")
    if token:
        query = """query($login:String!, $from:DateTime!, $to:DateTime!) {
          user(login:$login) { contributionsCollection(from:$from,to:$to) {
            contributionCalendar { weeks { contributionDays { date contributionCount contributionLevel } } }
          } } }"""
        try:
            data = request_json(
                "https://api.github.com/graphql",
                {"query":query, "variables":{
                    "login":USER, "from":FROM.isoformat()+"T00:00:00Z",
                    "to":TODAY.isoformat()+"T23:59:59Z"}},
                token,
            )
            if data.get("errors"): raise RuntimeError(str(data["errors"])[:250])
            weeks = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]["weeks"]
            result = {d["date"]:int(d["contributionCount"]) for w in weeks for d in w["contributionDays"]}
            if len(result) > 300:
                print("Dados: GitHub GraphQL; dias =",len(result))
                return result
            raise RuntimeError("Calendário incompleto")
        except Exception as exc:
            print("GitHub GraphQL indisponível:",exc)
    try:
        data = request_json(f"https://github-contributions-api.jogruber.de/v4/{USER}?y=last")
        result = {d["date"]:int(d["count"]) for d in data["contributions"]}
        if len(result)>300:
            print("Dados: contribuições públicas agregadas; dias =",len(result))
            return result
    except Exception as exc:
        print("API pública indisponível:",exc)
    raise RuntimeError("Sem dados comprovados. Não desenhar quadradinhos fictícios.")

def main():
    try:
        daily=get_counts()
    except Exception:
        if OUT.exists() and OUT.stat().st_size>2000:
            print("Preservando calendário anterior válido")
            return
        raise
    cell,gap=10,3
    step=cell+gap
    ncols=((TODAY-START).days//7)+1
    left,top=42,46
    width=left+step*ncols+17
    height=top+step*7+45
    parts=[f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{width}" height="{height}">',
           f'<rect width="100%" height="100%" rx="12" fill="#111114"/>',
           '<text x="18" y="23" fill="#fafafa" font-family="Arial, sans-serif" font-size="15" font-weight="bold">Calendário de contribuições</text>']
    for i,day in enumerate(["Dom","Seg","Ter","Qua","Qui","Sex","Sáb"]):
        if i in (1,3,5):
            parts.append(f'<text x="9" y="{top+i*step+9}" fill="#aaaab2" font-family="Arial" font-size="9">{day}</text>')
    previous_month=0
    total=0
    for week in range(ncols):
        first=START+timedelta(days=week*7)
        if first.month!=previous_month:
            previous_month=first.month
            parts.append(f'<text x="{left+week*step}" y="{top-9}" fill="#cccbd0" font-family="Arial" font-size="10">{SHORTMONTH[first.month-1]}</text>')
        for dayind in range(7):
            date=first+timedelta(days=dayind)
            if date>TODAY:continue
            val=daily.get(date.isoformat(),0)
            total+=val
            level=0 if val==0 else 1 if val<=2 else 2 if val<=5 else 3 if val<=10 else 4
            x=left+week*step
            y=top+dayind*step
            parts.append(f'<rect x="{x}" y="{y}" width="{cell}" height="{cell}" rx="2" fill="{C[level]}"><title>{date.isoformat()}: {val} contribuições</title></rect>')
    parts.extend([
        f'<text x="{left}" y="{height-18}" fill="#aaaab2" font-family="Arial" font-size="10">Últimos 12 meses · {total} contribuições públicas</text>',
        f'<text x="{width-125}" y="{height-18}" fill="#aaaab2" font-family="Arial" font-size="10">Menos</text>'
    ])
    for i,c in enumerate(C):
        parts.append(f'<rect x="{width-86+i*14}" y="{height-27}" width="10" height="10" rx="2" fill="{c}"/>')
    parts.append("</svg>")
    OUT.parent.mkdir(parents=True,exist_ok=True)
    cairosvg.svg2png(bytestring="".join(parts).encode("utf-8"),write_to=str(OUT),output_width=width*2)
    print("Calendário gerado:",OUT.name,OUT.stat().st_size,"bytes",total,"contribuições")
if __name__=="__main__":main()
