import torch
print("PyTorch version:", torch.__version__)
print("CUDA available:", torch.cuda.is_available())
if torch.cuda.is_available():
    print("GPU name:", torch.cuda.get_device_name(0))
    x = torch.rand(10000, 10000, device="cuda")
    print("Tensor sum:", x.sum().item())
import torchvision
print("torchvision:", torchvision.__version__)
import torchaudio
print("torchaudio:", torchaudio.__version__)
