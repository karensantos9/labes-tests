# QA08 — Comparação múltipla (REQ-06 revisada)

## Estado

Preparação de cenários BDD e matriz de testes a partir da REQ-06 revisada em 02/11/2026.
A REQ-06 é uma história de descoberta: esta entrega não representa testes automatizados executáveis nem validação de uma interface/endpoint ainda não implementados.

## Fonte de verdade

- REQ-06 revisada fornecida pela equipe de Requisitos.
- BE11 é uma proposta de contrato e precisa ser alinhada à REQ-06 revisada antes da implementação.

## Regra central de seleção e linhas

- O usuário pode selecionar até 3 alvos manuais no total, somando escolas e municípios.
- Cada escola selecionada gera uma série automática adicional de referência municipal. Essa série não consome vaga manual.
- Quantidade de linhas do gráfico = quantidade de alvos manuais + quantidade de escolas selecionadas, limitado a 6.
- Exemplos: 3 municípios = 3 linhas; 1 escola + 2 municípios = 4 linhas; 2 escolas + 1 município = 5 linhas; 3 escolas = 6 linhas.
- Uma referência automática e um município selecionado manualmente devem continuar como séries distintas, inclusive quando representam o mesmo município e têm valores iguais.
- Referência automática: traço distinto (REQ-06 exemplifica tracejado); seleção manual: traço distinto (REQ-06 exemplifica sólido).
- A média combinada entre municípios diferentes é proibida.

## Conteúdo

- `features/qa08-comparacao-multipla.feature`: cenários BDD em Gherkin para futura automação.
- `fixtures/matriz-qa08-req06-revisada.md`: cenários, resultados e camada de validação.
- `fixtures/combinacoes-linhas.json`: exemplos de seleção e quantidade esperada de linhas.
- `docs/revisao-be11-apos-req06.md`: pontos do rascunho BE11 que precisam ser atualizados.

## O que pode ser feito agora

- Revisar a matriz com Requisitos, Backend, Frontend, Dados e QA.
- Confirmar os cenários de limite, coexistência de linhas e lacunas.
- Solicitar atualização do BE11 para que o contrato represente as séries de referência automáticas separadamente.
- Manter os cenários como BDD planejado até existir implementação de BE11/Frontend.

## O que ainda não pode ser marcado como aprovado

- Bloqueio real do quarto alvo no seletor.
- Remoção individual e limpeza global executadas na interface.
- Número real de linhas renderizadas.
- Traços, legenda e tooltip exibidos na tela.
- Continuidade das demais séries durante uma lacuna.
- Composição inferior por município.
- Códigos HTTP efetivamente devolvidos pelo endpoint.

## Observações

Os testes QA06/BE10 não precisam ser alterados por esta revisão da REQ-06. A regra de cobertura de 60% aplica-se exclusivamente ao nível escolar, e os testes QA06 existentes verificam o cálculo/cobertura, sem atribuir alerta à agregação municipal.
