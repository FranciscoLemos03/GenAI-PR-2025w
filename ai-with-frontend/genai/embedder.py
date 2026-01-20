from sentence_transformers import SentenceTransformer

class Embedder:
    def __init__(self, model_name="BAAI/bge-small-en-v1.5", device="cpu"):
        """
        Initializes the BGE-small model which supports up to 512 tokens.
        BGE-small is superior to MiniLM for research-grade semantic accuracy.
        """
        self.model = SentenceTransformer(model_name, device=device)
        self.model.max_seq_length = 512 

    def encode(self, text: str):
        """
        Generates L2-normalized embeddings using the built-in normalization.
        Normalized embeddings allow you to use Dot Product as a fast Cosine Similarity.
        """
        # We use normalize_embeddings=True to handle the L2 math automatically.
        emb = self.model.encode(
            text, 
            normalize_embeddings=True, 
            convert_to_numpy=True)
        return emb.tolist()