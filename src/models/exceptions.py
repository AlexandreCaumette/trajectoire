class CustomException(Exception):
    def __init__(self, message, code_erreur=None) -> None:
        self.message = message
        self.code_erreur = code_erreur

        super().__init__(self.message)

    def __str__(self):
        string = self.message

        if self.code_erreur is not None:
            string = f"{string} (Code erreur : {self.code_erreur})"

        return string
