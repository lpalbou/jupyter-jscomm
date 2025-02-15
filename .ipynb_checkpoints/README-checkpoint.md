# jupyter-jscomm

A Python package to work around JavaScript-Python communication difficulties in Jupyter notebooks.
Basic strategy is to use a hidden widget holding a json payload with the variables you want to keep.

This code can for instance be used as a hack to copy the content of bokeh JS variables into these JS-Python accessible variables.


## Installation

```bash
pip install jupyter-jscomm
```

## Usage from a Jupyter notebook
```python
from jupyter_jscomm import JSComm

# Initialize the communication
comm = JSComm()

# Or initialize with custom class name to avoid collisions
comm1 = JSComm(class_name="my-comm-1")
comm2 = JSComm(class_name="my-comm-2")

# Each instance maintains its own state
comm1.add("var1", "Value for comm1")
comm2.add("var1", "Value for comm2")

# Add data from Python
comm1.add("var1", "Hello from Python")
comm2.add("var2", {"nested": "data"})

# Get data from JavaScript
value = comm1.get("var1")

# Update existing data
comm1.update("var1", "Updated value")

# Remove data
comm1.remove("var1")

# Clear all data
comm1.clear_all()
```

## Change JS variable from JS context
While this package ensures the creation of a "magic" JS variable (default class name "comm-class") where you can write from Python to JS and get the value back from JS to Python, one of the goal is to map an already existing variable to this "magic" JS variable

```javascript
// var my_existing_variable already contains the value I want to retrieve and expose in Python
var parent = document.getElementsByClassName("comm-class")[0];
var input = parent.querySelector(".widget-input");
input.value = '{"var1": ' + JSON.stringify(my_existing_variable + '}';
input.dispatchEvent(new Event('input', { bubbles: true }));
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.