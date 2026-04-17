import math
import torch
from PIL.Image import Image
from transformers import CLIPModel, CLIPProcessor
from vector_processor.core import ports, models


class ClipItemEmbedder(ports.ItemEmbedder):
    def __init__(self, model: CLIPModel, processor: CLIPProcessor, device: str):
        super().__init__()

        self.__model = model
        self.__processor = processor
        self.__device = device
        self.__model.eval()

    def get_item_embedding(self, item):
        text_emb = self.__encode_text(self.__prepare_text(item))

        if len(item.photos) < 1:
            image_emb = None
        else:
            image_emb = self.__encode_image(item.photos[0])

        if image_emb is not None:
            text_emb = text_emb / text_emb.norm(dim=-1, keepdim=True)
            image_emb = image_emb / image_emb.norm(dim=-1, keepdim=True)
            emb = 0.5 * text_emb + 0.5 * image_emb
        else:
            emb = text_emb

        emb = emb / emb.norm(dim=-1, keepdim=True)
        nparray = emb.cpu().numpy()[0]

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

    def __encode_text(self, text: str):
        inputs = self.__processor(
            text=[text],
            return_tensors="pt",
            padding=True,
            truncation=True,
        ).to(self.__device)

        with torch.inference_mode():
            emb = self.__model.get_text_features(**inputs)

            if not isinstance(emb, torch.Tensor):
                return emb.pooler_output

            return emb

    def __encode_image(self, image: Image):
        inputs = self.__processor(
            images=image,
            return_tensors="pt"
        ).to(self.__device)

        with torch.inference_mode():
            emb = self.__model.get_image_features(**inputs)

            if not isinstance(emb, torch.Tensor):
                return emb.pooler_output

            return emb
