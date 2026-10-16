
"""QA-02: testes independentes do índice de infraestrutura."""

from app.domain.infraestrutura import calcular_indice_infraestrutura
from contrato_qa import INDICADORES_ESPERADOS


def calcular(escola):
    """Executa o cálculo real do backend com o contrato de QA."""

    return calcular_indice_infraestrutura(
        escola.indicadores,
        indicadores_esperados=INDICADORES_ESPERADOS,
        cobertura_minima_percentual=None,
    )


def test_indice_registro_completo_com_17_indicadores(registro_factory):
    """Dez Sim e sete Não devem resultar em 58,82%."""

    valores = [1] * 10 + [0] * 7
    escola = registro_factory(15012345, valores)

    resultado = calcular(escola)

    assert resultado.percentual == 58.82
    assert resultado.presentes == 10
    assert resultado.validos == 17
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 100.0


def test_indice_registro_parcial_exclui_nulos(registro_factory):
    """Os dez nulos ficam fora do denominador."""

    valores = [1] * 5 + [0] * 2 + [None] * 10
    escola = registro_factory(15012345, valores)

    resultado = calcular(escola)

    assert resultado.percentual == 71.43
    assert resultado.presentes == 5
    assert resultado.validos == 7
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 41.18


def test_indice_sim_com_demais_indicadores_nulos(registro_factory):
    """Um Sim válido e dezesseis nulos devem resultar em 100%."""

    valores = [1] + [None] * 16
    escola = registro_factory(15012345, valores)

    resultado = calcular(escola)

    assert resultado.percentual == 100.0
    assert resultado.presentes == 1
    assert resultado.validos == 1
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 5.88


def test_indice_nao_com_demais_indicadores_nulos(registro_factory):
    """Um Não válido e dezesseis nulos devem resultar em 0%."""

    valores = [0] + [None] * 16
    escola = registro_factory(15012345, valores)

    resultado = calcular(escola)

    assert resultado.percentual == 0.0
    assert resultado.presentes == 0
    assert resultado.validos == 1
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 5.88


def test_indice_todos_zero_e_valido(registro_factory):
    """Dezessete Não representam índice válido de 0%, não ausência de dados."""

    escola = registro_factory(15012345, [0] * 17)

    resultado = calcular(escola)

    assert resultado.percentual == 0.0
    assert resultado.presentes == 0
    assert resultado.validos == 17
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 100.0


def test_indice_todos_nulos_retorna_none(registro_factory):
    """Sem indicadores válidos, o índice precisa ser nulo."""

    escola = registro_factory(15012345, [None] * 17)

    resultado = calcular(escola)

    assert resultado.percentual is None
    assert resultado.presentes == 0
    assert resultado.validos == 0
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 0.0


def test_indicadores_ausentes_sao_tratados_como_nulos(registro_factory):
    """Um dicionário parcial não deve reduzir o total esperado de 17."""

    valores = {
        INDICADORES_ESPERADOS[0]: 1,
        INDICADORES_ESPERADOS[1]: 0,
    }
    escola = registro_factory(15012345, valores)

    resultado = calcular(escola)

    assert resultado.percentual == 50.0
    assert resultado.presentes == 1
    assert resultado.validos == 2
    assert resultado.total_indicadores == 17
    assert resultado.cobertura_indicadores_percentual == 11.76
