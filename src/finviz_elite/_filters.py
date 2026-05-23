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


# --- Fundamental tier -------------------------------------------------


class FilterPE(Enum):
    """Screener P/E (price/earnings) filter, mapped to its ``f=`` token."""

    LOW = "fa_pe_low"
    PROFITABLE = "fa_pe_profitable"
    HIGH = "fa_pe_high"
    UNDER_5 = "fa_pe_u5"
    UNDER_10 = "fa_pe_u10"
    UNDER_15 = "fa_pe_u15"
    UNDER_20 = "fa_pe_u20"
    UNDER_25 = "fa_pe_u25"
    UNDER_30 = "fa_pe_u30"
    UNDER_35 = "fa_pe_u35"
    UNDER_40 = "fa_pe_u40"
    UNDER_45 = "fa_pe_u45"
    UNDER_50 = "fa_pe_u50"
    OVER_5 = "fa_pe_o5"
    OVER_10 = "fa_pe_o10"
    OVER_15 = "fa_pe_o15"
    OVER_20 = "fa_pe_o20"
    OVER_25 = "fa_pe_o25"
    OVER_30 = "fa_pe_o30"
    OVER_35 = "fa_pe_o35"
    OVER_40 = "fa_pe_o40"
    OVER_45 = "fa_pe_o45"
    OVER_50 = "fa_pe_o50"


class FilterForwardPE(Enum):
    """Screener Forward P/E filter, mapped to its ``f=`` token."""

    LOW = "fa_fpe_low"
    PROFITABLE = "fa_fpe_profitable"
    HIGH = "fa_fpe_high"
    UNDER_5 = "fa_fpe_u5"
    UNDER_10 = "fa_fpe_u10"
    UNDER_15 = "fa_fpe_u15"
    UNDER_20 = "fa_fpe_u20"
    UNDER_25 = "fa_fpe_u25"
    UNDER_30 = "fa_fpe_u30"
    UNDER_35 = "fa_fpe_u35"
    UNDER_40 = "fa_fpe_u40"
    UNDER_45 = "fa_fpe_u45"
    UNDER_50 = "fa_fpe_u50"
    OVER_5 = "fa_fpe_o5"
    OVER_10 = "fa_fpe_o10"
    OVER_15 = "fa_fpe_o15"
    OVER_20 = "fa_fpe_o20"
    OVER_25 = "fa_fpe_o25"
    OVER_30 = "fa_fpe_o30"
    OVER_35 = "fa_fpe_o35"
    OVER_40 = "fa_fpe_o40"
    OVER_45 = "fa_fpe_o45"
    OVER_50 = "fa_fpe_o50"


class FilterPEG(Enum):
    """Screener PEG (P/E to growth) filter, mapped to its ``f=`` token."""

    LOW = "fa_peg_low"
    HIGH = "fa_peg_high"
    UNDER_1 = "fa_peg_u1"
    UNDER_2 = "fa_peg_u2"
    UNDER_3 = "fa_peg_u3"
    OVER_1 = "fa_peg_o1"
    OVER_2 = "fa_peg_o2"
    OVER_3 = "fa_peg_o3"


class FilterPS(Enum):
    """Screener P/S (price/sales) filter, mapped to its ``f=`` token."""

    LOW = "fa_ps_low"
    HIGH = "fa_ps_high"
    UNDER_1 = "fa_ps_u1"
    UNDER_2 = "fa_ps_u2"
    UNDER_3 = "fa_ps_u3"
    UNDER_4 = "fa_ps_u4"
    UNDER_5 = "fa_ps_u5"
    UNDER_6 = "fa_ps_u6"
    UNDER_7 = "fa_ps_u7"
    UNDER_8 = "fa_ps_u8"
    UNDER_9 = "fa_ps_u9"
    UNDER_10 = "fa_ps_u10"
    OVER_1 = "fa_ps_o1"
    OVER_2 = "fa_ps_o2"
    OVER_3 = "fa_ps_o3"
    OVER_4 = "fa_ps_o4"
    OVER_5 = "fa_ps_o5"
    OVER_6 = "fa_ps_o6"
    OVER_7 = "fa_ps_o7"
    OVER_8 = "fa_ps_o8"
    OVER_9 = "fa_ps_o9"
    OVER_10 = "fa_ps_o10"


class FilterPB(Enum):
    """Screener P/B (price/book) filter, mapped to its ``f=`` token."""

    LOW = "fa_pb_low"
    HIGH = "fa_pb_high"
    UNDER_1 = "fa_pb_u1"
    UNDER_2 = "fa_pb_u2"
    UNDER_3 = "fa_pb_u3"
    UNDER_4 = "fa_pb_u4"
    UNDER_5 = "fa_pb_u5"
    UNDER_6 = "fa_pb_u6"
    UNDER_7 = "fa_pb_u7"
    UNDER_8 = "fa_pb_u8"
    UNDER_9 = "fa_pb_u9"
    UNDER_10 = "fa_pb_u10"
    OVER_1 = "fa_pb_o1"
    OVER_2 = "fa_pb_o2"
    OVER_3 = "fa_pb_o3"
    OVER_4 = "fa_pb_o4"
    OVER_5 = "fa_pb_o5"
    OVER_6 = "fa_pb_o6"
    OVER_7 = "fa_pb_o7"
    OVER_8 = "fa_pb_o8"
    OVER_9 = "fa_pb_o9"
    OVER_10 = "fa_pb_o10"


class FilterPC(Enum):
    """Screener P/Cash filter, mapped to its ``f=`` token."""

    LOW = "fa_pc_low"
    HIGH = "fa_pc_high"
    UNDER_1 = "fa_pc_u1"
    UNDER_2 = "fa_pc_u2"
    UNDER_3 = "fa_pc_u3"
    UNDER_4 = "fa_pc_u4"
    UNDER_5 = "fa_pc_u5"
    UNDER_6 = "fa_pc_u6"
    UNDER_7 = "fa_pc_u7"
    UNDER_8 = "fa_pc_u8"
    UNDER_9 = "fa_pc_u9"
    UNDER_10 = "fa_pc_u10"
    OVER_1 = "fa_pc_o1"
    OVER_2 = "fa_pc_o2"
    OVER_3 = "fa_pc_o3"
    OVER_4 = "fa_pc_o4"
    OVER_5 = "fa_pc_o5"
    OVER_6 = "fa_pc_o6"
    OVER_7 = "fa_pc_o7"
    OVER_8 = "fa_pc_o8"
    OVER_9 = "fa_pc_o9"
    OVER_10 = "fa_pc_o10"
    OVER_20 = "fa_pc_o20"
    OVER_30 = "fa_pc_o30"
    OVER_40 = "fa_pc_o40"
    OVER_50 = "fa_pc_o50"


class FilterPFCF(Enum):
    """Screener P/Free Cash Flow filter, mapped to its ``f=`` token."""

    LOW = "fa_pfcf_low"
    HIGH = "fa_pfcf_high"
    UNDER_5 = "fa_pfcf_u5"
    UNDER_10 = "fa_pfcf_u10"
    UNDER_15 = "fa_pfcf_u15"
    UNDER_20 = "fa_pfcf_u20"
    UNDER_25 = "fa_pfcf_u25"
    UNDER_30 = "fa_pfcf_u30"
    UNDER_35 = "fa_pfcf_u35"
    UNDER_40 = "fa_pfcf_u40"
    UNDER_45 = "fa_pfcf_u45"
    UNDER_50 = "fa_pfcf_u50"
    UNDER_60 = "fa_pfcf_u60"
    UNDER_70 = "fa_pfcf_u70"
    UNDER_80 = "fa_pfcf_u80"
    UNDER_90 = "fa_pfcf_u90"
    UNDER_100 = "fa_pfcf_u100"
    OVER_5 = "fa_pfcf_o5"
    OVER_10 = "fa_pfcf_o10"
    OVER_15 = "fa_pfcf_o15"
    OVER_20 = "fa_pfcf_o20"
    OVER_25 = "fa_pfcf_o25"
    OVER_30 = "fa_pfcf_o30"
    OVER_35 = "fa_pfcf_o35"
    OVER_40 = "fa_pfcf_o40"
    OVER_45 = "fa_pfcf_o45"
    OVER_50 = "fa_pfcf_o50"
    OVER_60 = "fa_pfcf_o60"
    OVER_70 = "fa_pfcf_o70"
    OVER_80 = "fa_pfcf_o80"
    OVER_90 = "fa_pfcf_o90"
    OVER_100 = "fa_pfcf_o100"


class FilterEPSGrowthThisYear(Enum):
    """Screener EPS growth this year filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_epsyoy_neg"
    POSITIVE = "fa_epsyoy_pos"
    POSITIVE_LOW = "fa_epsyoy_poslow"
    HIGH = "fa_epsyoy_high"
    UNDER_5_PCT = "fa_epsyoy_u5"
    UNDER_10_PCT = "fa_epsyoy_u10"
    UNDER_15_PCT = "fa_epsyoy_u15"
    UNDER_20_PCT = "fa_epsyoy_u20"
    UNDER_25_PCT = "fa_epsyoy_u25"
    UNDER_30_PCT = "fa_epsyoy_u30"
    OVER_5_PCT = "fa_epsyoy_o5"
    OVER_10_PCT = "fa_epsyoy_o10"
    OVER_15_PCT = "fa_epsyoy_o15"
    OVER_20_PCT = "fa_epsyoy_o20"
    OVER_25_PCT = "fa_epsyoy_o25"
    OVER_30_PCT = "fa_epsyoy_o30"


class FilterEPSGrowthNextYear(Enum):
    """Screener EPS growth next year filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_epsyoy1_neg"
    POSITIVE = "fa_epsyoy1_pos"
    POSITIVE_LOW = "fa_epsyoy1_poslow"
    HIGH = "fa_epsyoy1_high"
    UNDER_5_PCT = "fa_epsyoy1_u5"
    UNDER_10_PCT = "fa_epsyoy1_u10"
    UNDER_15_PCT = "fa_epsyoy1_u15"
    UNDER_20_PCT = "fa_epsyoy1_u20"
    UNDER_25_PCT = "fa_epsyoy1_u25"
    UNDER_30_PCT = "fa_epsyoy1_u30"
    OVER_5_PCT = "fa_epsyoy1_o5"
    OVER_10_PCT = "fa_epsyoy1_o10"
    OVER_15_PCT = "fa_epsyoy1_o15"
    OVER_20_PCT = "fa_epsyoy1_o20"
    OVER_25_PCT = "fa_epsyoy1_o25"
    OVER_30_PCT = "fa_epsyoy1_o30"


class FilterEPSGrowthPast5Y(Enum):
    """Screener EPS growth past 5 years filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_eps5years_neg"
    POSITIVE = "fa_eps5years_pos"
    POSITIVE_LOW = "fa_eps5years_poslow"
    HIGH = "fa_eps5years_high"
    UNDER_5_PCT = "fa_eps5years_u5"
    UNDER_10_PCT = "fa_eps5years_u10"
    UNDER_15_PCT = "fa_eps5years_u15"
    UNDER_20_PCT = "fa_eps5years_u20"
    UNDER_25_PCT = "fa_eps5years_u25"
    UNDER_30_PCT = "fa_eps5years_u30"
    OVER_5_PCT = "fa_eps5years_o5"
    OVER_10_PCT = "fa_eps5years_o10"
    OVER_15_PCT = "fa_eps5years_o15"
    OVER_20_PCT = "fa_eps5years_o20"
    OVER_25_PCT = "fa_eps5years_o25"
    OVER_30_PCT = "fa_eps5years_o30"


class FilterEPSGrowthNext5Y(Enum):
    """Screener EPS growth next 5 years filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_estltgrowth_neg"
    POSITIVE = "fa_estltgrowth_pos"
    POSITIVE_LOW = "fa_estltgrowth_poslow"
    HIGH = "fa_estltgrowth_high"
    UNDER_5_PCT = "fa_estltgrowth_u5"
    UNDER_10_PCT = "fa_estltgrowth_u10"
    UNDER_15_PCT = "fa_estltgrowth_u15"
    UNDER_20_PCT = "fa_estltgrowth_u20"
    UNDER_25_PCT = "fa_estltgrowth_u25"
    UNDER_30_PCT = "fa_estltgrowth_u30"
    OVER_5_PCT = "fa_estltgrowth_o5"
    OVER_10_PCT = "fa_estltgrowth_o10"
    OVER_15_PCT = "fa_estltgrowth_o15"
    OVER_20_PCT = "fa_estltgrowth_o20"
    OVER_25_PCT = "fa_estltgrowth_o25"
    OVER_30_PCT = "fa_estltgrowth_o30"


class FilterSalesGrowthPast5Y(Enum):
    """Screener sales growth past 5 years filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_sales5years_neg"
    POSITIVE = "fa_sales5years_pos"
    POSITIVE_LOW = "fa_sales5years_poslow"
    HIGH = "fa_sales5years_high"
    UNDER_5_PCT = "fa_sales5years_u5"
    UNDER_10_PCT = "fa_sales5years_u10"
    UNDER_15_PCT = "fa_sales5years_u15"
    UNDER_20_PCT = "fa_sales5years_u20"
    UNDER_25_PCT = "fa_sales5years_u25"
    UNDER_30_PCT = "fa_sales5years_u30"
    OVER_5_PCT = "fa_sales5years_o5"
    OVER_10_PCT = "fa_sales5years_o10"
    OVER_15_PCT = "fa_sales5years_o15"
    OVER_20_PCT = "fa_sales5years_o20"
    OVER_25_PCT = "fa_sales5years_o25"
    OVER_30_PCT = "fa_sales5years_o30"


class FilterEPSGrowthTTM(Enum):
    """Screener EPS growth ttm filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_epsyoyttm_neg"
    POSITIVE = "fa_epsyoyttm_pos"
    POSITIVE_LOW = "fa_epsyoyttm_poslow"
    HIGH = "fa_epsyoyttm_high"
    UNDER_5_PCT = "fa_epsyoyttm_u5"
    UNDER_10_PCT = "fa_epsyoyttm_u10"
    UNDER_15_PCT = "fa_epsyoyttm_u15"
    UNDER_20_PCT = "fa_epsyoyttm_u20"
    UNDER_25_PCT = "fa_epsyoyttm_u25"
    UNDER_30_PCT = "fa_epsyoyttm_u30"
    OVER_5_PCT = "fa_epsyoyttm_o5"
    OVER_10_PCT = "fa_epsyoyttm_o10"
    OVER_15_PCT = "fa_epsyoyttm_o15"
    OVER_20_PCT = "fa_epsyoyttm_o20"
    OVER_25_PCT = "fa_epsyoyttm_o25"
    OVER_30_PCT = "fa_epsyoyttm_o30"


class FilterEPSGrowthQoQ(Enum):
    """Screener EPS growth quarter-over-quarter filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_epsqoq_neg"
    POSITIVE = "fa_epsqoq_pos"
    POSITIVE_LOW = "fa_epsqoq_poslow"
    HIGH = "fa_epsqoq_high"
    UNDER_5_PCT = "fa_epsqoq_u5"
    UNDER_10_PCT = "fa_epsqoq_u10"
    UNDER_15_PCT = "fa_epsqoq_u15"
    UNDER_20_PCT = "fa_epsqoq_u20"
    UNDER_25_PCT = "fa_epsqoq_u25"
    UNDER_30_PCT = "fa_epsqoq_u30"
    OVER_5_PCT = "fa_epsqoq_o5"
    OVER_10_PCT = "fa_epsqoq_o10"
    OVER_15_PCT = "fa_epsqoq_o15"
    OVER_20_PCT = "fa_epsqoq_o20"
    OVER_25_PCT = "fa_epsqoq_o25"
    OVER_30_PCT = "fa_epsqoq_o30"


class FilterSalesGrowthQoQ(Enum):
    """Screener sales growth quarter-over-quarter filter, mapped to its ``f=`` token."""

    NEGATIVE = "fa_salesqoq_neg"
    POSITIVE = "fa_salesqoq_pos"
    POSITIVE_LOW = "fa_salesqoq_poslow"
    HIGH = "fa_salesqoq_high"
    UNDER_5_PCT = "fa_salesqoq_u5"
    UNDER_10_PCT = "fa_salesqoq_u10"
    UNDER_15_PCT = "fa_salesqoq_u15"
    UNDER_20_PCT = "fa_salesqoq_u20"
    UNDER_25_PCT = "fa_salesqoq_u25"
    UNDER_30_PCT = "fa_salesqoq_u30"
    OVER_5_PCT = "fa_salesqoq_o5"
    OVER_10_PCT = "fa_salesqoq_o10"
    OVER_15_PCT = "fa_salesqoq_o15"
    OVER_20_PCT = "fa_salesqoq_o20"
    OVER_25_PCT = "fa_salesqoq_o25"
    OVER_30_PCT = "fa_salesqoq_o30"


class FilterEarningsRevenueSurprise(Enum):
    """Screener earnings & revenue surprise filter, mapped to its ``f=`` token."""

    BOTH_POSITIVE = "fa_epsrev_bp"
    BOTH_MET = "fa_epsrev_bm"
    BOTH_NEGATIVE = "fa_epsrev_bn"
    EPS_POSITIVE = "fa_epsrev_ep"
    EPS_MET = "fa_epsrev_em"
    EPS_NEGATIVE = "fa_epsrev_en"
    EPS_UNDER_5_PCT = "fa_epsrev_eu5"
    EPS_UNDER_10_PCT = "fa_epsrev_eu10"
    EPS_UNDER_20_PCT = "fa_epsrev_eu20"
    EPS_UNDER_30_PCT = "fa_epsrev_eu30"
    EPS_UNDER_40_PCT = "fa_epsrev_eu40"
    EPS_UNDER_50_PCT = "fa_epsrev_eu50"
    EPS_UNDER_100_PCT = "fa_epsrev_eu100"
    EPS_OVER_5_PCT = "fa_epsrev_eo5"
    EPS_OVER_10_PCT = "fa_epsrev_eo10"
    EPS_OVER_20_PCT = "fa_epsrev_eo20"
    EPS_OVER_30_PCT = "fa_epsrev_eo30"
    EPS_OVER_40_PCT = "fa_epsrev_eo40"
    EPS_OVER_50_PCT = "fa_epsrev_eo50"
    EPS_OVER_60_PCT = "fa_epsrev_eo60"
    EPS_OVER_70_PCT = "fa_epsrev_eo70"
    EPS_OVER_80_PCT = "fa_epsrev_eo80"
    EPS_OVER_90_PCT = "fa_epsrev_eo90"
    EPS_OVER_100_PCT = "fa_epsrev_eo100"
    EPS_OVER_200_PCT = "fa_epsrev_eo200"
    REVENUE_POSITIVE = "fa_epsrev_rp"
    REVENUE_MET = "fa_epsrev_rm"
    REVENUE_NEGATIVE = "fa_epsrev_rn"
    REVENUE_UNDER_5_PCT = "fa_epsrev_ru5"
    REVENUE_UNDER_10_PCT = "fa_epsrev_ru10"
    REVENUE_UNDER_20_PCT = "fa_epsrev_ru20"
    REVENUE_UNDER_30_PCT = "fa_epsrev_ru30"
    REVENUE_UNDER_40_PCT = "fa_epsrev_ru40"
    REVENUE_UNDER_50_PCT = "fa_epsrev_ru50"
    REVENUE_UNDER_100_PCT = "fa_epsrev_ru100"
    REVENUE_OVER_5_PCT = "fa_epsrev_ro5"
    REVENUE_OVER_10_PCT = "fa_epsrev_ro10"
    REVENUE_OVER_20_PCT = "fa_epsrev_ro20"
    REVENUE_OVER_30_PCT = "fa_epsrev_ro30"
    REVENUE_OVER_40_PCT = "fa_epsrev_ro40"
    REVENUE_OVER_50_PCT = "fa_epsrev_ro50"
    REVENUE_OVER_60_PCT = "fa_epsrev_ro60"
    REVENUE_OVER_70_PCT = "fa_epsrev_ro70"
    REVENUE_OVER_80_PCT = "fa_epsrev_ro80"
    REVENUE_OVER_90_PCT = "fa_epsrev_ro90"
    REVENUE_OVER_100_PCT = "fa_epsrev_ro100"
    REVENUE_OVER_200_PCT = "fa_epsrev_ro200"


class FilterDividendYield(Enum):
    """Screener dividend yield filter, mapped to its ``f=`` token."""

    NONE = "fa_div_none"
    POSITIVE = "fa_div_pos"
    HIGH = "fa_div_high"
    VERY_HIGH = "fa_div_veryhigh"
    OVER_1_PCT = "fa_div_o1"
    OVER_2_PCT = "fa_div_o2"
    OVER_3_PCT = "fa_div_o3"
    OVER_4_PCT = "fa_div_o4"
    OVER_5_PCT = "fa_div_o5"
    OVER_6_PCT = "fa_div_o6"
    OVER_7_PCT = "fa_div_o7"
    OVER_8_PCT = "fa_div_o8"
    OVER_9_PCT = "fa_div_o9"
    OVER_10_PCT = "fa_div_o10"


class FilterPayoutRatio(Enum):
    """Screener dividend payout ratio filter, mapped to its ``f=`` token."""

    NONE = "fa_payoutratio_none"
    POSITIVE = "fa_payoutratio_pos"
    LOW = "fa_payoutratio_low"
    HIGH = "fa_payoutratio_high"
    OVER_0_PCT = "fa_payoutratio_o0"
    OVER_10_PCT = "fa_payoutratio_o10"
    OVER_20_PCT = "fa_payoutratio_o20"
    OVER_30_PCT = "fa_payoutratio_o30"
    OVER_40_PCT = "fa_payoutratio_o40"
    OVER_50_PCT = "fa_payoutratio_o50"
    OVER_60_PCT = "fa_payoutratio_o60"
    OVER_70_PCT = "fa_payoutratio_o70"
    OVER_80_PCT = "fa_payoutratio_o80"
    OVER_90_PCT = "fa_payoutratio_o90"
    OVER_100_PCT = "fa_payoutratio_o100"
    UNDER_10_PCT = "fa_payoutratio_u10"
    UNDER_20_PCT = "fa_payoutratio_u20"
    UNDER_30_PCT = "fa_payoutratio_u30"
    UNDER_40_PCT = "fa_payoutratio_u40"
    UNDER_50_PCT = "fa_payoutratio_u50"
    UNDER_60_PCT = "fa_payoutratio_u60"
    UNDER_70_PCT = "fa_payoutratio_u70"
    UNDER_80_PCT = "fa_payoutratio_u80"
    UNDER_90_PCT = "fa_payoutratio_u90"
    UNDER_100_PCT = "fa_payoutratio_u100"


class FilterReturnOnAssets(Enum):
    """Screener Return on Assets filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_roa_pos"
    NEGATIVE = "fa_roa_neg"
    VERY_POSITIVE = "fa_roa_verypos"
    VERY_NEGATIVE = "fa_roa_veryneg"
    UNDER_NEG_5_PCT = "fa_roa_u-5"
    UNDER_NEG_10_PCT = "fa_roa_u-10"
    UNDER_NEG_15_PCT = "fa_roa_u-15"
    UNDER_NEG_20_PCT = "fa_roa_u-20"
    UNDER_NEG_25_PCT = "fa_roa_u-25"
    UNDER_NEG_30_PCT = "fa_roa_u-30"
    UNDER_NEG_35_PCT = "fa_roa_u-35"
    UNDER_NEG_40_PCT = "fa_roa_u-40"
    UNDER_NEG_45_PCT = "fa_roa_u-45"
    UNDER_NEG_50_PCT = "fa_roa_u-50"
    OVER_5_PCT = "fa_roa_o5"
    OVER_10_PCT = "fa_roa_o10"
    OVER_15_PCT = "fa_roa_o15"
    OVER_20_PCT = "fa_roa_o20"
    OVER_25_PCT = "fa_roa_o25"
    OVER_30_PCT = "fa_roa_o30"
    OVER_35_PCT = "fa_roa_o35"
    OVER_40_PCT = "fa_roa_o40"
    OVER_45_PCT = "fa_roa_o45"
    OVER_50_PCT = "fa_roa_o50"


class FilterReturnOnEquity(Enum):
    """Screener Return on Equity filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_roe_pos"
    NEGATIVE = "fa_roe_neg"
    VERY_POSITIVE = "fa_roe_verypos"
    VERY_NEGATIVE = "fa_roe_veryneg"
    UNDER_NEG_5_PCT = "fa_roe_u-5"
    UNDER_NEG_10_PCT = "fa_roe_u-10"
    UNDER_NEG_15_PCT = "fa_roe_u-15"
    UNDER_NEG_20_PCT = "fa_roe_u-20"
    UNDER_NEG_25_PCT = "fa_roe_u-25"
    UNDER_NEG_30_PCT = "fa_roe_u-30"
    UNDER_NEG_35_PCT = "fa_roe_u-35"
    UNDER_NEG_40_PCT = "fa_roe_u-40"
    UNDER_NEG_45_PCT = "fa_roe_u-45"
    UNDER_NEG_50_PCT = "fa_roe_u-50"
    OVER_5_PCT = "fa_roe_o5"
    OVER_10_PCT = "fa_roe_o10"
    OVER_15_PCT = "fa_roe_o15"
    OVER_20_PCT = "fa_roe_o20"
    OVER_25_PCT = "fa_roe_o25"
    OVER_30_PCT = "fa_roe_o30"
    OVER_35_PCT = "fa_roe_o35"
    OVER_40_PCT = "fa_roe_o40"
    OVER_45_PCT = "fa_roe_o45"
    OVER_50_PCT = "fa_roe_o50"


class FilterReturnOnInvestment(Enum):
    """Screener Return on Investment filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_roi_pos"
    NEGATIVE = "fa_roi_neg"
    VERY_POSITIVE = "fa_roi_verypos"
    VERY_NEGATIVE = "fa_roi_veryneg"
    UNDER_NEG_5_PCT = "fa_roi_u-5"
    UNDER_NEG_10_PCT = "fa_roi_u-10"
    UNDER_NEG_15_PCT = "fa_roi_u-15"
    UNDER_NEG_20_PCT = "fa_roi_u-20"
    UNDER_NEG_25_PCT = "fa_roi_u-25"
    UNDER_NEG_30_PCT = "fa_roi_u-30"
    UNDER_NEG_35_PCT = "fa_roi_u-35"
    UNDER_NEG_40_PCT = "fa_roi_u-40"
    UNDER_NEG_45_PCT = "fa_roi_u-45"
    UNDER_NEG_50_PCT = "fa_roi_u-50"
    OVER_5_PCT = "fa_roi_o5"
    OVER_10_PCT = "fa_roi_o10"
    OVER_15_PCT = "fa_roi_o15"
    OVER_20_PCT = "fa_roi_o20"
    OVER_25_PCT = "fa_roi_o25"
    OVER_30_PCT = "fa_roi_o30"
    OVER_35_PCT = "fa_roi_o35"
    OVER_40_PCT = "fa_roi_o40"
    OVER_45_PCT = "fa_roi_o45"
    OVER_50_PCT = "fa_roi_o50"


class FilterCurrentRatio(Enum):
    """Screener current ratio filter, mapped to its ``f=`` token."""

    HIGH = "fa_curratio_high"
    LOW = "fa_curratio_low"
    UNDER_1 = "fa_curratio_u1"
    UNDER_0_5 = "fa_curratio_u0.5"
    OVER_0_5 = "fa_curratio_o0.5"
    OVER_1 = "fa_curratio_o1"
    OVER_1_5 = "fa_curratio_o1.5"
    OVER_2 = "fa_curratio_o2"
    OVER_3 = "fa_curratio_o3"
    OVER_4 = "fa_curratio_o4"
    OVER_5 = "fa_curratio_o5"
    OVER_10 = "fa_curratio_o10"


class FilterQuickRatio(Enum):
    """Screener quick ratio filter, mapped to its ``f=`` token."""

    HIGH = "fa_quickratio_high"
    LOW = "fa_quickratio_low"
    UNDER_1 = "fa_quickratio_u1"
    UNDER_0_5 = "fa_quickratio_u0.5"
    OVER_0_5 = "fa_quickratio_o0.5"
    OVER_1 = "fa_quickratio_o1"
    OVER_1_5 = "fa_quickratio_o1.5"
    OVER_2 = "fa_quickratio_o2"
    OVER_3 = "fa_quickratio_o3"
    OVER_4 = "fa_quickratio_o4"
    OVER_5 = "fa_quickratio_o5"
    OVER_10 = "fa_quickratio_o10"


class FilterLTDebtEquity(Enum):
    """Screener long-term debt/equity filter, mapped to its ``f=`` token."""

    HIGH = "fa_ltdebteq_high"
    LOW = "fa_ltdebteq_low"
    UNDER_1 = "fa_ltdebteq_u1"
    UNDER_0_9 = "fa_ltdebteq_u0.9"
    UNDER_0_8 = "fa_ltdebteq_u0.8"
    UNDER_0_7 = "fa_ltdebteq_u0.7"
    UNDER_0_6 = "fa_ltdebteq_u0.6"
    UNDER_0_5 = "fa_ltdebteq_u0.5"
    UNDER_0_4 = "fa_ltdebteq_u0.4"
    UNDER_0_3 = "fa_ltdebteq_u0.3"
    UNDER_0_2 = "fa_ltdebteq_u0.2"
    UNDER_0_1 = "fa_ltdebteq_u0.1"
    OVER_0_1 = "fa_ltdebteq_o0.1"
    OVER_0_2 = "fa_ltdebteq_o0.2"
    OVER_0_3 = "fa_ltdebteq_o0.3"
    OVER_0_4 = "fa_ltdebteq_o0.4"
    OVER_0_5 = "fa_ltdebteq_o0.5"
    OVER_0_6 = "fa_ltdebteq_o0.6"
    OVER_0_7 = "fa_ltdebteq_o0.7"
    OVER_0_8 = "fa_ltdebteq_o0.8"
    OVER_0_9 = "fa_ltdebteq_o0.9"
    OVER_1 = "fa_ltdebteq_o1"


class FilterDebtEquity(Enum):
    """Screener total debt/equity filter, mapped to its ``f=`` token."""

    HIGH = "fa_debteq_high"
    LOW = "fa_debteq_low"
    UNDER_1 = "fa_debteq_u1"
    UNDER_0_9 = "fa_debteq_u0.9"
    UNDER_0_8 = "fa_debteq_u0.8"
    UNDER_0_7 = "fa_debteq_u0.7"
    UNDER_0_6 = "fa_debteq_u0.6"
    UNDER_0_5 = "fa_debteq_u0.5"
    UNDER_0_4 = "fa_debteq_u0.4"
    UNDER_0_3 = "fa_debteq_u0.3"
    UNDER_0_2 = "fa_debteq_u0.2"
    UNDER_0_1 = "fa_debteq_u0.1"
    OVER_0_1 = "fa_debteq_o0.1"
    OVER_0_2 = "fa_debteq_o0.2"
    OVER_0_3 = "fa_debteq_o0.3"
    OVER_0_4 = "fa_debteq_o0.4"
    OVER_0_5 = "fa_debteq_o0.5"
    OVER_0_6 = "fa_debteq_o0.6"
    OVER_0_7 = "fa_debteq_o0.7"
    OVER_0_8 = "fa_debteq_o0.8"
    OVER_0_9 = "fa_debteq_o0.9"
    OVER_1 = "fa_debteq_o1"


class FilterGrossMargin(Enum):
    """Screener gross margin filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_grossmargin_pos"
    NEGATIVE = "fa_grossmargin_neg"
    HIGH = "fa_grossmargin_high"
    UNDER_NEG_100_PCT = "fa_grossmargin_u-100"
    UNDER_NEG_70_PCT = "fa_grossmargin_u-70"
    UNDER_NEG_50_PCT = "fa_grossmargin_u-50"
    UNDER_NEG_30_PCT = "fa_grossmargin_u-30"
    UNDER_NEG_20_PCT = "fa_grossmargin_u-20"
    UNDER_NEG_10_PCT = "fa_grossmargin_u-10"
    UNDER_0_PCT = "fa_grossmargin_u0"
    UNDER_5_PCT = "fa_grossmargin_u5"
    UNDER_10_PCT = "fa_grossmargin_u10"
    UNDER_15_PCT = "fa_grossmargin_u15"
    UNDER_20_PCT = "fa_grossmargin_u20"
    UNDER_25_PCT = "fa_grossmargin_u25"
    UNDER_30_PCT = "fa_grossmargin_u30"
    UNDER_35_PCT = "fa_grossmargin_u35"
    UNDER_40_PCT = "fa_grossmargin_u40"
    UNDER_45_PCT = "fa_grossmargin_u45"
    UNDER_50_PCT = "fa_grossmargin_u50"
    UNDER_60_PCT = "fa_grossmargin_u60"
    UNDER_70_PCT = "fa_grossmargin_u70"
    UNDER_80_PCT = "fa_grossmargin_u80"
    UNDER_90_PCT = "fa_grossmargin_u90"
    OVER_0_PCT = "fa_grossmargin_o0"
    OVER_5_PCT = "fa_grossmargin_o5"
    OVER_10_PCT = "fa_grossmargin_o10"
    OVER_15_PCT = "fa_grossmargin_o15"
    OVER_20_PCT = "fa_grossmargin_o20"
    OVER_25_PCT = "fa_grossmargin_o25"
    OVER_30_PCT = "fa_grossmargin_o30"
    OVER_35_PCT = "fa_grossmargin_o35"
    OVER_40_PCT = "fa_grossmargin_o40"
    OVER_45_PCT = "fa_grossmargin_o45"
    OVER_50_PCT = "fa_grossmargin_o50"
    OVER_60_PCT = "fa_grossmargin_o60"
    OVER_70_PCT = "fa_grossmargin_o70"
    OVER_80_PCT = "fa_grossmargin_o80"
    OVER_90_PCT = "fa_grossmargin_o90"


class FilterOperatingMargin(Enum):
    """Screener operating margin filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_opermargin_pos"
    NEGATIVE = "fa_opermargin_neg"
    HIGH = "fa_opermargin_high"
    VERY_NEGATIVE = "fa_opermargin_veryneg"
    UNDER_NEG_100_PCT = "fa_opermargin_u-100"
    UNDER_NEG_70_PCT = "fa_opermargin_u-70"
    UNDER_NEG_50_PCT = "fa_opermargin_u-50"
    UNDER_NEG_30_PCT = "fa_opermargin_u-30"
    UNDER_NEG_20_PCT = "fa_opermargin_u-20"
    UNDER_NEG_10_PCT = "fa_opermargin_u-10"
    UNDER_0_PCT = "fa_opermargin_u0"
    UNDER_5_PCT = "fa_opermargin_u5"
    UNDER_10_PCT = "fa_opermargin_u10"
    UNDER_15_PCT = "fa_opermargin_u15"
    UNDER_20_PCT = "fa_opermargin_u20"
    UNDER_25_PCT = "fa_opermargin_u25"
    UNDER_30_PCT = "fa_opermargin_u30"
    UNDER_35_PCT = "fa_opermargin_u35"
    UNDER_40_PCT = "fa_opermargin_u40"
    UNDER_45_PCT = "fa_opermargin_u45"
    UNDER_50_PCT = "fa_opermargin_u50"
    UNDER_60_PCT = "fa_opermargin_u60"
    UNDER_70_PCT = "fa_opermargin_u70"
    UNDER_80_PCT = "fa_opermargin_u80"
    UNDER_90_PCT = "fa_opermargin_u90"
    OVER_0_PCT = "fa_opermargin_o0"
    OVER_5_PCT = "fa_opermargin_o5"
    OVER_10_PCT = "fa_opermargin_o10"
    OVER_15_PCT = "fa_opermargin_o15"
    OVER_20_PCT = "fa_opermargin_o20"
    OVER_25_PCT = "fa_opermargin_o25"
    OVER_30_PCT = "fa_opermargin_o30"
    OVER_35_PCT = "fa_opermargin_o35"
    OVER_40_PCT = "fa_opermargin_o40"
    OVER_45_PCT = "fa_opermargin_o45"
    OVER_50_PCT = "fa_opermargin_o50"
    OVER_60_PCT = "fa_opermargin_o60"
    OVER_70_PCT = "fa_opermargin_o70"
    OVER_80_PCT = "fa_opermargin_o80"
    OVER_90_PCT = "fa_opermargin_o90"


class FilterNetMargin(Enum):
    """Screener net profit margin filter, mapped to its ``f=`` token."""

    POSITIVE = "fa_netmargin_pos"
    NEGATIVE = "fa_netmargin_neg"
    HIGH = "fa_netmargin_high"
    VERY_NEGATIVE = "fa_netmargin_veryneg"
    UNDER_NEG_100_PCT = "fa_netmargin_u-100"
    UNDER_NEG_70_PCT = "fa_netmargin_u-70"
    UNDER_NEG_50_PCT = "fa_netmargin_u-50"
    UNDER_NEG_30_PCT = "fa_netmargin_u-30"
    UNDER_NEG_20_PCT = "fa_netmargin_u-20"
    UNDER_NEG_10_PCT = "fa_netmargin_u-10"
    UNDER_0_PCT = "fa_netmargin_u0"
    UNDER_5_PCT = "fa_netmargin_u5"
    UNDER_10_PCT = "fa_netmargin_u10"
    UNDER_15_PCT = "fa_netmargin_u15"
    UNDER_20_PCT = "fa_netmargin_u20"
    UNDER_25_PCT = "fa_netmargin_u25"
    UNDER_30_PCT = "fa_netmargin_u30"
    UNDER_35_PCT = "fa_netmargin_u35"
    UNDER_40_PCT = "fa_netmargin_u40"
    UNDER_45_PCT = "fa_netmargin_u45"
    UNDER_50_PCT = "fa_netmargin_u50"
    UNDER_60_PCT = "fa_netmargin_u60"
    UNDER_70_PCT = "fa_netmargin_u70"
    UNDER_80_PCT = "fa_netmargin_u80"
    UNDER_90_PCT = "fa_netmargin_u90"
    OVER_0_PCT = "fa_netmargin_o0"
    OVER_5_PCT = "fa_netmargin_o5"
    OVER_10_PCT = "fa_netmargin_o10"
    OVER_15_PCT = "fa_netmargin_o15"
    OVER_20_PCT = "fa_netmargin_o20"
    OVER_25_PCT = "fa_netmargin_o25"
    OVER_30_PCT = "fa_netmargin_o30"
    OVER_35_PCT = "fa_netmargin_o35"
    OVER_40_PCT = "fa_netmargin_o40"
    OVER_45_PCT = "fa_netmargin_o45"
    OVER_50_PCT = "fa_netmargin_o50"
    OVER_60_PCT = "fa_netmargin_o60"
    OVER_70_PCT = "fa_netmargin_o70"
    OVER_80_PCT = "fa_netmargin_o80"
    OVER_90_PCT = "fa_netmargin_o90"


class FilterInsiderOwnership(Enum):
    """Screener insider ownership filter, mapped to its ``f=`` token."""

    LOW = "sh_insiderown_low"
    HIGH = "sh_insiderown_high"
    VERY_HIGH = "sh_insiderown_veryhigh"
    OVER_10_PCT = "sh_insiderown_o10"
    OVER_20_PCT = "sh_insiderown_o20"
    OVER_30_PCT = "sh_insiderown_o30"
    OVER_40_PCT = "sh_insiderown_o40"
    OVER_50_PCT = "sh_insiderown_o50"
    OVER_60_PCT = "sh_insiderown_o60"
    OVER_70_PCT = "sh_insiderown_o70"
    OVER_80_PCT = "sh_insiderown_o80"
    OVER_90_PCT = "sh_insiderown_o90"


class FilterInsiderTransactions(Enum):
    """Screener insider transactions filter, mapped to its ``f=`` token."""

    VERY_NEGATIVE = "sh_insidertrans_veryneg"
    NEGATIVE = "sh_insidertrans_neg"
    POSITIVE = "sh_insidertrans_pos"
    VERY_POSITIVE = "sh_insidertrans_verypos"
    UNDER_NEG_5_PCT = "sh_insidertrans_u-5"
    UNDER_NEG_10_PCT = "sh_insidertrans_u-10"
    UNDER_NEG_15_PCT = "sh_insidertrans_u-15"
    UNDER_NEG_20_PCT = "sh_insidertrans_u-20"
    UNDER_NEG_25_PCT = "sh_insidertrans_u-25"
    UNDER_NEG_30_PCT = "sh_insidertrans_u-30"
    UNDER_NEG_35_PCT = "sh_insidertrans_u-35"
    UNDER_NEG_40_PCT = "sh_insidertrans_u-40"
    UNDER_NEG_45_PCT = "sh_insidertrans_u-45"
    UNDER_NEG_50_PCT = "sh_insidertrans_u-50"
    UNDER_NEG_60_PCT = "sh_insidertrans_u-60"
    UNDER_NEG_70_PCT = "sh_insidertrans_u-70"
    UNDER_NEG_80_PCT = "sh_insidertrans_u-80"
    UNDER_NEG_90_PCT = "sh_insidertrans_u-90"
    OVER_5_PCT = "sh_insidertrans_o5"
    OVER_10_PCT = "sh_insidertrans_o10"
    OVER_15_PCT = "sh_insidertrans_o15"
    OVER_20_PCT = "sh_insidertrans_o20"
    OVER_25_PCT = "sh_insidertrans_o25"
    OVER_30_PCT = "sh_insidertrans_o30"
    OVER_35_PCT = "sh_insidertrans_o35"
    OVER_40_PCT = "sh_insidertrans_o40"
    OVER_45_PCT = "sh_insidertrans_o45"
    OVER_50_PCT = "sh_insidertrans_o50"
    OVER_60_PCT = "sh_insidertrans_o60"
    OVER_70_PCT = "sh_insidertrans_o70"
    OVER_80_PCT = "sh_insidertrans_o80"
    OVER_90_PCT = "sh_insidertrans_o90"


class FilterInstitutionalOwnership(Enum):
    """Screener institutional ownership filter, mapped to its ``f=`` token."""

    LOW = "sh_instown_low"
    HIGH = "sh_instown_high"
    UNDER_10_PCT = "sh_instown_u10"
    UNDER_20_PCT = "sh_instown_u20"
    UNDER_30_PCT = "sh_instown_u30"
    UNDER_40_PCT = "sh_instown_u40"
    UNDER_50_PCT = "sh_instown_u50"
    UNDER_60_PCT = "sh_instown_u60"
    UNDER_70_PCT = "sh_instown_u70"
    UNDER_80_PCT = "sh_instown_u80"
    UNDER_90_PCT = "sh_instown_u90"
    OVER_10_PCT = "sh_instown_o10"
    OVER_20_PCT = "sh_instown_o20"
    OVER_30_PCT = "sh_instown_o30"
    OVER_40_PCT = "sh_instown_o40"
    OVER_50_PCT = "sh_instown_o50"
    OVER_60_PCT = "sh_instown_o60"
    OVER_70_PCT = "sh_instown_o70"
    OVER_80_PCT = "sh_instown_o80"
    OVER_90_PCT = "sh_instown_o90"


class FilterInstitutionalTransactions(Enum):
    """Screener institutional transactions filter, mapped to its ``f=`` token."""

    VERY_NEGATIVE = "sh_insttrans_veryneg"
    NEGATIVE = "sh_insttrans_neg"
    POSITIVE = "sh_insttrans_pos"
    VERY_POSITIVE = "sh_insttrans_verypos"
    UNDER_NEG_5_PCT = "sh_insttrans_u-5"
    UNDER_NEG_10_PCT = "sh_insttrans_u-10"
    UNDER_NEG_15_PCT = "sh_insttrans_u-15"
    UNDER_NEG_20_PCT = "sh_insttrans_u-20"
    UNDER_NEG_25_PCT = "sh_insttrans_u-25"
    UNDER_NEG_30_PCT = "sh_insttrans_u-30"
    UNDER_NEG_35_PCT = "sh_insttrans_u-35"
    UNDER_NEG_40_PCT = "sh_insttrans_u-40"
    UNDER_NEG_45_PCT = "sh_insttrans_u-45"
    UNDER_NEG_50_PCT = "sh_insttrans_u-50"
    OVER_5_PCT = "sh_insttrans_o5"
    OVER_10_PCT = "sh_insttrans_o10"
    OVER_15_PCT = "sh_insttrans_o15"
    OVER_20_PCT = "sh_insttrans_o20"
    OVER_25_PCT = "sh_insttrans_o25"
    OVER_30_PCT = "sh_insttrans_o30"
    OVER_35_PCT = "sh_insttrans_o35"
    OVER_40_PCT = "sh_insttrans_o40"
    OVER_45_PCT = "sh_insttrans_o45"
    OVER_50_PCT = "sh_insttrans_o50"


class FilterFloatShort(Enum):
    """Screener float-short percentage filter, mapped to its ``f=`` token."""

    LOW = "sh_short_low"
    HIGH = "sh_short_high"
    UNDER_5_PCT = "sh_short_u5"
    UNDER_10_PCT = "sh_short_u10"
    UNDER_15_PCT = "sh_short_u15"
    UNDER_20_PCT = "sh_short_u20"
    UNDER_25_PCT = "sh_short_u25"
    UNDER_30_PCT = "sh_short_u30"
    OVER_5_PCT = "sh_short_o5"
    OVER_10_PCT = "sh_short_o10"
    OVER_15_PCT = "sh_short_o15"
    OVER_20_PCT = "sh_short_o20"
    OVER_25_PCT = "sh_short_o25"
    OVER_30_PCT = "sh_short_o30"

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
    FilterPE,
    FilterForwardPE,
    FilterPEG,
    FilterPS,
    FilterPB,
    FilterPC,
    FilterPFCF,
    FilterEPSGrowthThisYear,
    FilterEPSGrowthNextYear,
    FilterEPSGrowthPast5Y,
    FilterEPSGrowthNext5Y,
    FilterSalesGrowthPast5Y,
    FilterEPSGrowthTTM,
    FilterEPSGrowthQoQ,
    FilterSalesGrowthQoQ,
    FilterEarningsRevenueSurprise,
    FilterDividendYield,
    FilterPayoutRatio,
    FilterReturnOnAssets,
    FilterReturnOnEquity,
    FilterReturnOnInvestment,
    FilterCurrentRatio,
    FilterQuickRatio,
    FilterLTDebtEquity,
    FilterDebtEquity,
    FilterGrossMargin,
    FilterOperatingMargin,
    FilterNetMargin,
    FilterInsiderOwnership,
    FilterInsiderTransactions,
    FilterInstitutionalOwnership,
    FilterInstitutionalTransactions,
    FilterFloatShort,
]
