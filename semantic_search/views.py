from django.shortcuts import render
from django.utils import timezone

from events.models import Event
from .services.embeddings import embed_text, model_name
from .services.ranker import cosine_top_k

def _event_text(e: Event) -> str:
    """
    Funció auxiliar que concatena els camps rellevants d'un esdeveniment
    per generar un text complet que representa l'esdeveniment.
    """
    # Agafem els camps més importants de l'esdeveniment
    parts = [
        e.title or "",
        e.description or "",
        e.category or "",
        e.tags or "",
    ]
    # Els unim amb el separador | i eliminem camps buits
    return " | ".join([p.strip() for p in parts if p and p.strip()])

def semantic_search(request):
    """
    Vista principal de la cerca semàntica.
    Processa la query de l'usuari, la converteix en vector,
    compara amb els esdeveniments i retorna els més similars.
    """
    # Obtenim la query de l'usuari des del paràmetre GET
    q = (request.GET.get("q") or "").strip()
    # Comprovem si l'usuari vol filtrar només esdeveniments futurs
    only_future = request.GET.get("future") == "1"

    # Inicialitzem variables per emmagatzemar resultats i temps de cerca
    results = []
    search_time = None
    
    # Si hi ha text de cerca, processem la petició
    if q:
        import time
        start_time = time.time()
        
        # Convertim la query de l'usuari en un vector d'embedding
        q_vec = embed_text(q)

        # Obtenim només els camps necessaris per millorar el rendiment
        all_events = Event.objects.only('id', 'title', 'description', 'category', 'tags', 'scheduled_date', 'embedding')
        
        # Preparem la llista d'esdeveniments amb els seus embeddings
        items = []
        for e in all_events:
            # Si volem només futurs, filtrem els que ja han passat
            if only_future and e.scheduled_date < timezone.now():
                continue
            
            # Obtenim l'embedding de l'esdeveniment
            emb = getattr(e, "embedding", None)
            # Validem que l'embedding sigui vàlid (llista amb contingut)
            if emb and isinstance(emb, list) and len(emb) > 0:
                items.append((e, emb))

        # Calculem la similitud i obtenim els 20 més rellevants
        ranked = cosine_top_k(q_vec, items, k=20)
        
        # Filtrem resultats amb score mínim de 0.2 (20% de similitud)
        results = [(e, s) for e, s in ranked if s > 0.2]
        
        # Calculem el temps de cerca en mil·lisegons
        search_time = round((time.time() - start_time) * 1000, 2)

    # Preparem el context per al template
    context = {
        "query": q,
        "results": results, 
        "only_future": only_future,
        "embedding_model": model_name(),
        "search_time": search_time,
        "total_results": len(results),
    }
    return render(request, "semantic_search/search.html", context)