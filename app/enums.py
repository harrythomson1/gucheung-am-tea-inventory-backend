import enum


class TransactionType(enum.Enum):
    sale = "sale"
    donation = "donation"
    ceremony = "ceremony"
    damaged = "damaged"
    convert = "convert"
    harvest = "harvest"
    repackage = "repackage"


class SalesChannelType(enum.Enum):
    online = "online"
    offline = "offline"


class PackagingType(enum.Enum):
    silver = "silver"
    wing = "wing"
    gift = "gift"
    mixed = "mixed"
    standard = "standard"


class FlushType(enum.Enum):
    first = "first"
    second = "second"
    mixed = "mixed"
