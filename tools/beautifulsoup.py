def wiki_tables(url, number_of_table_on_webpage, list_column, pandas_doc_name):

    """sample tables coming from the url at xlsx or csv format

    Parameters
    ----------
    number_of_table_on_webpage : int
        Number of table on the wabpage. For exemple the fourth table on
        the webpage, then number_of_table_on_webpage = 3 because it start
        from zero like the index of list.
    list_column : list or str
        Expect list of int type or "all". If specific columns are needed so use
        a list of int, if all columns are needed so write "all".
    pandas_doc_name : str
        It will be the name given to the doc saved in the directory
        /Users/Alex/perso/files/tableurs

    Returns
    -------
    None
        Create a doc at xlsx or csv format name and located according
        pandas_doc_name parameter
    """

    import os
    import re
    
    from bs4 import BeautifulSoup as bs
    import pandas as pd
    import requests
    

    webpage = requests.get(url)
    soup = bs(webpage.content)

    # pandasDocName if ".xlsx" or "csv" is missing or if ".xls" instead of ".xlsx" 
    if pandas_doc_name[-4:len(pandas_doc_name)] == ".xls":
        pandas_doc_name = pandas_doc_name + "x"
    elif  (pandas_doc_name[-5:len(pandas_doc_name)] != ".xlsx" and
           pandas_doc_name[-4:len(pandas_doc_name)] != ".csv"):
        pandas_doc_name = pandas_doc_name + ".xlsx"

    # number of column measurement if list_column == "all"
    table = soup.body.find_all("table")
    th = table[number_of_table_on_webPage].find_all("th")
    if list_column == "all":
        list_column = []
        for h in range(0, len(th)):
            list_column.append(h)

    # extraction of strings from the cells of the column choose and cleaning of the table
    for i in list_column:
        liste_wiki_column_contents = []
        table = soup.body.find_all("table")
        # delete of text in tag with display:none
        display_none = table[number_of_table_on_webpage].find_all(attrs={"style":"display:none"})
        if len(display_none) > 0:
            for k in range(0, len(display_none)):
                display_none[k].extract()
        # delete "class="reference""
        class_reference = table[number_of_table_on_webpage].find_all(attrs={"class":"reference"})
        if len(class_reference) > 0:
            for l in range(0, len(class_reference)):
                class_reference[l].extract()    
        th = table[number_of_table_on_webpage].find_all("th")
        column_title = th[i].get_text().replace("\n","")
        tr = table[number_of_table_on_webpage].find_all("tr")
        for j in range(1, len(tr)):
            td = tr[j].find_all("td")
            liste_wiki_column_contents.append(td[i].get_text().replace("\n",""))
            

        # writting in doc excel
        os.chdir("/Users/Alex/perso/files")
        # if the doc exist
        if os.path.exists(pandas_doc_name):
            if pandas_doc_name[-5:len(pandasDocName)] == ".xlsx":
                df = pd.read_excel(pandas_doc_name)
                df[column_title] = liste_wiki_column_contents
                df.to_excel(f"/Users/Alex/perso/files/tableurs/{pandas_doc_name}", index=False)
            elif pandas_doc_name[-4:len(pandas_doc_name)] == ".csv":
                df = pd.read_csv(pandas_doc_name)
                df[column_title] = liste_wiki_column_contents
                df.to_csv(f"/Users/Alex/perso/files/tableurs/{pandas_doc_name}", index=False)
        # if it does not exist
        else:
            df = pd.data_frame({column_title:liste_wiki_column_contents})
            if pandas_doc_name[-5:len(pandas_doc_name)] == ".xlsx":
                df.to_excel(f"/Users/Alex/perso/files/tableurs/{pandas_doc_name}", index=False)
            elif pandas_doc_name[-4:len(pandas_doc_name)] == ".csv":
                df.to_csv(f"/Users/Alex/perso/files/tableurs/{pandas_doc_name}", index=False)

    
