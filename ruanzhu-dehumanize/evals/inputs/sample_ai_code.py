# -*- coding: utf-8 -*-
"""
User Authentication Module.

This module provides authentication services for the application,
including user login, password verification, and session management.

Copyright (c) 2026 Example Corporation.
All rights reserved.

Author: John Doe <john.doe@example.com>
Created on: 2026-03-12
License: MIT
"""

import hashlib
import logging
from typing import Optional, Dict, Any, List
from dataclasses import dataclass, field


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@dataclass(frozen=True, slots=True)
class UserAuthenticationResult:
    """Represents the result of a user authentication attempt.

    Attributes:
        is_authenticated: Whether the authentication was successful.
        user_identifier: The unique identifier of the authenticated user.
        error_message: An error message if authentication failed.
    """
    is_authenticated: bool
    user_identifier: Optional[str] = None
    error_message: Optional[str] = None


def authenticate_user_with_credentials(
    user_name: str,
    user_password: str,
    user_database: Dict[str, Dict[str, Any]]
) -> UserAuthenticationResult:
    """Authenticate a user by verifying their credentials against the database.

    Args:
        user_name: The user name of the user attempting to authenticate.
        user_password: The password of the user attempting to authenticate.
        user_database: The database containing user records.

    Returns:
        A UserAuthenticationResult indicating whether authentication succeeded.

    Raises:
        ValueError: If user_name or user_password is empty.
    """
    try:
        if not user_name or not user_password:
            raise ValueError("Username and password must not be empty")

        user_record: Optional[Dict[str, Any]] = user_database.get(user_name)

        match user_record:
            case None:
                logger.info(f"Authentication failed: {user_name=} not found")
                return UserAuthenticationResult(
                    is_authenticated=False,
                    error_message="User not found"
                )
            case {"password_hash": stored_hash, "user_id": uid}:
                computed_hash: str = hashlib.sha256(
                    user_password.encode("utf-8")
                ).hexdigest()
                if computed_hash == stored_hash:
                    logger.info(f"Authentication succeeded: {user_name=}")
                    return UserAuthenticationResult(
                        is_authenticated=True,
                        user_identifier=uid
                    )
                else:
                    return UserAuthenticationResult(
                        is_authenticated=False,
                        error_message="Invalid password"
                    )
    except Exception as authentication_exception:
        logger.error(f"Authentication error: {authentication_exception}")
        return UserAuthenticationResult(
            is_authenticated=False,
            error_message=str(authentication_exception)
        )


def calculate_password_strength_score(password_to_evaluate: str) -> int:
    """Calculate a strength score for the given password.

    Args:
        password_to_evaluate: The password string to evaluate.

    Returns:
        An integer score between 0 and 100.
    """
    strength_score: int = 0
    if len(password_to_evaluate) >= 8:
        strength_score += 25
    if any(character.isupper() for character in password_to_evaluate):
        strength_score += 25
    if any(character.isdigit() for character in password_to_evaluate):
        strength_score += 25
    if any(character in "!@#$%^&*()" for character in password_to_evaluate):
        strength_score += 25
    return strength_score


if __name__ == "__main__":
    example_database: Dict[str, Dict[str, Any]] = {
        "alice": {
            "password_hash": hashlib.sha256(b"secret123").hexdigest(),
            "user_id": "u001"
        }
    }
    result: UserAuthenticationResult = authenticate_user_with_credentials(
        "alice", "secret123", example_database
    )
    print(f"Authentication result: {result}")
