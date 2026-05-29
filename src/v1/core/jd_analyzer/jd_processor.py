class JDProcessor:

    def clean_jd_text(
        self,
        jd_text
    ):

        cleaned_text = jd_text.strip()

        cleaned_text = cleaned_text.replace(
            "\n",
            " "
        )

        cleaned_text = " ".join(
            cleaned_text.split()
        )

        return cleaned_text