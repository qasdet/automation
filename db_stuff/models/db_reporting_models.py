from typing import List, Optional
from sqlalchemy import (
    BigInteger,
    Boolean,
    Computed,
    Date,
    DateTime,
    Double,
    ForeignKeyConstraint,
    Identity,
    Index,
    Integer,
    PrimaryKeyConstraint,
    SmallInteger,
    Text,
    UniqueConstraint,
    Uuid,
    text,
)
from sqlalchemy.dialects.postgresql import ENUM, JSONB
from sqlalchemy.orm import declarative_base, mapped_column, relationship
from sqlalchemy.orm.base import Mapped

Base = declarative_base()


class Campaigns(Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='campaigns_pkey'),
        Index('campaigns_created_at_idx', 'created_at'),
        Index('campaigns_updated_at_idx', 'updated_at'),
        Index('campaigns_uuid_idx', 'uuid', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    uuid = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))


class ConversionPtrs(Base):
    __tablename__ = 'conversion_ptrs'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='conversion_ptrs_pkey'),
        Index('conversion_ptrs_created_at_idx', 'created_at'),
        Index('conversion_ptrs_external_parent_id_idx', 'external_parent_id'),
        Index('conversion_ptrs_source_code_idx', 'source_code'),
        Index('conversion_ptrs_source_type_idx', 'source_type'),
        Index('conversion_ptrs_unique_idx', 'external_id', 'source_code', unique=True),
        Index('conversion_ptrs_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    external_id = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    source_type = mapped_column(Text, nullable=False)
    source_code = mapped_column(Text, nullable=False)
    is_valid = mapped_column(Boolean, nullable=False, server_default=text('true'))
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    external_parent_id = mapped_column(Text, comment='╠юцхЄ с√Є№ єърчрэ шфхэЄшЇшърЄюЁ ёўхЄўшър')

    sources_data: Mapped[List['SourcesData']] = relationship('SourcesData', uselist=True, back_populates='conversion_ptr')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='conversion_ptr')


class CreativeFrames(Base):
    __tablename__ = 'creative_frames'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='creative_frames_pkey'),
        Index('creative_frames_created_at_idx', 'created_at'),
        Index('creative_frames_updated_at_idx', 'updated_at'),
        Index('creative_frames_uuid_idx', 'uuid', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    uuid = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    creatives: Mapped[List['Creatives']] = relationship('Creatives', uselist=True, back_populates='frame')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='creative_frame')


class CreativeReports(Base):
    __tablename__ = 'creative_reports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='creative_reports_pkey'),
        Index('creative_reports_campaign_id_idx', 'campaign_id', unique=True),
        Index('creative_reports_created_at_idx', 'created_at'),
        Index('creative_reports_finish_on_idx', 'finish_on'),
        Index('creative_reports_generate_finished_at_idx', 'generate_finished_at'),
        Index('creative_reports_generate_started_at_idx', 'generate_started_at'),
        Index('creative_reports_start_on_idx', 'start_on'),
        Index('creative_reports_status_idx', 'status'),
        Index('creative_reports_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    campaign_id = mapped_column(Text, nullable=False)
    start_on = mapped_column(Date, nullable=False)
    finish_on = mapped_column(Date, nullable=False)
    data = mapped_column(JSONB, nullable=False)
    status = mapped_column(ENUM('digital_report_status', 'PROCESSING', 'READY', name='digital_report_status'), nullable=False, server_default=text("'PROCESSING'::digital_report_status"))
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    generate_started_at = mapped_column(DateTime(True))
    generate_finished_at = mapped_column(DateTime(True))

    creative_report_settings: Mapped[List['CreativeReportSettings']] = relationship('CreativeReportSettings', uselist=True, back_populates='report')


class Dates(Base):
    __tablename__ = 'dates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='dates_pkey'),
        UniqueConstraint('date_at', name='dates_date_at_key'),
        Index('dates_created_at_idx', 'created_at'),
        Index('dates_date_on_idx', 'date_on'),
        Index('dates_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    date_at = mapped_column(DateTime(True), nullable=False)
    date_on = mapped_column(Date, Computed("(date_at AT TIME ZONE 'UTC'::text)", persisted=True), nullable=False)
    year = mapped_column(SmallInteger, Computed("EXTRACT(year FROM (date_at AT TIME ZONE 'UTC'::text))", persisted=True), nullable=False)
    month = mapped_column(SmallInteger, Computed("EXTRACT(month FROM (date_at AT TIME ZONE 'UTC'::text))", persisted=True), nullable=False)
    day = mapped_column(SmallInteger, Computed("EXTRACT(day FROM (date_at AT TIME ZONE 'UTC'::text))", persisted=True), nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    sources_data: Mapped[List['SourcesData']] = relationship('SourcesData', uselist=True, back_populates='date')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='date')


class DigitalReports(Base):
    __tablename__ = 'digital_reports'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='digital_reports_pkey'),
        Index('digital_reports_campaign_id_idx', 'campaign_id', unique=True),
        Index('digital_reports_created_at_idx', 'created_at'),
        Index('digital_reports_finish_on_idx', 'finish_on'),
        Index('digital_reports_generate_finished_at_idx', 'generate_finished_at'),
        Index('digital_reports_generate_started_at_idx', 'generate_started_at'),
        Index('digital_reports_start_on_idx', 'start_on'),
        Index('digital_reports_status_idx', 'status'),
        Index('digital_reports_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    campaign_id = mapped_column(Text, nullable=False)
    start_on = mapped_column(Date, nullable=False)
    finish_on = mapped_column(Date, nullable=False)
    data = mapped_column(JSONB, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    status = mapped_column(ENUM('digital_report_status', 'PROCESSING', 'READY', name='digital_report_status'), server_default=text("'PROCESSING'::digital_report_status"))
    generate_started_at = mapped_column(DateTime(True))
    generate_finished_at = mapped_column(DateTime(True))

    digital_report_settings: Mapped[List['DigitalReportSettings']] = relationship('DigitalReportSettings', uselist=True, back_populates='digital_report')


class GooseDbVersion(Base):
    __tablename__ = 'goose_db_version'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='goose_db_version_pkey'),
    )

    id = mapped_column(Integer)
    version_id = mapped_column(BigInteger, nullable=False)
    is_applied = mapped_column(Boolean, nullable=False)
    tstamp = mapped_column(DateTime, server_default=text('now()'))


class MetricCodes(Base):
    __tablename__ = 'metric_codes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='metric_codes_pkey'),
        Index('metric_codes_code_idx', 'code', unique=True),
        Index('metric_codes_created_at_idx', 'created_at'),
        Index('metric_codes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    sources_data: Mapped[List['SourcesData']] = relationship('SourcesData', uselist=True, back_populates='metric_code')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='metric_code')


class Placements(Base):
    __tablename__ = 'placements'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='placements_pkey'),
        Index('placements_created_at_idx', 'created_at'),
        Index('placements_updated_at_idx', 'updated_at'),
        Index('placements_uuid_idx', 'uuid', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    uuid = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    sources_data: Mapped[List['SourcesData']] = relationship('SourcesData', uselist=True, back_populates='placement')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='placement')


class SourceTypes(Base):
    __tablename__ = 'source_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='source_types_pkey'),
        Index('source_types_created_at_idx', 'created_at'),
        Index('source_types_name_idx', 'name', unique=True),
        Index('source_types_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    sources_data: Mapped[List['SourcesData']] = relationship('SourcesData', uselist=True, back_populates='source_type')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='source_type')


class CreativeReportSettings(Base):
    __tablename__ = 'creative_report_settings'
    __table_args__ = (
        ForeignKeyConstraint(['report_id'], ['creative_reports.id'], ondelete='CASCADE', name='creative_report_settings_report_id_fkey'),
        PrimaryKeyConstraint('id', name='creative_report_settings_pkey'),
        Index('creative_report_settings_created_at_idx', 'created_at'),
        Index('creative_report_settings_report_id_idx', 'report_id'),
        Index('creative_report_settings_updated_at_idx', 'updated_at'),
        Index('creative_report_settings_user_id_report_id_idx', 'user_id', 'report_id', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    user_id = mapped_column(Uuid, nullable=False)
    report_id = mapped_column(BigInteger, nullable=False)
    settings = mapped_column(JSONB, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    report: Mapped['CreativeReports'] = relationship('CreativeReports', back_populates='creative_report_settings')


class Creatives(Base):
    __tablename__ = 'creatives'
    __table_args__ = (
        ForeignKeyConstraint(['frame_id'], ['creative_frames.id'], name='creatives_frame_id_fkey'),
        PrimaryKeyConstraint('id', name='creatives_pkey'),
        Index('creatives_created_at_idx', 'created_at'),
        Index('creatives_frame_id_idx', 'frame_id'),
        Index('creatives_updated_at_idx', 'updated_at'),
        Index('creatives_uuid_idx', 'uuid', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    uuid = mapped_column(Uuid, nullable=False)
    frame_id = mapped_column(BigInteger, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    frame: Mapped['CreativeFrames'] = relationship('CreativeFrames', back_populates='creatives')
    creatives_data: Mapped[List['CreativesData']] = relationship('CreativesData', uselist=True, back_populates='creative')


class DigitalReportSettings(Base):
    __tablename__ = 'digital_report_settings'
    __table_args__ = (
        ForeignKeyConstraint(['digital_report_id'], ['digital_reports.id'], ondelete='CASCADE', onupdate='CASCADE', name='digital_report_settings_digital_report_id_fkey'),
        PrimaryKeyConstraint('id', name='digital_report_settings_pkey'),
        Index('digital_report_settings_created_at_idx', 'created_at'),
        Index('digital_report_settings_digital_report_id_idx', 'digital_report_id'),
        Index('digital_report_settings_updated_at_idx', 'updated_at'),
        Index('digital_report_settings_user_id_digital_report_id_idx', 'user_id', 'digital_report_id', unique=True),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    user_id = mapped_column(Uuid, nullable=False)
    digital_report_id = mapped_column(BigInteger, nullable=False)
    settings = mapped_column(JSONB, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))

    digital_report: Mapped['DigitalReports'] = relationship('DigitalReports', back_populates='digital_report_settings')


class SourcesData(Base):
    __tablename__ = 'sources_data'
    __table_args__ = (
        ForeignKeyConstraint(['conversion_ptr_id'], ['conversion_ptrs.id'], ondelete='RESTRICT', onupdate='CASCADE', name='sources_data_conversion_ptr_id_fkey'),
        ForeignKeyConstraint(['date_id'], ['dates.id'], ondelete='RESTRICT', onupdate='CASCADE', name='sources_data_date_id_fkey'),
        ForeignKeyConstraint(['metric_code_id'], ['metric_codes.id'], ondelete='RESTRICT', onupdate='CASCADE', name='sources_data_metric_code_id_fkey'),
        ForeignKeyConstraint(['placement_id'], ['placements.id'], ondelete='RESTRICT', onupdate='CASCADE', name='sources_data_placement_id_fkey'),
        ForeignKeyConstraint(['source_type_id'], ['source_types.id'], ondelete='RESTRICT', onupdate='CASCADE', name='sources_data_source_type_id_fkey'),
        PrimaryKeyConstraint('id', name='sources_data_pkey'),
        Index('sources_data_changed_by_event_id_idx', 'changed_by_event_id'),
        Index('sources_data_conversion_ptr_id_idx', 'conversion_ptr_id'),
        Index('sources_data_created_at_idx', 'created_at'),
        Index('sources_data_date_id_idx', 'date_id'),
        Index('sources_data_is_calculated_idx', 'is_calculated'),
        Index('sources_data_is_manual_idx', 'is_manual'),
        Index('sources_data_metric_code_id_idx', 'metric_code_id'),
        Index('sources_data_placement_id_idx', 'placement_id'),
        Index('sources_data_source_type_id_idx', 'source_type_id'),
        Index('sources_data_unique_with_conversion_idx', 'date_id', 'metric_code_id', 'placement_id', 'source_type_id', 'conversion_ptr_id', unique=True),
        Index('sources_data_unique_without_conversion_idx', 'date_id', 'metric_code_id', 'placement_id', 'source_type_id', unique=True),
        Index('sources_data_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    value = mapped_column(Double(53), nullable=False)
    date_id = mapped_column(BigInteger, nullable=False)
    metric_code_id = mapped_column(BigInteger, nullable=False)
    placement_id = mapped_column(BigInteger, nullable=False)
    is_valid = mapped_column(Boolean, nullable=False, server_default=text('true'))
    source_type_id = mapped_column(BigInteger, nullable=False)
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    is_calculated = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='╟эрўхэшх ьхЄЁшъш ЁрёёўшЄрэю ртЄюьрЄшўхёъш: фр/эхЄ')
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('clock_timestamp()'))
    is_manual = mapped_column(Boolean, nullable=False, server_default=text('false'), comment='╧Ёюшчтхфхэ ыш Ёєўэющ шьяюЁЄ ёЄрЄшёЄшъш')
    conversion_ptr_id = mapped_column(BigInteger)
    changed_by_event_id = mapped_column(Uuid, comment='ID ёюс√Єш , ъюЄюЁюх яюёыхфэшь ьхэ ыю чряшё№. ╚ёяюы№чєхЄё  эряЁшьхЁ, фы  т√ тыхэш  ёЄрЁ√ї чряшёхщ, яюёых юсэютыхэш  фрээ√ї.')

    conversion_ptr: Mapped[Optional['ConversionPtrs']] = relationship('ConversionPtrs', back_populates='sources_data')
    date: Mapped['Dates'] = relationship('Dates', back_populates='sources_data')
    metric_code: Mapped['MetricCodes'] = relationship('MetricCodes', back_populates='sources_data')
    placement: Mapped['Placements'] = relationship('Placements', back_populates='sources_data')
    source_type: Mapped['SourceTypes'] = relationship('SourceTypes', back_populates='sources_data')


class CreativesData(Base):
    __tablename__ = 'creatives_data'
    __table_args__ = (
        ForeignKeyConstraint(['conversion_ptr_id'], ['conversion_ptrs.id'], ondelete='CASCADE', name='creatives_data_conversion_ptr_id_fkey'),
        ForeignKeyConstraint(['creative_frame_id'], ['creative_frames.id'], ondelete='CASCADE', name='creatives_data_creative_frame_id_fkey'),
        ForeignKeyConstraint(['creative_id'], ['creatives.id'], ondelete='CASCADE', name='creatives_data_creative_id_fkey'),
        ForeignKeyConstraint(['date_id'], ['dates.id'], ondelete='CASCADE', name='creatives_data_date_id_fkey'),
        ForeignKeyConstraint(['metric_code_id'], ['metric_codes.id'], ondelete='CASCADE', name='creatives_data_metric_code_id_fkey'),
        ForeignKeyConstraint(['placement_id'], ['placements.id'], ondelete='CASCADE', name='creatives_data_placement_id_fkey'),
        ForeignKeyConstraint(['source_type_id'], ['source_types.id'], ondelete='CASCADE', name='creatives_data_source_type_id_fkey'),
        PrimaryKeyConstraint('id', name='creatives_data_pkey'),
        Index('creatives_data_changed_by_event_id_idx', 'changed_by_event_id'),
        Index('creatives_data_conversion_ptr_id_idx', 'conversion_ptr_id'),
        Index('creatives_data_created_at_idx', 'created_at'),
        Index('creatives_data_creative_frame_id_idx', 'creative_frame_id'),
        Index('creatives_data_creative_id_idx', 'creative_id'),
        Index('creatives_data_date_id_idx', 'date_id'),
        Index('creatives_data_date_id_placement_id_metric_code_id_source__idx1', 'date_id', 'placement_id', 'metric_code_id', 'source_type_id', 'creative_id', 'creative_frame_id', unique=True),
        Index('creatives_data_date_id_placement_id_metric_code_id_source_t_idx', 'date_id', 'placement_id', 'metric_code_id', 'source_type_id', 'conversion_ptr_id', 'creative_id', 'creative_frame_id', unique=True),
        Index('creatives_data_metric_code_id_idx', 'metric_code_id'),
        Index('creatives_data_placement_id_idx', 'placement_id'),
        Index('creatives_data_source_type_id_idx', 'source_type_id'),
        Index('creatives_data_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(BigInteger, Identity(start=1, increment=1, minvalue=1, maxvalue=9223372036854775807, cycle=False, cache=1))
    value = mapped_column(Double(53), nullable=False)
    date_id = mapped_column(BigInteger, nullable=False)
    metric_code_id = mapped_column(BigInteger, nullable=False)
    placement_id = mapped_column(BigInteger, nullable=False)
    source_type_id = mapped_column(BigInteger, nullable=False)
    is_calculated = mapped_column(Boolean, nullable=False, server_default=text('false'))
    creative_id = mapped_column(BigInteger, nullable=False)
    creative_frame_id = mapped_column(BigInteger, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    conversion_ptr_id = mapped_column(BigInteger)
    changed_by_event_id = mapped_column(Uuid)

    conversion_ptr: Mapped[Optional['ConversionPtrs']] = relationship('ConversionPtrs', back_populates='creatives_data')
    creative_frame: Mapped['CreativeFrames'] = relationship('CreativeFrames', back_populates='creatives_data')
    creative: Mapped['Creatives'] = relationship('Creatives', back_populates='creatives_data')
    date: Mapped['Dates'] = relationship('Dates', back_populates='creatives_data')
    metric_code: Mapped['MetricCodes'] = relationship('MetricCodes', back_populates='creatives_data')
    placement: Mapped['Placements'] = relationship('Placements', back_populates='creatives_data')
    source_type: Mapped['SourceTypes'] = relationship('SourceTypes', back_populates='creatives_data')
