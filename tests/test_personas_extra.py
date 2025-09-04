import pytest


def test_personas_helpers():
    from src import personas as p
    # get_all_personas includes restritas
    allp = p.get_all_personas()
    assert 'helpful' in allp and 'jailbreak' in allp
    # info + description
    info = p.get_persona_info('helpful')
    assert isinstance(info, dict)
    assert p.get_persona_description('helpful')
    # inválida
    assert p.get_persona_info('nope') is None
    assert p.get_persona_description('nope') == 'Personalidade não encontrada'
    # restrições
    assert p.is_restricted_persona('jailbreak') is True
    assert p.is_restricted_persona('helpful') is False
    # can_use_persona
    assert p.can_use_persona('jailbreak', is_admin=False) is False
    assert p.can_use_persona('jailbreak', is_admin=True) is True
    assert p.can_use_persona('helpful', is_admin=False) is True
    # list_personas_for_user
    pub = p.list_personas_for_user(False)
    adm = p.list_personas_for_user(True)
    assert 'helpful' in pub and 'jailbreak' not in pub
    assert 'jailbreak' in adm
