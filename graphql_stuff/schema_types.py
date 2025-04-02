from enum import Enum
from typing import Any, ClassVar, List, Optional, TypedDict

## Scalars

Time = Any
Decimal = Any
Upload = Any
JSON = Any
Date = Any

ReportMetaInterface = TypedDict(
    "ReportMetaInterface",
    {
        "label": Optional[str],
        "code": str,
        "extra": Optional["JSON"],
    },
)

MarketTarget = Enum("MarketTarget", "REACH PERFORMANCE BRANDFORMANCE")

CampaignCreateAction = Enum("CampaignCreateAction", "DRAFT PLANNING")
TokenStatus = Enum("TokenStatus", "ACTIVE NOT_ACTIVE")
IToolType = Enum("IToolType", "SITE POSTCLICK VERIFIER TRACKER")
ItokenStatusType = Enum("ItokenStatusType", "ERROR OK RETRY NOTFOUND")
YandexService = Enum("YandexService", "DIRECT METRIC")
MediaType = Enum("MediaType", "TV DIGITAL OUTDOOR")
MetricType = Enum("MetricType", "QUANTITATIVE PRICE BENCHMARKS")
LandingType = Enum("LandingType", "WEB_LINK APPSFLYER_OL APPSFLYER_SPL")
OrganizationLinkField = Enum(
    "OrganizationLinkField", "clientName brandName productName"
)

OrganizationStatus = Enum("OrganizationStatus", "new active blocked")
OrganizationRole = Enum("OrganizationRole", "agency client")
OrganizationSortField = Enum(
    "OrganizationSortField",
    "fullName inn kpp address phone status registeredAt blockedAt",
)

PlacementCalcEventAction = Enum("PlacementCalcEventAction", "ADD DELETE")
TrackingMethod = Enum("TrackingMethod", "PIXEL_SHOWS PIXEL_CLICKS")
PricelistType = Enum("PricelistType", "FEDERAL REGIONAL AUCTION")
PricelistStatus = Enum("PricelistStatus", "CREATED APPROVED ACTIVE")
PricelistField = Enum("PricelistField", "type status startOn finishOn")
PricePositionField = Enum("PricePositionField", "code priceWithoutVat")
Platform = Enum("Platform", "DESKTOP MOBILE SMART_TV")
PlacementType = Enum("PlacementType", "DYNAMIC STATIC")
UserStatus = Enum("UserStatus", "NEW ACTIVE BLOCKED")
ProfileSortField = Enum(
    "ProfileSortField",
    "login surname name email orgName status registeredAt blockedAt",
)
ProjectPlatform = Enum("ProjectPlatform", "WEB APP")
ReportMetaMetricType = Enum("ReportMetaMetricType", "float integer percent")
SortDirection = Enum("SortDirection", "asc desc")
OperationType = Enum("OperationType", "gt lt")
PublishMethod = Enum("PublishMethod", "none manual auto")
GatherMethod = Enum("GatherMethod", "MANUAL AUTO")
TVOperationType = Enum("TVOperationType", "eq gt lt range_gt range_lt")
SourceType = Enum("SourceType", "SITE POSTCLICK VERIFIER TRACKER")
SourceStatus = Enum("SourceStatus", "active paused deleted")
SourceToolType = Enum("SourceToolType", "POSTCLICK VERIFIER TRACKER")
DataEventType = Enum("DataEventType", "CampaignCreate CampaignUpdate CampaignDelete")
TplPlacementType = Enum("TplPlacementType", "DYNAMIC STATIC")
TplPlatform = Enum("TplPlatform", "DESKTOP MOBILE SMART_TV")
TplOperationType = Enum("TplOperationType", "gt lt")

AdFormat = TypedDict(
    "AdFormat",
    {
        "id": str,
        "name": str,
        "naming": str,
        "code": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdSize = TypedDict(
    "AdSize",
    {
        "id": str,
        "name": str,
        "code": str,
        "naming": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdSystem = TypedDict(
    "AdSystem",
    {
        "id": str,
        "name": str,
        "naming": str,
    },
)

AdminInfo = TypedDict(
    "AdminInfo",
    {
        "id": str,
        "name": Optional[str],
        "email": Optional[str],
        "phone": Optional[str],
        "login": Optional[str],
        "registeredAt": Optional["Time"],
    },
)

Agency = TypedDict(
    "Agency",
    {
        "id": str,
        "name": str,
        "naming": str,
    },
)

AppsflyerPartner = TypedDict(
    "AppsflyerPartner",
    {
        "id": str,
        "name": str,
        "identifier": str,
        "accountName": Optional[str],
        "adID": Optional[str],
    },
)

BrandAwareness = TypedDict(
    "BrandAwareness",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

Brand = TypedDict(
    "Brand",
    {
        "id": str,
        "name": str,
        "clients": List["Client"],
        "naming": str,
        "code": str,
        "awareness": Optional["BrandAwareness"],
        "createdAt": "Time",
        "updatedAt": "Time",
        "organization": "Organization",
    },
)

BuyType = TypedDict(
    "BuyType",
    {
        "id": str,
        "name": str,
        "naming": str,
        "code": str,
        "unit": str,
        "placementType": "PlacementType",
        "orderNo": int,
    },
)

CampaignStatus = TypedDict(
    "CampaignStatus",
    {
        "id": str,
        "name": str,
        "code": str,
    },
)

Campaign = TypedDict(
    "Campaign",
    {
        "id": str,
        "name": str,
        "code": Optional[str],
        "status": "CampaignStatus",
        "client": "Client",
        "brand": "Brand",
        "product": "Product",
        "coBrands": List["Brand"],
        "agency": Optional["Agency"],
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
        "documents": List["CampaignDoc"],
        "createdAt": "Time",
        "updatedAt": "Time",
        "uniqueNamingPart": Optional[str],
        "approvedMplan": Optional["Mplan"],
        "isReportReady": Optional[bool],
        "budget": Optional["Decimal"],
        "department": Optional["Department"],
        "marketTarget": Optional["MarketTarget"],
        "targetAudience": Optional[str],
        "targetGeo": Optional[str],
        "conditions": Optional[str],
        "representative": Optional["Person"],
        "canRepresentativeSetEmpty": bool,
    },
)

CampaignDoc = TypedDict(
    "CampaignDoc",
    {
        "id": str,
        "code": str,
        "name": str,
        "path": str,
        "size": int,
    },
)

Candidate = TypedDict(
    "Candidate",
    {
        "id": str,
        "name": str,
        "surname": str,
        "email": str,
        "firmName": str,
        "phone": str,
        "role": str,
        "comments": Optional[str],
        "isPerformed": bool,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

Channel = TypedDict(
    "Channel",
    {
        "name": str,
        "code": str,
        "naming": str,
        "mediaType": "MediaType",
        "isUsedBySplan": bool,
    },
)

Client = TypedDict(
    "Client",
    {
        "id": str,
        "name": str,
        "naming": str,
        "code": str,
        "fullName": Optional[str],
        "inn": Optional[str],
        "kpp": Optional[str],
        "organization": "Organization",
    },
)

Creative = TypedDict(
    "Creative",
    {
        "id": str,
        "name": str,
        "naming": str,
        "hash": str,
        "fileMetadata": Optional["CreativeFileMetadata"],
        "frameID": str,
        "adSize": Optional["AdSize"],
        "isLinked": bool,
    },
)

PlacementCreative = TypedDict(
    "PlacementCreative",
    {
        "id": str,
        "name": str,
        "naming": str,
        "hash": str,
        "url": Optional[str],
        "creative": "Creative",
    },
)

CreativeFileMetadata = TypedDict(
    "CreativeFileMetadata",
    {
        "externalFileID": str,
        "width": int,
        "height": int,
        "size": int,
        "type": str,
    },
)

CreativeFrame = TypedDict(
    "CreativeFrame",
    {
        "id": str,
        "name": str,
        "naming": str,
        "creatives": List["Creative"],
    },
)

PlacementCreativeFrame = TypedDict(
    "PlacementCreativeFrame",
    {
        "id": str,
        "name": str,
        "naming": str,
        "creatives": List["Creative"],
    },
)

Department = TypedDict(
    "Department",
    {
        "id": str,
        "name": str,
        "naming": str,
        "code": str,
    },
)

DigitalReportFilterData = TypedDict(
    "DigitalReportFilterData",
    {
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
    },
)

DigitalReport = TypedDict(
    "DigitalReport",
    {
        "report": "Report",
        "updatedAt": Optional["Time"],
        "filterData": "DigitalReportFilterData",
    },
)

Service = TypedDict(
    "Service",
    {
        "name": str,
        "version": str,
        "schema": str,
    },
)

Goal = TypedDict(
    "Goal",
    {
        "id": str,
        "name": str,
        "code": str,
        "metrics": List["Metric"],
        "naming": str,
    },
)

IntegrationToken = TypedDict(
    "IntegrationToken",
    {
        "id": str,
        "iTool": "IntegrationTool",
        "account": str,
        "status": "TokenStatus",
        "expiredAt": "Time",
    },
)

IntegrationTool = TypedDict(
    "IntegrationTool",
    {
        "id": str,
        "name": str,
        "code": str,
        "type": "IToolType",
    },
)

ItokenStatus = TypedDict(
    "ItokenStatus",
    {
        "state": str,
        "message": str,
        "status": "ItokenStatusType",
        "tokenID": Optional[str],
    },
)

FactConversion = TypedDict(
    "FactConversion",
    {
        "id": str,
        "name": str,
        "sourceCode": str,
    },
)

MatchedConversionsTable = TypedDict(
    "MatchedConversionsTable",
    {
        "landingURLs": List[str],
        "integrationTool": "IntegrationTool",
        "counterID": str,
        "placementNames": List[str],
        "matchedConversions": List["PlanFactConversion"],
        "factConversions": List["FactConversion"],
    },
)

PlanFactConversion = TypedDict(
    "PlanFactConversion",
    {
        "id": Optional[str],
        "mplanConversion": "MplanConversion",
        "factConversion": Optional["FactConversion"],
    },
)

Metric = TypedDict(
    "Metric",
    {
        "name": str,
        "description": Optional[str],
        "code": str,
        "operation": "OperationType",
        "unit": "Unit",
        "precision": int,
        "canSplit": bool,
        "isConversion": bool,
        "isTracker": bool,
        "type": "MetricType",
    },
)

MplanConversion = TypedDict(
    "MplanConversion",
    {
        "id": str,
        "name": str,
    },
)

Mplan = TypedDict(
    "Mplan",
    {
        "id": str,
        "orderNo": int,
        "campaign": "Campaign",
        "status": "MplanStatus",
        "constraints": List["MplanConstraint"],
        "landings": List["MplanLanding"],
        "placementsCount": int,
        "conversions": List["MplanConversion"],
        "budget": "MplanBudget",
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

MplanStatus = TypedDict(
    "MplanStatus",
    {
        "id": dict,
        "name": str,
        "code": str,
    },
)

MplanBudget = TypedDict(
    "MplanBudget",
    {
        "remainingSum": "Decimal",
        "sum": "Decimal",
        "campaignHasBudget": bool,
        "hasMetric": bool,
    },
)

MplanConstraint = TypedDict(
    "MplanConstraint",
    {
        "id": str,
        "metric": "Metric",
        "operation": "OperationType",
        "value": "Decimal",
    },
)

MplanLanding = TypedDict(
    "MplanLanding",
    {
        "id": str,
        "url": str,
        "type": "LandingType",
    },
)

MplanDataUpload = TypedDict(
    "MplanDataUpload",
    {
        "id": str,
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
        "uploadedAt": "Time",
        "source": "Source",
        "placements": List["Placement"],
        "uploader": "Person",
    },
)

ImportValidationProblem = TypedDict(
    "ImportValidationProblem",
    {
        "group": str,
        "cell": str,
        "value": str,
        "problem": str,
    },
)

NavBar = TypedDict(
    "NavBar",
    {
        "horizontalMenu": List["NavBarItem"],
        "userMenu": List["NavBarItem"],
    },
)

NavBarItem = TypedDict(
    "NavBarItem",
    {
        "title": str,
        "code": str,
        "path": str,
    },
)

OrganizationLink = TypedDict(
    "OrganizationLink",
    {
        "id": str,
        "organization": "Organization",
        "client": "Client",
        "brand": "Brand",
        "product": Optional["Product"],
    },
)

Organization = TypedDict(
    "Organization",
    {
        "id": str,
        "role": "OrganizationRole",
        "status": "OrganizationStatus",
        "okopf": Optional[str],
        "fullName": str,
        "shortName": str,
        "firmName": Optional[str],
        "inn": str,
        "ogrn": Optional[str],
        "kpp": Optional[str],
        "address": Optional[str],
        "phone": Optional[str],
        "email": str,
        "registeredAt": Optional["Time"],
        "blockedAt": Optional["Time"],
    },
)

PlacementComment = TypedDict(
    "PlacementComment",
    {
        "id": str,
        "text": str,
        "placementID": str,
        "creator": "Person",
        "createdAt": "Time",
    },
)

PlacementMetricList = TypedDict(
    "PlacementMetricList",
    {
        "metrics": List["PlacementMetric"],
        "conversionLinks": List["PlacementConversionLink"],
    },
)

PlacementMetric = TypedDict(
    "PlacementMetric",
    {
        "id": str,
        "placementID": str,
        "metric": "Metric",
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementConversionLink = TypedDict(
    "PlacementConversionLink",
    {
        "id": str,
        "placementID": str,
        "mplanConversion": "MplanConversion",
        "isMain": bool,
        "metrics": List["PlacementMetric"],
    },
)

PlacementPricing = TypedDict(
    "PlacementPricing",
    {
        "placementID": str,
        "pricePerUnit": "Decimal",
        "numberOfUnitsPerPeriod": "Decimal",
        "markupForFrequency": "Decimal",
        "markupForPlatform": "Decimal",
        "markupForGeotargeting": "Decimal",
        "markupForGenderAge": "Decimal",
        "markupForSeasonality": "Decimal",
        "markupForCurrencyTransfer": "Decimal",
        "markupForOther": "Decimal",
        "mediaDiscount": "Decimal",
        "vat": "Decimal",
        "calculated": "PlacementPricingCalculated",
    },
)

PlacementPricingCalculated = TypedDict(
    "PlacementPricingCalculated",
    {
        "totalByMarkup": "Decimal",
        "costPlacementWithoutVAT": "Decimal",
        "costPlacementWithVAT": "Decimal",
    },
)

PlacementStatus = TypedDict(
    "PlacementStatus",
    {
        "id": str,
        "name": str,
        "code": str,
    },
)

PlacementStatusHistory = TypedDict(
    "PlacementStatusHistory",
    {
        "id": str,
        "oldStatus": Optional["PlacementStatus"],
        "status": "PlacementStatus",
        "comment": Optional["PlacementComment"],
        "creator": "Person",
        "time": "Time",
    },
)

PlacementStatusProgress = TypedDict(
    "PlacementStatusProgress",
    {
        "status": "PlacementStatus",
        "history": Optional["PlacementStatusHistory"],
        "reached": bool,
    },
)

PlacementTargeting = TypedDict(
    "PlacementTargeting",
    {
        "targetAudience": Optional[str],
        "targetGeo": Optional[str],
    },
)

PlacementTool = TypedDict(
    "PlacementTool",
    {
        "id": str,
        "placementID": str,
        "type": "IToolType",
        "gatherMethod": Optional["GatherMethod"],
        "publishMethod": Optional["PublishMethod"],
        "trackingMethod": Optional["TrackingMethod"],
        "iToken": Optional["IntegrationToken"],
        "iTool": Optional["IntegrationTool"],
        "apps": Optional[List["PlacementToolApp"]],
        "counterID": Optional[str],
    },
)

PlacementToolApp = TypedDict(
    "PlacementToolApp",
    {
        "id": str,
        "applicationID": str,
        "applicationName": str,
        "applicationPlatform": Optional[str],
        "inAppEvents": Optional[List[str]],
    },
)

AppsflyerApp = TypedDict(
    "AppsflyerApp",
    {
        "applicationID": str,
        "applicationName": str,
        "applicationPlatform": str,
    },
)

PlacementCalcMetrics = TypedDict(
    "PlacementCalcMetrics",
    {
        "metrics": List["PlacementCalcMetric"],
        "conversions": List["PlacementCalcConversion"],
        "mplanBudget": Optional["MplanBudget"],
    },
)

PlacementCalcMetric = TypedDict(
    "PlacementCalcMetric",
    {
        "id": Optional[str],
        "metricCode": str,
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementCalcConversion = TypedDict(
    "PlacementCalcConversion",
    {
        "id": str,
        "isMain": bool,
        "metrics": List["PlacementCalcMetric"],
    },
)

Placement = TypedDict(
    "Placement",
    {
        "id": str,
        "mplan": Optional["Mplan"],
        "status": "PlacementStatus",
        "name": str,
        "naming": Optional[str],
        "extraNaming": Optional[str],
        "site": "Source",
        "startOn": "Time",
        "finishOn": "Time",
        "landingURL": Optional[str],
        "channel": Optional["Channel"],
        "buyType": Optional["BuyType"],
        "adFormat": Optional["AdFormat"],
        "adSizes": List["AdSize"],
        "createdAt": "Time",
        "updatedAt": "Time",
        "publishedAt": Optional["Time"],
        "campaignName": Optional[str],
        "adsetName": Optional[str],
        "adURL": Optional[str],
        "siteSection": Optional["SiteSection"],
        "siteElement": Optional["SiteElement"],
        "adSystem": Optional["AdSystem"],
        "appsflyerPartner": Optional["AppsflyerPartner"],
        "landingType": "LandingType",
        "appsflyerParameter": Optional["PlacementAppsflyerParameter"],
        "project": Optional["Project"],
        "placementType": Optional["PlacementType"],
        "platforms": List["Platform"],
        "seller": "Seller",
        "timekeeping": Optional[int],
        "creativesCount": int,
        "budget": "Decimal",
        "tools": List["PlacementTool"],
    },
)

MplanStatusCount = TypedDict(
    "MplanStatusCount",
    {
        "id": str,
        "count": int,
    },
)

PlacementChannelsCount = TypedDict(
    "PlacementChannelsCount",
    {
        "channel": Optional["Channel"],
        "count": int,
    },
)

PlacementAppsflyerParameter = TypedDict(
    "PlacementAppsflyerParameter",
    {
        "id": str,
        "placementID": str,
        "retargeting": bool,
        "reEngagementPeriod": Optional[str],
        "attributionWindowPeriod": Optional[str],
    },
)

Pricelist = TypedDict(
    "Pricelist",
    {
        "id": str,
        "client": "Client",
        "code": str,
        "type": "PricelistType",
        "startOn": "Time",
        "finishOn": "Time",
        "createdAt": "Time",
        "creator": "Person",
        "status": "PricelistStatus",
        "approvedAt": Optional["Time"],
        "approver": Optional["Person"],
        "comments": Optional[str],
    },
)

PricePosition = TypedDict(
    "PricePosition",
    {
        "id": str,
        "pricelistID": str,
        "code": str,
        "seller": Optional["Seller"],
        "region": Optional[str],
        "providerPosition": Optional[str],
        "sites": List["Source"],
        "onSitePosition": str,
        "channel": "Channel",
        "format": Optional["AdFormat"],
        "sizes": List["AdSize"],
        "placementType": Optional["PlacementType"],
        "buyType": "BuyType",
        "platforms": List["Platform"],
        "defaultGeoTargeting": Optional[str],
        "defaultFrequency": Optional[int],
        "priceWithoutVat": "Decimal",
        "vatRate": int,
        "mediaRate": "Decimal",
        "extraCharge": Optional["Decimal"],
        "guaranteedCapacity": "Decimal",
        "comment": Optional[str],
        "januaryCoef": "Decimal",
        "februaryCoef": "Decimal",
        "marchCoef": "Decimal",
        "aprilCoef": "Decimal",
        "mayCoef": "Decimal",
        "juneCoef": "Decimal",
        "julyCoef": "Decimal",
        "augustCoef": "Decimal",
        "septemberCoef": "Decimal",
        "octoberCoef": "Decimal",
        "novemberCoef": "Decimal",
        "decemberCoef": "Decimal",
        "extraChargeMaxRate": int,
        "dayFrequencyRate": Optional[int],
        "weekFrequencyRate": Optional[int],
        "monthFrequencyRate": Optional[int],
        "rfGeoRate": Optional[int],
        "regionGeoRate": Optional[int],
        "superGeoRate": Optional[int],
        "genderRate": Optional[int],
        "incomeRate": Optional[int],
        "interestsRate": Optional[int],
        "platformRate": Optional[int],
        "cellOperatorRate": Optional[int],
        "secondBrandRate": Optional[int],
        "whiteListRate": Optional[int],
        "brandSafetyRate": Optional[int],
    },
)

ProductCategory = TypedDict(
    "ProductCategory",
    {
        "id": str,
        "name": str,
        "code": str,
        "type": "ProductType",
        "isUsedBySplan": bool,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductGeography = TypedDict(
    "ProductGeography",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductPriceCategory = TypedDict(
    "ProductPriceCategory",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductPurchaseFrequency = TypedDict(
    "ProductPurchaseFrequency",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductSeasonality = TypedDict(
    "ProductSeasonality",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductSeasonalityValue = TypedDict(
    "ProductSeasonalityValue",
    {
        "id": str,
        "name": str,
        "code": str,
        "productSeasonalityID": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

ProductType = TypedDict(
    "ProductType",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

Product = TypedDict(
    "Product",
    {
        "id": str,
        "name": str,
        "brands": List["Brand"],
        "naming": str,
        "code": str,
        "deepLink": Optional[str],
        "geography": Optional["ProductGeography"],
        "type": Optional["ProductType"],
        "category": Optional["ProductCategory"],
        "priceCategory": Optional["ProductPriceCategory"],
        "seasonality": Optional["ProductSeasonality"],
        "seasonalityValues": List["ProductSeasonalityValue"],
        "purchaseFrequency": Optional["ProductPurchaseFrequency"],
        "createdAt": "Time",
        "updatedAt": "Time",
        "organization": "Organization",
    },
)

User = TypedDict(
    "User",
    {
        "id": str,
        "status": "UserStatus",
        "login": str,
        "email": str,
        "phone": str,
        "registeredAt": Optional["Time"],
        "blockedAt": Optional["Time"],
    },
)

UserRole = TypedDict(
    "UserRole",
    {
        "id": str,
        "code": str,
        "name": str,
        "description": str,
    },
)

Person = TypedDict(
    "Person",
    {
        "id": str,
        "organizationID": str,
        "name": Optional[str],
        "surname": Optional[str],
        "middleName": Optional[str],
        "contactPhone": Optional[str],
    },
)

Profile = TypedDict(
    "Profile",
    {
        "user": "User",
        "person": "Person",
        "roles": List["UserRole"],
        "organization": "Organization",
    },
)

Project = TypedDict(
    "Project",
    {
        "id": str,
        "name": str,
        "url": Optional[str],
        "platform": "ProjectPlatform",
        "naming": str,
    },
)

Report = TypedDict(
    "Report",
    {
        "report": "ReportInfo",
        "meta": "ReportMeta",
        "data": List["ReportData"],
    },
)

ReportInfo = TypedDict(
    "ReportInfo",
    {
        "label": Optional[str],
        "code": str,
    },
)

ReportMeta = TypedDict(
    "ReportMeta",
    {
        "dimensions": List["ReportMetaDimension"],
        "metrics": List["ReportMetaMetric"],
    },
)

ReportData = TypedDict(
    "ReportData",
    {
        "children": List["ReportData"],
        "dimensions": List["ReportDataDimension"],
        "metrics": List[str],
    },
)

ReportDataDimension = TypedDict(
    "ReportDataDimension",
    {
        "label": Optional[str],
        "code": str,
        "extra": Optional["JSON"],
    },
)

Seller = TypedDict(
    "Seller",
    {
        "id": str,
        "name": str,
        "code": str,
        "naming": str,
        "sources": List["Source"],
    },
)

SiteElement = TypedDict(
    "SiteElement",
    {
        "id": str,
        "name": str,
        "naming": str,
    },
)

SiteSection = TypedDict(
    "SiteSection",
    {
        "id": str,
        "name": str,
        "naming": str,
    },
)

Source = TypedDict(
    "Source",
    {
        "id": str,
        "name": str,
        "shortName": str,
        "hasAdset": bool,
        "code": str,
        "naming": str,
        "url": str,
        "type": "SourceType",
        "status": "SourceStatus",
        "publishMethod": "PublishMethod",
        "canAutoGather": bool,
        "seller": Optional["Seller"],
        "adSizes": List["SourceAdSize"],
        "buyTypes": List["SourceBuyType"],
    },
)

SourceAdSize = TypedDict(
    "SourceAdSize",
    {
        "adFormat": "AdFormat",
        "adSize": "AdSize",
    },
)

SourceBuyType = TypedDict(
    "SourceBuyType",
    {
        "adFormat": "AdFormat",
        "buyType": "BuyType",
    },
)

SMPAudience = TypedDict(
    "SMPAudience",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

SMPCommunication = TypedDict(
    "SMPCommunication",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

SMPCompetitorStrategy = TypedDict(
    "SMPCompetitorStrategy",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

SMPGoal = TypedDict(
    "SMPGoal",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

SMPProductKnowledge = TypedDict(
    "SMPProductKnowledge",
    {
        "id": str,
        "name": str,
        "code": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

StratPlan = TypedDict(
    "StratPlan",
    {
        "id": str,
        "client": "SMPDefaultEntity",
        "brand": "SMPDefaultEntity",
        "product": Optional["SMPDefaultEntity"],
        "productCategory": Optional["SMPDefaultEntity"],
        "smpGoal": "SMPGoal",
        "smpCompetitorStrategy": "SMPCompetitorStrategy",
        "dateStart": "Date",
        "dateEnd": "Date",
        "smpAudience": "SMPAudience",
        "hasSubAudience": bool,
        "smpProductKnowledge": "SMPProductKnowledge",
        "smpCommunication": "SMPCommunication",
        "createdAt": "Time",
        "updatedAt": "Time",
        "averageCampaignCost": Optional["Decimal"],
        "averageWeekCost": Optional["Decimal"],
        "averageWeekWeight": Optional["Decimal"],
        "mediaMixText": Optional[str],
        "recommendedCampaignCost": Optional["Decimal"],
        "channelsCosts": Optional[List["ChannelsCost"]],
        "metricsValues": Optional[List["MetricsValue"]],
    },
)

SMPDefaultEntity = TypedDict(
    "SMPDefaultEntity",
    {
        "id": str,
        "name": str,
        "code": str,
    },
)

ChannelsCost = TypedDict(
    "ChannelsCost",
    {
        "id": str,
        "channelName": str,
        "cost": "Decimal",
        "rate": "Decimal",
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

MetricsValue = TypedDict(
    "MetricsValue",
    {
        "id": str,
        "metricName": str,
        "value": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

DataEvent = TypedDict(
    "DataEvent",
    {
        "id": str,
        "name": "DataEventType",
    },
)

Subscription = TypedDict(
    "Subscription",
    {
        "dataEvents": "DataEventsSubscriptionResult",
    },
)

DataEventsSubscriptionResult = ClassVar["DataEvent"]

TVCampaign = TypedDict(
    "TVCampaign",
    {
        "id": str,
        "name": str,
        "status": str,
        "client": "Client",
        "brand": Optional["Brand"],
        "product": Optional["Product"],
        "startOn": "Time",
        "finishOn": "Time",
        "marketTargets": Optional[str],
        "targetAudience": Optional[str],
        "conditions": Optional[str],
        "createdAt": "Time",
        "updatedAt": "Time",
        "orderNo": int,
    },
)

TVMetric = TypedDict(
    "TVMetric",
    {
        "code": str,
        "isLimit": bool,
        "name": str,
        "unitCode": str,
        "op": "TVOperationType",
        "precision": int,
        "canSplit": bool,
        "orderNo": int,
        "description": str,
    },
)

TVMplanGoal = TypedDict(
    "TVMplanGoal",
    {
        "name": str,
        "code": str,
        "message": str,
        "effectiveFrequencyAble": bool,
    },
)

TVMplan = TypedDict(
    "TVMplan",
    {
        "id": str,
        "campaignID": str,
        "status": str,
        "goal": "TVMplanGoal",
        "constraints": List["TVMplanConstraint"],
        "orderNo": int,
    },
)

TVMplanConstraint = TypedDict(
    "TVMplanConstraint",
    {
        "id": str,
        "metricCode": str,
        "op": "TVOperationType",
        "value": "Decimal",
    },
)

Unit = TypedDict(
    "Unit",
    {
        "code": str,
        "name": str,
        "shortName": str,
        "orderNo": int,
    },
)

UtmParameter = TypedDict(
    "UtmParameter",
    {
        "id": str,
        "code": str,
        "name": str,
        "templates": List["UtmTemplate"],
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

UtmTemplate = TypedDict(
    "UtmTemplate",
    {
        "id": str,
        "code": str,
        "name": str,
        "instruction": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

PlacementUtmParameter = TypedDict(
    "PlacementUtmParameter",
    {
        "parameter": "UtmParameter",
        "arbitraryValue": bool,
        "template": Optional["UtmTemplate"],
        "value": str,
    },
)

PlacementUtmParameters = TypedDict(
    "PlacementUtmParameters",
    {
        "parameters": List["PlacementUtmParameter"],
        "adURL": str,
    },
)

XlsDoc = TypedDict(
    "XlsDoc",
    {
        "name": str,
        "path": str,
    },
)

PlacementTemplateMetric = TypedDict(
    "PlacementTemplateMetric",
    {
        "id": str,
        "metric": "Metric",
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementTemplateConversion = TypedDict(
    "PlacementTemplateConversion",
    {
        "id": str,
        "name": Optional[str],
        "isMain": bool,
        "metrics": List["PlacementTemplateMetric"],
    },
)

PlacementTemplateMetricList = TypedDict(
    "PlacementTemplateMetricList",
    {
        "metrics": List["PlacementTemplateMetric"],
        "conversions": List["PlacementTemplateConversion"],
    },
)

MplanTemplate = TypedDict(
    "MplanTemplate",
    {
        "id": str,
        "name": str,
        "client": "Client",
        "constraints": List["MplanTemplateConstraint"],
        "landings": List[str],
        "placementTemplatesCount": int,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

MplanTemplateConstraint = TypedDict(
    "MplanTemplateConstraint",
    {
        "id": str,
        "metric": "Metric",
        "operation": "TplOperationType",
        "value": "Decimal",
    },
)

PlacementTemplate = TypedDict(
    "PlacementTemplate",
    {
        "id": str,
        "name": str,
        "client": "Client",
        "site": "Source",
        "seller": "Seller",
        "channel": Optional["Channel"],
        "placementType": Optional["TplPlacementType"],
        "buyType": Optional["BuyType"],
        "adFormat": Optional["AdFormat"],
        "adSizes": List["AdSize"],
        "platforms": List["TplPlatform"],
        "target_audience": str,
        "target_geo": str,
        "createdAt": "Time",
        "updatedAt": "Time",
    },
)

Mutation = TypedDict(
    "Mutation",
    {
        "adminAdFormatCreate": "AdminAdFormatCreateMutationResult",
        "adminAdFormatUpdate": "AdminAdFormatUpdateMutationResult",
        "adminAdFormatDelete": "AdminAdFormatDeleteMutationResult",
        "adminAdSizeUpdate": "AdminAdSizeUpdateMutationResult",
        "adminAdSizeCreate": "AdminAdSizeCreateMutationResult",
        "adminAdSizeDelete": "AdminAdSizeDeleteMutationResult",
        "adSystemCreate": "AdSystemCreateMutationResult",
        "adminCreate": "AdminCreateMutationResult",
        "adminUpdate": "AdminUpdateMutationResult",
        "adminDelete": "AdminDeleteMutationResult",
        "agencyCreate": "AgencyCreateMutationResult",
        "appsflyerPartnerCreate": "AppsflyerPartnerCreateMutationResult",
        "adminBrandAwarenessUpdate": "AdminBrandAwarenessUpdateMutationResult",
        "adminBrandCreate": "AdminBrandCreateMutationResult",
        "adminBrandUpdate": "AdminBrandUpdateMutationResult",
        "adminBrandDelete": "AdminBrandDeleteMutationResult",
        "brandUpdate": "BrandUpdateMutationResult",
        "brandDelete": "BrandDeleteMutationResult",
        "brandCreate": "BrandCreateMutationResult",
        "adminBuyTypeCreate": "AdminBuyTypeCreateMutationResult",
        "adminBuyTypeUpdate": "AdminBuyTypeUpdateMutationResult",
        "adminBuyTypeDelete": "AdminBuyTypeDeleteMutationResult",
        "adminCampaignStatusUpdate": "AdminCampaignStatusUpdateMutationResult",
        "campaignCreate": "CampaignCreateMutationResult",
        "campaignUpdate": "CampaignUpdateMutationResult",
        "campaignDelete": "CampaignDeleteMutationResult",
        "campaignDocUpload": "CampaignDocUploadMutationResult",
        "campaignDocDelete": "CampaignDocDeleteMutationResult",
        "campaignCancel": "CampaignCancelMutationResult",
        "adminCandidateDelete": "AdminCandidateDeleteMutationResult",
        "adminChannelCreate": "AdminChannelCreateMutationResult",
        "adminChannelUpdate": "AdminChannelUpdateMutationResult",
        "adminClientCreate": "AdminClientCreateMutationResult",
        "adminClientUpdate": "AdminClientUpdateMutationResult",
        "adminClientDelete": "AdminClientDeleteMutationResult",
        "clientCreate": "ClientCreateMutationResult",
        "clientUpdate": "ClientUpdateMutationResult",
        "clientDelete": "ClientDeleteMutationResult",
        "creativeCreate": "CreativeCreateMutationResult",
        "creativeUpdate": "CreativeUpdateMutationResult",
        "creativesDelete": "CreativesDeleteMutationResult",
        "creativesExclude": "CreativesExcludeMutationResult",
        "creativeFileAttach": "CreativeFileAttachMutationResult",
        "creativeFileDetach": "CreativeFileDetachMutationResult",
        "creativeFrameCreate": "CreativeFrameCreateMutationResult",
        "creativeFrameDelete": "CreativeFrameDeleteMutationResult",
        "creativeFrameExclude": "CreativeFrameExcludeMutationResult",
        "placementCreativesCreate": "PlacementCreativesCreateMutationResult",
        "placementCreativesUpdate": "PlacementCreativesUpdateMutationResult",
        "placementCreativesDelete": "PlacementCreativesDeleteMutationResult",
        "placementCreativesExclude": "PlacementCreativesExcludeMutationResult",
        "placementCreativeFileAttach": "PlacementCreativeFileAttachMutationResult",
        "adminGoalCreate": "AdminGoalCreateMutationResult",
        "adminGoalUpdate": "AdminGoalUpdateMutationResult",
        "adminGoalDelete": "AdminGoalDeleteMutationResult",
        "integrationTokenSave": "IntegrationTokenSaveMutationResult",
        "adRiverAuth": "AdRiverAuthMutationResult",
        "matchedConversionsSave": "MatchedConversionsSaveMutationResult",
        "adminMetricUpdate": "AdminMetricUpdateMutationResult",
        "mplanConversionCreate": "MplanConversionCreateMutationResult",
        "mplanConversionUpdate": "MplanConversionUpdateMutationResult",
        "mplanConversionDelete": "MplanConversionDeleteMutationResult",
        "mplanDraftCreate": "MplanDraftCreateMutationResult",
        "mplanDraftSave": "MplanDraftSaveMutationResult",
        "mplanDelete": "MplanDeleteMutationResult",
        "mplanPlanningCreate": "MplanPlanningCreateMutationResult",
        "mplanLandingAdd": "MplanLandingAddMutationResult",
        "mplanDataUploadImport": "MplanDataUploadImportMutationResult",
        "mplanFromTemplateCreate": "MplanFromTemplateCreateMutationResult",
        "mplanXLSImport": "MplanXLSImportMutationResult",
        "adminOrganizationLinkCreate": "AdminOrganizationLinkCreateMutationResult",
        "adminOrganizationLinkDelete": "AdminOrganizationLinkDeleteMutationResult",
        "organizationLinkCreate": "OrganizationLinkCreateMutationResult",
        "organizationLinkDelete": "OrganizationLinkDeleteMutationResult",
        "adminOrganizationCreate": "AdminOrganizationCreateMutationResult",
        "adminOrganizationUpdate": "AdminOrganizationUpdateMutationResult",
        "adminOrganizationBlock": "AdminOrganizationBlockMutationResult",
        "adminOrganizationActivate": "AdminOrganizationActivateMutationResult",
        "organizationUpdate": "OrganizationUpdateMutationResult",
        "placementCommentSave": "PlacementCommentSaveMutationResult",
        "placementMetricsSave": "PlacementMetricsSaveMutationResult",
        "placementPricingSave": "PlacementPricingSaveMutationResult",
        "adminPlacementStatusUpdate": "AdminPlacementStatusUpdateMutationResult",
        "placementTargetingSave": "PlacementTargetingSaveMutationResult",
        "placementToolsSave": "PlacementToolsSaveMutationResult",
        "placementToolPostClickUpdate": "PlacementToolPostClickUpdateMutationResult",
        "placementCreate": "PlacementCreateMutationResult",
        "placementSave": "PlacementSaveMutationResult",
        "placementExclude": "PlacementExcludeMutationResult",
        "placementDelete": "PlacementDeleteMutationResult",
        "placementPublish": "PlacementPublishMutationResult",
        "placementSetupIncomplete": "PlacementSetupIncompleteMutationResult",
        "placementSetupComplete": "PlacementSetupCompleteMutationResult",
        "placementDuplicate": "PlacementDuplicateMutationResult",
        "placementsApprove": "PlacementsApproveMutationResult",
        "placementsRequestApproval": "PlacementsRequestApprovalMutationResult",
        "placementRejectedRequestApproval": "PlacementRejectedRequestApprovalMutationResult",
        "representativePlacementApprove": "RepresentativePlacementApproveMutationResult",
        "representativePlacementReject": "RepresentativePlacementRejectMutationResult",
        "placementFromTemplateCreate": "PlacementFromTemplateCreateMutationResult",
        "pricelistCreate": "PricelistCreateMutationResult",
        "pricelistUpdate": "PricelistUpdateMutationResult",
        "pricelistDelete": "PricelistDeleteMutationResult",
        "pricePositionCreate": "PricePositionCreateMutationResult",
        "pricePositionUpdate": "PricePositionUpdateMutationResult",
        "pricePositionDelete": "PricePositionDeleteMutationResult",
        "adminProductCategoryCreate": "AdminProductCategoryCreateMutationResult",
        "adminProductCategoryUpdate": "AdminProductCategoryUpdateMutationResult",
        "adminProductGeographyUpdate": "AdminProductGeographyUpdateMutationResult",
        "adminProductPriceCategoryUpdate": "AdminProductPriceCategoryUpdateMutationResult",
        "adminProductPurchaseFrequencyUpdate": "AdminProductPurchaseFrequencyUpdateMutationResult",
        "adminProductSeasonalityUpdate": "AdminProductSeasonalityUpdateMutationResult",
        "adminProductSeasonalityValueUpdate": "AdminProductSeasonalityValueUpdateMutationResult",
        "adminProductTypeUpdate": "AdminProductTypeUpdateMutationResult",
        "adminProductCreate": "AdminProductCreateMutationResult",
        "adminProductUpdate": "AdminProductUpdateMutationResult",
        "adminProductDelete": "AdminProductDeleteMutationResult",
        "productCreate": "ProductCreateMutationResult",
        "productUpdate": "ProductUpdateMutationResult",
        "productDelete": "ProductDeleteMutationResult",
        "myProfileUpdate": "MyProfileUpdateMutationResult",
        "profileCreate": "ProfileCreateMutationResult",
        "profileUpdate": "ProfileUpdateMutationResult",
        "profileBlock": "ProfileBlockMutationResult",
        "profileActivate": "ProfileActivateMutationResult",
        "adminProfileCreate": "AdminProfileCreateMutationResult",
        "adminProfileUpdate": "AdminProfileUpdateMutationResult",
        "adminProfileBlock": "AdminProfileBlockMutationResult",
        "adminProfileActivate": "AdminProfileActivateMutationResult",
        "adminSellerUpdate": "AdminSellerUpdateMutationResult",
        "siteElementCreate": "SiteElementCreateMutationResult",
        "siteSectionCreate": "SiteSectionCreateMutationResult",
        "adminSourceSiteCreate": "AdminSourceSiteCreateMutationResult",
        "adminSourceSiteUpdate": "AdminSourceSiteUpdateMutationResult",
        "adminSourceToolCreate": "AdminSourceToolCreateMutationResult",
        "adminSourceToolUpdate": "AdminSourceToolUpdateMutationResult",
        "stratPlanSave": "StratPlanSaveMutationResult",
        "stratPlanUpdate": "StratPlanUpdateMutationResult",
        "stratPlanDelete": "StratPlanDeleteMutationResult",
        "tvCampaignDraftCreate": "TvCampaignDraftCreateMutationResult",
        "tvCampaignDraftSave": "TvCampaignDraftSaveMutationResult",
        "tvCampaignPlanningCreate": "TvCampaignPlanningCreateMutationResult",
        "tvCampaignDelete": "TvCampaignDeleteMutationResult",
        "tvCampaignCancel": "TvCampaignCancelMutationResult",
        "tvMplanDraftCreate": "TvMplanDraftCreateMutationResult",
        "tvMplanDraftSave": "TvMplanDraftSaveMutationResult",
        "tvMplanCreate": "TvMplanCreateMutationResult",
        "tvMplanDelete": "TvMplanDeleteMutationResult",
        "adminUnitUpsert": "AdminUnitUpsertMutationResult",
        "placementUtmParametersSave": "PlacementUtmParametersSaveMutationResult",
        "templateFromMplanCreate": "TemplateFromMplanCreateMutationResult",
        "mplanTemplateUpdate": "MplanTemplateUpdateMutationResult",
        "mplanTemplateDelete": "MplanTemplateDeleteMutationResult",
        "templateFromPlacementCreate": "TemplateFromPlacementCreateMutationResult",
        "placementTemplateCreate": "PlacementTemplateCreateMutationResult",
        "placementTemplateUpdate": "PlacementTemplateUpdateMutationResult",
        "placementTemplateDelete": "PlacementTemplateDeleteMutationResult",
    },
)

AdminAdFormatCreateParams = TypedDict(
    "AdminAdFormatCreateParams",
    {
        "data": "AdminAdFormatCreateData",
    },
)

AdminAdFormatCreateMutationResult = ClassVar["AdFormat"]

AdminAdFormatUpdateParams = TypedDict(
    "AdminAdFormatUpdateParams",
    {
        "id": str,
        "data": "AdminAdFormatUpdateData",
    },
)

AdminAdFormatUpdateMutationResult = ClassVar["AdFormat"]

AdminAdFormatDeleteParams = TypedDict(
    "AdminAdFormatDeleteParams",
    {
        "id": str,
    },
)

AdminAdFormatDeleteMutationResult = bool

AdminAdSizeUpdateParams = TypedDict(
    "AdminAdSizeUpdateParams",
    {
        "id": str,
        "data": "AdminAdSizeUpdateData",
    },
)

AdminAdSizeUpdateMutationResult = ClassVar["AdSize"]

AdminAdSizeCreateParams = TypedDict(
    "AdminAdSizeCreateParams",
    {
        "data": "AdminAdSizeCreateData",
    },
)

AdminAdSizeCreateMutationResult = ClassVar["AdSize"]

AdminAdSizeDeleteParams = TypedDict(
    "AdminAdSizeDeleteParams",
    {
        "id": str,
    },
)

AdminAdSizeDeleteMutationResult = bool

AdSystemCreateParams = TypedDict(
    "AdSystemCreateParams",
    {
        "data": "AdSystemData",
    },
)

AdSystemCreateMutationResult = ClassVar["AdSystem"]

AdminCreateParams = TypedDict(
    "AdminCreateParams",
    {
        "data": "AdminData",
    },
)

AdminCreateMutationResult = ClassVar["AdminInfo"]

AdminUpdateParams = TypedDict(
    "AdminUpdateParams",
    {
        "id": str,
        "data": "AdminData",
    },
)

AdminUpdateMutationResult = ClassVar["AdminInfo"]

AdminDeleteParams = TypedDict(
    "AdminDeleteParams",
    {
        "id": str,
    },
)

AdminDeleteMutationResult = bool

AgencyCreateParams = TypedDict(
    "AgencyCreateParams",
    {
        "data": "AgencyData",
    },
)

AgencyCreateMutationResult = ClassVar["Agency"]

AppsflyerPartnerCreateParams = TypedDict(
    "AppsflyerPartnerCreateParams",
    {
        "data": "AppsflyerPartnerData",
    },
)

AppsflyerPartnerCreateMutationResult = ClassVar["AppsflyerPartner"]

AdminBrandAwarenessUpdateParams = TypedDict(
    "AdminBrandAwarenessUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminBrandAwarenessUpdateMutationResult = ClassVar[Optional["BrandAwareness"]]

AdminBrandCreateParams = TypedDict(
    "AdminBrandCreateParams",
    {
        "organizationID": str,
        "data": "BrandData",
    },
)

AdminBrandCreateMutationResult = ClassVar["Brand"]

AdminBrandUpdateParams = TypedDict(
    "AdminBrandUpdateParams",
    {
        "id": str,
        "data": "BrandData",
    },
)

AdminBrandUpdateMutationResult = ClassVar["Brand"]

AdminBrandDeleteParams = TypedDict(
    "AdminBrandDeleteParams",
    {
        "id": str,
    },
)

AdminBrandDeleteMutationResult = bool

BrandUpdateParams = TypedDict(
    "BrandUpdateParams",
    {
        "id": str,
        "data": "BrandData",
    },
)

BrandUpdateMutationResult = ClassVar["Brand"]

BrandDeleteParams = TypedDict(
    "BrandDeleteParams",
    {
        "id": str,
    },
)

BrandDeleteMutationResult = bool

BrandCreateParams = TypedDict(
    "BrandCreateParams",
    {
        "clientID": Optional[str],
        "data": "BrandData",
    },
)

BrandCreateMutationResult = ClassVar["Brand"]

AdminBuyTypeCreateParams = TypedDict(
    "AdminBuyTypeCreateParams",
    {
        "data": "AdminBuyTypeCreateData",
    },
)

AdminBuyTypeCreateMutationResult = ClassVar["BuyType"]

AdminBuyTypeUpdateParams = TypedDict(
    "AdminBuyTypeUpdateParams",
    {
        "id": str,
        "data": "AdminBuyTypeUpdateData",
    },
)

AdminBuyTypeUpdateMutationResult = ClassVar["BuyType"]

AdminBuyTypeDeleteParams = TypedDict(
    "AdminBuyTypeDeleteParams",
    {
        "id": str,
    },
)

AdminBuyTypeDeleteMutationResult = bool

AdminCampaignStatusUpdateParams = TypedDict(
    "AdminCampaignStatusUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminCampaignStatusUpdateMutationResult = ClassVar[Optional["CampaignStatus"]]

CampaignCreateParams = TypedDict(
    "CampaignCreateParams",
    {
        "action": "CampaignCreateAction",
        "data": "CampaignData",
        "draftID": Optional[str],
    },
)

CampaignCreateMutationResult = ClassVar["Campaign"]

CampaignUpdateParams = TypedDict(
    "CampaignUpdateParams",
    {
        "id": str,
        "data": "CampaignData",
    },
)

CampaignUpdateMutationResult = ClassVar["Campaign"]

CampaignDeleteParams = TypedDict(
    "CampaignDeleteParams",
    {
        "id": str,
    },
)

CampaignDeleteMutationResult = bool

CampaignDocUploadParams = TypedDict(
    "CampaignDocUploadParams",
    {
        "data": "CampaignDocData",
    },
)

CampaignDocUploadMutationResult = ClassVar[Optional["CampaignDoc"]]

CampaignDocDeleteParams = TypedDict(
    "CampaignDocDeleteParams",
    {
        "id": str,
    },
)

CampaignDocDeleteMutationResult = bool

CampaignCancelParams = TypedDict(
    "CampaignCancelParams",
    {
        "id": str,
    },
)

CampaignCancelMutationResult = bool

AdminCandidateDeleteParams = TypedDict(
    "AdminCandidateDeleteParams",
    {
        "id": str,
    },
)

AdminCandidateDeleteMutationResult = bool

AdminChannelCreateParams = TypedDict(
    "AdminChannelCreateParams",
    {
        "data": "ChannelCreateData",
    },
)

AdminChannelCreateMutationResult = ClassVar["Channel"]

AdminChannelUpdateParams = TypedDict(
    "AdminChannelUpdateParams",
    {
        "code": str,
        "data": "ChannelUpdateData",
    },
)

AdminChannelUpdateMutationResult = ClassVar["Channel"]

AdminClientCreateParams = TypedDict(
    "AdminClientCreateParams",
    {
        "data": "AdminClientCreateData",
    },
)

AdminClientCreateMutationResult = ClassVar["Client"]

AdminClientUpdateParams = TypedDict(
    "AdminClientUpdateParams",
    {
        "id": str,
        "data": "ClientData",
    },
)

AdminClientUpdateMutationResult = ClassVar["Client"]

AdminClientDeleteParams = TypedDict(
    "AdminClientDeleteParams",
    {
        "id": str,
    },
)

AdminClientDeleteMutationResult = bool

ClientCreateParams = TypedDict(
    "ClientCreateParams",
    {
        "data": "ClientData",
    },
)

ClientCreateMutationResult = ClassVar["Client"]

ClientUpdateParams = TypedDict(
    "ClientUpdateParams",
    {
        "id": str,
        "data": "ClientData",
    },
)

ClientUpdateMutationResult = ClassVar["Client"]

ClientDeleteParams = TypedDict(
    "ClientDeleteParams",
    {
        "id": str,
    },
)

ClientDeleteMutationResult = bool

CreativeCreateParams = TypedDict(
    "CreativeCreateParams",
    {
        "data": "CreativeCreateData",
    },
)

CreativeCreateMutationResult = ClassVar["Creative"]

CreativeUpdateParams = TypedDict(
    "CreativeUpdateParams",
    {
        "data": "CreativeUpdateData",
    },
)

CreativeUpdateMutationResult = ClassVar["Creative"]

CreativesDeleteParams = TypedDict(
    "CreativesDeleteParams",
    {
        "ids": List[str],
    },
)

CreativesDeleteMutationResult = bool

CreativesExcludeParams = TypedDict(
    "CreativesExcludeParams",
    {
        "ids": List[str],
    },
)

CreativesExcludeMutationResult = bool

CreativeFileAttachParams = TypedDict(
    "CreativeFileAttachParams",
    {
        "data": "CreativeFileAttachData",
    },
)

CreativeFileAttachMutationResult = ClassVar["Creative"]

CreativeFileDetachParams = TypedDict(
    "CreativeFileDetachParams",
    {
        "creativeID": str,
    },
)

CreativeFileDetachMutationResult = ClassVar["Creative"]

CreativeFrameCreateParams = TypedDict(
    "CreativeFrameCreateParams",
    {
        "data": "CreativeFrameCreateData",
    },
)

CreativeFrameCreateMutationResult = ClassVar["CreativeFrame"]

CreativeFrameDeleteParams = TypedDict(
    "CreativeFrameDeleteParams",
    {
        "id": str,
    },
)

CreativeFrameDeleteMutationResult = bool

CreativeFrameExcludeParams = TypedDict(
    "CreativeFrameExcludeParams",
    {
        "id": str,
    },
)

CreativeFrameExcludeMutationResult = bool

PlacementCreativesCreateParams = TypedDict(
    "PlacementCreativesCreateParams",
    {
        "data": "PlacementCreativesCreateData",
    },
)

PlacementCreativesCreateMutationResult = ClassVar[List["PlacementCreative"]]

PlacementCreativesUpdateParams = TypedDict(
    "PlacementCreativesUpdateParams",
    {
        "data": List["PlacementCreativeUpdateData"],
    },
)

PlacementCreativesUpdateMutationResult = ClassVar[List["PlacementCreative"]]

PlacementCreativesDeleteParams = TypedDict(
    "PlacementCreativesDeleteParams",
    {
        "ids": List[str],
    },
)

PlacementCreativesDeleteMutationResult = bool

PlacementCreativesExcludeParams = TypedDict(
    "PlacementCreativesExcludeParams",
    {
        "ids": List[str],
    },
)

PlacementCreativesExcludeMutationResult = bool

PlacementCreativeFileAttachParams = TypedDict(
    "PlacementCreativeFileAttachParams",
    {
        "data": "PlacementCreativeFileAttachData",
    },
)

PlacementCreativeFileAttachMutationResult = ClassVar["PlacementCreative"]

AdminGoalCreateParams = TypedDict(
    "AdminGoalCreateParams",
    {
        "data": "GoalData",
    },
)

AdminGoalCreateMutationResult = ClassVar["Goal"]

AdminGoalUpdateParams = TypedDict(
    "AdminGoalUpdateParams",
    {
        "id": str,
        "data": "GoalData",
    },
)

AdminGoalUpdateMutationResult = ClassVar["Goal"]

AdminGoalDeleteParams = TypedDict(
    "AdminGoalDeleteParams",
    {
        "id": str,
    },
)

AdminGoalDeleteMutationResult = bool

IntegrationTokenSaveParams = TypedDict(
    "IntegrationTokenSaveParams",
    {
        "data": "IntegrationTokenData",
    },
)

IntegrationTokenSaveMutationResult = ClassVar["IntegrationToken"]

AdRiverAuthParams = TypedDict(
    "AdRiverAuthParams",
    {
        "login": str,
        "password": str,
    },
)

AdRiverAuthMutationResult = str

MatchedConversionsSaveParams = TypedDict(
    "MatchedConversionsSaveParams",
    {
        "mplanID": str,
        "data": List["MatchedConversionsData"],
    },
)

MatchedConversionsSaveMutationResult = ClassVar[List["MatchedConversionsTable"]]

AdminMetricUpdateParams = TypedDict(
    "AdminMetricUpdateParams",
    {
        "code": str,
        "data": "MetricData",
    },
)

AdminMetricUpdateMutationResult = ClassVar[Optional["Metric"]]

MplanConversionCreateParams = TypedDict(
    "MplanConversionCreateParams",
    {
        "data": "MplanConversionData",
    },
)

MplanConversionCreateMutationResult = ClassVar[Optional["MplanConversion"]]

MplanConversionUpdateParams = TypedDict(
    "MplanConversionUpdateParams",
    {
        "id": str,
        "data": "MplanConversionData",
    },
)

MplanConversionUpdateMutationResult = ClassVar[Optional["MplanConversion"]]

MplanConversionDeleteParams = TypedDict(
    "MplanConversionDeleteParams",
    {
        "id": str,
    },
)

MplanConversionDeleteMutationResult = bool

MplanDraftCreateParams = TypedDict(
    "MplanDraftCreateParams",
    {
        "data": "MplanData",
    },
)

MplanDraftCreateMutationResult = ClassVar["Mplan"]

MplanDraftSaveParams = TypedDict(
    "MplanDraftSaveParams",
    {
        "id": str,
        "data": "MplanData",
    },
)

MplanDraftSaveMutationResult = ClassVar["Mplan"]

MplanDeleteParams = TypedDict(
    "MplanDeleteParams",
    {
        "id": str,
    },
)

MplanDeleteMutationResult = bool

MplanPlanningCreateParams = TypedDict(
    "MplanPlanningCreateParams",
    {
        "draftID": Optional[str],
        "data": "MplanData",
    },
)

MplanPlanningCreateMutationResult = ClassVar["Mplan"]

MplanLandingAddParams = TypedDict(
    "MplanLandingAddParams",
    {
        "data": "MplanLandingData",
    },
)

MplanLandingAddMutationResult = ClassVar["MplanLanding"]

MplanDataUploadImportParams = TypedDict(
    "MplanDataUploadImportParams",
    {
        "data": "MplanDataUploadImportData",
    },
)

MplanDataUploadImportMutationResult = bool

MplanFromTemplateCreateParams = TypedDict(
    "MplanFromTemplateCreateParams",
    {
        "templateID": str,
        "data": "MplanFromTemplateData",
    },
)

MplanFromTemplateCreateMutationResult = ClassVar["Mplan"]

MplanXLSImportParams = TypedDict(
    "MplanXLSImportParams",
    {
        "data": "MplanXLSImportData",
    },
)

MplanXLSImportMutationResult = ClassVar[List["ImportValidationProblem"]]

AdminOrganizationLinkCreateParams = TypedDict(
    "AdminOrganizationLinkCreateParams",
    {
        "data": "AdminOrganizationLinkData",
    },
)

AdminOrganizationLinkCreateMutationResult = ClassVar["OrganizationLink"]

AdminOrganizationLinkDeleteParams = TypedDict(
    "AdminOrganizationLinkDeleteParams",
    {
        "id": str,
    },
)

AdminOrganizationLinkDeleteMutationResult = bool

OrganizationLinkCreateParams = TypedDict(
    "OrganizationLinkCreateParams",
    {
        "data": "OrganizationLinkData",
    },
)

OrganizationLinkCreateMutationResult = ClassVar["OrganizationLink"]

OrganizationLinkDeleteParams = TypedDict(
    "OrganizationLinkDeleteParams",
    {
        "id": str,
    },
)

OrganizationLinkDeleteMutationResult = bool

AdminOrganizationCreateParams = TypedDict(
    "AdminOrganizationCreateParams",
    {
        "data": "OrganizationData",
    },
)

AdminOrganizationCreateMutationResult = ClassVar["Organization"]

AdminOrganizationUpdateParams = TypedDict(
    "AdminOrganizationUpdateParams",
    {
        "id": str,
        "data": "OrganizationData",
    },
)

AdminOrganizationUpdateMutationResult = ClassVar["Organization"]

AdminOrganizationBlockParams = TypedDict(
    "AdminOrganizationBlockParams",
    {
        "id": str,
    },
)

AdminOrganizationBlockMutationResult = ClassVar["Organization"]

AdminOrganizationActivateParams = TypedDict(
    "AdminOrganizationActivateParams",
    {
        "id": str,
    },
)

AdminOrganizationActivateMutationResult = ClassVar["Organization"]

OrganizationUpdateParams = TypedDict(
    "OrganizationUpdateParams",
    {
        "data": "OrganizationData",
    },
)

OrganizationUpdateMutationResult = ClassVar["Organization"]

PlacementCommentSaveParams = TypedDict(
    "PlacementCommentSaveParams",
    {
        "placementID": str,
        "data": "PlacementCommentData",
    },
)

PlacementCommentSaveMutationResult = ClassVar["PlacementComment"]

PlacementMetricsSaveParams = TypedDict(
    "PlacementMetricsSaveParams",
    {
        "placementID": str,
        "data": "PlacementMetricListData",
    },
)

PlacementMetricsSaveMutationResult = ClassVar["PlacementMetricList"]

PlacementPricingSaveParams = TypedDict(
    "PlacementPricingSaveParams",
    {
        "placementID": str,
        "data": "PlacementPricingData",
    },
)

PlacementPricingSaveMutationResult = ClassVar["PlacementPricing"]

AdminPlacementStatusUpdateParams = TypedDict(
    "AdminPlacementStatusUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminPlacementStatusUpdateMutationResult = ClassVar["PlacementStatus"]

PlacementTargetingSaveParams = TypedDict(
    "PlacementTargetingSaveParams",
    {
        "placementID": str,
        "data": "PlacementTargetingData",
    },
)

PlacementTargetingSaveMutationResult = ClassVar["PlacementTargeting"]

PlacementToolsSaveParams = TypedDict(
    "PlacementToolsSaveParams",
    {
        "id": str,
        "data": List["PlacementToolData"],
    },
)

PlacementToolsSaveMutationResult = ClassVar[List["PlacementTool"]]

PlacementToolPostClickUpdateParams = TypedDict(
    "PlacementToolPostClickUpdateParams",
    {
        "placementID": str,
        "data": "PlacementToolUpdateData",
    },
)

PlacementToolPostClickUpdateMutationResult = ClassVar["PlacementTool"]

PlacementCreateParams = TypedDict(
    "PlacementCreateParams",
    {
        "data": "PlacementData",
    },
)

PlacementCreateMutationResult = ClassVar[Optional["Placement"]]

PlacementSaveParams = TypedDict(
    "PlacementSaveParams",
    {
        "id": str,
        "data": "PlacementData",
    },
)

PlacementSaveMutationResult = ClassVar[Optional["Placement"]]

PlacementExcludeParams = TypedDict(
    "PlacementExcludeParams",
    {
        "id": str,
    },
)

PlacementExcludeMutationResult = bool

PlacementDeleteParams = TypedDict(
    "PlacementDeleteParams",
    {
        "id": List[str],
    },
)

PlacementDeleteMutationResult = int

PlacementPublishParams = TypedDict(
    "PlacementPublishParams",
    {
        "id": str,
    },
)

PlacementPublishMutationResult = bool

PlacementSetupIncompleteParams = TypedDict(
    "PlacementSetupIncompleteParams",
    {
        "id": str,
    },
)

PlacementSetupIncompleteMutationResult = bool

PlacementSetupCompleteParams = TypedDict(
    "PlacementSetupCompleteParams",
    {
        "id": str,
    },
)

PlacementSetupCompleteMutationResult = bool

PlacementDuplicateParams = TypedDict(
    "PlacementDuplicateParams",
    {
        "placementID": str,
        "data": "PlacementDuplicateData",
    },
)

PlacementDuplicateMutationResult = ClassVar["Placement"]

PlacementsApproveParams = TypedDict(
    "PlacementsApproveParams",
    {
        "mplanID": str,
        "placementIDs": List[str],
    },
)

PlacementsApproveMutationResult = ClassVar[List["Placement"]]

PlacementsRequestApprovalParams = TypedDict(
    "PlacementsRequestApprovalParams",
    {
        "mplanID": str,
        "placementIDs": List[str],
    },
)

PlacementsRequestApprovalMutationResult = ClassVar[List["Placement"]]

PlacementRejectedRequestApprovalParams = TypedDict(
    "PlacementRejectedRequestApprovalParams",
    {
        "placementID": str,
        "comment": Optional["PlacementCommentData"],
    },
)

PlacementRejectedRequestApprovalMutationResult = ClassVar["Placement"]

RepresentativePlacementApproveParams = TypedDict(
    "RepresentativePlacementApproveParams",
    {
        "placementID": str,
        "comment": Optional["PlacementCommentData"],
    },
)

RepresentativePlacementApproveMutationResult = ClassVar["Placement"]

RepresentativePlacementRejectParams = TypedDict(
    "RepresentativePlacementRejectParams",
    {
        "placementID": str,
        "comment": Optional["PlacementCommentData"],
    },
)

RepresentativePlacementRejectMutationResult = ClassVar["Placement"]

PlacementFromTemplateCreateParams = TypedDict(
    "PlacementFromTemplateCreateParams",
    {
        "templateID": str,
        "data": "PlacementFromTemplateData",
    },
)

PlacementFromTemplateCreateMutationResult = ClassVar["Placement"]

PricelistCreateParams = TypedDict(
    "PricelistCreateParams",
    {
        "data": "PricelistCreateData",
    },
)

PricelistCreateMutationResult = ClassVar["Pricelist"]

PricelistUpdateParams = TypedDict(
    "PricelistUpdateParams",
    {
        "id": str,
        "data": "PricelistUpdateData",
    },
)

PricelistUpdateMutationResult = ClassVar["Pricelist"]

PricelistDeleteParams = TypedDict(
    "PricelistDeleteParams",
    {
        "id": str,
    },
)

PricelistDeleteMutationResult = bool

PricePositionCreateParams = TypedDict(
    "PricePositionCreateParams",
    {
        "pricelistID": str,
        "data": "PricePositionData",
    },
)

PricePositionCreateMutationResult = ClassVar["PricePosition"]

PricePositionUpdateParams = TypedDict(
    "PricePositionUpdateParams",
    {
        "id": str,
        "data": "PricePositionData",
    },
)

PricePositionUpdateMutationResult = ClassVar["PricePosition"]

PricePositionDeleteParams = TypedDict(
    "PricePositionDeleteParams",
    {
        "id": str,
    },
)

PricePositionDeleteMutationResult = bool

AdminProductCategoryCreateParams = TypedDict(
    "AdminProductCategoryCreateParams",
    {
        "data": "ProductCategoryCreateData",
    },
)

AdminProductCategoryCreateMutationResult = ClassVar["ProductCategory"]

AdminProductCategoryUpdateParams = TypedDict(
    "AdminProductCategoryUpdateParams",
    {
        "id": str,
        "data": "ProductCategoryUpdateData",
    },
)

AdminProductCategoryUpdateMutationResult = ClassVar["ProductCategory"]

AdminProductGeographyUpdateParams = TypedDict(
    "AdminProductGeographyUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductGeographyUpdateMutationResult = ClassVar[Optional["ProductGeography"]]

AdminProductPriceCategoryUpdateParams = TypedDict(
    "AdminProductPriceCategoryUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductPriceCategoryUpdateMutationResult = ClassVar[
    Optional["ProductPriceCategory"]
]

AdminProductPurchaseFrequencyUpdateParams = TypedDict(
    "AdminProductPurchaseFrequencyUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductPurchaseFrequencyUpdateMutationResult = ClassVar[
    Optional["ProductPurchaseFrequency"]
]

AdminProductSeasonalityUpdateParams = TypedDict(
    "AdminProductSeasonalityUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductSeasonalityUpdateMutationResult = ClassVar[Optional["ProductSeasonality"]]

AdminProductSeasonalityValueUpdateParams = TypedDict(
    "AdminProductSeasonalityValueUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductSeasonalityValueUpdateMutationResult = ClassVar[
    Optional["ProductSeasonalityValue"]
]

AdminProductTypeUpdateParams = TypedDict(
    "AdminProductTypeUpdateParams",
    {
        "id": str,
        "data": "SimpleDict",
    },
)

AdminProductTypeUpdateMutationResult = ClassVar[Optional["ProductType"]]

AdminProductCreateParams = TypedDict(
    "AdminProductCreateParams",
    {
        "data": "AdminProductData",
    },
)

AdminProductCreateMutationResult = ClassVar["Product"]

AdminProductUpdateParams = TypedDict(
    "AdminProductUpdateParams",
    {
        "id": str,
        "data": "AdminProductData",
    },
)

AdminProductUpdateMutationResult = ClassVar["Product"]

AdminProductDeleteParams = TypedDict(
    "AdminProductDeleteParams",
    {
        "id": str,
    },
)

AdminProductDeleteMutationResult = bool

ProductCreateParams = TypedDict(
    "ProductCreateParams",
    {
        "data": "ProductData",
    },
)

ProductCreateMutationResult = ClassVar["Product"]

ProductUpdateParams = TypedDict(
    "ProductUpdateParams",
    {
        "id": str,
        "data": "ProductData",
    },
)

ProductUpdateMutationResult = ClassVar["Product"]

ProductDeleteParams = TypedDict(
    "ProductDeleteParams",
    {
        "id": str,
    },
)

ProductDeleteMutationResult = bool

MyProfileUpdateParams = TypedDict(
    "MyProfileUpdateParams",
    {
        "data": "ProfileData",
    },
)

MyProfileUpdateMutationResult = ClassVar["Profile"]

ProfileCreateParams = TypedDict(
    "ProfileCreateParams",
    {
        "data": "ProfileData",
    },
)

ProfileCreateMutationResult = ClassVar["Profile"]

ProfileUpdateParams = TypedDict(
    "ProfileUpdateParams",
    {
        "id": str,
        "data": "ProfileData",
    },
)

ProfileUpdateMutationResult = ClassVar["Profile"]

ProfileBlockParams = TypedDict(
    "ProfileBlockParams",
    {
        "id": str,
    },
)

ProfileBlockMutationResult = ClassVar["Profile"]

ProfileActivateParams = TypedDict(
    "ProfileActivateParams",
    {
        "id": str,
    },
)

ProfileActivateMutationResult = ClassVar["Profile"]

AdminProfileCreateParams = TypedDict(
    "AdminProfileCreateParams",
    {
        "data": "AdminProfileData",
    },
)

AdminProfileCreateMutationResult = ClassVar["Profile"]

AdminProfileUpdateParams = TypedDict(
    "AdminProfileUpdateParams",
    {
        "id": str,
        "data": "AdminProfileData",
    },
)

AdminProfileUpdateMutationResult = ClassVar["Profile"]

AdminProfileBlockParams = TypedDict(
    "AdminProfileBlockParams",
    {
        "id": str,
    },
)

AdminProfileBlockMutationResult = ClassVar["Profile"]

AdminProfileActivateParams = TypedDict(
    "AdminProfileActivateParams",
    {
        "id": str,
    },
)

AdminProfileActivateMutationResult = ClassVar["Profile"]

AdminSellerUpdateParams = TypedDict(
    "AdminSellerUpdateParams",
    {
        "id": str,
        "data": "SellerData",
    },
)

AdminSellerUpdateMutationResult = ClassVar["Seller"]

SiteElementCreateParams = TypedDict(
    "SiteElementCreateParams",
    {
        "data": "SiteElementData",
    },
)

SiteElementCreateMutationResult = ClassVar["SiteElement"]

SiteSectionCreateParams = TypedDict(
    "SiteSectionCreateParams",
    {
        "data": "SiteSectionData",
    },
)

SiteSectionCreateMutationResult = ClassVar["SiteSection"]

AdminSourceSiteCreateParams = TypedDict(
    "AdminSourceSiteCreateParams",
    {
        "data": "SourceSiteDataCreate",
    },
)

AdminSourceSiteCreateMutationResult = ClassVar["Source"]

AdminSourceSiteUpdateParams = TypedDict(
    "AdminSourceSiteUpdateParams",
    {
        "id": str,
        "data": "SourceSiteDataUpdate",
    },
)

AdminSourceSiteUpdateMutationResult = ClassVar["Source"]

AdminSourceToolCreateParams = TypedDict(
    "AdminSourceToolCreateParams",
    {
        "data": "SourceToolDataCreate",
    },
)

AdminSourceToolCreateMutationResult = ClassVar["Source"]

AdminSourceToolUpdateParams = TypedDict(
    "AdminSourceToolUpdateParams",
    {
        "id": str,
        "data": "SourceToolDataUpdate",
    },
)

AdminSourceToolUpdateMutationResult = ClassVar["Source"]

StratPlanSaveParams = TypedDict(
    "StratPlanSaveParams",
    {
        "data": "StratPlanData",
    },
)

StratPlanSaveMutationResult = ClassVar[Optional["StratPlan"]]

StratPlanUpdateParams = TypedDict(
    "StratPlanUpdateParams",
    {
        "id": str,
        "data": "StratPlanData",
    },
)

StratPlanUpdateMutationResult = ClassVar[Optional["StratPlan"]]

StratPlanDeleteParams = TypedDict(
    "StratPlanDeleteParams",
    {
        "id": str,
    },
)

StratPlanDeleteMutationResult = bool

TvCampaignDraftCreateParams = TypedDict(
    "TvCampaignDraftCreateParams",
    {
        "data": "TVCampaignData",
    },
)

TvCampaignDraftCreateMutationResult = ClassVar["TVCampaign"]

TvCampaignDraftSaveParams = TypedDict(
    "TvCampaignDraftSaveParams",
    {
        "id": str,
        "data": "TVCampaignData",
    },
)

TvCampaignDraftSaveMutationResult = ClassVar["TVCampaign"]

TvCampaignPlanningCreateParams = TypedDict(
    "TvCampaignPlanningCreateParams",
    {
        "draftID": Optional[str],
        "data": "TVCampaignData",
    },
)

TvCampaignPlanningCreateMutationResult = ClassVar["TVCampaign"]

TvCampaignDeleteParams = TypedDict(
    "TvCampaignDeleteParams",
    {
        "id": str,
    },
)

TvCampaignDeleteMutationResult = bool

TvCampaignCancelParams = TypedDict(
    "TvCampaignCancelParams",
    {
        "id": str,
    },
)

TvCampaignCancelMutationResult = bool

TvMplanDraftCreateParams = TypedDict(
    "TvMplanDraftCreateParams",
    {
        "data": "TVMplanData",
    },
)

TvMplanDraftCreateMutationResult = ClassVar["TVMplan"]

TvMplanDraftSaveParams = TypedDict(
    "TvMplanDraftSaveParams",
    {
        "id": str,
        "data": "TVMplanData",
    },
)

TvMplanDraftSaveMutationResult = ClassVar["TVMplan"]

TvMplanCreateParams = TypedDict(
    "TvMplanCreateParams",
    {
        "data": "TVMplanData",
    },
)

TvMplanCreateMutationResult = ClassVar["TVMplan"]

TvMplanDeleteParams = TypedDict(
    "TvMplanDeleteParams",
    {
        "id": str,
    },
)

TvMplanDeleteMutationResult = bool

AdminUnitUpsertParams = TypedDict(
    "AdminUnitUpsertParams",
    {
        "code": str,
        "data": "UnitData",
    },
)

AdminUnitUpsertMutationResult = ClassVar["Unit"]

PlacementUtmParametersSaveParams = TypedDict(
    "PlacementUtmParametersSaveParams",
    {
        "placementID": str,
        "data": List["PlacementUtmParameterData"],
    },
)

PlacementUtmParametersSaveMutationResult = ClassVar["PlacementUtmParameters"]

TemplateFromMplanCreateParams = TypedDict(
    "TemplateFromMplanCreateParams",
    {
        "mplanID": str,
        "overwriteDuplicate": bool,
    },
)

TemplateFromMplanCreateMutationResult = ClassVar["MplanTemplate"]

MplanTemplateUpdateParams = TypedDict(
    "MplanTemplateUpdateParams",
    {
        "templateID": str,
        "data": "MplanTemplateData",
    },
)

MplanTemplateUpdateMutationResult = ClassVar["MplanTemplate"]

MplanTemplateDeleteParams = TypedDict(
    "MplanTemplateDeleteParams",
    {
        "templateID": str,
    },
)

MplanTemplateDeleteMutationResult = bool

TemplateFromPlacementCreateParams = TypedDict(
    "TemplateFromPlacementCreateParams",
    {
        "placementID": str,
        "data": "TemplateFromPlacementData",
    },
)

TemplateFromPlacementCreateMutationResult = ClassVar["PlacementTemplate"]

PlacementTemplateCreateParams = TypedDict(
    "PlacementTemplateCreateParams",
    {
        "data": "PlacementTemplateData",
    },
)

PlacementTemplateCreateMutationResult = ClassVar["PlacementTemplate"]

PlacementTemplateUpdateParams = TypedDict(
    "PlacementTemplateUpdateParams",
    {
        "templateID": str,
        "data": "PlacementTemplateData",
    },
)

PlacementTemplateUpdateMutationResult = ClassVar["PlacementTemplate"]

PlacementTemplateDeleteParams = TypedDict(
    "PlacementTemplateDeleteParams",
    {
        "templateID": str,
    },
)

PlacementTemplateDeleteMutationResult = bool

Query = TypedDict(
    "Query",
    {
        "adminAdFormats": "AdminAdFormatsQueryResult",
        "adFormats": "AdFormatsQueryResult",
        "adminAdSizes": "AdminAdSizesQueryResult",
        "adSizes": "AdSizesQueryResult",
        "adSystems": "AdSystemsQueryResult",
        "adminInfoGet": "AdminInfoGetQueryResult",
        "agencies": "AgenciesQueryResult",
        "appsflyerPartners": "AppsflyerPartnersQueryResult",
        "adminBrandAwarenesses": "AdminBrandAwarenessesQueryResult",
        "brandAwarenesses": "BrandAwarenessesQueryResult",
        "adminBrands": "AdminBrandsQueryResult",
        "brands": "BrandsQueryResult",
        "adminBuyTypes": "AdminBuyTypesQueryResult",
        "buyTypes": "BuyTypesQueryResult",
        "adminCampaignStatuses": "AdminCampaignStatusesQueryResult",
        "campaignStatuses": "CampaignStatusesQueryResult",
        "campaigns": "CampaignsQueryResult",
        "adminCandidates": "AdminCandidatesQueryResult",
        "adminChannels": "AdminChannelsQueryResult",
        "channels": "ChannelsQueryResult",
        "adminClients": "AdminClientsQueryResult",
        "clients": "ClientsQueryResult",
        "placementCreatives": "PlacementCreativesQueryResult",
        "placementCreativeFrames": "PlacementCreativeFramesQueryResult",
        "creativeFrames": "CreativeFramesQueryResult",
        "departments": "DepartmentsQueryResult",
        "digitalReport": "DigitalReportQueryResult",
        "service": "ServiceQueryResult",
        "adminGoals": "AdminGoalsQueryResult",
        "goals": "GoalsQueryResult",
        "integrationTokens": "IntegrationTokensQueryResult",
        "integrationTools": "IntegrationToolsQueryResult",
        "yandexAuthLinkGet": "YandexAuthLinkGetQueryResult",
        "yandexAuthStatusGet": "YandexAuthStatusGetQueryResult",
        "vkAuthLinkGet": "VkAuthLinkGetQueryResult",
        "vkAuthStatusGet": "VkAuthStatusGetQueryResult",
        "googleAuthLinkGet": "GoogleAuthLinkGetQueryResult",
        "integrationConversions": "IntegrationConversionsQueryResult",
        "matchedConversionsTablesGenerate": "MatchedConversionsTablesGenerateQueryResult",
        "adminMetrics": "AdminMetricsQueryResult",
        "metrics": "MetricsQueryResult",
        "mplans": "MplansQueryResult",
        "mplanXLSExport": "MplanXLSExportQueryResult",
        "mplanXLSTemplate": "MplanXLSTemplateQueryResult",
        "mplanDataUploads": "MplanDataUploadsQueryResult",
        "mplanDataUploadTemplate": "MplanDataUploadTemplateQueryResult",
        "navBarGet": "NavBarGetQueryResult",
        "adminOrganizationLinks": "AdminOrganizationLinksQueryResult",
        "organizationLinks": "OrganizationLinksQueryResult",
        "adminOrganizations": "AdminOrganizationsQueryResult",
        "placementComments": "PlacementCommentsQueryResult",
        "placementMetrics": "PlacementMetricsQueryResult",
        "placementPricing": "PlacementPricingQueryResult",
        "placementPricingCalculate": "PlacementPricingCalculateQueryResult",
        "adminPlacementStatuses": "AdminPlacementStatusesQueryResult",
        "placementStatuses": "PlacementStatusesQueryResult",
        "placementStatusesHistory": "PlacementStatusesHistoryQueryResult",
        "placementStatusesProgress": "PlacementStatusesProgressQueryResult",
        "placementTargeting": "PlacementTargetingQueryResult",
        "placementTools": "PlacementToolsQueryResult",
        "placementAppsflyerApps": "PlacementAppsflyerAppsQueryResult",
        "placementCalcMetrics": "PlacementCalcMetricsQueryResult",
        "placements": "PlacementsQueryResult",
        "placementsByChannelsCount": "PlacementsByChannelsCountQueryResult",
        "placementsCount": "PlacementsCountQueryResult",
        "placementsByMplanAndStatusesCount": "PlacementsByMplanAndStatusesCountQueryResult",
        "pricelists": "PricelistsQueryResult",
        "pricePositions": "PricePositionsQueryResult",
        "adminProductCategories": "AdminProductCategoriesQueryResult",
        "productCategories": "ProductCategoriesQueryResult",
        "adminProductGeographies": "AdminProductGeographiesQueryResult",
        "productGeographies": "ProductGeographiesQueryResult",
        "adminProductPriceCategories": "AdminProductPriceCategoriesQueryResult",
        "productPriceCategories": "ProductPriceCategoriesQueryResult",
        "adminProductPurchaseFrequencies": "AdminProductPurchaseFrequenciesQueryResult",
        "productPurchaseFrequencies": "ProductPurchaseFrequenciesQueryResult",
        "adminProductSeasonalities": "AdminProductSeasonalitiesQueryResult",
        "adminProductSeasonalityValues": "AdminProductSeasonalityValuesQueryResult",
        "productSeasonalities": "ProductSeasonalitiesQueryResult",
        "productSeasonalityValues": "ProductSeasonalityValuesQueryResult",
        "adminProductTypes": "AdminProductTypesQueryResult",
        "productTypes": "ProductTypesQueryResult",
        "adminProducts": "AdminProductsQueryResult",
        "products": "ProductsQueryResult",
        "myProfile": "MyProfileQueryResult",
        "profiles": "ProfilesQueryResult",
        "userRoles": "UserRolesQueryResult",
        "representatives": "RepresentativesQueryResult",
        "adminProfiles": "AdminProfilesQueryResult",
        "adminUserRoles": "AdminUserRolesQueryResult",
        "projects": "ProjectsQueryResult",
        "reportDigitalCreatives": "ReportDigitalCreativesQueryResult",
        "reportDigitalCreativesExport": "ReportDigitalCreativesExportQueryResult",
        "reportStratplanChannelsCosts": "ReportStratplanChannelsCostsQueryResult",
        "reportStratplanMetricsValues": "ReportStratplanMetricsValuesQueryResult",
        "reportStratplanMediaCostsAndWordStats": "ReportStratplanMediaCostsAndWordStatsQueryResult",
        "reportDigitalConnections": "ReportDigitalConnectionsQueryResult",
        "reportMplanBudgetMetrics": "ReportMplanBudgetMetricsQueryResult",
        "reportMplanBudgetPerMonth": "ReportMplanBudgetPerMonthQueryResult",
        "reportMplanBudgetPerSeller": "ReportMplanBudgetPerSellerQueryResult",
        "reportMplanCampaignCalendar": "ReportMplanCampaignCalendarQueryResult",
        "reportMplanMetrics": "ReportMplanMetricsQueryResult",
        "reportSiteActivityCalendar": "ReportSiteActivityCalendarQueryResult",
        "reportPlacementsBudgetPerStatuses": "ReportPlacementsBudgetPerStatusesQueryResult",
        "adminSellers": "AdminSellersQueryResult",
        "sellers": "SellersQueryResult",
        "siteElements": "SiteElementsQueryResult",
        "siteSections": "SiteSectionsQueryResult",
        "adminSources": "AdminSourcesQueryResult",
        "sources": "SourcesQueryResult",
        "smpAudiences": "SmpAudiencesQueryResult",
        "smpCommunications": "SmpCommunicationsQueryResult",
        "smpCompetitorStrategies": "SmpCompetitorStrategiesQueryResult",
        "smpGoals": "SmpGoalsQueryResult",
        "smpProductKnowledges": "SmpProductKnowledgesQueryResult",
        "stratPlans": "StratPlansQueryResult",
        "tvCampaigns": "TvCampaignsQueryResult",
        "tvMetrics": "TvMetricsQueryResult",
        "tvMplanGoals": "TvMplanGoalsQueryResult",
        "tvMplans": "TvMplansQueryResult",
        "adminUnits": "AdminUnitsQueryResult",
        "units": "UnitsQueryResult",
        "placementUtmParameters": "PlacementUtmParametersQueryResult",
        "placementUtmParameterCalculate": "PlacementUtmParameterCalculateQueryResult",
        "placementUtmParametersCalculate": "PlacementUtmParametersCalculateQueryResult",
        "placementTemplateMetrics": "PlacementTemplateMetricsQueryResult",
        "mplanTemplates": "MplanTemplatesQueryResult",
        "placementTemplates": "PlacementTemplatesQueryResult",
    },
)

AdminAdFormatsParams = TypedDict(
    "AdminAdFormatsParams",
    {
        "id": Optional[str],
        "filter": Optional["AdFormatFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminAdFormatsQueryResult = ClassVar[List["AdFormat"]]

AdFormatsParams = TypedDict(
    "AdFormatsParams",
    {
        "id": Optional[str],
        "filter": Optional["AdFormatFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdFormatsQueryResult = ClassVar[List["AdFormat"]]

AdminAdSizesParams = TypedDict(
    "AdminAdSizesParams",
    {
        "id": Optional[str],
        "filter": Optional["AdSizeFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminAdSizesQueryResult = ClassVar[List["AdSize"]]

AdSizesParams = TypedDict(
    "AdSizesParams",
    {
        "id": Optional[str],
        "filter": Optional["AdSizeFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdSizesQueryResult = ClassVar[List["AdSize"]]

AdSystemsParams = TypedDict(
    "AdSystemsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdSystemsQueryResult = ClassVar[List["AdSystem"]]

AdminInfoGetQueryResult = ClassVar["AdminInfo"]

AgenciesParams = TypedDict(
    "AgenciesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AgenciesQueryResult = ClassVar[List["Agency"]]

AppsflyerPartnersParams = TypedDict(
    "AppsflyerPartnersParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AppsflyerPartnersQueryResult = ClassVar[List["AppsflyerPartner"]]

AdminBrandAwarenessesParams = TypedDict(
    "AdminBrandAwarenessesParams",
    {
        "id": Optional[str],
    },
)

AdminBrandAwarenessesQueryResult = ClassVar[List["BrandAwareness"]]

BrandAwarenessesParams = TypedDict(
    "BrandAwarenessesParams",
    {
        "id": Optional[str],
    },
)

BrandAwarenessesQueryResult = ClassVar[List["BrandAwareness"]]

AdminBrandsParams = TypedDict(
    "AdminBrandsParams",
    {
        "id": Optional[str],
        "filter": Optional["AdminBrandFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminBrandsQueryResult = ClassVar[List["Brand"]]

BrandsParams = TypedDict(
    "BrandsParams",
    {
        "id": Optional[str],
        "filter": Optional["BrandFilter"],
        "slice": Optional["ListSlice"],
    },
)

BrandsQueryResult = ClassVar[List["Brand"]]

AdminBuyTypesParams = TypedDict(
    "AdminBuyTypesParams",
    {
        "id": Optional[str],
        "filter": Optional["BuyTypeFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminBuyTypesQueryResult = ClassVar[List["BuyType"]]

BuyTypesParams = TypedDict(
    "BuyTypesParams",
    {
        "id": Optional[str],
        "filter": Optional["BuyTypeFilter"],
        "slice": Optional["ListSlice"],
    },
)

BuyTypesQueryResult = ClassVar[List["BuyType"]]

AdminCampaignStatusesParams = TypedDict(
    "AdminCampaignStatusesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdminCampaignStatusesQueryResult = ClassVar[List["CampaignStatus"]]

CampaignStatusesParams = TypedDict(
    "CampaignStatusesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

CampaignStatusesQueryResult = ClassVar[List["CampaignStatus"]]

CampaignsParams = TypedDict(
    "CampaignsParams",
    {
        "id": Optional[str],
        "filter": Optional["CampaignFilter"],
        "slice": Optional["ListSlice"],
    },
)

CampaignsQueryResult = ClassVar[List["Campaign"]]

AdminCandidatesParams = TypedDict(
    "AdminCandidatesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdminCandidatesQueryResult = ClassVar[List["Candidate"]]

AdminChannelsParams = TypedDict(
    "AdminChannelsParams",
    {
        "code": Optional[str],
        "slice": Optional["ListSlice"],
        "filter": Optional["ChannelFilter"],
    },
)

AdminChannelsQueryResult = ClassVar[List["Channel"]]

ChannelsParams = TypedDict(
    "ChannelsParams",
    {
        "code": Optional[str],
        "slice": Optional["ListSlice"],
        "filter": Optional["ChannelFilter"],
    },
)

ChannelsQueryResult = ClassVar[List["Channel"]]

AdminClientsParams = TypedDict(
    "AdminClientsParams",
    {
        "id": Optional[str],
        "filter": Optional["AdminClientFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminClientsQueryResult = ClassVar[List["Client"]]

ClientsParams = TypedDict(
    "ClientsParams",
    {
        "id": Optional[str],
        "filter": Optional["ClientFilter"],
        "slice": Optional["ListSlice"],
    },
)

ClientsQueryResult = ClassVar[List["Client"]]

PlacementCreativesParams = TypedDict(
    "PlacementCreativesParams",
    {
        "placementID": str,
    },
)

PlacementCreativesQueryResult = ClassVar[List["PlacementCreative"]]

PlacementCreativeFramesParams = TypedDict(
    "PlacementCreativeFramesParams",
    {
        "placementID": str,
    },
)

PlacementCreativeFramesQueryResult = ClassVar[List["PlacementCreativeFrame"]]

CreativeFramesParams = TypedDict(
    "CreativeFramesParams",
    {
        "campaignID": str,
    },
)

CreativeFramesQueryResult = ClassVar[List["CreativeFrame"]]

DepartmentsParams = TypedDict(
    "DepartmentsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

DepartmentsQueryResult = ClassVar[List["Department"]]

DigitalReportParams = TypedDict(
    "DigitalReportParams",
    {
        "id": str,
        "filter": "DigitalReportFilter",
    },
)

DigitalReportQueryResult = ClassVar["DigitalReport"]

ServiceQueryResult = ClassVar["Service"]

AdminGoalsParams = TypedDict(
    "AdminGoalsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdminGoalsQueryResult = ClassVar[List["Goal"]]

GoalsParams = TypedDict(
    "GoalsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

GoalsQueryResult = ClassVar[List["Goal"]]

IntegrationTokensParams = TypedDict(
    "IntegrationTokensParams",
    {
        "filter": Optional["IntegrationTokenFilter"],
        "slice": Optional["ListSlice"],
    },
)

IntegrationTokensQueryResult = ClassVar[List["IntegrationToken"]]

IntegrationToolsParams = TypedDict(
    "IntegrationToolsParams",
    {
        "id": Optional[str],
        "filter": Optional["IntegrationToolFilter"],
    },
)

IntegrationToolsQueryResult = ClassVar[List["IntegrationTool"]]

YandexAuthLinkGetParams = TypedDict(
    "YandexAuthLinkGetParams",
    {
        "service": "YandexService",
    },
)

YandexAuthLinkGetQueryResult = str

YandexAuthStatusGetParams = TypedDict(
    "YandexAuthStatusGetParams",
    {
        "state": str,
        "service": "YandexService",
    },
)

YandexAuthStatusGetQueryResult = ClassVar["ItokenStatus"]

VkAuthLinkGetQueryResult = str

VkAuthStatusGetParams = TypedDict(
    "VkAuthStatusGetParams",
    {
        "state": str,
    },
)

VkAuthStatusGetQueryResult = ClassVar["ItokenStatus"]

GoogleAuthLinkGetQueryResult = str

IntegrationConversionsParams = TypedDict(
    "IntegrationConversionsParams",
    {
        "mplanID": str,
        "sourceCode": str,
        "counterID": str,
    },
)

IntegrationConversionsQueryResult = ClassVar[List["FactConversion"]]

MatchedConversionsTablesGenerateParams = TypedDict(
    "MatchedConversionsTablesGenerateParams",
    {
        "mplanID": str,
    },
)

MatchedConversionsTablesGenerateQueryResult = ClassVar[List["MatchedConversionsTable"]]

AdminMetricsParams = TypedDict(
    "AdminMetricsParams",
    {
        "code": Optional[str],
        "filter": Optional["MetricFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminMetricsQueryResult = ClassVar[List["Metric"]]

MetricsParams = TypedDict(
    "MetricsParams",
    {
        "code": Optional[str],
        "filter": Optional["MetricFilter"],
        "slice": Optional["ListSlice"],
    },
)

MetricsQueryResult = ClassVar[List["Metric"]]

MplansParams = TypedDict(
    "MplansParams",
    {
        "id": Optional[str],
        "filter": Optional["MplanFilter"],
        "slice": Optional["ListSlice"],
    },
)

MplansQueryResult = ClassVar[List["Mplan"]]

MplanXLSExportParams = TypedDict(
    "MplanXLSExportParams",
    {
        "mplanID": str,
    },
)

MplanXLSExportQueryResult = ClassVar["XlsDoc"]

MplanXLSTemplateParams = TypedDict(
    "MplanXLSTemplateParams",
    {
        "campaignID": str,
    },
)

MplanXLSTemplateQueryResult = ClassVar["XlsDoc"]

MplanDataUploadsParams = TypedDict(
    "MplanDataUploadsParams",
    {
        "mplanID": str,
        "slice": Optional["ListSlice"],
    },
)

MplanDataUploadsQueryResult = ClassVar[List["MplanDataUpload"]]

MplanDataUploadTemplateQueryResult = ClassVar["XlsDoc"]

NavBarGetQueryResult = ClassVar[Optional["NavBar"]]

AdminOrganizationLinksParams = TypedDict(
    "AdminOrganizationLinksParams",
    {
        "filter": Optional["AdminOrganizationLinkFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["OrganizationLinkSort"],
    },
)

AdminOrganizationLinksQueryResult = ClassVar[List["OrganizationLink"]]

OrganizationLinksParams = TypedDict(
    "OrganizationLinksParams",
    {
        "filter": Optional["OrganizationLinkFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["OrganizationLinkSort"],
    },
)

OrganizationLinksQueryResult = ClassVar[List["OrganizationLink"]]

AdminOrganizationsParams = TypedDict(
    "AdminOrganizationsParams",
    {
        "id": Optional[str],
        "filter": Optional["OrganizationFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["OrganizationSort"],
    },
)

AdminOrganizationsQueryResult = ClassVar[List["Organization"]]

PlacementCommentsParams = TypedDict(
    "PlacementCommentsParams",
    {
        "placementID": str,
        "slice": Optional["ListSlice"],
    },
)

PlacementCommentsQueryResult = ClassVar[List["PlacementComment"]]

PlacementMetricsParams = TypedDict(
    "PlacementMetricsParams",
    {
        "placementID": str,
    },
)

PlacementMetricsQueryResult = ClassVar["PlacementMetricList"]

PlacementPricingParams = TypedDict(
    "PlacementPricingParams",
    {
        "placementID": str,
    },
)

PlacementPricingQueryResult = ClassVar["PlacementPricing"]

PlacementPricingCalculateParams = TypedDict(
    "PlacementPricingCalculateParams",
    {
        "data": "PlacementPricingData",
    },
)

PlacementPricingCalculateQueryResult = ClassVar["PlacementPricingCalculated"]

AdminPlacementStatusesParams = TypedDict(
    "AdminPlacementStatusesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdminPlacementStatusesQueryResult = ClassVar[List["PlacementStatus"]]

PlacementStatusesParams = TypedDict(
    "PlacementStatusesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

PlacementStatusesQueryResult = ClassVar[List["PlacementStatus"]]

PlacementStatusesHistoryParams = TypedDict(
    "PlacementStatusesHistoryParams",
    {
        "id": Optional[str],
        "filter": Optional["PlacementStatusFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["PlacementStatusSort"],
    },
)

PlacementStatusesHistoryQueryResult = ClassVar[List["PlacementStatusHistory"]]

PlacementStatusesProgressParams = TypedDict(
    "PlacementStatusesProgressParams",
    {
        "placementID": str,
    },
)

PlacementStatusesProgressQueryResult = ClassVar[List["PlacementStatusProgress"]]

PlacementTargetingParams = TypedDict(
    "PlacementTargetingParams",
    {
        "placementID": str,
    },
)

PlacementTargetingQueryResult = ClassVar[Optional["PlacementTargeting"]]

PlacementToolsParams = TypedDict(
    "PlacementToolsParams",
    {
        "placementID": str,
    },
)

PlacementToolsQueryResult = ClassVar[List["PlacementTool"]]

PlacementAppsflyerAppsParams = TypedDict(
    "PlacementAppsflyerAppsParams",
    {
        "placementID": str,
        "iTokenID": Optional[str],
    },
)

PlacementAppsflyerAppsQueryResult = ClassVar[Optional[List["AppsflyerApp"]]]

PlacementCalcMetricsParams = TypedDict(
    "PlacementCalcMetricsParams",
    {
        "data": "PlacementCalcMetricsData",
        "event": "PlacementCalcMetricsEvent",
    },
)

PlacementCalcMetricsQueryResult = ClassVar["PlacementCalcMetrics"]

PlacementsParams = TypedDict(
    "PlacementsParams",
    {
        "id": Optional[str],
        "filter": Optional["PlacementFilter"],
        "slice": Optional["ListSlice"],
    },
)

PlacementsQueryResult = ClassVar[List["Placement"]]

PlacementsByChannelsCountParams = TypedDict(
    "PlacementsByChannelsCountParams",
    {
        "filter": Optional["PlacementFilter"],
    },
)

PlacementsByChannelsCountQueryResult = ClassVar[List["PlacementChannelsCount"]]

PlacementsCountParams = TypedDict(
    "PlacementsCountParams",
    {
        "filter": Optional["PlacementFilter"],
    },
)

PlacementsCountQueryResult = int

PlacementsByMplanAndStatusesCountParams = TypedDict(
    "PlacementsByMplanAndStatusesCountParams",
    {
        "mplanID": str,
        "statusIDs": List[str],
    },
)

PlacementsByMplanAndStatusesCountQueryResult = ClassVar[List["MplanStatusCount"]]

PricelistsParams = TypedDict(
    "PricelistsParams",
    {
        "id": Optional[str],
        "filter": Optional["PricelistFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["PricelistSort"],
    },
)

PricelistsQueryResult = ClassVar[List["Pricelist"]]

PricePositionsParams = TypedDict(
    "PricePositionsParams",
    {
        "id": Optional[str],
        "pricelistID": str,
        "slice": Optional["ListSlice"],
        "sort": Optional["PricePositionSort"],
    },
)

PricePositionsQueryResult = ClassVar[List["PricePosition"]]

AdminProductCategoriesParams = TypedDict(
    "AdminProductCategoriesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
        "filter": Optional["ProductCategoryFilter"],
    },
)

AdminProductCategoriesQueryResult = ClassVar[List["ProductCategory"]]

ProductCategoriesParams = TypedDict(
    "ProductCategoriesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
        "filter": Optional["ProductCategoryFilter"],
    },
)

ProductCategoriesQueryResult = ClassVar[List["ProductCategory"]]

AdminProductGeographiesParams = TypedDict(
    "AdminProductGeographiesParams",
    {
        "id": Optional[str],
    },
)

AdminProductGeographiesQueryResult = ClassVar[List["ProductGeography"]]

ProductGeographiesParams = TypedDict(
    "ProductGeographiesParams",
    {
        "id": Optional[str],
    },
)

ProductGeographiesQueryResult = ClassVar[List["ProductGeography"]]

AdminProductPriceCategoriesParams = TypedDict(
    "AdminProductPriceCategoriesParams",
    {
        "id": Optional[str],
    },
)

AdminProductPriceCategoriesQueryResult = ClassVar[List["ProductPriceCategory"]]

ProductPriceCategoriesParams = TypedDict(
    "ProductPriceCategoriesParams",
    {
        "id": Optional[str],
    },
)

ProductPriceCategoriesQueryResult = ClassVar[List["ProductPriceCategory"]]

AdminProductPurchaseFrequenciesParams = TypedDict(
    "AdminProductPurchaseFrequenciesParams",
    {
        "id": Optional[str],
    },
)

AdminProductPurchaseFrequenciesQueryResult = ClassVar[List["ProductPurchaseFrequency"]]

ProductPurchaseFrequenciesParams = TypedDict(
    "ProductPurchaseFrequenciesParams",
    {
        "id": Optional[str],
    },
)

ProductPurchaseFrequenciesQueryResult = ClassVar[List["ProductPurchaseFrequency"]]

AdminProductSeasonalitiesParams = TypedDict(
    "AdminProductSeasonalitiesParams",
    {
        "id": Optional[str],
    },
)

AdminProductSeasonalitiesQueryResult = ClassVar[List["ProductSeasonality"]]

AdminProductSeasonalityValuesParams = TypedDict(
    "AdminProductSeasonalityValuesParams",
    {
        "seasonalityID": Optional[str],
        "id": Optional[str],
    },
)

AdminProductSeasonalityValuesQueryResult = ClassVar[List["ProductSeasonalityValue"]]

ProductSeasonalitiesParams = TypedDict(
    "ProductSeasonalitiesParams",
    {
        "id": Optional[str],
    },
)

ProductSeasonalitiesQueryResult = ClassVar[List["ProductSeasonality"]]

ProductSeasonalityValuesParams = TypedDict(
    "ProductSeasonalityValuesParams",
    {
        "seasonalityID": Optional[str],
        "id": Optional[str],
    },
)

ProductSeasonalityValuesQueryResult = ClassVar[List["ProductSeasonalityValue"]]

AdminProductTypesParams = TypedDict(
    "AdminProductTypesParams",
    {
        "id": Optional[str],
    },
)

AdminProductTypesQueryResult = ClassVar[List["ProductType"]]

ProductTypesParams = TypedDict(
    "ProductTypesParams",
    {
        "id": Optional[str],
    },
)

ProductTypesQueryResult = ClassVar[List["ProductType"]]

AdminProductsParams = TypedDict(
    "AdminProductsParams",
    {
        "id": Optional[str],
        "filter": Optional["AdminProductFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminProductsQueryResult = ClassVar[List["Product"]]

ProductsParams = TypedDict(
    "ProductsParams",
    {
        "id": Optional[str],
        "filter": Optional["ProductFilter"],
        "slice": Optional["ListSlice"],
    },
)

ProductsQueryResult = ClassVar[List["Product"]]

MyProfileQueryResult = ClassVar["Profile"]

ProfilesParams = TypedDict(
    "ProfilesParams",
    {
        "id": Optional[str],
        "filter": Optional["ProfileFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["ProfileSort"],
    },
)

ProfilesQueryResult = ClassVar[List["Profile"]]

UserRolesQueryResult = ClassVar[List["UserRole"]]

RepresentativesQueryResult = ClassVar[List["Person"]]

AdminProfilesParams = TypedDict(
    "AdminProfilesParams",
    {
        "id": Optional[str],
        "filter": Optional["ProfileFilter"],
        "slice": Optional["ListSlice"],
        "sort": Optional["ProfileSort"],
    },
)

AdminProfilesQueryResult = ClassVar[List["Profile"]]

AdminUserRolesQueryResult = ClassVar[List["UserRole"]]

ProjectsParams = TypedDict(
    "ProjectsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

ProjectsQueryResult = ClassVar[List["Project"]]

ReportDigitalCreativesParams = TypedDict(
    "ReportDigitalCreativesParams",
    {
        "campaignID": str,
        "filter": "DigitalReportFilter",
    },
)

ReportDigitalCreativesQueryResult = ClassVar["DigitalReport"]

ReportDigitalCreativesExportParams = TypedDict(
    "ReportDigitalCreativesExportParams",
    {
        "campaignID": str,
        "filter": "DigitalReportFilter",
    },
)

ReportDigitalCreativesExportQueryResult = ClassVar["XlsDoc"]

ReportStratplanChannelsCostsParams = TypedDict(
    "ReportStratplanChannelsCostsParams",
    {
        "id": str,
    },
)

ReportStratplanChannelsCostsQueryResult = ClassVar["Report"]

ReportStratplanMetricsValuesParams = TypedDict(
    "ReportStratplanMetricsValuesParams",
    {
        "id": str,
    },
)

ReportStratplanMetricsValuesQueryResult = ClassVar["Report"]

ReportStratplanMediaCostsAndWordStatsParams = TypedDict(
    "ReportStratplanMediaCostsAndWordStatsParams",
    {
        "id": str,
    },
)

ReportStratplanMediaCostsAndWordStatsQueryResult = ClassVar["Report"]

ReportDigitalConnectionsParams = TypedDict(
    "ReportDigitalConnectionsParams",
    {
        "mplanID": str,
    },
)

ReportDigitalConnectionsQueryResult = ClassVar["Report"]

ReportMplanBudgetMetricsParams = TypedDict(
    "ReportMplanBudgetMetricsParams",
    {
        "mplanID": str,
        "metricCode": str,
    },
)

ReportMplanBudgetMetricsQueryResult = ClassVar["Report"]

ReportMplanBudgetPerMonthParams = TypedDict(
    "ReportMplanBudgetPerMonthParams",
    {
        "mplanID": str,
    },
)

ReportMplanBudgetPerMonthQueryResult = ClassVar["Report"]

ReportMplanBudgetPerSellerParams = TypedDict(
    "ReportMplanBudgetPerSellerParams",
    {
        "mplanID": str,
    },
)

ReportMplanBudgetPerSellerQueryResult = ClassVar["Report"]

ReportMplanCampaignCalendarParams = TypedDict(
    "ReportMplanCampaignCalendarParams",
    {
        "mplanID": str,
    },
)

ReportMplanCampaignCalendarQueryResult = ClassVar["Report"]

ReportMplanMetricsParams = TypedDict(
    "ReportMplanMetricsParams",
    {
        "mplanID": str,
    },
)

ReportMplanMetricsQueryResult = ClassVar["Report"]

ReportSiteActivityCalendarParams = TypedDict(
    "ReportSiteActivityCalendarParams",
    {
        "mplanID": str,
    },
)

ReportSiteActivityCalendarQueryResult = ClassVar["Report"]

ReportPlacementsBudgetPerStatusesParams = TypedDict(
    "ReportPlacementsBudgetPerStatusesParams",
    {
        "mplanID": str,
    },
)

ReportPlacementsBudgetPerStatusesQueryResult = ClassVar["Report"]

AdminSellersParams = TypedDict(
    "AdminSellersParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

AdminSellersQueryResult = ClassVar[List["Seller"]]

SellersParams = TypedDict(
    "SellersParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SellersQueryResult = ClassVar[List["Seller"]]

SiteElementsParams = TypedDict(
    "SiteElementsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SiteElementsQueryResult = ClassVar[List["SiteElement"]]

SiteSectionsParams = TypedDict(
    "SiteSectionsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SiteSectionsQueryResult = ClassVar[List["SiteSection"]]

AdminSourcesParams = TypedDict(
    "AdminSourcesParams",
    {
        "id": Optional[str],
        "filter": Optional["SourceFilter"],
        "slice": Optional["ListSlice"],
    },
)

AdminSourcesQueryResult = ClassVar[List["Source"]]

SourcesParams = TypedDict(
    "SourcesParams",
    {
        "id": Optional[str],
        "filter": Optional["SourceFilter"],
        "slice": Optional["ListSlice"],
    },
)

SourcesQueryResult = ClassVar[List["Source"]]

SmpAudiencesParams = TypedDict(
    "SmpAudiencesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SmpAudiencesQueryResult = ClassVar[List["SMPAudience"]]

SmpCommunicationsParams = TypedDict(
    "SmpCommunicationsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SmpCommunicationsQueryResult = ClassVar[List["SMPCommunication"]]

SmpCompetitorStrategiesParams = TypedDict(
    "SmpCompetitorStrategiesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SmpCompetitorStrategiesQueryResult = ClassVar[List["SMPCompetitorStrategy"]]

SmpGoalsParams = TypedDict(
    "SmpGoalsParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SmpGoalsQueryResult = ClassVar[List["SMPGoal"]]

SmpProductKnowledgesParams = TypedDict(
    "SmpProductKnowledgesParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

SmpProductKnowledgesQueryResult = ClassVar[List["SMPProductKnowledge"]]

StratPlansParams = TypedDict(
    "StratPlansParams",
    {
        "id": Optional[str],
        "slice": Optional["ListSlice"],
    },
)

StratPlansQueryResult = ClassVar[List["StratPlan"]]

TvCampaignsParams = TypedDict(
    "TvCampaignsParams",
    {
        "id": Optional[str],
    },
)

TvCampaignsQueryResult = ClassVar[List["TVCampaign"]]

TvMetricsParams = TypedDict(
    "TvMetricsParams",
    {
        "code": Optional[str],
    },
)

TvMetricsQueryResult = ClassVar[List["TVMetric"]]

TvMplanGoalsParams = TypedDict(
    "TvMplanGoalsParams",
    {
        "code": Optional[str],
    },
)

TvMplanGoalsQueryResult = ClassVar[List["TVMplanGoal"]]

TvMplansParams = TypedDict(
    "TvMplansParams",
    {
        "id": Optional[str],
        "campaignID": Optional[str],
    },
)

TvMplansQueryResult = ClassVar[List["TVMplan"]]

AdminUnitsParams = TypedDict(
    "AdminUnitsParams",
    {
        "code": Optional[str],
    },
)

AdminUnitsQueryResult = ClassVar[List["Unit"]]

UnitsParams = TypedDict(
    "UnitsParams",
    {
        "code": Optional[str],
    },
)

UnitsQueryResult = ClassVar[List["Unit"]]

PlacementUtmParametersParams = TypedDict(
    "PlacementUtmParametersParams",
    {
        "placementID": str,
    },
)

PlacementUtmParametersQueryResult = ClassVar["PlacementUtmParameters"]

PlacementUtmParameterCalculateParams = TypedDict(
    "PlacementUtmParameterCalculateParams",
    {
        "placementID": str,
        "data": "PlacementUtmParameterData",
    },
)

PlacementUtmParameterCalculateQueryResult = ClassVar["PlacementUtmParameter"]

PlacementUtmParametersCalculateParams = TypedDict(
    "PlacementUtmParametersCalculateParams",
    {
        "placementID": str,
        "data": List["PlacementUtmParameterData"],
    },
)

PlacementUtmParametersCalculateQueryResult = ClassVar["PlacementUtmParameters"]

PlacementTemplateMetricsParams = TypedDict(
    "PlacementTemplateMetricsParams",
    {
        "templateID": str,
    },
)

PlacementTemplateMetricsQueryResult = ClassVar["PlacementTemplateMetricList"]

MplanTemplatesParams = TypedDict(
    "MplanTemplatesParams",
    {
        "id": Optional[str],
        "filter": Optional["MplanTemplateFilter"],
        "slice": Optional["ListSlice"],
    },
)

MplanTemplatesQueryResult = ClassVar[List["MplanTemplate"]]

PlacementTemplatesParams = TypedDict(
    "PlacementTemplatesParams",
    {
        "id": Optional[str],
        "filter": Optional["PlacementTemplateFilter"],
        "slice": Optional["ListSlice"],
    },
)

PlacementTemplatesQueryResult = ClassVar[List["PlacementTemplate"]]

ReportMetaDimension = TypedDict(
    "ReportMetaDimension",
    {
        "label": Optional[str],
        "code": str,
        "leafs": List["ReportMetaDimension"],
        "extra": Optional["JSON"],
    },
)

ReportMetaMetric = TypedDict(
    "ReportMetaMetric",
    {
        "label": Optional[str],
        "code": str,
        "type": "ReportMetaMetricType",
        "leafs": List["ReportMetaMetric"],
        "extra": Optional["JSON"],
    },
)

AdminAdFormatCreateData = TypedDict(
    "AdminAdFormatCreateData",
    {
        "name": str,
        "code": str,
        "naming": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdminAdFormatUpdateData = TypedDict(
    "AdminAdFormatUpdateData",
    {
        "name": str,
        "naming": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdFormatFilter = TypedDict(
    "AdFormatFilter",
    {
        "sourceIDs": Optional[List[str]],
        "adSizeIDs": Optional[List[str]],
        "isActive": Optional[bool],
        "channelCodes": Optional[List[str]],
    },
)

AdminAdSizeUpdateData = TypedDict(
    "AdminAdSizeUpdateData",
    {
        "name": str,
        "naming": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdminAdSizeCreateData = TypedDict(
    "AdminAdSizeCreateData",
    {
        "name": str,
        "code": str,
        "naming": str,
        "isActive": bool,
        "channelCode": str,
    },
)

AdSizeFilter = TypedDict(
    "AdSizeFilter",
    {
        "sourceIDs": Optional[List[str]],
        "adFormatIDs": Optional[List[str]],
        "isActive": Optional[bool],
        "channelCodes": Optional[List[str]],
    },
)

AdSystemData = TypedDict(
    "AdSystemData",
    {
        "name": str,
        "naming": str,
    },
)

AdminData = TypedDict(
    "AdminData",
    {
        "name": str,
        "email": str,
        "phone": str,
        "login": str,
    },
)

AgencyData = TypedDict(
    "AgencyData",
    {
        "name": str,
        "naming": str,
    },
)

AppsflyerPartnerData = TypedDict(
    "AppsflyerPartnerData",
    {
        "name": str,
        "identifier": str,
        "accountName": Optional[str],
        "adID": Optional[str],
    },
)

BrandData = TypedDict(
    "BrandData",
    {
        "name": str,
        "naming": str,
        "awarenessID": Optional[str],
    },
)

AdminBrandFilter = TypedDict(
    "AdminBrandFilter",
    {
        "clientIDs": Optional[List[str]],
        "organizationID": Optional[str],
    },
)

BrandFilter = TypedDict(
    "BrandFilter",
    {
        "clientIDs": Optional[List[str]],
    },
)

AdminBuyTypeCreateData = TypedDict(
    "AdminBuyTypeCreateData",
    {
        "name": str,
        "code": str,
        "naming": str,
        "unit": str,
        "placementType": "PlacementType",
    },
)

AdminBuyTypeUpdateData = TypedDict(
    "AdminBuyTypeUpdateData",
    {
        "name": str,
        "naming": str,
        "unit": str,
        "placementType": "PlacementType",
    },
)

BuyTypeFilter = TypedDict(
    "BuyTypeFilter",
    {
        "sourceID": Optional[List[str]],
        "adFormatID": Optional[List[str]],
        "placementType": Optional["PlacementType"],
    },
)

CampaignData = TypedDict(
    "CampaignData",
    {
        "name": Optional[str],
        "code": Optional[str],
        "clientID": Optional[str],
        "brandID": Optional[str],
        "productID": Optional[str],
        "coBrands": Optional[List[str]],
        "agencyID": Optional[str],
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
        "budget": Optional["Decimal"],
        "departmentID": Optional[str],
        "marketTarget": Optional["MarketTarget"],
        "targetAudience": Optional[str],
        "targetGeo": Optional[str],
        "conditions": Optional[str],
        "representativeUserID": Optional[str],
    },
)

CampaignFilter = TypedDict(
    "CampaignFilter",
    {
        "clientIDs": Optional[List[str]],
        "brandIDs": Optional[List[str]],
        "productIDs": Optional[List[str]],
        "statusIDs": Optional[List[str]],
        "namePart": Optional[str],
        "activeFrom": Optional["Time"],
        "activeUntil": Optional["Time"],
        "updatedFrom": Optional["Time"],
        "updatedUntil": Optional["Time"],
    },
)

CampaignDocData = TypedDict(
    "CampaignDocData",
    {
        "campaignID": str,
        "code": str,
        "name": str,
        "file": "Upload",
    },
)

CandidateData = TypedDict(
    "CandidateData",
    {
        "name": str,
        "surname": str,
        "email": str,
        "firmName": str,
        "phone": str,
        "role": str,
        "comments": Optional[str],
        "isPerformed": Optional[bool],
    },
)

ChannelCreateData = TypedDict(
    "ChannelCreateData",
    {
        "code": str,
        "name": str,
        "naming": str,
        "mediaType": "MediaType",
        "isUsedBySplan": bool,
    },
)

ChannelUpdateData = TypedDict(
    "ChannelUpdateData",
    {
        "name": str,
        "naming": str,
        "mediaType": "MediaType",
        "isUsedBySplan": bool,
    },
)

ChannelFilter = TypedDict(
    "ChannelFilter",
    {
        "mediaTypes": Optional[List["MediaType"]],
        "isUsedBySplan": Optional[bool],
    },
)

AdminClientCreateData = TypedDict(
    "AdminClientCreateData",
    {
        "name": str,
        "naming": str,
        "fullName": Optional[str],
        "inn": Optional[str],
        "kpp": Optional[str],
        "organizationID": str,
    },
)

ClientData = TypedDict(
    "ClientData",
    {
        "name": str,
        "naming": str,
        "fullName": Optional[str],
        "inn": Optional[str],
        "kpp": Optional[str],
    },
)

AdminClientFilter = TypedDict(
    "AdminClientFilter",
    {
        "ids": Optional[List[str]],
        "name": Optional[str],
        "organizationID": Optional[str],
    },
)

ClientFilter = TypedDict(
    "ClientFilter",
    {
        "ids": Optional[List[str]],
        "name": Optional[str],
    },
)

CreativeCreateData = TypedDict(
    "CreativeCreateData",
    {
        "frameID": str,
        "externalFileID": Optional[str],
        "name": Optional[str],
        "naming": Optional[str],
        "adSizeID": str,
    },
)

CreativeUpdateData = TypedDict(
    "CreativeUpdateData",
    {
        "id": str,
        "frameID": str,
        "externalFileID": Optional[str],
        "name": Optional[str],
        "adSizeID": str,
    },
)

PlacementCreativesCreateData = TypedDict(
    "PlacementCreativesCreateData",
    {
        "creativeIDs": List[str],
        "placementID": str,
    },
)

PlacementCreativeUpdateData = TypedDict(
    "PlacementCreativeUpdateData",
    {
        "id": str,
        "name": Optional[str],
    },
)

CreativeFrameCreateData = TypedDict(
    "CreativeFrameCreateData",
    {
        "name": str,
        "naming": str,
        "campaignID": str,
    },
)

CreativeFileAttachData = TypedDict(
    "CreativeFileAttachData",
    {
        "creativeID": str,
        "externalFileID": str,
    },
)

PlacementCreativeFileAttachData = TypedDict(
    "PlacementCreativeFileAttachData",
    {
        "placementCreativeID": str,
        "externalFileID": str,
    },
)

DigitalReportFilter = TypedDict(
    "DigitalReportFilter",
    {
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
    },
)

GoalData = TypedDict(
    "GoalData",
    {
        "name": str,
        "code": str,
        "metricCodes": List[str],
        "naming": str,
    },
)

IntegrationTokenFilter = TypedDict(
    "IntegrationTokenFilter",
    {
        "iToolIDs": Optional[List[str]],
        "status": Optional["TokenStatus"],
    },
)

IntegrationTokenData = TypedDict(
    "IntegrationTokenData",
    {
        "iToolID": str,
        "account": str,
        "accessToken": str,
    },
)

IntegrationToolFilter = TypedDict(
    "IntegrationToolFilter",
    {
        "types": Optional[List["IToolType"]],
        "codes": Optional[List[str]],
    },
)

FactConversionData = TypedDict(
    "FactConversionData",
    {
        "id": str,
        "name": str,
        "sourceCode": str,
    },
)

PlanFactConversionData = TypedDict(
    "PlanFactConversionData",
    {
        "mplanConversionID": str,
        "factConversion": Optional["FactConversionData"],
    },
)

MatchedConversionsData = TypedDict(
    "MatchedConversionsData",
    {
        "sourceCode": str,
        "counterID": Optional[str],
        "matchedConversions": List["PlanFactConversionData"],
    },
)

MetricData = TypedDict(
    "MetricData",
    {
        "name": str,
        "description": Optional[str],
        "operation": "OperationType",
        "precision": int,
        "canSplit": bool,
        "isConversion": bool,
        "isTracker": bool,
        "type": "MetricType",
    },
)

MetricFilter = TypedDict(
    "MetricFilter",
    {
        "codes": Optional[List[str]],
        "goalIDs": Optional[List[str]],
        "canSplit": Optional[bool],
        "isConversion": Optional[bool],
        "isTracker": Optional[bool],
        "type": Optional["MetricType"],
    },
)

MplanConversionData = TypedDict(
    "MplanConversionData",
    {
        "mplanID": str,
        "name": str,
    },
)

MplanData = TypedDict(
    "MplanData",
    {
        "campaignID": str,
        "landings": Optional[List[str]],
        "constraints": Optional[List["MplanConstraintData"]],
    },
)

MplanConstraintData = TypedDict(
    "MplanConstraintData",
    {
        "id": Optional[str],
        "metricCode": str,
        "operation": "OperationType",
        "value": "Decimal",
    },
)

MplanLandingData = TypedDict(
    "MplanLandingData",
    {
        "mplanID": str,
        "url": str,
    },
)

MplanFilter = TypedDict(
    "MplanFilter",
    {
        "campaignID": Optional[List[str]],
    },
)

MplanDataUploadImportData = TypedDict(
    "MplanDataUploadImportData",
    {
        "externalFileID": str,
        "mplanID": str,
    },
)

MplanFromTemplateData = TypedDict(
    "MplanFromTemplateData",
    {
        "campaignID": str,
    },
)

MplanXLSImportData = TypedDict(
    "MplanXLSImportData",
    {
        "externalFileID": str,
        "campaignID": str,
    },
)

OrganizationLinkSort = TypedDict(
    "OrganizationLinkSort",
    {
        "direction": Optional["SortDirection"],
        "field": Optional["OrganizationLinkField"],
    },
)

AdminOrganizationLinkFilter = TypedDict(
    "AdminOrganizationLinkFilter",
    {
        "clientName": Optional[str],
        "brandName": Optional[str],
        "productName": Optional[str],
        "organizationID": Optional[str],
    },
)

OrganizationLinkFilter = TypedDict(
    "OrganizationLinkFilter",
    {
        "clientName": Optional[str],
        "brandName": Optional[str],
        "productName": Optional[str],
    },
)

AdminOrganizationLinkData = TypedDict(
    "AdminOrganizationLinkData",
    {
        "organizationID": str,
        "clientID": str,
        "brandID": str,
        "productID": str,
    },
)

OrganizationLinkData = TypedDict(
    "OrganizationLinkData",
    {
        "clientID": str,
        "brandID": str,
        "productID": str,
    },
)

OrganizationData = TypedDict(
    "OrganizationData",
    {
        "roleCode": "OrganizationRole",
        "okopf": Optional[str],
        "fullName": str,
        "shortName": str,
        "firmName": Optional[str],
        "inn": str,
        "ogrn": Optional[str],
        "kpp": Optional[str],
        "address": Optional[str],
        "phone": Optional[str],
        "email": str,
    },
)

OrganizationFilter = TypedDict(
    "OrganizationFilter",
    {
        "fullName": Optional[str],
        "inn": Optional[str],
        "kpp": Optional[str],
        "address": Optional[str],
        "phone": Optional[str],
        "statuses": Optional[List["OrganizationStatus"]],
        "registeredFrom": Optional["Time"],
        "registeredTo": Optional["Time"],
        "blockedFrom": Optional["Time"],
        "blockedTo": Optional["Time"],
    },
)

OrganizationSort = TypedDict(
    "OrganizationSort",
    {
        "direction": Optional["SortDirection"],
        "field": Optional["OrganizationSortField"],
    },
)

PlacementCommentData = TypedDict(
    "PlacementCommentData",
    {
        "text": str,
    },
)

PlacementMetricListData = TypedDict(
    "PlacementMetricListData",
    {
        "metrics": Optional[List["PlacementMetricData"]],
        "conversionLinks": Optional[List["PlacementConversionLinkData"]],
    },
)

PlacementMetricData = TypedDict(
    "PlacementMetricData",
    {
        "id": Optional[str],
        "metricCode": str,
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementConversionLinkData = TypedDict(
    "PlacementConversionLinkData",
    {
        "id": Optional[str],
        "mplanConversionID": str,
        "isMain": bool,
        "metrics": List["PlacementMetricData"],
    },
)

PlacementPricingData = TypedDict(
    "PlacementPricingData",
    {
        "pricePerUnit": "Decimal",
        "numberOfUnitsPerPeriod": "Decimal",
        "markupForFrequency": "Decimal",
        "markupForPlatform": "Decimal",
        "markupForGeotargeting": "Decimal",
        "markupForGenderAge": "Decimal",
        "markupForSeasonality": "Decimal",
        "markupForCurrencyTransfer": "Decimal",
        "markupForOther": "Decimal",
        "mediaDiscount": "Decimal",
        "vat": "Decimal",
    },
)

PlacementStatusFilter = TypedDict(
    "PlacementStatusFilter",
    {
        "placementID": Optional[str],
        "statusCodes": Optional[List[str]],
    },
)

PlacementStatusSort = TypedDict(
    "PlacementStatusSort",
    {
        "direction": Optional["SortDirection"],
    },
)

PlacementTargetingData = TypedDict(
    "PlacementTargetingData",
    {
        "targetAudience": Optional[str],
        "targetGeo": Optional[str],
    },
)

PlacementToolUpdateData = TypedDict(
    "PlacementToolUpdateData",
    {
        "counterID": str,
    },
)

PlacementToolData = TypedDict(
    "PlacementToolData",
    {
        "type": "IToolType",
        "gatherMethod": Optional["GatherMethod"],
        "publishMethod": Optional["PublishMethod"],
        "trackingMethod": Optional["TrackingMethod"],
        "iTokenID": Optional[str],
        "iToolID": Optional[str],
        "apps": Optional[List["PlacementToolAppData"]],
        "counterID": Optional[str],
    },
)

PlacementAppsflyerParameterData = TypedDict(
    "PlacementAppsflyerParameterData",
    {
        "retargeting": bool,
        "reEngagementPeriod": Optional[str],
        "attributionWindowPeriod": Optional[str],
    },
)

PlacementToolAppData = TypedDict(
    "PlacementToolAppData",
    {
        "applicationID": str,
        "applicationName": str,
        "applicationPlatform": Optional[str],
        "inAppEvents": Optional[List[str]],
    },
)

PlacementCalcMetricData = TypedDict(
    "PlacementCalcMetricData",
    {
        "id": Optional[str],
        "metricCode": str,
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementCalcConversionData = TypedDict(
    "PlacementCalcConversionData",
    {
        "id": Optional[str],
        "isMain": bool,
        "metrics": List["PlacementCalcMetricData"],
    },
)

PlacementCalcMetricsData = TypedDict(
    "PlacementCalcMetricsData",
    {
        "metrics": List["PlacementCalcMetricData"],
        "conversions": List["PlacementCalcConversionData"],
        "mplanID": Optional[str],
        "placementID": Optional[str],
    },
)

PlacementCalcMetricsEvent = TypedDict(
    "PlacementCalcMetricsEvent",
    {
        "eventAction": Optional["PlacementCalcEventAction"],
        "id": Optional[str],
        "metricCode": Optional[str],
        "newMetricCode": Optional[str],
        "conversionID": Optional[str],
        "value": Optional["Decimal"],
        "buyTypeCode": Optional[str],
    },
)

PlacementData = TypedDict(
    "PlacementData",
    {
        "mplanID": str,
        "name": str,
        "extraNaming": Optional[str],
        "siteID": Optional[str],
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
        "landingURL": Optional[str],
        "channelCode": Optional[str],
        "buyTypeID": Optional[str],
        "adFormatID": Optional[str],
        "adSizes": Optional[List[str]],
        "siteSectionID": Optional[str],
        "siteElementID": Optional[str],
        "adSystemID": Optional[str],
        "appsflyerPartnerID": Optional[str],
        "appsflyerParameter": Optional["PlacementAppsflyerParameterData"],
        "projectID": Optional[str],
        "placementType": Optional["PlacementType"],
        "platforms": List["Platform"],
        "sellerID": Optional[str],
        "timekeeping": Optional[int],
    },
)

PlacementFilter = TypedDict(
    "PlacementFilter",
    {
        "statusIDs": Optional[List[str]],
        "statusCodes": Optional[List[str]],
        "mplanIDs": Optional[List[str]],
        "mplanConversionIDs": Optional[List[str]],
        "channelCode": Optional["ChannelCodeFilter"],
    },
)

ChannelCodeFilter = TypedDict(
    "ChannelCodeFilter",
    {
        "isEmpty": Optional[bool],
        "codes": Optional[List[str]],
    },
)

PlacementDuplicateData = TypedDict(
    "PlacementDuplicateData",
    {
        "name": str,
    },
)

PlacementFromTemplateData = TypedDict(
    "PlacementFromTemplateData",
    {
        "mplanID": str,
        "name": str,
        "startOn": "Time",
        "finishOn": "Time",
    },
)

PricePositionData = TypedDict(
    "PricePositionData",
    {
        "code": str,
        "sellerID": Optional[str],
        "region": Optional[str],
        "providerPosition": Optional[str],
        "siteIDs": Optional[List[str]],
        "onSitePosition": str,
        "channelCode": str,
        "formatID": Optional[str],
        "sizeIDs": Optional[List[str]],
        "placementType": Optional["PlacementType"],
        "buyTypeID": str,
        "platforms": Optional[List["Platform"]],
        "defaultGeoTargeting": Optional[str],
        "defaultFrequency": Optional[int],
        "priceWithoutVat": "Decimal",
        "vatRate": int,
        "mediaRate": "Decimal",
        "extraCharge": Optional["Decimal"],
        "guaranteedCapacity": "Decimal",
        "comment": Optional[str],
        "januaryCoef": "Decimal",
        "februaryCoef": "Decimal",
        "marchCoef": "Decimal",
        "aprilCoef": "Decimal",
        "mayCoef": "Decimal",
        "juneCoef": "Decimal",
        "julyCoef": "Decimal",
        "augustCoef": "Decimal",
        "septemberCoef": "Decimal",
        "octoberCoef": "Decimal",
        "novemberCoef": "Decimal",
        "decemberCoef": "Decimal",
        "extraChargeMaxRate": int,
        "dayFrequencyRate": Optional[int],
        "weekFrequencyRate": Optional[int],
        "monthFrequencyRate": Optional[int],
        "rfGeoRate": Optional[int],
        "regionGeoRate": Optional[int],
        "superGeoRate": Optional[int],
        "genderRate": Optional[int],
        "incomeRate": Optional[int],
        "interestsRate": Optional[int],
        "platformRate": Optional[int],
        "cellOperatorRate": Optional[int],
        "secondBrandRate": Optional[int],
        "whiteListRate": Optional[int],
        "brandSafetyRate": Optional[int],
    },
)

PricelistCreateData = TypedDict(
    "PricelistCreateData",
    {
        "clientID": str,
        "code": str,
        "type": "PricelistType",
        "startOn": "Time",
        "finishOn": "Time",
        "status": "PricelistStatus",
        "comments": Optional[str],
    },
)

PricelistUpdateData = TypedDict(
    "PricelistUpdateData",
    {
        "code": str,
        "startOn": "Time",
        "finishOn": "Time",
        "status": "PricelistStatus",
        "comments": Optional[str],
    },
)

PricelistFilter = TypedDict(
    "PricelistFilter",
    {
        "clientIDs": Optional[List[str]],
        "status": Optional["PricelistStatus"],
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
        "type": Optional["PricelistType"],
    },
)

PricelistSort = TypedDict(
    "PricelistSort",
    {
        "direction": Optional["SortDirection"],
        "field": Optional["PricelistField"],
    },
)

PricePositionSort = TypedDict(
    "PricePositionSort",
    {
        "direction": Optional["SortDirection"],
        "field": Optional["PricePositionField"],
    },
)

ProductCategoryCreateData = TypedDict(
    "ProductCategoryCreateData",
    {
        "name": str,
        "code": str,
        "typeID": str,
        "isUsedBySplan": bool,
    },
)

ProductCategoryUpdateData = TypedDict(
    "ProductCategoryUpdateData",
    {
        "name": str,
        "typeID": str,
        "isUsedBySplan": bool,
    },
)

ProductCategoryFilter = TypedDict(
    "ProductCategoryFilter",
    {
        "typeID": Optional[str],
        "isUsedBySplan": Optional[bool],
    },
)

ProductLinks = TypedDict(
    "ProductLinks",
    {
        "clientID": str,
        "brandID": str,
    },
)

AdminProductData = TypedDict(
    "AdminProductData",
    {
        "name": str,
        "naming": str,
        "deepLink": Optional[str],
        "geographyID": Optional[str],
        "typeID": str,
        "categoryID": str,
        "priceCategoryID": Optional[str],
        "seasonalityID": Optional[str],
        "seasonalityValueIDs": Optional[List[str]],
        "purchaseFrequencyID": Optional[str],
        "organizationID": str,
    },
)

ProductData = TypedDict(
    "ProductData",
    {
        "name": str,
        "naming": str,
        "deepLink": Optional[str],
        "links": Optional["ProductLinks"],
        "geographyID": Optional[str],
        "typeID": str,
        "categoryID": str,
        "priceCategoryID": Optional[str],
        "seasonalityID": Optional[str],
        "seasonalityValueIDs": Optional[List[str]],
        "purchaseFrequencyID": Optional[str],
    },
)

AdminProductFilter = TypedDict(
    "AdminProductFilter",
    {
        "name": Optional[str],
        "brandIDs": Optional[List[str]],
        "clientIDs": Optional[List[str]],
        "organizationID": Optional[str],
    },
)

ProductFilter = TypedDict(
    "ProductFilter",
    {
        "name": Optional[str],
        "brandIDs": Optional[List[str]],
        "clientIDs": Optional[List[str]],
    },
)

AdminProfileData = TypedDict(
    "AdminProfileData",
    {
        "name": Optional[str],
        "surname": Optional[str],
        "middleName": Optional[str],
        "organizationID": str,
        "login": str,
        "email": str,
        "phone": str,
        "contactPhone": Optional[str],
        "rolesID": Optional[List[str]],
    },
)

ProfileData = TypedDict(
    "ProfileData",
    {
        "name": Optional[str],
        "surname": Optional[str],
        "middleName": Optional[str],
        "login": str,
        "email": str,
        "phone": str,
        "contactPhone": Optional[str],
        "rolesID": Optional[List[str]],
    },
)

ProfileFilter = TypedDict(
    "ProfileFilter",
    {
        "login": Optional[str],
        "surname": Optional[str],
        "name": Optional[str],
        "email": Optional[str],
        "orgName": Optional[str],
        "status": Optional["UserStatus"],
        "registeredFrom": Optional["Time"],
        "registeredTo": Optional["Time"],
        "blockedFrom": Optional["Time"],
        "blockedTo": Optional["Time"],
    },
)

ProfileSort = TypedDict(
    "ProfileSort",
    {
        "direction": Optional["SortDirection"],
        "field": Optional["ProfileSortField"],
    },
)

SellerData = TypedDict(
    "SellerData",
    {
        "name": str,
        "naming": str,
        "sources": List[str],
    },
)

ListSlice = TypedDict(
    "ListSlice",
    {
        "offset": Optional[int],
        "limit": Optional[int],
    },
)

SimpleDict = TypedDict(
    "SimpleDict",
    {
        "name": str,
    },
)

SiteElementData = TypedDict(
    "SiteElementData",
    {
        "name": str,
        "naming": str,
    },
)

SiteSectionData = TypedDict(
    "SiteSectionData",
    {
        "name": str,
        "naming": str,
    },
)

SourceFilter = TypedDict(
    "SourceFilter",
    {
        "sellerID": Optional[List[str]],
        "type": Optional[List["SourceType"]],
        "adSizeID": Optional[List[str]],
        "buyTypeID": Optional[List[str]],
        "status": Optional["SourceStatus"],
        "publishMethod": Optional["PublishMethod"],
        "canAutoGather": Optional[bool],
    },
)

SourceAdSizeData = TypedDict(
    "SourceAdSizeData",
    {
        "adFormatID": str,
        "adSizeID": str,
    },
)

SourceBuyTypeData = TypedDict(
    "SourceBuyTypeData",
    {
        "adFormatID": str,
        "buyTypeID": str,
    },
)

SourceSiteDataCreate = TypedDict(
    "SourceSiteDataCreate",
    {
        "name": str,
        "shortName": str,
        "code": str,
        "url": str,
        "naming": str,
        "hasAdset": bool,
        "canAutoGather": bool,
        "publishMethod": "PublishMethod",
        "status": "SourceStatus",
        "sellerID": Optional[str],
        "adSizes": List["SourceAdSizeData"],
        "buyTypes": List["SourceBuyTypeData"],
    },
)

SourceSiteDataUpdate = TypedDict(
    "SourceSiteDataUpdate",
    {
        "name": str,
        "shortName": str,
        "url": str,
        "naming": str,
        "hasAdset": bool,
        "canAutoGather": bool,
        "publishMethod": "PublishMethod",
        "status": "SourceStatus",
        "sellerID": Optional[str],
        "adSizes": List["SourceAdSizeData"],
        "buyTypes": List["SourceBuyTypeData"],
    },
)

SourceToolDataCreate = TypedDict(
    "SourceToolDataCreate",
    {
        "name": str,
        "shortName": str,
        "code": str,
        "url": str,
        "naming": str,
        "canAutoGather": bool,
        "status": "SourceStatus",
        "type": "SourceToolType",
    },
)

SourceToolDataUpdate = TypedDict(
    "SourceToolDataUpdate",
    {
        "name": str,
        "url": str,
        "naming": str,
        "canAutoGather": bool,
        "status": "SourceStatus",
    },
)

StratPlanData = TypedDict(
    "StratPlanData",
    {
        "clientCode": str,
        "brandCode": str,
        "productCode": Optional[str],
        "productCategoryCode": Optional[str],
        "smpGoalID": str,
        "smpCompetitorStrategyID": str,
        "dateStart": "Date",
        "dateEnd": "Date",
        "smpAudienceID": str,
        "hasSubAudience": bool,
        "smpProductKnowledgeID": str,
        "smpCommunicationID": str,
    },
)

TVCampaignData = TypedDict(
    "TVCampaignData",
    {
        "name": str,
        "clientID": str,
        "brandID": Optional[str],
        "productID": Optional[str],
        "startOn": "Time",
        "finishOn": "Time",
        "marketTargets": Optional[str],
        "targetAudience": Optional[str],
        "conditions": Optional[str],
    },
)

TVCampaignFilter = TypedDict(
    "TVCampaignFilter",
    {
        "clientID": Optional[List[str]],
        "brandID": Optional[List[str]],
        "productID": Optional[List[str]],
        "statusID": Optional[List[str]],
        "startOn": Optional["Time"],
        "finishOn": Optional["Time"],
    },
)

TVMplanData = TypedDict(
    "TVMplanData",
    {
        "campaignID": str,
        "goalCode": str,
        "constraints": List["TVMplanConstraintData"],
    },
)

TVMplanConstraintData = TypedDict(
    "TVMplanConstraintData",
    {
        "id": Optional[str],
        "metricCode": str,
        "op": "TVOperationType",
        "value": "Decimal",
    },
)

UnitData = TypedDict(
    "UnitData",
    {
        "name": str,
        "shortName": str,
        "orderNo": int,
    },
)

PlacementUtmParameterData = TypedDict(
    "PlacementUtmParameterData",
    {
        "parameterID": str,
        "arbitraryValue": bool,
        "templateID": Optional[str],
        "value": Optional[str],
    },
)

PlacementTemplateMetricData = TypedDict(
    "PlacementTemplateMetricData",
    {
        "metricCode": str,
        "value": "Decimal",
        "isCalculated": bool,
    },
)

PlacementTemplateConversionData = TypedDict(
    "PlacementTemplateConversionData",
    {
        "name": Optional[str],
        "isMain": bool,
        "metrics": List["PlacementTemplateMetricData"],
    },
)

PlacementTemplateMetricListData = TypedDict(
    "PlacementTemplateMetricListData",
    {
        "metrics": List["PlacementTemplateMetricData"],
        "conversions": List["PlacementTemplateConversionData"],
    },
)

MplanTemplateFilter = TypedDict(
    "MplanTemplateFilter",
    {
        "name": Optional[str],
        "placementsCount": Optional[int],
        "clientID": Optional[str],
    },
)

MplanTemplateData = TypedDict(
    "MplanTemplateData",
    {
        "name": str,
    },
)

PlacementTemplateFilter = TypedDict(
    "PlacementTemplateFilter",
    {
        "clientID": Optional[str],
        "mplanTemplateID": Optional[str],
        "isBelongsToMplanTemplate": Optional[bool],
    },
)

TemplateFromPlacementData = TypedDict(
    "TemplateFromPlacementData",
    {
        "clientID": str,
    },
)

PlacementTemplateData = TypedDict(
    "PlacementTemplateData",
    {
        "clientID": str,
        "siteID": str,
        "sellerID": str,
        "channelCode": str,
        "placementType": "TplPlacementType",
        "buyTypeID": str,
        "adFormatID": Optional[str],
        "adSizeIDs": Optional[List[str]],
        "metricList": Optional["PlacementTemplateMetricListData"],
    },
)
