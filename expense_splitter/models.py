from dataclasses import dataclass, field


@dataclass
class Expense:
    description: str
    amount: float
    payer: str
    participants: list
    mode: str = "equal"          # equal | percent | shares
    weights: dict = field(default_factory=dict)
    category: str = "general"
