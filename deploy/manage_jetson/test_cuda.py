import torch
import torchvision
print(torchvision.__version__)
print(torch.__version__)
print('CUDA available: ' + str(torch.cuda.is_available()))  # Should be True
print('cuDNN version: ' + str(torch.backends.cudnn.version()))
#torch.tensor(data, dtype=*, device='cuda')
a = torch.cuda.FloatTensor(2).zero_()
print('Tensor a = ' + str(a))
b = torch.randn(2).cuda()
print('Tensor b = ' + str(b))
c = a + b
print('Tensor c = ' + str(c))

print("PyTorch Version:", torch.__version__)
print("CUDA Version:", torch.version.cuda)
print("cuDNN Version:", torch.backends.cudnn.version())
print("CUDA Available:", torch.cuda.is_available())

if torch.cuda.is_available():
    device = torch.device("cuda")
    print("CUDA is available!")
    print("Device Name:", torch.cuda.get_device_name(0))
    x = torch.tensor([1.0, 2.0, 3.0]).to(device)
    y = x * 2
    print(y)
else:
    print("GPU is not available, running on CPU.")
