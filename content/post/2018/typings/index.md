---
title: Types in Python
date: 2018-10-20
tags: 
    - python
    - clean code
    - typings
categories:
    - python
    - clean code
---

Coming from languages like Java/C#, I found something missing in python.     
I miss defining **types** for variables and methods.

<!--more-->

**Variables: Python vs Java**
{{< highlight python  >}}
# Python Variables
name = "Tom"
cost = 5
{{< / highlight >}}

{{< highlight java  >}}
// Java Variables
String name = "Tom"
int cost = 5
{{< / highlight >}}

**Methods: Python vs Java**

{{< highlight python  >}}
# Python method

def add(a,b):
    return a + b
{{< / highlight >}}

{{< highlight java  >}}
// Java method

public String add (String a, String b) {
    return a + b
}
{{< / highlight >}}

What does the python version of the add function take?
What does it return?

The add operator works for string, integers, list. 
Is that intended?


Some of the benefits of a language that supports types are:      
- documentation of inputs and outputs      
- capture error in wrong usage      
- better code completion with IDE    
{{< figure src="static/auto_complete.png"  >}}


Luckily for us, with [PEP484](https://www.python.org/dev/peps/pep-0484/) python 3.6 supports types.




**Variables: Typed**    
With built in primitive types, all that is needed

{{< highlight python  >}}
# Python Variables
name: str = "Tom"
cost: int = 5
{{< / highlight >}}

For more complex types,
{{< highlight python  >}}
from typing import List, Set, Dict, Tuple, Optional

elements: List[int] = [1,2]
unique_elems: Set[int] = {6, 7}

scores: Dict[str, float] = {'user1': 2.0, 'user_2':5.2}


info: Tuple[int, str] = (2, "tom")
{{< / highlight >}}

**Methods: Typed**    

{{< highlight python  >}}
from typing import Union, List

def add_nums(a:int,b:int) -> int:
    return a + b

def add (a:Union[List,str,int],b:Union[List,str,int] ) -> [List,str,int] :
    return a +b
{{< / highlight >}}


Example of defining own types

{{< highlight python  >}}
from typing import Tuple

LatLngType = Tuple[float, float]

point: LatLngType = (50.12, 70.21) 

{{< / highlight >}}

# Type Checking
Python doesn't have anything built in the language that enforces types.     
However there is [mypy](http://mypy-lang.org/), a project from Dropbox.


Installation
```
pip install mypy
```

Running
```
mypy test.py
```

Consider this sample code. Do you see the error(s)?
{{< figure src="static/error.png" caption="Fig: python code with errors"  >}}


{{< figure src="static/mypy_output.png" caption="Fig: Mypy output"  >}}

Looking at the output, we see that we are wrongly:   
- forgot a return statement    
- accessing an attribute that doesn't exist

At my work, we have started including types and mypy as part of our work.
It has made our code base more maintainable.

