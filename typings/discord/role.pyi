"""
This type stub file was generated by pyright.
"""

import datetime
from typing import Any, List, Optional, TYPE_CHECKING, Union
from .asset import Asset
from .permissions import Permissions
from .colour import Colour
from .mixins import Hashable
from .types.role import Role as RolePayload, RoleTags as RoleTagPayload
from .guild import Guild
from .member import Member
from .state import ConnectionState

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
__all__ = ('RoleTags', 'Role')
if TYPE_CHECKING:
    ...
class RoleTags:
    """Represents tags on a role.

    A role tag is a piece of extra information attached to a managed role
    that gives it context for the reason the role is managed.

    While this can be accessed, a useful interface is also provided in the
    :class:`Role` and :class:`Guild` classes as well.

    .. versionadded:: 1.6

    Attributes
    ------------
    bot_id: Optional[:class:`int`]
        The bot's user ID that manages this role.
    integration_id: Optional[:class:`int`]
        The integration ID that manages the role.
    """
    __slots__ = ...
    def __init__(self, data: RoleTagPayload) -> None:
        ...
    
    def is_bot_managed(self) -> bool:
        """:class:`bool`: Whether the role is associated with a bot."""
        ...
    
    def is_premium_subscriber(self) -> bool:
        """:class:`bool`: Whether the role is the premium subscriber, AKA "boost", role for the guild."""
        ...
    
    def is_integration(self) -> bool:
        """:class:`bool`: Whether the role is managed by an integration."""
        ...
    
    def __repr__(self) -> str:
        ...
    


class Role(Hashable):
    """Represents a Discord role in a :class:`Guild`.

    .. container:: operations

        .. describe:: x == y

            Checks if two roles are equal.

        .. describe:: x != y

            Checks if two roles are not equal.

        .. describe:: x > y

            Checks if a role is higher than another in the hierarchy.

        .. describe:: x < y

            Checks if a role is lower than another in the hierarchy.

        .. describe:: x >= y

            Checks if a role is higher or equal to another in the hierarchy.

        .. describe:: x <= y

            Checks if a role is lower or equal to another in the hierarchy.

        .. describe:: hash(x)

            Return the role's hash.

        .. describe:: str(x)

            Returns the role's name.

    Attributes
    ----------
    id: :class:`int`
        The ID for the role.
    name: :class:`str`
        The name of the role.
    guild: :class:`Guild`
        The guild the role belongs to.
    hoist: :class:`bool`
         Indicates if the role will be displayed separately from other members.
    position: :class:`int`
        The position of the role. This number is usually positive. The bottom
        role has a position of 0.

        .. warning::

            Multiple roles can have the same position number. As a consequence
            of this, comparing via role position is prone to subtle bugs if
            checking for role hierarchy. The recommended and correct way to
            compare for roles in the hierarchy is using the comparison
            operators on the role objects themselves.

    unicode_emoji: Optional[:class:`str`]
        The role's unicode emoji, if available.

        .. note::

            If :attr:`icon` is not ``None``, it is displayed as role icon
            instead of the unicode emoji under this attribute.

            If you want the icon that a role has displayed, consider using :attr:`display_icon`.

        .. versionadded:: 2.0

    managed: :class:`bool`
        Indicates if the role is managed by the guild through some form of
        integrations such as Twitch.
    mentionable: :class:`bool`
        Indicates if the role can be mentioned by users.
    tags: Optional[:class:`RoleTags`]
        The role tags associated with this role.
    """
    __slots__ = ...
    def __init__(self, *, guild: Guild, state: ConnectionState, data: RolePayload) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self) -> str:
        ...
    
    def __lt__(self, other: object) -> bool:
        ...
    
    def __le__(self, other: Any) -> bool:
        ...
    
    def __gt__(self, other: Any) -> bool:
        ...
    
    def __ge__(self, other: object) -> bool:
        ...
    
    def is_default(self) -> bool:
        """:class:`bool`: Checks if the role is the default role."""
        ...
    
    def is_bot_managed(self) -> bool:
        """:class:`bool`: Whether the role is associated with a bot.

        .. versionadded:: 1.6
        """
        ...
    
    def is_premium_subscriber(self) -> bool:
        """:class:`bool`: Whether the role is the premium subscriber, AKA "boost", role for the guild.

        .. versionadded:: 1.6
        """
        ...
    
    def is_integration(self) -> bool:
        """:class:`bool`: Whether the role is managed by an integration.

        .. versionadded:: 1.6
        """
        ...
    
    def is_assignable(self) -> bool:
        """:class:`bool`: Whether the role is able to be assigned or removed by the bot.

        .. versionadded:: 2.0
        """
        ...
    
    @property
    def permissions(self) -> Permissions:
        """:class:`Permissions`: Returns the role's permissions."""
        ...
    
    @property
    def colour(self) -> Colour:
        """:class:`Colour`: Returns the role colour. An alias exists under ``color``."""
        ...
    
    @property
    def color(self) -> Colour:
        """:class:`Colour`: Returns the role color. An alias exists under ``colour``."""
        ...
    
    @property
    def icon(self) -> Optional[Asset]:
        """Optional[:class:`.Asset`]: Returns the role's icon asset, if available.

        .. note::
            If this is ``None``, the role might instead have unicode emoji as its icon
            if :attr:`unicode_emoji` is not ``None``.

            If you want the icon that a role has displayed, consider using :attr:`display_icon`.

        .. versionadded:: 2.0
        """
        ...
    
    @property
    def display_icon(self) -> Optional[Union[Asset, str]]:
        """Optional[Union[:class:`.Asset`, :class:`str`]]: Returns the role's display icon, if available.

        .. versionadded:: 2.0
        """
        ...
    
    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the role's creation time in UTC."""
        ...
    
    @property
    def mention(self) -> str:
        """:class:`str`: Returns a string that allows you to mention a role."""
        ...
    
    @property
    def members(self) -> List[Member]:
        """List[:class:`Member`]: Returns all the members with this role."""
        ...
    
    async def edit(self, *, name: str = ..., permissions: Permissions = ..., colour: Union[Colour, int] = ..., color: Union[Colour, int] = ..., hoist: bool = ..., display_icon: Optional[Union[bytes, str]] = ..., mentionable: bool = ..., position: int = ..., reason: Optional[str] = ...) -> Optional[Role]:
        """|coro|

        Edits the role.

        You must have the :attr:`~Permissions.manage_roles` permission to
        use this.

        All fields are optional.

        .. versionchanged:: 1.4
            Can now pass ``int`` to ``colour`` keyword-only parameter.

        .. versionchanged:: 2.0
            Edits are no longer in-place, the newly edited role is returned instead.

        .. versionadded:: 2.0
            The ``display_icon`` keyword-only parameter was added.

        .. versionchanged:: 2.0
            This function will now raise :exc:`ValueError` instead of
            ``InvalidArgument``.

        Parameters
        -----------
        name: :class:`str`
            The new role name to change to.
        permissions: :class:`Permissions`
            The new permissions to change to.
        colour: Union[:class:`Colour`, :class:`int`]
            The new colour to change to. (aliased to color as well)
        hoist: :class:`bool`
            Indicates if the role should be shown separately in the member list.
        display_icon: Optional[Union[:class:`bytes`, :class:`str`]]
            A :term:`py:bytes-like object` representing the icon
            or :class:`str` representing unicode emoji that should be used as a role icon.
            Could be ``None`` to denote removal of the icon.
            Only PNG/JPEG is supported.
            This is only available to guilds that contain ``ROLE_ICONS`` in :attr:`Guild.features`.
        mentionable: :class:`bool`
            Indicates if the role should be mentionable by others.
        position: :class:`int`
            The new role's position. This must be below your top role's
            position or it will fail.
        reason: Optional[:class:`str`]
            The reason for editing this role. Shows up on the audit log.

        Raises
        -------
        Forbidden
            You do not have permissions to change the role.
        HTTPException
            Editing the role failed.
        ValueError
            An invalid position was given or the default
            role was asked to be moved.

        Returns
        --------
        :class:`Role`
            The newly edited role.
        """
        ...
    
    async def delete(self, *, reason: Optional[str] = ...) -> None:
        """|coro|

        Deletes the role.

        You must have the :attr:`~Permissions.manage_roles` permission to
        use this.

        Parameters
        -----------
        reason: Optional[:class:`str`]
            The reason for deleting this role. Shows up on the audit log.

        Raises
        --------
        Forbidden
            You do not have permissions to delete the role.
        HTTPException
            Deleting the role failed.
        """
        ...
    


