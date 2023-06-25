clean:
    find . -name 'themes' -prune -o -name '*DS*' -exec rm {} \;

check-link:
    lychee  --cache --suggest content


update-theme:
    git submodule update --remote --rebase

update-precommit:
    pre-commit autoupdate

update: update-precommit update-theme

format:
    pre-commit run -a

build:
    hugo

commit: format build
    aic -a
