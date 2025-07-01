from .mailmeteor import Mailmeteor

class EmailVerifierFactory:
    @staticmethod
    def create(verifier_type: str):
        verifier_type = verifier_type.strip().lower()
        if verifier_type == "mailmeteor":
            return Mailmeteor()
        raise ValueError(f"Unknown verifier type: {verifier_type}")