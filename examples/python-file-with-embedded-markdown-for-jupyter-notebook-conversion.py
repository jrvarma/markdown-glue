# <markdowncell> : slide
# # Demonstrate Conversion to Notebook from Markdown + Python Code

# <markdowncell> : slide
# # Slide One

# This is `markdown` text.

# <markdowncell> : fragment

# More text in a fragment followed by a codecell.

# <codecell> : fragment
print([n**2 for n in range(10)])

# <markdowncell> : slide
# # Slide Two

# <codecell> : fragment
import numpy as np
import matplotlib.pyplot as plt
#%matplotlib inline
x = np.arange(0, 10, 0.1)
plt.plot(x, np.sin(x))
plt.show()

# <markdowncell> : slide
# # The End
