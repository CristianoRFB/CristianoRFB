#!/usr/bin/env python3
"""Gera currículo PDF público a partir de experiências confirmadas no currículo 2026/LinkedIn."""
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, KeepTogether

ROOT=Path(__file__).resolve().parents[2]
OUTPUT=ROOT/"assets/Curriculo_Cristiano_Ronaldo_Ferreira_Bueno.pdf"
OUTPUT.parent.mkdir(parents=True,exist_ok=True)
ink=colors.HexColor("#20212A")
red=colors.HexColor("#B3002D")
sub=colors.HexColor("#555762")
grey=colors.HexColor("#E7E7EB")
styles={
 "name":ParagraphStyle("name",fontName="Helvetica-Bold",fontSize=18.7,leading=21,textColor=ink,spaceAfter=3),
 "headline":ParagraphStyle("headline",fontName="Helvetica-Bold",fontSize=9.7,leading=13,textColor=red,spaceAfter=7),
 "contact":ParagraphStyle("contact",fontSize=8.1,leading=11,textColor=sub,spaceAfter=4),
 "section":ParagraphStyle("section",fontName="Helvetica-Bold",fontSize=10,leading=13,textColor=red,spaceBefore=11,spaceAfter=5),
 "text":ParagraphStyle("text",fontSize=8.75,leading=12.1,textColor=ink,spaceAfter=4),
 "small":ParagraphStyle("small",fontSize=8.2,leading=11.3,textColor=ink,spaceAfter=3),
 "role":ParagraphStyle("role",fontName="Helvetica-Bold",fontSize=9.0,leading=12,textColor=ink,spaceAfter=2),
}
def para(text,kind="text"):return Paragraph(text,styles[kind])
def section(title):return para(title.upper(),"section")
def item(title, desc):
    return [para(title,"role"),para(desc,"small")]
doc=SimpleDocTemplate(str(OUTPUT),pagesize=A4,rightMargin=19*mm,leftMargin=19*mm,topMargin=17*mm,bottomMargin=16*mm,author="Cristiano Ronaldo Ferreira Bueno",title="Currículo | Cristiano Ronaldo Ferreira Bueno")
flow=[
    para("Cristiano Ronaldo Ferreira Bueno","name"),
    para("DESENVOLVEDOR FULL STACK | SAAS, SISTEMAS DE GESTÃO E PRODUTOS DIGITAIS","headline"),
    para("Jales - SP  |  <link href='mailto:crisf.bueno10@gmail.com'>crisf.bueno10@gmail.com</link>  |  <link href='https://github.com/CristianoRFB'>GitHub</link>  |  <link href='https://www.linkedin.com/in/cristiano-ronaldo-38022033b/'>LinkedIn</link>","contact"),
    section("Resumo"),
    para("Estudante de Análise e Desenvolvimento de Sistemas na Fatec Jales, com formação técnica pela ETEC. Desenvolvedor freelancer com experiência prática em interfaces, aplicações web, APIs REST, bancos de dados, automação e soluções SaaS. Trabalha com foco em organização de processos, usabilidade e resolução de problemas de negócios."),
    section("Experiência"),
    *item("Desenvolvedor Freelancer | 2025 - atual","Desenvolvimento de websites e sistemas web responsivos; integração de APIs REST e bancos de dados; aplicações com React, Next.js, TypeScript, C#/.NET e Tailwind CSS; soluções de gestão e automação."),
    *item("Designer Gráfico Freelancer | 2022 - atual","Criação de identidades visuais, logotipos, materiais digitais e layouts para web."),
    section("Projetos selecionados"),
    *item("Caravana 77 | SaaS para organizadores","Plataforma em desenvolvimento para inscrições, passageiros, comprovantes, financeiro e check-in; arquitetura multi-tenant e isolamento de dados por organização. React, TypeScript e Firebase."),
    *item("SaaS Food / Restaurante | Sistema de gestão e pedidos","Aplicação para cardápio digital, pedidos, reservas, QR Code de mesas e gestão administrativa, com React/Next.js, Firebase e Cloudflare Workers."),
    *item("SIGO | Sistema de gestão de oficinas","Projeto integrador em equipe; interfaces, integrações com API e fluxo de acompanhamento dos serviços do veículo pelo cliente."),
    *item("Adrenalina | Gestão de lan house","Aplicações desktop para administração e estação cliente, servidor local, autenticação e persistência. C#, .NET, WinForms, WPF e SQLite."),
    section("Competências"),
    para("<b>Frontend:</b> React, Next.js, JavaScript, TypeScript, HTML, CSS, Tailwind CSS, Astro<br/>"
         "<b>Backend:</b> C#, ASP.NET Core, Node.js, Express.js, Python, Laravel, APIs REST<br/>"
         "<b>Dados &amp; ferramentas:</b> PostgreSQL, MySQL, SQL Server, MongoDB, Supabase, Firebase, Git/GitHub, Docker, Swagger, Excel e Power BI","small"),
    section("Formação"),
    para("<b>Fatec Jales:</b> Análise e Desenvolvimento de Sistemas (em andamento)<br/><b>ETEC:</b> Técnico em Desenvolvimento de Sistemas (concluído em 2024)","small"),
    section("Idiomas & certificados"),
    para("<b>Português:</b> nativo | <b>Inglês:</b> avançado | <b>Espanhol, Italiano e Russo:</b> básico<br/>"
         "<b>Certificações e eventos:</b> Análise de Dados com Power BI; Arquitetura de Software e Performance; Como alavancar sua carreira com Power BI; Tendências e Carreira em TI (Even3, out/2026).","small"),
]
def footer(canvas, document):
    canvas.setStrokeColor(grey)
    canvas.line(19*mm,12.8*mm,A4[0]-19*mm,12.8*mm)
    canvas.setFont("Helvetica",7)
    canvas.setFillColor(sub)
    canvas.drawString(19*mm,9.5*mm,"Portfólio e projetos: github.com/CristianoRFB")
doc.build(flow,onFirstPage=footer,onLaterPages=footer)
if OUTPUT.stat().st_size<4000: raise SystemExit("PDF muito pequeno")
print("Currículo gerado:",OUTPUT.name,OUTPUT.stat().st_size,"bytes")
