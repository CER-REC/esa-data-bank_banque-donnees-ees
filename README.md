# BERDI - Methods

**** _**La version française suit**_ **** 

Environmental and Socio-Economic Assessments (ESAs) can be several hundred pages long and are submitted to the CER as a series of PDF documents. These PDFs contain qualitative and quantitative data, including text, tables, figures, maps and satellite images. 

While the information contained in each ESA is comprehensive, it is not easily searchable or accessible due to the limitations of the PDF format. No raw data files, such as tables in CSV format, are filed with the CER -- all relevant information is contained within the PDF file. Those interested in analysing, comparing, or processing the data must extract it manually, by copying and pasting information from the PDF into other software programs, such as spreadsheet software. This is time-intensive and tedious.

A team of data scientists at the CER created the process for automatically identifying ESA table and figure titles and extracting table data as a CSV. This process uses several open-source libraries in the Python programming language. All code is open source and available on the CER's GitHub repository.

### Step 1: Collect the relevant PDF documents
CER staff manually identified 1,902 ESA PDF documents in [REGDOCS](https://apps.cer-rec.gc.ca/REGDOCS/Home/Index). REGDOCS is the CER's on-line repository of public documents related to the design, construction, operation, and abandonment of federally regulated pipelines. A file that indexes all of these documents is available in our GitHub repository.

### Step 2: Convert PDF documents to text files
Each PDF was converted into a more computer-friendly text format using the [Python Tika library](https://github.com/chrismattmann/tika-python). 

### Step 3: Extract tables and figures
The next step was to identify unique features of each PDF page and their location coordinates. This information allows users to identify pages that have image features (ex. size of blocks, presence of text, etc.) and is used in modeling to identify ESA Figures. The [Python PyMuPDF library](https://pymupdf.readthedocs.io/en/latest/intro/) was used to extract these page-level PDF details. 

The extraction of tables from each PDF relied on a separate process. The [Python Camelot library](https://camelot-py.readthedocs.io/en/master/) was used to convert all tables from the PDFs into CSV (comma-separated value) files. Camelot relies on the presence of unique table features, (e.g. demarcated lines or presence of white space between cells) to identify tables in a PDF document.

Once tables and figures were identified, the next task was to label them with their respective title. 

### Step 4: Identify table and figure titles
The team used the ESA tables of contents from the PDF files (when available) together with a set of regular expressions to identify table and figure titles. Titles were then matched with their respective table or figure using regular expressions. In some instances, titles as they appear in the table of contents differed from the title spelling in the actual table or figure. Some calibration on matching was employed to match titles with figures or tables in such instances. 

### Step 5: Validate and verify
In general, programming the extraction of data out of PDFs is an imperfect process because each PDF can contain different table formats and be prepared and saved using different techniques. For example, tables with clear, black borders are easier to extract accurately compared to tables that have unclear or no borders. Our team employed a manual validation process for a sample of the tables, figures, and PDFs. It is possible that there are tables in PDFs that were not extracted or tables that were extracted, but are missing some data. It is estimated that 94% to 98% of all tables in PDF have been extracted, and that 88% to 94% of all tables have complete data (based on a random sample of 384 tables). 

All images were inspected and it was found that 92.1% of images had correct page numbers, 89.4% had correct titles, and 99.95% were faithful to the original image. Figure extraction was not perfect because of different titles for the same figure appearing in the table of contents vs. the body of text (due to spelling variability, inconsistency in labeling formats, or no title present). Secondly, figure titles that were embedded as images were undetected with a text-based extraction approach.  Finally, in a small percentage of PDF files (0.95%), the extraction process led to corrupt images where the text/image blocks are partially retained and the rest of the figure is replaced by black colour. 

While it is not a perfect process due to inconsistency in formatting, tables and figures can now be searched quickly, and tables can be downloaded in a machine-readable format - both possibilities that did not exist previously.

### Step 6: Extract alignment sheets
Based on visual inspection, we assumed that we might classify a particular page of a PDF as an alignment sheet or not based on certain features present on the page. Some of the important features chosen for this classification task are area of the images, number of images on a page, number of words on a page, and presence of some keywords (such as scale, kilometers or meters, figure, or north, etc.). We then trained several classification models using k-nearest neighbor, support vector machine, random forest, and Xgboost on a sample dataset of PDFs and calculated the accuracy of these models. The optimum classification model was selected based on the accuracy and the process time. The final model can be found in the [models](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/models) repo. Since we got an accuracy level of >95% for the optimal model, we then used this model to classify all the PDF pages in the BERDI databank to classify alignment sheets.

### Step 7: Extract VECs and VSCs labels
ESA documents include the analysis of potential biophysical and socio-economic effects of constructing and operating the proposed pipeline project. Biophysical components are also known as Valued Environmental Components (VECs), and socio-economic components are also referred to as Valued Socio-economic Components (VSCs). To extract VECs and VSCs, a list of keywords synonymous to each of the 22 VECs and VSCs was compiled, and a simple keyword search approach was used to find keywords of interest in the extracted titles (in Step 4 above) and the corresponding CSV text for tables.

### Step 8: Identify Indigenous Knowledge
Tables, Figures, Alignment-sheet containing sensitive Indigenous Knowledge (IK) had to be precluded from the search results in BERDI. The team used Natural Language Processing and other Machine Learning algorithms to identify if extracted texts from the document pages with corresponding tables, figures, and alignment-sheet contain Indigenous knowledge. In particular, we used Topic Modeling to discover optimum number of topics in the documents and used the topics and their relative weights as a set of features to build the classification models. In addition to this input, presence of manually curated keywords, absolute and normalized by page length, was also included. Sensitive IK tables, figures and alignment sheets were labelled by subject matter experts to provide a labelled dataset, in three iterations to improve model performance. Several classification methods were tested and measured on false omission rate of sensitive IK in search results: support vector machines, decision tree, random forest, XGBoost. Also, classification models were fit using an ensemble learning approach on an 80:20 split of the labeled data. Due to the skew in proportion of the labels, an Upsampling technique was implemented to synthetically generate and inject datapoints from the minority class into the training dataset. Random forest classification, on topic weights and presence of keywords, was found to be the best performing model in terms of false omission rate on left out data (0.67%), without penalizing false discovery rate (13%)


### Acknowledgments
The data science team at the University of British Columbia was instrumental in guiding this project in its early days. The Canada Energy Regulator acknowledges the work of Nipun Goyal, Louis (Xiang) Luo, and Prakhar Sinha (with support from Martha Essak, Erin Martin-Serrano, Stuart Donald, and Gene Moo Lee) at the [Centre for Operations Excellence](https://www.sauder.ubc.ca/thought-leadership/research-outreach-centres/centre-operations-excellence), UBC Sauder School of Business.

# CIBER - méthodes

Les évaluations environnementales et socioéconomiques (« EES ») peuvent compter plusieurs centaines de pages et sont soumises à la Régie de l’énergie du Canada sous forme de fichiers PDF. Ces fichiers renferment des données qualitatives et quantitatives, notamment du texte, des tableaux, des figures, des cartes et des images satellites. 

Bien que l’information contenue dans les EES soit détaillée, elle n’est pas facilement consultable ni accessible en raison des limites inhérentes aux fichiers PDF. Aucun fichier de données brutes, comme des tableaux en format CSV, n’est déposé auprès de la Régie; toute l’information pertinente se trouve dans les fichiers PDF. Les personnes qui souhaitent analyser, comparer ou traiter les données doivent les extraire manuellement, en copiant et en collant l’information du fichier PDF dans d’autres logiciels, comme des tableurs. C’est un processus long et fastidieux.

Une équipe de scientifiques de données de la Régie a établi un processus permettant de repérer automatiquement les titres des tableaux et des figures des EES ainsi que d’extraire les données contenues dans les tableaux en format CSV. Ce processus nécessite l’utilisation de plusieurs bibliothèques ouvertes dans le langage de programmation Python. Des précisions sur la méthode employée peuvent être téléchargées et tous les codes sont ouverts et accessibles à partir du dépôt GitHub de la Régie.

### Étape 1 – Recueillir les documents PDF pertinents
Le personnel de la Régie a répertorié manuellement 1 902 EES en format PDF dans [REGDOCS](https://apps.cer-rec.gc.ca/REGDOCS/Home/Index), le dépôt en ligne de la Régie qui renferme des documents publics sur la conception, la construction, l’exploitation et la cessation d’exploitation des pipelines de ressort fédéral. Un fichier qui répertorie tous ces documents se trouve dans le dépôt central GitHub.

### Étape 2 – Convertir les fichiers PDF en fichiers texte
Chaque fichier PDF a été converti dans un format texte plus convivial au moyen de la [bibliothèque Tika Python](https://github.com/chrismattmann/tika-python). 

### Étape 3 – Extraire des tableaux et des figures
L’étape suivante a consisté à recenser les caractéristiques uniques sur chaque page du PDF et les coordonnées de leurs emplacements. Cette information permet aux utilisateurs de repérer les pages qui ont des caractéristiques d’image (p. ex., taille des blocs, présence de texte) et est utilisée lors de la modélisation pour répertorier les figures qui se trouvent dans les EES. La [bibliothèque PyMuPDF de Python](https://pymupdf.readthedocs.io/en/latest/intro/) a été utilisée pour extraire les détails au niveau de la page. 

L’extraction des tableaux de chaque fichier PDF s’est faite au moyen d’un processus distinct. La bibliothèque Camelot de Python a servi à convertir tous les tableaux des fichiers PDF en fichiers CSV (valeurs séparées par des virgules). La [bibliothèque Camelot](https://camelot-py.readthedocs.io/en/master/) se sert des caractéristiques uniques (p. ex., lignes de délimitation ou espace blanc entre les cellules) pour repérer les tableaux dans un fichier PDF. Une fois que les tableaux et les figures ont été répertoriés, la tâche suivante a consisté à les étiqueter. 

### Étape 4 – Titres de tableaux et de figures
L’équipe a utilisé les tables des matières des EES dans les fichiers PDF (lorsqu’elles étaient présentes) ainsi qu’un ensemble d’expressions courantes pour repérer les titres des tableaux et des figures. Les titres ont ensuite été appariés à leur tableau ou figure respectifs à l’aide d’expressions courantes. Dans certains cas, les titres figurant dans la table des matières différaient des titres apparaissant dans les tableaux ou les figures. Une calibration a donc été nécessaire pour apparier certains titres avec des figures ou des tableaux. 

### Étape 5 – Valider et vérifier
En général, la programmation de l’extraction des données de fichiers PDF est un processus imparfait, car chaque fichier PDF peut renfermer divers formats de tableau et avoir été préparé et enregistré au moyen de techniques différentes. Par exemple, les tableaux à bordure noire claire sont plus faciles à extraire avec précision que ceux dont la bordure est floue ou inexistante. Notre équipe a utilisé un processus de validation manuel pour un ensemble de tableaux, de figures et de fichiers PDF. Il est possible qu’il y ait des tableaux dans les fichiers PDF qui n’ont pas été extraits ou qui l’ont été mais pour lesquels il manque certaines données. On estime que de 94 % à 98 % de tous les tableaux en format PDF ont été extraits et que de 88 % à 94 % de ceux-ci présentent des données complètes (sur la base d’un échantillon de 384 tableaux pris au hasard).

Toutes les images ont été revues et on a ainsi constaté que 92,1 % d’entre elles montraient le bon numéro de page, 89,4 % avaient le bon titre et 99,95 % étaient fidèles à l’image originale. L’extraction des figures n’était pas parfaite en raison de titres différents dans la table des matières (au niveau de l’orthographe ou des formats d’étiquetage), parfois même de l’absence totale de titre. Aussi, les titres des figures intégrés aux images demeuraient invisibles en raison de la méthode d’extraction choisie, fondée sur le texte. Enfin, dans un faible pourcentage de fichiers PDF (0,95 %), le processus d’extraction a mené à des images corrompues où des blocs texte/image étaient partiellement conservés alors que le reste de la figure était tout noir.

Bien qu’il ne s’agisse pas d’un processus parfait en raison d’un manque d’uniformité quant à la mise en page, les tableaux et les figures peuvent maintenant être consultés rapidement et les tableaux peuvent être téléchargés dans un format lisible par machine, deux possibilités qui n’existaient pas auparavant.

### Étape 6 – Extraction de cartes-tracés
Après avoir effectué une analyse visuelle, nous avons déterminé que la présence de certaines caractéristiques sur une page précise d’un document PDF nous permettait d’établir s’il s’agissait d’une feuille de tracé ou non. La zone des images, la présence de certains mots clés (comme échelle, kilomètre ou mètre, figure, nord, etc.), le nombre d’images et le nombre de mots sur la page sont quelques-unes des caractéristiques qui ont été utilisées pour établir cette classification. À partir d’un échantillon de fichiers PDF, nous avons ensuite entraîné plusieurs modèles de classification à l’aide de la méthode des k plus proches voisins, d’une machine à vecteurs de support, d’une forêt aléatoire et de Xgboost, puis nous avons calculé l’exactitude de ces modèles. Le [modèle](https://github.com/CER-REC/esa-data-bank_banque-donnees-ees/tree/master/models) de classification optimal a été choisi en fonction de l’exactitude et du temps de traitement. Comme ce modèle optimal a obtenu un niveau d’exactitude supérieur à 95 %, nous l’avons utilisé pour classer toutes les pages PDF de la banque de données des EES pour classer les cartes-tracés.

### Étape 7 : Extraction des étiquettes CEV ou CSV
Les documents de l’EES comprennent l’analyse des possibles effets biophysiques et socioéconomiques de la construction et de l’exploitation du projet pipelinier proposé. Les composantes biophysiques sont aussi connues sous le nom de composantes environnementales valorisées (« CEV »), et les composantes socioéconomiques, sous celui de composantes socioéconomiques valorisées (« CSV »). Pour extraire ces composantes, une liste de mots-clés correspondant à chacune des 22 CEV et CSV a été compilée, et une méthode de recherche simple par mots-clés a été utilisée pour trouver les mots-clés d’intérêt dans les titres extraits (à l’étape 4 ci-dessus) et le texte CSV correspondant pour les tableaux. 

### Étape 8 – Supprimer les connaissances autochtones de nature délicate
Les tableaux, figures et cartes-tracés renfermant des connaissances autochtones de nature délicate ont dû être supprimés des résultats de recherche dans CIBER. L’équipe a utilisé le traitement du langage naturel et d’autres algorithmes d’apprentissage automatique pour déterminer si les textes extraits des pages de documents renfermant les tableaux, figures et cartes-tracés correspondants contiennent des connaissances autochtones. Nous avons utilisé la modélisation par sujet pour découvrir le nombre optimal de sujets dans les documents et nous nous sommes servis des sujets et de leur importance relative comme un ensemble de caractéristiques pour élaborer les modèles de classification. Nous avons également ajouté des mots-clés triés manuellement, absolus et normalisés par longueur de page. Pour améliorer le rendement du modèle, les experts en la matière ont créé un ensemble de données étiquetées en repérant les tableaux, figures et cartes-tracés renfermant des connaissances autochtones. Plusieurs méthodes de classification ont été essayées et évaluées en fonction du taux de fausses omissions de connaissances autochtones de nature délicate dans les résultats de recherche : machines à vecteurs de soutien, arbre de décision, forêt aléatoire, XGBoost. Les modèles de classification ont été adaptés à l’aide d’une approche d’apprentissage d’ensemble selon une répartition 80/20 des données étiquetées. En raison de l’asymétrie de la proportion des étiquettes, une technique de suréchantillonnage a été mise en œuvre pour générer et injecter de façon synthétique des points de données de la classe de la minorité dans l’ensemble de données de formation. La classification par forêts aléatoires selon l’importance des sujets et la présence de mots-clés a été jugée le meilleur modèle en ce qui concerne le taux de fausses omissions (0,67 %), sans que soit pénalisé le taux de fausses découvertes (13 %).


### Remerciements
L’équipe responsable de la science des données de l’Université de la Colombie-Britannique a joué un rôle déterminant quant à l’orientation de ce projet à ses débuts. La Régie de l’énergie du Canada tient à souligner le travail de Nipun Goyal, Louis (Xiang) Luo et Prakhar Sinha (avec le soutien de Martha Essak, Erin Martin-Serrano, Stuart Donald et Gene Moo Lee) du [Centre for Operations Excellence](https://www.sauder.ubc.ca/thought-leadership/research-outreach-centres/centre-operations-excellence) de la Sauder School of Business de l’Université de la Colombie-Britannique.

