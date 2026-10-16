# Evidências de execução — QA-01 e QA-02

## Execução mais recente informada

| Campo | Resultado |
|---|---|
| Data | 2026-10-16 |
| Sistema | Windows (`win32`) |
| Python | 3.12.2 |
| pytest | 9.1.1 |
| Branch do backend | `feature/SIE-30-school-municipality-analysis` |
| HEAD do backend informado | `7c43848` — merge PR #11 (`fix/BE-07-async-route-tests`) |
| Commit mínimo exigido pela equipe | `50ccd66` (PR #9), confirmado como ancestral do HEAD testado |
| Testes coletados | 19 |
| Testes aprovados | **19** |
| Falhas | **0** |
| Erros | **0** |
| Ignorados | **0** |
| Duração | **5,38 segundos** |
| Código de saída | **0** |
| Resultado geral | **Suíte aprovada** |

A saída real do pytest informou:

```text
============================= test session starts =============================
platform win32 -- Python 3.12.2, pytest-9.1.1
collected 19 items
============================= 19 passed in 5.38s =============================
Código de saída: 0
```

## Distribuição dos testes

| Arquivo | Testes aprovados |
|---|---:|
| `test_qa02_indice.py` | 7 |
| `test_qa02_comparacao.py` | 8 |
| `test_qa02_serie.py` | 4 |
| **Total** | **19** |

## Cenários novos validados

- **QA01-15:** diferença calculada com valores exatos antes do arredondamento; 2/3 − 1/3 deve resultar em 33,33 p.p., não 33,34.
- **QA01-16:** média calculada com valores exatos antes do arredondamento; média de 0% e 2/3 deve resultar em 33,33%, não 33,34%.
- **QA01-17:** consulta dos pares por município histórico de cada ano (2022 e 2024).

## Regras cobertas

- Índice = 100 × indicadores presentes (`Sim`) ÷ indicadores válidos.
- `Não` permanece no denominador como zero; NULL fica fora do denominador.
- Índice nulo quando nenhum indicador é válido.
- Indicadores ausentes tratados conforme o contrato esperado de 17 indicadores.
- Exclusão da escola selecionada e filtro por município/ano.
- Média aritmética simples, calculada sem arredondamento intermediário.
- Diferença em pontos percentuais, calculada sem arredondamento intermediário.
- Quantidade, denominador e cobertura dos pares válidos.
- Município sem outras escolas versus município com escolas sem índices válidos.
- Escola selecionada sem dados, mas com média municipal calculável.
- Ordenação e preservação dos anos 2022–2025.
- Distinção entre ano sem registro e registro com todos os indicadores nulos.
- Consulta do município associado ao registro histórico de cada ano.

## Arquivos de evidência

- `qa01-qa02-junit.xml`: regenerado pelo pytest na execução de 19 testes.
- `execucao-qa01-qa02.txt`: deve conter o log em UTF-8, com o nome de pasta legível como `Código`.

## Verificação do commit do backend

**Confirmação realizada:** no backend em HEAD `7c43848`, o comando `git -C "$env:LABES_API_ROOT" merge-base --is-ancestor 50ccd66 HEAD` retornou código `0`. Portanto, o backend testado contém o commit mínimo `50ccd66` exigido pela equipe.

## Limites de escopo

Esta evidência cobre somente QA-01 e QA-02 e não comprova a validação da rota HTTP real (QA-03), integração com o frontend (QA-04) nem homologação oficial da metodologia provisória.
