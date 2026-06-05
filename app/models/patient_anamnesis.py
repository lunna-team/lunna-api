from sqlalchemy import Column, ForeignKey, Boolean, SmallInteger, String, Text
from sqlalchemy.orm import relationship
from app.models.base import BaseModel


class PatientAnamnesis(BaseModel):
    __tablename__ = 'patient_anamnesis'

    patient_id = Column(
        ForeignKey('patients.id', ondelete='CASCADE'),
        unique=True, nullable=False,
    )

    # Doenças pré-existentes
    has_diabetes = Column(Boolean, default=False, nullable=False)
    has_hipertensao = Column(Boolean, default=False, nullable=False)
    has_cardiopatia = Column(Boolean, default=False, nullable=False)
    has_epilepsia = Column(Boolean, default=False, nullable=False)
    has_tireoide = Column(Boolean, default=False, nullable=False)
    has_doenca_renal = Column(Boolean, default=False, nullable=False)
    has_autoimune = Column(Boolean, default=False, nullable=False)
    outras_doencas = Column(Text, nullable=True)

    # Alergias
    alergias_medicamentos = Column(Text, nullable=True)
    outras_alergias = Column(Text, nullable=True)

    # Antecedentes familiares
    familiar_diabetes = Column(Boolean, default=False, nullable=False)
    familiar_hipertensao = Column(Boolean, default=False, nullable=False)
    familiar_gemelaridade = Column(Boolean, default=False, nullable=False)
    familiar_malformacoes = Column(Boolean, default=False, nullable=False)
    outros_familiares = Column(Text, nullable=True)

    # Hábitos
    tabagismo = Column(Boolean, default=False, nullable=False)
    tabagismo_cigarros_dia = Column(SmallInteger, nullable=True)
    alcool = Column(Boolean, default=False, nullable=False)
    alcool_frequencia = Column(String(20), nullable=True)  # 'social' | 'semanal' | 'diario'
    drogas_ilicitas = Column(Boolean, default=False, nullable=False)
    atividade_fisica = Column(Boolean, default=False, nullable=False)
    atividade_fisica_descricao = Column(String(255), nullable=True)

    # Antecedentes obstétricos relevantes
    pre_eclampsia_anterior = Column(Boolean, default=False, nullable=False)
    diabetes_gestacional_anterior = Column(Boolean, default=False, nullable=False)
    perda_fetal_anterior = Column(Boolean, default=False, nullable=False)
    prematuridade_anterior = Column(Boolean, default=False, nullable=False)
    intercorrencias_anteriores = Column(Text, nullable=True)

    # GESTA (G/P/A)
    gesta = Column(SmallInteger, nullable=True)
    para = Column(SmallInteger, nullable=True)
    abortos = Column(SmallInteger, nullable=True)
    tipo_parto_anterior = Column(String(20), nullable=True)  # 'normal' | 'cesarea' | 'ambos'

    # Novas doenças pré-existentes
    has_hiv = Column(Boolean, default=False, nullable=False)
    has_depressao_ansiedade = Column(Boolean, default=False, nullable=False)
    has_asma = Column(Boolean, default=False, nullable=False)
    has_trombofilia = Column(Boolean, default=False, nullable=False)

    # Antecedentes familiares adicionais
    familiar_trombose = Column(Boolean, default=False, nullable=False)

    # Hábitos de vida adicionais
    violencia_domestica = Column(Boolean, default=False, nullable=False)
    sono_qualidade = Column(String(20), nullable=True)  # 'boa' | 'regular' | 'ruim'
    estresse_nivel = Column(String(20), nullable=True)  # 'baixo' | 'moderado' | 'alto'
    exposicao_ocupacional = Column(Text, nullable=True)

    # Suporte social / Acompanhante
    acompanhante_nome = Column(String(200), nullable=True)
    acompanhante_parentesco = Column(String(100), nullable=True)
    acompanhante_telefone = Column(String(30), nullable=True)
    situacao_conjugal = Column(String(30), nullable=True)  # 'casada' | 'uniao_estavel' | 'solteira' | 'outro'

    patient = relationship("Patient")
