import os
import sys
import pytest
import pandas as pd

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from find_lit_source import search_publications, save_lit_to_csv
from openai_analysis import analyze_abstract_openai

# Sample parameters for testing
SAMPLE_QUERY = "machine learning AND additive manufacturing"
START_YEAR = 2020
END_YEAR = 2025
LIMIT = 3

@pytest.fixture
def sample_publications():
    pubs = search_publications(SAMPLE_QUERY, START_YEAR, END_YEAR, LIMIT)
    assert isinstance(pubs, list)
    return pubs

def test_search_publications(sample_publications):
    """
    Test that search_publications returns a list of dictionaries with expected keys
    """
    expected_keys = {"title", "authors", "year", "doi", "url", "abstract"}
    for pub in sample_publications:
        missing = expected_keys - set(pub.keys())
        assert not missing, f"Publication is missing keys: {missing}"

def test_save_lit_to_csv(tmp_path, sample_publications):
    """
    Test that save_lit_to_csv creates CSV file with expected columns
    """
    data_folder = tmp_path / "data"
    data_folder.mkdir(exist_ok=True)
    save_lit_to_csv(sample_publications, folder=str(data_folder), suffix="_test")
    
    # Check for one CSV file
    csv_files = list(data_folder.glob("*.csv"))
    assert len(csv_files) > 0, "No CSV file was created."
    
    # Check for the expected columns in CSV file
    df = pd.read_csv(csv_files[0])
    expected_columns = {"title", "authors", "year", "doi", "url", "abstract"}
    missing_columns = expected_columns - set(df.columns)
    assert not missing_columns, f"CSV file is missing columns: {missing_columns}"

def test_analyze_abstract_openai():
    """
    Test that analyze_abstract_openai returns a dictionary with the keys
    'research_question', 'objective', and 'contribution'.
    """
    if not os.getenv("OPENAI_API_KEY"):
        pytest.skip("OPENAI_API_KEY not set.")
    
    sample_abstract = (
        "Abstract: In this study, we investigate how generative AI has transformed manufacturing industries. "
        "Our objective is to develop a novel algorithm to optimize production, "
        "and we demonstrate that our approach significantly improves production efficiency."
    )
    result = analyze_abstract_openai(sample_abstract)
    assert isinstance(result, dict), "Result not a dictionary."
    
    required_keys = {"research_question", "objective", "contribution"}
    missing_keys = required_keys - set(result.keys())
    assert not missing_keys, f"Analysis result having missing keys: {missing_keys}"
    
    # Check the extracted values are not default "Not identified".
    for key in required_keys:
        assert result[key] != "Not identified", f"{key} was not properly extracted."

if __name__ == "__main__":
    pytest.main()
