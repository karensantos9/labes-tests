# QA-01 e QA-02 — Análise Temporal Escola × Município

## Objetivo

Preparar fixtures calculáveis e executar testes independentes das regras matemáticas da análise temporal Escola × Município para o MVP da Sprint 3.

Este conjunto de testes é mantido no repositório `labes-tests` e utiliza as funções do backend disponibilizadas pela variável de ambiente `LABES_API_ROOT`. A suíte não exige iniciar a API nem conectar ao banco de dados.

## Escopo

- **QA-01:** documentar cenários de teste, dados artificiais e resultados esperados conferidos manualmente.
- **QA-02:** automatizar as regras de cálculo do índice, comparação municipal e série temporal.
- Anos da série histórica: 2022, 2023, 2024 e 2025.
- Indicadores esperados: 17.
- Valores usados nos dados de teste: `1` (Sim), `0` (Não) e `None` (NULL).
- NULL não é convertido em zero e fica fora do denominador.
- Não há cobertura mínima obrigatória neste MVP.
- A média municipal é a média aritmética simples dos índices válidos das outras escolas do mesmo município e ano, excluindo a escola selecionada.
- A diferença é expressa em pontos percentuais (p.p.).
- A série deve preservar os anos sem registro, com os campos de índice/diferença nulos quando aplicável.

## Estrutura

- `fixtures/matriz-qa01.md`: cenários, entradas e resultados esperados.
- `tests/conftest.py`: configuração e fábrica de registros artificiais.
- `tests/contrato_qa.py`: lista independente dos indicadores e anos esperados.
- `tests/test_qa02_indice.py`: testes do índice da escola.
- `tests/test_qa02_comparacao.py`: testes de média municipal, pares e diferença.
- `tests/test_qa02_serie.py`: testes de ordenação e lacunas temporais.
- `evidencias/README.md`: registro da execução.
- `evidencias/qa01-qa02-junit.xml`: relatório JUnit da execução registrada.
- `evidencias/execucao-qa01-qa02.txt`: log detalhado, caso gerado na execução.

## Preparar e executar no PowerShell

Defina `LABES_API_ROOT` com o caminho da pasta extraída do projeto `labes-api` que contém `pyproject.toml` e a pasta `app`. Não use o caminho do arquivo `.zip`.

Exemplo — ajuste o caminho ao local em que o backend foi extraído:

```powershell
$env:LABES_API_ROOT = "C:\Users\karen\Downloads\labes-api-extraido\labes-api-feature-SIE-30-school-municipality-analysis"

$qaRoot = Join-Path (Get-Location).Path "Código\Testes Automatizados\QA-01-QA-02"
$testsDir = Join-Path $qaRoot "tests"
$evidenceDir = Join-Path $qaRoot "evidencias"
$junitPath = Join-Path $evidenceDir "qa01-qa02-junit.xml"

uv run --project "$env:LABES_API_ROOT" python -m pytest `
    "$testsDir" -v "--junitxml=$junitPath"
```

Execute o comando a partir da raiz do repositório `labes-tests`. O ambiente Python gerenciado por `uv` deve ter as dependências do backend instaladas.

## Última execução registrada

- Resultado: **16 testes aprovados**.
- Duração: **0,83 segundo**.
- Código de saída: **0**.
- Escopo: testes independentes de QA-01/QA-02.

Detalhes e evidências: consulte [`evidencias/README.md`](evidencias/README.md).

## Fora do escopo desta suíte

Esta suíte não substitui os testes HTTP da QA-03 nem os testes visuais/funcionais do frontend da QA-04. Essas etapas dependem da rota e da integração executável previstas pela equipe.
