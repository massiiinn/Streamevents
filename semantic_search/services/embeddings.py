import threading
from sentence_transformers import SentenceTransformer

# Nom del model multilingüe que s'utilitzarà per generar els embeddings
_MODEL_NAME = "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
# Lock per garantir que només un thread carregui el model a la vegada
_lock = threading.Lock()
# Variable global per emmagatzemar el model carregat
_model = None

def get_model():
    """
    Carrega el model de forma lazy i thread-safe.
    Només es carrega una vegada en memòria.
    """
    global _model
    # Si el model no està carregat
    if _model is None:
        # Bloquejem per evitar que múltiples threads elcarreguin simultàniament
        with _lock:
            # Double-check: si un altre thread ja l'ha carregat, no ho fem de nou
            if _model is None:
                print(f"Carregant model: {_MODEL_NAME}...")
                _model = SentenceTransformer(_MODEL_NAME)
                print("Model carregat correctament.")
    return _model

def embed_text(text: str) -> list[float]:
    """
    Converteix un text en un vector d'embedding normalitzat.
    
    Args:
        text: Text a convertir
        
    Returns:
        Llista de floats que representen l'embedding
    """
    # Netegem el text d'espais en blanc
    text = (text or "").strip()
    # Si el text és buit, retornem una llista buida
    if not text:
        return []
    
    # Obtenim el model
    model = get_model()
    # Generem l'embedding normalitzat (vector de 384 dimensions)
    vec = model.encode([text], normalize_embeddings=True)[0]
    # Convertim el numpy array a llista de Python
    return vec.tolist()

def model_name() -> str:
    """Retorna el nom del model utilitzat."""
    return _MODEL_NAME