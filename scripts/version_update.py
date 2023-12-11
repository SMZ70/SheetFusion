import re
from pathlib import Path

import toml

ROOT_DIR = Path(__file__).parent.parent


def get_semantic_version(version):
    # Extract the semantic version (major.minor.patch) from the full version
    semantic_prerelease = re.match(r"^(\d+\.\d+\.\d+)(?:-(.+))?", version)

    if semantic_prerelease:
        semantic_version = semantic_prerelease.group(1)
        pre_release = semantic_prerelease.group(2) or ""
        return semantic_version, pre_release

    raise ValueError(f"Semantic version not found in {version}")


if __name__ == "__main__":
    # Read the version from the .toml file
    with open(ROOT_DIR / "pyproject.toml", "r") as toml_file:
        data = toml.load(toml_file)

    try:
        version = data["project"]["version"]
    except KeyError:
        raise ValueError("Version not found in pyproject.toml")

    # Check if the changelog includes the semantic version
    semantic_version, pre_release = get_semantic_version(version)
    with open(ROOT_DIR / "CHANGELOG.md", "r") as changelog_file:
        changelog = changelog_file.read()

    if semantic_version not in changelog and not pre_release:
        raise ValueError(
            f"Semantic version {semantic_version} not found in CHANGELOG.md"
        )

    # Replace the version in the README
    with open(ROOT_DIR / "README.md", "r+") as readme_file:
        readme_content = readme_file.read()

        # Replace the version in the README. Example:
        # [version]: https://img.shields.io/badge/Version-1.0.4-blue
        current_version = re.search(
            r"^\[version\]\:\s*https:.+Version-(.+)\-",
            readme_content,
            re.MULTILINE,
        )
        if current_version:
            readme_content = readme_content.replace(
                current_version.group(1), semantic_version + pre_release
            )
            readme_file.seek(0)
            readme_file.write(readme_content)
            readme_file.truncate()
        else:
            raise ValueError("Version not found in README.md")
