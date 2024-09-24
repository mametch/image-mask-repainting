import matplotlib.pyplot as plt
import torch
import torchvision
from PIL import Image
from torchvision import transforms


class InferenceSegm:
    def __init__(self) -> None:
        self.model = torchvision.models.segmentation.deeplabv3_resnet101(
            pretrained=True
        )
        self.model.eval()
        self.preprocess = transforms.Compose(
            [
                transforms.Resize(520),
                transforms.ToTensor(),
                transforms.Normalize(
                    mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]
                ),
            ]
        )
        self.human_index = 15

    def inference(self, input_image):
        input_tensor = self.preprocess(input_image)
        input_batch = input_tensor.unsqueeze(0)

        if torch.cuda.is_available():
            input_batch = input_batch.to("cuda")
            self.model.to("cuda")

        with torch.no_grad():
            output = self.model(input_batch)["out"][0]

        output_predictions = output.argmax(0)
        human_mask = (output_predictions == self.human_index).float()

        return human_mask.cpu().numpy()


if __name__ == "__main__":
    input_img = Image.open("test_img/2024-09-24_20-19-02_0.png")
    infSeg = InferenceSegm()
    mask = infSeg.inference(input_img)

    plt.imshow(mask, cmap="gray")
    plt.show()
