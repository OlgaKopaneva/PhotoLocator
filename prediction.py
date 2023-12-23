import torch
import torchvision.models as models
import torch.nn as nn
from torchvision import transforms
from PIL import Image


model = models.resnet50(pretrained=False)
fc_new = nn.Linear(in_features=2048, out_features=11, bias=True)
model.fc = fc_new
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model.load_state_dict(torch.load('classification_resnet.pth', map_location=torch.device('cpu')))

model.eval()

def predict(image_path: str):
    decode_dict = {
        0: 'all_souls',
        1: 'ashmolean',
        2: 'balliol',
        3: 'bodleian',
        4: 'christ_church',
        5: 'cornmarket',
        6: 'hertford',
        7: 'keble',
        8: 'magdalen',
        9: 'pitt_rivers',
        10: 'radcliffe_camera'
    }
    image = Image.open(image_path)
     # Преобразование изображения для модели
    transform = transforms.Compose([
        transforms.Resize((224, 224)),
        transforms.ToTensor(),
    ])
    image = transform(image)
    image = image.unsqueeze(0)  # Добавить батч размерность
    # Предсказание
    with torch.no_grad():
        outputs = model(image)
        _, predicted = torch.max(outputs.data, 1)
    predicted_class = decode_dict[predicted.item()]
    # Отправка ответа
    return predicted_class
