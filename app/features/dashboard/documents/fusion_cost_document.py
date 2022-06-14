from typing import TypedDict


class FusionCostDocument(TypedDict):
    color: str
    fiat_symbol: str
    fusion_fees_fiat: int
    fusion_fees_mtb: int
    input_cost_fiat: int
    input_cost_mtb: int
    inputs_cost_fiat: int
    inputs_cost_mtb: int
    inputs_count: int
    inputs_required_level: int
    market_value_fiat: float
    market_value_mtb: int
    target_name: str
    total_cost_fiat: float
    input_hero_rarity: str
    total_cost_mtb: int