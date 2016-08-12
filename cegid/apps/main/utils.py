from cegid.settings import PUBMED_SEARCH_TERMS
import datetime
import requests

def get_pubmed_articles(search_terms=None,number=40,year=None):
    '''get_pubmed_articles will retrieve a list of articles to render into visualization
    See helix(N) in the index.html template for the number, 20 per helix = 40 total.
    :param search_terms: a list of search terms for the query, default is AND
    :param number: the number of articles to retrieve
    :param year: the year to retrieve. Default will return current year
    '''
    if search_terms == None:
        search_terms = PUBMED_SEARCH_TERMS
    if not isinstance(search_terms,list):
        search_terms = [search_terms]

    # Add search terms to query
    search_base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi?db=pubmed&term="
    retrieval_base = "http://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?db=pubmed&retmode=json&rettype=abstract&id="
    search_terms = "%5d+AND+".join(search_terms)
    url = "%s%s" %(search_base,search_terms)
    
    # If the user doesn't provide a year, use current
    if year == None:
        now = datetime.datetime.now()
        year = str(now.year)

    url = url + "+AND+%s" %year + "%5bpdat%5d&retmode=json&retmax=" + str(number)
    pmids = get_result(url)
    if pmids != None:
        if "esearchresult" in pmids:
            if "idlist" in pmids["esearchresult"]:
                pmids = pmids["esearchresult"]["idlist"]
                if len(pmids) > 0:
                    pmids = ",".join(pmids)
                    url = "%s%s" %(retrieval_base,pmids)
                    return get_result(url)
    return None



def get_result(url,return_json=True):
    '''get_result will use requests to retrieve a web page result. If not possible, None is returned
    :param url: the url to retrieve
    '''
    result = requests.get(url)
    if result.status_code == 200:
        if return_json == True:
            return result.json()
        return result
    return None
