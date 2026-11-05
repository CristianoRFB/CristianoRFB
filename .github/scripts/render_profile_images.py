#!/usr/bin/env python3
"""Exporta cartões SVG versionados para PNG (compatíveis com o app móvel GitHub).

As imagens de estatísticas vêm do gerador existente. O painel Adrenalina
é uma prévia ilustrativa mantida no repositório Lan-House; cópia de fonte
versionada aqui para evitar serviços externos e URLs instáveis.
"""
from pathlib import Path
import cairosvg

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "assets"
OUT.mkdir(parents=True, exist_ok=True)

ASSETS = [
    ("profile-summary-card-output/radical/3-stats.svg", "stats.png", 1020),
    ("profile-summary-card-output/radical/2-most-commit-language.svg", "languages.png", 1020),
    ("profile-summary-card-output/radical/0-profile-details.svg", "contributions.png", 1400),
    (".github/assets/adrenalina-admin.svg", "adrenalina-admin.png", 960),
]

for source, target, width in ASSETS:
    svg = ROOT / source
    if not svg.is_file():
        raise SystemExit(f"Arquivo obrigatório ausente: {source}")
    output = OUT / target
    cairosvg.svg2png(
        bytestring=svg.read_bytes(),
        write_to=str(output),
        output_width=width,
    )
    if output.stat().st_size < 1024:
        raise SystemExit(f"PNG inesperadamente vazio: {output}")
    print(f"{output.relative_to(ROOT)}: {output.stat().st_size} bytes")
