clean:
    find . -name 'themes' -prune -o -name '*DS*' -exec rm {} \;

update-theme:
    git submodule update --remote --rebase

update-precommit:
    pre-commit autoupdate

update: update-precommit update-theme

format:
    pre-commit run -a

commit: format
    aic -a
