
"""Configurações e fixtures compartilhadas pelos testes de QA."""

import os
import sys
from collections.abc import Mapping
from pathlib import Path

import pytest


# 1. Localizar a pasta do backend a partir da variável de ambiente.
api_root_text = os.environ.get("LABES_API_ROOT")

if not api_root_text:
    raise RuntimeError(
        "A variável LABES_API_ROOT não foi definida. "
        "Defina-a com o caminho da pasta extraída do backend."
    )

API_ROOT = Path(api_root_text).resolve()

# 2. Conferir se o caminho aponta para o projeto correto.
arquivo_dominio = API_ROOT / "app" / "domain" / "infraestrutura.py"

if not arquivo_dominio.is_file():
    raise RuntimeError(
        f"Backend não encontrado em {API_ROOT}. "
        "Confira a variável LABES_API_ROOT."
    )

# 3. Permitir que os testes importem o código do backend
#    e o contrato independente que está na pasta tests.
TESTS_DIR = Path(__file__).resolve().parent

for caminho in (str(API_ROOT), str(TESTS_DIR)):
    if caminho not in sys.path:
        sys.path.insert(0, caminho)


from app.domain.infraestrutura import InfraestruturaRegistroBruto
from contrato_qa import INDICADORES_ESPERADOS


@pytest.fixture
def registro_factory():
    """Cria registros artificiais de escolas para reutilizar nos testes.

    Aceita uma lista de exatamente 17 valores ou um dicionário parcial.
    No dicionário parcial, as chaves ausentes serão tratadas como nulas
    pela função de cálculo quando receber INDICADORES_ESPERADOS.
    """

    def criar(
        co_entidade: int,
        valores: list[int | None]
        | tuple[int | None, ...]
        | Mapping[str, int | None],
        *,
        ano: int = 2024,
        co_municipio: int = 1501402,
        no_entidade: str | None = None,
        no_municipio: str = "Belém",
    ) -> InfraestruturaRegistroBruto:

        # Permite construir um registro usando somente alguns indicadores.
        if isinstance(valores, Mapping):
            indicadores = dict(valores)

            desconhecidos = (
                set(indicadores) - set(INDICADORES_ESPERADOS)
            )

            if desconhecidos:
                raise ValueError(
                    f"Indicadores desconhecidos: {sorted(desconhecidos)}"
                )

        # Para uma lista, exige os 17 valores na ordem do contrato.
        else:
            lista_valores = list(valores)

            if len(lista_valores) != len(INDICADORES_ESPERADOS):
                raise ValueError(
                    "O registro deve conter exatamente 17 valores."
                )

            indicadores = dict(
                zip(
                    INDICADORES_ESPERADOS,
                    lista_valores,
                    strict=True,
                )
            )

        return InfraestruturaRegistroBruto(
            co_entidade=co_entidade,
            no_entidade=no_entidade or f"Escola {co_entidade}",
            co_municipio=co_municipio,
            no_municipio=no_municipio,
            nu_ano_censo=ano,
            indicadores=indicadores,
        )

    return criar
