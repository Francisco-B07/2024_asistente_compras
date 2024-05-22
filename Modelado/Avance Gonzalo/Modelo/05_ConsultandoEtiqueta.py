import torch
from torchvision.models import resnet50
from torchvision import transforms

# Cargar el modelo preentrenado ResNet-50
model = resnet50(pretrained=True)
model.eval()

# Obtener las etiquetas del modelo (clasificación de ImageNet)
labels_path = 'https://raw.githubusercontent.com/anishathalye/imagenet-simple-labels/master/imagenet-simple-labels.json'
labels = torch.hub.load_state_dict_from_url(labels_path)

# Índice de clase predicho (por ejemplo, 584)
predicted_index = 584

# Obtener la etiqueta correspondiente al índice
predicted_label = labels[predicted_index]

print(f"Etiqueta predicha: {predicted_label}")