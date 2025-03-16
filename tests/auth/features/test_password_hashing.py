from unittest import mock

from argon2.exceptions import VerifyMismatchError
from features.authentication.password_hashing import PasswordHashing


class TestPasswordHashing:
    def test_hash_password_returns_string(self):
        # Arrange
        test_password = "secure_password123"

        # Act
        result = PasswordHashing.hash_password(test_password)

        # Assert
        assert isinstance(result, str)
        assert result != test_password  # Hashed value should be different from original
        assert len(result) > 0

    def test_hash_password_is_salted(self):
        # Arrange
        test_password = "secure_password123"

        # Act
        # Create two hashes for the same password
        hash1 = PasswordHashing.hash_password(test_password)
        hash2 = PasswordHashing.hash_password(test_password)

        # Assert
        # Two hashes of the same password should be different due to salting
        assert hash1 != hash2

    def test_hash_password_uses_argon2(self):
        # Arrange
        test_password = "secure_password123"

        # Create a mock PasswordHasher
        mock_hasher = mock.Mock()
        mock_hasher.hash.return_value = "mocked_hash_value"

        # Act
        with mock.patch("features.authentication.password_hashing.argon2.PasswordHasher", return_value=mock_hasher):
            # Create a new instance to use our mock
            original_hasher = PasswordHashing.password_hasher
            PasswordHashing.password_hasher = mock_hasher

            try:
                result = PasswordHashing.hash_password(test_password)
            finally:
                # Restore the original hasher
                PasswordHashing.password_hasher = original_hasher

        # Assert
        mock_hasher.hash.assert_called_once_with(password=test_password)
        assert result == "mocked_hash_value"

    def test_verify_password_correct_returns_true(self):
        # Arrange
        test_password = "secure_password123"
        hashed_password = PasswordHashing.hash_password(test_password)

        # Act
        result = PasswordHashing.verify_password(test_password, hashed_password)

        # Assert
        assert result is True

    def test_verify_password_incorrect_returns_false(self):
        # Arrange
        correct_password = "secure_password123"
        incorrect_password = "wrong_password456"
        hashed_password = PasswordHashing.hash_password(correct_password)

        # Act
        result = PasswordHashing.verify_password(incorrect_password, hashed_password)

        # Assert
        assert result is False

    def test_verify_password_handles_verify_mismatch_error(self):
        # Arrange
        test_password = "secure_password123"
        hashed_password = "some_hashed_value"

        # Create a mock PasswordHasher
        mock_hasher = mock.Mock()
        mock_hasher.verify.side_effect = VerifyMismatchError()

        # Act
        with mock.patch("features.authentication.password_hashing.argon2.PasswordHasher", return_value=mock_hasher):
            # Create a new instance to use our mock
            original_hasher = PasswordHashing.password_hasher
            PasswordHashing.password_hasher = mock_hasher

            try:
                result = PasswordHashing.verify_password(test_password, hashed_password)
            finally:
                # Restore the original hasher
                PasswordHashing.password_hasher = original_hasher

        # Assert
        mock_hasher.verify.assert_called_once_with(hashed_password, test_password)
        assert result is False

    def test_verify_password_handles_invalid_hash_error(self):
        # Arrange
        test_password = "secure_password123"
        invalid_hash = "not_a_valid_hash"

        # Act & Assert
        # The verify_password method should handle this case and return False
        # rather than allowing the exception to propagate
        result = PasswordHashing.verify_password(test_password, invalid_hash)
        assert result is False

    def test_password_hasher_configuration(self):
        # This test verifies that the password hasher is configured with the expected parameters
        hasher = PasswordHashing.password_hasher

        # Using RFC_9106_HIGH_MEMORY profile
        from argon2.profiles import RFC_9106_HIGH_MEMORY

        assert hasher.time_cost == RFC_9106_HIGH_MEMORY.time_cost
        assert hasher.memory_cost == RFC_9106_HIGH_MEMORY.memory_cost
        assert hasher.parallelism == RFC_9106_HIGH_MEMORY.parallelism
        assert hasher.hash_len == RFC_9106_HIGH_MEMORY.hash_len
        assert hasher.salt_len == RFC_9106_HIGH_MEMORY.salt_len
        assert hasher.type == RFC_9106_HIGH_MEMORY.type

    def test_edge_case_empty_password(self):
        # Arrange
        empty_password = ""

        # Act
        hashed = PasswordHashing.hash_password(empty_password)
        result = PasswordHashing.verify_password(empty_password, hashed)

        # Assert
        assert result is True

    def test_edge_case_very_long_password(self):
        # Arrange
        long_password = "a" * 1000  # 1000 character password

        # Act
        hashed = PasswordHashing.hash_password(long_password)
        result = PasswordHashing.verify_password(long_password, hashed)

        # Assert
        assert result is True
