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
elevation"""


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
bay
orca"""

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
mires
mangrove forest
carr
pocosin
floodplains
vernal pool
baygall"""

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
owl
beaver
moose
polar bear
bison
puffin
lynx
deer
wolf
reindeer
bear
cougar
goose
coyote
wolverine
raccoon
elk
crane
porcupine
fox
hare
loon
marmot
rabbit
bobcat
owl
rattlesnake
insect
bug
weasel
otter
skunk
mineral lick
minerallick"""

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

all_canadian_species_at_risk = """Taxidea taxus jacksoni

Taxidea taxus jeffersonii

Blaireau

Badger jeffersonii

Taxidea taxus jeffersonii

Bat

Perimyotis subflavus

Pipistrelle de l’Est

Caribou

Rangifer tarandus pearyi

Caribou de Peary

Rangifer tarandus caribou

Kangaroo Rat

Dipodomys ordii

Rat kangourou d’Ord

Marmot

Marmota vancouverensis

Mole

Scapanus townsendii

dychei

Reithrodontomys megalotis dychei

Myotis

Myotis lucifugus

Myotis septentrionalis

Seal 

Lacs des Loups Marins

Phoca vitulina mellonae

Shrew

Sorex bendirii

Musaraigne de Bendire

Beluga

Delphinapterus leucas

Blue Whale

Balaenoptera musculus

Killer Whale

Orcinus orca

Whale

Eubalaena glacialis

Eubalaena japonica

Hyperoodon ampullatus

Sei Whale

Balaenoptera borealis

Rorqual boréal population du Pacifique

Birds

Bobwhite

Colinus virginianus

auricollis
    
Icteria virens auricollis

virens

Icteria virens virens

Crane

Grus americana

Grue blanche

Curlew

Numenius borealis

Flycatcher

Empidonax virescens

Grebe

Podiceps auritus

Gull

Pagophila eburnea

Mouette blanche

rufa

Calidris canutus rufa

Lark

Eremophila alpestris strigata

Owl

Tyto alba

Owl

Athene cunicularia

caurina

Strix occidentalis caurina

Plover

Charadrius montanus

circumcinctus

Charadrius melodus circumcinctus

melodus

Charadrius melodus melodus

King Rail

Rallus elegans

urophasianus

Centrocercus urophasianus urophasianus

Sapsucker

Sphyrapicus thyroideus

Shearwater

Ardenna creatopus

Puffin

migrans

Lanius ludovicianus migrans

Coastal Vesper

Pooecetes gramineus affinis

Henslow

Ammodramus henslowii

Black Swift

Cypseloides niger

Roseate

Sterna dougallii

Sage Thrasher

Oreoscoptes montanus

Cerulean Warbler

Setophaga cerulea

warbler

kirtland

Dendroica kirtlandii

Prothonotary

Protonotaria citrea

Woodpecker

Melanerpes erythrocephalus

Picoides albolarvatus

Blanchard\'s Cricket

Acris blanchardi

Rainette grillon de Blanchard

Northern Leopard

Lithobates pipiens

Oregon Spotted

Rana pretiosa

Salamander

Allegheny Mountain Dusky

Desmognathus ochrophaeus

Allegheny Mountain Dusky

Desmognathus ochrophaeus

Eastern Tiger

Ambystoma tigrinum

Jefferson

Ambystoma jeffersonianum

Northern Dusky

Desmognathus fuscus

Small-mouthed

Ambystoma texanum

Western Tiger

Ambystoma mavortium

Fowler\'s Toad

Anaxyrus fowleri

Eastern Foxsnake

Pantherophis gloydi

Eastern Foxsnake

Pantherophis gloydi

Butler\'s Gartersnake

Thamnophis butleri

Greater Short-horned Lizard

Phrynosoma hernandesi

Massasauga

Sistrurus catenatus

Desert Nightsnake

Hypsiglena chlorophaea

Queensnake

Regina septemvittata

Blue Racer

Coluber constrictor foxii

Gray Ratsnake

Pantherophis spiloides

Leatherback Sea Turtle

Dermochelys coriacea

Sea Turtle

Loggerhead Sea Turtle

Caretta caretta

Five-Lined Skink

Plestiodon fasciatus

Sharp-tailed Snake

Contia tenuis

Spiny Softshell

Apalone spinifera

Blanding\'s Turtle

Emydoidea blandingii

Spotted Turtle

Clemmys guttata

Western Painted Turtle

Chrysemys picta bellii

Striped Bass

Morone saxatilis

Silver Chub

Macrhybopsis storeriana

Lake Chubsucker

Erimyzon sucetta

Shortnose Cisco

Coregonus reighardi

Spring Cisco

Coregonus sp.

Nooksack Dace

Rhinichthys cataractae ssp.

Redside Dace

Clinostomus elongatus

Speckled Dace

Rhinichthys osculus

Channel Darter

Percina copelandi

Channel Darter

Percina copelandi

Spotted Gar

Lepisosteus oculatus

Western Brook Lamprey

Lampetra richardsoni

Northern Madtom

Noturus stigmosus

Copper Redhorse

Moxostoma hubbsi

Atlantic Salmon

Salmo salar

Basking Shark

Cetorhinus maximus

White Shark

Carcharodon carcharias

Shiner, Carmine (Notropis percobromus)

Smelt, Rainbow (Osmerus mordax) Lake Utopia large-bodied population

Smelt, Rainbow (Osmerus mordax) Lake Utopia small-bodied population

Stickleback, Enos Lake Benthic Threespine (Gasterosteus aculeatus)

Stickleback, Enos Lake Limnetic Threespine (Gasterosteus aculeatus)

Stickleback, Misty Lake Lentic Threespine (Gasterosteus aculeatus)

Stickleback, Misty Lake Lotic Threespine (Gasterosteus aculeatus)

Stickleback, Paxton Lake Benthic Threespine (Gasterosteus aculeatus)

Stickleback, Paxton Lake Limnetic Threespine (Gasterosteus aculeatus)

Stickleback, Vananda Creek Benthic Threespine (Gasterosteus aculeatus)

Stickleback, Vananda Creek Limnetic Threespine (Gasterosteus aculeatus)

Sturgeon, White (Acipenser transmontanus) Nechako River population

Sturgeon, White (Acipenser transmontanus) Upper Columbia River population

Sturgeon, White (Acipenser transmontanus) Upper Fraser River population

Sturgeon, White (Acipenser transmontanus) Upper Kootenay River population

Trout, Rainbow (Oncorhynchus mykiss) Athabasca River populations

Whitefish, Atlantic (Coregonus huntsmani)

Abalone, Northern (Haliotis kamtschatkana)

Bean, Rayed (Villosa fabalis)

Fawnsfoot (Truncilla donaciformis)

Forestsnail, Broad-banded (Allogona profunda)

Forestsnail, Oregon (Allogona townsendiana)

Globelet, Proud (Patera pennsylvanica)

Hickorynut (Obovaria olivaria)

Hickorynut, Round (Obovaria subrotunda)

Kidneyshell (Ptychobranchus fasciolaris)

Lilliput (Toxolasma parvum)

Mussel, Salamander (Simpsonaias ambigua)

Physa, Hotwater (Physella wrighti)

Pigtoe, Round (Pleurobema sintoxia)

Riffleshell, Northern (Epioblasma torulosa rangiana)

Snail, Banff Springs (Physella johnsoni)

Snuffbox (Epioblasma triquetra)

Blue, Island (Plebejus saepiolus insulanus)

Borer, Aweme (Papaipema aweme)

Borer, Hoptree (Prays atomocella)

Buckmoth, Bogbean (Hemileuca sp.)

Bumble Bee, Gypsy Cuckoo (Bombus bohemicus)

Bumble Bee, Rusty-patched (Bombus affinis)

Checkerspot, Taylor’s (Euphydryas editha taylori)

Clubtail, Olive (Stylurus olivaceus)

Clubtail, Rapids (Gomphus quadricolor)

Clubtail, Riverine (Stylurus amnicola) Great Lakes Plains population

Clubtail, Skillet (Gomphus ventricosus)

Crawling Water Beetle, Hungerford’s (Brychius hungerfordi)

Cuckoo Bee, Macropis (Epeoloides pilosulus)

Diving Beetle, Bert’s Predaceous (Sanfilippodytes bertae)

Duskywing, Eastern Persius (Erynnis persius persius)

Efferia, Okanagan (Efferia okanagana)

Emerald, Hine’s (Somatochlora hineana)

Flower Moth, White (Schinia bimatris)

Gold-edged Gem (Schinia avemensis)

Hairstreak, Behr’s (Satyrium behrii)

Hairstreak, Half-moon (Satyrium semiluna)

Metalmark, Mormon (Apodemia mormo) Southern Mountain population

Moth, Dusky Dune (Copablepharon longipenne)

Moth, Edwards’ Beach (Anarta edwardsii)

Moth, Five-spotted Bogus Yucca (Prodoxus quinquepunctellus)

Moth, Non-pollinating Yucca (Tegeticula corruptrix)

Moth, Sand-verbena (Copablepharon fuscum)

Moth, Yucca (Tegeticula yuccasella)

Ringlet, Maritime (Coenonympha nipisiquit)

Skipper, Dakota (Hesperia dacotae)

Skipperling, Poweshiek (Oarisma poweshiek)

Skipper, Ottoe (Hesperia ottoe)

Sun Moth, False-foxglove (Pyrrhia aurantiago)

Tiger Beetle, Cobblestone (Cicindela marginipennis)

Tiger Beetle, Northern Barrens (Cicindela patruela)

Tiger Beetle, Wallis’ Dark Saltflat (Cicindela parowana wallisi)

Agalinis, Gattinger’s (Agalinis gattingeri)

Agalinis, Rough (Agalinis aspera)

Agalinis, Skinner’s (Agalinis skinneriana)

Ammannia, Scarlet (Ammannia robusta)

Aster, Short-rayed Alkali (Symphyotrichum frondosum)

Avens, Eastern Mountain (Geum peckii)

Balsamroot, Deltoid (Balsamorhiza deltoidea)

Beakrush, Tall (Rhynchospora macrostachya)

Birch, Cherry (Betula lenta)

Bluehearts (Buchnera americana)

Braya, Fernald’s (Braya fernaldii)

Braya, Hairy (Braya pilosa)

Braya, Long’s (Braya longii)

Bugbane, Tall (Actaea elata)

Bulrush, Bashful (Trichophorum planifolium)

Bush-clover, Slender (Lespedeza virginica)

Buttercup, California (Ranunculus californicus)

Buttercup, Water-plantain (Ranunculus alismifolius)

Butternut (Juglans cinerea)

Cactus, Eastern Prickly Pear (Opuntia humifusa)

Campion, Spalding’s (Silene spaldingii)

Catchfly, Coastal Scouler’s (Silene scouleri grandis)

Centaury, Muhlenberg’s (Centaurium muehlenbergii)

Chestnut, American (Castanea dentata)

Colicroot (Aletris farinosa)

Collomia, Slender (Collomia tenella)

Columbo, American (Frasera caroliniensis)

Coreopsis, Pink (Coreopsis rosea)

Dogwood, Eastern Flowering (Cornus florida)

Evening-primrose, Contorted-pod (Camissonia contorta)

Fern, Southern Maidenhair (Adiantum capillus-veneris)

Fringed-orchid, Eastern Prairie (Platanthera leucophaea)

Fringed-orchid, Western Prairie (Platanthera praeclara)

Gentian, Plymouth (Sabatia kennedyana)

Gentian, White Prairie (Gentiana alba)

Ginseng, American (Panax quinquefolius)

Goat’s-rue, Virginia (Tephrosia virginiana)

Goldenrod, Showy (Solidago speciosa) Great Lakes Plains population

Goldfields, Rayless (Lasthenia glaberrima)

Grass, Forked Three-awned (Aristida basiramea)

Ironweed, Fascicled (Vernonia fasciculata)

Lewisia, Tweedy’s (Lewisiopsis tweedyi)

Lipocarpha, Small-flowered (Lipocarpha micrantha)

Lotus, Seaside Birds-foot (Lotus formosissimus)

Lousewort, Furbish’s (Pedicularis furbishiae)

Lupine, Dense-flowered (Lupinus densiflorus)

Lupine, Prairie (Lupinus lepidus)

Lupine, Streambank (Lupinus rivularis)

Mallow, Virginia (Sida hermaphrodita)

White Meconella

Meconella oregana
Microseris, Coast (Microseris bigelovii)
Milkwort, Pink (Polygala incarnata)
Mountain-mint, Hoary (Pycnanthemum incanum)
Mulberry, Red (Morus rubra)
Orchid, Phantom (Cephalanthera austiniae)
Owl-clover, Bearded (Triphysaria versicolor)
Owl-clover, Grand Coulee (Orthocarpus barbatus)
Owl-clover, Rosy (Orthocarpus bracteosus)
Owl-clover, Victoria’s (Castilleja victoriae)
Paintbrush, Golden (Castilleja levisecta)
Phacelia, Branched (Phacelia ramosissima)
Pine, Whitebark (Pinus albicaulis)
Plantain, Heart-leaved (Plantago cordata)
Pogonia, Large Whorled (Isotria verticillata)
Pogonia, Nodding (Triphora trianthophora)
Pogonia, Small Whorled (Isotria medeoloides)
Pondweed, Ogden’s (Potamogeton ogdenii)
Popcornflower, Fragrant (Plagiobothrys figuratus)
Pussytoes, Stoloniferous (Antennaria flagellaris)
Quillwort, Engelmann’s (Isoetes engelmannii)
Rockcress, Quebec (Boechera quebecensis)
Rush, Kellogg’s (Juncus kelloggii)
Sand-verbena, Pink (Abronia umbellata)
Sand-verbena, Small-flowered (Tripterocalyx micranthus)
Sandwort, Dwarf (Minuartia pusilla)
Sedge, False Hop (Carex lupuliformis)
Sedge, Foothill (Carex tumulicola)
Sedge, Juniper (Carex juniperorum)
Silverpuffs, Lindley’s False (Uropappus lindleyi)
Spike-primrose, Brook (Epilobium torreyi)
Spike-primrose, Dense (Epilobium densiflorum)
Spike-rush, Bent (Eleocharis geniculata) Great Lakes Plains population
Spike-rush, Bent (Eleocharis geniculata) Southern Mountain population
Spike-rush, Horsetail (Eleocharis equisetoides)
Sundew, Thread-leaved (Drosera filiformis)
Tonella, Small-flowered (Tonella tenella)
Toothcup (Rotala ramosior) Southern Mountain population
Tree, Cucumber (Magnolia acuminata)
Trefoil, Bog Bird’s-foot (Lotus pinnatus)
Trillium, Drooping (Trillium flexipes)
Triteleia, Howell’s (Triteleia howellii)
Violet, Bird’s-foot (Viola pedata)
Violet praemorsa subspecies, Yellow Montane (Viola praemorsa ssp. praemorsa)
Willow, Barrens (Salix jejuna)
Wintergreen, Spotted (Chimaphila maculata)
Wood-poppy (Stylophorum diphyllum)
Woolly-heads, Tall (Psilocarphus elatior)
Woolly-heads, Dwarf (Psilocarphus brevissimus) Southern Mountain population
Lichens
Lichen, Batwing Vinyl (Leptogium platynum)
Lichen, Boreal Felt (Erioderma pedicellatum) Atlantic population
Lichen, Pale-bellied Frost (Physconia subpallida)
Lichen, Seaside Centipede (Heterodermia sitchensis)
Lichen, Vole Ears (Erioderma mollissimum)
Mosses
Cord-moss, Rusty (Entosthodon rubiginosus)
Moss, Acuteleaf Small Limestone (Seligeria acutifolia)
Moss, Margined Streamside (Scouleria marginata)
Moss, Nugget (Microbryum vlassovii)
Moss, Poor Pocket (Fissidens pauperculus)
Moss, Rigid Apple (Bartramia stricta)
Moss, Roell’s Brotherella (Brotherella roellii)
Moss, Silver Hair (Fabronia pusilla)
PART 3
Threatened Species
Mammals
Bat, Pallid (Antrozous pallidus)
Bison, Wood (Bison bison athabascae)
Caribou, Woodland (Rangifer tarandus caribou) Boreal population
Caribou, Woodland (Rangifer tarandus caribou) Southern Mountain population
Ermine haidarum subspecies (Mustela erminea haidarum)
Fox, Grey (Urocyon cinereoargenteus)
Fox, Swift (Vulpes velox)
Marten, American (Martes americana atrata) Newfoundland population
Prairie Dog, Black-tailed (Cynomys ludovicianus)
Whale, Beluga (Delphinapterus leucas) Cumberland Sound population
Whale, Fin (Balaenoptera physalus) Pacific population
Whale, Killer (Orcinus orca) Northeast Pacific northern resident population
Whale, Killer (Orcinus orca) Northeast Pacific offshore population
Whale, Killer (Orcinus orca) Northeast Pacific transient population
Birds
Albatross, Short-tailed (Phoebastria albatrus)
Bittern, Least (Ixobrychus exilis)
Bobolink (Dolichonyx oryzivorus)
Bunting, Lark (Calamospiza melanocorys)
Crossbill percna subspecies, Red (Loxia curvirostra percna)
Flycatcher, Olive-sided (Contopus cooperi)
Goshawk laingi subspecies, Northern (Accipiter gentilis laingi)
Gull, Ross’s (Rhodostethia rosea)
Hawk, Ferruginous (Buteo regalis)
Knot roselaari type, Red (Calidris canutus roselaari type)
Longspur, Chestnut-collared (Calcarius ornatus)
Longspur, McCown’s (Rhynchophanes mccownii)
Meadowlark, Eastern (Sturnella magna)
Murrelet, Marbled (Brachyramphus marmoratus)
Nighthawk, Common (Chordeiles minor)
Owl, Barn (Tyto alba) Western population
Owl brooksi subspecies, Northern Saw-whet (Aegolius acadicus brooksi)
Pipit, Sprague’s (Anthus spragueii)
Screech-owl kennicottii subspecies, Western (Megascops kennicottii kennicottii)
Screech-owl macfarlanei subspecies, Western (Megascops kennicottii macfarlanei)
Shrike excubitorides subspecies, Loggerhead (Lanius ludovicianus excubitorides)
Swallow, Bank (Riparia riparia)
Swallow, Barn (Hirundo rustica)
Swift, Chimney (Chaetura pelagica)
Thrush, Bicknell’s (Catharus bicknelli)
Thrush, Wood (Hylocichla mustelina)
Warbler, Canada (Wilsonia canadensis)
Warbler, Golden-winged (Vermivora chrysoptera)
Waterthrush, Louisiana (Parkesia motacilla)
Whip-poor-will (Caprimulgus vociferus)
Woodpecker, Lewis’s (Melanerpes lewis)
Amphibians
Frog, Rocky Mountain Tailed (Ascaphus montanus)
Frog, Western Chorus (Pseudacris triseriata) Great Lakes / St. Lawrence – Canadian Shield population
Salamander, Coastal Giant (Dicamptodon tenebrosus)
Salamander, Spring (Gyrinophilus porphyriticus) Adirondack / Appalachian population
Spadefoot, Great Basin (Spea intermontana)
Reptiles
Gophersnake, Great Basin (Pituophis catenifer deserticola)
Massasauga (Sistrurus catenatus) Great Lakes/St. Lawrence population
Racer, Eastern Yellow-bellied (Coluber constrictor flaviventris)
Ratsnake, Gray (Pantherophis spiloides) Great Lakes/St. Lawrence population
Rattlesnake, Western (Crotalus oreganos)
Ribbonsnake, Eastern (Thamnophis sauritus) Atlantic population
Snake, Eastern Hog-nosed (Heterodon platirhinos)
Turtle, Blanding’s (Emydoidea blandingii) Great Lakes / St. Lawrence population
Turtle, Wood (Glyptemys insculpta)
Fish
Darter, Eastern Sand (Ammocrypta pellucida) Ontario populations
Darter, Eastern Sand (Ammocrypta pellucida) Quebec populations
Lamprey, Vancouver (Entosphenus macrostomus)
Minnow, Plains (Hybognathus placitus)
Minnow, Pugnose (Opsopoeodus emiliae)
Minnow, Western Silvery (Hybognathus argyritis)
Redhorse, Black (Moxostoma duquesnei)
Sculpin, Coastrange (Cottus aleuticus) Cultus population
Sculpin, Rocky Mountain (Cottus sp.) Eastslope populations
Shiner, Pugnose (Notropis anogenus)
Shiner, Silver (Notropis photogenis)
Spotted Wolffish (Anarhichas minor)
Sucker, Mountain (Catostomus platyrhynchus) Milk River populations
Sucker, Salish (Catostomus sp. cf. catostomus)
Trout, Bull (Salvelinus confluentus) Saskatchewan – Nelson Rivers populations
Trout, Westslope Cutthroat (Oncorhynchus clarkii lewisi) Alberta population
Wolffish, Northern (Anarhichas denticulatus)
Molluscs
Atlantic Mud-piddock (Barnea truncata)
Jumping-slug, Dromedary (Hemphillia dromedarius)
Mapleleaf (Quadrula quadrula) Saskatchewan – Nelson Rivers population
Taildropper, Blue-grey (Prophysaon coeruleum)
Wartyback, Threehorn (Obliquaria reflexa)
Arthropods
Flower Moth, Verna’s (Schinia verna)
Skipper, Dun (Euphyes vestris) Western population
Sweat Bee, Sable Island (Lasioglossum sablense)
Tiger Beetle, Audouin’s Night-stalking (Omus audouini)
Tiger Beetle, Gibson’s Big Sand (Cicindela formosa gibsoni)
Plants
Arnica, Griscom’s (Arnica griscomii ssp. griscomii)
Aster, Anticosti (Symphyotrichum anticostense)
Aster, Gulf of St. Lawrence (Symphyotrichum laurentianum)
Aster, Western Silvery (Symphyotrichum sericeum)
Aster, White Wood (Eurybia divaricata)
Aster, Willowleaf (Symphyotrichum praealtum)
Baccharis, Eastern (Baccharis halimifolia)
Bartonia, Branched (Bartonia paniculata ssp. paniculata)
Blazing Star, Dense (Liatris spicata)
Coffee-tree, Kentucky (Gymnocladus dioicus)
Cryptantha, Tiny (Cryptantha minima)
Daisy, Lakeside (Hymenoxys herbacea)
Deerberry (Vaccinium stamineum)
Desert-parsley, Gray’s (Lomatium grayi)
Fern, Lemmon’s Holly (Polystichum lemmonii)
Fern, Mountain Holly (Polystichum scopulinum)
Gentian, Victorin’s (Gentianopsis virgata ssp. victorinii)
Goldenrod, Showy (Solidago speciosa) Boreal population
Goldenseal (Hydrastis canadensis)
Goosefoot, Smooth (Chenopodium subglabrum)
Greenbrier, Round-leaved (Smilax rotundifolia) Great Lakes Plains population
Hackberry, Dwarf (Celtis tenuifolia)
Hyacinth, Wild (Camassia scilloides)
Jacob’s-ladder, Van Brunt’s (Polemonium vanbruntiae)
Lady’s-slipper, Small White (Cypripedium candidum)
Locoweed, Hare-footed (Oxytropis lagopus)
Meadowfoam, Macoun’s (Limnanthes macounii)
Mosquito-fern, Mexican (Azolla mexicana)
Mouse-ear-cress, Slender (Halimolobos virgata)
Paintbrush, Cliff (Castilleja rupicola)
Pepperbush, Sweet (Clethra alnifolia)
Phlox, Showy (Phlox speciosa ssp. occidentalis)
Popcornflower, Slender (Plagiobothrys tenellus)
Quillwort, Bolander’s (Isoetes bolanderi)
Rue-anemone, False (Enemion biternatum)
Sanicle, Bear’s-foot (Sanicula arctopoides)
Sanicle, Purple (Sanicula bipinnatifida)
Soapweed (Yucca glauca)
Spiderwort, Western (Tradescantia occidentalis)
Thistle, Hill’s (Cirsium hillii)
Toothcup (Rotala ramosior) Great Lakes Plains population
Twayblade, Purple (Liparis liliifolia)
Water-willow, American (Justicia americana)
Willow, Green-scaled (Salix chlorolepis)
Woodsia, Blunt-lobed (Woodsia obtusa)
Lichens
Bone, Seaside (Hypogymnia heterophylla)
Lichen, Black-foam (Anzia colpodes)
Lichen, Crumpled Tarpaper (Collema coniophilum)
Lichen, Wrinkled Shingle (Pannaria lurida)
Waterfan, Eastern (Peltigera hydrothyria)
Mosses
Bryum, Porsild’s (Mielichhoferia macrocarpa)
Moss, Alkaline Wing-nerved (Pterygoneurum kozlovii)
Moss, Haller’s Apple (Bartramia halleriana)
Moss, Spoon-leaved (Bryoandersonia illecebra)
PART 4
Special Concern
Mammals
Badger taxus subspecies, American (Taxidea taxus taxus)
Bat, Spotted (Euderma maculatum)
Bear, Grizzly (Ursus arctos) Western population
Bear, Polar (Ursus maritimus)
Beaver, Mountain (Aplodontia rufa)
Caribou, Barren-ground (Rangifer tarandus groenlandicus) Dolphin and Union population
Caribou, Woodland (Rangifer tarandus caribou) Northern Mountain population
Cottontail nuttallii subspecies, Nuttall’s (Sylvilagus nuttallii nuttallii)
Mole, Eastern (Scalopus aquaticus)
Mouse megalotis subspecies, Western Harvest (Reithrodontomys megalotis megalotis)
Otter, Sea (Enhydra lutris)
Pika, Collared (Ochotona collaris)
Porpoise, Harbour (Phocoena phocoena) Pacific Ocean population
Sea Lion, Steller (Eumetopias jubatus)
Vole, Woodland (Microtus pinetorum)
Whale, Bowhead (Balaena mysticetus) Bering-Chukchi-Beaufort population
Whale, Fin (Balaenoptera physalus) Atlantic population
Whale, Grey (Eschrichtius robustus) Eastern North Pacific population
Whale, Humpback (Megaptera novaeangliae) North Pacific population
Whale, Sowerby’s Beaked (Mesoplodon bidens)
Wolf, Eastern (Canis lupus lycaon)
Wolverine (Gulo gulo)
Birds
Albatross, Black-footed (Phoebastria nigripes)
Auklet, Cassin’s (Ptychoramphus aleuticus)
Blackbird, Rusty (Euphagus carolinus)
Curlew, Long-billed (Numenius americanus)
Duck, Harlequin (Histrionicus histrionicus) Eastern population
Falcon anatum/tundrius, Peregrine (Falco peregrinus anatum/tundrius)
Falcon pealei subspecies, Peregrine (Falco peregrinus pealei)
Goldeneye, Barrow’s (Bucephala islandica) Eastern population
Grebe, Horned (Podiceps auritus) Western population
Grebe, Western (Aechmophorus occidentalis)
Grosbeak, Evening (Coccothraustes vespertinus)
Heron fannini subspecies, Great Blue (Ardea herodias fannini)
Knot islandica subspecies, Red (Calidris canutus islandica)
Murrelet, Ancient (Synthliboramphus antiquus)
Owl, Flammulated (Otus flammeolus)
Owl, Short-eared (Asio flammeus)
Phalarope, Red-necked (Phalaropus lobatus)
Pigeon, Band-tailed (Patagioenas fasciata)
Rail, Yellow (Coturnicops noveboracensis)
Sandpiper, Buff-breasted (Tryngites subruficollis)
Sparrow, Baird’s (Ammodramus bairdii)
Sparrow pratensis subspecies, Grasshopper (Ammodramus savannarum pratensis)
Sparrow princeps subspecies, Savannah (Passerculus sandwichensis princeps)
Wood-pewee, Eastern (Contopus virens)
Amphibians
Frog, Coastal Tailed (Ascaphus truei)
Frog, Northern Leopard (Lithobates pipiens) Western Boreal/Prairie populations
Frog, Red-legged (Rana aurora)
Salamander, Coeur d’Alene (Plethodon idahoensis)
Salamander, Wandering (Aneides vagrans)
Salamander, Western Tiger (Ambystoma mavortium) Prairie/Boreal population
Toad, Great Plains (Anaxyrus cognatus)
Toad, Western (Anaxyrus boreas) Calling population
Toad, Western (Anaxyrus boreas) Non-calling population
Reptiles
Boa, Rubber (Charina bottae)
Milksnake (Lampropeltis triangulum)
Racer, Western Yellow-bellied (Coluber constrictor mormon)
Rattlesnake, Prairie (Crotalus viridis)
Ribbonsnake, Eastern (Thamnophis sauritus) Great Lakes population
Skink, Five-lined (Plestiodon fasciatus) Great Lakes/St. Lawrence population
Skink, Prairie (Plestiodon septentrionalis)
Skink, Western (Plestiodon skiltonianus)
Turtle, Eastern Musk (Sternotherus odoratus)
Turtle, Eastern Painted (Chrysemys picta picta)
Turtle, Midland Painted (Chrysemys picta marginata)
Turtle, Northern Map (Graptemys geographica)
Turtle, Snapping (Chelydra serpentina)
Turtle, Western Painted (Chrysemys picta bellii) Intermountain - Rocky Mountain population
Watersnake, Lake Erie (Nerodia sipedon insularum)
Fish
Buffalo, Bigmouth (Ictiobus cyprinellus) Saskatchewan – Nelson River populations
Darter, Channel (Percina copelandi) St. Lawrence populations
Dolly Varden (Salvelinus malma malma) Western Arctic populations
Killifish, Banded (Fundulus diaphanus) Newfoundland populations
Kiyi, Upper Great Lakes (Coregonus kiyi kiyi)
Lamprey, Northern Brook (Ichthyomyzon fossor) Great Lakes – Upper St. Lawrence populations
Lamprey, Silver (Ichthyomyzon unicuspis) Great Lakes – Upper St. Lawrence populations
Minnow, Cutlip (Exoglossum maxillingua)
Pickerel, Grass (Esox americanus vermiculatus)
Redhorse, River (Moxostoma carinatum)
Rockfish type I, Rougheye (Sebastes sp. type I)
Rockfish type II, Rougheye (Sebastes sp. type II)
Rockfish, Yelloweye (Sebastes ruberrimus) Pacific Ocean inside waters population
Rockfish, Yelloweye (Sebastes ruberrimus) Pacific Ocean outside waters population
Sculpin, Columbia (Cottus hubbsi)
Sculpin, Deepwater (Myoxocephalus thompsonii) Great Lakes - Western St. Lawrence populations
Sculpin, Rocky Mountain (Cottus sp.) Westslope populations
Sculpin, Shorthead (Cottus confusus)
Shark, Bluntnose Sixgill (Hexanchus griseus)
Shiner, Bridle (Notropis bifrenatus)
Stickleback, Giant Threespine (Gasterosteus aculeatus)
Stickleback, Unarmoured Threespine (Gasterosteus aculeatus)
Sturgeon, Green (Acipenser medirostris)
Sturgeon, Lake (Acipenser fulvescens) Southern Hudson Bay – James Bay populations
Sturgeon, Shortnose (Acipenser brevirostrum)
Sucker, Mountain (Catostomus platyrhynchus) Pacific populations
Sucker, Spotted (Minytrema melanops)
Sunfish, Northern (Lepomis peltastes) Great Lakes – Upper St. Lawrence populations
Thornyhead, Longspine (Sebastolobus altivelis)
Tope (Galeorhinus galeus)
Topminnow, Blackstripe (Fundulus notatus)
Trout, Bull (Salvelinus confluentus) South Coast British Columbia populations
Trout, Bull (Salvelinus confluentus) Western Arctic populations
Trout, Westslope Cutthroat (Oncorhynchus clarkii lewisi) British Columbia population
Warmouth (Lepomis gulosus)
Wolffish, Atlantic (Anarhichas lupus)
Molluscs
Floater, Brook (Alasmidonta varicosa)
Jumping-slug, Warty (Hemphillia glandulosa)
Lampmussel, Wavy-rayed (Lampsilis fasciola)
Lampmussel, Yellow (Lampsilis cariosa)
Mantleslug, Magnum (Magnipelta mycophaga)
Mapleleaf (Quadrula quadrula) Great Lakes – Upper St. Lawrence population
Mussel, Rocky Mountain Ridged (Gonidea angulata)
Oyster, Olympia (Ostrea lurida)
Pondmussel, Eastern (Ligumia nasuta)
Rainbow (Villosa iris)
Slug, Haida Gwaii (Staala gwaii)
Slug, Pygmy (Kootenaia burkei)
Slug, Sheathed (Zacoleus idahoensis)
Vertigo, Threaded (Nearctula sp.)
Arthropods
Bumble Bee, Yellow-banded (Bombus terricola)
Dancer, Vivid (Argia vivida)
Grasshopper, Greenish-white (Hypochlora alba)
Leafhopper, Red-tailed (Aflexia rubranura) Great Lakes Plains population
Leafhopper, Red-tailed (Aflexia rubranura) Prairie population
Metalmark, Mormon (Apodemia mormo) Prairie population
Monarch (Danaus plexippus)
Moth, Pale Yellow Dune (Copablepharon grandis)
Skipper, Sonora (Polites sonora)
Snaketail, Pygmy (Ophiogomphus howei)
Spider, Georgia Basin Bog (Gnaphosa snohomish)
Tachinid Fly, Dune (Germaria angustata)
Weidemeyer’s Admiral (Limenitis weidemeyerii)
Plants
Ash, Blue (Fraxinus quadrangulata)
Aster, Crooked-stem (Symphyotrichum prenanthoides)
Aster, Nahanni (Symphyotrichum nahanniense)
Aster, White-top (Sericocarpus rigidus)
Beggarticks, Vancouver Island (Bidens amplissima)
Blue Flag, Western (Iris missouriensis)
Buffalograss (Bouteloua dactyloides)
Fern, American Hart’s-tongue (Asplenium scolopendrium)
Fern, Coastal Wood (Dryopteris arguta)
Goldencrest (Lophiola aurea)
Goldenrod, Houghton’s (Solidago houghtonii)
Goldenrod, Riddell’s (Solidago riddellii)
Hairgrass, Mackenzie (Deschampsia mackenzieana)
Hoptree, Common (Ptelea trifoliata)
Indian-plantain, Tuberous (Arnoglossum plantagineum)
Iris, Dwarf Lake (Iris lacustris)
Lilaeopsis, Eastern (Lilaeopsis chinensis)
Lily, Lyall’s Mariposa (Calochortus lyallii)
Milk-vetch, Fernald’s (Astragalus robbinsii var. fernaldii)
Pennywort, Water (Hydrocotyle umbellata)
Pinweed, Beach (Lechea maritima)
Podistera, Yukon (Podistera yukonensis)
Pondweed, Hill’s (Potamogeton hillii)
Prairie-clover, Hairy (Dalea villosa)
Quillwort, Prototype (Isoetes prototypus)
Redroot (Lachnanthes caroliniana)
Rose, Climbing Prairie (Rosa setigera)
Rose-mallow, Swamp (Hibiscus moscheutos)
Rush, New Jersey (Juncus caesariensis)
Saxifrage, Spiked (Micranthes spicata)
Sedge, Baikal (Carex sabulosa)
Spike-rush, Tubercled (Eleocharis tuberculosa)
Tansy, Floccose (Tanacetum huronense var. floccosum)
Thistle, Pitcher’s (Cirsium pitcheri)
Thrift, Athabasca (Armeria maritima interior)
Water-hemlock, Victorin’s (Cicuta maculata var. victorinii)
Wild Buckwheat, Yukon (Eriogonum flavum var. aquilinum)
Willow, Felt-leaf (Salix silicicola)
Willow, Sand-dune Short-capsuled (Salix brachycarpa var. psammophila)
Willow, Turnor’s (Salix turnorii)
Woolly-heads, Dwarf (Psilocarphus brevissimus) Prairie population
Yarrow, Large-headed Woolly (Achillea millefolium var. megacephalum)
Mosses
Cord-moss, Banded (Entosthodon fascicularis)
Moss, Columbian Carpet (Bryoerythrophyllum columbianum)
Moss, Twisted Oak (Syntrichia laevipila)
Tassel, Tiny (Crossidium seriatum)
Lichens
Glass-whiskers, Frosted (Sclerophora peronella) Nova Scotia population
Jellyskin, Flooded (Leptogium rivulare)
Lichen, Blue Felt (Degelia plumbea)
Lichen, Boreal Felt (Erioderma pedicallatum) Boreal population
Lichen, Cryptic Paw (Nephroma occultum)
Lichen, Oldgrowth Specklebelly (Pseudocyphellaria rainierensis)
Lichen, Peacock Vinyl (Leptogium polycarpum)
Mountain Crab-eye (Acroscyphus sphaerophoroides)
Waterfan, Western (Peltigera gowardii)""".split('\n\n')

Species_at_Risk.append(all_canadian_species_at_risk)

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