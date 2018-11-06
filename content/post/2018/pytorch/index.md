---
title: Intro to pytorch
date: 2018-09-16
tags: 
    - pytorch
    - deep-learning
categories:
    - infrastructure
---


# Seed

Numpy Seed
```
import numpy as np
np.random.seed(0)
```

Cpu Seed
```
import torch
torch.manual_seed(5)
```


Gpu Seed
```
torch.cuda..manual_seed(5)
```



# Creating tesosrs
```
t =torch.ones(1,2)

```


# Conversion 
Torch -> Numpy
```
t =torch.ones(1,2)
t.numpy()
```
if GPU:

```
t.cuda.numpy()
```


Numpy -> Torch
```
n = np.ones((2, 1))
torch.from_numpy(n)
```




# Tensor operations

Vector Operation
```
a = torch.ones(1,2)
b = torch.ones(1,2)

a + b 
a.add(b)
torch.add(a,b)
```


Pytorch supports other operatiosn like add, subtract, multiply

Vector Operation (inplace)

```
a.add_(b)
```