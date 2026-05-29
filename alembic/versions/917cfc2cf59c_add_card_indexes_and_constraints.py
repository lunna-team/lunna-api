"""add_card_indexes_and_constraints

Revision ID: 917cfc2cf59c
Revises: 054ee456f1d5
Create Date: 2026-05-29 05:01:48.701643

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '917cfc2cf59c'
down_revision: Union[str, None] = '054ee456f1d5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_index(op.f('ix_doctor_card_sections_doctor_id'), 'doctor_card_sections', ['doctor_id'], unique=False)
    op.create_index(op.f('ix_patient_card_entries_patient_id'), 'patient_card_entries', ['patient_id'], unique=False)
    op.create_index(op.f('ix_patient_card_entries_section_id'), 'patient_card_entries', ['section_id'], unique=False)
    op.create_index(op.f('ix_patient_card_field_values_patient_id'), 'patient_card_field_values', ['patient_id'], unique=False)
    op.create_index(op.f('ix_patient_card_field_values_section_id'), 'patient_card_field_values', ['section_id'], unique=False)
    op.create_unique_constraint('uq_patient_card_field_values_patient_section_label', 'patient_card_field_values', ['patient_id', 'section_id', 'label'])


def downgrade() -> None:
    op.drop_constraint('uq_patient_card_field_values_patient_section_label', 'patient_card_field_values', type_='unique')
    op.drop_index(op.f('ix_patient_card_field_values_section_id'), table_name='patient_card_field_values')
    op.drop_index(op.f('ix_patient_card_field_values_patient_id'), table_name='patient_card_field_values')
    op.drop_index(op.f('ix_patient_card_entries_section_id'), table_name='patient_card_entries')
    op.drop_index(op.f('ix_patient_card_entries_patient_id'), table_name='patient_card_entries')
    op.drop_index(op.f('ix_doctor_card_sections_doctor_id'), table_name='doctor_card_sections')
