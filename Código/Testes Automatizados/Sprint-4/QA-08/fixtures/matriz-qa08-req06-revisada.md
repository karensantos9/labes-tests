# Matriz QA08 — Comparação múltipla (REQ-06 revisada)

## Regras consolidadas

1. Até 3 alvos manuais no total, somando escolas e municípios.
2. Cada escola selecionada gera uma referência territorial automática, que não consome vaga manual.
3. Total de linhas do gráfico = alvos manuais + referências automáticas das escolas; máximo de 6.
4. Referência automática e município manual do mesmo território são séries distintas; não deduplicar.
5. Referência automática é distinguida visualmente (exemplo: tracejada); seleção manual (exemplo: sólida).
6. Tooltip deve identificar os valores consolidados de ambas as séries e o município histórico correspondente ao ano.
7. Não há média combinada de municípios diferentes.
8. Se o índice escolar estiver indisponível no ano, a linha da escola tem lacuna; a referência municipal pode permanecer se tiver dados válidos; outras linhas continuam.
9. Limpar Filtros retorna ao estado vazio do MVP; remoção individual libera uma vaga.
10. Limiar de cobertura de 60% é exclusivo do nível escolar.
11. Composição inferior apresenta o detalhamento de cada município individualmente como X de Y escolas.

## Matriz de cenários

| ID | Cenário | Massa/Pré-condição | Resultado esperado | Camada | Situação |
|---|---|---|---|---|---|
| QA08-01 | Limite de três alvos manuais | 3 escolas; tentar 4º alvo | Inserção bloqueada; três alvos preservados | FE + contrato BE11 | Preparado, não executado |
| QA08-02 | Seleção mista 2 escolas + 1 município | 3 alvos manuais | Até 5 linhas: 2 escolas + 2 refs + 1 município | FE | Preparado, não executado |
| QA08-03 | Seleção mista 1 escola + 2 municípios | 3 alvos manuais | Até 4 linhas: escola + ref + 2 municípios | FE | Preparado, não executado |
| QA08-04 | Três escolas | 3 escolas com referência anual | Até 6 linhas | FE + BE11 | Preparado, não executado |
| QA08-05 | Três municípios | 3 municípios | 3 linhas, sem linha agregada | FE + BE11 | Preparado, não executado |
| QA08-06 | Quarto alvo manual | Já existem 3 alvos mistos | Seletor desativado; API deve validar limite conforme contrato aprovado | FE + BE | Preparado, não executado |
| QA08-07 | Remoção individual | 3 alvos selecionados | Remove somente um e libera vaga | FE | Preparado, não executado |
| QA08-08 | Limpar Filtros | Seleção não vazia | Remove todos e retorna ao estado vazio | FE | Preparado, não executado |
| QA08-09 | Município manual igual à referência automática | Escola de Belém + município Belém | Duas séries municipais distintas; referência exclui escola, município manual usa regra geral da rede | BE + FE + DAD07 | Preparado; regra DAD07 precisa detalhar universo/fórmula |
| QA08-10 | Valores iguais nas duas séries | Mesmo município e mesmo ano | Não deduplicar; traços distintos e tooltip com ambas | FE | Preparado, não executado |
| QA08-11 | Referência muda de município historicamente | Escola muda de município entre anos | Legenda estável ligada à escola; tooltip mostra município exato de cada ano | BE + FE | Preparado, não executado |
| QA08-12 | Índice da escola indisponível em 2024 | Escola sem valor em 2024; referência válida | NULL/lacuna apenas na escola; referência e outras séries continuam | BE + FE | Preparado, não executado |
| QA08-13 | Estado vazio | Nenhum alvo | Estado inicial do MVP | FE | Preparado, não executado |
| QA08-14 | Erro de requisição/código inválido | Falha ou alvo inválido | Erro específico, aviso na UI e opção de tentar novamente | BE + FE | Preparado; status HTTP depende do BE11 aprovado |
| QA08-15 | Composição para mais de um município | Dois ou três municípios | Cada município detalhado individualmente como X de Y escolas | BE + FE + DAD07 | Preparado, não executado |
| QA08-16 | Limiar de 60% | Escola e município com coberturas variadas | Alerta somente para escola; sem bloqueio dos resultados | BE + FE | Regra definida; execução pendente |

## Contagem esperada de linhas

| Seleção manual | Referências automáticas | Total máximo de linhas |
|---|---:|---:|
| 3 municípios | 0 | 3 |
| 2 escolas + 1 município | 2 | 5 |
| 1 escola + 2 municípios | 1 | 4 |
| 3 escolas | 3 | 6 |

A referência automática é uma série complementar por escola selecionada. Se uma escola não possuir município histórico num determinado ano, o ponto daquela referência deverá seguir o contrato de dados ausentes; isso não autoriza eliminar as demais séries.

## Pendências a confirmar antes da automação

- DAD07: universo de escolas e fórmula da média municipal manual, inclusive cobertura/denominador.
- BE11: estrutura explícita para séries de referência automática como séries independentes.
- BE11: erro HTTP específico para códigos inválidos e alvos inexistentes.
- Frontend: mapeamento visual de estilos (sólido/tracejado), tooltip consolidado e tratamento de séries equivalentes.
- Produto/PO: validar se a ordem dos alvos selecionados precisa ser preservada (consta no BE11 rascunho, não foi explicitada na REQ-06 revisada).

## Nota de escopo

Esta matriz é uma preparação de QA para uma história de descoberta. Nenhum cenário deve ser marcado como aprovado até existir implementação executável e evidência real.
