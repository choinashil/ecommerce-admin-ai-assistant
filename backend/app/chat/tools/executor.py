from sqlalchemy.orm import Session

from app.shared.display_id import to_display_id
from app.guide.service import search_guide
from app.product.service import create_product, list_products


def execute_tool(db: Session, tool_name: str, arguments: dict) -> dict:
    """tool_name에 해당하는 함수를 실행하고 결과를 dict로 반환한다."""
    handler = _TOOL_HANDLERS.get(tool_name)

    if handler is None:
        return {"error": f"알 수 없는 tool: {tool_name}"}

    return handler(db, arguments)


def _handle_search_guide(db: Session, arguments: dict) -> dict:
    query = arguments["query"]
    results = search_guide(db, query)
    return {"results": results, "total": len(results)}


def _handle_create_product(db: Session, arguments: dict) -> dict:
    product = create_product(db, name=arguments["name"], price=arguments["price"])
    return {
        "id": to_display_id("products", product.id),
        "name": product.name,
        "price": product.price,
        "status": product.status.value,
        "created_at": product.created_at.isoformat(),
        "updated_at": product.updated_at.isoformat(),
    }


def _handle_list_products(db: Session, arguments: dict) -> dict:
    status = arguments.get("status")
    products = list_products(db, status=status)
    return {
        "products": [
            {
                "id": to_display_id("products", p.id),
                "name": p.name,
                "price": p.price,
                "status": p.status.value,
                "created_at": p.created_at.isoformat(),
                "updated_at": p.updated_at.isoformat(),
            }
            for p in products
        ],
        "total": len(products),
    }


_TOOL_HANDLERS = {
    "search_guide": _handle_search_guide,
    "create_product": _handle_create_product,
    "list_products": _handle_list_products,
}
