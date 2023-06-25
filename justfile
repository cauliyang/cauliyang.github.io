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
update: update-precommit update-theme

# Formats the code using pre-commit
format:
    # Formatting code...
    pre-commit run -a
    # Code formatting completed.

# Builds the website using Hugo
build:
    # Building website...
    hugo
    # Website build completed.

# Starts the Hugo server
server:
    # Starting Hugo server...
    hugo server

# Formats the code, builds the website, and commits the changes
commit: format build
    # Committing changes...
    aic -a
    # Changes committed.
