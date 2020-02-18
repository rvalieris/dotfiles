
# env vars
[ -r ~/.config/shell/env.sh ] && source ~/.config/shell/env.sh

# remove duplicates from PATH
export PATH="$(perl -e 'print join(":", grep { not $seen{$_}++ } split(/:/, $ENV{PATH}))')"
export MANPATH="$(perl -e 'print join(":", grep { not $seen{$_}++ } split(/:/, $ENV{MANPATH}))'):"

# end of non-interactive conf
[ -z "$PS1" ] && return

# interactive stuff
source ~/.config/shell/interactive.env.sh

PS1="\[$(tput setaf 1)\]"
PS1+='$(ec=$?;[ $ec -ne 0 ] && echo -n "$ec") '
PS1+="\[$(tput bold;tput setaf 0)\]"'\h '
PS1+="\[$(tput setaf 4)\]"'\W'
PS1+="\[$(tput setaf 2)\]"'\$ '"\[$(tput sgr0)\]"

# disable flow control
stty ixoff -ixon
stty stop undef
stty start undef

export HISTFILE=~/.cache/bash_history
export HISTCONTROL=ignoredups

# prevent shell from exiting with Ctrl-d
IGNOREEOF=10

shopt -s checkwinsize

# case insensitive completion
bind 'set completion-ignore-case on'
