from rapidfuzz import process, fuzz
from fastapi import FastAPI
from sqlalchemy import text
from db.init_db import Session

lol = [{"code": "CNCWN", "name": "Chiwan", "parent_slug": "china_south_main"},
       {"code": "IESNN", "name": "Shannon", "parent_slug": "north_europe_sub"},
       {"code": "FRLVE", "name": "Le Verdon-sur-Mer", "parent_slug": "north_europe_sub"},
       {"code": "NOOSL", "name": "Oslo", "parent_slug": "norway_south_east"},
       {"code": "GBPME", "name": "Portsmouth", "parent_slug": "uk_sub"},
       {"code": "NOSVG", "name": "Stavanger", "parent_slug": "norway_south_west"},
       {"code": "FIHEL", "name": "Helsingfors (Helsinki)", "parent_slug": "finland_main"},
       {"code": "NOMAY", "name": "Måløy", "parent_slug": "scandinavia"},
       {"code": "FRLIO", "name": "Lyon", "parent_slug": "north_europe_sub"},
       {"code": "SEHAD", "name": "Halmstad", "parent_slug": "kattegat"},
       {"code": "GBTIL", "name": "Tilbury", "parent_slug": "uk_sub"},
       {"code": "DKCPH", "name": "Copenhagen (København)", "parent_slug": "kattegat"},
       {"code": "NOFRK", "name": "Fredrikstad", "parent_slug": "norway_south_east"},
       {"code": "CNYAT", "name": "Yantai", "parent_slug": "china_east_main"},
       {"code": "CNSNZ", "name": "Shenzhen", "parent_slug": "china_south_main"},
       {"code": "NOSKE", "name": "Skien", "parent_slug": "scandinavia"},
       {"code": "DEWVN", "name": "Wilhelmshaven", "parent_slug": "north_europe_sub"},
       {"code": "NOKSU", "name": "Kristiansund", "parent_slug": "norway_north_west"},
       {"code": "SEMMA", "name": "Malmö", "parent_slug": "kattegat"},
       {"code": "FIRAA", "name": "Brahestad (Raahe)", "parent_slug": "baltic"},
       {"code": "FRDKK", "name": "Dunkerque", "parent_slug": "north_europe_sub"},
       {"code": "GBLON", "name": "London", "parent_slug": "uk_sub"},
       {"code": "NOSVE", "name": "Svelgen", "parent_slug": "norway_north_west"},
       {"code": "FRBAS", "name": "Bassens", "parent_slug": "north_europe_sub"},
       {"code": "NLMOE", "name": "Moerdijk", "parent_slug": "north_europe_sub"},
       {"code": "IEDUB", "name": "Dublin", "parent_slug": "north_europe_sub"},
       {"code": "FRDPE", "name": "Dieppe", "parent_slug": "north_europe_sub"},
       {"code": "FIKOK", "name": "Karleby (Kokkola)", "parent_slug": "baltic"},
       {"code": "NLRTM", "name": "Rotterdam", "parent_slug": "north_europe_main"},
       {"code": "GBLTP", "name": "London Thamesport", "parent_slug": "uk_sub"},
       {"code": "BEZEE", "name": "Zeebrugge", "parent_slug": "north_europe_main"},
       {"code": "FIOUL", "name": "Uleåborg (Oulu)", "parent_slug": "baltic"},
       {"code": "NOFUS", "name": "Fusa", "parent_slug": "scandinavia"},
       {"code": "FRNEG", "name": "Bougenais", "parent_slug": "north_europe_sub"},
       {"code": "DEBRE", "name": "Bremen", "parent_slug": "north_europe_sub"},
       {"code": "SENRK", "name": "Norrköping", "parent_slug": "stockholm_area"},
       {"code": "RUKDT", "name": "Kronshtadt", "parent_slug": "baltic"},
       {"code": "FRLRH", "name": "La Rochelle", "parent_slug": "north_europe_sub"},
       {"code": "FIMTY", "name": "Mantyluoto", "parent_slug": "baltic"},
       {"code": "NOIKR", "name": "Ikornnes", "parent_slug": "scandinavia"},
       {"code": "DKFRC", "name": "Fredericia", "parent_slug": "kattegat"},
       {"code": "NOHVI", "name": "Håvik", "parent_slug": "norway_south_west"},
       {"code": "FRMTX", "name": "Montoir-de-Bretagne", "parent_slug": "north_europe_sub"},
       {"code": "FIKTK", "name": "Kotka", "parent_slug": "finland_main"},
       {"code": "EEMUG", "name": "Muuga", "parent_slug": "baltic"},
       {"code": "PLSZZ", "name": "Szczecin", "parent_slug": "baltic"},
       {"code": "NOUME", "name": "Straume Industriområde", "parent_slug": "norway_south_west"},
       {"code": "CNSHK", "name": "Shekou", "parent_slug": "china_south_main"},
       {"code": "GBTEE", "name": "Teesport", "parent_slug": "uk_sub"},
       {"code": "FRBOD", "name": "Bordeaux", "parent_slug": "north_europe_sub"},
       {"code": "FRLEH", "name": "Le Havre", "parent_slug": "north_europe_main"},
       {"code": "HKHKG", "name": "Hong Kong", "parent_slug": "china_south_main"},
       {"code": "SESOE", "name": "Södertälje", "parent_slug": "stockholm_area"},
       {"code": "NOHAL", "name": "Halden", "parent_slug": "scandinavia"},
       {"code": "ESGIJ", "name": "Gijón", "parent_slug": "north_europe_sub"},
       {"code": "NOBVG", "name": "Berlevåg", "parent_slug": "scandinavia"},
       {"code": "IEORK", "name": "Cork", "parent_slug": "north_europe_sub"},
       {"code": "DEBRV", "name": "Bremerhaven", "parent_slug": "north_europe_main"},
       {"code": "ESZAZ", "name": "Zaragoza", "parent_slug": "north_europe_sub"},
       {"code": "SEWAL", "name": "Wallhamn", "parent_slug": "scandinavia"},
       {"code": "CNNBO", "name": "Ningbo", "parent_slug": "china_east_main"},
       {"code": "NOFRO", "name": "Florø", "parent_slug": "scandinavia"},
       {"code": "CNDAL", "name": "Dalian", "parent_slug": "china_north_main"},
       {"code": "GBMNC", "name": "Manchester", "parent_slug": "uk_sub"},
       {"code": "PLGDY", "name": "Gdynia", "parent_slug": "poland_main"},
       {"code": "CNSGH", "name": "Shanghai", "parent_slug": "china_east_main"},
       {"code": "FITKU", "name": "Åbo (Turku)", "parent_slug": "baltic"},
       {"code": "GBHUL", "name": "Hull", "parent_slug": "uk_sub"},
       {"code": "ESVGO", "name": "Vigo", "parent_slug": "north_europe_sub"},
       {"code": "SEHEL", "name": "Helsingborg", "parent_slug": "kattegat"},
       {"code": "NOMOL", "name": "Molde", "parent_slug": "norway_north_west"},
       {"code": "NOTON", "name": "Tønsberg", "parent_slug": "norway_south_east"},
       {"code": "CNHDG", "name": "Huadu Pt", "parent_slug": "china_south_main"},
       {"code": "BEANR", "name": "Antwerpen", "parent_slug": "north_europe_main"},
       {"code": "FIRAU", "name": "Rauma (Raumo)", "parent_slug": "finland_main"},
       {"code": "PLGDN", "name": "Gdansk", "parent_slug": "poland_main"},
       {"code": "NODRM", "name": "Drammen", "parent_slug": "norway_south_east"},
       {"code": "NOSAS", "name": "Sandnes", "parent_slug": "norway_south_west"},
       {"code": "NOKRS", "name": "Kristiansand", "parent_slug": "norway_south_east"},
       {"code": "NOSUN", "name": "Sunndalsøra", "parent_slug": "scandinavia"},
       {"code": "GBBEL", "name": "Belfast", "parent_slug": "uk_sub"},
       {"code": "DKAAR", "name": "Århus", "parent_slug": "kattegat"},
       {"code": "FRURO", "name": "Rouen", "parent_slug": "north_europe_sub"},
       {"code": "GBLGP", "name": "London Gateway Port", "parent_slug": "uk_sub"},
       {"code": "SEAHU", "name": "Åhus", "parent_slug": "scandinavia"},
       {"code": "NOBVK", "name": "Brevik", "parent_slug": "norway_south_east"},
       {"code": "FRANT", "name": "Antibes", "parent_slug": "north_europe_sub"},
       {"code": "RUARH", "name": "Arkhangelsk", "parent_slug": "russia_north_west"},
       {"code": "NOTOS", "name": "Tromsø", "parent_slug": "scandinavia"},
       {"code": "SEGOT", "name": "Gothenburg (Göteborg)", "parent_slug": "kattegat"},
       {"code": "FIIMA", "name": "Imatra", "parent_slug": "baltic"},
       {"code": "FIKEM", "name": "Kemi/Torneå (Kemi/Tornio)", "parent_slug": "baltic"},
       {"code": "GBGRG", "name": "Grangemouth", "parent_slug": "uk_sub"},
       {"code": "EETLL", "name": "Tallinn", "parent_slug": "baltic_main"},
       {"code": "FIHMN", "name": "Fredrikshamn (Hamina)", "parent_slug": "baltic"},
       {"code": "RULED", "name": "Saint Petersburg (ex Leningrad)", "parent_slug": "baltic"},
       {"code": "GBLIV", "name": "Liverpool", "parent_slug": "uk_sub"},
       {"code": "CNGGZ", "name": "Guangzhou", "parent_slug": "china_south_main"},
       {"code": "NOTRD", "name": "Trondheim", "parent_slug": "norway_north_west"},
       {"code": "FRIRK", "name": "Dunkirk", "parent_slug": "north_europe_sub"},
       {"code": "FRNTE", "name": "Nantes", "parent_slug": "north_europe_sub"},
       {"code": "CNQIN", "name": "Qingdao", "parent_slug": "china_east_main"},
       {"code": "RULUG", "name": "Lugovoye", "parent_slug": "baltic"},
       {"code": "GBBRS", "name": "Bristol", "parent_slug": "uk_sub"},
       {"code": "GBGOO", "name": "Goole", "parent_slug": "uk_sub"},
       {"code": "CNLYG", "name": "Lianyungang", "parent_slug": "china_east_main"},
       {"code": "GBTHP", "name": "Thamesport", "parent_slug": "uk_sub"},
       {"code": "NOHAU", "name": "Haugesund", "parent_slug": "norway_south_west"},
       {"code": "LVRIX", "name": "Riga", "parent_slug": "baltic_main"},
       {"code": "DKAAL", "name": "Aalborg", "parent_slug": "scandinavia"},
       {"code": "GBFXT", "name": "Felixstowe", "parent_slug": "uk_main"},
       {"code": "NOMSS", "name": "Moss", "parent_slug": "norway_south_east"},
       {"code": "NLAMS", "name": "Amsterdam", "parent_slug": "north_europe_sub"},
       {"code": "FOTHO", "name": "Thorshavn", "parent_slug": "scandinavia"},
       {"code": "NOHYR", "name": "Høyanger", "parent_slug": "scandinavia"},
       {"code": "NOTAE", "name": "Tananger", "parent_slug": "scandinavia"},
       {"code": "CNTXG", "name": "Xingang (Tianjin New Pt)", "parent_slug": "china_north_main"},
       {"code": "SEGVX", "name": "Gävle", "parent_slug": "stockholm_area"},
       {"code": "GBSOU", "name": "Southampton", "parent_slug": "uk_main"},
       {"code": "CNXAM", "name": "Xiamen", "parent_slug": "china_east_main"},
       {"code": "RUULU", "name": "Ust'-Luga", "parent_slug": "baltic"},
       {"code": "NOBGO", "name": "Bergen", "parent_slug": "norway_south_west"},
       {"code": "ESMPG", "name": "Marin, Pontevedra", "parent_slug": "north_europe_sub"},
       {"code": "DEHAM", "name": "Hamburg", "parent_slug": "north_europe_main"},
       {"code": "SEOXE", "name": "Oxelösund", "parent_slug": "stockholm_area"},
       {"code": "NOLAR", "name": "Larvik", "parent_slug": "norway_south_east"},
       {"code": "CNYTN", "name": "Yantian", "parent_slug": "china_south_main"},
       {"code": "ISREY", "name": "Reykjavík", "parent_slug": "scandinavia"},
       {"code": "ESBIO", "name": "Bilbao", "parent_slug": "north_europe_sub"},
       {"code": "ISGRT", "name": "Grundartangi", "parent_slug": "scandinavia"},
       {"code": "NOGJM", "name": "Gjemnes", "parent_slug": "scandinavia"},
       {"code": "FRBES", "name": "Brest", "parent_slug": "north_europe_sub"},
       {"code": "NOORK", "name": "Orkanger", "parent_slug": "norway_north_west"},
       {"code": "NOAES", "name": "Ålesund", "parent_slug": "norway_north_west"},
       {"code": "SESTO", "name": "Stockholm", "parent_slug": "stockholm_area"},
       {"code": "GBIMM", "name": "Immingham", "parent_slug": "uk_sub"},
       {"code": "LTKLJ", "name": "Klaipeda", "parent_slug": "baltic_main"},
       {"code": "RUKGD", "name": "Kaliningrad", "parent_slug": "baltic"},
       {"code": "GBGRK", "name": "Greenock", "parent_slug": "uk_sub"},
       {"code": "SEPIT", "name": "Piteå", "parent_slug": "scandinavia"},
       {"code": "ESVIT", "name": "Vitoria-Gasteiz", "parent_slug": "north_europe_sub"},
       {"code": "DKEBJ", "name": "Esbjerg", "parent_slug": "scandinavia"},
       {"code": "GBSSH", "name": "South Shields", "parent_slug": "uk_sub"}]

choices = ["Atlanta Falcons", "New York Jets", "New York Giants", "Dallas Cowboys"]


def fuzzy_search_port(string_search: str, list_of_ports: list[dict], number_of_best_candidates: int) -> list[list[tuple[str, int | float, str]]]:
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
    list_of_scores = (process.extract(string_search, row, scorer=fuzz.WRatio) for row in list_of_ports)

    # Then it necessary to sort the value based on each of the value have the most score
    # by taking the highest score of the list of tuples as the sort argument
    sorted_scores = sorted(list_of_scores,
                           key=lambda list_of_tuples: max(element[1] for element in list_of_tuples), reverse=True)

    return sorted_scores[: number_of_best_candidates]


with Session() as session:
    #query = text('select code, name, parent_slug from ports')
    query = text("select false where "
                 "EXISTS (select code from ports where ports.code = 'DKAAL' or ports.)")

    query = text("select (select false from ports where ports.code = 'DKAAL'), "
                 "(select true from ports where ports.name = 'DKAAxL'), "
                 "(select true from ports where ports.parent_slug = 'DKxAAL');")
    results = session.execute(query).fetchone()

print(results, any(results))
"""
temp = fuzzy_search_port("Amsterdamse", results, 4)
for element in temp:
    print(element)
"""