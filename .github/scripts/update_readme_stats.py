#!/usr/bin/env python3
"""Atualiza os contadores legíveis do README com os dados já gerados pelo workflow.

Fonte única: profile-summary-card-output/radical/3-stats.svg
Não consulta APIs externas nem inventa valores se o gerador falhar.
"""

from __future__ import annotations

import re
import xml.etree.ElementTree as ET
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parents[2]
SVG_PATH = ROOT / "profile-summary-card-output/radical/3-stats.svg"
README_PATH = ROOT / "README.md"

START = "<!-- PROFILE_STATS_START -->"
END = "<!-- PROFILE_STATS_END -->"

LABELS = (
    "Total Stars:",
    "Total Commits:",
    "Total PRs:",
    "Total Issues:",
    "Contributed to:",
)
NUMBER_PATTERN = re.compile(r"\d[\d,]*(?:\.\d+)?[kKmM]?")


def read_counts() -> dict[str, str]:
    root = ET.parse(SVG_PATH).getroot()
    texts = [
        "".join(element.itertext()).strip()
        for element in root.iter()
        if element.tag.split("}")[-1] == "text"
    ]

    try:
        positions = [texts.index(label) for label in LABELS]
    except ValueError as exc:
        raise RuntimeError("Cartão de estatísticas não contém os rótulos esperados") from exc

    if positions != list(range(positions[0], positions[0] + len(LABELS))):
        raise RuntimeError("Ordem dos rótulos no cartão mudou; dados não serão publicados")

    values = texts[positions[-1] + 1 : positions[-1] + 1 + len(LABELS)]
    if len(values) != len(LABELS) or any(not NUMBER_PATTERN.fullmatch(v) for v in values):
        raise RuntimeError("Valores inesperados no SVG; README preservado")

    return dict(zip(LABELS, values))


def render_block(counts: dict[str, str]) -> str:
    updated_at = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%d/%m/%Y")
    return f"""\
{START}
| Indicador | Total | Histórico |
| :--- | ---: | :--- |
| Commits | **{counts["Total Commits:"]}** | [Ver commits](https://github.com/search?q=author%3ACristianoRFB&type=commits) |
| Pull requests | **{counts["Total PRs:"]}** | [Ver PRs](https://github.com/search?q=author%3ACristianoRFB&type=pullrequests) |
| Issues | **{counts["Total Issues:"]}** | [Ver issues](https://github.com/search?q=author%3ACristianoRFB&type=issues) |
| Repositórios com contribuições | **{counts["Contributed to:"]}** | [Ver atividade](https://github.com/CristianoRFB?tab=overview) |

<sub>Atualizado automaticamente em {updated_at} (horário de Brasília). Totais calculados pelo gerador de estatísticas do perfil; não representam apenas o ano atual.</sub>
{END}"""


def main() -> None:
    counts = read_counts()
    original = README_PATH.read_text(encoding="utf-8")
    pattern = re.compile(re.escape(START) + r".*?" + re.escape(END), re.DOTALL)
    if len(pattern.findall(original)) != 1:
        raise RuntimeError("Marcadores de estatísticas ausentes ou duplicados no README")

    updated = pattern.sub(lambda _: render_block(counts), original, count=1)
    # O cache de imagens do GitHub pode preservar cartões antigos. Altere a
    # versão diária das três imagens para que o app obtenha os novos PNGs.
    version = datetime.now(ZoneInfo("America/Sao_Paulo")).strftime("%Y%m%d")
    image_pattern = re.compile(
        r"(https://raw\.githubusercontent\.com/CristianoRFB/CristianoRFB/main/"
        r"assets/(?:stats|languages|contributions)\.png)\?v=\d{8}"
    )
    if len(image_pattern.findall(updated)) != 3:
        raise RuntimeError("São esperadas exatamente três imagens de estatísticas versionadas")
    updated = image_pattern.sub(lambda match: match.group(1) + "?v=" + version, updated)
    if updated != original:
        README_PATH.write_text(updated, encoding="utf-8")
    print("Estatísticas atualizadas:", ", ".join(f"{k} {v}" for k, v in counts.items()))


if __name__ == "__main__":
    main()
