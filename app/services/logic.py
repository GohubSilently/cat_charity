from app.models import InvestmentInformation


def allocate(
    target: InvestmentInformation,
    sources: list[InvestmentInformation],
) -> list[InvestmentInformation]:
    update_sources = []
    for source in sources:
        update_sources.append(source)
        remainder = min(
            source.full_amount - source.invested_amount,
            target.full_amount - target.invested_amount
        )
        for object in (target, source):
            object.invested_amount += remainder
            object.close_fund()
        if target.fully_invested:
            break
    return update_sources
