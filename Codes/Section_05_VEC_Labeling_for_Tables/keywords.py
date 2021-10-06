import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import *
from nltk.tokenize import word_tokenize

Landscape_terrain_and_weather = """Physical and Meteorological Environment
Physical Environment
Meteorological Environment
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
terrain
landscape
weather
physiography
bedrock
geology
natural hazard"""


Soil = """Soil Productivity
Soil
Agriculture
Topsoil
Subsoil
Soil horizon
Drainage
Erosion
soil contamination
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

Plants = """Vegetation
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
chokecherry
Gattinger\'s Agalinis
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
Bird\'s-foot Violet
Viola pedata
Yellow Montane Violet praemorsa
praemorsa
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
Batwing Vinyl Lichen
Leptogium platynum
Boreal Felt Lichen
Erioderma pedicellatum
Pale-bellied Frost Lichen
Physconia subpallida
Seaside Centipede Lichen
Heterodermia sitchensis
Vole Ears Lichen
Rusty Cord-moss
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
Griscom’s Arnica
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
Seaside Bone
Hypogymnia heterophylla
Black-foam Lichen
Anzia colpodes
Crumpled Tarpaper Lichen
Collema coniophilum
Wrinkled Shingle Lichen
Pannaria lurida
Eastern Waterfan
Peltigera hydrothyria
Porsild\'s Bryum
Mielichhoferia macrocarpa
Alkaline Wing-nerved Moss
Pterygoneurum kozlovii
Haller\'s Apple Moss
Bartramia halleriana
Spoon-leaved Moss
Bryoandersonia illecebra
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
Fernald\'s Milk-vetch
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
Peltigera gowardii"""

Water = """Water Quality and Quantity
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
aquatics
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
creek
tidal
subtidal
mercury
water contamination"""

Fish = """Fish
Fish Habitat
fish-bearing
fisheries
Fisheries and Oceans Canada
mercury
water contamination
deleterious
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
acquatic
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
sea
ocean
lake
pond
bay
subtidal
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
Vananda Creek Benthic Threespine Stickleback
Vananda Creek Limnetic Threespine Stickleback
Gasterosteus aculeatus
White Sturgeon
Acipenser transmontanus
Rainbow Trout
Oncorhynchus mykiss
Atlantic Whitefish
Coregonus huntsmani
Eastern Sand Darter
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
Bigmouth Buffalo
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
Westslope Cutthroat Trout
Oncorhynchus clarkii lewisi
Warmouth
Lepomis gulosus
Atlantic Wolffish
Anarhichas lupus"""

Wetlands = """Wetlands
Class (wetland class)
wetland
Bog
Fen
Marsh
Swamp
Shallow water
Wetland function
Hydrological function
Drainage area
Canadian wetland classification system
Federal policy on wetland conservation
Wetland monitoring
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
baygall
slough"""

Wildlife = """Wildlife and Wildlife Habitat
wildlife
wildlife habitat
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
eggs
Den
migration
staging
movement corridors
forest interior
denning
Wintering
overwintering
national park
national wildlife reserve
national wildlife area
world biosphere reserve
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
mollusk
mollusc
reptile
amphibian
mineral lick
minerallick
hunting
trapping
American Badger jacksoni
jaksoni
Badger
Taxidea taxus jacksoni
American Badger jeffersonii
Taxidea taxus jeffersonii
American Badger jeffersonii
jeffersonii
Taxidea taxus jeffersonii
Tri-coloured Bat
Perimyotis subflavus
Peary Caribou
Caribou
Rangifer tarandus pearyi
Woodland Caribou
Rangifer tarandus caribou
Ord\'s Kangaroo Rat
Dipodomys ordii
Vancouver Island Marmot
Marmota vancouverensis
Townsend\'s Mole
Scapanus townsendii
Western Harvest Mouse dychei
dychei
Reithrodontomys megalotis dychei
Little Brown Myotis
Myotis
Myotis lucifugus
Northern Myotis
Myotis septentrionalis
Northern Bobwhite
Colinus virginianus
Yellow-breasted Chat auricollis
auricollis
Icteria virens auricollis
Yellow-breasted Chat virens
virens
Icteria virens virens
Whooping Crane
Grus americana
Eskimo Curlew
Numenius borealis
Acadian Flycatcher
Empidonax virescens
Horned Grebe
Podiceps auritus
Ivory Gull
Pagophila eburnea
Red Knot rufa
rufa
Calidris canutus rufa
Streaked Horned Lark
Eremophila alpestris strigata
Barn Owl
Tyto alba
Burrowing Owl
Athene cunicularia
Spotted Owl caurina
caurina
Strix occidentalis caurina
Mountain Plover
Charadrius montanus
Piping Plover circumcinctus
circuinctus
Charadrius melodus circumcinctus
Piping Plover melodus
melodus
Charadrius melodus melodus
King Rail
Rallus elegans
Greater Sage-Grouse urophasianus subspecies
Centrocercus urophasianus urophasianus
Williamson\'s Sapsucker
Sphyrapicus thyroideus
Pink-footed Shearwater
Ardenna creatopus
Loggerhead Shrike migrans
migrans
Lanius ludovicianus migrans
Coastal Vesper Sparrow
Pooecetes gramineus affinis
Henslow\'s Sparrow
Ammodramus henslowii
Black Swift
Cypseloides niger
Roseate Tern
Sterna dougallii
Sage Thrasher
Oreoscoptes montanus
Cerulean Warbler
Setophaga cerulea
Kirtland\'s Warbler
Dendroica kirtlandii
Prothonotary Warbler
Protonotaria citrea
Red-headed Woodpecker
Melanerpes erythrocephalus
White-headed Woodpecker
Picoides albolarvatus
Cricket Frog
Acris blanchardi
Northern Leopard Frog
Lithobates pipiens
Oregon Spotted Frog
Rana pretiosa
Allegheny Mountain Dusky Salamander
Desmognathus ochrophaeus
Allegheny Mountain Dusky Salamander
Desmognathus ochrophaeus
Eastern Tiger Salamander
Ambystoma tigrinum
Jefferson Salamander
Ambystoma jeffersonianum
Northern Dusky Salamander
Desmognathus fuscus
Small-mouthed Salamander
Ambystoma texanum
Western Tiger Salamander
Ambystoma mavortium
Fowler\'s Toad
Anaxyrus fowleri
Eastern Reptiles
Foxsnake
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
Leatherback Sea Turtle
Dermochelys coriacea
Loggerhead Sea Turtle
Caretta caretta
Five-lined Skink
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
Broad-banded Forestsnail
Allogona profunda
Oregon Forestsnail
Allogona townsendiana
Proud Globelet
Patera pennsylvanica
Hotwater Physa
Physella wrighti
Island Blue
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
Pallid Bat
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
Short-tailed Birds
Albatross
Phoebastria albatrus
Least Bittern
Ixobrychus exilis
Bobolink
Dolichonyx oryzivorus
Lark Bunting
Calamospiza melanocorys
Red Crossbill percna
percna
Loxia curvirostra percna
Olive-sided Flycatcher
Contopus cooperi
Northern Goshawk laingi
laingi
Accipiter gentilis laingi
Ross\'s Gull
Rhodostethia rosea
Ferruginous Hawk
Buteo regalis
Red Knot roselaari type
Calidris canutus roselaari
roselaari
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
Northern Saw-whet Owl brooksi
brooksi
Aegolius acadicus brooksi
Sprague\'s Pipit
Anthus spragueii
Western Screech-owl kennicottii
kennicottii
Megascops kennicottii kennicottii
Megascops kennicottii macfarlanei
Loggerhead Shrike excubitorides
excubitorides
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
Rocky Mountain Tailed Frog
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
Dromedary Jumping-slug
Hemphillia dromedarius
Blue-grey Taildropper
Prophysaon coeruleum
Verna\'s Flower Moth
Schinia verna
Dun Skipper
Euphyes vestris
Sable Island Sweat Bee
Lasioglossum sablense
Audouin\'s Night-stalking Tiger Beetle
Omus audouini
Gibson\'s Big Sand Tiger Beetle
Cicindela formosa gibsoni
Badger taxus
taxus
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
Nuttall\'s Cottontail nuttallii
nuttallii
Sylvilagus nuttallii nuttallii
Eastern Mole
Scalopus aquaticus
Western Harvest Mouse megalotis subspecies
Reithrodontomys megalotis megalotis
Collared Pika
Ochotona collaris
Woodland Vole
Microtus pinetorum
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
Great Blue Heron fannini
fannini
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
Rubber Boa
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
Brook Floater
Alasmidonta varicosa
Warty Jumping-slug
Hemphillia glandulosa
Haida Gwaii Slug
Staala gwaii
Pygmy Slug
Kootenaia burkei
Sheathed Slug
Zacoleus idahoensis
Threaded Vertigo
Nearctula sp.
Magnum Mantleslug
Magnipelta mycophaga
Yellow-banded Bumble Bee
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
orca
Northern Abalone
Haliotis kamtschatkana
Rayed Bean
Villosa fabalis
Fawnsfoot
Truncilla donaciformis
Kidneyshell
Ptychobranchus fasciolaris
Lilliput
Toxolasma parvum
Salamander Mussel
Simpsonaias ambigua
Round Pigtoe
Pleurobema sintoxia
Northern Riffleshell
Epioblasma torulosa rangiana
Banff Springs Snail
Physella johnsoni
Snuffbox
Epioblasma triquetra
Atlantic Mud-piddock
Barnea truncata
Mapleleaf
Quadrula quadrula
Threehorn Wartyback
Obliquaria reflexa
Sea Otter
Enhydra lutris
Harbour Porpoise
Phocoena phocoena
Steller Sea Lion
Eumetopias jubatus
whale
marine mammal
marine organisms
Bowhead Whale
Balaena mysticetus
Fin Whale
Balaenoptera physalus
Grey Whale
Eschrichtius robustus
Humpback Whale
Megaptera novaeangliae
Sowerby\'s Beaked Whale
Brook Floater
Alasmidonta varicosa
Wavy-rayed Lampmussel
Lampsilis fasciola
Yellow Lampmussel
Lampsilis cariosa
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
Harbour Seal Lacs des Loups Marins
Seal
Phoca vitulina mellonae
Pacific Water Shrew
Sorex bendirii
Whale
Beluga Whale
Delphinapterus leucas
Blue Whale
Balaenoptera musculus
Blue Whale
Balaenoptera musculus
Killer Whale
Orcinus orca
North Atlantic Right Whale
Eubalaena glacialis
North Pacific Right Whale
Eubalaena japonica
Northern Bottlenose Whale
Hyperoodon ampullatus
Sei Whale
Balaenoptera borealis
Beluga Whale
Delphinapterus leucas
Fin Whale
Balaenoptera physalus
Killer Whale
Orcinus orcaesoplodon bidens
clam
scallop
butterfly"""

Species_at_Risk = """Species at Risk
Species of Special Status
Rare Species
SARA
s. 73
section 73
Species At Risk Act
Endangered Species
Threatened Species
Endangered Wildlife
Critical Habitat
COSEWIC
Committee on the Status of Endangered Wildlife in Canada
Critical habitat
Designation
Schedule 1
At Risk
Endangered
Critical timing window
Restricted activity period
Canadian Wildlife Service
CWS
Recovery Strategy
Action Plan
Permit
Caribou
Bat
special conservation status
American Badger jacksoni
jaksoni
Badger
Taxidea taxus jacksoni
American Badger jeffersonii
Taxidea taxus jeffersonii
American Badger jeffersonii
jeffersonii
Taxidea taxus jeffersonii
Tri-coloured Bat
Perimyotis subflavus
Peary Caribou
Caribou
Rangifer tarandus pearyi
Woodland Caribou
Rangifer tarandus caribou
Ord\'s Kangaroo Rat
Dipodomys ordii
Vancouver Island Marmot
Marmota vancouverensis
Townsend\'s Mole
Scapanus townsendii
Western Harvest Mouse dychei
dychei
Reithrodontomys megalotis dychei
Little Brown Myotis
Myotis
Myotis lucifugus
Northern Myotis
Myotis septentrionalis
Harbour Seal Lacs des Loups Marins
Seal
Phoca vitulina mellonae
Pacific Water Shrew
Sorex bendirii
Whale
Beluga Whale
Delphinapterus leucas
Blue Whale
Balaenoptera musculus
Blue Whale
Balaenoptera musculus
Killer Whale
Orcinus orca
North Atlantic Right Whale
Eubalaena glacialis
North Pacific Right Whale
Eubalaena japonica
Northern Bottlenose Whale
Hyperoodon ampullatus
Sei Whale
Balaenoptera borealis
Northern Bobwhite
Colinus virginianus
Yellow-breasted Chat auricollis
auricollis
Icteria virens auricollis
Yellow-breasted Chat virens
virens
Icteria virens virens
Whooping Crane
Grus americana
Eskimo Curlew
Numenius borealis
Acadian Flycatcher
Empidonax virescens
Horned Grebe
Podiceps auritus
Ivory Gull
Pagophila eburnea
Red Knot rufa
rufa
Calidris canutus rufa
Streaked Horned Lark
Eremophila alpestris strigata
Barn Owl
Tyto alba
Burrowing Owl
Athene cunicularia
Spotted Owl caurina
caurina
Strix occidentalis caurina
Mountain Plover
Charadrius montanus
Piping Plover circumcinctus
circuinctus
Charadrius melodus circumcinctus
Piping Plover melodus
melodus
Charadrius melodus melodus
King Rail
Rallus elegans
Greater Sage-Grouse urophasianus subspecies
Centrocercus urophasianus urophasianus
Williamson\'s Sapsucker
Sphyrapicus thyroideus
Pink-footed Shearwater
Ardenna creatopus
Loggerhead Shrike migrans
migrans
Lanius ludovicianus migrans
Coastal Vesper Sparrow
Pooecetes gramineus affinis
Henslow\'s Sparrow
Ammodramus henslowii
Black Swift
Cypseloides niger
Roseate Tern
Sterna dougallii
Sage Thrasher
Oreoscoptes montanus
Cerulean Warbler
Setophaga cerulea
Kirtland\'s Warbler
Dendroica kirtlandii
Prothonotary Warbler
Protonotaria citrea
Red-headed Woodpecker
Melanerpes erythrocephalus
White-headed Woodpecker
Picoides albolarvatus
Cricket Frog
Acris blanchardi
Northern Leopard Frog
Lithobates pipiens
Oregon Spotted Frog
Rana pretiosa
Allegheny Mountain Dusky Salamander
Desmognathus ochrophaeus
Allegheny Mountain Dusky Salamander
Desmognathus ochrophaeus
Eastern Tiger Salamander
Ambystoma tigrinum
Jefferson Salamander
Ambystoma jeffersonianum
Northern Dusky Salamander
Desmognathus fuscus
Small-mouthed Salamander
Ambystoma texanum
Western Tiger Salamander
Ambystoma mavortium
Fowler\'s Toad
Anaxyrus fowleri
Eastern Reptiles
Foxsnake
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
Leatherback Sea Turtle
Dermochelys coriacea
Loggerhead Sea Turtle
Caretta caretta
Five-lined Skink
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
Island Blue
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
Gattinger\'s Agalinis
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
Bird\'s-foot Violet
Viola pedata
Yellow Montane Violet praemorsa
praemorsa
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
Batwing Vinyl Lichen
Leptogium platynum
Boreal Felt Lichen
Erioderma pedicellatum
Pale-bellied Frost Lichen
Physconia subpallida
Seaside Centipede Lichen
Heterodermia sitchensis
Vole Ears Lichen
Erioderma mollissimum
Rusty Cord-moss
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
Pallid Bat
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
blacktailed prairie dog
dog
cat
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
Red Crossbill percna
percna
Loxia curvirostra percna
Olive-sided Flycatcher
Contopus cooperi
Northern Goshawk laingi
laingi
Accipiter gentilis laingi
Ross\'s Gull
Rhodostethia rosea
Ferruginous Hawk
Buteo regalis
Red Knot roselaari type
Calidris canutus roselaari
roselaari
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
Northern Saw-whet Owl brooksi
brooksi
Aegolius acadicus brooksi
Sprague\'s Pipit
Anthus spragueii
Western Screech-owl kennicottii
kennicottii
Megascops kennicottii kennicottii
Megascops kennicottii macfarlanei
Loggerhead Shrike excubitorides
excubitorides
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
Rocky Mountain Tailed Frog
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
Eastern Sand Darter
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
Verna\'s Flower Moth
Schinia verna
Dun Skipper
Euphyes vestris
Sable Island Sweat Bee
Lasioglossum sablense
Audouin\'s Night-stalking Tiger Beetle
Omus audouini
Gibson\'s Big Sand Tiger Beetle
Cicindela formosa gibsoni
Griscom’s Arnica
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
Seaside Bone
Hypogymnia heterophylla
Black-foam Lichen
Anzia colpodes
Crumpled Tarpaper Lichen
Collema coniophilum
Wrinkled Shingle Lichen
Pannaria lurida
Eastern Waterfan
Peltigera hydrothyria
Porsild\'s Bryum
Mielichhoferia macrocarpa
Alkaline Wing-nerved Moss
Pterygoneurum kozlovii
Haller\'s Apple Moss
Bartramia halleriana
Spoon-leaved Moss
Bryoandersonia illecebra
Badger taxus
taxus
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
Nuttall\'s Cottontail nuttallii
nuttallii
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
Great Blue Heron fannini
fannini
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
Rubber Boa
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
Bigmouth Buffalo
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
Brook Floater
Alasmidonta varicosa
Warty Jumping-slug
Hemphillia glandulosa
Haida Gwaii Slug
Staala gwaii
Pygmy Slug
Kootenaia burkei
Sheathed Slug
Zacoleus idahoensis
Threaded Vertigo
Nearctula sp.
Magnum Mantleslug
Magnipelta mycophaga
Wavy-rayed Lampmussel
Lampsilis fasciola
Yellow Lampmussel
Lampsilis cariosa
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
Yellow-banded Bumble Bee
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
Fernald\'s Milk-vetch
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
Peltigera gowardii"""

Air_emissions = """Air Emissions
Air
CAC
criteria air contaminant
Emissions
Construction equipment
vehicular emissions
CCME
Volatile organic compounds
Combustion
Leak
Fugitive emissions
Flaring
Incinerating
Averaging Period
incineration
Smoke
Venting
Pollute
pollutant
National Pollutant Release Inventory
Exceedance
Release
Ambient
Hydrogen sulphide
H2S
particulate
so2
sulfur dioxide
mercaptans
dust
NO2
ozone
nitrogen dioxide
oxides of nitrogen
NOX
Clean Air Act
concentration
groundlevel
ground-level
gm3
receptor"""

Greenhouse_gas_emissions = """GHG Emissions and Climate Change
greenhouse
greenhouse gas
green house gas
greenhouse gases
climate change
point source
area source
release
leak
burning
assumption
offset
off-set
International Standards Organization
ISO
ghg
ozone
global warming
Assessment of Upstream GHG Emissions
upstream
quantitative
throughput
net zero
net-zero
Environment and Climate Change Canada (ECCC)
Threshold
CO2
Carbon dioxide
CO2 equivalent
Methane
ch4
steam
hydrogen
combustion
fugitive
venting
flaring"""

Noise = """Acoustic Environment
Sound
Noise
Equipment
Frequency
Inaudible
Audible
Decibel
Notification
Noise control
Noise management
loud
quiet
db
acoustic
construction traffic
blasting
machinery
gas plant
compression station"""

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
regulatory
regulations
Federal Wetland Policy"""

Indigenous_land_water_and_air_use = """Traditional Land and Resource Use
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
settlement area
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
eskimo
Crown land
?Akisq'nuk
?Esdilagh
'Namgis
Aamjiwnaang
Fort Liard
Adams Lake
Ahousaht
Ahtahkakoop
&Abrevethélets
Aklavik
Tobacco Plains
Ahkwesáhsne Kanien'kehá:ka
Alderville
Alexander
Alexis Nakota Sioux
Tsi Del Del
Alkali Lake
Anaham
Anderson Lake
Animbiigoo Zaagi'igan Anishinaabek
Big Island
Anishinabe of Wauzhushk Onigum
St. Mary's
Ikpiarjuk
Tsiigehtchic
Aseniwuche Winewak
Ashcroft
Athabasca Chipewyan
Whitefish Lake
Attawapiskat
Aundeck-Omni-Kaning
Grise Fiord
Awaetlala
Peerless Trout
Barren Lands
Batchewana
Beardy's and Okemasis'
Bearskin Lake
Beausoleil
Beaver
Beaver Lake
Scia'new
Fort Norman
Behdzi Ahda"
Heíltsuk
Nuxalk
Big Cove
Joseph Bighead Cree
Big River
Bigstone Cree
Birch Narrows
Birdtail Sioux
Walpole Island
Stony Rapids
Little Black River
Marcel Colomb
Blood
Bloodvein
Blueberry River
Montana Cree
St'uxtews
Boothroyd
Boston Bar
Bridge River
Brokenhead Ojibway
Wet'suwet'en
Qikiqtarjuaq
Brunwick House
Tjipogtotjg
Buffalo Point
Buffalo River Dene
Oxford House
Burns Lake
Burnt Church
Tsleil Waututh
Calling Lake
Cambridge Bay
Wei Wai Kum
Stswecem'c/Xgat'tem
Canoe Lake Cree
Canupawakpa Dakota
Kinngait
Cape Mudge
Carcross/Tagish
Ceg-a-Kin
Cayoose Creek
Ch'iyáqtel
Chacachas
Chakastaypasin
Seton Lake
Champagne and Aishihik
Chawathil
Cheam
Chehalis
Chemainus
Chemawawin Cree
Cheslatta Carrier
Big Bear
Janvier
Chisasibi
Tla-o-qui-aht
Clearwater River Dene
Clyde River
Cold Lake
Coldwater
Comox
Constance Lake
Cook's Ferry
Cote
Cowessess
Cowichan
O-Chi-Chak-Ko-Sipi
Mikisew Cree
Cross Lake
Cumberland House
Dakota Plains Wahpeton
Dakota Tipi
Dauphin River
Day Star
Daylu Dena Council
Skeetchestn
Dease River
Dechi Laot'i
Deh Gah Gotie Dene
Fort Franklin
Dene Tha'
Fort Resolution
Nitinaht
Tli Cho
Doig River
Douglas
Driftpile
Duncan's
Dzawada'enuxw
Ebb and Flow
Natoaganeg
Ehattesaht
Kesyehot'ine
Enoch
Ermineskin Cree
Esdilah
Esquimalt
Fairford
Fisher River Cree
Fishing lake
Flying Dust
Fond du Lac Denesuline
Fort Churchill
Fort Folly
Fort Good Hope
Fort Albany
Fort Alexander
Smith's Landing
Fort George
Fort MacKay
Fort McMurray
Fort McPherson
Fort Nelson
Fort Rupert Band
Liidlii Kue
Fort Smith
Fort Ware
Xaxl'ip
Fox Lake Cree
Nadleh Whut'en
Frog Lake
Gamblers
Rae Lakes
Garden Hill
Gesgapegiag
Gingolx
Gitanmaax
Kitwancool
Gitg'a'ata
Kitkatla
New Aiyansh
Gitsegukla
Kitselas
Gitwangak
Gitwinksihlkw
Gitxsan
Glen Vowell
God's Lake
Manto Sipi
George Gordon
Grand Rapids
Grouard
Gwa'Sala-Nakwaxda'xw
Gwawaenuk
Hagwilget
Haisla
Halalt
Halfway River
Hatchet Lake
Hay River
Heart Lake
Hesquiaht
Tenlenaitmux
Wanipigow
Holman
Homalco
Horse Lake
Hupacasath
Huu-ay-aht
Iglulik
Indian Birch
Indian Island
Inuvik
Iqaluit
Iskut
Ministikwan
Kinonjeoshtegon
James Smith
Jean Marie River
Muskoday
K'ómoks
Ka'a'gee Tu
Ka:'yu:'k't'h'/Che:k:tles7et'h'
Kahkewistahaw
Kahnawà:ke
Kamloops
Kanaka Bar
Kanehsatà:ke
Rankin Inlet
Kaska Nation
Katzie
Poor Man or Lean Man
Keeseekoose
Riding Mountain Band
Kehewin Cree
Kelly Lake
Kelly Lake Cree
Kelly Lake Métis Settlement
Lake Harbour
Kinistin
Kispiox
Kitasoo/Xai'Xais
Kitsumkalum
Klahoose
Kluane
Kluskus
Kwanlin Dun
Kwantlen
Kwaw-Kwaw-Apilt
Kwiakah
Kwicksutaineuk-ah-kwaw-ah-mish
Kwikwetlem
Lac La Martre
Lac La Ronge
Leq'á:mel
Lakalzap
Lake Babine
Lake Cowichan
Lake Manitoba
Lake St. Martin
Lax-Kw'alaams
Lean Man
Lekwungen
Lhtakot'en
Liard
Mount Currie
T'it'q'et
Restigouche
Little Black Bear
Little Grand Rapids
Little Pine
Little Red River Cree
Little Salmon Carmacks
Little Saskatchewan
Skwlax
Long Plain
Loon River
Louis Bull
Yaqan Nukiy
Lower Nicola
Lower Similkameen
Lubicon Lake
Lucky Man
Snowdrift
Lyackson
Lytton
Madawaska Maliseet
Makwa Sahgaiehcan
Malahat
Maliseet
Mamalilikulla-Qwe'Qwa'Sot'Em
Manawan
Mathias Colomb
Matsqui
McLeod Lake
Metlakatla
Miawpukek Mi'kamawey Mawi'omi
La Nation Micmac de Gespeg
Mistawasis
Mittimatalik
Mississaugas of the New Credit
Kenhtë:ke Kanyen'keh·:ka
Montreal Lake Cree
Moose Lake
Moosomin
Moricetown
Mosquito, Grizzly Bear's Head, Lean Man
Mowachaht/Muchalaht
Muscowpetung
Utshimassit
Muskeg Lake
Muskowekwan
Musqueam
N'ahadehe
Na-Cho Nyak Dun
Nak'azdli
Nanoose
Nazko
Nee Tahi Buhn
Nekaneet
Xeni Gwet'in
Nisichawayasihk
Neskonlith
Nicomen
Nisga'a Nation
Nooaitch
Northlands Denesuline
Northwest Angle No. 33
Northwest Angle 37
Simpcw
Norway House
Nuchatlaht
Nunavut
Nuwitti
Nut Lake
Oak Lake
O'Chiese
Sioux Valley Dakota
Ocean Man
Ochapowace
Opitciwan
Odanak
Ohamil
Okanagan
Okanese
Old Masset Village Council
Willow Crees
Onion Lake
Opaskwayak Cree
O-Pipon-Na-Piwin Cree
Oregon Jack Creek
Oromocto
Osoyoos
Oujé Bougoumou Cree
Oweekeno
Pacheedaht
Pangnirtung
Pasqua
Pauingassi
Paul
Paulatuk
Pauquachin
Ts'kw'aylaxw
Peepeekisis
Peguis
Pehdzeh Ki
Selkirk
Peigan
Pelican Lake
Penelakut
Penticton
Peter Ballantyne
Peter Chapman
Peters
Pheasant Rump Nakota
Piapot
Algonquins of Pikwákanagán
Pine Creek
Piyesiw-awasis
Popkum
Poplar River
Poundmaker
Prophet River Band, Dene Tsaa Tse K'Nai
Qalipu Mi'Kmaq
Qausuittuq
Qayqayt
Qualicum
Quatsino
Rat Portage
Red Earth
Red Pheasant
Red Sucker Lake
Rolling River
Roseau River Anishinabe
Ross River
Sachs Harbour
Saddle Lake Cree
Saik'uz
Sakimay
Samahquam
Sambaah Ke Dene
Samson
Sandy Bay
Sapotaweyak
Saulteau
Saulteaux
Sawridge
Scowlitz
Seabird Island
Shishálh
Semiahmoo
Secwepemc
Shackan
Shamattawa
Shoal Lake
Shxwhá:y Village
Sîkîp Sâkahikan
Siksika
Sinixt
Siska
Six Nations
Skatin
Skawahlook
Skidegate
Skin Tyee
Skulkayn
Skownan
Skuppah
Skwah
Tla'Amin
Snuneymuxw
Soda Creek
Soowahlie
Splatsin
Tataskweyak Cree
Spuzzum
Squamish
Squiala
St. Theresa Point
Standing Buffalo Dakota
Star Blanket
Stellat'en
Yunesit'in
Stoney Nakoda
Stony Knoll
Sturgeon Lake
Sturgeon Lake Cree
Sucker Creek, AB
Sucker Creek, ON
T'exelc
Semá:th
Sunchild
Swan Lake
Swan River
Sweetgrass
Ta'an Kwäch'än
Tahltan
Takla Lake
Taku River Tlingit
Tallcree
Teetl'itzheh
Teslin Tlingit
The Key
Tl'azt'en
Tl'esqox
Tli Cho Government
Turner Island
Tobique
Valley River
Toquaht
T'Sou-ke
Tr'on dëk Hwëch'in
Ts'ueh Nda
Tsartlip
Tsawout
Tsawwassen
Tsay Keh Dene
Tseshaht
Tseycum
Tsuu T'ina
Tuktoyaktuk
Uchucklesaht
Ucluelet
Ulkatcho
Union Bar
Upper Nicola
Upper Similkameen
Vuntut Gwitchin
Wahpeton Dakota
War Lake
Wasagamack
Waswanipi Cree
Waywayseecappo
Wemotaci
Nation Huronne Wendat
Westbank
West Moberly
Wet'suwet'en Nation
Whispering Pines/Clinton
White Bear
White River
Whitecap Dakota
Atikameg
Witchekan Lake
Wolastokwik NeGoot-Gook
Wôlinak
Wood Mountain Lakota
Woodland Cree
Wrigley
Yeqwyeqwí:ws
Yale
Yekooche
Yellowknives Dene
York Factory
Columbia Lake
Alexandria
Chippewas of Sarnia
Acho Dene Koe
Sexqeltqin
Aitchelitz
Akun'kunik'
Akwesasne
Redstone Band
Esketemc
Tl'etinqox-t'in
N'quatqua
Lake Nipigon Ojibway
Anishinaabeg of Naongashiing
Aqam
Arctic Bay
Arctic Red River
Grande Cache
Atikameksheng  Anishnawbek
Sucker Creek
Ausuittuq
Da'naxda'xw
Bald Hill
Beardy's and Okemasis
Beaver Lake Cree
Beecher Bay
Tulita Dene
Bella Bella
Bella Coola
Elsipogtog
Naongashiing
Big Island Lake
Turnor Lake
Bkejwanong
Black Lake Denesuliné
Makadewaagamijiwanong
Black Sturgeon
Kainai
Bobtail
Bonaparte
Nxwisten
Broman Lake
Broughton Island
Buctouche
Bunibonibee
Ts'il kaz koh
Esgenoopetitj
Burrard
Jean Baptiste Gambler
Ikaluktutiak
Campbell River
Canoe Creek
Cape Dorset
We Wai Kai
Carry the Kettle Nakota
Sekw'el'was
Ch'yaqtel
Tsal'alh
Chi:yo:m
Sts'Ailes
Stz'uminus
Chemawawin
Chief Big Bear
Chipewyan Prairie
Clayoquot
Kangiqtugaapik
Crane River
Cree Chip
Pimicikamak
Waskahikanihk Cree Cree
Lower Post
Deadman's Creek
Wekwèti
Fort Providence
Déline
Deninu K'ue
Ditidaht
Dog Rib Rae
Xa'xtsa
Tsawataineuk
Eel Ground
English River
Ermineskin
Pinaymootang
Fisher River
Sayisi Dene
K'asho Got'ine
Sagkeeng
Fort Fitzgerald Dene
Lheidli T'enneh
Kwawkewlth
Fort Simpson
Salt River 195
Kwadacha
Fountain
Fox Lake
Fraser Lake
Gamèti
Gitanyow
Hartley Bay
Gitkxaala
Gitlakdamix
Gits'ilaasu
God's Lake Narrows
Manto Sipi Cree
Goodfish
Misipawistik Cree
Kapawe'no
Kitamaat
K'atlodeeche
High Bar
Hollow Water
Uluqsaqtuuq
Xwémalhkwu
Ohiaht
Wuskwi Sipihk
Island Lake
Jackhead
Tthe'k'ehdeli
John Smith
Comoks
Kakisa
Kyuquot
Tk'emlúps
Kangiqliniq
Kawacatoose
Keeseekoowenin
Kimmirut
Lhoosk'uz Dene
Kwikwasut'inuxw Haxwa'mis
Wha Ti
Lakahahmen
Laxgalt'Sap
Nat'oot'en
Lapatack Cree
Kawacatoose or Mosquito, Grizzly Bear's Head, Lean Man
Songhees
Red Bluff
Lil'wat
Lillooet
Listuguj
Little Shuswap Lake
Lower Kootenay
Lù'an Män Ku Dän
Lutsel K'e Dene
Maliseet of Viger
Manouane
Mathias Colomb Cree
Tsek'hene
Purtujuq
Mohawks of the Bay of Quinte
Montreal Lake
Mosakahiken
Witset
Mushuau Innu
Petequakey
Nahanni Butte
Nak'azdli Whut'en
Snaw-naw-as
Nemaiah
Nelson House
Northlands
Northwest Angle 33
Northwest Angle No. 37
North Thompson
Norway House Cree
Tlatlasikwala
Yellow Quill
Oak River
Obedjiwan
Shxw'ow'hamel
One Arrow
The Pas
O-Pipon-Na-Piwin
Oujé Bougoumou
Wuikinuvx
Pacheenaht
Panniqtuuq
Pavillion
Pelly Band
Piikani
Peter Ballantyne Cree
Skw'atels
Golden Lake
Thunderchild
Poor Man
Prophet River
Resolute Bay
Onihcikiskowapowin
Stony Creek
Zagime Anishinabek
Trout Lake
White Mud River
Sapotaweyak Cree
Sq'éwlets
Sechelt
Waterhen Lake
Sq'ewá:lxw
Sq'ewq&emacryl
Water Hen
Sliammon
Xatsu'll/Cm'etem
Spallumcheen
Tataskweyak
Stone
Young Chipeeweyan
Sukwekwin
Sumas
Tetlit Gwich'in
Toosey
Tlowitsis-mumtagila
Tootinaowaziibeeng
T'Souke
West Point
Tyendinaga
Weymontachi
Whitefish
Yakweakwioose
Akisq'nuk
Alexis Creek
Gwichya Gwich'in
Atikameksheng Anishnawbek
Tanakteuk
Kapuskwatinak
Begaee Shuhagot'ine
Black River
Xwísten
Tzeachten
Chalath
Waskahikanihk Cree
Poplar House People
Kwakiutl
God's River
Misipawistik
Ulukhaktok
Ministikwan Lake Cree
Mosquito
Pukatawagan
Pond Inlet
Mosakahiken Cree
Necoslie
Whitefish Bay
South Indian Lake
Pikwàkanagàn
Dene Tsaa Tse K'Nai
Saddle Lake
Shoal River
Skowkale
Split Lake
Williams Lake
Tlowitsis
Whitefish Lake, AB
Whitefish Lake (Atikameg)
Peerless Lake
Grizzly Bear's Head
Animakhee Wazhing
Whitefish Lake, ON"""

Electricity_and_electromagnetism = """Electromagnetism and Corona Discharge
electromagnetism
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
radio interference
television interference
foul weather
ambient conditions
240 kV"""

Proximity_to_people = """Human Occupancy and Resource Use
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
TLU Impact assessment"""

Archaeological_paleontological_historical_and_culturally_significant_sites_and_resources = """Heritage Resources
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
grading
trenching
excavating
drilling
clearing of vegetation
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
Yukon heritage resources Board
oldforest
old forest"""

Human_access_to_boats_and_waterways = """Navigation and Navigation Safety
Navigation
Nonnavigable
Navigation protection activities
Guide lines
Guide wires
Signage
Waterway
Crossing
crossing plan
impacting Navigation
dewatering of navigable waters
navigable waters
navigable waterway
navigable
navigate
watercourse
watercourse crossing
water crossing
crossing methodology
horizontal directional drilling
HDD
bridge
marine
marine terminal
waterway user
recreational waterway user
navigational use
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

Impact_to_social_and_cultural_well_being = """Social and Cultural Well-Being
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
drugs
substance abuse
stresses
household cohesion
illegal
disruptive activities
privacy
inhabited
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

Impact_to_human_health_and_viewscapes = """Human Health and Aesthetics
viewscapes
toxic
human health
nuisances
health
death
illness
disease
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
mortality
beauty
odour"""

Social_cultural_economic_infrastructure_and_services = """Infrastructure and Services
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
bridge
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
motel
construction
increased demand"""

Economic_Offsets_and_Impact = """Employment and Economy
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
high-school
college
cegep
diploma
degree
university
non-university
bachelor
certificate
Economy
wage
tips
commission
dividend
pension
child support payment
spousal support payment
jobs
monetary
salary
cash
personnel
cotractors
workers
workforce
staff
labour force
labor force
economic well-being
procurement
tax
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
self-employment
retirement
investment
contracting
contract
procurement
ordering
training
training programs
education
opportunity
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
employment
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
income
compensation
partnership
collaboration
distribution
outreach
commitment
financial
benefits
monitoring
environmental monitoring certificate program"""

Treaty_and_Indigenous_Rights = """Rights of Indigenous Peoples
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
Indigenous
Aboriginal
Native
Indian
Métis
Metis
Inuit
Inuk
Communities
Nation
Band
Tribe
Settlement
Treaty
Crown Land
Traditional Land
territory
Traditional Territory
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
infringe
exercise rights
practice rights
customs
traditions
practices
access to lands
access to resources
travel ways
land availability
resource availability
governancy system
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
Hunt
fishing
Harvest
Culturally significant
Culturally modified tree
Gather
Berries
Medicine
Berry picking
Elder
Trapping
engagement
trap
Ceremony
ceremonies
Medicinal
Cultural
First Peoples
rights-bearing
reserves
first nations
shxw’ōwhámel
lheidlit’enneh
whispering pines first nation
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
Ojibwa
Yellowknives
popkum first nation
leq’á:mel first nation
alexander first nation
samson cree first nation
o’chiese first nation
ermineskin cree nation
enoch cree nation
eskimo
?Akisq'nuk
?Esdilagh
'Namgis
Aamjiwnaang
Fort Liard
Adams Lake
Ahousaht
Ahtahkakoop
&Abrevethélets
Aklavik
Tobacco Plains
Ahkwesáhsne Kanien'kehá:ka
Alderville
Alexander
Alexis Nakota Sioux
Tsi Del Del
Alkali Lake
Anaham
Anderson Lake
Animbiigoo Zaagi'igan Anishinaabek
Big Island
Anishinabe of Wauzhushk Onigum
St. Mary's
Ikpiarjuk
Tsiigehtchic
Aseniwuche Winewak
Ashcroft
Athabasca Chipewyan
Whitefish Lake
Attawapiskat
Aundeck-Omni-Kaning
Grise Fiord
Awaetlala
Peerless Trout
Barren Lands
Batchewana
Beardy's and Okemasis'
Bearskin Lake
Beausoleil
Beaver
Beaver Lake
Scia'new
Fort Norman
Behdzi Ahda"
Heíltsuk
Nuxalk
Big Cove
Joseph Bighead Cree
Big River
Bigstone Cree
Birch Narrows
Birdtail Sioux
Walpole Island
Stony Rapids
Little Black River
Marcel Colomb
Blood
Bloodvein
Blueberry River
Montana Cree
St'uxtews
Boothroyd
Boston Bar
Bridge River
Brokenhead Ojibway
Wet'suwet'en
Qikiqtarjuaq
Brunwick House
Tjipogtotjg
Buffalo Point
Buffalo River Dene
Oxford House
Burns Lake
Burnt Church
Tsleil Waututh
Calling Lake
Cambridge Bay
Wei Wai Kum
Stswecem'c/Xgat'tem
Canoe Lake Cree
Canupawakpa Dakota
Kinngait
Cape Mudge
Carcross/Tagish
Ceg-a-Kin
Cayoose Creek
Ch'iyáqtel
Chacachas
Chakastaypasin
Seton Lake
Champagne and Aishihik
Chawathil
Cheam
Chehalis
Chemainus
Chemawawin Cree
Cheslatta Carrier
Big Bear
Janvier
Chisasibi
Tla-o-qui-aht
Clearwater River Dene
Clyde River
Cold Lake
Coldwater
Comox
Constance Lake
Cook's Ferry
Cote
Cowessess
Cowichan
O-Chi-Chak-Ko-Sipi
Mikisew Cree
Cross Lake
Cumberland House
Dakota Plains Wahpeton
Dakota Tipi
Dauphin River
Day Star
Daylu Dena Council
Skeetchestn
Dease River
Dechi Laot'i
Deh Gah Gotie Dene
Fort Franklin
Dene Tha'
Fort Resolution
Nitinaht
Tli Cho
Doig River
Douglas
Driftpile
Duncan's
Dzawada'enuxw
Ebb and Flow
Natoaganeg
Ehattesaht
Kesyehot'ine
Enoch
Ermineskin Cree
Esdilah
Esquimalt
Fairford
Fisher River Cree
Fishing lake
Flying Dust
Fond du Lac Denesuline
Fort Churchill
Fort Folly
Fort Good Hope
Fort Albany
Fort Alexander
Smith's Landing
Fort George
Fort MacKay
Fort McMurray
Fort McPherson
Fort Nelson
Fort Rupert Band
Liidlii Kue
Fort Smith
Fort Ware
Xaxl'ip
Fox Lake Cree
Nadleh Whut'en
Frog Lake
Gamblers
Rae Lakes
Garden Hill
Gesgapegiag
Gingolx
Gitanmaax
Kitwancool
Gitg'a'ata
Kitkatla
New Aiyansh
Gitsegukla
Kitselas
Gitwangak
Gitwinksihlkw
Gitxsan
Glen Vowell
God's Lake
Manto Sipi
George Gordon
Grand Rapids
Grouard
Gwa'Sala-Nakwaxda'xw
Gwawaenuk
Hagwilget
Haisla
Halalt
Halfway River
Hatchet Lake
Hay River
Heart Lake
Hesquiaht
Tenlenaitmux
Wanipigow
Holman
Homalco
Horse Lake
Hupacasath
Huu-ay-aht
Iglulik
Indian Birch
Indian Island
Inuvik
Iqaluit
Iskut
Ministikwan
Kinonjeoshtegon
James Smith
Jean Marie River
Muskoday
K'ómoks
Ka'a'gee Tu
Ka:'yu:'k't'h'/Che:k:tles7et'h'
Kahkewistahaw
Kahnawà:ke
Kamloops
Kanaka Bar
Kanehsatà:ke
Rankin Inlet
Kaska Nation
Katzie
Poor Man or Lean Man
Keeseekoose
Riding Mountain Band
Kehewin Cree
Kelly Lake
Kelly Lake Cree
Kelly Lake Métis Settlement
Lake Harbour
Kinistin
Kispiox
Kitasoo/Xai'Xais
Kitsumkalum
Klahoose
Kluane
Kluskus
Kwanlin Dun
Kwantlen
Kwaw-Kwaw-Apilt
Kwiakah
Kwicksutaineuk-ah-kwaw-ah-mish
Kwikwetlem
Lac La Martre
Lac La Ronge
Leq'á:mel
Lakalzap
Lake Babine
Lake Cowichan
Lake Manitoba
Lake St. Martin
Lax-Kw'alaams
Lean Man
Lekwungen
Lhtakot'en
Liard
Mount Currie
T'it'q'et
Restigouche
Little Black Bear
Little Grand Rapids
Little Pine
Little Red River Cree
Little Salmon Carmacks
Little Saskatchewan
Skwlax
Long Plain
Loon River
Louis Bull
Yaqan Nukiy
Lower Nicola
Lower Similkameen
Lubicon Lake
Lucky Man
Snowdrift
Lyackson
Lytton
Madawaska Maliseet
Makwa Sahgaiehcan
Malahat
Maliseet
Mamalilikulla-Qwe'Qwa'Sot'Em
Manawan
Mathias Colomb
Matsqui
McLeod Lake
Metlakatla
Miawpukek Mi'kamawey Mawi'omi
La Nation Micmac de Gespeg
Mistawasis
Mittimatalik
Mississaugas of the New Credit
Kenhtë:ke Kanyen'keh·:ka
Montreal Lake Cree
Moose Lake
Moosomin
Moricetown
Mosquito, Grizzly Bear's Head, Lean Man
Mowachaht/Muchalaht
Muscowpetung
Utshimassit
Muskeg Lake
Muskowekwan
Musqueam
N'ahadehe
Na-Cho Nyak Dun
Nak'azdli
Nanoose
Nazko
Nee Tahi Buhn
Nekaneet
Xeni Gwet'in
Nisichawayasihk
Neskonlith
Nicomen
Nisga'a Nation
Nooaitch
Northlands Denesuline
Northwest Angle No. 33
Northwest Angle 37
Simpcw
Norway House
Nuchatlaht
Nunavut
Nuwitti
Nut Lake
Oak Lake
O'Chiese
Sioux Valley Dakota
Ocean Man
Ochapowace
Opitciwan
Odanak
Ohamil
Okanagan
Okanese
Old Masset Village Council
Willow Crees
Onion Lake
Opaskwayak Cree
O-Pipon-Na-Piwin Cree
Oregon Jack Creek
Oromocto
Osoyoos
Oujé Bougoumou Cree
Oweekeno
Pacheedaht
Pangnirtung
Pasqua
Pauingassi
Paul
Paulatuk
Pauquachin
Ts'kw'aylaxw
Peepeekisis
Peguis
Pehdzeh Ki
Selkirk
Peigan
Pelican Lake
Penelakut
Penticton
Peter Ballantyne
Peter Chapman
Peters
Pheasant Rump Nakota
Piapot
Algonquins of Pikwákanagán
Pine Creek
Piyesiw-awasis
Popkum
Poplar River
Poundmaker
Prophet River Band, Dene Tsaa Tse K'Nai
Qalipu Mi'Kmaq
Qausuittuq
Qayqayt
Qualicum
Quatsino
Rat Portage
Red Earth
Red Pheasant
Red Sucker Lake
Rolling River
Roseau River Anishinabe
Ross River
Sachs Harbour
Saddle Lake Cree
Saik'uz
Sakimay
Samahquam
Sambaah Ke Dene
Samson
Sandy Bay
Sapotaweyak
Saulteau
Saulteaux
Sawridge
Scowlitz
Seabird Island
Shishálh
Semiahmoo
Secwepemc
Shackan
Shamattawa
Shoal Lake
Shxwhá:y Village
Sîkîp Sâkahikan
Siksika
Sinixt
Siska
Six Nations
Skatin
Skawahlook
Skidegate
Skin Tyee
Skulkayn
Skownan
Skuppah
Skwah
Tla'Amin
Snuneymuxw
Soda Creek
Soowahlie
Splatsin
Tataskweyak Cree
Spuzzum
Squamish
Squiala
St. Theresa Point
Standing Buffalo Dakota
Star Blanket
Stellat'en
Yunesit'in
Stoney Nakoda
Stony Knoll
Sturgeon Lake
Sturgeon Lake Cree
Sucker Creek, AB
Sucker Creek, ON
T'exelc
Semá:th
Sunchild
Swan Lake
Swan River
Sweetgrass
Ta'an Kwäch'än
Tahltan
Takla Lake
Taku River Tlingit
Tallcree
Teetl'itzheh
Teslin Tlingit
The Key
Tl'azt'en
Tl'esqox
Tli Cho Government
Turner Island
Tobique
Valley River
Toquaht
T'Sou-ke
Tr'on dëk Hwëch'in
Ts'ueh Nda
Tsartlip
Tsawout
Tsawwassen
Tsay Keh Dene
Tseshaht
Tseycum
Tsuu T'ina
Tuktoyaktuk
Uchucklesaht
Ucluelet
Ulkatcho
Union Bar
Upper Nicola
Upper Similkameen
Vuntut Gwitchin
Wahpeton Dakota
War Lake
Wasagamack
Waswanipi Cree
Waywayseecappo
Wemotaci
Nation Huronne Wendat
Westbank
West Moberly
Wet'suwet'en Nation
Whispering Pines/Clinton
White Bear
White River
Whitecap Dakota
Atikameg
Witchekan Lake
Wolastokwik NeGoot-Gook
Wôlinak
Wood Mountain Lakota
Woodland Cree
Wrigley
Yeqwyeqwí:ws
Yale
Yekooche
Yellowknives Dene
York Factory
Columbia Lake
Alexandria
Chippewas of Sarnia
Acho Dene Koe
Sexqeltqin
Aitchelitz
Akun'kunik'
Akwesasne
Redstone Band
Esketemc
Tl'etinqox-t'in
N'quatqua
Lake Nipigon Ojibway
Anishinaabeg of Naongashiing
Aqam
Arctic Bay
Arctic Red River
Grande Cache
Atikameksheng  Anishnawbek
Sucker Creek
Ausuittuq
Da'naxda'xw
Bald Hill
Beardy's and Okemasis
Beaver Lake Cree
Beecher Bay
Tulita Dene
Bella Bella
Bella Coola
Elsipogtog
Naongashiing
Big Island Lake
Turnor Lake
Bkejwanong
Black Lake Denesuliné
Makadewaagamijiwanong
Black Sturgeon
Kainai
Bobtail
Bonaparte
Nxwisten
Broman Lake
Broughton Island
Buctouche
Bunibonibee
Ts'il kaz koh
Esgenoopetitj
Burrard
Jean Baptiste Gambler
Ikaluktutiak
Campbell River
Canoe Creek
Cape Dorset
We Wai Kai
Carry the Kettle Nakota
Sekw'el'was
Ch'yaqtel
Tsal'alh
Chi:yo:m
Sts'Ailes
Stz'uminus
Chemawawin
Chief Big Bear
Chipewyan Prairie
Clayoquot
Kangiqtugaapik
Crane River
Cree Chip
Pimicikamak
Waskahikanihk Cree Cree
Lower Post
Deadman's Creek
Wekwèti
Fort Providence
Déline
Deninu K'ue
Ditidaht
Dog Rib Rae
Xa'xtsa
Tsawataineuk
Eel Ground
English River
Ermineskin
Pinaymootang
Fisher River
Sayisi Dene
K'asho Got'ine
Sagkeeng
Fort Fitzgerald Dene
Lheidli T'enneh
Kwawkewlth
Fort Simpson
Salt River 195
Kwadacha
Fountain
Fox Lake
Fraser Lake
Gamèti
Gitanyow
Hartley Bay
Gitkxaala
Gitlakdamix
Gits'ilaasu
God's Lake Narrows
Manto Sipi Cree
Goodfish
Misipawistik Cree
Kapawe'no
Kitamaat
K'atlodeeche
High Bar
Hollow Water
Uluqsaqtuuq
Xwémalhkwu
Ohiaht
Wuskwi Sipihk
Island Lake
Jackhead
Tthe'k'ehdeli
John Smith
Comoks
Kakisa
Kyuquot
Tk'emlúps
Kangiqliniq
Kawacatoose
Keeseekoowenin
Kimmirut
Lhoosk'uz Dene
Kwikwasut'inuxw Haxwa'mis
Wha Ti
Lakahahmen
Laxgalt'Sap
Nat'oot'en
Lapatack Cree
Kawacatoose or Mosquito, Grizzly Bear's Head, Lean Man
Songhees
Red Bluff
Lil'wat
Lillooet
Listuguj
Little Shuswap Lake
Lower Kootenay
Lù'an Män Ku Dän
Lutsel K'e Dene
Maliseet of Viger
Manouane
Mathias Colomb Cree
Tsek'hene
Purtujuq
Mohawks of the Bay of Quinte
Montreal Lake
Mosakahiken
Witset
Mushuau Innu
Petequakey
Nahanni Butte
Nak'azdli Whut'en
Snaw-naw-as
Nemaiah
Nelson House
Northlands
Northwest Angle 33
Northwest Angle No. 37
North Thompson
Norway House Cree
Tlatlasikwala
Yellow Quill
Oak River
Obedjiwan
Shxw'ow'hamel
One Arrow
The Pas
O-Pipon-Na-Piwin
Oujé Bougoumou
Wuikinuvx
Pacheenaht
Panniqtuuq
Pavillion
Pelly Band
Piikani
Peter Ballantyne Cree
Skw'atels
Golden Lake
Thunderchild
Poor Man
Prophet River
Resolute Bay
Onihcikiskowapowin
Stony Creek
Zagime Anishinabek
Trout Lake
White Mud River
Sapotaweyak Cree
Sq'éwlets
Sechelt
Waterhen Lake
Sq'ewá:lxw
Sq'ewq&emacryl
Water Hen
Sliammon
Xatsu'll/Cm'etem
Spallumcheen
Tataskweyak
Stone
Young Chipeeweyan
Sukwekwin
Sumas
Tetlit Gwich'in
Toosey
Tlowitsis-mumtagila
Tootinaowaziibeeng
T'Souke
West Point
Tyendinaga
Weymontachi
Whitefish
Yakweakwioose
Akisq'nuk
Alexis Creek
Gwichya Gwich'in
Atikameksheng Anishnawbek
Tanakteuk
Kapuskwatinak
Begaee Shuhagot'ine
Black River
Xwísten
Tzeachten
Chalath
Waskahikanihk Cree
Poplar House People
Kwakiutl
God's River
Misipawistik
Ulukhaktok
Ministikwan Lake Cree
Mosquito
Pukatawagan
Pond Inlet
Mosakahiken Cree
Necoslie
Whitefish Bay
South Indian Lake
Pikwàkanagàn
Dene Tsaa Tse K'Nai
Saddle Lake
Shoal River
Skowkale
Split Lake
Williams Lake
Tlowitsis
Whitefish Lake, AB
Whitefish Lake (Atikameg)
Peerless Lake
Grizzly Bear's Head
Animakhee Wazhing
Whitefish Lake, ON"""

keywords = [Landscape_terrain_and_weather, 
            Soil,
            Plants,
            Water,
            Fish,
            Wetlands,
            Wildlife,
            Species_at_Risk,
            Greenhouse_gas_emissions,
            Air_emissions,
            Noise,
            Electricity_and_electromagnetism,
            Proximity_to_people,
            Archaeological_paleontological_historical_and_culturally_significant_sites_and_resources,
            Human_access_to_boats_and_waterways,
            Indigenous_land_water_and_air_use,
            Impact_to_social_and_cultural_well_being,
            Impact_to_human_health_and_viewscapes,
            Social_cultural_economic_infrastructure_and_services,
            Economic_Offsets_and_Impact,
            Environmental_Obligations,
            Treaty_and_Indigenous_Rights]

keywords = [x.lower().split("\n") for x in keywords]

stemmer = PorterStemmer()

for i, label_keywords in enumerate(keywords):
    stemmed_words = []
    for word in label_keywords:
        token_words = word_tokenize(word)
        stemmed_tokens = [stemmer.stem(t) for t in token_words if t not in stopwords.words("english")]
        stemmed_words.append(" ".join(stemmed_tokens))
    keywords[i] = stemmed_words

print(keywords[0], keywords[1], keywords[2], keywords[3], keywords[4], keywords[5], keywords[6], keywords[7], keywords[8])

with open("keywords.pkl", "wb") as f:
    pickle.dump(keywords, f)