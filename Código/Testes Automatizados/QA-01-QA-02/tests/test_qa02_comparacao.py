
"""QA-02: testes independentes da comparação escola x município."""

import pytest

from app.domain.infraestrutura import (
    calcular_comparacao_infraestrutura_ano,
)
from contrato_qa import INDICADORES_ESPERADOS


def calcular_comparacao(
    escola,
    referencias,
    *,
    indicadores_esperados=INDICADORES_ESPERADOS,
):
    """Executa a função real do backend usando o contrato de QA.

    Permite restringir indicadores em cenários matemáticos de precisão,
    como 2/3 e 1/3, sem alterar a fixture geral de 17 indicadores.
    """

    return calcular_comparacao_infraestrutura_ano(
        escola,
        referencias,
        indicadores_esperados=indicadores_esperados,
        cobertura_minima_percentual=None,
    )


def test_comparacao_exclui_escola_selecionada_e_filtra_referencias(
    registro_factory,
):
    """Só entram na média escolas diferentes da selecionada,
    pertencentes ao mesmo município e ao mesmo ano.
    """

    escola = registro_factory(
        15012345,
        [1] * 10 + [0] * 7,
        ano=2024,
    )

    referencia_zero = registro_factory(
        15000001,
        [0] * 17,
        ano=2024,
    )

    referencia_cem = registro_factory(
        15000002,
        [1] * 17,
        ano=2024,
    )

    outro_municipio = registro_factory(
        15000003,
        [1] * 17,
        ano=2024,
        co_municipio=9999999,
    )

    outro_ano = registro_factory(
        15000004,
        [1] * 17,
        ano=2023,
    )

    # Incluímos propositalmente a própria escola na lista.
    # A função deve excluí-la da comparação.
    referencias = [
        escola,
        referencia_zero,
        referencia_cem,
        outro_municipio,
        outro_ano,
    ]

    resultado = calcular_comparacao(escola, referencias)

    assert resultado.situacao == "disponivel"

    assert resultado.indice_escola_percentual == 58.82
    assert resultado.quantidade_indicadores_presentes == 10
    assert resultado.quantidade_indicadores_validos == 17
    assert resultado.total_indicadores == 17

    assert resultado.media_municipal_percentual == 50.0
    assert resultado.diferenca_pontos_percentuais == 8.82

    assert resultado.quantidade_pares_validos == 2
    assert resultado.denominador_pares == 2
    assert resultado.cobertura_pares_percentual == 100.0


def test_media_municipal_simples_pesa_cada_escola_igualmente(
    registro_factory,
):
    """A média é dos índices das escolas, não dos indicadores agrupados."""

    escola = registro_factory(
        15012345,
        [1] * 17,
        ano=2024,
    )

    referencia_zero = registro_factory(
        15000001,
        [0] * 17,
        ano=2024,
    )

    # Apenas um indicador válido: índice de 100%.
    referencia_cem_com_baixa_cobertura = registro_factory(
        15000002,
        [1] + [None] * 16,
        ano=2024,
    )

    resultado = calcular_comparacao(
        escola,
        [referencia_zero, referencia_cem_com_baixa_cobertura],
    )

    # Média aritmética simples: (0 + 100) / 2 = 50%.
    assert resultado.media_municipal_percentual == 50.0

    # A escola selecionada tem índice de 100%.
    assert resultado.indice_escola_percentual == 100.0

    # Diferença expressa em pontos percentuais.
    assert resultado.diferenca_pontos_percentuais == 50.0

    assert resultado.quantidade_pares_validos == 2
    assert resultado.denominador_pares == 2
    assert resultado.cobertura_pares_percentual == 100.0


def test_municipio_sem_outras_escolas(registro_factory):
    """Sem referências, não há média nem diferença municipal."""

    escola = registro_factory(
        15012345,
        [1] * 17,
        ano=2024,
    )

    resultado = calcular_comparacao(escola, [])

    assert resultado.situacao == "sem_pares_municipio"

    assert resultado.indice_escola_percentual == 100.0

    assert resultado.quantidade_pares_validos == 0
    assert resultado.denominador_pares == 0

    assert resultado.cobertura_pares_percentual is None
    assert resultado.media_municipal_percentual is None
    assert resultado.diferenca_pontos_percentuais is None


def test_municipio_com_escolas_mas_sem_pares_validos(
    registro_factory,
):
    """Referências existentes com todos os indicadores nulos
    não podem produzir uma média municipal.
    """

    escola = registro_factory(
        15012345,
        [1] * 17,
        ano=2024,
    )

    referencia_sem_dados_a = registro_factory(
        15000001,
        [None] * 17,
        ano=2024,
    )

    referencia_sem_dados_b = registro_factory(
        15000002,
        [None] * 17,
        ano=2024,
    )

    resultado = calcular_comparacao(
        escola,
        [referencia_sem_dados_a, referencia_sem_dados_b],
    )

    assert resultado.situacao == "sem_pares_validos"

    assert resultado.indice_escola_percentual == 100.0

    assert resultado.quantidade_pares_validos == 0
    assert resultado.denominador_pares == 2
    assert resultado.cobertura_pares_percentual == 0.0

    assert resultado.media_municipal_percentual is None
    assert resultado.diferenca_pontos_percentuais is None


def test_escola_sem_dados_pode_ter_media_municipal_valida(
    registro_factory,
):
    """O índice da escola pode ser nulo mesmo com pares válidos."""

    escola = registro_factory(
        15012345,
        [None] * 17,
        ano=2024,
    )

    referencia = registro_factory(
        15000001,
        [1] * 17,
        ano=2024,
    )

    resultado = calcular_comparacao(escola, [referencia])

    assert resultado.situacao == "escola_sem_dados"

    assert resultado.indice_escola_percentual is None
    assert resultado.diferenca_pontos_percentuais is None

    # A média dos pares continua sendo calculável.
    assert resultado.media_municipal_percentual == 100.0

    assert resultado.quantidade_pares_validos == 1
    assert resultado.denominador_pares == 1
    assert resultado.cobertura_pares_percentual == 100.0



def test_comparacao_com_uma_unica_referencia_valida(registro_factory):
    """Uma única referência válida determina a média municipal."""

    escola = registro_factory(
        15012345,
        [1] * 10 + [0] * 7,
        ano=2024,
    )
    referencia = registro_factory(
        15000001,
        [1] * 17,
        ano=2024,
    )

    resultado = calcular_comparacao(escola, [referencia])

    assert resultado.situacao == "disponivel"
    assert resultado.indice_escola_percentual == 58.82
    assert resultado.media_municipal_percentual == 100.0
    assert resultado.diferenca_pontos_percentuais == -41.18
    assert resultado.quantidade_pares_validos == 1
    assert resultado.denominador_pares == 1
    assert resultado.cobertura_pares_percentual == 100.0


def test_diferenca_calculada_com_valores_exatos_antes_do_arredondamento(
    registro_factory,
):
    """A diferença usa os índices exatos antes de arredondar o resultado."""

    indicadores_tres = INDICADORES_ESPERADOS[:3]

    escola = registro_factory(
        15012345,
        [1, 1, 0] + [None] * 14,
        ano=2024,
    )
    referencia = registro_factory(
        15000001,
        [1, 0, 0] + [None] * 14,
        ano=2024,
    )

    resultado = calcular_comparacao(
        escola,
        [referencia],
        indicadores_esperados=indicadores_tres,
    )

    # Escola: 2/3 = 66,666...%; referência: 1/3 = 33,333...%.
    assert resultado.indice_escola_percentual == 66.67
    assert resultado.media_municipal_percentual == 33.33
    # 2/3 - 1/3 = 1/3 = 33,333... p.p.; não 66,67 - 33,33 = 33,34.
    assert resultado.diferenca_pontos_percentuais == 33.33
    assert resultado.quantidade_pares_validos == 1
    assert resultado.denominador_pares == 1


def test_media_municipal_calculada_com_valores_exatos_antes_do_arredondamento(
    registro_factory,
):
    """A média usa o índice exato dos pares antes de arredondar."""

    indicadores_tres = INDICADORES_ESPERADOS[:3]

    escola = registro_factory(
        15012345,
        [1, 1, 1] + [None] * 14,
        ano=2024,
    )
    referencia_zero = registro_factory(
        15000001,
        [0, 0, 0] + [None] * 14,
        ano=2024,
    )
    referencia_dois_tercos = registro_factory(
        15000002,
        [1, 1, 0] + [None] * 14,
        ano=2024,
    )

    resultado = calcular_comparacao(
        escola,
        [referencia_zero, referencia_dois_tercos],
        indicadores_esperados=indicadores_tres,
    )

    # Média exata: (0 + 200/3) / 2 = 100/3 = 33,333...%.
    assert resultado.indice_escola_percentual == 100.0
    assert resultado.media_municipal_percentual == 33.33
    assert resultado.diferenca_pontos_percentuais == 66.67
    assert resultado.quantidade_pares_validos == 2
    assert resultado.denominador_pares == 2
    assert resultado.cobertura_pares_percentual == 100.0
