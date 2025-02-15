import ipywidgets as widgets
from IPython.display import Javascript, display
import json
from typing import Any, Optional, Dict

class JSComm:
    """A class to handle JavaScript-Python communication in Jupyter notebooks using hidden widgets."""
    
    def __init__(self, class_name: str = "comm-class"):
        """Initialize the JSComm instance with a hidden widget.
        
        Args:
            class_name (str, optional): Custom class name for the widget. 
                                      Defaults to "comm-class".
                                      Use this to avoid collisions when using multiple instances.
        """
        self.class_name = class_name
        self.widget = widgets.Text(value="{}")
        self.widget.layout.display = "none"
        self.widget.add_class(self.class_name)
        display(self.widget)
    
    def _execute_js(self, script: str) -> None:
        """Execute JavaScript code in the notebook.
        
        Args:
            script (str): JavaScript code to execute
        """
        display(Javascript(script))
    
    def _get_current_data(self) -> Dict:
        """Get the current data from the widget.
        
        Returns:
            Dict: Current data stored in the widget
        """
        try:
            return json.loads(self.widget.value)
        except json.JSONDecodeError:
            return {}
    
    def _update_widget(self, data: Dict) -> None:
        """Update the widget with new data.
        
        Args:
            data (Dict): Data to store in the widget
        """
        js_code = f"""
        var parent = document.getElementsByClassName("{self.class_name}")[0];
        if (parent) {{
            var input = parent.querySelector(".widget-input");
            if (input) {{
                input.value = '{json.dumps(data)}';
                input.dispatchEvent(new Event('input', {{ bubbles: true }}));
            }} else {{
                console.error("Input element not found");
            }}
        }} else {{
            console.error("Parent element not found");
        }}
        """
        self._execute_js(js_code)

    def has(self, key : str):
        """Check if a key already exists
        
        Args:
            key (str): Key to add
                    
        Returns:
            Boolean: True if key already exists, False otherwise
        """        
        return key in self._get_current_data()

    def set(self, key: str, value: Any) -> None:
        """Add a new key-value pair to the stored data. If the key exists, will update it
        
        Args:
            key (str): Key to add
            value (Any): Value to associate with the key            
        """
        data = self._get_current_data()
        if key in data :
            self.update(key, value)
        else:
            self.add(key, value)
    
    def add(self, key: str, value: Any) -> None:
        """Add a new key-value pair to the stored data.
        
        Args:
            key (str): Key to add
            value (Any): Value to associate with the key
            
        Raises:
            KeyError: If the key already exists
        """
        data = self._get_current_data()
        if key in data:
            raise KeyError(f"Key '{key}' already exists. Use update() to modify existing keys.")
        data[key] = value
        self._update_widget(data)
    
    def update(self, key: str, value: Any) -> None:
        """Update an existing key with a new value.
        
        Args:
            key (str): Key to update
            value (Any): New value for the key
            
        Raises:
            KeyError: If the key doesn't exist
        """
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist. Use add() to create new keys.")
        data[key] = value
        self._update_widget(data)
    
    def get(self, key: str) -> Any:
        """Get the value associated with a key.
        
        Args:
            key (str): Key to retrieve
        
        Returns:
            Any: Value associated with the key
        
        Raises:
            KeyError: If the key doesn't exist
        """
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist")
        return data[key]
    
    def remove(self, key: str) -> None:
        """Remove a key-value pair from the stored data.
        
        Args:
            key (str): Key to remove
        
        Raises:
            KeyError: If the key doesn't exist
        """
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist")
        del data[key]
        self._update_widget(data)
    
    def clear_all(self) -> None:
        """Remove all stored data."""
        self._update_widget({})