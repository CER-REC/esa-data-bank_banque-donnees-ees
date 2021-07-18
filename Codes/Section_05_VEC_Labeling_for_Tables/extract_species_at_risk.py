import re

species_at_risk_string = """Badger jacksoni subspecies, American (Taxidea taxus jacksoni)

Blaireau d’Amérique de la sous-espèce jacksoni

Badger jeffersonii subspecies, American (Taxidea taxus jeffersonii) Eastern population

Blaireau d’Amérique de la sous-espèce jeffersonii population de l’Est

Badger jeffersonii subspecies, American (Taxidea taxus jeffersonii) Western population

Blaireau d’Amérique de la sous-espèce jeffersonii population de l’Ouest

Bat, Tri-coloured (Perimyotis subflavus)

Pipistrelle de l’Est

Caribou, Peary (Rangifer tarandus pearyi)

Caribou de Peary

Caribou, Woodland (Rangifer tarandus caribou) Atlantic — Gaspésie population

Caribou des bois population de la Gaspésie — Atlantique

Kangaroo Rat, Ord’s (Dipodomys ordii)

Rat kangourou d’Ord

Marmot, Vancouver Island (Marmota vancouverensis)

Marmotte de l’île Vancouver

Mole, Townsend’s (Scapanus townsendii)

Taupe de Townsend

Mouse dychei subspecies, Western Harvest (Reithrodontomys megalotis dychei)

Souris des moissons de la sous-espèce dychei

Myotis, Little Brown (Myotis lucifugus)

Petite chauve-souris brune

Myotis, Northern (Myotis septentrionalis)

Chauve-souris nordique

Seal Lacs des Loups Marins subspecies, Harbour (Phoca vitulina mellonae)

Phoque commun de la sous-espèce des Lacs des Loups Marins

Shrew, Pacific Water (Sorex bendirii)

Musaraigne de Bendire

Whale, Beluga (Delphinapterus leucas) St. Lawrence Estuary population

Béluga population de l’estuaire du Saint-Laurent

Whale, Blue (Balaenoptera musculus) Atlantic population

Rorqual bleu population de l’Atlantique

Whale, Blue (Balaenoptera musculus) Pacific population

Rorqual bleu population du Pacifique

Whale, Killer (Orcinus orca) Northeast Pacific southern resident population

Épaulard population résidente du sud du Pacifique Nord-Est

Whale, North Atlantic Right (Eubalaena glacialis)

Baleine noire de l’Atlantique Nord

Whale, North Pacific Right (Eubalaena japonica)

Baleine noire du Pacifique Nord

Whale, Northern Bottlenose (Hyperoodon ampullatus) Scotian Shelf population

Baleine à bec commune, population du plateau néo-écossais

Whale, Sei (Balaenoptera borealis) Pacific population

Rorqual boréal population du Pacifique

Birds
Bobwhite, Northern (Colinus virginianus)

Colin de Virginie

Chat auricollis subspecies, Yellow-breasted (Icteria virens auricollis) Southern Mountain population

Paruline polyglotte de la sous-espèce auricollis population des montagnes du Sud

Chat virens subspecies, Yellow-breasted (Icteria virens virens)

Paruline polyglotte de la sous-espèce virens

Crane, Whooping (Grus americana)

Grue blanche

Curlew, Eskimo (Numenius borealis)

Courlis esquimau

Flycatcher, Acadian (Empidonax virescens)

Moucherolle vert

Grebe, Horned (Podiceps auritus) Magdalen Islands population

Grèbe esclavon population des îles de la Madeleine

Gull, Ivory (Pagophila eburnea)

Mouette blanche

Knot rufa subspecies, Red (Calidris canutus rufa)

Bécasseau maubèche de la sous-espèce rufa

Lark, Streaked Horned (Eremophila alpestris strigata)

Alouette hausse-col de la sous-espèce strigata

Owl, Barn (Tyto alba) Eastern population

Effraie des clochers population de l’Est

Owl, Burrowing (Athene cunicularia)

Chevêche des terriers

Owl caurina subspecies, Spotted (Strix occidentalis caurina)

Chouette tachetée de la sous-espèce caurina

Plover, Mountain (Charadrius montanus)

Pluvier montagnard

Plover circumcinctus subspecies, Piping (Charadrius melodus circumcinctus)

Pluvier siffleur de la sous-espèce circumcinctus

Plover melodus subspecies, Piping (Charadrius melodus melodus)

Pluvier siffleur de la sous-espèce melodus

Rail, King (Rallus elegans)

Râle élégant

Sage-Grouse urophasianus subspecies, Greater (Centrocercus urophasianus urophasianus)

Tétras des armoises de la sous-espèce urophasianus

Sapsucker, Williamson’s (Sphyrapicus thyroideus)

Pic de Williamson

Shearwater, Pink-footed (Ardenna creatopus)

Puffin à pieds roses

Shrike migrans subspecies, Loggerhead (Lanius ludovicianus migrans)

Pie-grièche migratrice de la sous-espèce migrans

Sparrow, Coastal Vesper (Pooecetes gramineus affinis)

Bruant vespéral de la sous-espèce affinis

Sparrow, Henslow’s (Ammodramus henslowii)

Bruant de Henslow

Swift, Black (Cypseloides niger)

Martinet sombre

Tern, Roseate (Sterna dougallii)

Sterne de Dougall

Thrasher, Sage (Oreoscoptes montanus)

Moqueur des armoises

Warbler, Cerulean (Setophaga cerulea)

Paruline azurée

Warbler, Kirtland’s (Dendroica kirtlandii)

Paruline de Kirtland

Warbler, Prothonotary (Protonotaria citrea)

Paruline orangée

Woodpecker, Red-headed (Melanerpes erythrocephalus)

Pic à tête rouge

Woodpecker, White-headed (Picoides albolarvatus)

Pic à tête blanche

Amphibians
Frog, Blanchard’s Cricket (Acris blanchardi)

Rainette grillon de Blanchard

Frog, Northern Leopard (Lithobates pipiens) Rocky Mountain population

Grenouille léopard population des Rocheuses

Frog, Oregon Spotted (Rana pretiosa)

Grenouille maculée de l’Oregon

Salamander, Allegheny Mountain Dusky (Desmognathus ochrophaeus) Appalachian population

Salamandre sombre des montagnes population des Appalaches

Salamander, Allegheny Mountain Dusky (Desmognathus ochrophaeus) Carolinian population

Salamandre sombre des montagnes population carolinienne

Salamander, Eastern Tiger (Ambystoma tigrinum) Prairie population

Salamandre tigrée de l’Est population des Prairies

Salamander, Jefferson (Ambystoma jeffersonianum)

Salamandre de Jefferson

Salamander, Northern Dusky (Desmognathus fuscus) Carolinian population

Salamandre sombre du Nord population carolinienne

Salamander, Small-mouthed (Ambystoma texanum)

Salamandre à nez court

Salamander, Western Tiger (Ambystoma mavortium) Southern Mountain population

Salamandre tigrée de l’Ouest population des montagnes du Sud

Toad, Fowler’s (Anaxyrus fowleri)

Crapaud de Fowler

Reptiles
Foxsnake, Eastern (Pantherophis gloydi) Carolinian population

Couleuvre fauve de l’Est population carolinienne

Foxsnake, Eastern (Pantherophis gloydi) Great Lakes / St. Lawrence population

Couleuvre fauve de l’Est population des Grands Lacs et du Saint-Laurent

Gartersnake, Butler’s (Thamnophis butleri)

Couleuvre à petite tête

Lizard, Greater Short-horned (Phrynosoma hernandesi)

Grand iguane à petites cornes

Massasauga (Sistrurus catenatus) Carolinian population

Massasauga population carolinienne

Nightsnake, Desert (Hypsiglena chlorophaea)

Couleuvre nocturne du désert

Queensnake (Regina septemvittata)

Couleuvre royale

Racer, Blue (Coluber constrictor foxii)

Couleuvre agile bleue

Ratsnake, Gray (Pantherophis spiloides) Carolinian population

Couleuvre obscure population carolinienne

Sea Turtle, Leatherback (Dermochelys coriacea) Atlantic population

Tortue luth population de l’Atlantique

Sea Turtle, Leatherback (Dermochelys coriacea) Pacific population

Tortue luth population du Pacifique

Sea Turtle, Loggerhead (Caretta caretta)

Tortue caouanne

Skink, Five-lined (Plestiodon fasciatus) Carolinian population

Scinque pentaligne population carolinienne

Snake, Sharp-tailed (Contia tenuis)

Couleuvre à queue fine

Softshell, Spiny (Apalone spinifera)

Tortue molle à épines

Turtle, Blanding’s (Emydoidea blandingii) Nova Scotia population

Tortue mouchetée population de la Nouvelle-Écosse

Turtle, Spotted (Clemmys guttata)

Tortue ponctuée

Turtle, Western Painted (Chrysemys picta bellii) Pacific Coast population

Tortue peinte de l’Ouest, population de la côte du Pacifique

Fish
Bass, Striped (Morone saxatilis) St. Lawrence River population

Bar rayé population du fleuve Saint-Laurent

Chub, Silver (Macrhybopsis storeriana) Great Lakes – Upper St. Lawrence populations

Méné à grandes écailles populations des Grands Lacs et du haut Saint-Laurent

Chubsucker, Lake (Erimyzon sucetta)

Sucet de lac

Cisco, Shortnose (Coregonus reighardi)

Cisco à museau court

Cisco, Spring (Coregonus sp.)

Cisco de printemps

Dace, Nooksack (Rhinichthys cataractae ssp.)

Naseux de la Nooksack

Dace, Redside (Clinostomus elongatus)

Méné long

Dace, Speckled (Rhinichthys osculus)

Naseux moucheté

Darter, Channel (Percina copelandi) Lake Erie populations

Fouille-roche gris populations du lac Érié

Darter, Channel (Percina copelandi) Lake Ontario populations

Fouille-roche gris populations du lac Ontario

Gar, Spotted (Lepisosteus oculatus)

Lépisosté tacheté

Lamprey, Western Brook (Lampetra richardsoni) Morrison Creek population

Lamproie de l’ouest population du ruisseau Morrison

Madtom, Northern (Noturus stigmosus)

Chat-fou du Nord

Redhorse, Copper (Moxostoma hubbsi)

Chevalier cuivré

Salmon, Atlantic (Salmo salar) Inner Bay of Fundy population

Saumon atlantique population de l’intérieur de la baie de Fundy

Shark, Basking (Cetorhinus maximus) Pacific population

Pèlerin population du Pacifique

Shark, White (Carcharodon carcharias) Atlantic population

Grand requin blanc population de l’Atlantique

Shiner, Carmine (Notropis percobromus)

Tête carminée

Smelt, Rainbow (Osmerus mordax) Lake Utopia large-bodied population

Éperlan arc-en-ciel population d’individus de grande taille du lac Utopia

Smelt, Rainbow (Osmerus mordax) Lake Utopia small-bodied population

Éperlan arc-en-ciel population d’individus de petite taille du lac Utopia

Stickleback, Enos Lake Benthic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines benthique du lac Enos

Stickleback, Enos Lake Limnetic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines limnétique du lac Enos

Stickleback, Misty Lake Lentic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines lentique du lac Misty

Stickleback, Misty Lake Lotic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines lotique du lac Misty

Stickleback, Paxton Lake Benthic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines benthique du lac Paxton

Stickleback, Paxton Lake Limnetic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines limnétique du lac Paxton

Stickleback, Vananda Creek Benthic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines benthique du ruisseau Vananda

Stickleback, Vananda Creek Limnetic Threespine (Gasterosteus aculeatus)

Épinoche à trois épines limnétique du ruisseau Vananda

Sturgeon, White (Acipenser transmontanus) Nechako River population

Esturgeon blanc population de la rivière Nechako

Sturgeon, White (Acipenser transmontanus) Upper Columbia River population

Esturgeon blanc population du cours supérieur du Columbia

Sturgeon, White (Acipenser transmontanus) Upper Fraser River population

Esturgeon blanc population du cours supérieur du Fraser

Sturgeon, White (Acipenser transmontanus) Upper Kootenay River population

Esturgeon blanc population du cours supérieur de la rivière Kootenay

Trout, Rainbow (Oncorhynchus mykiss) Athabasca River populations

Truite arc-en-ciel populations de la rivière Athabasca

Whitefish, Atlantic (Coregonus huntsmani)

Corégone de l’Atlantique

Molluscs
Abalone, Northern (Haliotis kamtschatkana)

Ormeau nordique

Bean, Rayed (Villosa fabalis)

Villeuse haricot

Fawnsfoot (Truncilla donaciformis)

Troncille pied-de-faon

Forestsnail, Broad-banded (Allogona profunda)

Escargot-forestier écharge

Forestsnail, Oregon (Allogona townsendiana)

Escargot-forestier de Townsend

Globelet, Proud (Patera pennsylvanica)

Patère de Pennsylvanie

Hickorynut (Obovaria olivaria)

Obovarie olivâtre

Hickorynut, Round (Obovaria subrotunda)

Obovarie ronde

Kidneyshell (Ptychobranchus fasciolaris)

Ptychobranche réniforme

Lilliput (Toxolasma parvum)

Toxolasme nain

Mussel, Salamander (Simpsonaias ambigua)

Mulette du Necture

Physa, Hotwater (Physella wrighti)

Physe d’eau chaude

Pigtoe, Round (Pleurobema sintoxia)

Pleurobème écarlate

Riffleshell, Northern (Epioblasma torulosa rangiana)

Épioblasme ventrue

Snail, Banff Springs (Physella johnsoni)

Physe des fontaines de Banff

Snuffbox (Epioblasma triquetra)

Épioblasme tricorne

Arthropods
Blue, Island (Plebejus saepiolus insulanus)

Bleu insulaire

Borer, Aweme (Papaipema aweme)

Perce-tige d’Aweme

Borer, Hoptree (Prays atomocella)

Perceur du ptéléa

Buckmoth, Bogbean (Hemileuca sp.)

Hémileucin du ményanthe

Bumble Bee, Gypsy Cuckoo (Bombus bohemicus)

Psithyre bohémien

Bumble Bee, Rusty-patched (Bombus affinis)

Bourdon à tache rousse

Checkerspot, Taylor’s (Euphydryas editha taylori)

Damier de Taylor

Clubtail, Olive (Stylurus olivaceus)

Gomphe olive

Clubtail, Rapids (Gomphus quadricolor)

Gomphe des rapides

Clubtail, Riverine (Stylurus amnicola) Great Lakes Plains population

Gomphe riverain population des plaines des Grands Lacs

Clubtail, Skillet (Gomphus ventricosus)

Gomphe ventru

Crawling Water Beetle, Hungerford’s (Brychius hungerfordi)

Haliplide de Hungerford

Cuckoo Bee, Macropis (Epeoloides pilosulus)

Abeille-coucou de Macropis

Diving Beetle, Bert’s Predaceous (Sanfilippodytes bertae)

Hydropore de Bertha

Duskywing, Eastern Persius (Erynnis persius persius)

Hespérie Persius de l’Est

Efferia, Okanagan (Efferia okanagana)

Asile de l’Okanagan

Emerald, Hine’s (Somatochlora hineana)

Cordulie de Hine

Flower Moth, White (Schinia bimatris)

Héliotin blanc satiné

Gold-edged Gem (Schinia avemensis)

Héliotin d’Aweme

Hairstreak, Behr’s (Satyrium behrii)

Porte-queue de Behr

Hairstreak, Half-moon (Satyrium semiluna)

Porte-queue demi-lune

Metalmark, Mormon (Apodemia mormo) Southern Mountain population

Mormon population des montagnes du Sud

Moth, Dusky Dune (Copablepharon longipenne)

Noctuelle sombre des dunes

Moth, Edwards’ Beach (Anarta edwardsii)

Noctuelle d’Edwards

Moth, Five-spotted Bogus Yucca (Prodoxus quinquepunctellus)

Fausse-teigne à cinq points du yucca

Moth, Non-pollinating Yucca (Tegeticula corruptrix)

Teigne tricheuse du yucca

Moth, Sand-verbena (Copablepharon fuscum)

Noctuelle de l’abronie

Moth, Yucca (Tegeticula yuccasella)

Teigne du yucca

Ringlet, Maritime (Coenonympha nipisiquit)

Satyre fauve des Maritimes

Skipper, Dakota (Hesperia dacotae)

Hespérie du Dakota

Skipperling, Poweshiek (Oarisma poweshiek)

Hespérie de Poweshiek

Skipper, Ottoe (Hesperia ottoe)

Hespérie Ottoé

Sun Moth, False-foxglove (Pyrrhia aurantiago)

Héliotin orangé

Tiger Beetle, Cobblestone (Cicindela marginipennis)

Cicindèle des galets

Tiger Beetle, Northern Barrens (Cicindela patruela)

Cicindèle verte des pinèdes

Tiger Beetle, Wallis’ Dark Saltflat (Cicindela parowana wallisi)

Cicindèle de Wallis

Plants
Agalinis, Gattinger’s (Agalinis gattingeri)

Gérardie de Gattinger

Agalinis, Rough (Agalinis aspera)

Gérardie rude

Agalinis, Skinner’s (Agalinis skinneriana)

Gérardie de Skinner

Ammannia, Scarlet (Ammannia robusta)

Ammannie robuste

Aster, Short-rayed Alkali (Symphyotrichum frondosum)

Aster feuillu

Avens, Eastern Mountain (Geum peckii)

Benoîte de Peck

Balsamroot, Deltoid (Balsamorhiza deltoidea)

Balsamorhize à feuilles deltoïdes

Beakrush, Tall (Rhynchospora macrostachya)

Rhynchospore à gros épillets

Birch, Cherry (Betula lenta)

Bouleau flexible

Bluehearts (Buchnera americana)

Buchnéra d’Amérique

Braya, Fernald’s (Braya fernaldii)

Braya de Fernald

Braya, Hairy (Braya pilosa)

Braya poilu

Braya, Long’s (Braya longii)

Braya de Long

Bugbane, Tall (Actaea elata)

Cimicaire élevée

Bulrush, Bashful (Trichophorum planifolium)

Trichophore à feuilles plates

Bush-clover, Slender (Lespedeza virginica)

Lespédèze de Virginie

Buttercup, California (Ranunculus californicus)

Renoncule de Californie

Buttercup, Water-plantain (Ranunculus alismifolius)

Renoncule à feuilles d’alisme

Butternut (Juglans cinerea)

Noyer cendré

Cactus, Eastern Prickly Pear (Opuntia humifusa)

Oponce de l’Est

Campion, Spalding’s (Silene spaldingii)

Silène de Spalding

Catchfly, Coastal Scouler’s (Silene scouleri grandis)

Grand silène de Scouler

Centaury, Muhlenberg’s (Centaurium muehlenbergii)

Petite-centaurée de Muhlenberg

Chestnut, American (Castanea dentata)

Châtaignier d’Amérique

Colicroot (Aletris farinosa)

Alétris farineux

Collomia, Slender (Collomia tenella)

Collomia délicat

Columbo, American (Frasera caroliniensis)

Frasère de Caroline

Coreopsis, Pink (Coreopsis rosea)

Coréopsis rose

Dogwood, Eastern Flowering (Cornus florida)

Cornouiller fleuri

Evening-primrose, Contorted-pod (Camissonia contorta)

Onagre à fruits tordus

Fern, Southern Maidenhair (Adiantum capillus-veneris)

Adiante cheveux-de-Vénus

Fringed-orchid, Eastern Prairie (Platanthera leucophaea)

Platanthère blanchâtre de l’Est

Fringed-orchid, Western Prairie (Platanthera praeclara)

Platanthère blanchâtre de l’Ouest

Gentian, Plymouth (Sabatia kennedyana)

Sabatie de Kennedy

Gentian, White Prairie (Gentiana alba)

Gentiane blanche

Ginseng, American (Panax quinquefolius)

Ginseng à cinq folioles

Goat’s-rue, Virginia (Tephrosia virginiana)

Téphrosie de Virginie

Goldenrod, Showy (Solidago speciosa) Great Lakes Plains population

Verge d’or voyante population des plaines des Grands Lacs

Goldfields, Rayless (Lasthenia glaberrima)

Lasthénie glabre

Grass, Forked Three-awned (Aristida basiramea)

Aristide à rameaux basilaires

Ironweed, Fascicled (Vernonia fasciculata)

Vernonie fasciculée

Lewisia, Tweedy’s (Lewisiopsis tweedyi)

Léwisie de Tweedy

Lipocarpha, Small-flowered (Lipocarpha micrantha)

Lipocarphe à petites fleurs

Lotus, Seaside Birds-foot (Lotus formosissimus)

Lotier splendide

Lousewort, Furbish’s (Pedicularis furbishiae)

Pédiculaire de Furbish

Lupine, Dense-flowered (Lupinus densiflorus)

Lupin densiflore

Lupine, Prairie (Lupinus lepidus)

Lupin élégant

Lupine, Streambank (Lupinus rivularis)

Lupin des ruisseaux

Mallow, Virginia (Sida hermaphrodita)

Mauve de Virginie

Meconella, White (Meconella oregana)

Méconelle d’Orégon

Microseris, Coast (Microseris bigelovii)

Microséris de Bigelow

Milkwort, Pink (Polygala incarnata)

Polygale incarnat

Mountain-mint, Hoary (Pycnanthemum incanum)

Pycnanthème gris

Mulberry, Red (Morus rubra)

Mûrier rouge

Orchid, Phantom (Cephalanthera austiniae)

Céphalanthère d’Austin

Owl-clover, Bearded (Triphysaria versicolor)

Triphysaire versicolore

Owl-clover, Grand Coulee (Orthocarpus barbatus)

Orthocarpe barbu

Owl-clover, Rosy (Orthocarpus bracteosus)

Orthocarpe à épi feuillu

Owl-clover, Victoria’s (Castilleja victoriae)

Castilléjie de Victoria

Paintbrush, Golden (Castilleja levisecta)

Castilléjie dorée

Phacelia, Branched (Phacelia ramosissima)

Phacélie rameuse

Pine, Whitebark (Pinus albicaulis)

Pin à écorce blanche

Plantain, Heart-leaved (Plantago cordata)

Plantain à feuilles cordées

Pogonia, Large Whorled (Isotria verticillata)

Isotrie verticillée

Pogonia, Nodding (Triphora trianthophora)

Triphore penché

Pogonia, Small Whorled (Isotria medeoloides)

Isotrie fausse-médéole

Pondweed, Ogden’s (Potamogeton ogdenii)

Potamot de Ogden

Popcornflower, Fragrant (Plagiobothrys figuratus)

Plagiobothryde odorante

Pussytoes, Stoloniferous (Antennaria flagellaris)

Antennaire stolonifère

Quillwort, Engelmann’s (Isoetes engelmannii)

Isoète d’Engelmann

Rockcress, Quebec (Boechera quebecensis)

Arabette du Québec

Rush, Kellogg’s (Juncus kelloggii)

Jonc de Kellogg

Sand-verbena, Pink (Abronia umbellata)

Abronie rose

Sand-verbena, Small-flowered (Tripterocalyx micranthus)

Abronie à petites fleurs

Sandwort, Dwarf (Minuartia pusilla)

Minuartie naine

Sedge, False Hop (Carex lupuliformis)

Carex faux-lupulina

Sedge, Foothill (Carex tumulicola)

Carex tumulicole

Sedge, Juniper (Carex juniperorum)

Carex des genévriers

Silverpuffs, Lindley’s False (Uropappus lindleyi)

Uropappe de Lindley

Spike-primrose, Brook (Epilobium torreyi)

Épilobe de Torrey

Spike-primrose, Dense (Epilobium densiflorum)

Epilobe densiflore

Spike-rush, Bent (Eleocharis geniculata) Great Lakes Plains population

Éléocharide géniculée population des plaines des Grands Lacs

Spike-rush, Bent (Eleocharis geniculata) Southern Mountain population

Éléocharide géniculée population des montagnes du Sud

Spike-rush, Horsetail (Eleocharis equisetoides)

Éléocharide fausse-prêle

Sundew, Thread-leaved (Drosera filiformis)

Droséra filiforme

Tonella, Small-flowered (Tonella tenella)

Tonelle délicate

Toothcup (Rotala ramosior) Southern Mountain population

Rotala rameux population des montagnes du Sud

Tree, Cucumber (Magnolia acuminata)

Magnolia acuminé

Trefoil, Bog Bird’s-foot (Lotus pinnatus)

Lotier à feuilles pennées

Trillium, Drooping (Trillium flexipes)

Trille à pédoncule incliné

Triteleia, Howell’s (Triteleia howellii)

Tritéléia de Howell

Violet, Bird’s-foot (Viola pedata)

Violette pédalée

Violet praemorsa subspecies, Yellow Montane (Viola praemorsa ssp. praemorsa)

Violette jaune des monts de la sous-espèce praemorsa

Willow, Barrens (Salix jejuna)

Saule des landes

Wintergreen, Spotted (Chimaphila maculata)

Chimaphile maculée

Wood-poppy (Stylophorum diphyllum)

Stylophore à deux feuilles

Woolly-heads, Tall (Psilocarphus elatior)

Psilocarphe élevé

Woolly-heads, Dwarf (Psilocarphus brevissimus) Southern Mountain population

Psilocarphe nain, population des montagnes du Sud

Lichens
Lichen, Batwing Vinyl (Leptogium platynum)

Leptoge à grosses spores

Lichen, Boreal Felt (Erioderma pedicellatum) Atlantic population

Érioderme boréal population de l’Atlantique

Lichen, Pale-bellied Frost (Physconia subpallida)

Physconie pâle

Lichen, Seaside Centipede (Heterodermia sitchensis)

Hétérodermie maritime

Lichen, Vole Ears (Erioderma mollissimum)

Érioderme mou

Mosses
Cord-moss, Rusty (Entosthodon rubiginosus)

Entosthodon rouilleux

Moss, Acuteleaf Small Limestone (Seligeria acutifolia)

Séligérie à feuilles aiguës

Moss, Margined Streamside (Scouleria marginata)

Scoulérie à feuilles marginées

Moss, Nugget (Microbryum vlassovii)

Phasque de Vlassov

Moss, Poor Pocket (Fissidens pauperculus)

Fissident appauvri

Moss, Rigid Apple (Bartramia stricta)

Bartramie à feuilles dressées

Moss, Roell’s Brotherella (Brotherella roellii)

Brotherelle de Ro‌ell

Moss, Silver Hair (Fabronia pusilla)

Fabronie naine

PART 3
Threatened Species
Mammals
Bat, Pallid (Antrozous pallidus)

Chauve-souris blonde

Bison, Wood (Bison bison athabascae)

Bison des bois

Caribou, Woodland (Rangifer tarandus caribou) Boreal population

Caribou des bois population boréale

Caribou, Woodland (Rangifer tarandus caribou) Southern Mountain population

Caribou des bois population des montagnes du Sud

Ermine haidarum subspecies (Mustela erminea haidarum)

Hermine de la sous-espèce haidarum

Fox, Grey (Urocyon cinereoargenteus)

Renard gris

Fox, Swift (Vulpes velox)

Renard véloce

Marten, American (Martes americana atrata) Newfoundland population

Martre d’Amérique population de Terre-Neuve

Prairie Dog, Black-tailed (Cynomys ludovicianus)

Chien de prairie

Whale, Beluga (Delphinapterus leucas) Cumberland Sound population

Béluga population de la baie Cumberland

Whale, Fin (Balaenoptera physalus) Pacific population

Rorqual commun population du Pacifique

Whale, Killer (Orcinus orca) Northeast Pacific northern resident population

Épaulard population résidente du nord du Pacifique Nord-Est

Whale, Killer (Orcinus orca) Northeast Pacific offshore population

Épaulard population océanique du Pacifique Nord-Est

Whale, Killer (Orcinus orca) Northeast Pacific transient population

Épaulard population migratrice du Pacifique Nord-Est

Birds
Albatross, Short-tailed (Phoebastria albatrus)

Albatros à queue courte

Bittern, Least (Ixobrychus exilis)

Petit Blongios

Bobolink (Dolichonyx oryzivorus)

Goglu des prés

Bunting, Lark (Calamospiza melanocorys)

Bruant noir et blanc

Crossbill percna subspecies, Red (Loxia curvirostra percna)

Bec-croisé des sapins de la sous-espèce percna

Flycatcher, Olive-sided (Contopus cooperi)

Moucherolle à côtés olive

Goshawk laingi subspecies, Northern (Accipiter gentilis laingi)

Autour des palombes de la sous-espèce laingi

Gull, Ross’s (Rhodostethia rosea)

Mouette rosée

Hawk, Ferruginous (Buteo regalis)

Buse rouilleuse

Knot roselaari type, Red (Calidris canutus roselaari type)

Bécasseau maubèche du type roselaari

Longspur, Chestnut-collared (Calcarius ornatus)

Bruant à ventre noir

Longspur, McCown’s (Rhynchophanes mccownii)

Plectrophane de McCown

Meadowlark, Eastern (Sturnella magna)

Sturnelle des prés

Murrelet, Marbled (Brachyramphus marmoratus)

Guillemot marbré

Nighthawk, Common (Chordeiles minor)

Engoulevent d’Amérique

Owl, Barn (Tyto alba) Western population

Effraie des clochers population de l’Ouest

Owl brooksi subspecies, Northern Saw-whet (Aegolius acadicus brooksi)

Petite Nyctale de la sous-espèce brooksi

Pipit, Sprague’s (Anthus spragueii)

Pipit de Sprague

Screech-owl kennicottii subspecies, Western (Megascops kennicottii kennicottii)

Petit-duc des montagnes de la sous-espèce kennicottii

Screech-owl macfarlanei subspecies, Western (Megascops kennicottii macfarlanei)

Petit-duc des montagnes de la sous-espèce macfarlanei

Shrike excubitorides subspecies, Loggerhead (Lanius ludovicianus excubitorides)

Pie-grièche migratrice de la sous-espèce excubitorides

Swallow, Bank (Riparia riparia)

Hirondelle de rivage

Swallow, Barn (Hirundo rustica)

Hirondelle rustique

Swift, Chimney (Chaetura pelagica)

Martinet ramoneur

Thrush, Bicknell’s (Catharus bicknelli)

Grive de Bicknell

Thrush, Wood (Hylocichla mustelina)

Grive des bois

Warbler, Canada (Wilsonia canadensis)

Paruline du Canada

Warbler, Golden-winged (Vermivora chrysoptera)

Paruline à ailes dorées

Waterthrush, Louisiana (Parkesia motacilla)

Paruline hochequeue

Whip-poor-will (Caprimulgus vociferus)

Engoulevent bois-pourri

Woodpecker, Lewis’s (Melanerpes lewis)

Pic de Lewis

Amphibians
Frog, Rocky Mountain Tailed (Ascaphus montanus)

Grenouille-à-queue des Rocheuses

Frog, Western Chorus (Pseudacris triseriata) Great Lakes / St. Lawrence – Canadian Shield population

Rainette faux-grillon de l’Ouest population des Grands Lacs / Saint-Laurent et du Bouclier canadien

Salamander, Coastal Giant (Dicamptodon tenebrosus)

Grande salamandre

Salamander, Spring (Gyrinophilus porphyriticus) Adirondack / Appalachian population

Salamandre pourpre population des Adirondacks et des Appalaches

Spadefoot, Great Basin (Spea intermontana)

Crapaud du Grand Bassin

Reptiles
Gophersnake, Great Basin (Pituophis catenifer deserticola)

Couleuvre à nez mince du Grand Bassin

Massasauga (Sistrurus catenatus) Great Lakes/St. Lawrence population

Massasauga population des Grands Lacs et du Saint-Laurent

Racer, Eastern Yellow-bellied (Coluber constrictor flaviventris)

Couleuvre agile à ventre jaune de l’Est

Ratsnake, Gray (Pantherophis spiloides) Great Lakes/St. Lawrence population

Couleuvre obscure population des Grands Lacs et du Saint-Laurent

Rattlesnake, Western (Crotalus oreganos)

Crotale de l’Ouest

Ribbonsnake, Eastern (Thamnophis sauritus) Atlantic population

Couleuvre mince population de l’Atlantique

Snake, Eastern Hog-nosed (Heterodon platirhinos)

Couleuvre à nez plat

Turtle, Blanding’s (Emydoidea blandingii) Great Lakes / St. Lawrence population

Tortue mouchetée population des Grands Lacs et du Saint-Laurent

Turtle, Wood (Glyptemys insculpta)

Tortue des bois

Fish
Darter, Eastern Sand (Ammocrypta pellucida) Ontario populations

Dard de sable populations de l’Ontario

Darter, Eastern Sand (Ammocrypta pellucida) Quebec populations

Dard de sable populations du Québec

Lamprey, Vancouver (Entosphenus macrostomus)

Lamproie de Vancouver

Minnow, Plains (Hybognathus placitus)

Méné des plaines

Minnow, Pugnose (Opsopoeodus emiliae)

Petit-bec

Minnow, Western Silvery (Hybognathus argyritis)

Méné d’argent de l’Ouest

Redhorse, Black (Moxostoma duquesnei)

Chevalier noir

Sculpin, Coastrange (Cottus aleuticus) Cultus population

Chabot de la chaîne côtière population Cultus

Sculpin, Rocky Mountain (Cottus sp.) Eastslope populations

Chabot des montagnes Rocheuses populations du versant est

Shiner, Pugnose (Notropis anogenus)

Méné camus

Shiner, Silver (Notropis photogenis)

Méné miroir

Spotted Wolffish (Anarhichas minor)

Loup tacheté

Sucker, Mountain (Catostomus platyrhynchus) Milk River populations

Meunier des montagnes populations de la rivière Milk

Sucker, Salish (Catostomus sp. cf. catostomus)

Meunier de Salish

Trout, Bull (Salvelinus confluentus) Saskatchewan – Nelson Rivers populations

Omble à tête plate populations de la rivière Saskatchewan et du fleuve Nelson

Trout, Westslope Cutthroat (Oncorhynchus clarkii lewisi) Alberta population

Truite fardée versant de l’Ouest population de l’Alberta

Wolffish, Northern (Anarhichas denticulatus)

Loup à tête large

Molluscs
Atlantic Mud-piddock (Barnea truncata)

Pholade tronquée

Jumping-slug, Dromedary (Hemphillia dromedarius)

Limace-sauteuse dromadaire

Mapleleaf (Quadrula quadrula) Saskatchewan – Nelson Rivers population

Mulette feuille d’érable population de la rivière Saskatchewan et du fleuve Nelson

Taildropper, Blue-grey (Prophysaon coeruleum)

Limace-prophyse bleu-gris

Wartyback, Threehorn (Obliquaria reflexa)

Obliquaire à trois cornes

Arthropods
Flower Moth, Verna’s (Schinia verna)

Héliotin de Verna

Skipper, Dun (Euphyes vestris) Western population

Hespérie rurale population de l’Ouest

Sweat Bee, Sable Island (Lasioglossum sablense)

Halicte de l’île de Sable

Tiger Beetle, Audouin’s Night-stalking (Omus audouini)

Cicindèle d’Audouin

Tiger Beetle, Gibson’s Big Sand (Cicindela formosa gibsoni)

Cicindèle à grandes taches de Gibson

Plants
Arnica, Griscom’s (Arnica griscomii ssp. griscomii)

Arnica de Griscom

Aster, Anticosti (Symphyotrichum anticostense)

Aster d’Anticosti

Aster, Gulf of St. Lawrence (Symphyotrichum laurentianum)

Aster du golfe Saint-Laurent

Aster, Western Silvery (Symphyotrichum sericeum)

Aster soyeux

Aster, White Wood (Eurybia divaricata)

Aster à rameaux étalés

Aster, Willowleaf (Symphyotrichum praealtum)

Aster très élevé

Baccharis, Eastern (Baccharis halimifolia)

Baccharis à feuilles d’arroche

Bartonia, Branched (Bartonia paniculata ssp. paniculata)

Bartonie paniculée

Blazing Star, Dense (Liatris spicata)

Liatris à épi

Coffee-tree, Kentucky (Gymnocladus dioicus)

Chicot févier

Cryptantha, Tiny (Cryptantha minima)

Cryptanthe minuscule

Daisy, Lakeside (Hymenoxys herbacea)

Hyménoxys herbacé

Deerberry (Vaccinium stamineum)

Airelle à longues étamines

Desert-parsley, Gray’s (Lomatium grayi)

Lomatium de Gray

Fern, Lemmon’s Holly (Polystichum lemmonii)

Polystic de Lemmon

Fern, Mountain Holly (Polystichum scopulinum)

Polystic des rochers

Gentian, Victorin’s (Gentianopsis virgata ssp. victorinii)

Gentiane de Victorin

Goldenrod, Showy (Solidago speciosa) Boreal population

Verge d’or voyante population boréale

Goldenseal (Hydrastis canadensis)

Hydraste du Canada

Goosefoot, Smooth (Chenopodium subglabrum)

Chénopode glabre

Greenbrier, Round-leaved (Smilax rotundifolia) Great Lakes Plains population

Smilax à feuilles rondes population des plaines des Grands Lacs

Hackberry, Dwarf (Celtis tenuifolia)

Micocoulier rabougri

Hyacinth, Wild (Camassia scilloides)

Camassie faux-scille

Jacob’s-ladder, Van Brunt’s (Polemonium vanbruntiae)

Polémoine de Van Brunt

Lady’s-slipper, Small White (Cypripedium candidum)

Cypripède blanc

Locoweed, Hare-footed (Oxytropis lagopus)

Oxytrope patte-de-lièvre

Meadowfoam, Macoun’s (Limnanthes macounii)

Limnanthe de Macoun

Mosquito-fern, Mexican (Azolla mexicana)

Azolle du Mexique

Mouse-ear-cress, Slender (Halimolobos virgata)

Halimolobos mince

Paintbrush, Cliff (Castilleja rupicola)

Castilléjie des rochers

Pepperbush, Sweet (Clethra alnifolia)

Clèthre à feuilles d’aulne

Phlox, Showy (Phlox speciosa ssp. occidentalis)

Phlox de l’Ouest

Popcornflower, Slender (Plagiobothrys tenellus)

Plagiobothryde délicate

Quillwort, Bolander’s (Isoetes bolanderi)

Isoète de Bolander

Rue-anemone, False (Enemion biternatum)

Isopyre à feuilles biternées

Sanicle, Bear’s-foot (Sanicula arctopoides)

Sanicle patte-d’ours

Sanicle, Purple (Sanicula bipinnatifida)

Sanicle bipinnatifide

Soapweed (Yucca glauca)

Yucca glauque

Spiderwort, Western (Tradescantia occidentalis)

Tradescantie de l’Ouest

Thistle, Hill’s (Cirsium hillii)

Chardon de Hill

Toothcup (Rotala ramosior) Great Lakes Plains population

Rotala rameux population des plaines des Grands Lacs

Twayblade, Purple (Liparis liliifolia)

Liparis à feuilles de lis

Water-willow, American (Justicia americana)

Carmantine d’Amérique

Willow, Green-scaled (Salix chlorolepis)

Saule à bractées vertes

Woodsia, Blunt-lobed (Woodsia obtusa)

Woodsie à lobes arrondis

Lichens
Bone, Seaside (Hypogymnia heterophylla)

Hypogymnie maritime

Lichen, Black-foam (Anzia colpodes)

Anzie mousse-noire

Lichen, Crumpled Tarpaper (Collema coniophilum)

Collème bâche

Lichen, Wrinkled Shingle (Pannaria lurida)

Pannaire jaune pâle

Waterfan, Eastern (Peltigera hydrothyria)

Peltigère éventail d’eau de l’Est

Mosses
Bryum, Porsild’s (Mielichhoferia macrocarpa)

Bryum de Porsild

Moss, Alkaline Wing-nerved (Pterygoneurum kozlovii)

Ptérygoneure de Koslov

Moss, Haller’s Apple (Bartramia halleriana)

Bartramie de Haller

Moss, Spoon-leaved (Bryoandersonia illecebra)

Andersonie charmante

PART 4
Special Concern
Mammals
Badger taxus subspecies, American (Taxidea taxus taxus)

Blaireau d’Amérique de la sous-espèce taxus

Bat, Spotted (Euderma maculatum)

Oreillard maculé

Bear, Grizzly (Ursus arctos) Western population

Ours grizzli population de l’Ouest

Bear, Polar (Ursus maritimus)

Ours blanc

Beaver, Mountain (Aplodontia rufa)

Castor de montagne

Caribou, Barren-ground (Rangifer tarandus groenlandicus) Dolphin and Union population

Caribou de la toundra population Dolphin-et-Union

Caribou, Woodland (Rangifer tarandus caribou) Northern Mountain population

Caribou des bois population des montagnes du Nord

Cottontail nuttallii subspecies, Nuttall’s (Sylvilagus nuttallii nuttallii)

Lapin de Nuttall de la sous-espèce nuttallii

Mole, Eastern (Scalopus aquaticus)

Taupe à queue glabre

Mouse megalotis subspecies, Western Harvest (Reithrodontomys megalotis megalotis)

Souris des moissons de la sous-espèce megalotis

Otter, Sea (Enhydra lutris)

Loutre de mer

Pika, Collared (Ochotona collaris)

Pica à collier

Porpoise, Harbour (Phocoena phocoena) Pacific Ocean population

Marsouin commun population de l’océan Pacifique

Sea Lion, Steller (Eumetopias jubatus)

Otarie de Steller

Vole, Woodland (Microtus pinetorum)

Campagnol sylvestre

Whale, Bowhead (Balaena mysticetus) Bering-Chukchi-Beaufort population

Baleine boréale, population des mers de Béring, des Tchouktches et de Beaufort

Whale, Fin (Balaenoptera physalus) Atlantic population

Rorqual commun population de l’Atlantique

Whale, Grey (Eschrichtius robustus) Eastern North Pacific population

Baleine grise population du Pacifique Nord-Est

Whale, Humpback (Megaptera novaeangliae) North Pacific population

Rorqual à bosse population du Pacifique Nord

Whale, Sowerby’s Beaked (Mesoplodon bidens)

Baleine à bec de Sowerby

Wolf, Eastern (Canis lupus lycaon)

Loup de l’Est

Wolverine (Gulo gulo)

Carcajou

Birds
Albatross, Black-footed (Phoebastria nigripes)

Albatros à pieds noirs

Auklet, Cassin’s (Ptychoramphus aleuticus)

Starique de Cassin

Blackbird, Rusty (Euphagus carolinus)

Quiscale rouilleux

Curlew, Long-billed (Numenius americanus)

Courlis à long bec

Duck, Harlequin (Histrionicus histrionicus) Eastern population

Arlequin plongeur population de l’Est

Falcon anatum/tundrius, Peregrine (Falco peregrinus anatum/tundrius)

Faucon pèlerin anatum/tundrius

Falcon pealei subspecies, Peregrine (Falco peregrinus pealei)

Faucon pèlerin de la sous-espèce pealei

Goldeneye, Barrow’s (Bucephala islandica) Eastern population

Garrot d’Islande population de l’Est

Grebe, Horned (Podiceps auritus) Western population

Grèbe esclavon population de l’Ouest

Grebe, Western (Aechmophorus occidentalis)

Grèbe élégant

Grosbeak, Evening (Coccothraustes vespertinus)

Gros-bec errant

Heron fannini subspecies, Great Blue (Ardea herodias fannini)

Grand héron de la sous-espèce fannini

Knot islandica subspecies, Red (Calidris canutus islandica)

Bécasseau maubèche de la sous-espèce islandica

Murrelet, Ancient (Synthliboramphus antiquus)

Guillemot à cou blanc

Owl, Flammulated (Otus flammeolus)

Petit-duc nain

Owl, Short-eared (Asio flammeus)

Hibou des marais

Phalarope, Red-necked (Phalaropus lobatus)

Phalarope à bec étroit

Pigeon, Band-tailed (Patagioenas fasciata)

Pigeon à queue barrée

Rail, Yellow (Coturnicops noveboracensis)

Râle jaune

Sandpiper, Buff-breasted (Tryngites subruficollis)

Bécasseau roussâtre

Sparrow, Baird’s (Ammodramus bairdii)

Bruant de Baird

Sparrow pratensis subspecies, Grasshopper (Ammodramus savannarum pratensis)

Bruant sauterelle de la sous-espèce de l’Est

Sparrow princeps subspecies, Savannah (Passerculus sandwichensis princeps)

Bruant des prés de la sous-espèce princeps

Wood-pewee, Eastern (Contopus virens)

Pioui de l’Est

Amphibians
Frog, Coastal Tailed (Ascaphus truei)

Grenouille-à-queue côtière

Frog, Northern Leopard (Lithobates pipiens) Western Boreal/Prairie populations

Grenouille léopard populations des Prairies et de l’ouest de la zone boréale

Frog, Red-legged (Rana aurora)

Grenouille à pattes rouges

Salamander, Coeur d’Alene (Plethodon idahoensis)

Salamandre de Coeur d’Alène

Salamander, Wandering (Aneides vagrans)

Salamandre errante

Salamander, Western Tiger (Ambystoma mavortium) Prairie/Boreal population

Salamandre tigrée de l’Ouest population boréale et des Prairies

Toad, Great Plains (Anaxyrus cognatus)

Crapaud des steppes

Toad, Western (Anaxyrus boreas) Calling population

Crapaud de l’Ouest population chantante

Toad, Western (Anaxyrus boreas) Non-calling population

Crapaud de l’Ouest population non-chantante

Reptiles
Boa, Rubber (Charina bottae)

Boa caoutchouc

Milksnake (Lampropeltis triangulum)

Couleuvre tachetée

Racer, Western Yellow-bellied (Coluber constrictor mormon)

Couleuvre agile à ventre jaune de l’Ouest

Rattlesnake, Prairie (Crotalus viridis)

Crotale des prairies

Ribbonsnake, Eastern (Thamnophis sauritus) Great Lakes population

Couleuvre mince population des Grands Lacs

Skink, Five-lined (Plestiodon fasciatus) Great Lakes/St. Lawrence population

Scinque pentaligne population des Grands Lacs et du Saint-Laurent

Skink, Prairie (Plestiodon septentrionalis)

Scinque des Prairies

Skink, Western (Plestiodon skiltonianus)

Scinque de l’Ouest

Turtle, Eastern Musk (Sternotherus odoratus)

Tortue musquée

Turtle, Eastern Painted (Chrysemys picta picta)

Tortue peinte de l’Est

Turtle, Midland Painted (Chrysemys picta marginata)

Tortue peinte du Centre

Turtle, Northern Map (Graptemys geographica)

Tortue géographique

Turtle, Snapping (Chelydra serpentina)

Tortue serpentine

Turtle, Western Painted (Chrysemys picta bellii) Intermountain - Rocky Mountain population

Tortue peinte de l’Ouest, population intramontagnarde - des Rocheuses

Watersnake, Lake Erie (Nerodia sipedon insularum)

Couleuvre d’eau du lac Érié

Fish
Buffalo, Bigmouth (Ictiobus cyprinellus) Saskatchewan – Nelson River populations

Buffalo à grande bouche populations de la rivière Saskatchewan et du fleuve Nelson

Darter, Channel (Percina copelandi) St. Lawrence populations

Fouille-roche gris populations du Saint-Laurent

Dolly Varden (Salvelinus malma malma) Western Arctic populations

Dolly Varden populations de l’ouest de l’Arctique

Killifish, Banded (Fundulus diaphanus) Newfoundland populations

Fondule barré populations de Terre-Neuve

Kiyi, Upper Great Lakes (Coregonus kiyi kiyi)

Kiyi du secteur supérieur des Grands Lacs

Lamprey, Northern Brook (Ichthyomyzon fossor) Great Lakes – Upper St. Lawrence populations

Lamproie du Nord populations des Grands Lacs et du haut Saint-Laurent

Lamprey, Silver (Ichthyomyzon unicuspis) Great Lakes – Upper St. Lawrence populations

Lamproie argentée populations des Grands Lacs et du haut Saint-Laurent

Minnow, Cutlip (Exoglossum maxillingua)

Bec-de-lièvre

Pickerel, Grass (Esox americanus vermiculatus)

Brochet vermiculé

Redhorse, River (Moxostoma carinatum)

Chevalier de rivière

Rockfish type I, Rougheye (Sebastes sp. type I)

Sébaste à œil épineux du type I

Rockfish type II, Rougheye (Sebastes sp. type II)

Sébaste à œil épineux du type II

Rockfish, Yelloweye (Sebastes ruberrimus) Pacific Ocean inside waters population

Sébaste aux yeux jaunes population des eaux intérieures de l’océan Pacifique

Rockfish, Yelloweye (Sebastes ruberrimus) Pacific Ocean outside waters population

Sébaste aux yeux jaunes population des eaux extérieures de l’océan Pacifique

Sculpin, Columbia (Cottus hubbsi)

Chabot du Columbia

Sculpin, Deepwater (Myoxocephalus thompsonii) Great Lakes - Western St. Lawrence populations

Chabot de profondeur, populations des Grands Lacs - Ouest du Saint-Laurent

Sculpin, Rocky Mountain (Cottus sp.) Westslope populations

Chabot des montagnes Rocheuses populations du versant ouest

Sculpin, Shorthead (Cottus confusus)

Chabot à tête courte

Shark, Bluntnose Sixgill (Hexanchus griseus)

Requin griset

Shiner, Bridle (Notropis bifrenatus)

Méné d’herbe

Stickleback, Giant Threespine (Gasterosteus aculeatus)

Épinoche à trois épines géante

Stickleback, Unarmoured Threespine (Gasterosteus aculeatus)

Épinoche à trois épines lisse

Sturgeon, Green (Acipenser medirostris)

Esturgeon vert

Sturgeon, Lake (Acipenser fulvescens) Southern Hudson Bay – James Bay populations

Esturgeon jaune populations du sud de la baie d’Hudson et de la baie James

Sturgeon, Shortnose (Acipenser brevirostrum)

Esturgeon à museau court

Sucker, Mountain (Catostomus platyrhynchus) Pacific populations

Meunier des montagnes populations du Pacifique

Sucker, Spotted (Minytrema melanops)

Meunier tacheté

Sunfish, Northern (Lepomis peltastes) Great Lakes – Upper St. Lawrence populations

Crapet du Nord populations des Grands Lacs et du haut Saint-Laurent

Thornyhead, Longspine (Sebastolobus altivelis)

Sébastolobe à longues épines

Tope (Galeorhinus galeus)

Milandre

Topminnow, Blackstripe (Fundulus notatus)

Fondule rayé

Trout, Bull (Salvelinus confluentus) South Coast British Columbia populations

Omble à tête plate populations de la côte sud de la Colombie-Britannique

Trout, Bull (Salvelinus confluentus) Western Arctic populations

Omble à tête plate populations de l’ouest de l’Arctique

Trout, Westslope Cutthroat (Oncorhynchus clarkii lewisi) British Columbia population

Truite fardée versant de l’ouest population de la Colombie-Britannique

Warmouth (Lepomis gulosus)

Crapet sac-à-lait

Wolffish, Atlantic (Anarhichas lupus)

Loup Atlantique

Molluscs
Floater, Brook (Alasmidonta varicosa)

Alasmidonte renflée

Jumping-slug, Warty (Hemphillia glandulosa)

Limace-sauteuse glanduleuse

Lampmussel, Wavy-rayed (Lampsilis fasciola)

Lampsile fasciolée

Lampmussel, Yellow (Lampsilis cariosa)

Lampsile jaune

Mantleslug, Magnum (Magnipelta mycophaga)

Limace à grand manteau

Mapleleaf (Quadrula quadrula) Great Lakes – Upper St. Lawrence population

Mulette feuille d’érable population des Grands Lacs et du haut Saint-Laurent

Mussel, Rocky Mountain Ridged (Gonidea angulata)

Gonidée des Rocheuses

Oyster, Olympia (Ostrea lurida)

Huître plate du Pacifique

Pondmussel, Eastern (Ligumia nasuta)

Ligumie pointue

Rainbow (Villosa iris)

Villeuse irisée

Slug, Haida Gwaii (Staala gwaii)

Limace de Haida Gwaii

Slug, Pygmy (Kootenaia burkei)

Limace pygmée

Slug, Sheathed (Zacoleus idahoensis)

Limace gainée

Vertigo, Threaded (Nearctula sp.)

Vertigo à crêtes fines

Arthropods
Bumble Bee, Yellow-banded (Bombus terricola)

Bourdon terricole

Dancer, Vivid (Argia vivida)

Agrion vif

Grasshopper, Greenish-white (Hypochlora alba)

Criquet de l’armoise

Leafhopper, Red-tailed (Aflexia rubranura) Great Lakes Plains population

Cicadelle à queue rouge population des plaines des Grands Lacs

Leafhopper, Red-tailed (Aflexia rubranura) Prairie population

Cicadelle à queue rouge population des Prairies

Metalmark, Mormon (Apodemia mormo) Prairie population

Mormon population des Prairies

Monarch (Danaus plexippus)

Monarque

Moth, Pale Yellow Dune (Copablepharon grandis)

Noctuelle jaune pâle des dunes

Skipper, Sonora (Polites sonora)

Hespérie du Sonora

Snaketail, Pygmy (Ophiogomphus howei)

Ophiogomphe de Howe

Spider, Georgia Basin Bog (Gnaphosa snohomish)

Gnaphose de Snohomish

Tachinid Fly, Dune (Germaria angustata)

Mouche tachinide des dunes

Weidemeyer’s Admiral (Limenitis weidemeyerii)

Amiral de Weidemeyer

Plants
Ash, Blue (Fraxinus quadrangulata)

Frêne bleu

Aster, Crooked-stem (Symphyotrichum prenanthoides)

Aster fausse-prenanthe

Aster, Nahanni (Symphyotrichum nahanniense)

Aster de la Nahanni

Aster, White-top (Sericocarpus rigidus)

Aster rigide

Beggarticks, Vancouver Island (Bidens amplissima)

Grand bident

Blue Flag, Western (Iris missouriensis)

Iris du Missouri

Buffalograss (Bouteloua dactyloides)

Buchloé faux-dactyle

Fern, American Hart’s-tongue (Asplenium scolopendrium)

Scolopendre d’Amérique

Fern, Coastal Wood (Dryopteris arguta)

Dryoptéride côtière

Goldencrest (Lophiola aurea)

Lophiolie dorée

Goldenrod, Houghton’s (Solidago houghtonii)

Verge d’or de Houghton

Goldenrod, Riddell’s (Solidago riddellii)

Verge d’or de Riddell

Hairgrass, Mackenzie (Deschampsia mackenzieana)

Deschampsie du bassin du Mackenzie

Hoptree, Common (Ptelea trifoliata)

Ptéléa trifolié

Indian-plantain, Tuberous (Arnoglossum plantagineum)

Arnoglosse plantain

Iris, Dwarf Lake (Iris lacustris)

Iris lacustre

Lilaeopsis, Eastern (Lilaeopsis chinensis)

Liléopsis de l’Est

Lily, Lyall’s Mariposa (Calochortus lyallii)

Calochorte de Lyall

Milk-vetch, Fernald’s (Astragalus robbinsii var. fernaldii)

Astragale de Fernald

Pennywort, Water (Hydrocotyle umbellata)

Hydrocotyle à ombelle

Pinweed, Beach (Lechea maritima)

Léchéa maritime

Podistera, Yukon (Podistera yukonensis)

Podistère du Yukon

Pondweed, Hill’s (Potamogeton hillii)

Potamot de Hill

Prairie-clover, Hairy (Dalea villosa)

Dalée velue

Quillwort, Prototype (Isoetes prototypus)

Isoète prototype

Redroot (Lachnanthes caroliniana)

Lachnanthe de Caroline

Rose, Climbing Prairie (Rosa setigera)

Rosier sétigère

Rose-mallow, Swamp (Hibiscus moscheutos)

Ketmie des marais

Rush, New Jersey (Juncus caesariensis)

Jonc du New Jersey

Saxifrage, Spiked (Micranthes spicata)

Saxifrage à épis

Sedge, Baikal (Carex sabulosa)

Carex des sables

Spike-rush, Tubercled (Eleocharis tuberculosa)

Éléocharide tuberculée

Tansy, Floccose (Tanacetum huronense var. floccosum)

Tanaisie floconneuse

Thistle, Pitcher’s (Cirsium pitcheri)

Chardon de Pitcher

Thrift, Athabasca (Armeria maritima interior)

Arméria de l’Athabasca

Water-hemlock, Victorin’s (Cicuta maculata var. victorinii)

Cicutaire de Victorin

Wild Buckwheat, Yukon (Eriogonum flavum var. aquilinum)

Ériogone du Nord

Willow, Felt-leaf (Salix silicicola)

Saule silicicole

Willow, Sand-dune Short-capsuled (Salix brachycarpa var. psammophila)

Saule psammophile

Willow, Turnor’s (Salix turnorii)

Saule de Turnor

Woolly-heads, Dwarf (Psilocarphus brevissimus) Prairie population

Psilocarphe nain, population des Prairies

Yarrow, Large-headed Woolly (Achillea millefolium var. megacephalum)

Achillée à gros capitules

Mosses
Cord-moss, Banded (Entosthodon fascicularis)

Entosthodon fasciculé

Moss, Columbian Carpet (Bryoerythrophyllum columbianum)

Érythrophylle du Columbia

Moss, Twisted Oak (Syntrichia laevipila)

Tortule à poils lisses

Tassel, Tiny (Crossidium seriatum)

Petit pompon

Lichens
Glass-whiskers, Frosted (Sclerophora peronella) Nova Scotia population

Sclérophore givré population de la Nouvelle-Écosse

Jellyskin, Flooded (Leptogium rivulare)

Leptoge des terrains inondés

Lichen, Blue Felt (Degelia plumbea)

Dégélie plombée

Lichen, Boreal Felt (Erioderma pedicallatum) Boreal population

Érioderme boréal population boréale

Lichen, Cryptic Paw (Nephroma occultum)

Néphrome cryptique

Lichen, Oldgrowth Specklebelly (Pseudocyphellaria rainierensis)

Pseudocyphellie des forêts surannées

Lichen, Peacock Vinyl (Leptogium polycarpum)

Leptoge à quatre spores

Mountain Crab-eye (Acroscyphus sphaerophoroides)

Acroscyphe des montagnes

Waterfan, Western (Peltigera gowardii)

Peltigère éventail d’eau de l’Ouest""".split('\n\n')

def remove_every_even_item_from_list(l):
    return [x for i, x in enumerate(l) if i % 2 == 0]

species_at_risk_eng = remove_every_even_item_from_list(species_at_risk_string)

for s in species_at_risk_eng:
    print(s)