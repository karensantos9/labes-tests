
# Matriz de fixtures — QA-01

## 1. Convenções

Os dados são artificiais e servem exclusivamente para validar as regras de cálculo.

Os indicadores devem seguir a ordem registrada em `tests/contrato_qa.py`, em `INDICADORES_ESPERADOS`.

- `1` representa Sim.
- `0` representa Não.
- `None` representa NULL.
- `1 × 10` significa dez valores iguais a 1.
- A série temporal do MVP abrange 2022, 2023, 2024 e 2025.

O índice é calculado como:

Índice = 100 × quantidade de Sim / quantidade de indicadores válidos.

Os valores NULL ficam fora do denominador. Não há cobertura mínima obrigatória neste MVP.

## 2. Fixtures para o índice da escola

### QA01-01 — Registro completo

Entrada: `[1] * 10 + [0] * 7`

- Presentes: 10.
- Indicadores válidos: 17.
- Total esperado: 17.
- Cobertura dos indicadores: 100%.
- Índice esperado: 10 / 17 × 100 = 58,82%.

### QA01-02 — Registro parcial

Entrada: `[1] * 5 + [0] * 2 + [None] * 10`

- Presentes: 5.
- Indicadores válidos: 7.
- Total esperado: 17.
- Cobertura dos indicadores: 41,18%.
- Índice esperado: 5 / 7 × 100 = 71,43%.

### QA01-03 — Um indicador Sim

Entrada: `[1] + [None] * 16`

- Presentes: 1.
- Indicadores válidos: 1.
- Cobertura dos indicadores: 5,88%.
- Índice esperado: 100%.

### QA01-04 — Um indicador Não

Entrada: `[0] + [None] * 16`

- Presentes: 0.
- Indicadores válidos: 1.
- Cobertura dos indicadores: 5,88%.
- Índice esperado: 0%.

### QA01-05 — Todos os indicadores nulos

Entrada: `[None] * 17`

- Presentes: 0.
- Indicadores válidos: 0.
- Cobertura dos indicadores: 0%.
- Índice esperado: NULL.

### QA01-06 — Indicadores ausentes no dicionário

Entrada: somente os dois primeiros indicadores, com valores 1 e 0.

- Presentes: 1.
- Indicadores válidos: 2.
- Total esperado: 17.
- Cobertura dos indicadores: 11,76%.
- Índice esperado: 50%.

## 3. Fixtures para comparação municipal

### QA01-07 — Duas escolas de referência válidas

Escola selecionada: `[1] * 10 + [0] * 7`, índice de 58,82%.

Referências:
- Escola A: `[0] * 17`, índice de 0%.
- Escola B: `[1] * 17`, índice de 100%.

Resultados esperados:
- Denominador de pares: 2.
- Pares válidos: 2.
- Cobertura de pares: 100%.
- Média municipal: (0 + 100) / 2 = 50%.
- Diferença: 58,82 − 50 = +8,82 p.p.

### QA01-08 — Uma escola de referência válida

Escola selecionada: `[1] * 10 + [0] * 7`, índice de 58,82%.

Única referência: `[1] * 17`, índice de 100%.

Resultados esperados:
- Denominador de pares: 1.
- Pares válidos: 1.
- Média municipal: 100%.
- Diferença: 58,82 − 100 = −41,18 p.p.

### QA01-09 — Município sem outras escolas

Escola selecionada: `[1] * 17`.

Referências: lista vazia.

Resultados esperados:
- Índice da escola: 100%.
- Denominador de pares: 0.
- Pares válidos: 0.
- Cobertura de pares: NULL.
- Média municipal: NULL.
- Diferença: NULL.
- Situação: `sem_pares_municipio`.

### QA01-10 — Outras escolas sem índices válidos

Escola selecionada: `[1] * 17`.

Referências:
- Escola A: `[None] * 17`.
- Escola B: `[None] * 17`.

Resultados esperados:
- Denominador de pares: 2.
- Pares válidos: 0.
- Cobertura de pares: 0%.
- Média municipal: NULL.
- Diferença: NULL.
- Situação: `sem_pares_validos`.

### QA01-11 — Média simples sem ponderação por cobertura

Escola selecionada: `[1] * 17`, índice de 100%.

Referências:
- Escola A: `[0] * 17`, índice de 0%.
- Escola B: `[1] + [None] * 16`, índice de 100%.

Resultados esperados:
- Pares válidos: 2.
- Média municipal: (0 + 100) / 2 = 50%.
- Diferença: 100 − 50 = +50 p.p.

### QA01-12 — Exclusão da escola selecionada e filtros

Escola selecionada: `[1] * 10 + [0] * 7`, índice de 58,82%.

Lista de referências fornecida:
- A própria escola selecionada.
- Escola do mesmo município e ano, com índice de 0%.
- Escola do mesmo município e ano, com índice de 100%.
- Escola de outro município, com índice de 100%.
- Escola de outro ano, com índice de 100%.

Resultados esperados:
- A escola selecionada não participa da média.
- Escolas de outros municípios ou anos são ignoradas.
- Denominador de pares: 2.
- Pares válidos: 2.
- Média municipal: 50%.
- Diferença: +8,82 p.p.

## 4. Fixtures da série temporal

### QA01-13 — Lacunas e registro totalmente nulo

Histórico da escola selecionada:

| Ano | Entrada |
|---|---|
| 2022 | `[1] * 13 + [0] * 4` |
| 2023 | Sem registro |
| 2024 | `[None] * 17` |
| 2025 | Sem registro |

Referências:
- Em 2022: uma escola com índice de 100% e outra com índice de 0%.
- Em 2024: uma escola com índice de 100%.

Resultados esperados:
- Os quatro anos devem aparecer na série.
- 2022: índice da escola de 76,47%, média municipal de 50% e diferença de +26,47 p.p.
- 2023: índice da escola e diferença NULL.
- 2024: índice da escola NULL, média municipal de 100% e diferença NULL.
- 2025: índice da escola e diferença NULL.

### QA01-14 — Escola sem histórico em todo o período

Entrada: escola identificada, sem qualquer registro entre 2022 e 2025.

Resultados esperados:
- Série com exatamente quatro pontos.
- Anos ordenados de 2022 a 2025.
- Índice da escola NULL nos quatro anos.
- Média municipal e diferença NULL nos quatro anos, sem referências.

## 5. Cenários de precisão e município histórico

Os cenários QA01-15 e QA01-16 são fixtures matemáticas direcionadas para detectar arredondamento intermediário. Neles, a função recebe explicitamente os três primeiros indicadores esperados (`INDICADORES_ESPERADOS[:3]`) para produzir frações 2/3 e 1/3. Isso não altera o contrato geral do MVP, que continua definido por 17 indicadores.

### QA01-15 — Diferença sem arredondamento intermediário

Escola selecionada: valores dos três indicadores considerados: `[1, 1, 0]`; os outros 14 valores do registro são nulos e não fazem parte do conjunto de indicadores esperado deste cenário.

- Índice exato da escola: 2/3 × 100 = 66,666…%.
- Par municipal: `[1, 0, 0]` nos três indicadores considerados.
- Índice exato do par: 1/3 × 100 = 33,333…%.
- Diferença exata: (2/3 − 1/3) × 100 = 33,333… p.p.
- **Diferença final esperada: 33,33 p.p.**
- Não é correto calcular a diferença subtraindo os valores já arredondados (66,67 − 33,33 = 33,34 p.p.).

### QA01-16 — Média municipal sem arredondamento intermediário

Conjunto de indicadores considerados: os três primeiros indicadores do contrato, fornecidos explicitamente à função de cálculo.

- Par A: `[0, 0, 0]`, índice de 0%.
- Par B: `[1, 1, 0]`, índice exato de 2/3 × 100 = 66,666…%.
- Média exata: (0 + 200/3) / 2 = 100/3 = 33,333…%.
- **Média municipal final esperada: 33,33%.**
- Não é correto arredondar os índices dos pares antes de calcular a média, pois isso pode produzir 33,34% em vez do resultado definido.

### QA01-17 — Município histórico por ano

A mesma escola (`co_entidade = 15012345`) possui registros em municípios diferentes ao longo da série:

| Ano | Município do registro da escola | Código do município | Índice da escola | Índice da referência válida |
|---|---|---:|---:|---:|
| 2022 | Belém | 1501402 | 100% | 0% |
| 2024 | Ananindeua | 1500800 | 100% | 100% |

A identificação mais recente da escola pode indicar Ananindeua, mas isso não deve substituir o município associado ao registro histórico de 2022.

Resultados esperados:

- A consulta dos pares de 2022 deve usar `(ano=2022, co_municipio=1501402)`.
- A consulta dos pares de 2024 deve usar `(ano=2024, co_municipio=1500800)`.
- Em 2022: um par válido, média municipal de 0% e diferença de +100 p.p.
- Em 2024: um par válido, média municipal de 100% e diferença de 0 p.p.
- Os anos 2023 e 2025 continuam presentes na série histórica, mas não devem provocar consultas de pares baseadas em registros inexistentes da escola.

## 6. Revisão da matriz

Antes da entrega, conferir cada cenário contra os testes automatizados, registrar divergências e manter os resultados esperados independentes dos valores retornados pelo backend.
