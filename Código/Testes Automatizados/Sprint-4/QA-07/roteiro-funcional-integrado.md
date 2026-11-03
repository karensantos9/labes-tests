# Roteiro funcional integrado — QA07 | Sprint 4 | SIE V2

**Estado:** preparado; não executado. Executar somente após API e frontend estarem integrados no ambiente de QA.

## Matriz de cenários

| ID | Cenário | Passos essenciais | Resultado esperado | Evidência |
|---|---|---|---|---|
| QA07-01 | Carregamento normal | Abrir o painel e selecionar escola com histórico. | Metadados, série temporal e composição são carregados e correspondem ao payload. | Captura de tela + request/response |
| QA07-02 | Selecionar e limpar escola | Selecionar escola; em seguida acionar a limpeza do filtro. | Seleção aplicada e estado inicial restaurado sem dados residuais. | Capturas antes/depois |
| QA07-03 | Composição detalhada | Conferir os 17 indicadores no painel de composição. | Presentes, válidos, sem informação e percentuais correspondem à API. | Captura + conferência manual |
| QA07-04 | Baixa cobertura | Selecionar escola com cobertura inferior ao limiar confirmado. | Resultado continua visível e aviso informativo aparece, sem bloqueio. | Captura + payload |
| QA07-05 | NULL / sem dados | Consultar escola com indicadores todos nulos em um ano. | NULL não é convertido em zero; composição e série representam ausência de dados. | Captura + payload |
| QA07-06 | Sem histórico x inexistente | Consultar escola existente sem histórico e identificador inexistente. | Estados/mensagens diferentes, conforme contrato. | Capturas + respostas HTTP |
| QA07-07 | Município histórico | Consultar escola que muda de município ao longo do período. | Cada ano usa o município do registro histórico daquele ano. | Captura + payload |
| QA07-08 | Legenda e tooltip | Passar o cursor sobre pontos/séries do gráfico. | Rótulos identificam entidade, município e ano; valores correspondem ao payload. | Capturas |
| QA07-09 | Erro de requisição | Simular falha de rede/servidor em ambiente de teste. | Mensagem clara e possibilidade de tentar novamente. | Captura + log |
| QA07-10 | Regressão | Reexecutar cenários críticos após correções. | Fluxos anteriormente aprovados continuam funcionando. | Relatório de reteste |

## Registro obrigatório por cenário

- ID e título do cenário;
- ambiente, data/hora, navegador e versão;
- commit/versão do backend e frontend;
- massa de dados/identificadores usados;
- pré-condições e passos executados;
- resultado esperado e observado;
- status: aprovado, reprovado, bloqueado ou não executado;
- captura, request/response, log e defeito vinculado.

## Critério de encerramento

Não marcar QA07 como concluída enquanto os cenários aplicáveis não tiverem sido executados no ambiente integrado, defeitos relevantes estiverem registrados e retestes estiverem documentados.
