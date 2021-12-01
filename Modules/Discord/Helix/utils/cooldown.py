import asyncio
from typing import Any
from datetime import datetime, timezone, timedelta


class CoolDown:
    def __init__(self, seconds: float):
        """
        Simple cooldown mechanic.
        This class stores keys in dict which will be removed after certain X number of seconds.
        After initializing this class you should call start method.
        :param seconds: Default value to use for expiration of key if no value is passed on add_to_cool_down method.
        """
        if seconds < 1:
            raise ValueError("Cooldown has to be positive.")
        self._cool_down_seconds = timedelta(seconds=seconds)
        self._cool_downs = {}
        self._loop_running = True

    def add_to_cool_down(self, key: Any, *, seconds: int = None):
        """
        Add new key to cooldown.
        If key already is on cooldown it will be overwritten.
        :param key: any object that represents something that should be on cool-down
        :param seconds: integer representing number of seconds this key will exist before getting removed.
                        If it's not passed then default seconds will be used that was defined on class initialization.
        """
        if seconds is None:
            seconds = self._cool_down_seconds
        self._cool_downs[key] = self._get_current_datetime() + seconds

    def is_on_cool_down(self, key: Any) -> bool:
        """Checks if certain key is still on cooldown."""
        return key in self._cool_downs

    def retry_after(self, key: Any) -> float:
        """Returns float time in seconds representing time remaining until key expiration."""
        difference: timedelta = self._cool_downs[key] - self._get_current_datetime()
        return difference.seconds

    @classmethod
    def _get_current_datetime(cls) -> datetime:
        return datetime.now(timezone.utc)

    async def start(self):
        """Loop mechanics that removes expired keys."""
        while self._loop_running:
            to_delete = []
            for key, date in self._cool_downs.items():
                if self._get_current_datetime() > date:
                    to_delete.append(key)

            for key in to_delete:
                del self._cool_downs[key]

            await asyncio.sleep(1)