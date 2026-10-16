# Evidências de execução — QA-01 e QA-02

## Última execução registrada

| Campo | Resultado |
|---|---|
| Data da execução registrada | 2026-10-16 |
| Comando executado | `python -m pytest <pasta tests> -v --junitxml=<caminho do XML>` via `uv run --project "$env:LABES_API_ROOT"` |
| Testes aprovados | **16** |
| Testes falhos | **0** |
| Erros | **0** |
| Testes ignorados | **0** |
| Duração | **0,83 segundo** |
| Código de saída | **0** |
| Resultado geral | **Suíte aprovada** |
| Relatório JUnit | `qa01-qa02-junit.xml` |
| Log detalhado | `execucao-qa01-qa02.txt`, caso gerado e presente nesta pasta |

A saída do terminal apresentou:

```text
============================= 16 passed in 0.83s ==============================
Código de saída do pytest: 0
Suíte aprovada.
```

## Distribuição dos testes

| Arquivo | Quantidade registrada |
|---|---:|
| `test_qa02_indice.py` | 7 |
| `test_qa02_comparacao.py` | 6 |
| `test_qa02_serie.py` | 3 |
| **Total** | **16** |

## Regras cobertas

- Índice = 100 × indicadores presentes (`Sim`) ÷ indicadores válidos.
- `Não` conta como zero e permanece no denominador.
- `NULL` fica fora do denominador.
- Índice nulo quando não há indicadores válidos.
- Ausência de chaves de indicadores tratada conforme o contrato de 17 indicadores.
- Exclusão da escola selecionada da média municipal.
- Filtro de município e ano nas referências.
- Média aritmética simples dos índices das outras escolas válidas.
- Diferença em pontos percentuais.
- Quantidade, denominador e cobertura de pares válidos.
- Município sem outras escolas versus município com escolas, mas sem pares válidos.
- Escola selecionada sem dados, mas com média municipal calculável.
- Ordenação dos anos e preservação da série 2022–2025.
- Distinção entre ano sem registro e registro com todos os indicadores nulos.

## Observações de escopo

Esta evidência documenta somente QA-01 e QA-02. Não comprova a validação dos códigos HTTP da QA-03 nem da interface da QA-04.

O resultado de 16 testes refere-se à execução registrada no terminal. Preserve o XML JUnit e o log correspondente junto desta documentação. Se os testes forem alterados e executados novamente, atualize a contagem, a duração, o código de saída e os arquivos de evidência para refletir aquela execução real.
