# README do perfil — cartões de atividade (RFB Method)

Data: 23/11/2026 · Repositório: `CristianoRFB/CristianoRFB` · Branch: `main`

## Objetivo e invariantes

**Pedido:** adicionar 3 visuais que reproduzem a função dos links de referência fornecidos pelo usuário, usando a paleta preta/vermelha do perfil; pesquisar práticas de README e documentar a intervenção. **Preservar integralmente** todos os conteúdos, cards, projetos, links, currículo, imagens e seções existentes. Não criar outro título visível para a área de métricas.

Baseline consultada antes da intervenção: branch `main` HEAD `09e90c6e024344cccbd92c4605871b9897a6108b`; README blob `ee45b0541c6f838e348b734b5a8ca6909263c328`. Sem PRs e sem Issues abertos no repositório na triagem inicial.

## Referências de pesquisa

- GitHub Docs — [README do perfil](https://docs.github.com/en/account-and-profile/concepts/personal-profile): imagens e Markdown/HTML são aceitos no perfil.
- GitHub Docs — [Primeiros passos com Markdown no GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/quickstart-for-writing-on-github): conteúdo visual responsivo e complementar ao texto.
- [GitHub Readme Activity Graph](https://github.com/Ashutosh00710/github-readme-activity-graph): tipo de visual do **gráfico de atividade**. A hospedagem comunitária foi reportada como indisponível em parte de 2026, portanto **não depender dela na página principal**.
- [GitHub Readme Streak Stats](https://github.com/DenverCoder1/github-readme-streak-stats): referência do cartão de **sequência de contribuições**. O endereço Heroku antigo, presente na referência compartilhada, foi substituído por serviços mais recentes como [streak-stats.demolab.com](https://streak-stats.demolab.com/).
- [GitHub Profile Summary Cards](https://github.com/vn7n24fzkq/github-profile-summary-cards): referência do cartão de **horários de maior atividade**, já gerado diariamente pelo workflow existente.

As três URLs recebidas continham o usuário de outra conta (`GuilhermeOliveira0`). Os cartões adicionados usam somente `CristianoRFB`.

## Implementação e arquitetura

1. **Atividade recente (31 dias):** `assets/activity-graph.png`, gerado por `.github/scripts/generate_activity_extras.py`. Linha vermelha/área escura com dados reais das contribuições públicas por dia.
2. **Sequências / streak (últimos 12 meses):** `assets/streak-card.png`, gerado pelo mesmo script. Mostra total de contribuições do período, sequência atual e maior sequência do período, sem alegar recordes desde a criação da conta.
3. **Horários produtivos:** `assets/productive-time.png`, exportado em PNG a partir de `profile-summary-card-output/radical/4-productive-time.svg`, já calculado pelo gerador que usa `UTC_OFFSET: -3`.

Os dois primeiros gráficos reutilizam a função `get_counts()` do calendário existente (`.github/scripts/generate_contributions_calendar.py`), que consulta a GraphQL API do GitHub com `GITHUB_TOKEN` e possui fallback público já existente. Não são imagens artificiais nem demonstrativos inventados. Os dados podem não incluir contribuições privadas ou atividades não contabilizadas pela API.

**Identidade:** fundo `#0D0D10`, vermelho `#FF1744`, vermelho escuro `#85001F`, branco `#F5F5F5`. Imagens gravadas localmente no repositório via GitHub Actions, em vez de links para servidores externos sem garantia de disponibilidade. Mantidos `alt` descritivos e a leitura em mobile. Links apontam para a aba de contribuições.

**Fluxo:** GitHub Actions `estatisticas.yml` gera SVGs originais, converte cartões existentes para PNG, gera calendário atual, gera gráfico e sequência, gera currículo, atualiza os parâmetros diários de cache (`?v=AAAAMMDD`) e comita somente arquivos produzidos. A atualização agendada já existia; os novos outputs foram integrados ao mesmo processo. Não foi criado serviço pago.

## Protocolo de verificação

- [x] Confirmar estado e permissões do repositório e ausência de PRs/Issues em aberto.
- [x] Inspecionar README e preservar seu conteúdo existente, adicionando **somente** o bloco HTML identificado como `RFB VISUAL STATS`.
- [x] Preservar os quatro PNGs já referenciados e o botão de currículo.
- [x] Incluir três novos caminhos de imagem e respectivo texto alternativo.
- [x] GitHub Actions PASS na execução [45314742479](https://github.com/CristianoRFB/CristianoRFB/actions/runs/45314742479), após correção do push concorrente com rebase não forçado.
- [x] Três PNGs presentes em `assets/`: `activity-graph.png` (83038 bytes), `streak-card.png` (54237 bytes) e `productive-time.png` (35836 bytes).
- [x] README `main` contém exatamente três novas referências de imagem, preservando os cartões existentes, projetos e currículo.

## Reversão mínima

Remover apenas o bloco entre `<!-- RFB VISUAL STATS: ... -->` e `<!-- /RFB VISUAL STATS -->` para restaurar visualmente o README anterior; os demais visuais permanecem intocados. Se necessário, retirar somente as entradas dos novos PNGs e a chamada a `generate_activity_extras.py`, sem alterar os gráficos existentes.

**Limites:** a contagem de sequências considera exclusivamente o histórico público disponibilizado (aproximadamente 12 meses); não substitui o total vitalício de commits. Não foi realizado deploy de produto nem alteração em projetos de SaaS.

## Verificação da rodada (23/11/2026)

- PASS — extração via GitHub GraphQL para gráfico e streak (evidência: logs do Actions).
- PASS — geração de PNGs com identidade visual preto/vermelho; cartão de horários convertido do SVG existente.
- PASS — workflow concluído com sucesso e push no `main`; sem `force-push` e sem PR/Issue alterado.
- PASS — nenhuma seção existente do README foi editada manualmente fora da inserção dos três cartões; a automação diária segue atualizando os números.
- LIMITAÇÃO — não foi feita inspeção visual em navegador móvel real nesta rodada; PNGs possuem tamanhos válidos e podem ser vistos no GitHub.
