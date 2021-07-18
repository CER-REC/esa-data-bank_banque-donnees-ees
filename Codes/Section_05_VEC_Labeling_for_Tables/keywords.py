import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *

Physical_and_Meteorological_Environment = """Physical and Meteorological Environment
Precipitation
Snowfall
Wind
rain
Mean temperatures
Slope
Geotechnical
Slumping
Subsidence
Weather
Erosion
Ice
Permafrost
Climate trend
climate
water erosion
wind erosion
acid-generating rock
temperature
physical
meteorological
landslides
mudflows
slumping
subsidence
seismicity
flooding
migrating watercourses
eroding banks
extreme weather events
peak flow regime
ice jams
acid rock
climate variability
ground conditions
thaw
till
earthquake
avalanche
sloping
topography
elevation
"""


Soil_and_Soil_Productivity = """Soil Productivity
Soil
Agriculture
Topsoil
Subsoil
Soil horizon
Drainage
Erosion
Contamination
CCME
Canadian Council of Ministers of the Environment
Soil compaction
Soil structure
Soil classification
Soil handling
Containment
reclamation
thickness of horizon
tilth
grubbing
soil quality
salinity
sediments
rocks
minerals
sand
chernozem
DVG
Dunvargan
calcareous
CRW
sand
sandy
Glaciofluvial
boulders
gravel
silt
clay
stone
stoniness"""


# Diversity
# Abundance
# Ecological
# Inventory
# Community
# communities

# ecological community



Vegetation = """Vegetation
Plant
planting
Rare plant
Boreal
Grassland
Prairie
Forest
forested
Clearing
plant community
orchid
orchard
Weeds
Invasive species
invasive plants
Seed mix
Herbicide
Tree
leaf
branch
Growth
Old growth
Biodiversity
forestry
clubroot
wood
spruce
fir
birch
pine
aspen
tamarack
willow
beech
maple
black walnut
hickory
oak
redcedar
hemlock
Douglas-fir
genus
agricultural
root
seed
mulcher
mulch
bentgrass
sedge
carex
wood
moss
bulrush
oatgrass
mannagrass
flower
androgynum
Aulacomnium
undulatum
Atrichum
wheatgrass
parviflora
luzula
crawfordii
Achnatherum
needlegrass
eleocharis
reedgrass
calamagrostis
latifolia
Elymus
grain
wildrye
meadow
speargrass
shrub
chokecherry"""


Water_Quality_and_Quantity = """Water Quality and Quantity
Water
waterbody
water body
watercourse
evaporation
transpiration
Surface water
Ground water
Runoff
Contamination
contaminant
Water use
Hydrologic
hydrological
hydro
hydrostatic
salinity
blasting
Withdrawal
Flow
Peak
Basin
Inter-basin
Water Quality
Water quality testing
Water table
Containment
Sediment
sewer
waste
wastewater
biosolids
sludge
septage
groundwater
groundwater-related
aquifers
streamflow
acquatics
river
hydrometric
watershed
waterfall
sea
ocean
lake
pond
fjords
wadis
runs
reservoir
lagoon
bay
harbor
well
well-water
surface-water
surfacewater
hot spring
creek"""

Fish_and_Fish_Habitat = """Fish and Fish Habitat
Fish
fish-bearing
fisheries
Fisheries and Oceans Canada
DFO
Fisheries and Oceans
Local fisheries
Trout
Fisheries Act
Offsetting
Instream work
in-stream work
Restricted activity period
Fish-bearing water body
Riparian
Aquatic
Aquatic invasive species
Spawning
Fry
fingerling
alevin
chlorine
chlorinated
Sport fishery
Spawning deterrent
spawning period
Stream
River
In-stream
instream
Wetted width
substrate
whale
marine mammal
salmon
oncorhynchus
walleye
pike
crappie
redhorse
pumpkinseed fish
bowfin
bass
catfish
sunfish
bluegill
spotted gar
muskellunge
ruffe
yellow perch
shiner
sucker
whitefish
cisco
marine
clam
scallop
sea
ocean
lake
pond
bay"""

Wetlands = """Wetlands
Class (wetland class)
wetland
Bog
Fen
Marsh
Swamp
Shallow water
Intermittent
Permanent
Non-permanent
Wetland function
Offsetting
Hydrological function
Drainage area
Canadian wetland classification system
Federal policy on wetland conservation
Conservation
Wetland monitoring
Reclamation
Compensation
water recharge
potholes
ponds
peatbogs
mires"""

Wildlife_and_Wildlife_Habitat = """Wildlife and Wildlife Habitat
nocturnal
bat trees
hibernation
migratory birds
migratory bird sanctuary
MBCA
migratory birds convention act
Nesting
foraging
Restricted activity period
Mammal
Ungulate
Amphibian
Reptile
Breeding
Den
denning
Wintering
overwintering
Hibernaculum
hibernacula
Riparian habitat
Old growth habitat
Sensitive period
Sensory disturbance
Mortality
Mortality risk
Habitat alteration
Habitat loss
Habitat destruction
Range
Population
Distribution
Sanctuary
sanctuaries
Important Bird Area
Bat
caribou
bird
goose
amphibian
swans
frogs
toads
salamanders
newts
caecilians
furbearing
reptile
invertebrate
rattlesnake
snake
waterbird
bear
moose
bat
owl"""

Species_at_Risk = """Species at Risk
Species of Special Status
Rare
Sensitive
SARA
Species At Risk Act
COSEWIC
Committee on the Status of Endangered Wildlife in Canada
ECCC
Environment and Climate Change Canada
Critical habitat
Designation
Threshold
Schedule 1
At Risk
Endangered
Critical timing window
Restricted activity period
DFO
Fisheries and Oceans Canada
Canadian Wildlife Service
CWS
Recovery Strategy
Action Plan
Status
Listed
Permit
Offset
offsetting
Compensation
Caribou
Bat
special conservation status"""

Air_Emissions = """Air Emissions
Air
CAC
criteria air contaminant
Emissions
Ground-level
Receptor
Model
modelled
modelling
Construction equipment
Vehicle
vehicular emissions
CCME
Volatile organic compounds
Combustion
Leak
Fugitive emissions
Detection
Flaring
Incinerating
incineration
Smoke
Venting
Pollute
pollutant
National Pollutant Release Inventory
Exceedance
Permit
Release
Ambient
Air quality
Hydrogen sulphide
H2S
particulate
so2
mercaptans
dust"""

GHG_Emissions_and_Climate_Change = """GHG Emissions and Climate Change
greenhouse
greenhouse gas
green house gas
greenhouse gases
climate change
point source
area source
venting
fugitive
release
leak
burning
assumption
offset
carbon dioxide
CO2
CO2 equivalent
Target
Reduction
Percentage
Hinders
Net zero
net-zero
Reduce
Combustion emissions
International Standards Organization
ISO
methane
ghg
ozone
global warming"""

Assessment_of_Upstream_GHG_Emissions = """Assessment of Upstream GHG Emissions
upstream
quantitative
throughput
net zero
net-zero
Environment and Climate Change Canada (ECCC)
Venting
Threshold
CO2
Carbon dioxide
CO2 equivalent
Methane
emissions
steam
hydrogen
combustion
fugitive
venting
flaring"""

Acoustic_Environment = """Acoustic Environment
Sound
Noise
Receptor
Equipment
Frequency
Inaudible
Audible
Decibel
Notification
Noise control
Noise management
Model
modelling
Monitoring
monitor
db
acoustic"""


Environmental_Obligations = """Environmental Obligations
MBCA
migratory birds convention act
SARA
Species at risk act
DFO
Fisheries and Oceans Canada
Federal Wetland Policy
Hinder
Federal
Provincial
Territorial
International
Policy
Plan
Framework
Wildlife
Vegetation
Fish
Species at risk
Plant
law
legislation
regulations"""

Traditional_Land_and_Resource_Use = """Traditional Land and Resource Use
TLRU
traditional
Traditional ecological knowledge
Traditional Knowledge
Indigenous Knowledge
Aboriginal Knowledge
Aboriginal
Native
Indian
First Peoples
Treaty Lands
Indigenous Land
Traditional Territory
Oral Indigenous Knowledge
IK
OIK
TK
access to lands
access to resources
Hunt
hunting
fishing
Harvest
harvesting
Culturally significant
Culturally modified tree
Gather
Berries
Medicine
Berry picking
Indigenous
Elder
Knowledge Keeper
Trapping
trap
Ceremony
ceremonies
Medicinal
Cultural
Old growth
Spirit Bear
Spirit animal
spiritual
sacred area
sacred sites
metis
Métis
first nations
shxw’ōwhámel
lheidlit’enneh
whispering pines first nation
inuit
elders
kumik elder lodge
tribal
Abenaki
Innu
Montagnais-Naskapi
Oneida
Ahousaht
Interior Salish
Onondaga
Algonquin
Inuinnait
Copper Inuit
Pacheenaht
Assiniboine
Inuvialuit
Mackenzie Inuit
Petun
Atikamekw
Kainai
Piikani
Peigan
Baffin Island Inuit
K'asho Got'ine
Saldermiut Inuit
Beothuk
Kaska Dena
Sahtu Got'ine
Bearlake
Blackfoot Confederacy
Blackfoot
Kivallirmiut
Caribou Inuit
Secwepemc
Shuswap
Cayuga
Ktunaxa
Kootenay
Sekani
Central Coast Salish
Kwakwaka'wakw
Kwakiutl
Seneca
Coast Salish
Kyuquot and Checleseht
Shuta Got'ine
Cree
Labradormiut
Labrador Inuit
Siksika
Dakota
Lilwat
Lillooet
Slavey
Dakelh
Lingit
Tlingit
Stoney-Nakoda
Dane-zaa
Beaver
Syilx
Okanagan
Dene
Mi'kmaq
Tagish
Denesuline
Chipewyan
Mohawk
Tahltan
Ditidaht
Mowachaht-Muchalaht
Tla-o-qui-aht
Clayoquot
Ehattesaht
Nahani
Tlicho
Dogrib
Gitxsan
Gitksan
Netsilingmiut
Netsilik Inuit
Toquaht
Gwich'in
Neutral Confederacy
Tr'ondëk Hwëch'in (Han)
Haida
Nicola-Similkameen
Tseshaht
Sheshaht
Haisla
Kitamaat
Nisga'a
Tsilhqot'in
Chilcotin
Haudenosaunee
Six Nations
Iroquois
Nlaka'pamux
Thompson
Tsimshian
Heiltsuk
Northern Georgia Strait Coast Salish
Tsuut'ina
Sarcee
Hesquiaht
Nuchatlaht
Tutchone
Hupacasath
Opetchesaht
Nunavimmiut
Ungava Inuit
Uchucklesaht
Huu-ay-aht
Nuu-chah-nulth
Ucluelet
Huron-Wendat
Nuxalk
Bella Coola
Wolastoqiyik
Maliseet
Iglulingmuit
Iglulik Inuit
Odawa
Wetal
Tsetsaut
Inuit
Ojibwa
Yellowknives
popkum first nation
leq’á:mel first nation
alexander first nation
samson cree first nation
o’chiese first nation
ermineskin cree nation
enoch cree nation
indian
eskimo"""

Electromagnetism_and_Corona_Discharge = """Electromagnetism and Corona Discharge
voltage
ozone concentration
eletric
electricity
magnetic
magnetism
current
corona
discharge
magnetic
power line
powerline
electromagnetic
signals
maximum load
induction
frequency
inteference
radio
television
foul weather
ambient conditions
240 kV"""

Human_Occupancy_and_Resource_Use = """Human Occupancy and Resource Use
Human Occupancy and Resource Use
residents
human Occupancy
resource use
consultation
livestock
human
male
female
men
women
boy
girl
father
mother
parent
gender
rural
urban
residential
reserve
crops
orchards
orchid
vineyards
agriculture
recreation
park
scenic
parks canada
conservation area
international biological program
ecological reserves
preserves
industrial
commercial
agreement forests
timber sales area
controlled forest
managed forest
registered hunting
recognized hunting
trapping
guiding areas
commercial fishing
sport finishing
water reserves
water licenses
water supply
municipal
infrastructure
rail
navigable waterways
local
TLU Impact assessment"""

Heritage_Resources = """Heritage Resources
Heritage Resources
Heritage
Archaeology
Archeology
Archaeological
Archeological
Paleontology
Paleontological
Historic
Historic resource
Historic site
Hunting camp
Trail
Culturally significant
Dig site
Archaeologist
Archeologist
undiscovered
architectural
grave site
burial site
medicine wheel
culturally modified tree
CMT
archaeological report
archeological report
archaeological assessment
archeological assessment
pre-contact
post-contact
human remains
Permit
license
licence
clearance
Heritage Conservation Branch
Ontario ministry of tourism culture and sport
Heritage resources act
Alberta Ministry of Culture Multiculturalism and Status of Women
British Columbia Archeology Branch
Heritage conservation act
Historic sites and monuments act
Historic resources act
Heritage property act
Haida Gwaii Reconciliation act
Heritage Manitoba act
Onatario Heritage act
Loi sur les biens culturels
Heritage place protection act
Archeological sites protection act
richesse du patrimoine
permis de recherche archéologique
Heritage resources impact assessment
HRIA
Acheological impact assessment
AIA
Nunavut territorial lands use regulations
Northwest territories historical advisory Board
Yukon heritage resources Board"""

Navigation_and_Navigation_Safety = """Navigation and Navigation Safety
Navigation
Navigation protection activities
Guide lines
Guide wires
Signage
Waterway
Crossing
crossing plan
navigation
impacting Navigation
dewatering of navigable waters
navigable waters
navigable waterway
navigable
navigate
waterway
watercourse
watercourse crossing
water crossing
crossing
crossing methodology
horizontal directional drilling
HDD
bridge
temporary
permanent
marine
marine terminal
waterway user
recreational waterway user
navigational use
river
creek
tributary
tourism
tourist
guide outfitter
outfitter
angler
canoe
kayak
boat
sailing
sail
Fisheries and Oceans Canada
Navigation Protection Act
navigable watercourse
navigation Safety
scheduled waters
non-scheduled waters
recreation-related navigation
commercial-related navigation
watercourse users
waterway users
watercourse Crossing
crossing method
trenchless crossing
trenched crossing
navigation hazard
exposed instream
buoyancy issues
upstream
downstream
warning signs
warning Signage
instream
temporary vehicle crossing
bed
banks
preconstruction contours
hydraulic characteristics
erosion and sediment control
runoff
temporary crossing structure
fording
streambank
streambed
side containment"""

Social_and_Cultural_Well_Being = """Social and Cultural Well-Being
Social
Routing
socio-cultural
cultural
well-being
well being
families
workers
residents
community
traditions
alcohol
substance abuse
stresses
household cohesion
illegal
disruptive activities
privacy
inhabited
population
human behaviour
human behavior
workforce
peak workforce
mobile workforce
discipline measures
traffic control management
project schedule
Code of conduct policy
alcohol and drug policy
Indigenous service providers
regional service providers
social service 
cultural service
social agency
cultural agency
cultrual groups"""

Human_Health_and_Aesthetics = """Human Health and Aesthetics
toxic
human health
nuisances
health
Aesthetics
human receptors
CCME Guidelines
AER Directive 038
AUC Rule 012
release assessment
exposure assessment
dose-response
risk characterization
mental
Social
well-being
well being
stressors
emotional
public Safety
accidents
visual
obstruction of view
view points
angle of vision
quality of life
environmental changes
adverse human health effects
human receptors
air emissions
noise emissions
effluent discharge
CCME Guidelines
AER Directive 038
AUC Rule 012
risk assessment
ambient conditions
distance to edge of right-of-way
distance to edge of row
distance to schools
susceptible groups
elderly
children
recreationalists
Indigenous Women
visual impact assessment
visually absorb
landscape features 
view obstruction
Health canada
human health impact assessment
Canadian handbook on health impact assessment
health indicator data
statistics canada
mortality"""

Infrastructure_and_Services = """Infrastructure and Services
Infractructure
Services
Hospital
Urgent Care
ambulance
Fire services
Fire response
protective services
police services
Emergency response time
Emergency response
Hotel
Motel
RCMP
Royal Canadian Mounted police
medical response personnel
healthcare
social services
Local commercial accommodation
local accommodation
existing accommodation
worker accommodation
campground
Recreational Camp sites
recreational Resources
camp sites
Municipal waste
Municipal wateruse
Municipal water use
waste
contingency plan
traffic control
multi-passenger vehicles
restrict access
service providers
chemical waste
solid waste
liquid waste
landfills
industrial waste
non-hazardous waste
transfer stations
hazardous waste facilities
wastewater treatment facilities
recycling facilities
highways
roads
airports
911 dispatch services
Local commercial accommodation
Camp sites
Recreational Camp sites
railway
rail
roadway
road
highway
traffic
traffic flow
traffic usage levels
traffic patterns
pipeline
water main
water supply
sewage line
waste water
waste disposal
navigable waterway
powerline
power line
existing
pre-existing
preexisting
local services
regional services
services
accommodation
camping
facilities
recreation
recreational
ammenities
community services
essential services
emergency services
health care services
social services
police
fire
fire fighting
fire-fighting
firefighting
EMT
response time
healthcare
health care
hospital
housing
educational facilities
school
university
college
transportation
access
construction access
land access
right of way
right-of-way
ROW
temporary workspace
temporary work space
TWS
sewer
disposal
electricity
traffic usage
railways
availability of housing
local residents
heavy load vehicles
construction access permits
hotel
big box stores
town centre
property
motel"""

Employment_and_Economy = """Employment and Economy
Employment opportunities
Business opportunities
contracting opportunities
Project contracting
local contracting
subcontracting
Indigenous employment
Aboriginal employment
Aboriginal participation plan
Indigenous participation plan
Aboriginal businesses
Indigenous businesses
direct employment
prime contractor
local Business
local Economy
local economies
unemployment rate
employment rate
educational level
post-secondary
high school
certificate
diploma
degree
Economy
jobs
personnel
cotractors
workers
workforce
staff
labour force
labor force
economic well-being
procurement
tax revenue
taxes
revenue
Major industries
Primary industries
Key industrial sectors
tourism
mining
quarrying
oil and Gas
gas extraction
agriculture
forestry
fishing
hunting
construction
public administration
retail trade
temporary workforce
permanent workforce
permanent part-time Employment
permanent full-time Employment
temporary part-time Employment
temporary full-time Employment
employment
contracting
contract
procurement
ordering
training
training programs
education
opportunity
capacity
labor
labour
development plan
labour services
economic participation
project requirements
dollar value
contract value
worker
workforce
work force
revenue
tax levee
employment level
unemployment level
unemployment
education level
skill level
economic condition
direct revenue
indirect revenue
hardship
displacement
economic benefits plan
cooperation agreement
bid
qualification
partnership
collaboration
distribution
agreement
outreach
commitment
financial
community investment
investment
development
benefits
monitor
Indigenous monitoring"""

Rights_of_Indigenous_Peoples = """Rights of Indigenous Peoples
Indigenous and Treaty Rights
Aboriginal and Treaty Rights
Treaty Rights
Indigenous Rights
Aboriginal Rights
potential rights
established rights
asserted rights
protected rights
section 35 rights
Indian Act
Constitution Act, 1982
Constitution Act
section 35
s. 35
Constitution
constitutionally
Indigenous
Aboriginal
Native
Indian
Métis
Metis
Inuit
Inuk
Peoples
Communities
Nation
Band
Tribe
Settlement
Treaty
Treaty Lands
Crown Land
Indigenous Land
Traditional Land
territory
Traditional Territory
Indigenous Knowledge
Oral Indigenous Knowledge
Traditional Knowledge
IK
OIK
TK
Elder
knowledge keeper
knowledge holder
rights-bearing
engagement
Indigenous engagement
Aboriginal engagement
Crown
Crown Consultation
duty to consult
agent of the Crown
early engagement
CER Early Engagement Guide
Indigenous and Northern Affairs Canada
INAC
Crown-Indigenous Relations and Northern Affairs Canada
CIRNAC
Indigenous Services Canada
ISC
confidential
confidentiality
infringe
infringement
exercise rights
practice rights
values
customs
traditions
practices
access
access to lands
access to resources
travel ways
land availability
resource availability
Indigenous protcols
Indigenous laws
governancy system
Indigenous participation
Indigenous monitoring
Reconciliation
Truth and Reconciliation
TRC
Calls to Action
missing and murdered
MMIW
MMIWG
residential school
United Nations Declaration on the Rights of Indigenous Peoples
UNDRIP
Traditional Knowledge
Indigenous Knowledge
Aboriginal Knowledge
Aboriginal
Hunt
hunting
fishing
Harvest
harvesting
Culturally significant
Culturally modified tree
Gather
Berries
Medicine
Berry picking
Indigenous
Elder
Trapping
engagement
trap
Ceremony
ceremonies
Medicinal
Cultural
First Peoples
indian act
treaty
rights-bearing
indigenous rights
reserves
aboriginal
indigenous
metis
Métis
first nations
shxw’ōwhámel
lheidlit’enneh
whispering pines first nation
inuit
elders
kumik elder lodge
tribal
Abenaki
Innu
Montagnais-Naskapi
Oneida
Ahousaht
Interior Salish
Onondaga
Algonquin
Inuinnait
Copper Inuit
Pacheenaht
Assiniboine
Inuvialuit
Mackenzie Inuit
Petun
Atikamekw
Kainai
Piikani
Peigan
Baffin Island Inuit
K'asho Got'ine
Saldermiut Inuit
Beothuk
Kaska Dena
Sahtu Got'ine
Bearlake
Blackfoot Confederacy
Blackfoot
Kivallirmiut
Caribou Inuit
Secwepemc
Shuswap
Cayuga
Ktunaxa
Kootenay
Sekani
Central Coast Salish
Kwakwaka'wakw
Kwakiutl
Seneca
Coast Salish
Kyuquot and Checleseht
Shuta Got'ine
Cree
Labradormiut
Labrador Inuit
Siksika
Dakota
Lilwat
Lillooet
Slavey
Dakelh
Lingit
Tlingit
Stoney-Nakoda
Dane-zaa
Beaver
Syilx
Okanagan
Dene
Mi'kmaq
Tagish
Denesuline
Chipewyan
Mohawk
Tahltan
Ditidaht
Mowachaht-Muchalaht
Tla-o-qui-aht
Clayoquot
Ehattesaht
Nahani
Tlicho
Dogrib
Gitxsan
Gitksan
Netsilingmiut
Netsilik Inuit
Toquaht
Gwich'in
Neutral Confederacy
Tr'ondëk Hwëch'in (Han)
Haida
Nicola-Similkameen
Tseshaht
Sheshaht
Haisla
Kitamaat
Nisga'a
Tsilhqot'in
Chilcotin
Haudenosaunee
Six Nations
Iroquois
Nlaka'pamux
Thompson
Tsimshian
Heiltsuk
Northern Georgia Strait Coast Salish
Tsuut'ina
Sarcee
Hesquiaht
Nuchatlaht
Tutchone
Hupacasath
Opetchesaht
Nunavimmiut
Ungava Inuit
Uchucklesaht
Huu-ay-aht
Nuu-chah-nulth
Ucluelet
Huron-Wendat
Nuxalk
Bella Coola
Wolastoqiyik
Maliseet
Iglulingmuit
Iglulik Inuit
Odawa
Wetal
Tsetsaut
Inuit
Ojibwa
Yellowknives
popkum first nation
leq’á:mel first nation
alexander first nation
samson cree first nation
o’chiese first nation
ermineskin cree nation
enoch cree nation
indian
eskimo"""

keywords = [
    Physical_and_Meteorological_Environment,
    Soil_and_Soil_Productivity,
    Vegetation,
    Water_Quality_and_Quantity,
    Fish_and_Fish_Habitat,
    Wetlands,
    Wildlife_and_Wildlife_Habitat,
    Species_at_Risk,
    GHG_Emissions_and_Climate_Change,
    Assessment_of_Upstream_GHG_Emissions,
    Air_Emissions,
    Acoustic_Environment,
    Electromagnetism_and_Corona_Discharge,
    Human_Occupancy_and_Resource_Use,
    Heritage_Resources,
    Navigation_and_Navigation_Safety,
    Traditional_Land_and_Resource_Use,
    Social_and_Cultural_Well_Being,
    Human_Health_and_Aesthetics,
    Infrastructure_and_Services,
    Employment_and_Economy,
    Environmental_Obligations,
    Rights_of_Indigenous_Peoples,
]

keywords = [x.lower().split("\n") for x in keywords]

stemmer = PorterStemmer()

for i, label_keywords in enumerate(keywords):
    keywords[i] = [w for w in label_keywords if w not in stopwords.words("english")]
    keywords[i] = [stemmer.stem(w) for w in keywords[i]]

print(keywords[0])

with open("keywords.pkl", "wb") as f:
    pickle.dump(keywords, f)