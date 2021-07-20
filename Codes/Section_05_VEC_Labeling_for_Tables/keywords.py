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
Pipistrelle de l\'Est
Caribou
Rangifer tarandus pearyi
Caribou de Peary
Rangifer tarandus caribou
Kangaroo Rat
Dipodomys ordii
Rat kangourou d\'Ord
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
Barn Owl
Tyto alba
Burrowing Owl
Athene cunicularia
caurina
Spotted Owl
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
Carmine Shiner
Notropis percobromus
Rainbow Smelt
Osmerus mordax
Rainbow Smelt
Osmerus mordax
Enos Lake Benthic Threespine Stickleback
Gasterosteus aculeatus
Enos Lake Limnetic Threespine Stickleback
Misty Lake Lentic Threespine Stickleback
Misty Lake Lotic Threespine Stickleback
Paxton Lake Benthic Threespine Stickleback
Paxton Lake Limnetic Threespine Stickleback
Vananda Creek Benthic Threespine Stickleback
Vananda Creek Limnetic Threespine Stickleback
Gasterosteus aculeatus
White Sturgeon
Acipenser transmontanus
Rainbow Trout
Oncorhynchus mykiss
Atlantic Whitefish
Coregonus huntsmani
Northern Molluscs
Abalone
Haliotis kamtschatkana
Rayed Bean
Villosa fabalis
Fawnsfoot
Truncilla donaciformis
Broad-banded Forestsnail
Allogona profunda
Oregon Forestsnail
Allogona townsendiana
Proud Globelet
Patera pennsylvanica
Hickorynut
Obovaria olivaria
Round Hickorynut
Obovaria subrotunda
Kidneyshell
Ptychobranchus fasciolaris
Lilliput
Toxolasma parvum
Salamander Mussel
Simpsonaias ambigua
Hotwater Physa
Physella wrighti
Round Pigtoe
Pleurobema sintoxia
Northern Riffleshell
Epioblasma torulosa rangiana
Banff Springs Snail
Physella johnsoni
Snuffbox
Epioblasma triquetra
Island Arthropods
Blue
Plebejus saepiolus insulanus
Aweme Borer
Papaipema aweme
Hoptree Borer
Prays atomocella
Bogbean Buckmoth
Hemileuca sp.
Gypsy Cuckoo Bumble Bee
Bombus bohemicus
Rusty-patched Bumble Bee
Bombus affinis
Taylor\'s Checkerspot
Euphydryas editha taylori
Olive Clubtail
Stylurus olivaceus
Rapids Clubtail
Gomphus quadricolor
Riverine Clubtail
Stylurus amnicola
Skillet Clubtail
Gomphus ventricosus
Hungerford\'s Crawling Water Beetle
Brychius hungerfordi
Macropis Cuckoo Bee
Epeoloides pilosulus
Bert\'s Predaceous Diving Beetle
Sanfilippodytes bertae
Eastern Persius Duskywing
Erynnis persius persius
Okanagan Efferia
Efferia okanagana
Hine\'s Emerald
Somatochlora hineana
White Flower Moth
Schinia bimatris
Gold-edged Gem
Schinia avemensis
Behr\'s Hairstreak
Satyrium behrii
Half-moon Hairstreak
Satyrium semiluna
Mormon Metalmark
Apodemia mormo
Dusky Dune Moth
Copablepharon longipenne
Edwards\' Beach Moth
Anarta edwardsii
Five-spotted Bogus Yucca Moth
Prodoxus quinquepunctellus
Non-pollinating Yucca Moth
Tegeticula corruptrix
Sand-verbena Moth
Copablepharon fuscum
Yucca Moth
Tegeticula yuccasella
Maritime Ringlet
Coenonympha nipisiquit
Dakota Skipper
Hesperia dacotae
Poweshiek Skipperling
Oarisma poweshiek
Ottoe Skipper
Hesperia ottoe
False-foxglove Sun Moth
Pyrrhia aurantiago
Cobblestone Tiger Beetle
Cicindela marginipennis
Northern Barrens Tiger Beetle
Cicindela patruela
Wallis\' Dark Saltflat Tiger Beetle
Cicindela parowana wallisi
Gattinger\'s Plants
Agalinis
Agalinis gattingeri
Rough Agalinis
Agalinis aspera
Skinner\'s Agalinis
Agalinis skinneriana
Scarlet Ammannia
Ammannia robusta
Short-rayed Alkali Aster
Symphyotrichum frondosum
Eastern Mountain Avens
Geum peckii
Deltoid Balsamroot
Balsamorhiza deltoidea
Tall Beakrush
Rhynchospora macrostachya
Cherry Birch
Betula lenta
Bluehearts
Buchnera americana
Fernald\'s Braya
Braya fernaldii
Hairy Braya
Braya pilosa
Long\'s Braya
Braya longii
Tall Bugbane
Actaea elata
Bashful Bulrush
Trichophorum planifolium
Slender Bush-clover
Lespedeza virginica
California Buttercup
Ranunculus californicus
Water-plantain Buttercup
Ranunculus alismifolius
Butternut
Juglans cinerea
Eastern Prickly Pear Cactus
Opuntia humifusa
Spalding\'s Campion
Silene spaldingii
Coastal Scouler\'s Catchfly
Silene scouleri grandis
Muhlenberg\'s Centaury
Centaurium muehlenbergii
American Chestnut
Castanea dentata
Colicroot
Aletris farinosa
Slender Collomia
Collomia tenella
American Columbo
Frasera caroliniensis
Pink Coreopsis
Coreopsis rosea
Eastern Flowering Dogwood
Cornus florida
Contorted-pod Evening-primrose
Camissonia contorta
Southern Maidenhair Fern
Adiantum capillus-veneris
Eastern Prairie Fringed-orchid
Platanthera leucophaea
Western Prairie Fringed-orchid
Platanthera praeclara
Plymouth Gentian
Sabatia kennedyana
White Prairie Gentian
Gentiana alba
American Ginseng
Panax quinquefolius
Virginia Goat\'s-rue
Tephrosia virginiana
Showy Goldenrod
Solidago speciosa
Rayless Goldfields
Lasthenia glaberrima
Forked Three-awned Grass
Aristida basiramea
Fascicled Ironweed
Vernonia fasciculata
Tweedy\'s Lewisia
Lewisiopsis tweedyi
Small-flowered Lipocarpha
Lipocarpha micrantha
Seaside Birds-foot Lotus
Lotus formosissimus
Furbish\'s Lousewort
Pedicularis furbishiae
Dense-flowered Lupine
Lupinus densiflorus
Prairie Lupine
Lupinus lepidus
Streambank Lupine
Lupinus rivularis
Virginia Mallow
Sida hermaphrodita
White Meconella
Meconella oregana
Coast Microseris
Microseris bigelovii
Pink Milkwort
Polygala incarnata
Hoary Mountain-mint
Pycnanthemum incanum
Red Mulberry
Morus rubra
Phantom Orchid
Cephalanthera austiniae
Bearded Owl-clover
Triphysaria versicolor
Grand Coulee Owl-clover
Orthocarpus barbatus
Rosy Owl-clover
Orthocarpus bracteosus
Victoria\'s Owl-clover
Castilleja victoriae
Golden Paintbrush
Castilleja levisecta
Branched Phacelia
Phacelia ramosissima
Whitebark Pine
Pinus albicaulis
Heart-leaved Plantain
Plantago cordata
Large Whorled Pogonia
Isotria verticillata
Nodding Pogonia
Triphora trianthophora
Small Whorled Pogonia
Isotria medeoloides
Ogden\'s Pondweed
Potamogeton ogdenii
Fragrant Popcornflower
Plagiobothrys figuratus
Stoloniferous Pussytoes
Antennaria flagellaris
Engelmann\'s Quillwort
Isoetes engelmannii
Quebec Rockcress
Boechera quebecensis
Kellogg\'s Rush
Juncus kelloggii
Pink Sand-verbena
Abronia umbellata
Small-flowered Sand-verbena
Tripterocalyx micranthus
Dwarf Sandwort
Minuartia pusilla
False Hop Sedge
Carex lupuliformis
Foothill Sedge
Carex tumulicola
Juniper Sedge
Carex juniperorum
Lindley\'s False Silverpuffs
Uropappus lindleyi
Brook Spike-primrose
Epilobium torreyi
Dense Spike-primrose
Epilobium densiflorum
Bent Spike-rush
Eleocharis geniculata
Bent Spike-rush
Eleocharis geniculata
Horsetail Spike-rush
Eleocharis equisetoides
Thread-leaved Sundew
Drosera filiformis
Small-flowered Tonella
Tonella tenella
Toothcup
Rotala ramosior
Cucumber Tree
Magnolia acuminata
Bog Bird\'s-foot Trefoil
Lotus pinnatus
Drooping Trillium
Trillium flexipes
Howell\'s Triteleia
Triteleia howellii
Bird’s-foot Violet
Viola pedata
Yellow Montane Violet praemorsa subspecies
Viola praemorsa ssp. praemorsa
Barrens Willow
Salix jejuna
Spotted Wintergreen
Chimaphila maculata
Wood-poppy
Stylophorum diphyllum
Tall Woolly-heads
Psilocarphus elatior
Dwarf Woolly-heads
Psilocarphus brevissimus
Batwing Vinyl Lichens
Lichen
Leptogium platynum
Boreal Felt Lichen
Erioderma pedicellatum
Pale-bellied Frost Lichen
Physconia subpallida
Seaside Centipede Lichen
Heterodermia sitchensis
Vole Ears Lichen
Erioderma mollissimum
Rusty Mosses
Cord-moss
Entosthodon rubiginosus
Acuteleaf Small Limestone Moss
Seligeria acutifolia
Margined Streamside Moss
Scouleria marginata
Nugget Moss
Microbryum vlassovii
Poor Pocket Moss
Fissidens pauperculus
Rigid Apple Moss
Bartramia stricta
Roell\'s Brotherella Moss
Brotherella roellii
Silver Hair Moss
Fabronia pusilla
Bat
Antrozous pallidus
Wood Bison
Bison bison athabascae
Woodland Caribou
Rangifer tarandus caribou
Ermine haidarum subspecies
Mustela erminea haidarum
Grey Fox
Urocyon cinereoargenteus
Swift Fox
Vulpes velox
American Marten
Martes americana atrata
Black-tailed Prairie Dog
Cynomys ludovicianus
Beluga Whale
Delphinapterus leucas
Fin Whale
Balaenoptera physalus
Killer Whale
Orcinus orca
Short-tailed Birds
Albatross
Phoebastria albatrus
Least Bittern
Ixobrychus exilis
Bobolink
Dolichonyx oryzivorus
Lark Bunting
Calamospiza melanocorys
Red Crossbill percna subspecies
Loxia curvirostra percna
Olive-sided Flycatcher
Contopus cooperi
Northern Goshawk laingi subspecies
Accipiter gentilis laingi
Ross\'s Gull
Rhodostethia rosea
Ferruginous Hawk
Buteo regalis
Red Knot roselaari type
Calidris canutus roselaari type
Chestnut-collared Longspur
Calcarius ornatus
McCown\'s Longspur
Rhynchophanes mccownii
Eastern Meadowlark
Sturnella magna
Marbled Murrelet
Brachyramphus marmoratus
Common Nighthawk
Chordeiles minor
Barn Owl
Tyto alba
Northern Saw-whet Owl brooksi subspecies
Aegolius acadicus brooksi
Sprague\'s Pipit
Anthus spragueii
Western Screech-owl kennicottii subspecies
Megascops kennicottii kennicottii
Megascops kennicottii macfarlanei
Loggerhead Shrike excubitorides subspecies
Lanius ludovicianus excubitorides
Bank Swallow
Riparia riparia
Barn Swallow
Hirundo rustica
Chimney Swift
Chaetura pelagica
Bicknell\'s Thrush
Catharus bicknelli
Wood Thrush
Hylocichla mustelina
Canada Warbler
Wilsonia canadensis
Golden-winged Warbler
Vermivora chrysoptera
Louisiana Waterthrush
Parkesia motacilla
Whip-poor-will
Caprimulgus vociferus
Lewis\'s Woodpecker
Melanerpes lewis
Rocky Mountain Tailed Amphibians
Frog
Ascaphus montanus
Western Chorus Frog
Pseudacris triseriata
Coastal Giant Salamander
Dicamptodon tenebrosus
Spring Salamander
Gyrinophilus porphyriticus
Great Basin Spadefoot
Spea intermontana
Great Basin Reptiles
Gophersnake
Pituophis catenifer deserticola
Massasauga
Sistrurus catenatus
Eastern Yellow-bellied Racer
Coluber constrictor flaviventris
Gray Ratsnake
Pantherophis spiloides
Western Rattlesnake
Crotalus oreganos
Eastern Ribbonsnake
Thamnophis sauritus
Eastern Hog-nosed Snake
Heterodon platirhinos
Blanding\'s Turtle
Emydoidea blandingii
Wood Turtle
Glyptemys insculpta
Eastern Sand Fish
Darter
Ammocrypta pellucida
Eastern Sand Darter
Ammocrypta pellucida
Vancouver Lamprey
Entosphenus macrostomus
Plains Minnow
Hybognathus placitus
Pugnose Minnow
Opsopoeodus emiliae
Western Silvery Minnow
Hybognathus argyritis
Black Redhorse
Moxostoma duquesnei
Coastrange Sculpin
Cottus aleuticus
Rocky Mountain Sculpin
Cottus sp.
Pugnose Shiner
Notropis anogenus
Silver Shiner
Notropis photogenis
Spotted Wolffish
Anarhichas minor
Mountain Sucker
Catostomus platyrhynchus
Salish Sucker
Catostomus sp. cf. catostomus
Bull Trout
Salvelinus confluentus
Westslope Cutthroat Trout
Oncorhynchus clarkii lewisi
Northern Wolffish
Anarhichas denticulatus
Atlantic Mud-piddock
Barnea truncata
Dromedary Jumping-slug
Hemphillia dromedarius
Mapleleaf
Quadrula quadrula
Blue-grey Taildropper
Prophysaon coeruleum
Threehorn Wartyback
Obliquaria reflexa
Verna\'s Arthropods
Flower Moth
Schinia verna
Dun Skipper
Euphyes vestris
Sable Island Sweat Bee
Lasioglossum sablense
Audouin\'s Night-stalking Tiger Beetle
Omus audouini
Gibson\'s Big Sand Tiger Beetle
Cicindela formosa gibsoni
Griscom’s Plants
Arnica
Arnica griscomii ssp. griscomii
Anticosti Aster
Symphyotrichum anticostense
Gulf of St. Lawrence Aster
Symphyotrichum laurentianum
Western Silvery Aster
Symphyotrichum sericeum
White Wood Aster
Eurybia divaricata
Willowleaf Aster
Symphyotrichum praealtum
Eastern Baccharis
Baccharis halimifolia
Branched Bartonia
Bartonia paniculata ssp. paniculata
Dense Blazing Star
Liatris spicata
Kentucky Coffee-tree
Gymnocladus dioicus
Tiny Cryptantha
Cryptantha minima
Lakeside Daisy
Hymenoxys herbacea
Deerberry
Vaccinium stamineum
Gray\'s Desert-parsley
Lomatium grayi
Lemmon\'s Holly Fern
Polystichum lemmonii
Mountain Holly Fern
Polystichum scopulinum
Victorin\'s Gentian
Gentianopsis virgata ssp. victorinii
Showy Goldenrod
Solidago speciosa
Goldenseal
Hydrastis canadensis
Smooth Goosefoot
Chenopodium subglabrum
Round-leaved Greenbrier
Smilax rotundifolia
Dwarf Hackberry
Celtis tenuifolia
Wild Hyacinth
Camassia scilloides
Van Brunt\'s Jacob’s-ladder
Polemonium vanbruntiae
Small White Lady\'s-slipper
Cypripedium candidum
Hare-footed Locoweed
Oxytropis lagopus
Macoun\'s Meadowfoam
Limnanthes macounii
Mexican Mosquito-fern
Azolla mexicana
Slender Mouse-ear-cress
Halimolobos virgata
Cliff Paintbrush
Castilleja rupicola
Sweet Pepperbush
Clethra alnifolia
Showy Phlox
Phlox speciosa ssp. occidentalis
Slender Popcornflower
Plagiobothrys tenellus
Bolander\'s Quillwort
Isoetes bolanderi
False Rue-anemone
Enemion biternatum
Bear\'s-foot Sanicle
Sanicula arctopoides
Purple Sanicle
Sanicula bipinnatifida
Soapweed
Yucca glauca
Western Spiderwort
Tradescantia occidentalis
Hill\'s Thistle
Cirsium hillii
Toothcup
Rotala ramosior
Purple Twayblade
Liparis liliifolia
American Water-willow
Justicia americana
Green-scaled Willow
Salix chlorolepis
Blunt-lobed Woodsia
Woodsia obtusa
Seaside Lichens
Bone
Hypogymnia heterophylla
Black-foam Lichen
Anzia colpodes
Crumpled Tarpaper Lichen
Collema coniophilum
Wrinkled Shingle Lichen
Pannaria lurida
Eastern Waterfan
Peltigera hydrothyria
Porsild\'s Mosses
Bryum
Mielichhoferia macrocarpa
Alkaline Wing-nerved Moss
Pterygoneurum kozlovii
Haller\'s Apple Moss
Bartramia halleriana
Spoon-leaved Moss
Bryoandersonia illecebra
Badger taxus subspecies
Taxidea taxus taxus
Spotted Bat
Euderma maculatum
Grizzly Bear
Ursus arctos
Polar Bear
Ursus maritimus
Mountain Beaver
Aplodontia rufa
Barren-ground Caribou
Rangifer tarandus groenlandicus
Woodland Caribou
Rangifer tarandus caribou
Nuttall\'s Cottontail nuttallii subspecies
Sylvilagus nuttallii nuttallii
Eastern Mole
Scalopus aquaticus
Western Harvest Mouse megalotis subspecies
Reithrodontomys megalotis megalotis
Sea Otter
Enhydra lutris
Collared Pika
Ochotona collaris
Harbour Porpoise
Phocoena phocoena
Steller Sea Lion
Eumetopias jubatus
Woodland Vole
Microtus pinetorum
Bowhead Whale
Balaena mysticetus
Fin Whale
Balaenoptera physalus
Grey Whale
Eschrichtius robustus
Humpback Whale
Megaptera novaeangliae
Sowerby\'s Beaked Whale
Mesoplodon bidens
Eastern Wolf
Canis lupus lycaon
Wolverine
Gulo gulo
Black-footed Birds
Albatross
Phoebastria nigripes
Cassin\'s Auklet
Ptychoramphus aleuticus
Rusty Blackbird
Euphagus carolinus
Long-billed Curlew
Numenius americanus
Harlequin Duck
Histrionicus histrionicus
Peregrine Falcon anatum/tundrius
Falco peregrinus anatum/tundrius
Peregrine Falcon pealei subspecies
Falco peregrinus pealei
Barrow\'s Goldeneye
Bucephala islandica
Horned Grebe
Podiceps auritus
Western Grebe
Aechmophorus occidentalis
Evening Grosbeak
Coccothraustes vespertinus
Great Blue Heron fannini subspecies
Ardea herodias fannini
Red Knot islandica subspecies
Calidris canutus islandica
Ancient Murrelet
Synthliboramphus antiquus
Flammulated Owl
Otus flammeolus
Short-eared Owl
Asio flammeus
Red-necked Phalarope
Phalaropus lobatus
Band-tailed Pigeon
Patagioenas fasciata
Yellow Rail
Coturnicops noveboracensis
Buff-breasted Sandpiper
Tryngites subruficollis
Baird\'s Sparrow
Ammodramus bairdii
Grasshopper Sparrow pratensis subspecies
Ammodramus savannarum pratensis
Savannah Sparrow princeps subspecies
Passerculus sandwichensis princeps
Eastern Wood-pewee
Contopus virens
Coastal Tailed Amphibians
Ascaphus truei
Northern Leopard Frog
Lithobates pipiens
Red-legged Frog
Rana aurora
Coeur d\'Alene Salamander
Plethodon idahoensis
Wandering Salamander
Aneides vagrans
Western Tiger Salamander
Ambystoma mavortium
Great Plains Toad
Anaxyrus cognatus
Western Toad
Anaxyrus boreas
Western Toad
Anaxyrus boreas
Rubber Reptiles
Boa
Charina bottae
Milksnake
Lampropeltis triangulum
Western Yellow-bellied Racer
Coluber constrictor mormon
Prairie Rattlesnake
Crotalus viridis
Eastern Ribbonsnake
Thamnophis sauritus
Five-lined Skink
Plestiodon fasciatus
Prairie Skink
Plestiodon septentrionalis
Western Skink
Plestiodon skiltonianus
Eastern Musk Turtle
Sternotherus odoratus
Eastern Painted Turtle
Chrysemys picta picta
Midland Painted Turtle
Chrysemys picta marginata
Northern Map Turtle
Graptemys geographica
Snapping Turtle
Chelydra serpentina
Western Painted Turtle
Chrysemys picta bellii
Lake Erie Watersnake
Nerodia sipedon insularum
Bigmouth Fish
Buffalo
Ictiobus cyprinellus
Channel Darter
Percina copelandi
Dolly Varden
Salvelinus malma malma
Banded Killifish
Fundulus diaphanus
Upper Great Lakes Kiyi
Coregonus kiyi kiyi
Northern Brook Lamprey
Ichthyomyzon fossor
Silver Lamprey
Ichthyomyzon unicuspis
Cutlip Minnow
Exoglossum maxillingua
Grass Pickerel
Esox americanus vermiculatus
River Redhorse
Moxostoma carinatum
Rougheye Rockfish type I
Sebastes sp. type I
Rougheye Rockfish type II
Sebastes sp. type II
Yelloweye Rockfish
Sebastes ruberrimus
Yelloweye Rockfish
Sebastes ruberrimus
Columbia Sculpin
Cottus hubbsi
Deepwater Sculpin
Myoxocephalus thompsonii
Rocky Mountain Sculpin
Cottus sp.
Shorthead Sculpin
Cottus confusus
Bluntnose Sixgill Shark
Hexanchus griseus
Bridle Shiner
Notropis bifrenatus
Giant Threespine Stickleback
Gasterosteus aculeatus
Unarmoured Threespine Stickleback
Gasterosteus aculeatus
Green Sturgeon
Acipenser medirostris
Lake Sturgeon
Acipenser fulvescens
Shortnose Sturgeon
Acipenser brevirostrum
Mountain Sucker
Catostomus platyrhynchus
Spotted Sucker
Minytrema melanops
Northern Sunfish
Lepomis peltastes
Longspine Thornyhead
Sebastolobus altivelis
Tope
Galeorhinus galeus
Blackstripe Topminnow
Fundulus notatus
Bull Trout
Salvelinus confluentus
Bull Trout
Salvelinus confluentus
Westslope Cutthroat Trout
Oncorhynchus clarkii lewisi
Warmouth
Lepomis gulosus
Atlantic Wolffish
Anarhichas lupus
Brook Molluscs
Floater
Alasmidonta varicosa
Warty Jumping-slug
Hemphillia glandulosa
Wavy-rayed Lampmussel
Lampsilis fasciola
Yellow Lampmussel
Lampsilis cariosa
Magnum Mantleslug
Magnipelta mycophaga
Mapleleaf
Quadrula quadrula
Rocky Mountain Ridged Mussel
Gonidea angulata
Olympia Oyster
Ostrea lurida
Eastern Pondmussel
Ligumia nasuta
Rainbow
Villosa iris
Haida Gwaii Slug
Staala gwaii
Pygmy Slug
Kootenaia burkei
Sheathed Slug
Zacoleus idahoensis
Threaded Vertigo
Nearctula sp.
Yellow-banded Arthropods
Bumble Bee
Bombus terricola
Vivid Dancer
Argia vivida
Greenish-white Grasshopper
Hypochlora alba
Red-tailed Leafhopper
Aflexia rubranura
Red-tailed Leafhopper
Aflexia rubranura
Mormon Metalmark
Apodemia mormo
Monarch
Danaus plexippus
Pale Yellow Dune Moth
Copablepharon grandis
Sonora Skipper
Polites sonora
Pygmy Snaketail
Ophiogomphus howei
Georgia Basin Bog Spider
Gnaphosa snohomish
Dune Tachinid Fly
Germaria angustata
Weidemeyer\'s Admiral
Limenitis weidemeyerii
Blue Ash
Fraxinus quadrangulata
Crooked-stem Aster
Symphyotrichum prenanthoides
Nahanni Aster
Symphyotrichum nahanniense
White-top Aster
Sericocarpus rigidus
Vancouver Island Beggarticks
Bidens amplissima
Western Blue Flag
Iris missouriensis
Buffalograss
Bouteloua dactyloides
American Hart\'s-tongue Fern
Asplenium scolopendrium
Coastal Wood Fern
Dryopteris arguta
Goldencrest
Lophiola aurea
Houghton\'s Goldenrod
Solidago houghtonii
Riddell\'s Goldenrod
Solidago riddellii
Mackenzie Hairgrass
Deschampsia mackenzieana
Common Hoptree
Ptelea trifoliata
Tuberous Indian-plantain
Arnoglossum plantagineum
Dwarf Lake Iris
Iris lacustris
Eastern Lilaeopsis
Lilaeopsis chinensis
Lyall\'s Mariposa Lily
Calochortus lyallii
Fernald’s Milk-vetch
Astragalus robbinsii var. fernaldii
Water Pennywort
Hydrocotyle umbellata
Beach Pinweed
Lechea maritima
Yukon Podistera
Podistera yukonensis
Hill\'s Pondweed
Potamogeton hillii
Hairy Prairie-clover
Dalea villosa
Prototype Quillwort
Isoetes prototypus
Redroot
Lachnanthes caroliniana
Climbing Prairie Rose
Rosa setigera
Swamp Rose-mallow
Hibiscus moscheutos
New Jersey Rush
Juncus caesariensis
Spiked Saxifrage
Micranthes spicata
Baikal Sedge
Carex sabulosa
Tubercled Spike-rush
Eleocharis tuberculosa
Floccose Tansy
Tanacetum huronense var. floccosum
Pitcher\'s Thistle
Cirsium pitcheri
Athabasca Thrift
Armeria maritima interior
Victorin\'s Water-hemlock
Cicuta maculata var. victorinii
Yukon Wild Buckwheat
Eriogonum flavum var. aquilinum
Felt-leaf Willow
Salix silicicola
Sand-dune Short-capsuled Willow
Salix brachycarpa var. psammophila
Turnor\'s Willow
Salix turnorii
Dwarf Woolly-heads
Psilocarphus brevissimus
Large-headed Woolly Yarrow
Achillea millefolium var. megacephalum
Banded Mosses
Cord-moss
Entosthodon fascicularis
Columbian Carpet Moss
Bryoerythrophyllum columbianum
Twisted Oak Moss
Syntrichia laevipila
Tiny Tassel
Crossidium seriatum
Frosted Lichens
Glass-whiskers
Sclerophora peronella
Flooded Jellyskin
Leptogium rivulare
Blue Felt Lichen
Degelia plumbea
Boreal Felt Lichen
Erioderma pedicallatum
Cryptic Paw Lichen
Nephroma occultum
Oldgrowth Specklebelly Lichen
Pseudocyphellaria rainierensis
Peacock Vinyl Lichen
Leptogium polycarpum
Mountain Crab-eye
Acroscyphus sphaerophoroides
Western Waterfan
Peltigera gowardii""".split('\n')

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