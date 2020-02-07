
# local conf
[ -r $HOME/.local_shell_env ] && source $HOME/.local_shell_env

# remove duplicates from PATH
export PATH="$(perl -e 'print join(":", grep { not $seen{$_}++ } split(/:/, $ENV{PATH}))')"
export MANPATH="$(perl -e 'print join(":", grep { not $seen{$_}++ } split(/:/, $ENV{MANPATH}))')"

# end of non-interactive conf
[ -z "$PS1" ] && return

PS1="\[$(tput setaf 1)\]"
PS1+='$(ec=$?;[ $ec -ne 0 ] && echo -n "$ec") '
PS1+="\[$(tput bold;tput setaf 0)\]"'\h '
PS1+="\[$(tput setaf 4)\]"'\W'
PS1+="\[$(tput setaf 2)\]"'\$ '"\[$(tput sgr0)\]"
export PATH

# disable flow control
stty ixoff -ixon
stty stop undef
stty start undef

# aliases
[ -r $HOME/.shell/aliases.sh ] && source $HOME/.shell/aliases.sh

export HISTCONTROL=ignoredups

# prevent shell from exiting with Ctrl-d
IGNOREEOF=10

shopt -s checkwinsize
