import pytest
from src.personas import (
    PERSONAS, get_persona_prompt, get_available_personas,
    is_jailbreak_persona, list_personas_for_user, is_valid_persona
)


class TestPersonas:
    def test_public_personas_exist(self):
        # Validate current public personas structure
        expected = {"helpful", "professional", "creative", "teacher", "friend", "analyst", "motivational"}
        for name in expected:
            assert name in PERSONAS
            info = PERSONAS[name]
            assert isinstance(info, dict)
            assert isinstance(info.get("prompt"), str) and info["prompt"].strip() != ""

    def test_get_persona_prompt(self):
        # Existing persona
        prompt = get_persona_prompt("creative")
        assert prompt == PERSONAS["creative"]["prompt"]
        # Fallback for unknown persona -> helpful
        prompt2 = get_persona_prompt("non-existing")
        assert prompt2 == PERSONAS["helpful"]["prompt"]

    def test_get_available_personas(self):
        personas = get_available_personas()
        assert isinstance(personas, list)
        assert "helpful" in personas and "creative" in personas
        # Restricted not in public list
        assert "jailbreak" not in personas and "debug" not in personas

    def test_list_personas_for_user_admin_includes_restricted(self):
        # Non-admin
        public = list_personas_for_user(is_admin=False)
        assert "jailbreak" not in public and "debug" not in public
        # Admin
        admin = list_personas_for_user(is_admin=True)
        assert "jailbreak" in admin and "debug" in admin

    def test_is_jailbreak_persona(self):
        # Legacy jailbreak names return True
        assert is_jailbreak_persona("jailbreak-v1") is True
        assert is_jailbreak_persona("jailbreak-v2") is True
        assert is_jailbreak_persona("jailbreak-v3") is True
        # Public personas -> False
        for name in ["helpful", "creative", "teacher", "friend"]:
            assert is_jailbreak_persona(name) is False
        # Base name also treated as jailbreak
        assert is_jailbreak_persona("jailbreak") is True

    def test_persona_prompt_structure(self):
        for name, info in PERSONAS.items():
            assert isinstance(info, dict)
            prompt = info.get("prompt", "")
            assert isinstance(prompt, str)
            assert prompt.strip() != ""
