#!/usr/bin/env python3
"""Generate a transparent offline QA report for the synthetic 20x3 matrix."""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'tests'))
from test_20_brands import errors_for_output
SOURCE=ROOT/'tests/fixtures/20-brands-3-rounds.json'
DEST=ROOT/'docs/qa-20-marcas.md'


def run():
    data=json.loads(SOURCE.read_text(encoding='utf-8'))
    brands=data['cases']
    results=[]
    for brand in brands:
        checks=[]
        for candidate in brand['outputs']:
            errors=errors_for_output(brand,candidate,brands)
            checks.append((candidate['task'], not errors,errors))
        results.append((brand,checks))
    passed=sum(ok for b,checks in results for task,ok,err in checks)
    total=sum(len(checks) for b,checks in results)
    lines=[
        '# Marketing Hub | Auditoria de 20 marcas fictícias',
        '',
        '**Tipo de teste:** validação offline de perfil e revisão de amostras editoriais autoradas. **Não é uma avaliação da execução em outros modelos de IA.**',
        '',
        '## Resultado objetivo',
        '',
        f'- Perfis distintos: **{len(brands)}**.',
        f'- Passagens por marca: **3** (Instagram, LinkedIn e comentário).',
        f'- Amostras editoriais aprovadas pelos critérios automatizados: **{passed}/{total}**.',
        '- Critérios: relação com o assunto, ausência de termos proibidos, nenhuma outra marca identificada, sem promessas absolutas ou métricas inventadas, estrutura e tamanho dos textos, verificações básicas de idioma.',
        '- Os testes de unidade e validação JSON são executados pelo workflow de CI, separadamente.',
        '',
        '## Matrizes por marca (todas simuladas, nenhuma empresa real)',
        '',
        '| Marca fictícia | Tema | Instagram | LinkedIn | Comentário |',
        '|---|---|:---:|:---:|:---:|',
    ]
    for b,checks in results:
        symbols=['OK' if ok else 'FALHA' for _,ok,_ in checks]
        lines.append(f"| {b['display_name']} | {b['sector']} | {' | '.join(symbols)} |")
    lines += [
        '',
        '## Histórico da execução',
        '',
        '- Rodada inicial: 58/60 exemplos atenderam aos critérios; dois comentários eram genéricos para o nicho.',
        '- Correção: foram reescritos os dois comentários para mencionar, respectivamente, pão e tarefas de equipe; não afrouxamos a regra de relevância.',
        '- Nova rodada: 60/60 amostras autoradas passaram na bateria offline.',
        '- Testes negativos detectam termos proibidos, contaminação entre marcas, promessa não verificada, credencial sintética e nível inválido de formalidade.',
        '',
        '## Limites e decisão de lançamento',
        '',
        '**Não declarar compatibilidade ou qualidade editorial de 100% em diferentes IAs com base nesta auditoria.** As 60 amostras foram escritas como fixtures de avaliação; o repositório é uma skill/prompt e não contém motor de inferência próprio. Não houve chamadas reais ao Claude, Gemini, Copilot ou ChatGPT por instalação da skill. Uma validação funcional exigiria executar os 60 briefings em versões identificadas dos modelos, guardar saídas e fazer revisão editorial independente.',
        '',
        '**Situação:** o projeto é distribuído como prévia pública (beta), com escopo e limitações transparentes. Os testes offline validam estrutura e amostras autoradas; **não** comprovam desempenho na execução em GPT, Claude, Gemini ou Copilot. Não declarar nenhum modelo como validado até completar o protocolo de 60 respostas reais com revisão humana.',
        '',
        '## Reproduzir',
        '',
        '```bash',
        'python -m unittest discover -s tests -v',
        'python scripts/check_repo.py',
        'python scripts/report_20_brands.py',
        '```',
        '',
    ]
    DEST.write_text('\n'.join(lines),encoding='utf-8')
    print(f'Report generated: {passed}/{total} offline samples ({len(brands)} brands), at {DEST}')
    return 0 if total==60 and passed==total else 1

if __name__ == '__main__':
    sys.exit(run())
