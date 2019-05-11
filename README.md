# aioaprs

Asyncio Based APRS client

## Usage

### Install

```bash
$ pip install -U https://github.com/mrasband/aioaprs.get
```


### Use

```python
import asyncio
import dataclasses
import logging
import re
from typing import List, Optional

from . import (
    APRSClient,
    AreaFilter,
    Point,
    RangeFilter,
    TypeFilter,
    Types,
)

logging.basicConfig(level=logging.INFO)


async def main():
    async with APRSClient("KD0VTE", filters=[
        RangeFilter(Point(39.545917, -104.927592), 100),
        # Ignore everything except the Position reports
        ~TypeFilter([
            Types.ITEMS,
            Types.MESSAGE,
            Types.NWS,
            Types.OBJECTS,
            # Types.POSITION,
            Types.QUERY,
            Types.STATUS,
            Types.TELEMETRY,
            Types.USER_DEFINED,
            Types.WEATHER,
        ]),
    ]) as client:
        async for packet in client:
            print(packet)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
```
