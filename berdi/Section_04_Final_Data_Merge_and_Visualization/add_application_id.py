import pandas as pd

index_en = pd.read_csv('data/download_internal_Aug2022_merged/en/ESA_website_ENG.csv', encoding='utf-8-sig')  # 21643, 47
index_en['Project Download Path'].nunique()  # 39  # Brunswick project has been excluded
index_en['Table Download Path'].nunique()  # 14607

index_fr = pd.read_csv('data/download_internal_Aug2022_merged/fr/ESA_website_FRA.csv', encoding='utf-8-sig')  # 21643, 47
index_fr["Chemin d'accès pour télécharger le projet"].nunique()  # 39
index_fr["Chemin d'accès pour télécharger le tableau"].nunique()  # 14607

# Add IK label
index_ik = pd.read_csv('data/Finall_ESA_IK_Rerults_08_15.csv', encoding='utf-8-sig')  # 21643, 50
index_ik_sinclair = pd.read_csv('data/sinclair_page_count_fixed.csv', encoding='utf-8-sig')
df_ik_id = pd.concat([
    index_ik[index_ik['Application Short Name'] != 'Sinclair'][['ID', 'IK_Labels']],
    index_ik_sinclair[['ID', 'IK_Labels']]])

index_en = index_en.merge(df_ik_id, on='ID')
index_fr = index_fr.merge(df_ik_id, on='ID')

# Add Application ID
project_list = index_en['Application Short Name'].unique().tolist()
projects = {project: i for i, project in enumerate(project_list)}
project_fr_en = dict()

for _, item in index_en.merge(index_fr, on='ID')[['Application Short Name', 'Nom abrégé de la demande']].drop_duplicates().iterrows():
    project_fr_en[item['Nom abrégé de la demande']] = item['Application Short Name']

index_en['Application ID'] = index_en['Application Short Name'].apply(lambda x: projects[x])
index_fr['Application ID'] = index_fr['Nom abrégé de la demande'].apply(lambda x: projects[project_fr_en[x]])

index_en.to_csv('data/download_internal_Aug2022_merged/en/ESA_website_ENG.csv', encoding='utf-8-sig', index=False)
index_fr.to_csv('data/download_internal_Aug2022_merged/fr/ESA_website_FRA_IK.csv', encoding='utf-8-sig', index=False)

# exclude IK column in the external version


