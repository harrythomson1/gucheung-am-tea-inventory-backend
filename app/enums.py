import enum


class TransactionType(enum.Enum):
    sale = "sale"
    donation = "donation"
    ceremony = "ceremony"
    damaged = "damaged"
    convert = "convert"
    harvest = "harvest"


class SalesChannelType(enum.Enum):
    online = "online"
    offline = "offline"


class PackagingType(enum.Enum):
    foil = "foil"
    wing = "wing"
    gift = "gift"


class FlushType(enum.Enum):
    first = "first"
    second = "second"
