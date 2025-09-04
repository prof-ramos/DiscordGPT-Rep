import pytest


def test_setup_commands_registers():
    from src.aclient import DiscordClient
    client = DiscordClient()
    client.setup_commands()
    cmds = client.tree.get_commands()
    # Deve registrar pelo menos os 4 comandos definidos
    names = {c.name for c in cmds}
    assert {"chat","reset","persona","status"}.issubset(names)
