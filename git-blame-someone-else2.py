import click
import re
import subprocess as sp
import os


@click.command()
@click.argument("AUTHOR")
@click.argument("COMMIT")
def main(author, commit):
    aname = re.match("^(.*?)\s*<.*>$", author).groups()[0]
    aemail = re.match("^.*\s*<(.*)>$", author).groups()[0]
    scommit = commit[:7]

    cenv = os.environ.copy()
    cenv |= {
        "GIT_SEQUENCE_EDITOR": "sed -i '0,/pick/{s/pick/edit/}'",
        "GIT_COMMITER_NAME": aname,
        "GIT_COMMITER_EMAIL": aemail,

    }
    sp.run(f"git rebase -i {scommit}^", env=cenv)
    sp.run(f"git commit --amend --no-edit --author=\"{aname} <{aemail}>\"", env=cenv)
    sp.run("git rebase --continue", env=cenv)


if __name__ == "__main__":
    main()
