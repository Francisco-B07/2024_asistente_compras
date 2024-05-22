import torch
import torchvision.transforms as transforms
from torchvision.models import resnet50
from PIL import Image

# Cargar el modelo preentrenado ResNet-50
model = resnet50(pretrained=True)
model.eval()

# Transformaciones de imagen
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
])

# Cargar una imagen de fruta o verdura
image_path = 'prueba\Ajo En Bolsita (Kg).jpg'
image = Image.open(image_path)
image_tensor = transform(image).unsqueeze(0)

# Clasificar la imagen
with torch.no_grad():
    output = model(image_tensor)
    _, predicted_class = output.max(1)

# Etiqueta predicha (índice de clase)
print(f"Clase predicha: {predicted_class.item()}")
