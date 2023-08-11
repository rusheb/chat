from chat.server import hello_world

def test_dummy_server():
    assert hello_world() == "Hello, world!"