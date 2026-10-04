from diffusers import DiffusionPipeline
import torch
import os

pipe = DiffusionPipeline.from_pretrained(
    "segmind/tiny-sd",
    torch_dtype=torch.float32
)

pipe = pipe.to("cpu")

prompt = """
A natural realistic photograph of a single Indian farmer working in his field.
He is planting crops by hand in the soil.
He is wearing simple everyday farmer clothes.
Green crops around him, real village farmland, natural daylight,
ordinary rural life, realistic skin and clothing, candid photography,
no studio lighting, no fantasy, no family.
"""

image = pipe(prompt).images[0]

os.makedirs("images", exist_ok=True)

image.save("images/natural_farmer.png")
image.show()