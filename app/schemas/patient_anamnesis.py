from typing import Optional
from uuid import UUID
from app.schemas.base import CoreModel, BaseEntitySchema


class AnamnesisBase(CoreModel):
    has_diabetes: Optional[bool] = False
    has_hipertensao: Optional[bool] = False
    has_cardiopatia: Optional[bool] = False
    has_epilepsia: Optional[bool] = False
    has_tireoide: Optional[bool] = False
    has_doenca_renal: Optional[bool] = False
    has_autoimune: Optional[bool] = False
    outras_doencas: Optional[str] = None
    alergias_medicamentos: Optional[str] = None
    outras_alergias: Optional[str] = None
    familiar_diabetes: Optional[bool] = False
    familiar_hipertensao: Optional[bool] = False
    familiar_gemelaridade: Optional[bool] = False
    familiar_malformacoes: Optional[bool] = False
    outros_familiares: Optional[str] = None
    tabagismo: Optional[bool] = False
    tabagismo_cigarros_dia: Optional[int] = None
    alcool: Optional[bool] = False
    alcool_frequencia: Optional[str] = None
    drogas_ilicitas: Optional[bool] = False
    atividade_fisica: Optional[bool] = False
    atividade_fisica_descricao: Optional[str] = None
    pre_eclampsia_anterior: Optional[bool] = False
    diabetes_gestacional_anterior: Optional[bool] = False
    perda_fetal_anterior: Optional[bool] = False
    prematuridade_anterior: Optional[bool] = False
    intercorrencias_anteriores: Optional[str] = None

    # GESTA
    gesta: Optional[int] = None
    para: Optional[int] = None
    abortos: Optional[int] = None
    tipo_parto_anterior: Optional[str] = None

    # Novas doenças pré-existentes
    has_hiv: Optional[bool] = False
    has_depressao_ansiedade: Optional[bool] = False
    has_asma: Optional[bool] = False
    has_trombofilia: Optional[bool] = False

    # Antecedentes familiares adicionais
    familiar_trombose: Optional[bool] = False

    # Hábitos de vida adicionais
    violencia_domestica: Optional[bool] = False
    sono_qualidade: Optional[str] = None
    estresse_nivel: Optional[str] = None
    exposicao_ocupacional: Optional[str] = None

    # Suporte social / Acompanhante
    acompanhante_nome: Optional[str] = None
    acompanhante_parentesco: Optional[str] = None
    acompanhante_telefone: Optional[str] = None
    situacao_conjugal: Optional[str] = None


class AnamnesisCreate(AnamnesisBase):
    pass


class AnamnesisResponse(AnamnesisBase, BaseEntitySchema):
    patient_id: UUID
