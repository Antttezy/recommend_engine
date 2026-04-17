import math
import torch
from PIL.Image import Image
from transformers import CLIPModel, CLIPProcessor
from transformers.models.clip.modeling_clip import CLIPOutput
from vector_processor.core import ports, models, errors


class ClipItemEmbedder(ports.ItemEmbedder):
    def __init__(self, model: CLIPModel, processor: CLIPProcessor, device: str):
        super().__init__()

        self.__model = model
        self.__processor = processor
        self.__device = device
        self.__model.eval()

    def get_item_embedding(self, item):
        prepared_text = self.__prepare_text(item)

        if len(item.photos) < 1:
            raise errors.EmbeddingError("image required to create an embedding")
        else:
            embedding = self.__encode_text_with_image(prepared_text, item.photos[0])

        embedding = embedding / embedding.norm(dim=-1, keepdim=True)
        nparray = embedding.cpu().numpy()[0]

        return models.Embedding(data=nparray.tolist())

    def __prepare_text(self, item: models.ItemInfo):
        log_price = math.log1p(item.price)

        attrs = item.attributes
        attrs = ", ".join(f"{k}: {v}" for k, v in attrs.items())

        return (
            f"{item.name}. "
            f"{item.description}. "
            f"{attrs}. "
            f"price_log={log_price:.4f}"
        )

    def __encode_text_with_image(self, text: str, image: Image):
        inputs = self.__processor(
            text=[text],
            images=image,
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.__device)

        with torch.inference_mode():
            emb: CLIPOutput = self.__model(**inputs)
            return 0.5 * emb.image_embeds + 0.5 * emb.text_embeds
