from utils import script_directory


def specialize_template(template_path: str, specialization: list[tuple[str, str]]) -> str:
    with open(f"{script_directory()}/templates/{template_path}.template", "r") as f:
        contents = f.read()

        for (term, replacement) in specialization:
            searched = f"@@@{term}@@@"
            contents = contents.replace(searched, replacement)

        return contents


def specialize_template_to_file(template_path: str, output_path: str,
                                specialization: list[tuple[str, str]]):
    specialized = specialize_template(template_path, specialization)
    with open(output_path, "w") as f:
        f.write(specialized)
