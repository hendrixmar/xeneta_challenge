from typing import List

from rapidfuzz import process, fuzz
from sqlalchemy import text

from app.database import Session
from app.ports.utils import PortColumn, generate_port_filter




def get_ports(port_value: str, port_column: PortColumn) -> List[dict[str, str]]:
    temp_query = "select code, name, parent_slug from ports {filter}".format(
        filter=generate_port_filter(port_column, port_column.name, port_value)
    )

    with Session() as session:
        ports_rows = session.execute(text(temp_query)).fetchall()

    return [dict(row) for row in ports_rows]

def fuzzy_search_port(
        string_search: str, list_of_ports: list[dict], number_of_best_candidates: int
) -> list[dict]:
    """
    Find the port that is most similar to the string_search by comparing code, name, parent slug using
    fuzzy matching using the library rapidfuzz.

        Parameters:
                    string_search (str): The word you want to match with the ports
                    list_of_ports (list[dict]): A list of port ports represented as a dictionary
                    number_of_best_candidates (int): Limit the number of results

        Returns:
                best_results (list[List[dict]]): The n number

    """

    # The fuzzy search is applied for each of the dictionary of the list, and it will return a list of
    # tuple for each key word of the dictionary. The tuples have the following structure
    # (value of the key, score from 0 to 100, key of the value)
    # the similarity fuzzy search is done by each value of the dictionary
    list_of_scores = (
        process.extract(string_search, dict(row), scorer=fuzz.WRatio)
        for row in list_of_ports
    )

    # Then sort the tokens based on each of the value have the most score
    # by taking the highest score of the list of tuples as the sort argument
    sorted_scores = sorted(
        list_of_scores,
        key=lambda list_of_tuples: max(element[1] for element in list_of_tuples),
        reverse=True,
    )

    return sorted_scores[:number_of_best_candidates]
