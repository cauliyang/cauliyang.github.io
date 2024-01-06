# vim: set ft=make :

# Starts the Hugo server
server:
    # Starting Hugo server...
    hugo server

# Cleans all files named '*DS*' while ignoring the 'themes' directory
clean:
    # Starting cleanup...
    find . -name 'themes' -prune -o -name '*DS*' -exec rm {} \;
    # Cleanup completed.

# Checks for broken links in the content using lychee
check-link:
    # Checking for broken links...
    lychee  --cache --suggest content
    # Link check completed.

update-tikz:
	wget https://raw.githubusercontent.com/cauliyang/learn_tikz/main/main.pdf -O  content/latex/020-Tikz-learn-jouney/gallery/tikz.pdf

update-scinote:
	cp ../learning_notes/html/scinote.html static/

# Updates the 'themes' git submodule
update-theme:
    # Updating themes...
    git submodule update --remote --rebase
    # Themes update completed.

# Updates the pre-commit hooks
update-precommit:
    # Updating pre-commit hooks...
    pre-commit autoupdate
    # Pre-commit hooks update completed.

# Calls update-theme and update-precommit
update: update-precommit update-theme update-tikz

# Formats the code using pre-commit
format: clean
    # Formatting code...
    pre-commit run -a
    # Code formatting completed.

# Builds the website using Hugo
build:
    # Building website...
    hugo
    # Website build completed.

# Formats the code, builds the website, and commits the changes
commit: format build
    # Committing changes...
    git add .
    aic
    # Changes committed.
