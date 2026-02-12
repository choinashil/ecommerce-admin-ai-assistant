import pytest

from app.display_id import to_display_id, from_display_id, parse_pk


class TestToDisplayId:
    def test_conversations(self):
        assert to_display_id("conversations", 1) == "CON-1"

    def test_messages(self):
        assert to_display_id("messages", 42) == "MSG-42"

    def test_products(self):
        assert to_display_id("products", 100) == "PRD-100"

    def test_orders(self):
        assert to_display_id("orders", 7) == "ORD-7"

    def test_unknown_table(self):
        with pytest.raises(KeyError):
            to_display_id("unknown", 1)


class TestFromDisplayId:
    def test_conversations(self):
        assert from_display_id("CON-1") == ("conversations", 1)

    def test_messages(self):
        assert from_display_id("MSG-42") == ("messages", 42)

    def test_products(self):
        assert from_display_id("PRD-100") == ("products", 100)

    def test_orders(self):
        assert from_display_id("ORD-7") == ("orders", 7)

    def test_large_number(self):
        assert from_display_id("CON-99999") == ("conversations", 99999)

    def test_no_dash(self):
        with pytest.raises(ValueError, match="잘못된 display ID 형식"):
            from_display_id("CON1")

    def test_empty_string(self):
        with pytest.raises(ValueError, match="잘못된 display ID 형식"):
            from_display_id("")

    def test_unknown_prefix(self):
        with pytest.raises(ValueError, match="알 수 없는 prefix"):
            from_display_id("XXX-1")


class TestParsePk:
    def test_correct_table(self):
        assert parse_pk("CON-5", "conversations") == 5

    def test_table_mismatch(self):
        with pytest.raises(ValueError, match="잘못된 ID 타입"):
            parse_pk("CON-1", "orders")

    def test_msg_correct(self):
        assert parse_pk("MSG-10", "messages") == 10
