print("so far so good")
import torch
from torchvision import transforms
from PIL import Image
import pandas as pd
import numpy as np


class GarbagePredict():
    
    def __init__(self, labels_file='index_to_label.csv'):
        self.model = torch.load('ResNet_Transfer_model.pkl', map_location=torch.device('cpu'))
        self.model.eval()
        self.labels = pd.read_csv(labels_file)
        print('Model Loaded')

    def predict(self, image):
        img_transform = transforms.Compose([
              transforms.Resize(256),
              transforms.CenterCrop(224),
              transforms.ToTensor(),
          ])

        image = img_transform(image).unsqueeze(dim=0)
        pred_tensor = self.model(image)
        pred_tensor_np = pred_tensor.detach().numpy()[0]
        #plt = sns.barplot(x=self.labels.iloc[:,1], y=pred_tensor_np)

        prediction = torch.max(pred_tensor, dim=1)[1].item()
        label, suggestions = (self.labels.iloc[prediction, 1], self.labels.iloc[prediction, 2:])
        return label, suggestions

if __name__ == '__main__':
    test = GarbagePredict()
    testimg = Image.open('cardboard10.jpg').convert('RGB')
    print(test.predict(testimg)[0])

