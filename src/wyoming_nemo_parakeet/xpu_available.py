import torch


if __name__ == '__main__':
    xpu = torch.xpu.is_available()
    print(f"XPU is available: {xpu}")
