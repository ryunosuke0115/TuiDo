from typing import Optional, Any
import json
from pathlib import Path

class AuthService:
    def sign_up(self, supabase, email: str, password: str) -> None:
        supabase.auth.sign_up(
            {
                "email": email,
                "password": password
            }
        )

    def sign_in(self, supabase, email: str, password: str) -> Optional[Any]:
        session = supabase.auth.sign_in_with_password(
            {
                "email": email,
                "password": password
            }
        )
        return session

    def load_user_credentials(self) -> Optional[dict]:
        cred_path = Path(__file__).resolve().parent.parent.parent / "credentials" / "user.json"
        if cred_path.exists():
            with open(cred_path, "r") as f:
                return json.load(f)
        return None

    def save_user_credentials(self, email: str, password: str):
        cred_path = Path(__file__).resolve().parent.parent.parent / "credentials" / "user.json"
        with open(cred_path, "w") as f:
            json.dump({"email": email, "password": password}, f)
