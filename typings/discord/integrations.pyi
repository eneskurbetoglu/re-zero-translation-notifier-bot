"""
This type stub file was generated by pyright.
"""

from typing import Optional, TYPE_CHECKING
from .enums import ExpireBehaviour
from .guild import Guild
from .role import Role
from .state import ConnectionState
from .types.integration import Integration as IntegrationPayload, IntegrationAccount as IntegrationAccountPayload, IntegrationApplication as IntegrationApplicationPayload, PartialIntegration as PartialIntegrationPayload

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
__all__ = ('IntegrationAccount', 'IntegrationApplication', 'Integration', 'StreamIntegration', 'BotIntegration', 'PartialIntegration')
if TYPE_CHECKING:
    ...
class IntegrationAccount:
    """Represents an integration account.

    .. versionadded:: 1.4

    Attributes
    -----------
    id: :class:`str`
        The account ID.
    name: :class:`str`
        The account name.
    """
    __slots__ = ...
    def __init__(self, data: IntegrationAccountPayload) -> None:
        ...
    
    def __repr__(self) -> str:
        ...
    


class Integration:
    """Represents a guild integration.

    .. versionadded:: 1.4

    Attributes
    -----------
    id: :class:`int`
        The integration ID.
    name: :class:`str`
        The integration name.
    guild: :class:`Guild`
        The guild of the integration.
    type: :class:`str`
        The integration type (i.e. Twitch).
    enabled: :class:`bool`
        Whether the integration is currently enabled.
    account: :class:`IntegrationAccount`
        The account linked to this integration.
    user: :class:`User`
        The user that added this integration.
    """
    __slots__ = ...
    def __init__(self, *, data: IntegrationPayload, guild: Guild) -> None:
        ...
    
    def __repr__(self) -> str:
        ...
    
    async def delete(self, *, reason: Optional[str] = ...) -> None:
        """|coro|

        Deletes the integration.

        You must have the :attr:`~Permissions.manage_guild` permission to
        do this.

        Parameters
        -----------
        reason: :class:`str`
            The reason the integration was deleted. Shows up on the audit log.

            .. versionadded:: 2.0

        Raises
        -------
        Forbidden
            You do not have permission to delete the integration.
        HTTPException
            Deleting the integration failed.
        """
        ...
    


class StreamIntegration(Integration):
    """Represents a stream integration for Twitch or YouTube.

    .. versionadded:: 2.0

    Attributes
    ----------
    id: :class:`int`
        The integration ID.
    name: :class:`str`
        The integration name.
    guild: :class:`Guild`
        The guild of the integration.
    type: :class:`str`
        The integration type (i.e. Twitch).
    enabled: :class:`bool`
        Whether the integration is currently enabled.
    syncing: :class:`bool`
        Where the integration is currently syncing.
    enable_emoticons: Optional[:class:`bool`]
        Whether emoticons should be synced for this integration (currently twitch only).
    expire_behaviour: :class:`ExpireBehaviour`
        The behaviour of expiring subscribers. Aliased to ``expire_behavior`` as well.
    expire_grace_period: :class:`int`
        The grace period (in days) for expiring subscribers.
    user: :class:`User`
        The user for the integration.
    account: :class:`IntegrationAccount`
        The integration account information.
    synced_at: :class:`datetime.datetime`
        An aware UTC datetime representing when the integration was last synced.
    """
    __slots__ = ...
    @property
    def expire_behavior(self) -> ExpireBehaviour:
        """:class:`ExpireBehaviour`: An alias for :attr:`expire_behaviour`."""
        ...
    
    @property
    def role(self) -> Optional[Role]:
        """Optional[:class:`Role`] The role which the integration uses for subscribers."""
        ...
    
    async def edit(self, *, expire_behaviour: ExpireBehaviour = ..., expire_grace_period: int = ..., enable_emoticons: bool = ...) -> None:
        """|coro|

        Edits the integration.

        You must have the :attr:`~Permissions.manage_guild` permission to
        do this.

        .. versionchanged:: 2.0
            This function will now raise :exc:`TypeError` instead of
            ``InvalidArgument``.

        Parameters
        -----------
        expire_behaviour: :class:`ExpireBehaviour`
            The behaviour when an integration subscription lapses. Aliased to ``expire_behavior`` as well.
        expire_grace_period: :class:`int`
            The period (in days) where the integration will ignore lapsed subscriptions.
        enable_emoticons: :class:`bool`
            Where emoticons should be synced for this integration (currently twitch only).

        Raises
        -------
        Forbidden
            You do not have permission to edit the integration.
        HTTPException
            Editing the guild failed.
        TypeError
            ``expire_behaviour`` did not receive a :class:`ExpireBehaviour`.
        """
        ...
    
    async def sync(self) -> None:
        """|coro|

        Syncs the integration.

        You must have the :attr:`~Permissions.manage_guild` permission to
        do this.

        Raises
        -------
        Forbidden
            You do not have permission to sync the integration.
        HTTPException
            Syncing the integration failed.
        """
        ...
    


class IntegrationApplication:
    """Represents an application for a bot integration.

    .. versionadded:: 2.0

    Attributes
    ----------
    id: :class:`int`
        The ID for this application.
    name: :class:`str`
        The application's name.
    icon: Optional[:class:`str`]
        The application's icon hash.
    description: :class:`str`
        The application's description. Can be an empty string.
    summary: :class:`str`
        The summary of the application. Can be an empty string.
    user: Optional[:class:`User`]
        The bot user on this application.
    """
    __slots__ = ...
    def __init__(self, *, data: IntegrationApplicationPayload, state: ConnectionState) -> None:
        ...
    


class BotIntegration(Integration):
    """Represents a bot integration on discord.

    .. versionadded:: 2.0

    Attributes
    ----------
    id: :class:`int`
        The integration ID.
    name: :class:`str`
        The integration name.
    guild: :class:`Guild`
        The guild of the integration.
    type: :class:`str`
        The integration type (i.e. Twitch).
    enabled: :class:`bool`
        Whether the integration is currently enabled.
    user: :class:`User`
        The user that added this integration.
    account: :class:`IntegrationAccount`
        The integration account information.
    application: :class:`IntegrationApplication`
        The application tied to this integration.
    """
    __slots__ = ...


class PartialIntegration:
    """Represents a partial guild integration.

    .. versionadded:: 2.0

    Attributes
    -----------
    id: :class:`int`
        The integration ID.
    name: :class:`str`
        The integration name.
    guild: :class:`Guild`
        The guild of the integration.
    type: :class:`str`
        The integration type (i.e. Twitch).
    account: :class:`IntegrationAccount`
        The account linked to this integration.
    application_id: Optional[:class:`int`]
        The id of the application this integration belongs to.
    """
    __slots__ = ...
    def __init__(self, *, data: PartialIntegrationPayload, guild: Guild) -> None:
        ...
    
    def __repr__(self) -> str:
        ...
    


