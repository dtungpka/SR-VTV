#import and print pytorch version, cuda version, cudnn version
import torch
print(torch.__version__)
if torch.cuda.is_available():
    print(torch.version.cuda)
    print("Cuda available, version:",torch.backends.cudnn.version())
else:
    print("No cuda available")
