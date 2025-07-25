from common import dates
from common.git import Git
from common.releasedata import ProductData, config_from_argv

"""Fetches Apache HTTP Server versions and release date from its git repository
by looking at the STATUS file of each <major>.<minor>.x branch."""

config = config_from_argv()
with ProductData(config.product) as product_data:
    git = Git(config.url)
    git.setup()

    for branch in git.list_branches("refs/heads/?.?.x"):
        git.checkout(branch, file_list=["STATUS"])

        release_notes_file = git.repo_dir / "STATUS"
        if not release_notes_file.exists():
            continue

        with release_notes_file.open("rb") as f:
            release_notes = f.read().decode("utf-8", errors="ignore")

        for pattern in config.include_version_patterns:
            for (version, date_str) in pattern.findall(release_notes):
                product_data.declare_version(version, dates.parse_date(date_str))
