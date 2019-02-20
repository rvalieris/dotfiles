
# local conf
[ -r $HOME/.local_shell_env ] && source $HOME/.local_shell_env

# remove duplicates from PATH
export PATH="$(perl -e 'print join(":", grep { not $seen{$_}++ } split(/:/, $ENV{PATH}))')"

# end of non-interactive conf
[ -z "$PS1" ] && return

PS1='\e[0;31m$(ec=$?;[ $ec -ne 0 ] && echo -n "$ec") \e[1;30m\h \e[1;34m\W\e[0;32m\$ \e[0;40m'

# disable flow control
stty ixoff -ixon
stty stop undef
stty start undef

# aliases
[ -r $HOME/.shell/aliases.sh ] && source $HOME/.shell/aliases.sh
[ -x "$(which dircolors)" ] && eval "`dircolors -b`"

export EDITOR='vim'
export HISTCONTROL=ignoredups

# prevent shell from exiting with Ctrl-d
IGNOREEOF=10


