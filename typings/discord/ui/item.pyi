"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, Coroutine, Dict, Generic, Optional, TYPE_CHECKING, Tuple, Type, TypeVar
from ..interactions import Interaction
from ..enums import ComponentType
from ..components import Component

"""
The MIT License (MIT)

Copyright (c) 2015-present Rapptz

Permission is hereby granted, free of charge, to any person obtaining a
copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the
Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
DEALINGS IN THE SOFTWARE.
"""
__all__ = ('Item', )
if TYPE_CHECKING:
    ...
I = TypeVar('I', bound='Item')
V = TypeVar('V', bound='View', covariant=True)
ItemCallbackType = Callable[[V, Interaction, I], Coroutine[Any, Any, Any]]
class Item(Generic[V]):
    """Represents the base UI item that all UI components inherit from.

    The current UI items supported are:

    - :class:`discord.ui.Button`
    - :class:`discord.ui.Select`
    - :class:`discord.ui.TextInput`

    .. versionadded:: 2.0
    """
    __item_repr_attributes__: Tuple[str, ...] = ...
    def __init__(self) -> None:
        ...
    
    def to_component_dict(self) -> Dict[str, Any]:
        ...
    
    @classmethod
    def from_component(cls: Type[I], component: Component) -> I:
        ...
    
    @property
    def type(self) -> ComponentType:
        ...
    
    def is_dispatchable(self) -> bool:
        ...
    
    def is_persistent(self) -> bool:
        ...
    
    def __repr__(self) -> str:
        ...
    
    @property
    def row(self) -> Optional[int]:
        ...
    
    @row.setter
    def row(self, value: Optional[int]) -> None:
        ...
    
    @property
    def width(self) -> int:
        ...
    
    @property
    def view(self) -> Optional[V]:
        """Optional[:class:`View`]: The underlying view for this item."""
        ...
    
    async def callback(self, interaction: Interaction) -> Any:
        """|coro|

        The callback associated with this UI item.

        This can be overridden by subclasses.

        Parameters
        -----------
        interaction: :class:`.Interaction`
            The interaction that triggered this UI item.
        """
        ...
    


