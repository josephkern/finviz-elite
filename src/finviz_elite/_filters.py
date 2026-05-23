"""Screener filter enums and the Elite custom-range API.

Split from ``_enums.py`` so that module stays readable as the screener
filter taxonomy fills in -- one enum per filter category, plus the
``ScreenerRange`` enum for the Elite custom numeric-range API and the
``FilterEnum`` union the screener accepts.

Custom-range token shape (verified live against the screener UI):

- Closed:        ``{prefix}_{min}to{max}``    e.g. ``fa_pe_10to20``
- Min only:      ``{prefix}_{min}to``         e.g. ``fa_pe_10to``
- Max only:      ``{prefix}_to{max}``         e.g. ``fa_pe_to20``
- Both ``None``: token omitted -- Finviz rejects ``{prefix}_to``.
"""

from enum import Enum
from typing import Union


# --- Descriptive tier --------------------------------------------------


class FilterExchange(Enum):
    """Screener exchange filter, mapped to its ``f=`` token."""

    AMEX = "exch_amex"
    NASDAQ = "exch_nasd"
    NYSE = "exch_nyse"


class FilterIndex(Enum):
    """Screener index-membership filter, mapped to its ``f=`` token."""

    SP500 = "idx_sp500"
    DJIA = "idx_dji"
    NASDAQ100 = "idx_ndx"
    RUSSELL2000 = "idx_rut"


class FilterSector(Enum):
    """Screener sector filter, mapped to its ``f=`` token."""

    BASIC_MATERIALS = "sec_basicmaterials"
    COMMUNICATION_SERVICES = "sec_communicationservices"
    CONSUMER_CYCLICAL = "sec_consumercyclical"
    CONSUMER_DEFENSIVE = "sec_consumerdefensive"
    ENERGY = "sec_energy"
    FINANCIAL = "sec_financial"
    HEALTHCARE = "sec_healthcare"
    INDUSTRIALS = "sec_industrials"
    REAL_ESTATE = "sec_realestate"
    TECHNOLOGY = "sec_technology"
    UTILITIES = "sec_utilities"


class FilterIndustry(Enum):
    """Screener industry filter, mapped to its ``f=`` token.

    Industries are the next-level breakdown below sector; an industry
    belongs to exactly one sector. ``STOCKS_ONLY`` and
    ``EXCHANGE_TRADED_FUND`` are not industries per se -- they filter
    on the security type.
    """

    STOCKS_ONLY = "ind_stocksonly"
    EXCHANGE_TRADED_FUND = "ind_exchangetradedfund"
    ADVERTISING_AGENCIES = "ind_advertisingagencies"
    AEROSPACE_DEFENSE = "ind_aerospacedefense"
    AGRICULTURAL_INPUTS = "ind_agriculturalinputs"
    AIRLINES = "ind_airlines"
    AIRPORTS_AIR_SERVICES = "ind_airportsairservices"
    ALUMINUM = "ind_aluminum"
    APPAREL_MANUFACTURING = "ind_apparelmanufacturing"
    APPAREL_RETAIL = "ind_apparelretail"
    ASSET_MANAGEMENT = "ind_assetmanagement"
    AUTO_MANUFACTURERS = "ind_automanufacturers"
    AUTO_PARTS = "ind_autoparts"
    AUTO_TRUCK_DEALERSHIPS = "ind_autotruckdealerships"
    BANKS_DIVERSIFIED = "ind_banksdiversified"
    BANKS_REGIONAL = "ind_banksregional"
    BEVERAGES_BREWERS = "ind_beveragesbrewers"
    BEVERAGES_NON_ALCOHOLIC = "ind_beveragesnonalcoholic"
    BEVERAGES_WINERIES_DISTILLERIES = "ind_beverageswineriesdistilleries"
    BIOTECHNOLOGY = "ind_biotechnology"
    BROADCASTING = "ind_broadcasting"
    BUILDING_MATERIALS = "ind_buildingmaterials"
    BUILDING_PRODUCTS_EQUIPMENT = "ind_buildingproductsequipment"
    BUSINESS_EQUIPMENT_SUPPLIES = "ind_businessequipmentsupplies"
    CAPITAL_MARKETS = "ind_capitalmarkets"
    CHEMICALS = "ind_chemicals"
    CLOSED_END_FUND_DEBT = "ind_closedendfunddebt"
    CLOSED_END_FUND_EQUITY = "ind_closedendfundequity"
    CLOSED_END_FUND_FOREIGN = "ind_closedendfundforeign"
    COKING_COAL = "ind_cokingcoal"
    COMMUNICATION_EQUIPMENT = "ind_communicationequipment"
    COMPUTER_HARDWARE = "ind_computerhardware"
    CONFECTIONERS = "ind_confectioners"
    CONGLOMERATES = "ind_conglomerates"
    CONSULTING_SERVICES = "ind_consultingservices"
    CONSUMER_ELECTRONICS = "ind_consumerelectronics"
    COPPER = "ind_copper"
    CREDIT_SERVICES = "ind_creditservices"
    DEPARTMENT_STORES = "ind_departmentstores"
    DIAGNOSTICS_RESEARCH = "ind_diagnosticsresearch"
    DISCOUNT_STORES = "ind_discountstores"
    DRUG_MANUFACTURERS_GENERAL = "ind_drugmanufacturersgeneral"
    DRUG_MANUFACTURERS_SPECIALTY_GENERIC = "ind_drugmanufacturersspecialtygeneric"
    EDUCATION_TRAINING_SERVICES = "ind_educationtrainingservices"
    ELECTRICAL_EQUIPMENT_PARTS = "ind_electricalequipmentparts"
    ELECTRONIC_COMPONENTS = "ind_electroniccomponents"
    ELECTRONIC_GAMING_MULTIMEDIA = "ind_electronicgamingmultimedia"
    ELECTRONICS_COMPUTER_DISTRIBUTION = "ind_electronicscomputerdistribution"
    ENGINEERING_CONSTRUCTION = "ind_engineeringconstruction"
    ENTERTAINMENT = "ind_entertainment"
    FARM_HEAVY_CONSTRUCTION_MACHINERY = "ind_farmheavyconstructionmachinery"
    FARM_PRODUCTS = "ind_farmproducts"
    FINANCIAL_CONGLOMERATES = "ind_financialconglomerates"
    FINANCIAL_DATA_STOCK_EXCHANGES = "ind_financialdatastockexchanges"
    FOOD_DISTRIBUTION = "ind_fooddistribution"
    FOOTWEAR_ACCESSORIES = "ind_footwearaccessories"
    FURNISHINGS_FIXTURES_APPLIANCES = "ind_furnishingsfixturesappliances"
    GAMBLING = "ind_gambling"
    GOLD = "ind_gold"
    GROCERY_STORES = "ind_grocerystores"
    HEALTHCARE_PLANS = "ind_healthcareplans"
    HEALTH_INFORMATION_SERVICES = "ind_healthinformationservices"
    HOME_IMPROVEMENT_RETAIL = "ind_homeimprovementretail"
    HOUSEHOLD_PERSONAL_PRODUCTS = "ind_householdpersonalproducts"
    INDUSTRIAL_DISTRIBUTION = "ind_industrialdistribution"
    INFORMATION_TECHNOLOGY_SERVICES = "ind_informationtechnologyservices"
    INFRASTRUCTURE_OPERATIONS = "ind_infrastructureoperations"
    INSURANCE_BROKERS = "ind_insurancebrokers"
    INSURANCE_DIVERSIFIED = "ind_insurancediversified"
    INSURANCE_LIFE = "ind_insurancelife"
    INSURANCE_PROPERTY_CASUALTY = "ind_insurancepropertycasualty"
    INSURANCE_REINSURANCE = "ind_insurancereinsurance"
    INSURANCE_SPECIALTY = "ind_insurancespecialty"
    INTEGRATED_FREIGHT_LOGISTICS = "ind_integratedfreightlogistics"
    INTERNET_CONTENT_INFORMATION = "ind_internetcontentinformation"
    INTERNET_RETAIL = "ind_internetretail"
    LEISURE = "ind_leisure"
    LODGING = "ind_lodging"
    LUMBER_WOOD_PRODUCTION = "ind_lumberwoodproduction"
    LUXURY_GOODS = "ind_luxurygoods"
    MARINE_SHIPPING = "ind_marineshipping"
    MEDICAL_CARE_FACILITIES = "ind_medicalcarefacilities"
    MEDICAL_DEVICES = "ind_medicaldevices"
    MEDICAL_DISTRIBUTION = "ind_medicaldistribution"
    MEDICAL_INSTRUMENTS_SUPPLIES = "ind_medicalinstrumentssupplies"
    METAL_FABRICATION = "ind_metalfabrication"
    MORTGAGE_FINANCE = "ind_mortgagefinance"
    OIL_GAS_DRILLING = "ind_oilgasdrilling"
    OIL_GAS_EP = "ind_oilgasep"
    OIL_GAS_EQUIPMENT_SERVICES = "ind_oilgasequipmentservices"
    OIL_GAS_INTEGRATED = "ind_oilgasintegrated"
    OIL_GAS_MIDSTREAM = "ind_oilgasmidstream"
    OIL_GAS_REFINING_MARKETING = "ind_oilgasrefiningmarketing"
    OTHER_INDUSTRIAL_METALS_MINING = "ind_otherindustrialmetalsmining"
    OTHER_PRECIOUS_METALS_MINING = "ind_otherpreciousmetalsmining"
    PACKAGED_FOODS = "ind_packagedfoods"
    PACKAGING_CONTAINERS = "ind_packagingcontainers"
    PAPER_PAPER_PRODUCTS = "ind_paperpaperproducts"
    PERSONAL_SERVICES = "ind_personalservices"
    PHARMACEUTICAL_RETAILERS = "ind_pharmaceuticalretailers"
    POLLUTION_TREATMENT_CONTROLS = "ind_pollutiontreatmentcontrols"
    PUBLISHING = "ind_publishing"
    RAILROADS = "ind_railroads"
    REAL_ESTATE_DEVELOPMENT = "ind_realestatedevelopment"
    REAL_ESTATE_DIVERSIFIED = "ind_realestatediversified"
    REAL_ESTATE_SERVICES = "ind_realestateservices"
    RECREATIONAL_VEHICLES = "ind_recreationalvehicles"
    REIT_DIVERSIFIED = "ind_reitdiversified"
    REIT_HEALTHCARE_FACILITIES = "ind_reithealthcarefacilities"
    REIT_HOTEL_MOTEL = "ind_reithotelmotel"
    REIT_INDUSTRIAL = "ind_reitindustrial"
    REIT_MORTGAGE = "ind_reitmortgage"
    REIT_OFFICE = "ind_reitoffice"
    REIT_RESIDENTIAL = "ind_reitresidential"
    REIT_RETAIL = "ind_reitretail"
    REIT_SPECIALTY = "ind_reitspecialty"
    RENTAL_LEASING_SERVICES = "ind_rentalleasingservices"
    RESIDENTIAL_CONSTRUCTION = "ind_residentialconstruction"
    RESORTS_CASINOS = "ind_resortscasinos"
    RESTAURANTS = "ind_restaurants"
    SCIENTIFIC_TECHNICAL_INSTRUMENTS = "ind_scientifictechnicalinstruments"
    SECURITY_PROTECTION_SERVICES = "ind_securityprotectionservices"
    SEMICONDUCTOR_EQUIPMENT_MATERIALS = "ind_semiconductorequipmentmaterials"
    SEMICONDUCTORS = "ind_semiconductors"
    SHELL_COMPANIES = "ind_shellcompanies"
    SILVER = "ind_silver"
    SOFTWARE_APPLICATION = "ind_softwareapplication"
    SOFTWARE_INFRASTRUCTURE = "ind_softwareinfrastructure"
    SOLAR = "ind_solar"
    SPECIALTY_BUSINESS_SERVICES = "ind_specialtybusinessservices"
    SPECIALTY_CHEMICALS = "ind_specialtychemicals"
    SPECIALTY_INDUSTRIAL_MACHINERY = "ind_specialtyindustrialmachinery"
    SPECIALTY_RETAIL = "ind_specialtyretail"
    STAFFING_EMPLOYMENT_SERVICES = "ind_staffingemploymentservices"
    STEEL = "ind_steel"
    TELECOM_SERVICES = "ind_telecomservices"
    TEXTILE_MANUFACTURING = "ind_textilemanufacturing"
    THERMAL_COAL = "ind_thermalcoal"
    TOBACCO = "ind_tobacco"
    TOOLS_ACCESSORIES = "ind_toolsaccessories"
    TRAVEL_SERVICES = "ind_travelservices"
    TRUCKING = "ind_trucking"
    URANIUM = "ind_uranium"
    UTILITIES_DIVERSIFIED = "ind_utilitiesdiversified"
    UTILITIES_INDEPENDENT_POWER_PRODUCERS = "ind_utilitiesindependentpowerproducers"
    UTILITIES_REGULATED_ELECTRIC = "ind_utilitiesregulatedelectric"
    UTILITIES_REGULATED_GAS = "ind_utilitiesregulatedgas"
    UTILITIES_REGULATED_WATER = "ind_utilitiesregulatedwater"
    UTILITIES_RENEWABLE = "ind_utilitiesrenewable"
    WASTE_MANAGEMENT = "ind_wastemanagement"


class FilterCountry(Enum):
    """Screener country / geographic filter, mapped to its ``f=`` token.

    Filters on the company's country of domicile. The bundled regional
    aggregates (ASIA, EUROPE, LATIN_AMERICA, BRIC) and the FOREIGN
    bucket (NOT_USA) match Finviz's own grouping.
    """

    USA = "geo_usa"
    NOT_USA = "geo_notusa"
    ASIA = "geo_asia"
    EUROPE = "geo_europe"
    LATIN_AMERICA = "geo_latinamerica"
    BRIC = "geo_bric"
    ARGENTINA = "geo_argentina"
    AUSTRALIA = "geo_australia"
    BAHAMAS = "geo_bahamas"
    BELGIUM = "geo_belgium"
    BENELUX = "geo_benelux"
    BERMUDA = "geo_bermuda"
    BRAZIL = "geo_brazil"
    CANADA = "geo_canada"
    CAYMAN_ISLANDS = "geo_caymanislands"
    CHILE = "geo_chile"
    CHINA = "geo_china"
    CHINA_HONG_KONG = "geo_chinahongkong"
    COLOMBIA = "geo_colombia"
    CYPRUS = "geo_cyprus"
    DENMARK = "geo_denmark"
    FINLAND = "geo_finland"
    FRANCE = "geo_france"
    GERMANY = "geo_germany"
    GREECE = "geo_greece"
    HONG_KONG = "geo_hongkong"
    HUNGARY = "geo_hungary"
    ICELAND = "geo_iceland"
    INDIA = "geo_india"
    INDONESIA = "geo_indonesia"
    IRELAND = "geo_ireland"
    ISRAEL = "geo_israel"
    ITALY = "geo_italy"
    JAPAN = "geo_japan"
    KAZAKHSTAN = "geo_kazakhstan"
    LUXEMBOURG = "geo_luxembourg"
    MALAYSIA = "geo_malaysia"
    MALTA = "geo_malta"
    MEXICO = "geo_mexico"
    MONACO = "geo_monaco"
    NETHERLANDS = "geo_netherlands"
    NEW_ZEALAND = "geo_newzealand"
    NORWAY = "geo_norway"
    PANAMA = "geo_panama"
    PERU = "geo_peru"
    PHILIPPINES = "geo_philippines"
    PORTUGAL = "geo_portugal"
    RUSSIA = "geo_russia"
    SINGAPORE = "geo_singapore"
    SOUTH_AFRICA = "geo_southafrica"
    SOUTH_KOREA = "geo_southkorea"
    SPAIN = "geo_spain"
    SWEDEN = "geo_sweden"
    SWITZERLAND = "geo_switzerland"
    TAIWAN = "geo_taiwan"
    TURKEY = "geo_turkey"
    UNITED_ARAB_EMIRATES = "geo_unitedarabemirates"
    UNITED_KINGDOM = "geo_unitedkingdom"
    URUGUAY = "geo_uruguay"


class FilterMarketCap(Enum):
    """Screener market-cap filter, mapped to its ``f=`` token.

    Six preset bands (MEGA..NANO) plus the eight ``*_OVER`` /
    ``*_UNDER`` cumulative variants Finviz exposes.
    """

    MEGA = "cap_mega"             # $200bln and above
    LARGE = "cap_large"           # $10bln to $200bln
    MID = "cap_mid"               # $2bln to $10bln
    SMALL = "cap_small"           # $300mln to $2bln
    MICRO = "cap_micro"           # $50mln to $300mln
    NANO = "cap_nano"             # under $50mln
    LARGE_OVER = "cap_largeover"  # over $10bln
    MID_OVER = "cap_midover"      # over $2bln
    SMALL_OVER = "cap_smallover"  # over $300mln
    MICRO_OVER = "cap_microover"  # over $50mln
    LARGE_UNDER = "cap_largeunder"  # under $200bln
    MID_UNDER = "cap_midunder"    # under $10bln
    SMALL_UNDER = "cap_smallunder"  # under $2bln
    MICRO_UNDER = "cap_microunder"  # under $300mln


class FilterEarningsDate(Enum):
    """Screener earnings-date filter, mapped to its ``f=`` token.

    The ``_BEFORE_OPEN`` / ``_AFTER_CLOSE`` variants narrow the day
    bucket to the pre-market or after-hours report window.
    """

    TODAY = "earningsdate_today"
    TODAY_BEFORE_OPEN = "earningsdate_todaybefore"
    TODAY_AFTER_CLOSE = "earningsdate_todayafter"
    TOMORROW = "earningsdate_tomorrow"
    TOMORROW_BEFORE_OPEN = "earningsdate_tomorrowbefore"
    TOMORROW_AFTER_CLOSE = "earningsdate_tomorrowafter"
    YESTERDAY = "earningsdate_yesterday"
    YESTERDAY_BEFORE_OPEN = "earningsdate_yesterdaybefore"
    YESTERDAY_AFTER_CLOSE = "earningsdate_yesterdayafter"
    NEXT_5_DAYS = "earningsdate_nextdays5"
    PREV_5_DAYS = "earningsdate_prevdays5"
    THIS_WEEK = "earningsdate_thisweek"
    NEXT_WEEK = "earningsdate_nextweek"
    PREV_WEEK = "earningsdate_prevweek"
    THIS_MONTH = "earningsdate_thismonth"


class FilterIPODate(Enum):
    """Screener IPO-date filter, mapped to its ``f=`` token."""

    TODAY = "ipodate_today"
    YESTERDAY = "ipodate_yesterday"
    LAST_WEEK = "ipodate_prevweek"
    LAST_MONTH = "ipodate_prevmonth"
    LAST_QUARTER = "ipodate_prevquarter"
    LAST_YEAR = "ipodate_prevyear"
    LAST_2_YEARS = "ipodate_prev2yrs"
    LAST_3_YEARS = "ipodate_prev3yrs"
    LAST_5_YEARS = "ipodate_prev5yrs"
    OVER_1_YEAR_AGO = "ipodate_more1"
    OVER_5_YEARS_AGO = "ipodate_more5"
    OVER_10_YEARS_AGO = "ipodate_more10"
    OVER_15_YEARS_AGO = "ipodate_more15"
    OVER_20_YEARS_AGO = "ipodate_more20"
    OVER_25_YEARS_AGO = "ipodate_more25"


class FilterSharesOutstanding(Enum):
    """Screener shares-outstanding filter, mapped to its ``f=`` token.

    Brackets are absolute share counts (``M`` = millions). Use the
    ``ranges`` API with custom bounds for non-bracket cutoffs.
    """

    UNDER_1M = "sh_outstanding_u1"
    UNDER_5M = "sh_outstanding_u5"
    UNDER_10M = "sh_outstanding_u10"
    UNDER_20M = "sh_outstanding_u20"
    UNDER_50M = "sh_outstanding_u50"
    UNDER_100M = "sh_outstanding_u100"
    OVER_1M = "sh_outstanding_o1"
    OVER_2M = "sh_outstanding_o2"
    OVER_5M = "sh_outstanding_o5"
    OVER_10M = "sh_outstanding_o10"
    OVER_20M = "sh_outstanding_o20"
    OVER_50M = "sh_outstanding_o50"
    OVER_100M = "sh_outstanding_o100"
    OVER_200M = "sh_outstanding_o200"
    OVER_500M = "sh_outstanding_o500"
    OVER_1000M = "sh_outstanding_o1000"


class FilterFloat(Enum):
    """Screener float filter, mapped to its ``f=`` token.

    Two complementary bracket sets: absolute share counts
    (``*_1M`` .. ``*_1000M``) and float as a percentage of shares
    outstanding (``*_10_PCT`` .. ``*_90_PCT``).
    """

    UNDER_1M = "sh_float_u1"
    UNDER_5M = "sh_float_u5"
    UNDER_10M = "sh_float_u10"
    UNDER_20M = "sh_float_u20"
    UNDER_50M = "sh_float_u50"
    UNDER_100M = "sh_float_u100"
    OVER_1M = "sh_float_o1"
    OVER_2M = "sh_float_o2"
    OVER_5M = "sh_float_o5"
    OVER_10M = "sh_float_o10"
    OVER_20M = "sh_float_o20"
    OVER_50M = "sh_float_o50"
    OVER_100M = "sh_float_o100"
    OVER_200M = "sh_float_o200"
    OVER_500M = "sh_float_o500"
    OVER_1000M = "sh_float_o1000"
    UNDER_10_PCT = "sh_float_u10p"
    UNDER_20_PCT = "sh_float_u20p"
    UNDER_30_PCT = "sh_float_u30p"
    UNDER_40_PCT = "sh_float_u40p"
    UNDER_50_PCT = "sh_float_u50p"
    UNDER_60_PCT = "sh_float_u60p"
    UNDER_70_PCT = "sh_float_u70p"
    UNDER_80_PCT = "sh_float_u80p"
    UNDER_90_PCT = "sh_float_u90p"
    OVER_10_PCT = "sh_float_o10p"
    OVER_20_PCT = "sh_float_o20p"
    OVER_30_PCT = "sh_float_o30p"
    OVER_40_PCT = "sh_float_o40p"
    OVER_50_PCT = "sh_float_o50p"
    OVER_60_PCT = "sh_float_o60p"
    OVER_70_PCT = "sh_float_o70p"
    OVER_80_PCT = "sh_float_o80p"
    OVER_90_PCT = "sh_float_o90p"


class FilterOptionShort(Enum):
    """Screener optionable / shortable filter, mapped to its ``f=`` token.

    Filters on whether a security has listed options and/or is
    available to borrow short. The four NOT_*/_NOT_* combinations let
    callers AND a positive condition with its negation in a single
    pick.
    """

    OPTIONABLE = "sh_opt_option"
    SHORTABLE = "sh_opt_short"
    OPTIONABLE_AND_SHORTABLE = "sh_opt_optionshort"
    NOT_OPTIONABLE = "sh_opt_notoption"
    NOT_SHORTABLE = "sh_opt_notshort"
    OPTIONABLE_NOT_SHORTABLE = "sh_opt_optionnotshort"
    NOT_OPTIONABLE_SHORTABLE = "sh_opt_notoptionshort"
    NOT_OPTIONABLE_NOT_SHORTABLE = "sh_opt_notoptionnotshort"


class FilterAnalystRecom(Enum):
    """Screener analyst-recommendation filter, mapped to its ``f=`` token.

    Finviz collapses sell-side ratings onto a 1-5 scale: 1 = Strong
    Buy, 2 = Buy, 3 = Hold, 4 = Sell, 5 = Strong Sell. The ``_OR_BETTER``
    / ``_OR_WORSE`` variants are open-ended buckets toward the
    Strong Buy / Strong Sell ends.
    """

    STRONG_BUY = "an_recom_strongbuy"
    BUY_OR_BETTER = "an_recom_buybetter"
    BUY = "an_recom_buy"
    HOLD_OR_BETTER = "an_recom_holdbetter"
    HOLD = "an_recom_hold"
    HOLD_OR_WORSE = "an_recom_holdworse"
    SELL = "an_recom_sell"
    SELL_OR_WORSE = "an_recom_sellworse"
    STRONG_SELL = "an_recom_strongsell"


# --- Elite custom numeric ranges ---------------------------------------


class ScreenerRange(Enum):
    """Metrics that accept an Elite custom numeric range, mapped to the
    metric's ``f=`` token prefix.

    Bounds are supplied at call time via ``screener(ranges=...)``; the
    token is built as ``{prefix}_{min}to{max}`` with either side omitted
    when ``None``. Both bounds ``None`` skips the metric -- Finviz
    rejects ``{prefix}_to`` outright.
    """

    PE = "fa_pe"
    BETA = "ta_beta"


# Every screener filter enum is a member of this Union. The screener's
# ``filters`` param accepts any member of any enum in this Union, giving
# the MCP surface a single fully-typed pick-from-list.
FilterEnum = Union[
    FilterExchange,
    FilterIndex,
    FilterSector,
    FilterIndustry,
    FilterCountry,
    FilterMarketCap,
    FilterEarningsDate,
    FilterIPODate,
    FilterSharesOutstanding,
    FilterFloat,
    FilterOptionShort,
    FilterAnalystRecom,
]
