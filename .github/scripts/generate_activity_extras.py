#!/usr/bin/env python3
"""Dois cartões próprios para o README: atividade (31 dias) e sequência (12 meses).

RFB: não inventa métricas. Reusa a consulta de contribuições usada pelo
calendário atual. PNGs ficam no próprio repositório, sem serviço Heroku/Vercel.
"""
from __future__ import annotations

from datetime import date, timedelta
from pathlib import Path
import cairosvg

import generate_contributions_calendar as source

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)
BG = "#0D0D10"
PANEL = "#16161B"
RED = "#FF1744"
DARK_RED = "#85001F"
WHITE = "#F5F5F5"
MUTED = "#A8A8B3"
GRID = "#303039"


def text(x: int | float, y: int | float, value: str, size: int = 19,
         fill: str = MUTED, bold: bool = False, anchor: str = "start") -> str:
    weight = "bold" if bold else "normal"
    return (f'<text x="{x}" y="{y}" fill="{fill}" text-anchor="{anchor}" '
            f'font-family="Arial, Helvetica, sans-serif" font-weight="{weight}" '
            f'font-size="{size}">{value}</text>')


def render(svg_parts: list[str], width: int, height: int, output: Path, scale: int = 2) -> None:
    doc = (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" '
           f'viewBox="0 0 {width} {height}">' + "".join(svg_parts) + "</svg>")
    cairosvg.svg2png(bytestring=doc.encode("utf-8"),
                    write_to=str(output), output_width=width * scale)
    if not output.exists() or output.stat().st_size < 2000:
        raise RuntimeError(f"PNG ausente ou pequeno: {output}")
    print(f"{output.relative_to(ROOT)} ({output.stat().st_size} bytes)")


def activity_graph(counts: dict[str, int], today: date) -> None:
    width, height = 1050, 365
    left, top, right, bottom = 55, 73, 35, 58
    w, h = width-left-right, height-top-bottom
    last_31 = [(today-timedelta(days=30-i), 0) for i in range(31)]
    last_31 = [(d, counts.get(d.isoformat(), 0)) for d, _ in last_31]
    max_count = max(1, max(v for _, v in last_31))
    ceiling = max(5, ((max_count+4)//5)*5)
    points = [(left + i*w/30, top+h - v*h/ceiling) for i, (_,v) in enumerate(last_31)]
    point_str = " ".join(f"{x:.1f},{y:.1f}" for x,y in points)
    area = f"{left},{top+h} " + point_str + f" {left+w},{top+h}"
    parts = [
        f'<rect x="0" y="0" width="{width}" height="{height}" rx="18" fill="{BG}"/>',
        text(30,37,"Atividade recente",24,WHITE,True),
        text(width-28,37,"Últimos 31 dias · contribuições públicas",14,MUTED,False,"end"),
        '<defs><linearGradient id="areaFill" x1="0" y1="0" x2="0" y2="1">'
        f'<stop offset="0" stop-color="{RED}" stop-opacity=".45"/>'
        f'<stop offset="1" stop-color="{RED}" stop-opacity=".02"/>'
        '</linearGradient></defs>',
    ]
    for step in range(5):
        y=top+h-step*h/4
        value=round(ceiling*step/4)
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{left+w}" y2="{y:.1f}" stroke="{GRID}" stroke-width="1"/>')
        parts.append(text(left-13,y+5,str(value),12,MUTED,False,"end"))
    parts += [
        f'<polygon points="{area}" fill="url(#areaFill)"/>',
        f'<polyline points="{point_str}" fill="none" stroke="{RED}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round"/>',
    ]
    for i,(x,y) in enumerate(points):
        if last_31[i][1]>0:
            parts.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="3.2" fill="{WHITE}" stroke="{RED}" stroke-width="1.6"/>')
    for i in (0,5,10,15,20,25,30):
        x=points[i][0]
        label=last_31[i][0].strftime("%d/%m")
        parts.append(text(x, top+h+31,label,12,MUTED,False,"middle"))
    render(parts,width,height,OUT/"activity-graph.png")


def calculate_streaks(counts: dict[str,int], today: date) -> tuple[int,int,int]:
    if len(counts)<300:
        raise ValueError("Histórico insuficiente")
    days=sorted(date.fromisoformat(k) for k in counts)
    start=max(days[0],today-timedelta(days=364))
    end=min(today,days[-1])
    dates=[start+timedelta(days=i) for i in range((end-start).days+1)]
    positive = {d:counts.get(d.isoformat(),0)>0 for d in dates}
    total=sum(counts.get(d.isoformat(),0) for d in dates)
    longest=running=0
    for d in dates:
        running = running+1 if positive[d] else 0
        longest=max(longest,running)
    current=0
    latest=end
    # Manter streak de ontem se ainda não houver contribuições hoje.
    if latest==today and not positive.get(latest,False):
        latest-=timedelta(days=1)
    while latest>=start and positive.get(latest,False):
        current+=1
        latest-=timedelta(days=1)
    return total,current,longest


def streak_card(counts: dict[str,int], today: date) -> None:
    total,current,longest=calculate_streaks(counts,today)
    width,height=840,254
    third=width/3
    parts=[
        f'<rect width="{width}" height="{height}" rx="18" fill="{BG}"/>',
        text(28,38,"Sequência de contribuições",22,WHITE,True),
        text(width-26,38,"Últimos 12 meses",14,MUTED,False,"end"),
    ]
    for col in range(3):
        x=18+col*third
        parts.append(f'<rect x="{x:.1f}" y="62" width="{third-28:.1f}" height="154" rx="12" fill="{PANEL}" stroke="{GRID}"/>')
    data=[
        ("Contribuições",total,"No período"),
        ("Sequência atual",current,"Dias consecutivos"),
        ("Maior sequência",longest,"Dias no período"),
    ]
    for i,(label,value,desc) in enumerate(data):
        x=18+i*third+(third-28)/2
        parts.append(text(x,104,label,15,MUTED,False,"middle"))
        parts.append(text(x,160,str(value),43,RED,True,"middle"))
        parts.append(text(x,193,desc,12,MUTED,False,"middle"))
    parts.append(text(width/2,238,"Fonte: contribuições públicas da API do GitHub",11,MUTED,False,"middle"))
    render(parts,width,height,OUT/"streak-card.png")


def main() -> None:
    today=source.TODAY
    data=source.get_counts()
    if len(data)<300:
        raise RuntimeError("Não é possível gerar as estatísticas sem histórico verificável")
    activity_graph(data,today)
    streak_card(data,today)


if __name__=="__main__":
    main()
