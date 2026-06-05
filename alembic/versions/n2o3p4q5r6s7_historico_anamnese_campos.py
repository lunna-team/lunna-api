"""historico anamnese campos

Revision ID: n2o3p4q5r6s7
Revises: m1n2o3p4q5r6
Create Date: 2026-06-05

"""
from alembic import op
import sqlalchemy as sa

revision = 'n2o3p4q5r6s7'
down_revision = 'm1n2o3p4q5r6'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('patient_anamnesis', sa.Column('prematuridade_anterior', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('intercorrencias_anteriores', sa.Text(), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('gesta', sa.SmallInteger(), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('para', sa.SmallInteger(), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('abortos', sa.SmallInteger(), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('tipo_parto_anterior', sa.String(20), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('has_hiv', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('has_depressao_ansiedade', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('has_asma', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('has_trombofilia', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('familiar_trombose', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('violencia_domestica', sa.Boolean(), nullable=False, server_default='false'))
    op.add_column('patient_anamnesis', sa.Column('sono_qualidade', sa.String(20), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('estresse_nivel', sa.String(20), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('exposicao_ocupacional', sa.Text(), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('acompanhante_nome', sa.String(200), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('acompanhante_parentesco', sa.String(100), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('acompanhante_telefone', sa.String(30), nullable=True))
    op.add_column('patient_anamnesis', sa.Column('situacao_conjugal', sa.String(30), nullable=True))


def downgrade() -> None:
    for col in [
        'situacao_conjugal', 'acompanhante_telefone', 'acompanhante_parentesco', 'acompanhante_nome',
        'exposicao_ocupacional', 'estresse_nivel', 'sono_qualidade', 'violencia_domestica',
        'familiar_trombose', 'has_trombofilia', 'has_asma', 'has_depressao_ansiedade', 'has_hiv',
        'tipo_parto_anterior', 'abortos', 'para', 'gesta',
        'intercorrencias_anteriores', 'prematuridade_anterior',
    ]:
        op.drop_column('patient_anamnesis', col)
