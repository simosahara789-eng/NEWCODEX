from reverb_tool.client import ReverbClient


def test_client_requires_token() -> None:
    try:
        ReverbClient(token="")
        assert False, "Expected ValueError"
    except ValueError:
        assert True
