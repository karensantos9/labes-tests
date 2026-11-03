# QA08 — Cenários BDD baseados na REQ-06 revisada.
# Não executável até a implementação do frontend e do contrato BE11.

Feature: Comparação múltipla de escolas e municípios
  Como usuário do SIE V2
  Quero selecionar escolas e municípios simultaneamente
  Para comparar séries independentes sem misturar referências territoriais.

  Background:
    Given o período de análise é de 2022 a 2025

  @selecao @limite
  Scenario Outline: Permitir no máximo três alvos manuais em qualquer combinação
    Given que o usuário selecionou manualmente <escolas> escolas e <municipios> municípios
    And a quantidade total de alvos manuais é 3
    When tentar selecionar mais um alvo manual
    Then a seleção de novos itens deve estar desativada
    And os três alvos já selecionados devem ser preservados

    Examples:
      | escolas | municipios |
      | 3       | 0          |
      | 2       | 1          |
      | 1       | 2          |
      | 0       | 3          |

  @selecao @remocao
  Scenario: Remover um alvo individual libera uma vaga manual
    Given que existem três alvos manuais selecionados
    When o usuário remove individualmente um dos alvos
    Then os outros dois alvos devem permanecer selecionados
    And uma vaga manual deve ficar disponível

  @selecao @limpar-filtros
  Scenario: Limpar Filtros remove toda a seleção manual
    Given que existem alvos manuais selecionados
    When o usuário aciona "Limpar Filtros"
    Then todos os alvos manuais devem ser removidos
    And o painel deve retornar ao estado vazio inicial do MVP

  @grafico @selecao-mista
  Scenario: Uma escola e dois municípios geram até quatro linhas
    Given que o usuário selecionou manualmente uma escola e dois municípios
    When o gráfico for renderizado
    Then devem existir até quatro séries independentes
    And devem estar representadas a escola-alvo, sua referência municipal automática e os dois municípios manuais
    And não deve existir uma média combinada entre os municípios

  @grafico @limite
  Scenario: Três escolas podem gerar até seis linhas
    Given que o usuário selecionou manualmente três escolas
    When cada escola possuir referência municipal histórica disponível
    And o gráfico for renderizado
    Then devem existir até seis linhas independentes
    And cada referência municipal deve estar associada à respectiva escola
    And as referências automáticas não devem consumir vagas do seletor manual

  @grafico @municipios
  Scenario: Três municípios selecionados geram três séries municipais
    Given que o usuário selecionou manualmente três municípios
    When o gráfico for renderizado
    Then devem existir três séries municipais independentes
    And não deve existir uma quarta série de média combinada

  @grafico @coexistencia @mesmo-municipio
  Scenario: Município manual e referência automática do mesmo território permanecem separados
    Given que o usuário selecionou uma escola de Belém
    And selecionou manualmente o município de Belém
    When o gráfico for renderizado
    Then devem existir duas séries municipais distintas
    And a referência automática deve excluir individualmente a escola-alvo
    And o município manual deve representar a média geral da rede conforme a regra metodológica aprovada
    And uma série não deve ser deduplicada por possuir o mesmo código municipal da outra

  @grafico @estilo @tooltip
  Scenario: Séries equivalentes mantêm estilos e valores distintos no tooltip
    Given que a referência automática e o município manual possuem valores numéricos equivalentes em um ano
    When o usuário posicionar o cursor sobre o ponto do gráfico
    Then as duas séries devem continuar individualmente identificáveis
    And devem utilizar estilos de traço distintos
    And o tooltip deve apresentar os valores consolidados de ambas as séries

  @legenda @historico
  Scenario: Legenda identifica dinamicamente a referência municipal da escola
    Given que uma escola possui mudança de município entre anos históricos
    When o gráfico for renderizado e o usuário consultar um ponto anual
    Then a série de referência deve ser identificada como "Referência municipal da [Nome da Escola]"
    And o tooltip deve apresentar o nome exato do município correspondente àquele ano

  @dados-insuficientes @lacuna
  Scenario: Índice escolar indisponível não oculta referência municipal válida
    Given que a escola selecionada não possui índice calculável em 2024
    And a referência municipal possui dados válidos em 2024
    And existem outros alvos com dados válidos
    When o gráfico for renderizado
    Then o ponto de 2024 da série da escola deve ser NULL e produzir uma lacuna no traçado
    And a série da referência municipal deve permanecer visível em 2024
    And as demais séries devem continuar sendo renderizadas normalmente

  @estado-vazio
  Scenario: Painel sem filtros apresenta estado inicial do MVP
    Given que nenhum alvo manual está selecionado
    When o usuário acessa o painel
    Then deve ser exibido o estado vazio inicial definido para o MVP

  @erros @requisicao
  Scenario: Falha de requisição permite nova tentativa
    Given que existem alvos selecionados
    When a requisição de comparação múltipla falhar
    Then a interface deve apresentar um aviso de erro
    And deve permitir que o usuário tente novamente

  @erros @codigo-invalido
  Scenario: Código de alvo inválido apresenta erro específico
    Given que o usuário tenta consultar um alvo com código inválido
    When a requisição for processada
    Then o backend deve retornar o erro HTTP específico definido no contrato aprovado
    And a interface deve apresentar um aviso de erro
    And deve permitir nova tentativa após a correção da seleção

  @composicao
  Scenario: Composição inferior individualiza cada município selecionado
    Given que mais de um município está selecionado manualmente
    When o usuário visualizar a tabela inferior de composição
    Then cada município deve possuir seu próprio detalhamento percentual
    And cada indicador deve apresentar a relação "X de Y escolas" conforme o contrato
    And os resultados de municípios diferentes não devem ser agregados em uma linha única

  @cobertura
  Scenario: Limiar de 60 por cento aplica-se exclusivamente ao nível escolar
    Given que a comparação múltipla contém escolas e municípios
    When as coberturas forem avaliadas
    Then o alerta de cobertura de 60 por cento deve ser aplicado somente à escola-alvo
    And não deve ser aplicado automaticamente às séries de municípios ou referências municipais
    And a baixa cobertura não deve bloquear a exibição dos resultados
