from abc import ABC, abstractmethod
import random
from typing import Any, Dict, List, Optional, Union, Iterator
from itertools import product

class BaseIterator(ABC):
    """Base class for all iterators"""
    
    @abstractmethod
    def __init__(self, config: dict):
        self.config = config
        self.current_index = 0
        self.sequence = []
        
    @abstractmethod
    def next(self) -> Any:
        """Get next value in the sequence"""
        pass
    
    @abstractmethod
    def current(self) -> Any:
        """Get current value without advancing"""
        pass
    
    def reset(self):
        """Reset iterator to beginning"""
        self.current_index = 0

    @property
    def length(self) -> int:
        """Get total length of sequence"""
        return len(self.sequence)

class NumberRangeIterator(BaseIterator):
    """Iterator for numeric sequences"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        sequence_config = config.get('sequence', {})
        self.start = sequence_config.get('start', 1)
        self.end = sequence_config.get('end', 1)
        self.randomize = config.get('randomize', False)
        
        # Generate sequence
        self.sequence = list(range(self.start, self.end + 1))
        if self.randomize:
            random.shuffle(self.sequence)
    
    def next(self) -> Optional[int]:
        if self.current_index >= len(self.sequence):
            return None
        value = self.sequence[self.current_index]
        self.current_index += 1
        return value
    
    def current(self) -> Optional[int]:
        if self.current_index >= len(self.sequence):
            return None
        return self.sequence[self.current_index]

class StringListIterator(BaseIterator):
    """Iterator for list of strings"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.values = config.get('values', [])
        self.randomize = config.get('randomize', False)
        
        # Use provided values as sequence
        self.sequence = self.values.copy()
        if self.randomize:
            random.shuffle(self.sequence)
    
    def next(self) -> Optional[str]:
        if self.current_index >= len(self.sequence):
            return None
        value = self.sequence[self.current_index]
        self.current_index += 1
        return value
    
    def current(self) -> Optional[str]:
        if self.current_index >= len(self.sequence):
            return None
        return self.sequence[self.current_index]

class ComposedIterator(BaseIterator):
    """Iterator that composes multiple iterators"""
    
    def __init__(self, config: dict):
        super().__init__(config)
        self.iterators = {}
        self.current_values = {}
        
        # Initialize sub-iterators
        iterator_configs = config.get('iterators', {})
        for name, iter_config in iterator_configs.items():
            if iter_config['type'] == 'string_list':
                self.iterators[name] = StringListIterator(iter_config)
        
        # Generate all combinations
        sequences = [list(range(it.length)) for it in self.iterators.values()]
        combinations = list(product(*sequences))
        
        # Randomize if specified
        if config.get('randomize', False):
            random.shuffle(combinations)
            
        self.sequence = combinations
    
    def next(self) -> Optional[Dict[str, Any]]:
        if self.current_index >= len(self.sequence):
            return None
            
        # Get indices for current combination
        indices = self.sequence[self.current_index]
        
        # Update current values for each iterator
        result = {}
        for (name, iterator), index in zip(self.iterators.items(), indices):
            iterator.current_index = index
            result[name] = iterator.current()
            
        self.current_values = result
        self.current_index += 1
        return result
    
    def current(self) -> Optional[Dict[str, Any]]:
        if self.current_index >= len(self.sequence):
            return None
        return self.current_values

class URLPatternIterator:
    """Iterator that combines pattern substitution with composed iteration"""
    
    def __init__(self, config: dict):
        self.config = config
        self.base_url = config.get('base_url', '')
        self.pattern = config.get('pattern', '')
        self.variables = config.get('variables', {})
        
        # Create composed iterator
        self.value_iterator = ComposedIterator(config)
    
    def next(self) -> Optional[str]:
        """Get next URL in sequence"""
        next_values = self.value_iterator.next()
        if next_values is None:
            return None
            
        # Build URL by substituting all variables and current values
        url = self.pattern.format(
            base_url=self.base_url,
            **next_values,
            **self.variables
        )
        return url
    
    def current(self) -> Optional[str]:
        """Get current URL without advancing"""
        current_values = self.value_iterator.current()
        if current_values is None:
            return None
            
        url = self.pattern.format(
            base_url=self.base_url,
            **current_values,
            **self.variables
        )
        return url
    
    def reset(self):
        """Reset iterator to beginning"""
        self.value_iterator.reset()

    @property
    def current_values(self) -> Dict[str, Any]:
        """Get current iterator values for template rendering"""
        return self.value_iterator.current() or {} 