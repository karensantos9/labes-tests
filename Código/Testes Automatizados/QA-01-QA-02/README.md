# QA-01 e QA-02 — Análise Temporal Escola × Município

## Objetivo

Preparar fixtures calculáveis e executar testes independentes das regras matemáticas da análise temporal Escola × Município para o MVP da Sprint 3.

A suíte fica no repositório `labes-tests` e executa as funções do backend usando a variável de ambiente `LABES_API_ROOT`. Não é necessário iniciar a API nem conectar ao banco de dados.

## Escopo

- **QA-01:** documentar cenários, dados artificiais e resultados esperados conferidos manualmente.
- **QA-02:** automatizar as regras de cálculo do índice, da comparação municipal e da série temporal.
- Anos da série: 2022, 2023, 2024 e 2025.
- Indicadores candidatos: 17.
- `1` representa Sim; `0` representa Não; `None` representa NULL.
- NULL fica fora do denominador; Não conta como zero e permanece no denominador.
- Não há cobertura mínima obrigatória neste MVP.
- A média municipal é a média aritmética simples dos índices válidos das outras escolas do mesmo município, excluindo a escola selecionada.
- A média e a diferença devem ser calculadas com os valores não arredondados, aplicando o arredondamento apenas ao resultado final.
- Cada ano deve consultar os pares do município associado ao registro histórico daquele ano.
- A série deve preservar anos sem registro e registros cujo conjunto de indicadores é totalmente nulo.

## Estrutura

- `fixtures/matriz-qa01.md`: cenários QA01-01 a QA01-17, entradas e resultados esperados.
- `tests/conftest.py`: fábrica de registros artificiais.
- `tests/contrato_qa.py`: lista independente dos 17 indicadores e anos esperados.
- `tests/test_qa02_indice.py`: testes do índice.
- `tests/test_qa02_comparacao.py`: comparação municipal, precisão, diferença e pares válidos.
- `tests/test_qa02_serie.py`: ordenação, lacunas e município histórico por ano.
- `evidencias/README.md`: registro da execução.
- `evidencias/qa01-qa02-junit.xml`: relatório JUnit gerado pelo pytest.
- `evidencias/execucao-qa01-qa02.txt`: log da execução em UTF-8.

## Backend utilizado

- Branch observada: `feature/SIE-30-school-municipality-analysis`.
- HEAD observado na execução: `7c43848` — `Merge pull request #11 from rbecamend/fix/BE-07-async-route-tests`.
- Commit mínimo solicitado pela equipe: `50ccd66` (PR #9).

**Verificação de commit concluída:** o backend foi testado na branch `feature/SIE-30-school-municipality-analysis`, no HEAD `7c43848` (`Merge pull request #11 from rbecamend/fix/BE-07-async-route-tests`). O comando `git merge-base --is-ancestor 50ccd66 HEAD` retornou código `0`, confirmando que o HEAD testado contém o commit mínimo `50ccd66`, que inclui o PR #9.

## Última execução registrada

- Data: 2026-10-16.
- Ambiente: Windows (`win32`), Python 3.12.2, pytest 9.1.1.
- Resultado: **19 testes aprovados; 0 falhas; 0 erros; 0 ignorados**.
- Duração: **5,38 segundos**.
- Código de saída: **0**.
- Distribuição: 7 testes de índice, 8 de comparação e 4 de série temporal.

Consulte [`evidencias/README.md`](evidencias/README.md) e os arquivos de log e JUnit gerados pela execução correspondente.

## Execução

Defina `LABES_API_ROOT` com o caminho da cópia Git atualizada do backend que contém `pyproject.toml` e a pasta `app`. A partir desta pasta `QA-01-QA-02`, execute:

```powershell
$env:PYTHONUTF8 = "1"
uv run --project "$env:LABES_API_ROOT" python -m pytest tests -v --junitxml=evidencias/qa01-qa02-junit.xml
```

Se atualizar os testes, regenere também o log e atualize os resultados documentados de acordo com a saída real.

## Limites

Esta suíte não chama a rota HTTP real, não usa dump/warehouse e não valida a interface. QA-03 e QA-04 permanecem fora deste escopo.
