"""
Interface module for the Annotation Toolkit.
"""

from .generator import AnnotationGenerator
from .iterators import ComposedIterator, StringListIterator

__all__ = ['AnnotationGenerator', 'ComposedIterator', 'StringListIterator'] 