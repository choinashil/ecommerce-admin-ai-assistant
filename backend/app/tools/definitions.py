TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "create_product",
            "description": "새로운 상품을 등록한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "name": {
                        "type": "string",
                        "description": "상품명",
                    },
                    "price": {
                        "type": "integer",
                        "description": "상품 가격 (원)",
                    },
                },
                "required": ["name", "price"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "list_products",
            "description": "등록된 상품 목록을 조회한다.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["active", "inactive"],
                        "description": "상품 상태 필터 (미지정 시 전체 조회)",
                    },
                },
            },
        },
    },
]
