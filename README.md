krtpy
=====

Korean Romanization/Hangulization utility written in python

Installation
============

    $ python setup.py install

Usage
=====

```python
from krt import *

# To hangulize text in the utf8 format:
hangulize('chen')

# To romanize text in the utf8 format:
romanize('천')

# To hangulize text into a different output format:
hangulize('chen', 'euc-kr')

# To romanize text in different input/output formats:
romanize(raw='천',fromEncoding='euc-kr',toEncoding='utf8')
```

