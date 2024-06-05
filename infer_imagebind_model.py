from types import SimpleNamespace

import torch

from imagebind import data

ModalityType = SimpleNamespace(
    VISION="vision",
    TEXT="text",
    AUDIO="audio",
    THERMAL="thermal",
    DEPTH="depth",
    IMU="imu",
)

if __name__ == '__main__':
    device = 'cuda:0'
    device = torch.device(device)

    model = torch.load("checkpoints/imagebind_model.pt")
    model = model.to(device)
    model.eval()

    image_data_paths = ['/path/to/image/data']
    audio_data_paths = ['/path/to/audio/data']
    text_data = ["Sample Text String"]

    inputs = {
        ModalityType.VISION: data.load_and_transform_vision_data(image_data_paths, device),
        ModalityType.AUDIO: data.load_and_transform_audio_data(audio_data_paths, device),
        ModalityType.TEXT: data.load_and_transform_text(text_data, device)
    }

    with torch.no_grad():
        output = model(inputs)
    print(output)
    