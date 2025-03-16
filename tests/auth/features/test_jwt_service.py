import uuid
from datetime import datetime
from unittest import mock

import jwt
import pytest
from features.authentication.jwt_service import JWTService, JWTToken
from settings.auth import auth_settings


class TestJWTToken:
    def test_jwt_token_initialization(self):
        # Arrange
        exp_time = int(datetime.now().timestamp()) + 3600
        entity_id = uuid.uuid4()
        token_id = uuid.uuid4()

        # Act
        token = JWTToken(ent_id=entity_id, jti=token_id, exp=exp_time)

        # Assert
        assert token.ent_id == entity_id
        assert token.jti == token_id
        assert token.exp == exp_time
        assert token.iss == auth_settings.jwt_iss
        assert token.aud == auth_settings.jwt_aud

    def test_jwt_token_default_values(self):
        # Arrange
        exp_time = int(datetime.now().timestamp()) + 3600

        # Act
        token = JWTToken(exp=exp_time)

        # Assert
        assert isinstance(token.ent_id, uuid.UUID)
        assert isinstance(token.jti, uuid.UUID)
        assert token.exp == exp_time
        assert token.iss == auth_settings.jwt_iss
        assert token.aud == auth_settings.jwt_aud

    def test_jwt_token_serialization(self):
        # Arrange
        exp_time = int(datetime.now().timestamp()) + 3600
        entity_id = uuid.uuid4()
        token_id = uuid.uuid4()
        token = JWTToken(ent_id=entity_id, jti=token_id, exp=exp_time)

        # Act
        serialized = token.model_dump(mode="json")

        # Assert
        assert serialized["ent_id"] == str(entity_id)
        assert serialized["jti"] == str(token_id)
        assert serialized["exp"] == exp_time
        assert serialized["iss"] == auth_settings.jwt_iss
        assert serialized["aud"] == list(auth_settings.jwt_aud)


class TestJWTService:
    def test_encode_token(self):
        # Arrange
        test_exp = 3600  # 1 hour
        test_entity_id = uuid.uuid4()
        now = datetime.now()

        # Act
        with mock.patch("features.authentication.jwt_service.datetime") as mock_datetime:
            mock_datetime.now.return_value = now
            token_string, token_obj = JWTService.encode(exp=test_exp, ent_id=test_entity_id)

        # Assert
        expected_exp = int(now.timestamp()) + test_exp
        assert token_obj.ent_id == test_entity_id
        assert token_obj.exp == expected_exp

        # Verify JWT was properly encoded
        decoded = jwt.decode(
            token_string, key=auth_settings.jwt_key, algorithms=[auth_settings.jwt_algo], audience=auth_settings.jwt_aud
        )
        assert decoded["ent_id"] == str(test_entity_id)
        assert decoded["exp"] == expected_exp
        assert decoded["iss"] == auth_settings.jwt_iss
        assert decoded["aud"] == list(auth_settings.jwt_aud)  # JWT converts tuple to list

    def test_decode_token(self):
        # Arrange
        test_entity_id = uuid.uuid4()
        test_jti = uuid.uuid4()
        now = datetime.now()
        exp_time = int(now.timestamp()) + 3600

        payload = {
            "ent_id": str(test_entity_id),
            "jti": str(test_jti),
            "exp": exp_time,
            "iss": auth_settings.jwt_iss,
            "aud": auth_settings.jwt_aud,
        }

        token_string = jwt.encode(payload=payload, key=auth_settings.jwt_key, algorithm=auth_settings.jwt_algo)

        # Act
        result = JWTService.decode(token_string)

        # Assert
        assert isinstance(result, JWTToken)
        assert result.ent_id == test_entity_id
        assert result.jti == test_jti
        assert result.exp == exp_time
        assert result.iss == auth_settings.jwt_iss
        assert result.aud == auth_settings.jwt_aud

    def test_issue_token_pair(self):
        # Arrange
        test_entity_id = uuid.uuid4()
        now = datetime.now()

        # Act
        with mock.patch("features.authentication.jwt_service.datetime") as mock_datetime:
            mock_datetime.now.return_value = now
            access_token, access_content, refresh_token, refresh_content = JWTService.issue_token_pair(
                ent_id=test_entity_id
            )

        # Assert
        # Check access token
        assert access_content.ent_id == test_entity_id
        assert access_content.exp == int(now.timestamp()) + auth_settings.jwt_access_ttl

        # Check refresh token
        assert refresh_content.exp == int(now.timestamp()) + auth_settings.jwt_refresh_ttl

        # Verify token strings are valid JWT
        decoded_access = jwt.decode(
            access_token, key=auth_settings.jwt_key, algorithms=[auth_settings.jwt_algo], audience=auth_settings.jwt_aud
        )
        decoded_refresh = jwt.decode(
            refresh_token,
            key=auth_settings.jwt_key,
            algorithms=[auth_settings.jwt_algo],
            audience=auth_settings.jwt_aud,
        )

        assert decoded_access["ent_id"] == str(test_entity_id)
        assert decoded_refresh["exp"] == int(now.timestamp()) + auth_settings.jwt_refresh_ttl

    def test_decode_expired_token(self):
        # Arrange
        test_entity_id = uuid.uuid4()
        now = datetime.now()
        # Create a token that expired 1 hour ago
        exp_time = int(now.timestamp()) - 3600

        payload = {
            "ent_id": str(test_entity_id),
            "jti": str(uuid.uuid4()),
            "exp": exp_time,
            "iss": auth_settings.jwt_iss,
            "aud": auth_settings.jwt_aud,
        }

        token_string = jwt.encode(payload=payload, key=auth_settings.jwt_key, algorithm=auth_settings.jwt_algo)

        # Act & Assert
        with pytest.raises(jwt.ExpiredSignatureError):
            JWTService.decode(token_string)

    def test_decode_invalid_signature(self):
        # Arrange
        test_entity_id = uuid.uuid4()
        now = datetime.now()
        exp_time = int(now.timestamp()) + 3600

        payload = {
            "ent_id": str(test_entity_id),
            "jti": str(uuid.uuid4()),
            "exp": exp_time,
            "iss": auth_settings.jwt_iss,
            "aud": auth_settings.jwt_aud,
        }

        # Use a different key than the one in settings
        token_string = jwt.encode(payload=payload, key="wrong_key", algorithm=auth_settings.jwt_algo)

        # Act & Assert
        with pytest.raises(jwt.InvalidSignatureError):
            JWTService.decode(token_string)

    def test_decode_invalid_audience(self):
        # Arrange
        test_entity_id = uuid.uuid4()
        now = datetime.now()
        exp_time = int(now.timestamp()) + 3600

        payload = {
            "ent_id": str(test_entity_id),
            "jti": str(uuid.uuid4()),
            "exp": exp_time,
            "iss": auth_settings.jwt_iss,
            "aud": ["invalid_audience"],  # Different audience than configured
        }

        token_string = jwt.encode(payload=payload, key=auth_settings.jwt_key, algorithm=auth_settings.jwt_algo)

        # Act & Assert
        with pytest.raises(jwt.InvalidAudienceError):
            JWTService.decode(token_string)
