[ -z "$PS1" ] && return

PS1='\[\e[0;31m\]$(ec=$?;[ $ec -ne 0 ] && echo -n "$ec") \[\e[1;30m\]\h \[\e[1;34m\]\W\[\e[0;32m\]\$ \[\e[0;40m\]'

# disable flow control
stty ixoff -ixon
stty stop undef
stty start undef

# aliases
[ -r $HOME/.shell/aliases.sh ] && source $HOME/.shell/aliases.sh
[ -x "$(which lesspipe.sh)" ] && eval "`lesspipe.sh`"
[ -x "$(which dircolors)" ] && eval "`dircolors -b`"

# local scripts and binaries
for i in $HOME/.local/bin; do
	case ":$PATH:" in
		*":$i:"*) :;;
		*) PATH="$i:$PATH";;
	esac
done

export EDITOR='vim'
export HISTCONTROL=ignoredups

# prevent shell from exiting with Ctrl-d
IGNOREEOF=10

# local conf
[ -r $HOME/.bash_localrc ] && source $HOME/.bash_localrc

