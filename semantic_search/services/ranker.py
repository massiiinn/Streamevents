import numpy as np

def cosine_top_k(query_vec: list[float], items: list[tuple[object, list[float]]], k: int = 20):
    """
    Calcula la similitud cosinus entre el vector de la query i una llista d'ítems,
    retornant els k elements més similars.
    
    Args:
        query_vec: Vector de la cerca de l'usuari
        items: Llista de tuples (objecte_esdeveniment, embedding)
        k: Nombre màxim de resultats a retornar (per defecte 20)
        
    Returns:
        Llista de tuples (objecte, score) ordenada per score descendent
    """
    # Si no hi ha vector de query, no podem fer res
    if not query_vec:
        return []

    # Convertim el vector de query a numpy array
    q = np.array(query_vec, dtype=np.float32)
    # Si el vector té norma 0 (vector buit), no podem calcular similitud
    if np.linalg.norm(q) == 0:
        return []

    # Llista per emmagatzemar els resultats amb els seus scores
    scored = []
    # Recorrem cada esdeveniment amb el seu embedding
    for obj, emb in items:
        # Si l'embedding està buit, el saltem
        if not emb:
            continue
        # Convertim l'embedding a numpy array
        v = np.array(emb, dtype=np.float32)
        # Comprovem que els vectors tenen la mateixa dimensió i no són buits
        if v.shape != q.shape or np.linalg.norm(v) == 0:
            continue
        # Calculem el producte escalar (com els vectors estan normalitzats, això és la similitud cosinus)
        score = float(np.dot(q, v))
        # Afegim l'esdeveniment i el seu score a la llista
        scored.append((obj, score))

    # Ordenem per score descendent (el més similar primer)
    scored.sort(key=lambda x: x[1], reverse=True)
    # Retornem només els k primers resultats
    return scored[:k]