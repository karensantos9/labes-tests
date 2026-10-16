"""Contrato independente de indicadores e anos esperado pelo QA."""

ANOS_ESPERADOS = (2022, 2023, 2024, 2025)

INDICADORES_ESPERADOS = (
    "in_agua_potavel",
    "in_energia_rede_publica",
    "in_esgoto_rede_publica",
    "in_lixo_servico_coleta",
    "in_banheiro",
    "in_banheiro_pne",
    "in_biblioteca",
    "in_sala_leitura",
    "in_laboratorio_ciencias",
    "in_laboratorio_informatica",
    "in_sala_multiuso",
    "in_sala_atendimento_especial",
    "in_cozinha",
    "in_refeitorio",
    "in_quadra_esportes",
    "in_patio_coberto",
    "in_auditorio",
)

assert len(INDICADORES_ESPERADOS) == 17
assert len(set(INDICADORES_ESPERADOS)) == 17
