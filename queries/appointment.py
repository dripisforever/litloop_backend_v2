

def search(self, term, size):
    if size > 50:
        size = 50

    search_result = self.elastic_service.search(
        query={
            "multi_match": {
                "query": term,
                "fields": ["patient.full_name", "assigned_to.full_name"],
            }
        },
        size=size,
    )
    hits = search_result["hits"]["hits"]
    result = list(
        map(
            lambda x: AppointmentSchema(**x["_source"]),
            hits,
        )
    )
    return result
