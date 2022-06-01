"""
This type stub file was generated by pyright.
"""

from typing import Any, Callable, List, Optional, TYPE_CHECKING, Tuple, Union
from . import abc
from .gateway import *
from .player import AudioSource
from .client import Client
from .guild import Guild
from .user import ClientUser
from .channel import StageChannel, VoiceChannel
from .types.voice import GuildVoiceState as GuildVoiceStatePayload, SupportedModes, VoiceServerUpdate as VoiceServerUpdatePayload

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


Some documentation to refer to:

- Our main web socket (mWS) sends opcode 4 with a guild ID and channel ID.
- The mWS receives VOICE_STATE_UPDATE and VOICE_SERVER_UPDATE.
- We pull the session_id from VOICE_STATE_UPDATE.
- We pull the token, endpoint and server_id from VOICE_SERVER_UPDATE.
- Then we initiate the voice web socket (vWS) pointing to the endpoint.
- We send opcode 0 with the user_id, server_id, session_id and token using the vWS.
- The vWS sends back opcode 2 with an ssrc, port, modes(array) and hearbeat_interval.
- We send a UDP discovery packet to endpoint:port and receive our IP and our port in LE.
- Then we send our IP and port via vWS with opcode 1.
- When that's all done, we receive opcode 4 from the vWS.
- Finally we can transmit data to endpoint:port.
"""
if TYPE_CHECKING:
    VocalGuildChannel = Union[VoiceChannel, StageChannel]
has_nacl: bool
__all__ = ('VoiceProtocol', 'VoiceClient')
_log = ...
class VoiceProtocol:
    """A class that represents the Discord voice protocol.

    This is an abstract class. The library provides a concrete implementation
    under :class:`VoiceClient`.

    This class allows you to implement a protocol to allow for an external
    method of sending voice, such as Lavalink_ or a native library implementation.

    These classes are passed to :meth:`abc.Connectable.connect <VoiceChannel.connect>`.

    .. _Lavalink: https://github.com/freyacodes/Lavalink

    Parameters
    ------------
    client: :class:`Client`
        The client (or its subclasses) that started the connection request.
    channel: :class:`abc.Connectable`
        The voice channel that is being connected to.
    """
    def __init__(self, client: Client, channel: abc.Connectable) -> None:
        ...
    
    async def on_voice_state_update(self, data: GuildVoiceStatePayload) -> None:
        """|coro|

        An abstract method that is called when the client's voice state
        has changed. This corresponds to ``VOICE_STATE_UPDATE``.

        Parameters
        ------------
        data: :class:`dict`
            The raw `voice state payload`__.

            .. _voice_state_update_payload: https://discord.com/developers/docs/resources/voice#voice-state-object

            __ voice_state_update_payload_
        """
        ...
    
    async def on_voice_server_update(self, data: VoiceServerUpdatePayload) -> None:
        """|coro|

        An abstract method that is called when initially connecting to voice.
        This corresponds to ``VOICE_SERVER_UPDATE``.

        Parameters
        ------------
        data: :class:`dict`
            The raw `voice server update payload`__.

            .. _voice_server_update_payload: https://discord.com/developers/docs/topics/gateway#voice-server-update-voice-server-update-event-fields

            __ voice_server_update_payload_
        """
        ...
    
    async def connect(self, *, timeout: float, reconnect: bool, self_deaf: bool = ..., self_mute: bool = ...) -> None:
        """|coro|

        An abstract method called when the client initiates the connection request.

        When a connection is requested initially, the library calls the constructor
        under ``__init__`` and then calls :meth:`connect`. If :meth:`connect` fails at
        some point then :meth:`disconnect` is called.

        Within this method, to start the voice connection flow it is recommended to
        use :meth:`Guild.change_voice_state` to start the flow. After which,
        :meth:`on_voice_server_update` and :meth:`on_voice_state_update` will be called.
        The order that these two are called is unspecified.

        Parameters
        ------------
        timeout: :class:`float`
            The timeout for the connection.
        reconnect: :class:`bool`
            Whether reconnection is expected.
        self_mute: :class:`bool`
            Indicates if the client should be self-muted.

            .. versionadded: 2.0
        self_deaf: :class:`bool`
            Indicates if the client should be self-deafened.

            .. versionadded: 2.0
        """
        ...
    
    async def disconnect(self, *, force: bool) -> None:
        """|coro|

        An abstract method called when the client terminates the connection.

        See :meth:`cleanup`.

        Parameters
        ------------
        force: :class:`bool`
            Whether the disconnection was forced.
        """
        ...
    
    def cleanup(self) -> None:
        """This method *must* be called to ensure proper clean-up during a disconnect.

        It is advisable to call this from within :meth:`disconnect` when you are
        completely done with the voice protocol instance.

        This method removes it from the internal state cache that keeps track of
        currently alive voice clients. Failure to clean-up will cause subsequent
        connections to report that it's still connected.
        """
        ...
    


class VoiceClient(VoiceProtocol):
    """Represents a Discord voice connection.

    You do not create these, you typically get them from
    e.g. :meth:`VoiceChannel.connect`.

    Warning
    --------
    In order to use PCM based AudioSources, you must have the opus library
    installed on your system and loaded through :func:`opus.load_opus`.
    Otherwise, your AudioSources must be opus encoded (e.g. using :class:`FFmpegOpusAudio`)
    or the library will not be able to transmit audio.

    Attributes
    -----------
    session_id: :class:`str`
        The voice connection session ID.
    token: :class:`str`
        The voice connection token.
    endpoint: :class:`str`
        The endpoint we are connecting to.
    channel: Union[:class:`VoiceChannel`, :class:`StageChannel`]
        The voice channel connected to.
    """
    channel: VocalGuildChannel
    endpoint_ip: str
    voice_port: int
    ip: str
    port: int
    secret_key: List[int]
    ssrc: int
    def __init__(self, client: Client, channel: abc.Connectable) -> None:
        ...
    
    warn_nacl: bool = ...
    supported_modes: Tuple[SupportedModes, ...] = ...
    @property
    def guild(self) -> Guild:
        """:class:`Guild`: The guild we're connected to."""
        ...
    
    @property
    def user(self) -> ClientUser:
        """:class:`ClientUser`: The user connected to voice (i.e. ourselves)."""
        ...
    
    def checked_add(self, attr: str, value: int, limit: int) -> None:
        ...
    
    async def on_voice_state_update(self, data: GuildVoiceStatePayload) -> None:
        ...
    
    async def on_voice_server_update(self, data: VoiceServerUpdatePayload) -> None:
        ...
    
    async def voice_connect(self, self_deaf: bool = ..., self_mute: bool = ...) -> None:
        ...
    
    async def voice_disconnect(self) -> None:
        ...
    
    def prepare_handshake(self) -> None:
        ...
    
    def finish_handshake(self) -> None:
        ...
    
    async def connect_websocket(self) -> DiscordVoiceWebSocket:
        ...
    
    async def connect(self, *, reconnect: bool, timeout: float, self_deaf: bool = ..., self_mute: bool = ...) -> None:
        ...
    
    async def potential_reconnect(self) -> bool:
        ...
    
    @property
    def latency(self) -> float:
        """:class:`float`: Latency between a HEARTBEAT and a HEARTBEAT_ACK in seconds.

        This could be referred to as the Discord Voice WebSocket latency and is
        an analogue of user's voice latencies as seen in the Discord client.

        .. versionadded:: 1.4
        """
        ...
    
    @property
    def average_latency(self) -> float:
        """:class:`float`: Average of most recent 20 HEARTBEAT latencies in seconds.

        .. versionadded:: 1.4
        """
        ...
    
    async def poll_voice_ws(self, reconnect: bool) -> None:
        ...
    
    async def disconnect(self, *, force: bool = ...) -> None:
        """|coro|

        Disconnects this voice client from voice.
        """
        ...
    
    async def move_to(self, channel: Optional[abc.Snowflake]) -> None:
        """|coro|

        Moves you to a different voice channel.

        Parameters
        -----------
        channel: Optional[:class:`abc.Snowflake`]
            The channel to move to. Must be a voice channel.
        """
        ...
    
    def is_connected(self) -> bool:
        """Indicates if the voice client is connected to voice."""
        ...
    
    def play(self, source: AudioSource, *, after: Optional[Callable[[Optional[Exception]], Any]] = ...) -> None:
        """Plays an :class:`AudioSource`.

        The finalizer, ``after`` is called after the source has been exhausted
        or an error occurred.

        If an error happens while the audio player is running, the exception is
        caught and the audio player is then stopped.  If no after callback is
        passed, any caught exception will be displayed as if it were raised.

        Parameters
        -----------
        source: :class:`AudioSource`
            The audio source we're reading from.
        after: Callable[[Optional[:class:`Exception`]], Any]
            The finalizer that is called after the stream is exhausted.
            This function must have a single parameter, ``error``, that
            denotes an optional exception that was raised during playing.

        Raises
        -------
        ClientException
            Already playing audio or not connected.
        TypeError
            Source is not a :class:`AudioSource` or after is not a callable.
        OpusNotLoaded
            Source is not opus encoded and opus is not loaded.
        """
        ...
    
    def is_playing(self) -> bool:
        """Indicates if we're currently playing audio."""
        ...
    
    def is_paused(self) -> bool:
        """Indicates if we're playing audio, but if we're paused."""
        ...
    
    def stop(self) -> None:
        """Stops playing audio."""
        ...
    
    def pause(self) -> None:
        """Pauses the audio playing."""
        ...
    
    def resume(self) -> None:
        """Resumes the audio playing."""
        ...
    
    @property
    def source(self) -> Optional[AudioSource]:
        """Optional[:class:`AudioSource`]: The audio source being played, if playing.

        This property can also be used to change the audio source currently being played.
        """
        ...
    
    @source.setter
    def source(self, value: AudioSource) -> None:
        ...
    
    def send_audio_packet(self, data: bytes, *, encode: bool = ...) -> None:
        """Sends an audio packet composed of the data.

        You must be connected to play audio.

        Parameters
        ----------
        data: :class:`bytes`
            The :term:`py:bytes-like object` denoting PCM or Opus voice data.
        encode: :class:`bool`
            Indicates if ``data`` should be encoded into Opus.

        Raises
        -------
        ClientException
            You are not connected.
        opus.OpusError
            Encoding the data failed.
        """
        ...
    


