class FileValidator:
   

    ALLOWED_EXTENSIONS = [
        "pdf",
   
        "docx",
        "txt"
    ]


    def validate_extension(
            self,
            filename
    ):
        if not filename:

            return False

        normalized_filename = filename.lower()

        return any(
            normalized_filename.endswith(
                f".{ext}"
            )
            for ext in self.ALLOWED_EXTENSIONS
        )

    def validate_Extension(
            self,
            filename
    ):

        return self.validate_extension(
            filename
        )
        