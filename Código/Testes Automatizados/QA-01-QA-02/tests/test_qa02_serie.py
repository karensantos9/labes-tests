
"""QA-02: testes independentes da série temporal."""

import pytest

from app.domain.infraestrutura import (
    calcular_serie_comparacao_infraestrutura,
)
from app.schemas.infraestrutura import ComparacaoInfraestruturaResponse
from app.services.infraestrutura_service import (
    ANOS_COMPARACAO,
    InfraestruturaService,
)
from contrato_qa import INDICADORES_ESPERADOS


class RepositorioComparacaoFake:
    """Simula o repositório sem conexão com o banco de dados."""

    def __init__(
        self,
        *,
        identificacao,
        historico=None,
        pares=None,
    ):
        self.identificacao = identificacao
        self.historico = historico or []
        self.pares = pares or {}

        self.anos_consultados = None
        self.chamadas_pares = []

    async def find_identificacao_escola(self, *, co_entidade):
        return self.identificacao

    async def find_historico_escola(
        self,
        *,
        co_entidade,
        anos_comparaveis,
    ):
        self.anos_consultados = anos_comparaveis
        return self.historico

    async def find_pares_municipais(
        self,
        *,
        co_entidade_excluida,
        co_municipio,
        ano,
    ):
        self.chamadas_pares.append(
            {
                "co_entidade_excluida": co_entidade_excluida,
                "co_municipio": co_municipio,
                "ano": ano,
            }
        )

        return self.pares.get((co_municipio, ano), [])


def criar_identificacao():
    """Metadados fictícios da escola consultada."""

    return {
        "co_entidade": 15012345,
        "no_entidade": "Escola de teste QA",
        "co_municipio": 1501402,
        "no_municipio": "Belém",
    }


def test_dominio_ordena_registros_por_ano(registro_factory):
    """O domínio deve ordenar os registros existentes em ordem crescente."""

    escola_2025 = registro_factory(
        15012345, [1] * 17, ano=2025
    )
    escola_2022 = registro_factory(
        15012345, [1] * 17, ano=2022
    )
    escola_2024 = registro_factory(
        15012345, [1] * 17, ano=2024
    )

    serie = calcular_serie_comparacao_infraestrutura(
        [escola_2025, escola_2022, escola_2024],
        [],
        indicadores_esperados=INDICADORES_ESPERADOS,
        cobertura_minima_percentual=None,
    )

    # A função de domínio ordena os registros fornecidos.
    # Ela não deve ser confundida com a etapa do serviço
    # que cria os pontos dos anos ausentes.
    assert [ponto.ano for ponto in serie] == [
        2022,
        2024,
        2025,
    ]

@pytest.mark.asyncio
async def test_servico_preserva_lacunas_e_registros_totalmente_nulos(
    registro_factory,
):
    """A série deve ter 2022–2025, mesmo com anos sem registro.

    2023 não possui registro da escola.
    2024 possui registro, mas seus 17 indicadores são nulos.
    """

    # Preparar registros propositalmente fora de ordem.
    escola_2024 = registro_factory(
        15012345,
        [None] * 17,
        ano=2024,
    )

    escola_2022 = registro_factory(
        15012345,
        [1] * 13 + [0] * 4,
        ano=2022,
    )

    # Em 2022, os índices das duas referências são 100% e 0%.
    referencia_2022_cem = registro_factory(
        15000001,
        [1] * 17,
        ano=2022,
    )

    referencia_2022_zero = registro_factory(
        15000002,
        [0] * 17,
        ano=2022,
    )

    # Em 2024, a escola selecionada não tem índice,
    # mas a referência municipal possui índice de 100%.
    referencia_2024_cem = registro_factory(
        15000003,
        [1] * 17,
        ano=2024,
    )

    repositorio = RepositorioComparacaoFake(
        identificacao=criar_identificacao(),
        historico=[
            escola_2024,
            escola_2022,
        ],
        pares={
            (1501402, 2022): [
                referencia_2022_cem,
                referencia_2022_zero,
            ],
            (1501402, 2024): [
                referencia_2024_cem,
            ],
        },
    )

    servico = InfraestruturaService(repositorio)

    envelope = await servico.build_comparacao_municipio(
        co_entidade=15012345,
    )

    # Validar também o contrato da resposta.
    resposta = ComparacaoInfraestruturaResponse.model_validate(envelope)
    serie = resposta.model_dump(mode="json")["data"]["serie"]

    # O serviço precisa entregar exatamente os quatro anos do MVP.
    assert [ponto["ano"] for ponto in serie] == [
        2022,
        2023,
        2024,
        2025,
    ]
    assert [ponto["ano"] for ponto in serie] == list(
        ANOS_COMPARACAO
    )

    # 2022: cálculo completo e correto.
    assert serie[0]["situacao"] == "disponivel"
    assert serie[0]["indice_escola_percentual"] == 76.47
    assert serie[0]["media_municipal_percentual"] == 50.0
    assert serie[0]["diferenca_pontos_percentuais"] == 26.47
    assert serie[0]["quantidade_pares_validos"] == 2

    # 2023: não existe registro da escola.
    assert serie[1]["situacao"] == "escola_sem_dados"
    assert serie[1]["indice_escola_percentual"] is None
    assert serie[1]["media_municipal_percentual"] is None
    assert serie[1]["diferenca_pontos_percentuais"] is None
    assert serie[1]["total_indicadores"] == 17

    # 2024: há registro, mas todos os indicadores são nulos.
    assert serie[2]["situacao"] == "escola_sem_dados"
    assert serie[2]["indice_escola_percentual"] is None
    assert serie[2]["quantidade_indicadores_validos"] == 0
    assert serie[2]["total_indicadores"] == 17

    # A média municipal ainda pode ser calculada em 2024.
    assert serie[2]["media_municipal_percentual"] == 100.0
    assert serie[2]["diferenca_pontos_percentuais"] is None
    assert serie[2]["quantidade_pares_validos"] == 1

    # 2025: também não existe registro da escola.
    assert serie[3]["situacao"] == "escola_sem_dados"
    assert serie[3]["indice_escola_percentual"] is None
    assert serie[3]["media_municipal_percentual"] is None
    assert serie[3]["diferenca_pontos_percentuais"] is None
    assert serie[3]["total_indicadores"] == 17

    # O serviço consulta o histórico usando os quatro anos do MVP.
    assert repositorio.anos_consultados == ANOS_COMPARACAO

    # A consulta dos pares acontece somente para anos com registros
    # da escola. O serviço gera as lacunas para 2023 e 2025.
    anos_consultados_pares = {
        chamada["ano"]
        for chamada in repositorio.chamadas_pares
    }

    assert anos_consultados_pares == {2022, 2024}

@pytest.mark.asyncio
async def test_servico_cria_quatro_pontos_sem_historico(
):
    """Uma escola identificada sem histórico deve ter quatro pontos vazios."""

    repositorio = RepositorioComparacaoFake(
        identificacao=criar_identificacao(),
        historico=[],
        pares={},
    )

    servico = InfraestruturaService(repositorio)

    envelope = await servico.build_comparacao_municipio(
        co_entidade=15012345,
    )

    resposta = ComparacaoInfraestruturaResponse.model_validate(envelope)
    serie = resposta.model_dump(mode="json")["data"]["serie"]

    assert [ponto["ano"] for ponto in serie] == [
        2022,
        2023,
        2024,
        2025,
    ]

    assert len(serie) == 4

    for ponto in serie:
        assert ponto["situacao"] == "escola_sem_dados"
        assert ponto["indice_escola_percentual"] is None
        assert ponto["media_municipal_percentual"] is None
        assert ponto["diferenca_pontos_percentuais"] is None
        assert ponto["total_indicadores"] == 17

    assert repositorio.chamadas_pares == []



@pytest.mark.asyncio
async def test_servico_consulta_municipio_historico_de_cada_ano(
    registro_factory,
):
    """Cada ano deve consultar os pares do município do registro daquele ano."""

    escola_2022 = registro_factory(
        15012345,
        [1] * 17,
        ano=2022,
        co_municipio=1501402,
        no_municipio="Belém",
    )
    escola_2024 = registro_factory(
        15012345,
        [1] * 17,
        ano=2024,
        co_municipio=1500800,
        no_municipio="Ananindeua",
    )

    referencia_2022 = registro_factory(
        15000001,
        [0] * 17,
        ano=2022,
        co_municipio=1501402,
        no_municipio="Belém",
    )
    referencia_2024 = registro_factory(
        15000002,
        [1] * 17,
        ano=2024,
        co_municipio=1500800,
        no_municipio="Ananindeua",
    )

    # A identificação mais recente aponta para Ananindeua, mas o registro
    # histórico de 2022 pertence a Belém.
    identificacao_mais_recente = {
        "co_entidade": 15012345,
        "no_entidade": "Escola de teste QA",
        "co_municipio": 1500800,
        "no_municipio": "Ananindeua",
    }

    repositorio = RepositorioComparacaoFake(
        identificacao=identificacao_mais_recente,
        historico=[escola_2024, escola_2022],
        pares={
            (1501402, 2022): [referencia_2022],
            (1500800, 2024): [referencia_2024],
        },
    )

    servico = InfraestruturaService(repositorio)
    envelope = await servico.build_comparacao_municipio(
        co_entidade=15012345,
    )

    resposta = ComparacaoInfraestruturaResponse.model_validate(envelope)
    serie = resposta.model_dump(mode="json")["data"]["serie"]

    # As chamadas devem combinar município e ano do registro histórico.
    consultas = {
        (chamada["ano"], chamada["co_municipio"])
        for chamada in repositorio.chamadas_pares
    }
    assert consultas == {
        (2022, 1501402),
        (2024, 1500800),
    }
    assert all(
        chamada["co_entidade_excluida"] == 15012345
        for chamada in repositorio.chamadas_pares
    )

    por_ano = {ponto["ano"]: ponto for ponto in serie}

    # 2022 usa as referências de Belém: média de 0%.
    assert por_ano[2022]["media_municipal_percentual"] == 0.0
    assert por_ano[2022]["diferenca_pontos_percentuais"] == 100.0
    assert por_ano[2022]["quantidade_pares_validos"] == 1

    # 2024 usa as referências de Ananindeua: média de 100%.
    assert por_ano[2024]["media_municipal_percentual"] == 100.0
    assert por_ano[2024]["diferenca_pontos_percentuais"] == 0.0
    assert por_ano[2024]["quantidade_pares_validos"] == 1
