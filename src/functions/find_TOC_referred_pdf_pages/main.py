import pandas as pd

from src.util.database_connection import schema, engine
from src.functions.extract_TOCs.main import TOCType
from src.functions.find_TOC_referred_pdf_pages.helper_functions import find_toc_referred_pdf_pages_table,  \
    find_toc_referred_pdf_pages_figure
from src.functions.find_TOC_referred_pdf_pages.upsert_toc_referred_pdf_page import upsert_toc_referred_pdf_page
from src.functions.find_TOC_referred_pdf_pages.compose_regex_pattern import compose_content_type_regex, \
    compose_content_num_regex, compose_content_title_regex
from src.util.exception_and_logging.handle_exception import ExceptionHandler


def _check_all_tocs_extracted(application_id):
    """ check if TOCs have been extracted from all the pdf files in an application """
    query = f'''
        SELECT COUNT(*) as count
        FROM {schema}.Pdf
        WHERE ApplicationId = {application_id} AND TOCItemExtracted = 0;
    '''
    with ExceptionHandler(f"Error querying Pdfs of ApplicationId - {application_id}"), engine.begin() as conn:
        df_count = pd.read_sql(query, conn)

    with ExceptionHandler(f"Not all pdfs have TOCs extracted for ApplicationId - {application_id}"):
        if df_count.shape[0] < 1 or df_count.iloc[0]["count"] > 0:
            # if the count of pdfs that haven't had TOC item extracted is more than 0, meaning not all the TOCs from an
            # application have been extracted, raise an error
            raise ValueError(f"Not all pdfs have TOCs extracted for ApplicationId - {application_id}")


def find_toc_referred_pdf_pages(application_id, toc_type):
    """
    This function will find the referred pdf pages for all the TOC items that match the input toc_type and upsert the
    database table
    """
    # Preliminary check
    _check_all_tocs_extracted(application_id)

    # given an application, get all TOCs- content type, full title, order, pdf id, page num-
    # order by pdf regdocs id, page num, order
    with ExceptionHandler(f"Error querying TOCs of ApplicationId - {application_id}"), engine.begin() as conn:
        df_tocs = pd.read_sql(f'''
            SELECT pd.PdfId, p.PdfPageId, t.TOCId, t.ContentTitle
            FROM {schema}.TOC t 
                LEFT JOIN {schema}.PdfPage p ON t.PdfPageId = p.PdfPageId
                LEFT JOIN {schema}.Pdf pd ON p.PdfId = pd.PdfId
                INNER JOIN {schema}.Application a ON pd.ApplicationId = a.ApplicationId 
                    AND a.ApplicationId = {application_id}    
            WHERE t.ContentType = '{toc_type}'
            ORDER BY pd.RegdocsDataId, p.PageNumber, t.OrderNumber;
            ''', con=conn)

    # get a list of pdf ids for the application, order by regdocs id
    # the previous query retrieves all the TOCs; however some pdf doesn't have TOC items so not necessarily a complete
    # set of pdfs are returned by the last query
    with ExceptionHandler(f"Error querying Pdfs of ApplicationId - {application_id}"), engine.begin() as conn:
        df_pdfs = pd.read_sql(f''' 
            SELECT PdfId
            FROM {schema}.Pdf 
            WHERE ApplicationId = {application_id} 
            ORDER BY RegdocsDataId;
            ''', con=conn)
    pdf_id_list = df_pdfs["PdfId"].tolist()

    # the id of the latest pdf where referred pages were found for a TOC;
    # for the next TOC item, we will start the search for referred pages in this pdf
    curr_pdf_id = -1
    for _, row in df_tocs.iterrows():
        # iterate through all the TOCs
        full_title = row["ContentTitle"]  # i.e. Table 6.7 Watercourse and Fish-Bearing Wetland Crossing Table
        if full_title.count(" ") < 1:
            # if there is no whitespace, we won"t be able to use the following method to find referred pdf and pages
            continue

        # break down the TOC full title into content_type, content_num, content_title;
        # construct regex patterns for content_type, content_num, content_title
        content_type, content_num, content_title = full_title.split(" ", 2) if full_title.count(" ") > 1 \
            else full_title.split(" ") + ['']
        content_type_regex = compose_content_type_regex(content_type)
        content_num_regex = compose_content_num_regex(content_num)
        content_title_regex = compose_content_title_regex(content_title)

        # get a list of pdf_ids in the order of the likelihood the TOC might be referring to
        # - the current pdf id is the first in the list
        # - followed by the toc pdf to the last pdf in original ascending order
        # - followed by the one before toc pdf to the first pdf in descending order
        toc_pdf_id = row["PdfId"]
        index_toc_pdf_id = pdf_id_list.index(toc_pdf_id)
        reordered_pdf_id_list = (pdf_id_list[index_toc_pdf_id:]
                                 + pdf_id_list[index_toc_pdf_id-1::-1] if index_toc_pdf_id > 0 else [])
        if curr_pdf_id in reordered_pdf_id_list:
            reordered_pdf_id_list.insert(0, reordered_pdf_id_list.pop(reordered_pdf_id_list.index(curr_pdf_id)))

        for pdf_id in reordered_pdf_id_list:
            # iterate the pdf id in the reordered pdf id list
            if toc_type == TOCType.TABLE.value:
                pdf_page_id_list = find_toc_referred_pdf_pages_table(pdf_id,
                                                                     row["PdfPageId"],
                                                                     content_type_regex,
                                                                     content_num_regex,
                                                                     content_title_regex)
            else:  # toc_type == "Figure"
                pdf_page_id_list = find_toc_referred_pdf_pages_figure(pdf_id,
                                                                      row["PdfPageId"],
                                                                      content_num_regex,
                                                                      content_title)

            if pdf_page_id_list:
                # if there is any page in the pdf where we found matching text,
                # we update the database, update the current pdf id, and break out of the loop
                upsert_toc_referred_pdf_page(row["TOCId"], pdf_page_id_list)
                curr_pdf_id = pdf_id
                break
