from typing import List, Optional
from sqlalchemy import (
    ARRAY,
    BigInteger,
    Boolean,
    CheckConstraint,
    Date,
    DateTime,
    ForeignKeyConstraint,
    Index,
    Integer,
    Numeric,
    PrimaryKeyConstraint,
    Sequence,
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


class Admins(Base):
    __tablename__ = 'admins'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='admins_pkey'),
        Index('admins_created_at_idx', 'created_at'),
        Index('admins_lower_idx'),
        Index('admins_lower_idx1'),
        Index('admins_registered_at_idx', 'registered_at'),
        Index('admins_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    name = mapped_column(Text)
    email = mapped_column(Text)
    phone = mapped_column(Text)
    registered_at = mapped_column(DateTime(True))
    login = mapped_column(Text)


class Ages(Base):
    __tablename__ = 'ages'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='ages_pkey'),
        Index('ages_created_at_idx', 'created_at'),
        Index('ages_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_ages: Mapped[List['TargetingAges']] = relationship(
        'TargetingAges', uselist=True, back_populates='ages'
    )


class BrandAwarenesses(Base):
    __tablename__ = 'brand_awarenesses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='brand_awarenesses_pkey'),
        UniqueConstraint('code', name='brand_awarenesses_code_key'),
        Index('brand_awarenesses_created_at_idx', 'created_at'),
        Index('brand_awarenesses_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    brands: Mapped[List['Brands']] = relationship(
        'Brands', uselist=True, back_populates='awareness'
    )


class BuyTypes(Base):
    __tablename__ = 'buy_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='buy_types_pkey'),
        Index('buy_types_code_idx', 'code', unique=True),
        Index('buy_types_created_at_idx', 'created_at'),
        Index('buy_types_naming_idx', 'naming'),
        Index('buy_types_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)
    unit = mapped_column(Text, nullable=False)
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    placement_type = mapped_column(
        ENUM('placement_type', 'DYNAMIC', 'STATIC', name='placement_type'),
        nullable=False,
    )

    source_buy_types: Mapped[List['SourceBuyTypes']] = relationship(
        'SourceBuyTypes', uselist=True, back_populates='buy_type'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='buy_type'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='buy_type'
    )


class CampaignStatuses(Base):
    __tablename__ = 'campaign_statuses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='campaign_statuses_pkey'),
        Index('campaign_statuses_code_idx', 'code', unique=True),
        Index('campaign_statuses_created_at_idx', 'created_at'),
        Index('campaign_statuses_order_no_idx', 'order_no'),
        Index('campaign_statuses_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)
    order_no = mapped_column(Integer, nullable=False)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='status'
    )


class Campaigns(Base):
    __tablename__ = 'campaigns'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            name='campaigns_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['agency_id'],
            ['agencies.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='campaigns_agency_id_fkey',
        ),
        ForeignKeyConstraint(
            ['approved_mp_id'],
            ['mplans.id'],
            name='campaigns_approved_mp_id_fkey',
        ),
        ForeignKeyConstraint(
            ['brand_id'],
            ['brands.id'],
            onupdate='CASCADE',
            name='campaigns_brand_id_fkey',
        ),
        ForeignKeyConstraint(
            ['client_id'],
            ['clients.id'],
            onupdate='CASCADE',
            name='campaigns_client_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='campaigns_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['department_id'],
            ['departments.id'],
            onupdate='CASCADE',
            name='campaigns_department_id_fkey',
        ),
        ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            onupdate='CASCADE',
            name='campaigns_product_id_fkey',
        ),
        ForeignKeyConstraint(
            ['status_id'],
            ['campaign_statuses.id'],
            onupdate='CASCADE',
            name='campaigns_status_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='campaigns_pkey'),
        Index('campaigns_acl_organization_id_idx', 'acl_organization_id'),
        Index('campaigns_approved_mp_id_idx', 'approved_mp_id'),
        Index('campaigns_brand_id_idx', 'brand_id'),
        Index('campaigns_budget_idx', 'budget'),
        Index('campaigns_client_id_idx', 'client_id'),
        Index('campaigns_created_at_idx', 'created_at'),
        Index('campaigns_creator_user_id_idx', 'creator_user_id'),
        Index('campaigns_finish_on_idx', 'finish_on'),
        Index('campaigns_is_report_ready_idx', 'is_report_ready'),
        Index('campaigns_product_id_idx', 'product_id'),
        Index('campaigns_resplit_needed_by_id_idx', 'resplit_needed_by_id'),
        Index('campaigns_start_on_idx', 'start_on'),
        Index('campaigns_status_id_idx', 'status_id'),
        Index('campaigns_unique_code_idx', unique=True),
        Index('campaigns_unique_naming_part_idx', 'unique_naming_part'),
        Index('campaigns_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    status_id = mapped_column(Uuid, nullable=False)
    client_id = mapped_column(Uuid, nullable=False)
    acl_organization_id = mapped_column(
        Uuid, nullable=False, comment='Доступ: принадлежность к организации'
    )
    is_report_ready = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    brand_id = mapped_column(Uuid, nullable=False)
    product_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text)
    market_target = mapped_column(Text)
    start_on = mapped_column(Date)
    finish_on = mapped_column(Date)
    target_audience = mapped_column(Text)
    conditions = mapped_column(Text)
    unique_naming_part = mapped_column(Text)
    approved_mp_id = mapped_column(Uuid)
    agency_id = mapped_column(Uuid)
    budget = mapped_column(Numeric(20, 2))
    department_id = mapped_column(Uuid)
    resplit_needed_by_id = mapped_column(
        Uuid,
        comment='Поле, если заполнено, говорит о том, что требуется пересплитование '
                'данных и id действия, которое это вызвало. Обнуляется после '
                'успешного выполнения операции.',
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='campaigns'
    )
    agency: Mapped[Optional['Agencies']] = relationship(
        'Agencies', back_populates='campaigns'
    )
    approved_mp: Mapped[Optional['Mplans']] = relationship(
        'Mplans', foreign_keys=[approved_mp_id], back_populates='campaigns'
    )
    brand: Mapped['Brands'] = relationship(
        'Brands', back_populates='campaigns'
    )
    client: Mapped['Clients'] = relationship(
        'Clients', back_populates='campaigns'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='campaigns'
    )
    department: Mapped[Optional['Departments']] = relationship(
        'Departments', back_populates='campaigns'
    )
    product: Mapped['Products'] = relationship(
        'Products', back_populates='campaigns'
    )
    status: Mapped['CampaignStatuses'] = relationship(
        'CampaignStatuses', back_populates='campaigns'
    )
    mplans: Mapped[List['Mplans']] = relationship(
        'Mplans',
        uselist=True,
        foreign_keys='[Mplans.campaign_id]',
        back_populates='campaign',
    )
    campaign_docs: Mapped[List['CampaignDocs']] = relationship(
        'CampaignDocs', uselist=True, back_populates='campaign'
    )
    creative_frames: Mapped[List['CreativeFrames']] = relationship(
        'CreativeFrames', uselist=True, back_populates='campaign'
    )
    campaign_cobrands: Mapped[List['CampaignCobrands']] = relationship(
        'CampaignCobrands', uselist=True, back_populates='campaign'
    )


class Channels(Base):
    __tablename__ = 'channels'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='channels_pkey'),
        Index('channels_created_at_idx', 'created_at'),
        Index('channels_updated_at_idx', 'updated_at'),
    )

    code = mapped_column(Text)
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    media_type = mapped_column(
        ENUM('media_type', 'TV', 'DIGITAL', 'OUTDOOR', name='media_type'),
        nullable=False,
    )
    is_used_by_splan = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    ad_formats: Mapped[List['AdFormats']] = relationship(
        'AdFormats', uselist=True, back_populates='channels'
    )
    ad_sizes: Mapped[List['AdSizes']] = relationship(
        'AdSizes', uselist=True, back_populates='channels'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='channels'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='channels'
    )


class Countries(Base):
    __tablename__ = 'countries'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='countries_pkey'),
        Index('countries_code_idx', 'code', unique=True),
        Index('countries_created_at_idx', 'created_at'),
        Index('countries_name_idx', 'name'),
        Index('countries_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)

    districts: Mapped[List['Districts']] = relationship(
        'Districts', uselist=True, back_populates='country'
    )


class Employments(Base):
    __tablename__ = 'employments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='employments_pkey'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )


class Files(Base):
    __tablename__ = 'files'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='files_pkey'),
        Index('files_external_file_id_idx', 'external_file_id'),
        Index('files_height_idx', 'height'),
        Index('files_name_idx', 'name'),
        Index('files_size_idx', 'size'),
        Index('files_type_idx', 'type'),
        Index('files_width_idx', 'width'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    external_file_id = mapped_column(
        Text, nullable=False, comment='id файла, генерируемый сервисом tus+s3.'
    )
    name = mapped_column(Text)
    type = mapped_column(Text)
    size = mapped_column(BigInteger)
    height = mapped_column(BigInteger)
    width = mapped_column(BigInteger)

    creatives: Mapped[List['Creatives']] = relationship(
        'Creatives', uselist=True, back_populates='file'
    )


class Genders(Base):
    __tablename__ = 'genders'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='genders_pkey'),
        Index('genders_created_at_idx', 'created_at'),
        Index('genders_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_genders: Mapped[List['TargetingGenders']] = relationship(
        'TargetingGenders', uselist=True, back_populates='gender'
    )


class Goals(Base):
    __tablename__ = 'goals'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='goals_pkey'),
        Index('goals_code_idx', 'code', unique=True),
        Index('goals_created_at_idx', 'created_at'),
        Index('goals_naming_idx', 'naming'),
        Index('goals_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)

    mplans: Mapped[List['Mplans']] = relationship(
        'Mplans', uselist=True, back_populates='goal'
    )
    goal_metrics: Mapped[List['GoalMetrics']] = relationship(
        'GoalMetrics', uselist=True, back_populates='goal'
    )


class GooseDbVersion(Base):
    __tablename__ = 'goose_db_version'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='goose_db_version_pkey'),
    )

    id = mapped_column(Integer)
    version_id = mapped_column(BigInteger, nullable=False)
    is_applied = mapped_column(Boolean, nullable=False)
    tstamp = mapped_column(DateTime, server_default=text('now()'))


class Incomes(Base):
    __tablename__ = 'incomes'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='incomes_pkey'),
        Index('incomes_created_at_idx', 'created_at'),
        Index('incomes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_incomes: Mapped[List['TargetingIncomes']] = relationship(
        'TargetingIncomes', uselist=True, back_populates='income'
    )


class Kids(Base):
    __tablename__ = 'kids'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='kids_pkey'),
        Index('kids_created_at_idx', 'created_at'),
        Index('kids_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_kids: Mapped[List['TargetingKids']] = relationship(
        'TargetingKids', uselist=True, back_populates='kid'
    )


class Martials(Base):
    __tablename__ = 'martials'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='martials_pkey'),
        Index('martials_created_at_idx', 'created_at'),
        Index('martials_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_martials: Mapped[List['TargetingMartials']] = relationship(
        'TargetingMartials', uselist=True, back_populates='martial'
    )


class MplanStatuses(Base):
    __tablename__ = 'mplan_statuses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='mplan_statuses_pkey'),
        Index('mplan_statuses_code_idx', 'code', unique=True),
        Index('mplan_statuses_created_at_idx', 'created_at'),
        Index('mplan_statuses_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    mplans: Mapped[List['Mplans']] = relationship(
        'Mplans', uselist=True, back_populates='status'
    )


class Mplans(Base):
    __tablename__ = 'mplans'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            name='mplans_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['campaign_id'],
            ['campaigns.id'],
            onupdate='CASCADE',
            name='mplans_campaign_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='mplans_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['goal_id'],
            ['goals.id'],
            onupdate='CASCADE',
            name='mplans_goal_id_fkey',
        ),
        ForeignKeyConstraint(
            ['status_id'],
            ['mplan_statuses.id'],
            onupdate='CASCADE',
            name='mplans_status_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='mplans_pkey'),
        Index('mplans_acl_organization_id_idx', 'acl_organization_id'),
        Index('mplans_approved_at_idx', 'approved_at'),
        Index('mplans_campaign_id_idx', 'campaign_id'),
        Index('mplans_created_at_idx', 'created_at'),
        Index('mplans_creator_user_id_idx', 'creator_user_id'),
        Index('mplans_goal_id_idx', 'goal_id'),
        Index('mplans_order_no_idx', 'order_no'),
        Index('mplans_placements_count_idx', 'placements_count'),
        Index('mplans_status_id_idx', 'status_id'),
        Index('mplans_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    campaign_id = mapped_column(Uuid, nullable=False)
    status_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    placements_count = mapped_column(
        Integer, nullable=False, server_default=text('0')
    )
    acl_organization_id = mapped_column(
        Uuid, nullable=False, comment='Доступ: принадлежность к организации'
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    goal_id = mapped_column(Uuid, nullable=False)
    approved_at = mapped_column(DateTime(True))
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns',
        uselist=True,
        foreign_keys='[Campaigns.approved_mp_id]',
        back_populates='approved_mp',
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='mplans'
    )
    campaign: Mapped['Campaigns'] = relationship(
        'Campaigns', foreign_keys=[campaign_id], back_populates='mplans'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='mplans'
    )
    goal: Mapped['Goals'] = relationship('Goals', back_populates='mplans')
    status: Mapped['MplanStatuses'] = relationship(
        'MplanStatuses', back_populates='mplans'
    )
    mplan_conversions: Mapped[List['MplanConversions']] = relationship(
        'MplanConversions', uselist=True, back_populates='mplan'
    )
    mplan_landings: Mapped[List['MplanLandings']] = relationship(
        'MplanLandings', uselist=True, back_populates='mplan'
    )
    targetings: Mapped[List['Targetings']] = relationship(
        'Targetings', uselist=True, back_populates='mplan'
    )
    matched_conversions: Mapped[List['MatchedConversions']] = relationship(
        'MatchedConversions', uselist=True, back_populates='mplan'
    )
    mplan_constraints: Mapped[List['MplanConstraints']] = relationship(
        'MplanConstraints', uselist=True, back_populates='mplan'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='mplan'
    )

    def __repr__(self):
        return (
            f'<Mplans({self.id!r} {self.campaign_id!r} {self.status_id!r} {self.placements_count!r} {self.acl_organization_id!r}'
            f'{self.order_no!r} {self.goal_id!r} {self.approved_at!r} {self.creator_user_id!r})'
        )


class OldRegions(Base):
    __tablename__ = 'old_regions'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='regions_pkey'),
        Index('regions_created_at_idx', 'created_at'),
        Index('regions_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    targeting_old_regions: Mapped[List['TargetingOldRegions']] = relationship(
        'TargetingOldRegions', uselist=True, back_populates='region'
    )


class Organizations(Base):
    __tablename__ = 'organizations'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='organizations_pkey'),
        Index('organizations_blocked_at_idx', 'blocked_at'),
        Index('organizations_created_at_idx', 'created_at'),
        Index('organizations_inn_idx', 'inn'),
        Index('organizations_kpp_idx', 'kpp'),
        Index('organizations_lower_idx'),
        Index('organizations_ogrn_idx', 'ogrn'),
        Index('organizations_phone_idx', 'phone'),
        Index('organizations_registered_at_idx', 'registered_at'),
        Index('organizations_role_idx', 'role'),
        Index('organizations_status_idx', 'status'),
        Index('organizations_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    role = mapped_column(
        ENUM(
            'organization_role', 'agency', 'client', name='organization_role'
        ),
        nullable=False,
    )
    status = mapped_column(
        ENUM(
            'organization_status',
            'new',
            'active',
            'blocked',
            name='organization_status',
        ),
        nullable=False,
    )
    full_name = mapped_column(Text, nullable=False)
    short_name = mapped_column(Text, nullable=False)
    inn = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    okopf = mapped_column(Text)
    firm_name = mapped_column(Text)
    ogrn = mapped_column(Text)
    kpp = mapped_column(Text)
    address = mapped_column(Text)
    phone = mapped_column(Text)
    registered_at = mapped_column(DateTime(True))
    blocked_at = mapped_column(DateTime(True))

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='acl_organization'
    )
    mplans: Mapped[List['Mplans']] = relationship(
        'Mplans', uselist=True, back_populates='acl_organization'
    )
    ad_systems: Mapped[List['AdSystems']] = relationship(
        'AdSystems', uselist=True, back_populates='acl_organization'
    )
    agencies: Mapped[List['Agencies']] = relationship(
        'Agencies', uselist=True, back_populates='acl_organization'
    )
    appsflyer_partners: Mapped[List['AppsflyerPartners']] = relationship(
        'AppsflyerPartners', uselist=True, back_populates='acl_organization'
    )
    brands: Mapped[List['Brands']] = relationship(
        'Brands', uselist=True, back_populates='acl_organization'
    )
    campaign_docs: Mapped[List['CampaignDocs']] = relationship(
        'CampaignDocs', uselist=True, back_populates='acl_organization'
    )
    clients: Mapped[List['Clients']] = relationship(
        'Clients', uselist=True, back_populates='acl_organization'
    )
    creative_frames: Mapped[List['CreativeFrames']] = relationship(
        'CreativeFrames', uselist=True, back_populates='acl_organization'
    )
    departments: Mapped[List['Departments']] = relationship(
        'Departments', uselist=True, back_populates='acl_organization'
    )
    mplan_conversions: Mapped[List['MplanConversions']] = relationship(
        'MplanConversions', uselist=True, back_populates='acl_organization'
    )
    persons: Mapped[List['Persons']] = relationship(
        'Persons', uselist=True, back_populates='organization'
    )
    projects: Mapped[List['Projects']] = relationship(
        'Projects', uselist=True, back_populates='acl_organization'
    )
    site_elements: Mapped[List['SiteElements']] = relationship(
        'SiteElements', uselist=True, back_populates='acl_organization'
    )
    site_sections: Mapped[List['SiteSections']] = relationship(
        'SiteSections', uselist=True, back_populates='acl_organization'
    )
    targetings: Mapped[List['Targetings']] = relationship(
        'Targetings', uselist=True, back_populates='acl_organization'
    )
    creatives: Mapped[List['Creatives']] = relationship(
        'Creatives', uselist=True, back_populates='acl_organization'
    )
    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='acl_organization'
    )
    organization_links: Mapped[List['OrganizationLinks']] = relationship(
        'OrganizationLinks', uselist=True, back_populates='organization'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='acl_organization'
    )


class PlacementStatuses(Base):
    __tablename__ = 'placement_statuses'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='placement_statuses_pkey'),
        Index('placement_statuses_code_idx', 'code', unique=True),
        Index('placement_statuses_created_at_idx', 'created_at'),
        Index('placement_statuses_order_no_idx', 'order_no'),
        Index('placement_statuses_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(Integer, nullable=False)

    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='placement_status'
    )

    def __repr__(self):
        return (
            f'<PlacementStatuses({self.id!r} {self.name!r} {self.code!r}'
        )


class ProductGeographies(Base):
    __tablename__ = 'product_geographies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_geographies_pkey'),
        UniqueConstraint('code', name='product_geographies_code_key'),
        Index('product_geographies_created_at_idx', 'created_at'),
        Index('product_geographies_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='geography'
    )


class ProductPriceCategories(Base):
    __tablename__ = 'product_price_categories'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_price_categories_pkey'),
        UniqueConstraint('code', name='product_price_categories_code_key'),
        Index('product_price_categories_created_at_idx', 'created_at'),
        Index('product_price_categories_order_no_idx', 'order_no'),
        Index('product_price_categories_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(Integer, nullable=False)

    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='price_category'
    )


class ProductPurchaseFrequencies(Base):
    __tablename__ = 'product_purchase_frequencies'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_purchases_frequencies_pkey'),
        UniqueConstraint(
            'code', name='product_purchases_frequencies_code_key'
        ),
        Index('product_purchase_frequencies_created_at_idx', 'created_at'),
        Index('product_purchase_frequencies_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='purchase_frequency'
    )


class ProductSeasonalities(Base):
    __tablename__ = 'product_seasonalities'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_seasonalities_pkey'),
        UniqueConstraint('code', name='product_seasonalities_code_key'),
        Index('product_seasonalities_created_at_idx', 'created_at'),
        Index('product_seasonalities_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    product_seasonality_values: Mapped[
        List['ProductSeasonalityValues']
    ] = relationship(
        'ProductSeasonalityValues',
        uselist=True,
        back_populates='product_seasonality',
    )
    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='seasonality'
    )


class ProductTypes(Base):
    __tablename__ = 'product_types'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='product_types_pkey'),
        UniqueConstraint('code', name='product_types_code_key'),
        Index('product_types_created_at_idx', 'created_at'),
        Index('product_types_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    product_categories: Mapped[List['ProductCategories']] = relationship(
        'ProductCategories', uselist=True, back_populates='product_type'
    )
    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='type'
    )


class Segments(Base):
    __tablename__ = 'segments'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='segments_pkey'),
        Index('segments_created_at_idx', 'created_at'),
        Index('segments_name_idx', 'name'),
        Index('segments_naming_idx', 'naming'),
        Index('segments_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    type = mapped_column(
        ENUM('segment_type', 'FCT', 'INT', 'OWN', name='segment_type'),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_segments: Mapped[List['TargetingSegments']] = relationship(
        'TargetingSegments', uselist=True, back_populates='segment'
    )


class Sellers(Base):
    __tablename__ = 'sellers'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='sellers_pkey'),
        Index('sellers_code_idx', 'code', unique=True),
        Index('sellers_created_at_idx', 'created_at'),
        Index('sellers_naming_idx', 'naming'),
        Index('sellers_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)

    sources: Mapped[List['Sources']] = relationship(
        'Sources', uselist=True, back_populates='seller'
    )
    seller_sources: Mapped[List['SellerSources']] = relationship(
        'SellerSources', uselist=True, back_populates='seller'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='seller'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='seller'
    )


class TimePeriods(Base):
    __tablename__ = 'time_periods'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='time_periods_pkey'),
        Index('time_periods_created_at_idx', 'created_at'),
        Index('time_periods_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    targeting_time_periods: Mapped[
        List['TargetingTimePeriods']
    ] = relationship(
        'TargetingTimePeriods', uselist=True, back_populates='time_period'
    )


class Units(Base):
    __tablename__ = 'units'
    __table_args__ = (
        PrimaryKeyConstraint('code', name='units_pkey'),
        Index('units_created_at_idx', 'created_at'),
        Index('units_updated_at_idx', 'updated_at'),
    )

    code = mapped_column(Text)
    name = mapped_column(Text, nullable=False)
    short_name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    metrics: Mapped[List['Metrics']] = relationship(
        'Metrics', uselist=True, back_populates='units'
    )


class UserRoles(Base):
    __tablename__ = 'user_roles'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='user_roles_pkey'),
        Index('user_roles_code_idx', 'code', unique=True),
        Index('user_roles_created_at_idx', 'created_at'),
        Index('user_roles_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    description = mapped_column(Text, nullable=False)
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    user_role_links: Mapped[List['UserRoleLinks']] = relationship(
        'UserRoleLinks', uselist=True, back_populates='role'
    )


class Users(Base):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='users_pkey'),
        Index('users_blocked_at_idx', 'blocked_at'),
        Index('users_created_at_idx', 'created_at'),
        Index('users_email_idx', unique=True),
        Index('users_login_idx', unique=True),
        Index('users_phone_idx', unique=True),
        Index('users_registered_at_idx', 'registered_at'),
        Index('users_status_idx', 'status'),
        Index('users_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    status = mapped_column(Text, nullable=False)
    login = mapped_column(Text, nullable=False)
    email = mapped_column(Text, nullable=False)
    phone = mapped_column(Text, nullable=False)
    registered_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    blocked_at = mapped_column(DateTime(True))

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='creator_user'
    )
    mplans: Mapped[List['Mplans']] = relationship(
        'Mplans', uselist=True, back_populates='creator_user'
    )
    ad_systems: Mapped[List['AdSystems']] = relationship(
        'AdSystems', uselist=True, back_populates='creator_user'
    )
    agencies: Mapped[List['Agencies']] = relationship(
        'Agencies', uselist=True, back_populates='creator_user'
    )
    appsflyer_partners: Mapped[List['AppsflyerPartners']] = relationship(
        'AppsflyerPartners', uselist=True, back_populates='creator_user'
    )
    brands: Mapped[List['Brands']] = relationship(
        'Brands', uselist=True, back_populates='creator_user'
    )
    campaign_docs: Mapped[List['CampaignDocs']] = relationship(
        'CampaignDocs', uselist=True, back_populates='creator_user'
    )
    clients: Mapped[List['Clients']] = relationship(
        'Clients', uselist=True, back_populates='creator_user'
    )
    creative_frames: Mapped[List['CreativeFrames']] = relationship(
        'CreativeFrames', uselist=True, back_populates='creator_user'
    )
    departments: Mapped[List['Departments']] = relationship(
        'Departments', uselist=True, back_populates='creator_user'
    )
    mplan_conversions: Mapped[List['MplanConversions']] = relationship(
        'MplanConversions', uselist=True, back_populates='creator_user'
    )
    projects: Mapped[List['Projects']] = relationship(
        'Projects', uselist=True, back_populates='creator_user'
    )
    site_elements: Mapped[List['SiteElements']] = relationship(
        'SiteElements', uselist=True, back_populates='creator_user'
    )
    site_sections: Mapped[List['SiteSections']] = relationship(
        'SiteSections', uselist=True, back_populates='creator_user'
    )
    targetings: Mapped[List['Targetings']] = relationship(
        'Targetings', uselist=True, back_populates='creator_user'
    )
    user_role_links: Mapped[List['UserRoleLinks']] = relationship(
        'UserRoleLinks', uselist=True, back_populates='user'
    )
    creatives: Mapped[List['Creatives']] = relationship(
        'Creatives', uselist=True, back_populates='creator_user'
    )
    integration_tokens: Mapped[List['IntegrationTokens']] = relationship(
        'IntegrationTokens', uselist=True, back_populates='user'
    )
    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='creator_user'
    )
    organization_links: Mapped[List['OrganizationLinks']] = relationship(
        'OrganizationLinks', uselist=True, back_populates='creator_user'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='creator_user'
    )


class UtmParameters(Base):
    __tablename__ = 'utm_parameters'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='utm_parameters_pkey'),
        Index('utm_parameters_code_idx', 'code', unique=True),
        Index('utm_parameters_created_at_idx', 'created_at'),
        Index('utm_parameters_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    utm_parameters_templates: Mapped[
        List['UtmParametersTemplates']
    ] = relationship(
        'UtmParametersTemplates', uselist=True, back_populates='parameter'
    )
    placement_utm_parameters: Mapped[
        List['PlacementUtmParameters']
    ] = relationship(
        'PlacementUtmParameters', uselist=True, back_populates='parameter'
    )


class UtmTemplates(Base):
    __tablename__ = 'utm_templates'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='utm_templates_pkey'),
        Index('utm_templates_code_idx', 'code', unique=True),
        Index('utm_templates_created_at_idx', 'created_at'),
        Index('utm_templates_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    instruction = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    utm_parameters_templates: Mapped[
        List['UtmParametersTemplates']
    ] = relationship(
        'UtmParametersTemplates', uselist=True, back_populates='template'
    )
    placement_utm_parameters: Mapped[
        List['PlacementUtmParameters']
    ] = relationship(
        'PlacementUtmParameters', uselist=True, back_populates='template'
    )


class AdFormats(Base):
    __tablename__ = 'ad_formats'
    __table_args__ = (
        ForeignKeyConstraint(
            ['channel_code'],
            ['channels.code'],
            onupdate='CASCADE',
            name='ad_formats_channel_code_fkey',
        ),
        PrimaryKeyConstraint('id', name='ad_formats_pkey'),
        Index('ad_formats_channel_code_idx', 'channel_code'),
        Index('ad_formats_code_idx', 'code', unique=True),
        Index('ad_formats_created_at_idx', 'created_at'),
        Index('ad_formats_is_active_idx', 'is_active'),
        Index('ad_formats_naming_idx', 'naming'),
        Index('ad_formats_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)
    is_active = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    channel_code = mapped_column(Text, nullable=False)

    channels: Mapped['Channels'] = relationship(
        'Channels', back_populates='ad_formats'
    )
    source_ad_sizes: Mapped[List['SourceAdSizes']] = relationship(
        'SourceAdSizes', uselist=True, back_populates='ad_format'
    )
    source_buy_types: Mapped[List['SourceBuyTypes']] = relationship(
        'SourceBuyTypes', uselist=True, back_populates='ad_format'
    )
    creative_plug_templates: Mapped[
        List['CreativePlugTemplates']
    ] = relationship(
        'CreativePlugTemplates', uselist=True, back_populates='ad_format'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='ad_format'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='format'
    )


class AdSizes(Base):
    __tablename__ = 'ad_sizes'
    __table_args__ = (
        ForeignKeyConstraint(
            ['channel_code'],
            ['channels.code'],
            onupdate='CASCADE',
            name='ad_sizes_channel_code_fkey',
        ),
        PrimaryKeyConstraint('id', name='ad_sizes_pkey'),
        Index('ad_sizes_channel_code_idx', 'channel_code'),
        Index('ad_sizes_code_idx', 'code', unique=True),
        Index('ad_sizes_created_at_idx', 'created_at'),
        Index('ad_sizes_is_active_idx', 'is_active'),
        Index('ad_sizes_naming_idx', 'naming'),
        Index('ad_sizes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    is_active = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    channel_code = mapped_column(Text, nullable=False)

    channels: Mapped['Channels'] = relationship(
        'Channels', back_populates='ad_sizes'
    )
    source_ad_sizes: Mapped[List['SourceAdSizes']] = relationship(
        'SourceAdSizes', uselist=True, back_populates='ad_size'
    )
    creative_plug_templates: Mapped[
        List['CreativePlugTemplates']
    ] = relationship(
        'CreativePlugTemplates', uselist=True, back_populates='ad_size'
    )
    placement_ad_sizes: Mapped[List['PlacementAdSizes']] = relationship(
        'PlacementAdSizes', uselist=True, back_populates='ad_size'
    )
    price_position_ad_sizes: Mapped[
        List['PricePositionAdSizes']
    ] = relationship(
        'PricePositionAdSizes', uselist=True, back_populates='size'
    )


class AdSystems(Base):
    __tablename__ = 'ad_systems'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='ad_systems_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='ad_systems_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='ad_systems_pkey'),
        Index('ad_systems_acl_organization_id_idx', 'acl_organization_id'),
        Index('ad_systems_created_at_idx', 'created_at'),
        Index('ad_systems_creator_user_id_idx', 'creator_user_id'),
        Index('ad_systems_name_idx', 'name'),
        Index('ad_systems_naming_idx', 'naming'),
        Index('ad_systems_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='ad_systems'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='ad_systems'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='ad_system'
    )


class Agencies(Base):
    __tablename__ = 'agencies'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='agencies_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='agencies_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='agencies_pkey'),
        Index('agencies_acl_organization_id_idx', 'acl_organization_id'),
        Index('agencies_created_at_idx', 'created_at'),
        Index('agencies_creator_user_id_idx', 'creator_user_id'),
        Index('agencies_name_idx', 'name'),
        Index('agencies_naming_idx', 'naming'),
        Index('agencies_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='agency'
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='agencies'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='agencies'
    )


class AppsflyerPartners(Base):
    __tablename__ = 'appsflyer_partners'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='appsflyer_partners_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='appsflyer_partners_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='appsflyer_partners_pkey'),
        Index(
            'appsflyer_partners_acl_organization_id_idx', 'acl_organization_id'
        ),
        Index('appsflyer_partners_created_at_idx', 'created_at'),
        Index('appsflyer_partners_creator_user_id_idx', 'creator_user_id'),
        Index('appsflyer_partners_identifier_idx', 'identifier'),
        Index('appsflyer_partners_name_idx', 'name'),
        Index('appsflyer_partners_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    identifier = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    account_name = mapped_column(Text)
    ad_id = mapped_column(Text)
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='appsflyer_partners'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='appsflyer_partners'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='appsflyer_partner'
    )


class Brands(Base):
    __tablename__ = 'brands'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='brands_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['awareness_id'],
            ['brand_awarenesses.id'],
            name='brands_awareness_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='brands_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='brands_pkey'),
        UniqueConstraint('code', name='brands_code_key'),
        Index('brands_acl_organization_id_idx', 'acl_organization_id'),
        Index('brands_awareness_id_idx', 'awareness_id'),
        Index('brands_created_at_idx', 'created_at'),
        Index('brands_creator_user_id_idx', 'creator_user_id'),
        Index('brands_naming_idx', 'naming'),
        Index('brands_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    naming = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    acl_organization_id = mapped_column(Uuid, nullable=False)
    awareness_id = mapped_column(Uuid)
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='brand'
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='brands'
    )
    awareness: Mapped[Optional['BrandAwarenesses']] = relationship(
        'BrandAwarenesses', back_populates='brands', post_update=True
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='brands'
    )
    campaign_cobrands: Mapped[List['CampaignCobrands']] = relationship(
        'CampaignCobrands', uselist=True, back_populates='cobrand'
    )
    organization_links: Mapped[List['OrganizationLinks']] = relationship(
        'OrganizationLinks', uselist=True, back_populates='brand'
    )

    def __repr__(self):
        return (
            f'<Brands({self.id!r} {self.name!r} {self.created_at!r} {self.updated_at!r} {self.naming!r} {self.code!r} '
            f'{self.acl_organization_id!r} {self.awareness_id!r} {self.creator_user_id!r})'
        )


class CampaignDocs(Base):
    __tablename__ = 'campaign_docs'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            name='campaign_docs_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['campaign_id'],
            ['campaigns.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='campaign_docs_campaign_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='campaign_docs_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='campaign_docs_pkey'),
        Index('campaign_docs_acl_organization_id_idx', 'acl_organization_id'),
        Index('campaign_docs_campaign_id_idx', 'campaign_id'),
        Index('campaign_docs_created_at_idx', 'created_at'),
        Index('campaign_docs_creator_user_id_idx', 'creator_user_id'),
        Index('campaign_docs_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    campaign_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    path = mapped_column(Text, nullable=False)
    size = mapped_column(BigInteger, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    acl_organization_id = mapped_column(
        Uuid, nullable=False, comment='Доступ: принадлежность к организации'
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='campaign_docs'
    )
    campaign: Mapped['Campaigns'] = relationship(
        'Campaigns', back_populates='campaign_docs'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='campaign_docs'
    )


class Clients(Base):
    __tablename__ = 'clients'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='clients_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='clients_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='clients_pkey'),
        UniqueConstraint('code', name='clients_code_key'),
        Index('clients_acl_organization_id_idx', 'acl_organization_id'),
        Index('clients_created_at_idx', 'created_at'),
        Index('clients_creator_user_id_idx', 'creator_user_id'),
        Index('clients_inn_idx', 'inn'),
        Index('clients_kpp_idx', 'kpp'),
        Index('clients_naming_idx', 'naming'),
        Index('clients_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    naming = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    acl_organization_id = mapped_column(Uuid, nullable=False)
    full_name = mapped_column(Text)
    inn = mapped_column(Text)
    kpp = mapped_column(Text)
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='client'
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='clients'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='clients'
    )
    pricelists: Mapped[List['Pricelists']] = relationship(
        'Pricelists', uselist=True, back_populates='client'
    )
    organization_links: Mapped[List['OrganizationLinks']] = relationship(
        'OrganizationLinks', uselist=True, back_populates='client'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='client'
    )


class CreativeFrames(Base):
    __tablename__ = 'creative_frames'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='creative_frames_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['campaign_id'],
            ['campaigns.id'],
            onupdate='CASCADE',
            name='creative_frames_campaign_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='creative_frames_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='creative_frames_pkey'),
        Index('creative_frames_creator_user_id_idx', 'creator_user_id'),
        Index('creative_frames_is_active_idx', 'is_active'),
        Index(
            'creative_frames_name_campaign_id_idx',
            'name',
            'campaign_id',
            unique=True,
        ),
        Index('creative_frames_name_idx', 'name'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    campaign_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    is_active = mapped_column(
        Boolean, nullable=False, server_default=text('true')
    )
    acl_organization_id = mapped_column(Uuid, nullable=False)
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='creative_frames'
    )
    campaign: Mapped['Campaigns'] = relationship(
        'Campaigns', back_populates='creative_frames'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='creative_frames'
    )
    creatives: Mapped[List['Creatives']] = relationship(
        'Creatives', uselist=True, back_populates='frame'
    )


class Departments(Base):
    __tablename__ = 'departments'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='departments_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='departments_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='departments_pkey'),
        Index('departments_acl_organization_id_idx', 'acl_organization_id'),
        Index('departments_code_idx', 'code', unique=True),
        Index('departments_created_at_idx', 'created_at'),
        Index('departments_creator_user_id_idx', 'creator_user_id'),
        Index('departments_name_idx', 'name'),
        Index('departments_naming_idx', 'naming'),
        Index('departments_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    acl_organization_id = mapped_column(Uuid, nullable=False)
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='department'
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='departments'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='departments'
    )
    utm_parameters_templates: Mapped[
        List['UtmParametersTemplates']
    ] = relationship(
        'UtmParametersTemplates', uselist=True, back_populates='department'
    )


class Districts(Base):
    __tablename__ = 'districts'
    __table_args__ = (
        ForeignKeyConstraint(
            ['country_id'],
            ['countries.id'],
            onupdate='CASCADE',
            name='districts_country_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='districts_pkey'),
        Index('districts_code_idx', 'code', unique=True),
        Index('districts_country_id_idx', 'country_id'),
        Index('districts_created_at_idx', 'created_at'),
        Index('districts_name_idx', 'name'),
        Index('districts_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    country_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)

    country: Mapped['Countries'] = relationship(
        'Countries', back_populates='districts'
    )
    regions: Mapped[List['Regions']] = relationship(
        'Regions', uselist=True, back_populates='district'
    )


class Metrics(Base):
    __tablename__ = 'metrics'
    __table_args__ = (
        ForeignKeyConstraint(
            ['unit_code'],
            ['units.code'],
            onupdate='CASCADE',
            name='metrics_unit_code_fkey',
        ),
        PrimaryKeyConstraint('code', name='metrics_pkey'),
        Index('metrics_can_split_idx', 'can_split'),
        Index('metrics_code_idx', 'code', unique=True),
        Index('metrics_created_at_idx', 'created_at'),
        Index('metrics_is_conversion_idx', 'is_conversion'),
        Index('metrics_is_tracker_idx', 'is_tracker'),
        Index('metrics_operation_idx', 'operation'),
        Index('metrics_order_no_idx', 'order_no'),
        Index('metrics_source_type_idx', 'source_type'),
        Index('metrics_unit_code_idx', 'unit_code'),
        Index('metrics_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    type = mapped_column(ENUM('metric_type', 'QUANTITATIVE', 'PRICE', 'BENCHMARKS', name='metric_type'), nullable=False)
    code = mapped_column(Text, nullable=False)
    operation = mapped_column(
        ENUM('operation_type', 'lt', 'gt', name='operation_type'),
        nullable=False,
        server_default=text("'gt'::postgresql.operation_type"),
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    precision = mapped_column(
        SmallInteger, nullable=False, server_default=text('0')
    )
    can_split = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    is_conversion = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    is_tracker = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    order_no = mapped_column(Integer, nullable=False, server_default=text('0'))
    source_type = mapped_column(
        ENUM(
            'source_type',
            'SITE',
            'POSTCLICK',
            'VERIFIER',
            'TRACKER',
            name='source_type',
        ),
        nullable=False,
        server_default=text("'SITE'::postgresql.source_type"),
    )
    unit_code = mapped_column(Text, nullable=False)
    description = mapped_column(Text)

    units: Mapped['Units'] = relationship('Units', back_populates='metrics')
    goal_metrics: Mapped[List['GoalMetrics']] = relationship(
        'GoalMetrics', uselist=True, back_populates='metric'
    )
    mplan_constraints: Mapped[List['MplanConstraints']] = relationship(
        'MplanConstraints', uselist=True, back_populates='metric'
    )
    placement_metrics: Mapped[List['PlacementMetrics']] = relationship(
        'PlacementMetrics', uselist=True, back_populates='metric'
    )


class MplanConversions(Base):
    __tablename__ = 'mplan_conversions'
    __table_args__ = (
        ForeignKeyConstraint(['acl_organization_id'], ['organizations.id'],
                             name='mplan_conversions_acl_organization_id_fkey'),
        ForeignKeyConstraint(['creator_user_id'], ['users.id'], onupdate='CASCADE',
                             name='mplan_conversions_creator_user_id_fkey'),
        ForeignKeyConstraint(['mplan_id'], ['mplans.id'], ondelete='CASCADE', onupdate='CASCADE',
                             name='mplan_conversions_mplan_id_fkey'),
        PrimaryKeyConstraint('id', name='mplan_conversions_pkey'),
        Index('mplan_conversions_acl_organization_id_idx', 'acl_organization_id'),
        Index('mplan_conversions_created_at_idx', 'created_at'),
        Index('mplan_conversions_creator_user_id_idx', 'creator_user_id'),
        Index('mplan_conversions_is_default_idx', 'is_default'),
        Index('mplan_conversions_unique_idx', 'mplan_id', unique=True),
        Index('mplan_conversions_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    updated_at = mapped_column(DateTime(True), nullable=False, server_default=text('now()'))
    acl_organization_id = mapped_column(Uuid, nullable=False, comment='─юёЄєя: яЁшэрфыхцэюёЄ№ ъ юЁурэшчрЎшш')
    order_no = mapped_column(BigInteger, Sequence('order_no_seq', schema='postgresql'), nullable=False)
    is_default = mapped_column(Boolean, nullable=False, server_default=text('false'))
    mplan_id = mapped_column(Uuid)
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship('Organizations', back_populates='mplan_conversions')
    creator_user: Mapped[Optional['Users']] = relationship('Users', back_populates='mplan_conversions')
    mplan: Mapped[Optional['Mplans']] = relationship('Mplans', back_populates='mplan_conversions')
    matched_conversions: Mapped[List['MatchedConversions']] = relationship('MatchedConversions', uselist=True,
                                                                           back_populates='mplan_conversion')
    placement_conversion_links: Mapped[List['PlacementConversionLinks']] = relationship('PlacementConversionLinks',
                                                                                        uselist=True,
                                                                                        back_populates='mplan_conversion')

    def __repr__(self):
        return (
            f'<MplanConversions({self.id!r})'
        )


class MplanLandings(Base):
    __tablename__ = 'mplan_landings'
    __table_args__ = (
        ForeignKeyConstraint(
            ['mplan_id'],
            ['mplans.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='mplan_landings_mplan_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='mplan_landings_pkey'),
        Index('mplan_landings_created_at_idx', 'created_at'),
        Index('mplan_landings_mplan_id_lower_idx', 'mplan_id', unique=True),
        Index('mplan_landings_order_no_idx', 'order_no'),
        Index('mplan_landings_type_idx', 'type'),
        Index('mplan_landings_updated_at_idx', 'updated_at'),
        Index('mplan_landings_url_idx', 'url'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    url = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    type = mapped_column(
        ENUM(
            'landing_type',
            'WEB_LINK',
            'APPSFLYER_OL',
            'APPSFLYER_SPL',
            name='landing_type',
        ),
        nullable=False,
        server_default=text("'WEB_LINK'::postgresql.landing_type"),
    )
    mplan_id = mapped_column(Uuid, nullable=False)

    mplan: Mapped['Mplans'] = relationship(
        'Mplans', back_populates='mplan_landings'
    )


class Persons(Base):
    __tablename__ = 'persons'
    __table_args__ = (
        ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id'],
            name='persons_organization_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='persons_pkey'),
        Index('persons_created_at_idx', 'created_at'),
        Index('persons_organization_id_idx', 'organization_id'),
        Index('persons_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    organization_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    surname = mapped_column(Text)
    name = mapped_column(Text)
    middle_name = mapped_column(Text)
    contact_phone = mapped_column(Text)
    organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='persons'
    )
    pricelists: Mapped[List['Pricelists']] = relationship(
        'Pricelists',
        uselist=True,
        foreign_keys='[Pricelists.approver_id]',
        back_populates='approver',
    )
    pricelists_: Mapped[List['Pricelists']] = relationship(
        'Pricelists',
        uselist=True,
        foreign_keys='[Pricelists.creator_id]',
        back_populates='creator',
    )


class ProductCategories(Base):
    __tablename__ = 'product_categories'
    __table_args__ = (
        ForeignKeyConstraint(
            ['product_type_id'],
            ['product_types.id'],
            name='product_categories_product_type_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='product_categories_pkey'),
        UniqueConstraint('code', name='product_categories_code_key'),
        Index('product_categories_created_at_idx', 'created_at'),
        Index('product_categories_is_used_by_splan_idx', 'is_used_by_splan'),
        Index('product_categories_lower_idx', unique=True),
        Index('product_categories_product_type_id_idx', 'product_type_id'),
        Index('product_categories_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    is_used_by_splan = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    product_type_id = mapped_column(Uuid, nullable=False)

    product_type: Mapped['ProductTypes'] = relationship(
        'ProductTypes', back_populates='product_categories'
    )
    products: Mapped[List['Products']] = relationship(
        'Products', uselist=True, back_populates='category'
    )


class ProductSeasonalityValues(Base):
    __tablename__ = 'product_seasonality_values'
    __table_args__ = (
        ForeignKeyConstraint(
            ['product_seasonality_id'],
            ['product_seasonalities.id'],
            onupdate='CASCADE',
            name='product_seasonality_values_product_seasonality_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='product_seasonality_values_pkey'),
        UniqueConstraint('code', name='product_seasonality_values_code_key'),
        Index('product_seasonality_values_created_at_idx', 'created_at'),
        Index(
            'product_seasonality_values_product_seasonality_id_idx',
            'product_seasonality_id',
        ),
        Index('product_seasonality_values_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    product_seasonality_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    product_seasonality: Mapped['ProductSeasonalities'] = relationship(
        'ProductSeasonalities', back_populates='product_seasonality_values'
    )
    product_seasonality_value_links: Mapped[
        List['ProductSeasonalityValueLinks']
    ] = relationship(
        'ProductSeasonalityValueLinks',
        uselist=True,
        back_populates='seasonality_value',
    )


class Projects(Base):
    __tablename__ = 'projects'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='projects_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='projects_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='projects_pkey'),
        Index('projects_acl_organization_id_idx', 'acl_organization_id'),
        Index('projects_created_at_idx', 'created_at'),
        Index('projects_creator_user_id_idx', 'creator_user_id'),
        Index('projects_naming_idx', 'naming'),
        Index('projects_platform_idx', 'platform'),
        Index('projects_updated_at_idx', 'updated_at'),
        Index('projects_url_idx', 'url'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    platform = mapped_column(
        ENUM('project_platform', 'WEB', 'APP', name='project_platform'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    url = mapped_column(Text)
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='projects'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='projects'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='project'
    )


class SiteElements(Base):
    __tablename__ = 'site_elements'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='site_elements_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='site_elements_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='site_elements_pkey'),
        Index('site_elements_acl_organization_id_idx', 'acl_organization_id'),
        Index('site_elements_created_at_idx', 'created_at'),
        Index('site_elements_creator_user_id_idx', 'creator_user_id'),
        Index('site_elements_name_idx', 'name'),
        Index('site_elements_naming_idx', 'naming'),
        Index('site_elements_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='site_elements'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='site_elements'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='site_element'
    )


class SiteSections(Base):
    __tablename__ = 'site_sections'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='site_sections_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='site_sections_creator_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='site_sections_pkey'),
        Index('site_sections_acl_organization_id_idx', 'acl_organization_id'),
        Index('site_sections_created_at_idx', 'created_at'),
        Index('site_sections_creator_user_id_idx', 'creator_user_id'),
        Index('site_sections_name_idx', 'name'),
        Index('site_sections_naming_idx', 'naming'),
        Index('site_sections_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    acl_organization_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='site_sections'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='site_sections'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='site_section'
    )


class Sources(Base):
    __tablename__ = 'sources'
    __table_args__ = (
        CheckConstraint(
            "type = 'SITE'::postgresql.source_type AND seller_id IS NOT NULL OR type <> 'SITE'::postgresql.source_type",
            name='sources_seller_id_required',
        ),
        ForeignKeyConstraint(
            ['seller_id'],
            ['sellers.id'],
            onupdate='CASCADE',
            name='sources_seller_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='sources_pkey'),
        Index('sources_can_auto_gather_idx', 'can_auto_gather'),
        Index('sources_code_idx', 'code', unique=True),
        Index('sources_created_at_idx', 'created_at'),
        Index('sources_has_adset_idx', 'has_adset'),
        Index('sources_naming_idx', 'naming'),
        Index('sources_publish_method_idx', 'publish_method'),
        Index('sources_seller_id_idx', 'seller_id'),
        Index('sources_short_name_idx', 'short_name', unique=True),
        Index('sources_status_idx', 'status'),
        Index('sources_type_idx', 'type'),
        Index('sources_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    has_adset = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    naming = mapped_column(Text, nullable=False)
    url = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    code = mapped_column(Text, nullable=False)
    type = mapped_column(
        ENUM(
            'source_type',
            'SITE',
            'POSTCLICK',
            'VERIFIER',
            'TRACKER',
            name='source_type',
        ),
        nullable=False,
    )
    status = mapped_column(
        ENUM(
            'source_status',
            'active',
            'paused',
            'deleted',
            name='source_status',
        ),
        nullable=False,
    )
    publish_method = mapped_column(
        ENUM(
            'publish_method', 'none', 'manual', 'auto', name='publish_method'
        ),
        nullable=False,
    )
    can_auto_gather = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    short_name = mapped_column(Text, nullable=False)
    seller_id = mapped_column(Uuid)

    seller: Mapped[Optional['Sellers']] = relationship(
        'Sellers', back_populates='sources'
    )
    matched_conversions: Mapped[List['MatchedConversions']] = relationship(
        'MatchedConversions', uselist=True, back_populates='source'
    )
    seller_sources: Mapped[List['SellerSources']] = relationship(
        'SellerSources', uselist=True, back_populates='source'
    )
    source_ad_sizes: Mapped[List['SourceAdSizes']] = relationship(
        'SourceAdSizes', uselist=True, back_populates='source'
    )
    source_buy_types: Mapped[List['SourceBuyTypes']] = relationship(
        'SourceBuyTypes', uselist=True, back_populates='source'
    )
    source_macros: Mapped[List['SourceMacros']] = relationship(
        'SourceMacros', uselist=True, back_populates='source'
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='site'
    )
    price_position_sites: Mapped[List['PricePositionSites']] = relationship(
        'PricePositionSites', uselist=True, back_populates='site'
    )


class Targetings(Base):
    __tablename__ = 'targetings'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            name='targetings_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='targetings_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['mplan_id'],
            ['mplans.id'],
            ondelete='CASCADE',
            name='targetings_mplan_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targetings_pkey'),
        Index('targetings_acl_organization_id_idx', 'acl_organization_id'),
        Index('targetings_created_at_idx', 'created_at'),
        Index('targetings_creator_user_id_idx', 'creator_user_id'),
        Index('targetings_mplan_id_idx', 'mplan_id'),
        Index('targetings_name_mplan_id_idx', 'name', 'mplan_id', unique=True),
        Index('targetings_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    targeting_group = mapped_column(
        ENUM(
            'targeting_group',
            'BASE',
            'GEO',
            'INTERESTS',
            name='targeting_group',
        ),
        nullable=False,
    )
    mplan_id = mapped_column(Uuid, nullable=False)
    acl_organization_id = mapped_column(
        Uuid, nullable=False, comment='Доступ: принадлежность к организации'
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='targetings'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='targetings'
    )
    mplan: Mapped['Mplans'] = relationship(
        'Mplans', back_populates='targetings'
    )
    targeting_ages: Mapped[List['TargetingAges']] = relationship(
        'TargetingAges', uselist=True, back_populates='targeting'
    )
    targeting_genders: Mapped[List['TargetingGenders']] = relationship(
        'TargetingGenders', uselist=True, back_populates='targeting'
    )
    targeting_incomes: Mapped[List['TargetingIncomes']] = relationship(
        'TargetingIncomes', uselist=True, back_populates='targeting'
    )
    targeting_kids: Mapped[List['TargetingKids']] = relationship(
        'TargetingKids', uselist=True, back_populates='targeting'
    )
    targeting_martials: Mapped[List['TargetingMartials']] = relationship(
        'TargetingMartials', uselist=True, back_populates='targeting'
    )
    targeting_old_regions: Mapped[List['TargetingOldRegions']] = relationship(
        'TargetingOldRegions', uselist=True, back_populates='targeting'
    )
    targeting_segments: Mapped[List['TargetingSegments']] = relationship(
        'TargetingSegments', uselist=True, back_populates='targeting'
    )
    targeting_srequests: Mapped[List['TargetingSrequests']] = relationship(
        'TargetingSrequests', uselist=True, back_populates='targeting'
    )
    targeting_time_periods: Mapped[
        List['TargetingTimePeriods']
    ] = relationship(
        'TargetingTimePeriods', uselist=True, back_populates='targeting'
    )
    placement_targetings: Mapped[List['PlacementTargetings']] = relationship(
        'PlacementTargetings', uselist=True, back_populates='targeting'
    )
    targeting_cities: Mapped[List['TargetingCities']] = relationship(
        'TargetingCities', uselist=True, back_populates='targeting'
    )


class UserRoleLinks(Base):
    __tablename__ = 'user_role_links'
    __table_args__ = (
        ForeignKeyConstraint(
            ['role_id'],
            ['user_roles.id'],
            ondelete='CASCADE',
            name='user_role_links_role_id_fkey',
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            name='user_role_links_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='user_role_links_pkey'),
        Index('user_role_links_created_at_idx', 'created_at'),
        Index('user_role_links_role_id_idx', 'role_id'),
        Index('user_role_links_updated_at_idx', 'updated_at'),
        Index(
            'user_role_links_user_id_role_id_idx',
            'user_id',
            'role_id',
            unique=True,
        ),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    user_id = mapped_column(Uuid, nullable=False)
    role_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    role: Mapped['UserRoles'] = relationship(
        'UserRoles', back_populates='user_role_links'
    )
    user: Mapped['Users'] = relationship(
        'Users', back_populates='user_role_links'
    )


class CampaignCobrands(Base):
    __tablename__ = 'campaign_cobrands'
    __table_args__ = (
        ForeignKeyConstraint(
            ['campaign_id'],
            ['campaigns.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='campaign_cobrands_campaign_id_fkey',
        ),
        ForeignKeyConstraint(
            ['cobrand_id'],
            ['brands.id'],
            onupdate='CASCADE',
            name='campaign_cobrands_cobrand_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='campaign_cobrands_pkey'),
        Index(
            'campaign_cobrands_campaign_id_cobrand_id_idx',
            'campaign_id',
            'cobrand_id',
            unique=True,
        ),
        Index('campaign_cobrands_created_at_idx', 'created_at'),
        Index('campaign_cobrands_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    campaign_id = mapped_column(Uuid, nullable=False)
    cobrand_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    campaign: Mapped['Campaigns'] = relationship(
        'Campaigns', back_populates='campaign_cobrands'
    )
    cobrand: Mapped['Brands'] = relationship(
        'Brands', back_populates='campaign_cobrands'
    )


class Creatives(Base):
    __tablename__ = 'creatives'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='creatives_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='creatives_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['file_id'],
            ['files.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='creatives_file_id_fkey',
        ),
        ForeignKeyConstraint(
            ['frame_id'],
            ['creative_frames.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='creatives_frame_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='creatives_pkey'),
        Index('creatives_acl_organization_id_idx', 'acl_organization_id'),
        Index('creatives_created_at_idx', 'created_at'),
        Index('creatives_creator_user_id_idx', 'creator_user_id'),
        Index('creatives_file_id_idx', 'file_id'),
        Index('creatives_frame_id_idx', 'frame_id'),
        Index('creatives_naming_idx', 'naming'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    frame_id = mapped_column(Uuid, nullable=False)
    acl_organization_id = mapped_column(Uuid, nullable=False)
    naming = mapped_column(Text)
    file_id = mapped_column(Uuid)
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='creatives'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='creatives'
    )
    file: Mapped[Optional['Files']] = relationship(
        'Files', back_populates='creatives'
    )
    frame: Mapped['CreativeFrames'] = relationship(
        'CreativeFrames', back_populates='creatives'
    )
    placement_creatives: Mapped[List['PlacementCreatives']] = relationship(
        'PlacementCreatives', uselist=True, back_populates='creative'
    )


class GoalMetrics(Base):
    __tablename__ = 'goal_metrics'
    __table_args__ = (
        ForeignKeyConstraint(
            ['goal_id'],
            ['goals.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='goal_metrics_goal_id_fkey',
        ),
        ForeignKeyConstraint(
            ['metric_id'],
            ['metrics.id'],
            onupdate='CASCADE',
            name='goal_metrics_metric_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='goal_metrics_pkey'),
        Index('goal_metrics_created_at_idx', 'created_at'),
        Index(
            'goal_metrics_goal_id_metric_id_idx',
            'goal_id',
            'metric_id',
            unique=True,
        ),
        Index('goal_metrics_metric_id_idx', 'metric_id'),
        Index('goal_metrics_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    metric_id = mapped_column(Uuid, nullable=False)
    goal_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    goal: Mapped['Goals'] = relationship(
        'Goals', back_populates='goal_metrics'
    )
    metric: Mapped['Metrics'] = relationship(
        'Metrics', back_populates='goal_metrics'
    )


class IntegrationTokens(Base):
    __tablename__ = 'integration_tokens'
    __table_args__ = (
        ForeignKeyConstraint(
            ['itool_id'],
            ['integration_tools.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='integration_tokens_itool_id_fkey',
        ),
        ForeignKeyConstraint(
            ['user_id'],
            ['users.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='integration_tokens_user_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='integration_tokens_pkey'),
        Index('integration_tokens_created_at_idx', 'created_at'),
        Index('integration_tokens_expired_at_idx', 'expired_at'),
        Index('integration_tokens_account_idx', 'account'),
        Index('integration_tokens_itool_id_idx', 'itool_id'),
        Index(
            'integration_tokens_unique_idx',
            'user_id',
            'account',
            unique=True,
        ),
        Index('integration_tokens_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    user_id = mapped_column(Uuid, nullable=False)
    account = mapped_column(Text, nullable=False)
    token_data = mapped_column(JSONB, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    expired_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    status = mapped_column(
        ENUM(
            'access_token_status',
            'ACTIVE',
            'NOT_ACTIVE',
            name='access_token_status',
        ),
        nullable=False,
        server_default=text("'NOT_ACTIVE'::postgresql.access_token_status"),
    )
    itool_id = mapped_column(Uuid, nullable=False)

    user: Mapped['Users'] = relationship(
        'Users', back_populates='integration_tokens'
    )
    integration_tokens_history: Mapped[
        List['IntegrationTokensHistory']
    ] = relationship(
        'IntegrationTokensHistory',
        uselist=True,
        back_populates='integration_token',
    )
    placements: Mapped[List['Placements']] = relationship(
        'Placements', uselist=True, back_populates='site_integration_token'
    )
    placement_tools: Mapped[List['PlacementTools']] = relationship(
        'PlacementTools', uselist=True, back_populates='integration_token'
    )
    integration_tool: Mapped[List['IntegrationTools']] = relationship(
        'IntegrationTools', uselist=True, back_populates='integration_token'
    )


class IntegrationTools(Base):
    __tablename__ = 'integration_tools'
    __table_args__ = (
        PrimaryKeyConstraint('id', name='integration_tools_pkey'),
        Index('integration_tools_code_idx', 'code', unique=True),
        Index('integration_tools_created_at_idx', 'created_at'),
        Index('integration_tools_name_idx', 'name'),
        Index('integration_tools_type_idx', 'type'),
        Index('integration_tools_updated_at_idx', 'updated_at')
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    type = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    placement_tools: Mapped[List['PlacementTools']] = relationship(
        'PlacementTools', uselist=True, back_populates='integration_tool'
    )
    integration_token: Mapped[List['IntegrationTokens']] = relationship(
        'IntegrationTokens', uselist=True, back_populates='integration_tool')


class MatchedConversions(Base):
    __tablename__ = 'matched_conversions'
    __table_args__ = (
        ForeignKeyConstraint(
            ['mplan_conversion_id'],
            ['mplan_conversions.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='matched_conversions_mplan_conversion_id_fkey',
        ),
        ForeignKeyConstraint(
            ['mplan_id'],
            ['mplans.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='matched_conversions_mplan_id_fkey',
        ),
        ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            onupdate='CASCADE',
            name='matched_conversions_source_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='matched_conversions_pkey'),
        Index('matched_conversions_counter_id_idx', 'counter_id'),
        Index('matched_conversions_created_at_idx', 'created_at'),
        Index(
            'matched_conversions_fact_conversion_id_idx', 'fact_conversion_id'
        ),
        Index(
            'matched_conversions_fact_conversion_name_idx',
            'fact_conversion_name',
        ),
        Index(
            'matched_conversions_mplan_conversion_id_idx',
            'mplan_conversion_id',
        ),
        Index('matched_conversions_source_id_idx', 'source_id'),
        Index(
            'matched_conversions_unique_idx',
            'mplan_id',
            'mplan_conversion_id',
            'fact_conversion_id',
            'counter_id',
            'source_id',
            unique=True,
        ),
        Index(
            'matched_conversions_unique_null_idx',
            'mplan_id',
            'mplan_conversion_id',
            'fact_conversion_id',
            'counter_id',
            'source_id',
            unique=True,
        ),
        Index('matched_conversions_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    mplan_id = mapped_column(Uuid, nullable=False)
    mplan_conversion_id = mapped_column(Uuid, nullable=False)
    fact_conversion_id = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    fact_conversion_name = mapped_column(Text, nullable=False)
    source_id = mapped_column(Uuid, nullable=False)
    counter_id = mapped_column(Text)

    mplan_conversion: Mapped['MplanConversions'] = relationship(
        'MplanConversions', back_populates='matched_conversions'
    )
    mplan: Mapped['Mplans'] = relationship(
        'Mplans', back_populates='matched_conversions'
    )
    source: Mapped['Sources'] = relationship(
        'Sources', back_populates='matched_conversions'
    )


class MplanConstraints(Base):
    __tablename__ = 'mplan_constraints'
    __table_args__ = (
        ForeignKeyConstraint(
            ['metric_id'],
            ['metrics.id'],
            onupdate='CASCADE',
            name='mplan_constraints_metric_id_fkey',
        ),
        ForeignKeyConstraint(
            ['mplan_id'],
            ['mplans.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='mplan_constraints_mplan_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='mplan_constraints_pkey'),
        Index('mplan_constraints_created_at_idx', 'created_at'),
        Index('mplan_constraints_kind_idx', 'kind'),
        Index('mplan_constraints_metric_id_idx', 'metric_id'),
        Index('mplan_constraints_mplan_id_idx', 'mplan_id'),
        Index('mplan_constraints_operation_idx', 'operation'),
        Index('mplan_constraints_order_no_idx', 'order_no'),
        Index('mplan_constraints_result_idx', 'result'),
        Index('mplan_constraints_updated_at_idx', 'updated_at'),
        Index('mplan_constraints_value_idx', 'value'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    metric_id = mapped_column(Uuid, nullable=False)
    operation = mapped_column(
        ENUM('operation_type', 'lt', 'gt', name='operation_type'),
        nullable=False,
    )
    value = mapped_column(Numeric, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    kind = mapped_column(
        ENUM('metric_kind', 'HEAD', 'CONSTRAINT', name='metric_kind'),
        nullable=False,
        server_default=text("'CONSTRAINT'::postgresql.metric_kind"),
    )
    result = mapped_column(
        ENUM('metric_result', 'EXACTLY', 'MAXIMUM', name='metric_result'),
        nullable=False,
        server_default=text("'EXACTLY'::postgresql.metric_result"),
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    mplan_id = mapped_column(Uuid, nullable=False)

    metric: Mapped['Metrics'] = relationship(
        'Metrics', back_populates='mplan_constraints'
    )
    mplan: Mapped['Mplans'] = relationship(
        'Mplans', back_populates='mplan_constraints'
    )


class Pricelists(Base):
    __tablename__ = 'pricelists'
    __table_args__ = (
        ForeignKeyConstraint(
            ['approver_id'],
            ['persons.id'],
            onupdate='CASCADE',
            name='pricelists_approver_id_fkey',
        ),
        ForeignKeyConstraint(
            ['client_id'],
            ['clients.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='pricelists_client_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_id'],
            ['persons.id'],
            onupdate='CASCADE',
            name='pricelists_creator_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='pricelists_pkey'),
        Index('pricelists_approver_id_idx', 'approver_id'),
        Index('pricelists_client_id_idx', 'client_id'),
        Index('pricelists_code_idx', 'code'),
        Index('pricelists_created_at_idx', 'created_at'),
        Index('pricelists_creator_id_idx', 'creator_id'),
        Index('pricelists_finish_on_idx', 'finish_on'),
        Index('pricelists_start_on_idx', 'start_on'),
        Index('pricelists_status_idx', 'status'),
        Index('pricelists_type_idx', 'type'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    client_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text, nullable=False)
    type = mapped_column(
        ENUM(
            'pricelist_type',
            'FEDERAL',
            'REGIONAL',
            'AUCTION',
            name='pricelist_type',
        ),
        nullable=False,
    )
    start_on = mapped_column(Date, nullable=False)
    finish_on = mapped_column(Date, nullable=False)
    creator_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    status = mapped_column(
        ENUM(
            'pricelist_status',
            'CREATED',
            'APPROVED',
            'ACTIVE',
            name='pricelist_status',
        ),
        nullable=False,
    )
    approver_id = mapped_column(Uuid)
    approved_at = mapped_column(DateTime(True))
    comments = mapped_column(Text)

    approver: Mapped[Optional['Persons']] = relationship(
        'Persons', foreign_keys=[approver_id], back_populates='pricelists'
    )
    client: Mapped['Clients'] = relationship(
        'Clients', back_populates='pricelists'
    )
    creator: Mapped['Persons'] = relationship(
        'Persons', foreign_keys=[creator_id], back_populates='pricelists_'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='pricelist'
    )


class Products(Base):
    __tablename__ = 'products'
    __table_args__ = (
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            onupdate='CASCADE',
            name='products_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['category_id'],
            ['product_categories.id'],
            name='products_category_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='products_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['geography_id'],
            ['product_geographies.id'],
            name='products_geography_id_fkey',
        ),
        ForeignKeyConstraint(
            ['price_category_id'],
            ['product_price_categories.id'],
            name='products_price_category_id_fkey',
        ),
        ForeignKeyConstraint(
            ['purchase_frequency_id'],
            ['product_purchase_frequencies.id'],
            name='products_purchase_frequency_id_fkey',
        ),
        ForeignKeyConstraint(
            ['seasonality_id'],
            ['product_seasonalities.id'],
            name='products_seasonality_id_fkey',
        ),
        ForeignKeyConstraint(
            ['type_id'],
            ['product_types.id'],
            name='products_type_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='products_pkey'),
        UniqueConstraint('code', name='products_code_key'),
        Index('products_acl_organization_id_idx', 'acl_organization_id'),
        Index('products_category_id_idx', 'category_id'),
        Index('products_created_at_idx', 'created_at'),
        Index('products_creator_user_id_idx', 'creator_user_id'),
        Index('products_geography_id_idx', 'geography_id'),
        Index(
            'products_lower_acl_organization_id_idx',
            'acl_organization_id',
            unique=True,
        ),
        Index('products_naming_idx', 'naming'),
        Index('products_price_category_id_idx', 'price_category_id'),
        Index('products_purchase_frequency_id_idx', 'purchase_frequency_id'),
        Index('products_seasonality_id_idx', 'seasonality_id'),
        Index('products_type_id_idx', 'type_id'),
        Index('products_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    naming = mapped_column(Text, nullable=False)
    code = mapped_column(Text, nullable=False)
    acl_organization_id = mapped_column(Uuid, nullable=False)
    seasonality_id = mapped_column(Uuid)
    purchase_frequency_id = mapped_column(Uuid)
    type_id = mapped_column(Uuid)
    price_category_id = mapped_column(Uuid)
    category_id = mapped_column(Uuid)
    geography_id = mapped_column(Uuid)
    deep_link = mapped_column(Text)
    creator_user_id = mapped_column(Uuid)

    campaigns: Mapped[List['Campaigns']] = relationship(
        'Campaigns', uselist=True, back_populates='product'
    )
    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='products'
    )
    category: Mapped[Optional['ProductCategories']] = relationship(
        'ProductCategories', back_populates='products'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='products'
    )
    geography: Mapped[Optional['ProductGeographies']] = relationship(
        'ProductGeographies', back_populates='products'
    )
    price_category: Mapped[Optional['ProductPriceCategories']] = relationship(
        'ProductPriceCategories', back_populates='products'
    )
    purchase_frequency: Mapped[
        Optional['ProductPurchaseFrequencies']
    ] = relationship('ProductPurchaseFrequencies', back_populates='products')
    seasonality: Mapped[Optional['ProductSeasonalities']] = relationship(
        'ProductSeasonalities', back_populates='products'
    )
    type: Mapped[Optional['ProductTypes']] = relationship(
        'ProductTypes', back_populates='products'
    )
    creative_plug_templates: Mapped[
        List['CreativePlugTemplates']
    ] = relationship(
        'CreativePlugTemplates', uselist=True, back_populates='product'
    )
    organization_links: Mapped[List['OrganizationLinks']] = relationship(
        'OrganizationLinks', uselist=True, back_populates='product'
    )
    product_seasonality_value_links: Mapped[
        List['ProductSeasonalityValueLinks']
    ] = relationship(
        'ProductSeasonalityValueLinks', uselist=True, back_populates='product'
    )


class Regions(Base):
    __tablename__ = 'regions'
    __table_args__ = (
        ForeignKeyConstraint(
            ['district_id'],
            ['districts.id'],
            onupdate='CASCADE',
            name='regions_district_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='regions_pkey1'),
        Index('regions_code_idx', 'code', unique=True),
        Index('regions_created_at_idx1', 'created_at'),
        Index('regions_district_id_idx', 'district_id'),
        Index('regions_name_idx', 'name'),
        Index('regions_updated_at_idx1', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    district_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)

    district: Mapped['Districts'] = relationship(
        'Districts', back_populates='regions'
    )
    cities: Mapped[List['Cities']] = relationship(
        'Cities', uselist=True, back_populates='region'
    )
    price_positions: Mapped[List['PricePositions']] = relationship(
        'PricePositions', uselist=True, back_populates='region'
    )


class SellerSources(Base):
    __tablename__ = 'seller_sources'
    __table_args__ = (
        ForeignKeyConstraint(
            ['seller_id'],
            ['sellers.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='seller_sources_seller_id_fkey',
        ),
        ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            onupdate='CASCADE',
            name='seller_sources_source_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='seller_sources_pkey'),
        Index('seller_sources_created_at_idx', 'created_at'),
        Index(
            'seller_sources_seller_id_source_id_idx',
            'seller_id',
            'source_id',
            unique=True,
        ),
        Index('seller_sources_source_id_idx', 'source_id'),
        Index('seller_sources_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    seller_id = mapped_column(Uuid, nullable=False)
    source_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    seller: Mapped['Sellers'] = relationship(
        'Sellers', back_populates='seller_sources'
    )
    source: Mapped['Sources'] = relationship(
        'Sources', back_populates='seller_sources'
    )


class SourceAdSizes(Base):
    __tablename__ = 'source_ad_sizes'
    __table_args__ = (
        ForeignKeyConstraint(
            ['ad_format_id'],
            ['ad_formats.id'],
            onupdate='CASCADE',
            name='source_ad_sizes_ad_format_id_fkey',
        ),
        ForeignKeyConstraint(
            ['ad_size_id'],
            ['ad_sizes.id'],
            onupdate='CASCADE',
            name='source_ad_sizes_ad_size_id_fkey',
        ),
        ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='source_ad_sizes_source_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='source_ad_sizes_pkey'),
        Index('source_ad_sizes_ad_format_id_idx', 'ad_format_id'),
        Index('source_ad_sizes_ad_size_id_idx', 'ad_size_id'),
        Index('source_ad_sizes_created_at_idx', 'created_at'),
        Index(
            'source_ad_sizes_source_id_ad_format_id_ad_size_id_idx',
            'source_id',
            'ad_format_id',
            'ad_size_id',
            unique=True,
        ),
        Index('source_ad_sizes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    source_id = mapped_column(Uuid, nullable=False)
    ad_format_id = mapped_column(Uuid, nullable=False)
    ad_size_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    ad_format: Mapped['AdFormats'] = relationship(
        'AdFormats', back_populates='source_ad_sizes'
    )
    ad_size: Mapped['AdSizes'] = relationship(
        'AdSizes', back_populates='source_ad_sizes'
    )
    source: Mapped['Sources'] = relationship(
        'Sources', back_populates='source_ad_sizes'
    )


class SourceBuyTypes(Base):
    __tablename__ = 'source_buy_types'
    __table_args__ = (
        ForeignKeyConstraint(
            ['ad_format_id'],
            ['ad_formats.id'],
            onupdate='CASCADE',
            name='source_buy_types_ad_format_id_fkey',
        ),
        ForeignKeyConstraint(
            ['buy_type_id'],
            ['buy_types.id'],
            onupdate='CASCADE',
            name='source_buy_types_buy_type_id_fkey',
        ),
        ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='source_buy_types_source_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='source_buy_types_pkey'),
        Index('source_buy_types_ad_format_id_idx', 'ad_format_id'),
        Index('source_buy_types_buy_type_id_idx', 'buy_type_id'),
        Index('source_buy_types_created_at_idx', 'created_at'),
        Index(
            'source_buy_types_source_id_ad_format_id_buy_type_id_idx',
            'source_id',
            'ad_format_id',
            'buy_type_id',
            unique=True,
        ),
        Index('source_buy_types_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    source_id = mapped_column(Uuid, nullable=False)
    ad_format_id = mapped_column(Uuid, nullable=False)
    buy_type_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    ad_format: Mapped['AdFormats'] = relationship(
        'AdFormats', back_populates='source_buy_types'
    )
    buy_type: Mapped['BuyTypes'] = relationship(
        'BuyTypes', back_populates='source_buy_types'
    )
    source: Mapped['Sources'] = relationship(
        'Sources', back_populates='source_buy_types'
    )


class SourceMacros(Base):
    __tablename__ = 'source_macros'
    __table_args__ = (
        ForeignKeyConstraint(
            ['source_id'],
            ['sources.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='source_macros_source_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='source_macros_pkey'),
        Index('source_macros_code_idx', 'code', unique=True),
        Index('source_macros_created_at_idx', 'created_at'),
        Index('source_macros_source_id_idx', 'source_id'),
        Index('source_macros_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    source_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    value = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    source: Mapped['Sources'] = relationship(
        'Sources', back_populates='source_macros'
    )


class TargetingAges(Base):
    __tablename__ = 'targeting_ages'
    __table_args__ = (
        ForeignKeyConstraint(
            ['age_id'],
            ['ages.id'],
            onupdate='CASCADE',
            name='targeting_ages_age_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_ages_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_ages_pkey'),
        Index('targeting_ages_age_id_idx', 'age_id'),
        Index('targeting_ages_created_at_idx', 'created_at'),
        Index(
            'targeting_ages_targeting_id_age_id_idx',
            'targeting_id',
            'age_id',
            unique=True,
        ),
        Index('targeting_ages_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    age_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    ages: Mapped['Ages'] = relationship('Ages', back_populates='targeting_ages')
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_ages'
    )


class TargetingGenders(Base):
    __tablename__ = 'targeting_genders'
    __table_args__ = (
        ForeignKeyConstraint(
            ['gender_id'],
            ['genders.id'],
            onupdate='CASCADE',
            name='targeting_genders_gender_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_genders_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_genders_pkey'),
        Index('targeting_genders_created_at_idx', 'created_at'),
        Index('targeting_genders_gender_id_idx', 'gender_id'),
        Index(
            'targeting_genders_targeting_id_gender_id_idx',
            'targeting_id',
            'gender_id',
            unique=True,
        ),
        Index('targeting_genders_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    gender_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    gender: Mapped['Genders'] = relationship(
        'Genders', back_populates='targeting_genders'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_genders'
    )


class TargetingIncomes(Base):
    __tablename__ = 'targeting_incomes'
    __table_args__ = (
        ForeignKeyConstraint(
            ['income_id'],
            ['incomes.id'],
            onupdate='CASCADE',
            name='targeting_incomes_income_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_incomes_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_incomes_pkey'),
        Index('targeting_incomes_created_at_idx', 'created_at'),
        Index('targeting_incomes_income_id_idx', 'income_id'),
        Index(
            'targeting_incomes_targeting_id_income_id_idx',
            'targeting_id',
            'income_id',
            unique=True,
        ),
        Index('targeting_incomes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    income_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    income: Mapped['Incomes'] = relationship(
        'Incomes', back_populates='targeting_incomes'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_incomes'
    )


class TargetingKids(Base):
    __tablename__ = 'targeting_kids'
    __table_args__ = (
        ForeignKeyConstraint(
            ['kid_id'],
            ['kids.id'],
            onupdate='CASCADE',
            name='targeting_kids_kid_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_kids_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_kids_pkey'),
        Index('targeting_kids_created_at_idx', 'created_at'),
        Index('targeting_kids_kid_id_idx', 'kid_id'),
        Index(
            'targeting_kids_targeting_id_kid_id_idx',
            'targeting_id',
            'kid_id',
            unique=True,
        ),
        Index('targeting_kids_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    kid_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    kid: Mapped['Kids'] = relationship('Kids', back_populates='targeting_kids')
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_kids'
    )


class TargetingMartials(Base):
    __tablename__ = 'targeting_martials'
    __table_args__ = (
        ForeignKeyConstraint(
            ['martial_id'],
            ['martials.id'],
            onupdate='CASCADE',
            name='targeting_martials_martial_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_martials_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_martials_pkey'),
        Index('targeting_martials_created_at_idx', 'created_at'),
        Index('targeting_martials_martial_id_idx', 'martial_id'),
        Index(
            'targeting_martials_targeting_id_martial_id_idx',
            'targeting_id',
            'martial_id',
            unique=True,
        ),
        Index('targeting_martials_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    martial_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    martial: Mapped['Martials'] = relationship(
        'Martials', back_populates='targeting_martials'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_martials'
    )


class TargetingOldRegions(Base):
    __tablename__ = 'targeting_old_regions'
    __table_args__ = (
        ForeignKeyConstraint(
            ['region_id'],
            ['old_regions.id'],
            onupdate='CASCADE',
            name='targeting_regions_region_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_regions_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_regions_pkey'),
        Index('targeting_regions_created_at_idx', 'created_at'),
        Index('targeting_regions_region_id_idx', 'region_id'),
        Index(
            'targeting_regions_targeting_id_region_id_idx',
            'targeting_id',
            'region_id',
            unique=True,
        ),
        Index('targeting_regions_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    region_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    region: Mapped['OldRegions'] = relationship(
        'OldRegions', back_populates='targeting_old_regions'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_old_regions'
    )


class TargetingSegments(Base):
    __tablename__ = 'targeting_segments'
    __table_args__ = (
        ForeignKeyConstraint(
            ['segment_id'],
            ['segments.id'],
            ondelete='CASCADE',
            name='targeting_segments_segment_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            name='targeting_segments_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_segments_pkey'),
        Index('targeting_segments_created_at_idx', 'created_at'),
        Index('targeting_segments_segment_id_idx', 'segment_id'),
        Index(
            'targeting_segments_targeting_id_segment_id_idx',
            'targeting_id',
            'segment_id',
            unique=True,
        ),
        Index('targeting_segments_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    segment_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    segment: Mapped['Segments'] = relationship(
        'Segments', back_populates='targeting_segments'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_segments'
    )


class TargetingSrequests(Base):
    __tablename__ = 'targeting_srequests'
    __table_args__ = (
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_srequests_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_srequests_pkey'),
        Index('targeting_srequests_created_at_idx', 'created_at'),
        Index('targeting_srequests_targeting_id_idx', 'targeting_id'),
        Index(
            'targeting_srequests_targeting_id_lower_idx',
            'targeting_id',
            unique=True,
        ),
        Index('targeting_srequests_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_srequests'
    )


class TargetingTimePeriods(Base):
    __tablename__ = 'targeting_time_periods'
    __table_args__ = (
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_time_periods_targeting_id_fkey',
        ),
        ForeignKeyConstraint(
            ['time_period_id'],
            ['time_periods.id'],
            onupdate='CASCADE',
            name='targeting_time_periods_time_period_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_time_periods_pkey'),
        Index('targeting_time_periods_created_at_idx', 'created_at'),
        Index(
            'targeting_time_periods_targeting_id_time_period_id_idx',
            'targeting_id',
            'time_period_id',
            unique=True,
        ),
        Index('targeting_time_periods_time_period_id_idx', 'time_period_id'),
        Index('targeting_time_periods_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    time_period_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_time_periods'
    )
    time_period: Mapped['TimePeriods'] = relationship(
        'TimePeriods', back_populates='targeting_time_periods'
    )


class UtmParametersTemplates(Base):
    __tablename__ = 'utm_parameters_templates'
    __table_args__ = (
        ForeignKeyConstraint(
            ['department_id'],
            ['departments.id'],
            ondelete='CASCADE',
            name='utm_parameters_templates_department_id_fkey',
        ),
        ForeignKeyConstraint(
            ['parameter_id'],
            ['utm_parameters.id'],
            name='utm_parameters_templates_parameter_id_fkey',
        ),
        ForeignKeyConstraint(
            ['template_id'],
            ['utm_templates.id'],
            name='utm_parameters_templates_template_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='utm_parameters_templates_pkey'),
        Index('utm_parameters_templates_created_at_idx', 'created_at'),
        Index('utm_parameters_templates_department_id_idx', 'department_id'),
        Index(
            'utm_parameters_templates_parameter_id_template_id_departmen_idx',
            'parameter_id',
            'template_id',
            'department_id',
            unique=True,
        ),
        Index('utm_parameters_templates_template_id_idx', 'template_id'),
        Index('utm_parameters_templates_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    parameter_id = mapped_column(Uuid, nullable=False)
    template_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    department_id = mapped_column(Uuid)

    department: Mapped[Optional['Departments']] = relationship(
        'Departments', back_populates='utm_parameters_templates'
    )
    parameter: Mapped['UtmParameters'] = relationship(
        'UtmParameters', back_populates='utm_parameters_templates'
    )
    template: Mapped['UtmTemplates'] = relationship(
        'UtmTemplates', back_populates='utm_parameters_templates'
    )


class Cities(Base):
    __tablename__ = 'cities'
    __table_args__ = (
        ForeignKeyConstraint(
            ['region_id'],
            ['regions.id'],
            onupdate='CASCADE',
            name='cities_region_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='cities_pkey'),
        Index('cities_code_idx', 'code', unique=True),
        Index('cities_created_at_idx', 'created_at'),
        Index('cities_name_idx', 'name'),
        Index('cities_region_id_idx', 'region_id'),
        Index('cities_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    code = mapped_column(Text, nullable=False)
    name = mapped_column(Text, nullable=False)
    region_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    naming = mapped_column(Text, nullable=False)

    region: Mapped['Regions'] = relationship(
        'Regions', back_populates='cities'
    )
    targeting_cities: Mapped[List['TargetingCities']] = relationship(
        'TargetingCities', uselist=True, back_populates='city'
    )


class CreativePlugTemplates(Base):
    __tablename__ = 'creative_plug_templates'
    __table_args__ = (
        ForeignKeyConstraint(
            ['ad_format_id'],
            ['ad_formats.id'],
            name='creative_plug_templates_ad_format_id_fkey',
        ),
        ForeignKeyConstraint(
            ['ad_size_id'],
            ['ad_sizes.id'],
            name='creative_plug_templates_ad_size_id_fkey',
        ),
        ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            name='creative_plug_templates_product_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='creative_plug_templates_pkey'),
        Index('creative_plug_templates_ad_format_id_idx', 'ad_format_id'),
        Index('creative_plug_templates_ad_size_id_idx', 'ad_size_id'),
        Index('creative_plug_templates_created_at_idx', 'created_at'),
        Index('creative_plug_templates_name_idx', 'name'),
        Index('creative_plug_templates_naming_idx', 'naming'),
        Index('creative_plug_templates_product_id_idx', 'product_id'),
        Index('creative_plug_templates_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    product_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    ad_size_id = mapped_column(Uuid)
    ad_format_id = mapped_column(Uuid)

    ad_format: Mapped[Optional['AdFormats']] = relationship(
        'AdFormats', back_populates='creative_plug_templates'
    )
    ad_size: Mapped[Optional['AdSizes']] = relationship(
        'AdSizes', back_populates='creative_plug_templates'
    )
    product: Mapped['Products'] = relationship(
        'Products', back_populates='creative_plug_templates'
    )
    creative_plugs: Mapped[List['CreativePlugs']] = relationship(
        'CreativePlugs', uselist=True, back_populates='template'
    )


class IntegrationTokensHistory(Base):
    __tablename__ = 'integration_tokens_history'
    __table_args__ = (
        ForeignKeyConstraint(
            ['integration_token_id'],
            ['integration_tokens.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='integration_tokens_history_integration_token_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='integration_tokens_history_pkey'),
        Index('integration_tokens_history_created_at_idx', 'created_at'),
        Index('integration_tokens_history_event_date_idx', 'event_date'),
        Index(
            'integration_tokens_history_integration_token_id_idx',
            'integration_token_id',
        ),
        Index('integration_tokens_history_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    integration_token_id = mapped_column(Uuid, nullable=False)
    token_type = mapped_column(
        ENUM('token_type', 'ACCESS', 'REFRESH', name='token_type'),
        nullable=False,
    )
    event_date = mapped_column(DateTime(True), nullable=False)
    err_type = mapped_column(
        ENUM('token_err_type', 'ACCERR', 'ERR', name='token_err_type'),
        nullable=False,
    )
    err_description = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    integration_token: Mapped['IntegrationTokens'] = relationship(
        'IntegrationTokens', back_populates='integration_tokens_history'
    )


class OrganizationLinks(Base):
    __tablename__ = 'organization_links'
    __table_args__ = (
        ForeignKeyConstraint(
            ['brand_id'],
            ['brands.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='organization_links_brand_id_fkey',
        ),
        ForeignKeyConstraint(
            ['client_id'],
            ['clients.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='organization_links_client_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='organization_links_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['organization_id'],
            ['organizations.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='organization_links_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='organization_links_product_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='organization_links_pkey'),
        Index('organization_links_brand_id_idx', 'brand_id'),
        Index('organization_links_client_id_idx', 'client_id'),
        Index('organization_links_created_at_idx', 'created_at'),
        Index('organization_links_creator_user_id_idx', 'creator_user_id'),
        Index('organization_links_organization_id_idx', 'organization_id'),
        Index('organization_links_product_id_idx', 'product_id'),
        Index(
            'organization_links_unique_idx',
            'organization_id',
            'client_id',
            'brand_id',
            'product_id',
            unique=True,
        ),
        Index(
            'organization_links_unique_null_idx',
            'organization_id',
            'client_id',
            'brand_id',
            unique=True,
        ),
        Index('organization_links_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    organization_id = mapped_column(Uuid, nullable=False)
    client_id = mapped_column(Uuid, nullable=False)
    brand_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    product_id = mapped_column(Uuid)
    creator_user_id = mapped_column(Uuid)

    brand: Mapped['Brands'] = relationship(
        'Brands', back_populates='organization_links'
    )
    client: Mapped['Clients'] = relationship(
        'Clients', back_populates='organization_links'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='organization_links'
    )
    organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='organization_links'
    )
    product: Mapped[Optional['Products']] = relationship(
        'Products', back_populates='organization_links'
    )


class Placements(Base):
    __tablename__ = 'placements'
    __table_args__ = (
        CheckConstraint(
            'NOT (mplan_id IS NOT NULL AND is_template IS TRUE OR mplan_id IS NULL AND is_template IS NOT TRUE)',
            name='valid_template_check',
        ),
        CheckConstraint(
            'placement_type IS NOT NULL OR buy_type_id IS NULL',
            name='valid_buy_type_check',
        ),
        ForeignKeyConstraint(
            ['acl_organization_id'],
            ['organizations.id'],
            name='placements_acl_organization_id_fkey',
        ),
        ForeignKeyConstraint(
            ['ad_format_id'],
            ['ad_formats.id'],
            onupdate='CASCADE',
            name='placements_ad_format_id_fkey',
        ),
        ForeignKeyConstraint(
            ['ad_system_id'],
            ['ad_systems.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_ad_system_id_fkey',
        ),
        ForeignKeyConstraint(
            ['appsflyer_partner_id'],
            ['appsflyer_partners.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_appsflyer_partner_id_fkey',
        ),
        ForeignKeyConstraint(
            ['buy_type_id'],
            ['buy_types.id'],
            onupdate='CASCADE',
            name='placements_buy_type_id_fkey',
        ),
        ForeignKeyConstraint(
            ['channel_code'],
            ['channels.code'],
            onupdate='CASCADE',
            name='placements_channel_code_fkey',
        ),
        ForeignKeyConstraint(
            ['client_id'],
            ['clients.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_client_id_fkey',
        ),
        ForeignKeyConstraint(
            ['creator_user_id'],
            ['users.id'],
            onupdate='CASCADE',
            name='placements_creator_user_id_fkey',
        ),
        ForeignKeyConstraint(
            ['mplan_id'],
            ['mplans.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_mplan_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_status_id'],
            ['placement_statuses.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_placement_status_id_fkey',
        ),
        ForeignKeyConstraint(
            ['project_id'],
            ['projects.id'],
            onupdate='CASCADE',
            name='placements_project_id_fkey',
        ),
        ForeignKeyConstraint(
            ['seller_id'],
            ['sellers.id'],
            onupdate='CASCADE',
            name='placements_seller_id_fkey',
        ),
        ForeignKeyConstraint(
            ['site_element_id'],
            ['site_elements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_site_element_id_fkey',
        ),
        ForeignKeyConstraint(
            ['site_id'],
            ['sources.id'],
            onupdate='CASCADE',
            name='placements_site_id_fkey',
        ),
        ForeignKeyConstraint(
            ['site_integration_token_id'],
            ['integration_tokens.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_site_integration_token_id_fkey',
        ),
        ForeignKeyConstraint(
            ['site_section_id'],
            ['site_sections.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placements_site_section_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placements_pkey'),
        Index('placements_acl_organization_id_idx', 'acl_organization_id'),
        Index('placements_ad_format_id_idx', 'ad_format_id'),
        Index('placements_buy_type_id_idx', 'buy_type_id'),
        Index('placements_channel_code_idx', 'channel_code'),
        Index('placements_client_id_idx', 'client_id'),
        Index('placements_created_at_idx', 'created_at'),
        Index('placements_creator_user_id_idx', 'creator_user_id'),
        Index('placements_extra_naming_idx', 'extra_naming'),
        Index('placements_finish_on_idx', 'finish_on'),
        Index('placements_is_template_idx', 'is_template'),
        Index('placements_mplan_id_idx', 'mplan_id'),
        Index('placements_naming_idx', 'naming', unique=True),
        Index('placements_placement_status_at_idx', 'placement_status_at'),
        Index('placements_placement_status_id_idx', 'placement_status_id'),
        Index('placements_published_at_idx', 'published_at'),
        Index('placements_seller_id_idx', 'seller_id'),
        Index('placements_site_gather_method_idx', 'site_gather_method'),
        Index('placements_site_id_idx', 'site_id'),
        Index(
            'placements_site_integration_token_id_idx',
            'site_integration_token_id',
        ),
        Index('placements_site_publish_method_idx', 'site_publish_method'),
        Index('placements_start_on_idx', 'start_on'),
        Index('placements_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    placement_status_id = mapped_column(Uuid, nullable=False)
    name = mapped_column(Text, nullable=False)
    site_id = mapped_column(Uuid, nullable=False)
    start_on = mapped_column(Date, nullable=False)
    finish_on = mapped_column(Date, nullable=False)
    acl_organization_id = mapped_column(
        Uuid, nullable=False, comment='Доступ: принадлежность к организации'
    )
    placement_status_at = mapped_column(
        DateTime(True),
        nullable=False,
        server_default=text('now()'),
        comment='Дата установки текущего статуса',
    )
    seller_id = mapped_column(Uuid, nullable=False)
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    landing_type = mapped_column(
        ENUM(
            'landing_type',
            'WEB_LINK',
            'APPSFLYER_OL',
            'APPSFLYER_SPL',
            name='landing_type',
        ),
        nullable=False,
        server_default=text("'WEB_LINK'::postgresql.landing_type"),
    )
    is_template = mapped_column(
        Boolean,
        nullable=False,
        server_default=text('false'),
        comment='Признак, означающий, что размещение используется в качестве сценария',
    )
    site_integration_token_id = mapped_column(Uuid)
    naming = mapped_column(Text)
    landing_url = mapped_column(Text)
    buy_type_id = mapped_column(Uuid)
    ad_format_id = mapped_column(Uuid)
    ad_url = mapped_column(Text)
    utm_source = mapped_column(Text)
    utm_medium = mapped_column(Text)
    utm_campaign = mapped_column(Text)
    utm_term = mapped_column(Text)
    campaign_name = mapped_column(Text)
    adset_name = mapped_column(Text)
    site_publish_method = mapped_column(
        ENUM('publish_method', 'none', 'manual', 'auto', name='publish_method')
    )
    site_gather_method = mapped_column(
        ENUM('gather_method', 'manual', 'auto', name='gather_method')
    )
    published_at = mapped_column(DateTime(True))
    channel_code = mapped_column(Text)
    utm_content = mapped_column(Text)
    site_section_id = mapped_column(Uuid)
    site_element_id = mapped_column(Uuid)
    ad_system_id = mapped_column(Uuid)
    appsflyer_partner_id = mapped_column(Uuid)
    client_id = mapped_column(Uuid)
    extra_naming = mapped_column(Text)
    project_id = mapped_column(Uuid)
    pid = mapped_column(Text)
    af_channel = mapped_column(Text)
    c_parameter = mapped_column(Text)
    mplan_id = mapped_column(Uuid)
    placement_type = mapped_column(
        ENUM('placement_type', 'DYNAMIC', 'STATIC', name='placement_type')
    )
    creator_user_id = mapped_column(Uuid)

    acl_organization: Mapped['Organizations'] = relationship(
        'Organizations', back_populates='placements'
    )
    ad_format: Mapped[Optional['AdFormats']] = relationship(
        'AdFormats', back_populates='placements'
    )
    ad_system: Mapped[Optional['AdSystems']] = relationship(
        'AdSystems', back_populates='placements'
    )
    appsflyer_partner: Mapped[Optional['AppsflyerPartners']] = relationship(
        'AppsflyerPartners', back_populates='placements'
    )
    buy_type: Mapped[Optional['BuyTypes']] = relationship(
        'BuyTypes', back_populates='placements'
    )
    channels: Mapped[Optional['Channels']] = relationship(
        'Channels', back_populates='placements'
    )
    client: Mapped[Optional['Clients']] = relationship(
        'Clients', back_populates='placements'
    )
    creator_user: Mapped[Optional['Users']] = relationship(
        'Users', back_populates='placements'
    )
    mplan: Mapped[Optional['Mplans']] = relationship(
        'Mplans', back_populates='placements'
    )
    placement_status: Mapped['PlacementStatuses'] = relationship(
        'PlacementStatuses', back_populates='placements'
    )
    project: Mapped[Optional['Projects']] = relationship(
        'Projects', back_populates='placements'
    )
    seller: Mapped['Sellers'] = relationship(
        'Sellers', back_populates='placements'
    )
    site_element: Mapped[Optional['SiteElements']] = relationship(
        'SiteElements', back_populates='placements'
    )
    site: Mapped['Sources'] = relationship(
        'Sources', back_populates='placements'
    )
    site_integration_token: Mapped[
        Optional['IntegrationTokens']
    ] = relationship('IntegrationTokens', back_populates='placements')
    site_section: Mapped[Optional['SiteSections']] = relationship(
        'SiteSections', back_populates='placements'
    )
    creative_plugs: Mapped[List['CreativePlugs']] = relationship(
        'CreativePlugs', uselist=True, back_populates='placement'
    )
    placement_ad_sizes: Mapped[List['PlacementAdSizes']] = relationship(
        'PlacementAdSizes', uselist=True, back_populates='placement'
    )
    placement_appsflyer_parameters: Mapped[
        List['PlacementAppsflyerParameters']
    ] = relationship(
        'PlacementAppsflyerParameters',
        uselist=True,
        back_populates='placement',
    )
    placement_conversion_links: Mapped[
        List['PlacementConversionLinks']
    ] = relationship(
        'PlacementConversionLinks', uselist=True, back_populates='placement'
    )
    placement_creatives: Mapped[List['PlacementCreatives']] = relationship(
        'PlacementCreatives', uselist=True, back_populates='placement'
    )
    placement_platforms: Mapped[List['PlacementPlatforms']] = relationship(
        'PlacementPlatforms', uselist=True, back_populates='placement'
    )
    placement_targetings: Mapped[List['PlacementTargetings']] = relationship(
        'PlacementTargetings', uselist=True, back_populates='placement'
    )
    placement_tools: Mapped[List['PlacementTools']] = relationship(
        'PlacementTools', uselist=True, back_populates='placement'
    )
    placement_utm_parameters: Mapped[
        List['PlacementUtmParameters']
    ] = relationship(
        'PlacementUtmParameters', uselist=True, back_populates='placement'
    )
    placement_metrics: Mapped[List['PlacementMetrics']] = relationship(
        'PlacementMetrics', uselist=True, back_populates='placement'
    )

    def __repr__(self):
        return (
            f'<Placements({self.placement_status_id!r})'
        )


class PricePositions(Base):
    __tablename__ = 'price_positions'
    __table_args__ = (
        ForeignKeyConstraint(
            ['buy_type_id'],
            ['buy_types.id'],
            onupdate='CASCADE',
            name='price_positions_buy_type_id_fkey',
        ),
        ForeignKeyConstraint(
            ['channel_code'],
            ['channels.code'],
            onupdate='CASCADE',
            name='price_positions_channel_code_fkey',
        ),
        ForeignKeyConstraint(
            ['format_id'],
            ['ad_formats.id'],
            onupdate='CASCADE',
            name='price_positions_format_id_fkey',
        ),
        ForeignKeyConstraint(
            ['pricelist_id'],
            ['pricelists.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='price_positions_pricelist_id_fkey',
        ),
        ForeignKeyConstraint(
            ['region_id'],
            ['regions.id'],
            onupdate='CASCADE',
            name='price_positions_region_id_fkey',
        ),
        ForeignKeyConstraint(
            ['seller_id'],
            ['sellers.id'],
            onupdate='CASCADE',
            name='price_positions_seller_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='price_positions_pkey'),
        Index('price_positions_buy_type_id_idx', 'buy_type_id'),
        Index('price_positions_channel_code_idx', 'channel_code'),
        Index('price_positions_created_at_idx', 'created_at'),
        Index('price_positions_format_id_idx', 'format_id'),
        Index(
            'price_positions_pricelist_id_code_idx',
            'pricelist_id',
            'code',
            unique=True,
        ),
        Index('price_positions_region_id_idx', 'region_id'),
        Index('price_positions_seller_id_idx', 'seller_id'),
        Index('price_positions_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    pricelist_id = mapped_column(Uuid, nullable=False)
    code = mapped_column(Text, nullable=False)
    on_site_position = mapped_column(Text, nullable=False)
    channel_code = mapped_column(Text, nullable=False)
    buy_type_id = mapped_column(Uuid, nullable=False)
    price_without_vat = mapped_column(Numeric, nullable=False)
    vat_rate = mapped_column(Integer, nullable=False)
    media_rate = mapped_column(Numeric, nullable=False)
    guaranteed_capacity = mapped_column(Numeric, nullable=False)
    january_coef = mapped_column(Numeric, nullable=False)
    february_coef = mapped_column(Numeric, nullable=False)
    march_coef = mapped_column(Numeric, nullable=False)
    april_coef = mapped_column(Numeric, nullable=False)
    may_coef = mapped_column(Numeric, nullable=False)
    june_coef = mapped_column(Numeric, nullable=False)
    july_coef = mapped_column(Numeric, nullable=False)
    august_coef = mapped_column(Numeric, nullable=False)
    september_coef = mapped_column(Numeric, nullable=False)
    october_coef = mapped_column(Numeric, nullable=False)
    november_coef = mapped_column(Numeric, nullable=False)
    december_coef = mapped_column(Numeric, nullable=False)
    extra_charge_max_rate = mapped_column(Integer, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    seller_id = mapped_column(Uuid)
    region_id = mapped_column(Uuid)
    provider_position = mapped_column(Text)
    format_id = mapped_column(Uuid)
    placement_type = mapped_column(
        ENUM('placement_type', 'DYNAMIC', 'STATIC', name='placement_type')
    )
    default_geo_targeting = mapped_column(Text)
    default_frequency = mapped_column(Integer)
    extra_charge = mapped_column(Numeric)
    comment = mapped_column(Text)
    day_frequency_rate = mapped_column(Integer)
    week_frequency_rate = mapped_column(Integer)
    month_frequency_rate = mapped_column(Integer)
    rf_geo_rate = mapped_column(Integer)
    region_geo_rate = mapped_column(Integer)
    super_geo_rate = mapped_column(Integer)
    gender_rate = mapped_column(Integer)
    income_rate = mapped_column(Integer)
    interests_rate = mapped_column(Integer)
    platform_rate = mapped_column(Integer)
    cell_operator_rate = mapped_column(Integer)
    second_brand_rate = mapped_column(Integer)
    white_list_rate = mapped_column(Integer)
    brand_safety_rate = mapped_column(Integer)

    buy_type: Mapped['BuyTypes'] = relationship(
        'BuyTypes', back_populates='price_positions'
    )
    channels: Mapped['Channels'] = relationship(
        'Channels', back_populates='price_positions'
    )
    format: Mapped[Optional['AdFormats']] = relationship(
        'AdFormats', back_populates='price_positions'
    )
    pricelist: Mapped['Pricelists'] = relationship(
        'Pricelists', back_populates='price_positions'
    )
    region: Mapped[Optional['Regions']] = relationship(
        'Regions', back_populates='price_positions'
    )
    seller: Mapped[Optional['Sellers']] = relationship(
        'Sellers', back_populates='price_positions'
    )
    price_position_ad_sizes: Mapped[
        List['PricePositionAdSizes']
    ] = relationship(
        'PricePositionAdSizes', uselist=True, back_populates='price_position'
    )
    price_position_platforms: Mapped[
        List['PricePositionPlatforms']
    ] = relationship(
        'PricePositionPlatforms', uselist=True, back_populates='price_position'
    )
    price_position_sites: Mapped[List['PricePositionSites']] = relationship(
        'PricePositionSites', uselist=True, back_populates='price_position'
    )


class ProductSeasonalityValueLinks(Base):
    __tablename__ = 'product_seasonality_value_links'
    __table_args__ = (
        ForeignKeyConstraint(
            ['product_id'],
            ['products.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='product_seasonality_value_links_product_id_fkey',
        ),
        ForeignKeyConstraint(
            ['seasonality_value_id'],
            ['product_seasonality_values.id'],
            onupdate='CASCADE',
            name='product_seasonality_value_links_seasonality_value_id_fkey',
        ),
        PrimaryKeyConstraint(
            'id', name='product_seasonality_value_links_pkey'
        ),
        Index(
            'product_seasonality_value_lin_product_id_seasonality_value__idx',
            'product_id',
            'seasonality_value_id',
            unique=True,
        ),
        Index('product_seasonality_value_links_created_at_idx', 'created_at'),
        Index(
            'product_seasonality_value_links_seasonality_value_id_idx',
            'seasonality_value_id',
        ),
        Index('product_seasonality_value_links_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    product_id = mapped_column(Uuid, nullable=False)
    seasonality_value_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    product: Mapped['Products'] = relationship(
        'Products', back_populates='product_seasonality_value_links'
    )
    seasonality_value: Mapped['ProductSeasonalityValues'] = relationship(
        'ProductSeasonalityValues',
        back_populates='product_seasonality_value_links',
    )


class CreativePlugs(Base):
    __tablename__ = 'creative_plugs'
    __table_args__ = (
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            name='creative_plugs_placement_id_fkey',
        ),
        ForeignKeyConstraint(
            ['template_id'],
            ['creative_plug_templates.id'],
            ondelete='CASCADE',
            name='creative_plugs_template_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='creative_plugs_pkey'),
        Index('creative_plugs_created_at_idx', 'created_at'),
        Index('creative_plugs_landing_url_idx', 'landing_url'),
        Index('creative_plugs_link_url_idx', 'link_url'),
        Index('creative_plugs_name_idx', 'name'),
        Index('creative_plugs_naming_idx', 'naming'),
        Index('creative_plugs_placement_id_idx', 'placement_id'),
        Index('creative_plugs_template_id_idx', 'template_id'),
        Index('creative_plugs_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    name = mapped_column(Text, nullable=False)
    naming = mapped_column(Text, nullable=False)
    template_id = mapped_column(Uuid, nullable=False)
    placement_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    landing_url = mapped_column(Text)
    link_url = mapped_column(Text)

    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='creative_plugs'
    )
    template: Mapped['CreativePlugTemplates'] = relationship(
        'CreativePlugTemplates', back_populates='creative_plugs'
    )


class PlacementAdSizes(Base):
    __tablename__ = 'placement_ad_sizes'
    __table_args__ = (
        ForeignKeyConstraint(
            ['ad_size_id'],
            ['ad_sizes.id'],
            onupdate='CASCADE',
            name='placement_ad_sizes_ad_size_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_ad_sizes_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_ad_sizes_pkey'),
        Index('placement_ad_sizes_ad_size_id_idx', 'ad_size_id'),
        Index('placement_ad_sizes_created_at_idx', 'created_at'),
        Index(
            'placement_ad_sizes_placement_id_ad_size_id_idx',
            'placement_id',
            'ad_size_id',
            unique=True,
        ),
        Index('placement_ad_sizes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    ad_size_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    ad_size: Mapped['AdSizes'] = relationship(
        'AdSizes', back_populates='placement_ad_sizes'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_ad_sizes'
    )


class PlacementAppsflyerParameters(Base):
    __tablename__ = 'placement_appsflyer_parameters'
    __table_args__ = (
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_appsflyer_parameters_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_appsflyer_parameters_pkey'),
        Index('placement_appsflyer_parameters_created_at_idx', 'created_at'),
        Index(
            'placement_appsflyer_parameters_placement_id_idx', 'placement_id'
        ),
        Index('placement_appsflyer_parameters_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    retargeting = mapped_column(
        Boolean, nullable=False, server_default=text('true')
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    re_engagement_period = mapped_column(Text)
    attribution_window_period = mapped_column(Text)

    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_appsflyer_parameters'
    )


class PlacementConversionLinks(Base):
    __tablename__ = 'placement_conversion_links'
    __table_args__ = (
        ForeignKeyConstraint(
            ['mplan_conversion_id'],
            ['mplan_conversions.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_conversion_links_mplan_conversion_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_conversion_links_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_conversion_links_pkey'),
        Index('placement_conversion_links_created_at_idx', 'created_at'),
        Index('placement_conversion_links_is_main_idx', 'is_main'),
        Index(
            'placement_conversion_links_mplan_conversion_id_idx',
            'mplan_conversion_id',
        ),
        Index(
            'placement_conversion_links_unique_idx',
            'placement_id',
            'mplan_conversion_id',
            unique=True,
        ),
        Index('placement_conversion_links_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    mplan_conversion_id = mapped_column(Uuid, nullable=False)
    is_main = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    mplan_conversion: Mapped['MplanConversions'] = relationship(
        'MplanConversions', back_populates='placement_conversion_links'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_conversion_links'
    )
    placement_metrics: Mapped[List['PlacementMetrics']] = relationship(
        'PlacementMetrics',
        uselist=True,
        back_populates='placement_conversion_link',
    )


class PlacementCreatives(Base):
    __tablename__ = 'placement_creatives'
    __table_args__ = (
        ForeignKeyConstraint(
            ['creative_id'],
            ['creatives.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_creatives_creative_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_creatives_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_creatives_pkey'),
        Index('placement_creatives_creative_id_idx', 'creative_id'),
        Index('placement_creatives_hash_idx', 'hash'),
        Index('placement_creatives_is_active_idx', 'is_active'),
        Index('placement_creatives_name_idx', 'name'),
        Index('placement_creatives_placement_id_idx', 'placement_id'),
        Index(
            'placement_creatives_statistic_finish_on_idx',
            'statistic_finish_on',
        ),
        Index(
            'placement_creatives_statistic_start_on_idx', 'statistic_start_on'
        ),
        Index('placement_creatives_url_parameters_idx', 'url_parameters'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    creative_id = mapped_column(Uuid, nullable=False)
    placement_id = mapped_column(Uuid, nullable=False)
    is_active = mapped_column(
        Boolean, nullable=False, server_default=text('true')
    )
    name = mapped_column(Text)
    hash = mapped_column(Text)
    url_parameters = mapped_column(Text)
    statistic_start_on = mapped_column(Date)
    statistic_finish_on = mapped_column(Date)

    creative: Mapped['Creatives'] = relationship(
        'Creatives', back_populates='placement_creatives'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_creatives'
    )


class PlacementPlatforms(Base):
    __tablename__ = 'placement_platforms'
    __table_args__ = (
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_platforms_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_platforms_pkey'),
        Index('placement_platforms_created_at_idx', 'created_at'),
        Index(
            'placement_platforms_placement_id_platform_idx',
            'placement_id',
            'platform',
            unique=True,
        ),
        Index('placement_platforms_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    platform = mapped_column(
        ENUM('platform', 'DESKTOP', 'MOBILE', 'SMART_TV', name='platform'),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_platforms'
    )


class PlacementTargetings(Base):
    __tablename__ = 'placement_targetings'
    __table_args__ = (
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_targetings_placement_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            name='placement_targetings_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_targetings_pkey'),
        Index('placement_targetings_created_at_idx', 'created_at'),
        Index(
            'placement_targetings_placement_id_targeting_group_idx',
            'placement_id',
            'targeting_group',
            unique=True,
        ),
        Index(
            'placement_targetings_placement_id_targeting_id_idx',
            'placement_id',
            'targeting_id',
            unique=True,
        ),
        Index('placement_targetings_targeting_id_idx', 'targeting_id'),
        Index('placement_targetings_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    targeting_id = mapped_column(Uuid, nullable=False)
    targeting_group = mapped_column(
        ENUM(
            'targeting_group',
            'BASE',
            'GEO',
            'INTERESTS',
            name='targeting_group',
        ),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_targetings'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='placement_targetings'
    )


class PlacementTools(Base):
    __tablename__ = 'placement_tools'
    __table_args__ = (
        ForeignKeyConstraint(
            ['integration_token_id'],
            ['integration_tokens.id'],
            onupdate='CASCADE',
            name='placement_tools_integration_token_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_tools_placement_id_fkey',
        ),
        ForeignKeyConstraint(
            ['itool_id'],
            ['integration_tools.id'],
            onupdate='CASCADE',
            name='placement_tools_tool_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_tools_pkey'),
        Index('placement_tools_created_at_idx', 'created_at'),
        Index('placement_tools_gather_method_idx', 'gather_method'),
        Index(
            'placement_tools_integration_token_id_idx', 'integration_token_id'
        ),
        Index('placement_tools_lower_idx'),
        Index('placement_tools_placement_id_idx', 'placement_id'),
        Index(
            'placement_tools_placement_id_tool_type_idx',
            'placement_id',
            'tool_type',
            unique=True,
        ),
        Index('placement_tools_itool_id_idx', 'itool_id'),
        Index('placement_tools_tool_type_idx', 'tool_type'),
        Index('placement_tools_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    tool_type = mapped_column(
        ENUM(
            'source_type',
            'SITE',
            'POSTCLICK',
            'VERIFIER',
            'TRACKER',
            name='source_type',
        ),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    itool_id = mapped_column(Uuid, nullable=False)
    gather_method = mapped_column(
        ENUM('gather_method', 'manual', 'auto', name='gather_method')
    )
    integration_token_id = mapped_column(Uuid)
    counter_id = mapped_column(Text)

    integration_token: Mapped[Optional['IntegrationTokens']] = relationship(
        'IntegrationTokens', back_populates='placement_tools'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_tools'
    )
    integration_tool: Mapped[List['IntegrationTools']] = relationship(
        'IntegrationTools', uselist=True, back_populates='placement_tools'
    )
    applications: Mapped[List['Applications']] = relationship(
        'Applications', uselist=True, back_populates='placement_tool'
    )


class PlacementUtmParameters(Base):
    __tablename__ = 'placement_utm_parameters'
    __table_args__ = (
        ForeignKeyConstraint(
            ['parameter_id'],
            ['utm_parameters.id'],
            name='placement_utm_parameters_parameter_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_utm_parameters_placement_id_fkey',
        ),
        ForeignKeyConstraint(
            ['template_id'],
            ['utm_templates.id'],
            name='placement_utm_parameters_template_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_utm_parameters_pkey'),
        Index('placement_utm_parameters_created_at_idx', 'created_at'),
        Index('placement_utm_parameters_parameter_id_idx', 'parameter_id'),
        Index(
            'placement_utm_parameters_placement_id_parameter_id_idx',
            'placement_id',
            'parameter_id',
            unique=True,
        ),
        Index('placement_utm_parameters_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    parameter_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    arbitrary_value = mapped_column(
        Boolean, nullable=False, server_default=text('false')
    )
    template_id = mapped_column(Uuid)

    parameter: Mapped['UtmParameters'] = relationship(
        'UtmParameters', back_populates='placement_utm_parameters'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_utm_parameters'
    )
    template: Mapped[Optional['UtmTemplates']] = relationship(
        'UtmTemplates', back_populates='placement_utm_parameters'
    )


class PricePositionAdSizes(Base):
    __tablename__ = 'price_position_ad_sizes'
    __table_args__ = (
        ForeignKeyConstraint(
            ['price_position_id'],
            ['price_positions.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='price_position_ad_sizes_price_position_id_fkey',
        ),
        ForeignKeyConstraint(
            ['size_id'],
            ['ad_sizes.id'],
            onupdate='CASCADE',
            name='price_position_ad_sizes_size_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='price_position_ad_sizes_pkey'),
        Index('price_position_ad_sizes_created_at_idx', 'created_at'),
        Index(
            'price_position_ad_sizes_price_position_id_size_id_idx',
            'price_position_id',
            'size_id',
            unique=True,
        ),
        Index('price_position_ad_sizes_size_id_idx', 'size_id'),
        Index('price_position_ad_sizes_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    price_position_id = mapped_column(Uuid, nullable=False)
    size_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    price_position: Mapped['PricePositions'] = relationship(
        'PricePositions', back_populates='price_position_ad_sizes'
    )
    size: Mapped['AdSizes'] = relationship(
        'AdSizes', back_populates='price_position_ad_sizes'
    )


class PricePositionPlatforms(Base):
    __tablename__ = 'price_position_platforms'
    __table_args__ = (
        ForeignKeyConstraint(
            ['price_position_id'],
            ['price_positions.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='price_position_platforms_price_position_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='price_position_platforms_pkey'),
        Index('price_position_platforms_created_at_idx', 'created_at'),
        Index(
            'price_position_platforms_price_position_id_platform_idx',
            'price_position_id',
            'platform',
            unique=True,
        ),
        Index('price_position_platforms_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    price_position_id = mapped_column(Uuid, nullable=False)
    platform = mapped_column(
        ENUM('platform', 'DESKTOP', 'MOBILE', 'SMART_TV', name='platform'),
        nullable=False,
    )
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    price_position: Mapped['PricePositions'] = relationship(
        'PricePositions', back_populates='price_position_platforms'
    )


class PricePositionSites(Base):
    __tablename__ = 'price_position_sites'
    __table_args__ = (
        ForeignKeyConstraint(
            ['price_position_id'],
            ['price_positions.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='price_position_sites_price_position_id_fkey',
        ),
        ForeignKeyConstraint(
            ['site_id'],
            ['sources.id'],
            onupdate='CASCADE',
            name='price_position_sites_site_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='price_position_sites_pkey'),
        Index('price_position_sites_created_at_idx', 'created_at'),
        Index(
            'price_position_sites_price_position_id_site_id_idx',
            'price_position_id',
            'site_id',
            unique=True,
        ),
        Index('price_position_sites_site_id_idx', 'site_id'),
        Index('price_position_sites_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    price_position_id = mapped_column(Uuid, nullable=False)
    site_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )

    price_position: Mapped['PricePositions'] = relationship(
        'PricePositions', back_populates='price_position_sites'
    )
    site: Mapped['Sources'] = relationship(
        'Sources', back_populates='price_position_sites'
    )


class TargetingCities(Base):
    __tablename__ = 'targeting_cities'
    __table_args__ = (
        ForeignKeyConstraint(
            ['city_id'],
            ['cities.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='targeting_cities_city_id_fkey',
        ),
        ForeignKeyConstraint(
            ['targeting_id'],
            ['targetings.id'],
            ondelete='CASCADE',
            name='targeting_cities_targeting_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='targeting_cities_pkey'),
        Index('targeting_cities_city_id_idx', 'city_id'),
        Index('targeting_cities_created_at_idx', 'created_at'),
        Index(
            'targeting_cities_targeting_id_city_id_idx',
            'targeting_id',
            'city_id',
            unique=True,
        ),
        Index('targeting_cities_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    targeting_id = mapped_column(Uuid, nullable=False)
    city_id = mapped_column(Uuid, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )

    city: Mapped['Cities'] = relationship(
        'Cities', back_populates='targeting_cities'
    )
    targeting: Mapped['Targetings'] = relationship(
        'Targetings', back_populates='targeting_cities'
    )


class Applications(Base):
    __tablename__ = 'applications'
    __table_args__ = (
        ForeignKeyConstraint(
            ['placement_tool_id'],
            ['placement_tools.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='applications_placement_tool_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='applications_pkey'),
        Index('applications_app_id_idx', 'app_id'),
        Index('applications_created_at_idx', 'created_at'),
        Index(
            'applications_placement_tool_id_app_id_idx',
            'placement_tool_id',
            'app_id',
            unique=True,
        ),
        Index('applications_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_tool_id = mapped_column(Uuid, nullable=False)
    app_id = mapped_column(Text, nullable=False)
    app_name = mapped_column(Text, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    app_platform = mapped_column(Text)
    app_events = mapped_column(ARRAY(Text()))

    placement_tool: Mapped['PlacementTools'] = relationship(
        'PlacementTools', back_populates='applications'
    )


class PlacementMetrics(Base):
    __tablename__ = 'placement_metrics'
    __table_args__ = (
        ForeignKeyConstraint(
            ['metric_id'],
            ['metrics.id'],
            onupdate='CASCADE',
            name='placement_metrics_metric_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_conversion_link_id'],
            ['placement_conversion_links.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_metrics_placement_conversion_link_id_fkey',
        ),
        ForeignKeyConstraint(
            ['placement_id'],
            ['placements.id'],
            ondelete='CASCADE',
            onupdate='CASCADE',
            name='placement_metrics_placement_id_fkey',
        ),
        PrimaryKeyConstraint('id', name='placement_metrics_pkey'),
        Index('placement_metrics_created_at_idx', 'created_at'),
        Index('placement_metrics_is_calculated_idx', 'is_calculated'),
        Index('placement_metrics_metric_id_idx', 'metric_id'),
        Index(
            'placement_metrics_placement_conversion_link_id_idx',
            'placement_conversion_link_id',
        ),
        Index(
            'placement_metrics_unique_idx',
            'placement_id',
            'metric_id',
            unique=True,
        ),
        Index('placement_metrics_updated_at_idx', 'updated_at'),
    )

    id = mapped_column(Uuid, server_default=text('gen_random_uuid()'))
    placement_id = mapped_column(Uuid, nullable=False)
    metric_id = mapped_column(Uuid, nullable=False)
    value = mapped_column(Numeric, nullable=False)
    created_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    updated_at = mapped_column(
        DateTime(True), nullable=False, server_default=text('now()')
    )
    is_calculated = mapped_column(
        Boolean,
        nullable=False,
        server_default=text('false'),
        comment='Признак, означающий что значение метрики было автоматически рассчитано.',
    )
    order_no = mapped_column(
        BigInteger,
        Sequence('order_no_seq'),
        nullable=False,
    )
    placement_conversion_link_id = mapped_column(Uuid)

    metric: Mapped['Metrics'] = relationship(
        'Metrics', back_populates='placement_metrics'
    )
    placement_conversion_link: Mapped[
        Optional['PlacementConversionLinks']
    ] = relationship(
        'PlacementConversionLinks', back_populates='placement_metrics'
    )
    placement: Mapped['Placements'] = relationship(
        'Placements', back_populates='placement_metrics'
    )
