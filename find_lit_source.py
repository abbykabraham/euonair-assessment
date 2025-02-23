import arxiv
import logging
import os
import pandas as pd
import datetime
from openai_analysis import analyze_abstract_openai


# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def search_publications(query, start_year, end_year, limit = 5) -> list[dict]:
    """
    Literature search using the arXiv API

    Parameters:
        query (str): search query
        start_year (int): publications from...
        end_year (int): publication till...
        limit (int): Max no. of publication

    Returns:
        List[dict]: contains publications metadata
    """
    # ArXiv search object with the desired query and parameters
    search = arxiv.Search(
        query=query,
        max_results=limit,
        # sort_by=arxiv.SortCriterion.SubmittedDate,
        sort_by=arxiv.SortCriterion.Relevance
    )
    # ArXiv Client 
    client = arxiv.Client(page_size=limit)
    results = list(client.results(search))
    
    publications = []
    for result in results:
        pub_year = result.published.year if result.published else None
        logger.info(f"Paper: {result.title}, published: {pub_year}")
        
        if pub_year is not None and (pub_year < start_year or pub_year > end_year):
            continue

        publication = {
            "title": result.title or "N/A",
            "authors": ", ".join([author.name for author in result.authors]) if result.authors else "N/A",
            "year": pub_year if pub_year is not None else "N/A",
            "doi": result.doi or "N/A",
            "url": result.pdf_url or "N/A",
            "abstract": result.summary or "N/A"
        }
        publications.append(publication)
    return publications

def save_lit_to_csv(publications, folder = "data", suffix = "") -> None:
    if not os.path.exists(folder):
        os.makedirs(folder)
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.join(folder, f"publications_{timestamp}{suffix}.csv")
    df = pd.DataFrame(publications)
    df.to_csv(filename, index=False)
    logger.info(f"Saved {len(publications)} publications to {filename}")

def main():
    query = 'machine learning AND additive manufacturing'
    start_year = 2020
    end_year = 2025
    limit = 10

    publications = search_publications(query, start_year, end_year, limit)

    if not publications:
        print("No publications found or an error occurred.")
        return

    print("Publications found:\n")
    for pub in publications:
        print(f"Title: {pub['title']}")
        print(f"Authors: {pub['authors']}")
        print(f"Year: {pub['year']}")
        print(f"DOI: {pub['doi']}")
        print(f"URL: {pub['url']}")
        print(f"Abstract: {pub['abstract']}\n")
        print("-" * 80)
    
    # Save data to CSV
    save_lit_to_csv(publications, suffix="_raw")

    for pub in publications:
        try:
            analysis = analyze_abstract_openai(pub["abstract"])
            pub.update(analysis)
        except Exception as e:
            logger.error(f"Error analyzing abstract for paper '{pub['title']}': {e}")
            pub.update({
                "research_question": "Not identified",
                "objective": "Not identified",
                "contribution": "Not identified"
            })
    
    # Save analyzed data to CSV
    save_lit_to_csv(publications, suffix="_analyzed")

if __name__ == "__main__":
    main()
