from dataclasses import dataclass


@dataclass(frozen=True)
class Operation:
    name: str
    method: str
    path: str
    description: str


OPERATIONS: dict[str, Operation] = {
    "read_feedback": Operation("read_feedback", "GET", "/my/feedback", "Read feedback sent/received"),
    "write_feedback": Operation("write_feedback", "POST", "/my/feedback", "Create feedback"),
    "read_payouts": Operation("read_payouts", "GET", "/my/payouts", "Read payouts"),
    "read_listings": Operation("read_listings", "GET", "/my/listings", "Read listings"),
    "write_listings": Operation("write_listings", "POST", "/my/listings", "Create/update listings"),
    "read_lists": Operation("read_lists", "GET", "/my/feed", "Read watch list/feed"),
    "write_lists": Operation("write_lists", "POST", "/my/feed", "Update watch list/feed"),
    "read_messages": Operation("read_messages", "GET", "/my/messages", "Read messages"),
    "write_messages": Operation("write_messages", "POST", "/my/messages", "Send/update messages"),
    "read_offers": Operation("read_offers", "GET", "/my/offers", "Read offers"),
    "write_offers": Operation("write_offers", "POST", "/my/offers", "Create offers"),
    "read_orders": Operation("read_orders", "GET", "/my/orders", "Read orders"),
    "write_orders": Operation("write_orders", "PUT", "/my/orders", "Update order status"),
    "read_profile": Operation("read_profile", "GET", "/my/profile", "Read profile/shop details"),
    "write_profile": Operation("write_profile", "PUT", "/my/profile", "Update profile/shop settings"),
    "read_reviews": Operation("read_reviews", "GET", "/my/reviews", "Read reviews"),
    "write_reviews": Operation("write_reviews", "POST", "/my/reviews", "Write reviews"),
    "read_addresses": Operation("read_addresses", "GET", "/my/addresses", "Read addresses"),
    "write_addresses": Operation("write_addresses", "PUT", "/my/addresses", "Update addresses"),
}
