import uuid
from unittest.mock import patch

import pytest

from app.seller.model import Seller
from app.seller.service import create_seller, get_seller_by_token, generate_nickname


class TestGenerateNickname:
    def test_format(self):
        nickname = generate_nickname()
        parts = nickname.split("-")
        assert len(parts) == 3
        assert parts[2].isdigit()

    def test_randomness(self):
        nicknames = {generate_nickname() for _ in range(10)}
        assert len(nicknames) > 1


class TestCreateSeller:
    def test_creates_with_token_and_nickname(self, db):
        seller = create_seller(db)
        assert seller.id is not None
        assert isinstance(seller.token, uuid.UUID)
        assert len(seller.nickname) > 0

    def test_unique_tokens(self, db):
        s1 = create_seller(db)
        s2 = create_seller(db)
        assert s1.token != s2.token

    def test_unique_nicknames(self, db):
        s1 = create_seller(db)
        s2 = create_seller(db)
        assert s1.nickname != s2.nickname

    def test_retries_on_duplicate_nickname(self, db):
        existing = create_seller(db)
        with patch(
            "app.seller.service.generate_nickname",
            side_effect=[existing.nickname, "새로운-닉네임-42"],
        ):
            seller = create_seller(db)
        assert seller.nickname == "새로운-닉네임-42"

    def test_raises_when_retries_exhausted(self, db):
        existing = create_seller(db)
        with patch(
            "app.seller.service.generate_nickname",
            return_value=existing.nickname,
        ):
            with pytest.raises(RuntimeError, match="닉네임 생성에 실패"):
                create_seller(db)


class TestGetSellerByToken:
    def test_found(self, db):
        seller = create_seller(db)
        found = get_seller_by_token(db, str(seller.token))
        assert found is not None
        assert found.id == seller.id

    def test_not_found(self, db):
        result = get_seller_by_token(db, str(uuid.uuid4()))
        assert result is None
