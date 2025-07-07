# pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu128

import torch
import torch.nn as nn
print(torch.__version__)  # 应显示 2.x.x
print(torch.cuda.is_available())  # 应返回 True
print(torch.version.cuda)  # 应显示 12.8（PyTorch 编译版本）
nn.Linear(10, 10).cuda()  # 应正常运行