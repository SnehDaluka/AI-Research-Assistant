from backend.config import SIMILARITY_THRESHOLD

def build_prompt(query, search_results):
    relevant_results = [
        result
        for result in search_results
        if result["score"] >= SIMILARITY_THRESHOLD
    ]
    
    if not relevant_results:
        return None
    
    context = "\n".join([f"[{i+1}] \n {result['text']} \n\n {'-' * 50} \n\n" for i, result in enumerate(relevant_results)])
    

    return (
        f"Context:\n{context}"
        f"Question: \n\n{query}"
    )