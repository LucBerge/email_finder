from .mailmeteor import Mailmeteor
from .smtp import Smtp

class EmailVerifierFactory:
    @staticmethod
    def create(verifier_type: str):
        verifier_type = verifier_type.strip().lower()
        if verifier_type == "mailmeteor":
            return Mailmeteor()
        if verifier_type == "smtp":
            return Smtp()
        raise ValueError(f"Unknown verifier type: {verifier_type}")