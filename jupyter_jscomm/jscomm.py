import ipywidgets as widgets
from IPython.display import display
import json
from typing import Any, Dict

class JSComm:
    """A class to handle JavaScript-Python communication in Jupyter notebooks using hidden widgets."""
    
    def __init__(self, class_name: str = "comm-class"):
        self.class_name = class_name
        self.widget = widgets.Text(value="{}")
        self.widget.layout.display = "none"
        self.widget.add_class(self.class_name)
        
        # Register a callback on the widget's value change
        self.widget.observe(self._on_value_change, names='value')
        display(self.widget)
    
    def _on_value_change(self, change):
        """Callback when the widget value changes"""
        # This ensures the value is properly propagated
        self.widget.send_state('value')
    
    def _get_current_data(self) -> Dict:
        try:
            return json.loads(self.widget.value)
        except json.JSONDecodeError:
            return {}
    
    def _update_widget(self, data: Dict) -> None:
        """Update the widget with new data."""
        # Set the value directly on the widget
        value_str = json.dumps(data)
        self.widget.value = value_str
        
        # Using the widget's JavaScript comm channel
        self.widget.send({'method': 'update', 'value': value_str})

    def has(self, key: str):
        return key in self._get_current_data()

    def add(self, key: str, value: Any) -> None:
        data = self._get_current_data()
        if key in data:
            raise KeyError(f"Key '{key}' already exists. Use update() to modify existing keys.")
        data[key] = value
        self._update_widget(data)
    
    def update(self, key: str, value: Any) -> None:
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist. Use add() to create new keys.")
        data[key] = value
        self._update_widget(data)
    
    def set(self, key: str, value: Any) -> None:
        data = self._get_current_data()
        data[key] = value
        self._update_widget(data)
    
    def get(self, key: str) -> Any:
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist")
        return data[key]
    
    def remove(self, key: str) -> None:
        data = self._get_current_data()
        if key not in data:
            raise KeyError(f"Key '{key}' does not exist")
        del data[key]
        self._update_widget(data)
    
    def clear_all(self) -> None:
        self._update_widget({})