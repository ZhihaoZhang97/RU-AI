import torch

from languagebind import to_device, transform_dict, LanguageBindImageTokenizer

pretrained_ckpt = f'lb203/LanguageBind_Image'
tokenizer = LanguageBindImageTokenizer.from_pretrained(pretrained_ckpt, cache_dir='tokenizer_cache_dir')

if __name__ == '__main__':
    device = 'cuda:0'
    device = torch.device(device)

    model = torch.load("checkpoints/languagebind_model.pt")
    model = model.to(device)
    model.eval()

    modality_transform = {c: transform_dict[c](model.modality_config[c]) for c in model.clip_type.keys()}

    image_data_paths = ['/path/to/image/data']
    audio_data_paths = ['/path/to/audio/data']
    text_data = ["Sample Text String"]

    inputs = {
        'image': to_device(modality_transform['image'](image_data_paths), device),
        'audio': to_device(modality_transform['audio'](audio_data_paths), device),
        'language': to_device(tokenizer(text_data, max_length=77, padding='max_length',
                                             truncation=True, return_tensors='pt'), device)
    }

    with torch.no_grad():
        output = model(inputs)
    print(output)