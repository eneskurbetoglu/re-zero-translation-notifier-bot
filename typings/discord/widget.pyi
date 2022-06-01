"""
This type stub file was generated by pyright.
"""

import datetime
from typing import Optional, TYPE_CHECKING, Union
from .user import BaseUser
from .activity import BaseActivity, Spotify
from .invite import Invite
from .state import ConnectionState
from .types.widget import Widget as WidgetPayload, WidgetMember as WidgetMemberPayload

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
if TYPE_CHECKING:
    ...
__all__ = ('WidgetChannel', 'WidgetMember', 'Widget')
class WidgetChannel:
    """Represents a "partial" widget channel.

    .. container:: operations

        .. describe:: x == y

            Checks if two partial channels are the same.

        .. describe:: x != y

            Checks if two partial channels are not the same.

        .. describe:: hash(x)

            Return the partial channel's hash.

        .. describe:: str(x)

            Returns the partial channel's name.

    Attributes
    -----------
    id: :class:`int`
        The channel's ID.
    name: :class:`str`
        The channel's name.
    position: :class:`int`
        The channel's position
    """
    __slots__ = ...
    def __init__(self, id: int, name: str, position: int) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __repr__(self) -> str:
        ...
    
    @property
    def mention(self) -> str:
        """:class:`str`: The string that allows you to mention the channel."""
        ...
    
    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the channel's creation time in UTC."""
        ...
    


class WidgetMember(BaseUser):
    """Represents a "partial" member of the widget's guild.

    .. container:: operations

        .. describe:: x == y

            Checks if two widget members are the same.

        .. describe:: x != y

            Checks if two widget members are not the same.

        .. describe:: hash(x)

            Return the widget member's hash.

        .. describe:: str(x)

            Returns the widget member's `name#discriminator`.

    Attributes
    -----------
    id: :class:`int`
        The member's ID.
    name: :class:`str`
        The member's username.
    discriminator: :class:`str`
        The member's discriminator.
    bot: :class:`bool`
        Whether the member is a bot.
    status: :class:`Status`
        The member's status.
    nick: Optional[:class:`str`]
        The member's nickname.
    avatar: Optional[:class:`str`]
        The member's avatar hash.
    activity: Optional[Union[:class:`BaseActivity`, :class:`Spotify`]]
        The member's activity.
    deafened: Optional[:class:`bool`]
        Whether the member is currently deafened.
    muted: Optional[:class:`bool`]
        Whether the member is currently muted.
    suppress: Optional[:class:`bool`]
        Whether the member is currently being suppressed.
    connected_channel: Optional[:class:`WidgetChannel`]
        Which channel the member is connected to.
    """
    __slots__ = ...
    if TYPE_CHECKING:
        activity: Optional[Union[BaseActivity, Spotify]]
        ...
    def __init__(self, *, state: ConnectionState, data: WidgetMemberPayload, connected_channel: Optional[WidgetChannel] = ...) -> None:
        ...
    
    def __repr__(self) -> str:
        ...
    
    @property
    def display_name(self) -> str:
        """:class:`str`: Returns the member's display name."""
        ...
    


class Widget:
    """Represents a :class:`Guild` widget.

    .. container:: operations

        .. describe:: x == y

            Checks if two widgets are the same.

        .. describe:: x != y

            Checks if two widgets are not the same.

        .. describe:: str(x)

            Returns the widget's JSON URL.

    Attributes
    -----------
    id: :class:`int`
        The guild's ID.
    name: :class:`str`
        The guild's name.
    channels: List[:class:`WidgetChannel`]
        The accessible voice channels in the guild.
    members: List[:class:`Member`]
        The online members in the guild. Offline members
        do not appear in the widget.

        .. note::

            Due to a Discord limitation, if this data is available
            the users will be "anonymized" with linear IDs and discriminator
            information being incorrect. Likewise, the number of members
            retrieved is capped.
    presence_count: :class:`int`
        The approximate number of online members in the guild.
        Offline members are not included in this count.

        .. versionadded:: 2.0

    """
    __slots__ = ...
    def __init__(self, *, state: ConnectionState, data: WidgetPayload) -> None:
        ...
    
    def __str__(self) -> str:
        ...
    
    def __eq__(self, other: object) -> bool:
        ...
    
    def __repr__(self) -> str:
        ...
    
    @property
    def created_at(self) -> datetime.datetime:
        """:class:`datetime.datetime`: Returns the member's creation time in UTC."""
        ...
    
    @property
    def json_url(self) -> str:
        """:class:`str`: The JSON URL of the widget."""
        ...
    
    @property
    def invite_url(self) -> Optional[str]:
        """Optional[:class:`str`]: The invite URL for the guild, if available."""
        ...
    
    async def fetch_invite(self, *, with_counts: bool = ...) -> Optional[Invite]:
        """|coro|

        Retrieves an :class:`Invite` from the widget's invite URL.
        This is the same as :meth:`Client.fetch_invite`; the invite
        code is abstracted away.

        Parameters
        -----------
        with_counts: :class:`bool`
            Whether to include count information in the invite. This fills the
            :attr:`Invite.approximate_member_count` and :attr:`Invite.approximate_presence_count`
            fields.

        Returns
        --------
        Optional[:class:`Invite`]
            The invite from the widget's invite URL, if available.
        """
        ...
    


