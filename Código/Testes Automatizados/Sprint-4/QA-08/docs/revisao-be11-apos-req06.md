# Revisão de impacto — BE11 após REQ-06 revisada

## Conclusão

A REQ-06 revisada altera decisões que o rascunho BE11 anterior tratava de forma diferente. O documento BE11 deve ser atualizado antes de a API/FE implementar a comparação múltipla. Não há código BE11 executável para alterar nesta etapa; BE11 continua sendo descoberta.

## Pontos do BE11 que ficaram incompatíveis

### 1. Seção 3.3 — quantidade de linhas e referências

Rascunho anterior: `series` contém somente os alvos escolhidos e a referência municipal fica embutida em `referencia_territorial`; a referência não é uma série principal/auxiliar.

REQ-06 revisada: cada escola selecionada gera uma série complementar automática de referência municipal, sem consumir vaga do seletor manual. A referência deve ser desenhada como linha separada.

Ação: substituir essa decisão. A resposta BE11 precisa expor informação suficiente para o frontend renderizar a série automática independentemente da série da escola.

### 2. Seção 5 — exemplo da resposta

Rascunho anterior: o exemplo contém somente uma série para a escola e uma série para o município manual; a referência aparece apenas aninhada em cada ponto escolar.

REQ-06 revisada: em 1 escola + 2 municípios deve haver até 4 linhas; o exemplo de resposta precisa conter a série automática da referência como item independente.

Ação: revisar o envelope e o exemplo JSON. Avaliar um discriminador de origem/papel da série, por exemplo `alvo_manual` e `referencia_automatica`, e um identificador estável que associe a referência à escola de origem. Os nomes definitivos dos campos devem ser acordados por Backend/Frontend.

### 3. Seção 6 — semântica das séries

Rascunho anterior: referência municipal retorna em `referencia_territorial` e não é desenhada como linha independente.

REQ-06 revisada: a referência é uma série complementar; deve continuar mesmo quando o índice da escola estiver indisponível, caso a referência tenha dados válidos.

Ação: a resposta deve permitir que cada ponto da série automática seja calculado/consultado por município histórico e não dependa da disponibilidade do índice escolar naquele ano.

### 4. Seção 6.3 — coexistência e não deduplicação

Rascunho anterior: diz que a repetição semântica não é removida automaticamente, mas não especifica estilos, tooltip e as duas fórmulas.

REQ-06 revisada: se o município manual coincidir com a referência automática, as duas séries ficam visíveis. A automática exclui a escola-alvo; a manual representa a média geral global da rede. Valores equivalentes não podem levar à deduplicação; traços devem diferir e tooltip deve consolidar os valores.

Ação: documentar os dois identificadores/papéis de série, as fórmulas/universos (com DAD07), e os metadados necessários ao tooltip.

### 5. Seção 7 — lacunas e dados insuficientes

Rascunho anterior: lacuna interrompe somente a série afetada.

REQ-06 revisada: especifica que, quando o índice da escola está indisponível no ano, a referência municipal pode permanecer visível se tiver dados válidos; outras séries também continuam.

Ação: adicionar cenário explícito e garantir que a série de referência não seja derivada da existência do índice escolar.

### 6. Seção 12 — cenários de validação

Rascunho anterior: 1 escola + 2 municípios retorna exatamente 3 séries principais.

REQ-06 revisada: retorna até 4 linhas: escola, referência municipal automática e dois municípios manuais.

Ação: atualizar o cenário e incluir 3 escolas => até 6 linhas, 2 escolas + 1 município => até 5 linhas e 3 municípios => 3 linhas.

### 7. Novos aspectos não detalhados no rascunho

- limite total de 3 alvos manuais, independentemente de tipo;
- referências automáticas não consomem vagas manuais;
- até 6 linhas totais;
- remoção individual deve liberar uma vaga;
- `Limpar Filtros` retorna ao estado vazio;
- legenda dinâmica `Referência municipal da [Nome da Escola]`;
- tooltip deve informar o nome do município histórico de cada ano;
- linhas manual/automática com traços distintos (sólido/tracejado, conforme exemplo REQ-06);
- limiar de 60% é exclusivo do nível escolar;
- composição inferior mostra cada município como X de Y escolas.

## Contratos e decisões ainda pendentes

- DAD07: universo de escolas e fórmula da média geral global da rede para município manual, denominadores, cobertura e dados ausentes.
- BE11: códigos/status HTTP exatos. O rascunho propõe 422, 404, 500 e 503, mas a REQ-06 só exige erro HTTP específico; confirmar antes de transformar em assertiva obrigatória.
- Backend/Frontend: formato da série automática no JSON e associação com escola.
- Frontend: detalhes de estilo, legenda, tooltip e comportamento do gráfico.

## Código QA existente

Os testes QA06/BE10 não precisam ser alterados pela REQ-06 revisada. Eles verificam a composição municipal por indicador da escola-alvo e não implementam o comparador múltiplo. A regra de alerta de 60% permanece apenas para o nível escolar; não adicionar alerta às séries municipais.

A suíte QA08 deve permanecer em formato BDD/documentação até que BE11 e Frontend disponibilizem implementação executável.
