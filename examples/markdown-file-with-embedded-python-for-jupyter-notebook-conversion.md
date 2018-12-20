<!-- slide -->
# Demonstrate Conversion to Notebook from Markdown + Python Code 

<!-- slide -->
# Slide One

This is `markdown` text.

<!-- fragment -->

More text in a fragment followed by a codecell.

```
print([n**2 for n in range(10)])
```

<!-- slide -->
# Slide Two

```
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline
x = np.arange(0, 10, 0.1)
plt.plot(x, np.sin(x))
plt.show()
```

<!-- slide -->
# The End

