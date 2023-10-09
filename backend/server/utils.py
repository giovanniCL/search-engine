import re
def pre_process_query(query):
    if not query: return []
    query = query.lower()
    split_query = re.split(r"\s+", query)
    return split_query