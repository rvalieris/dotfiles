
# local conf
typeset -U path
[ -r $HOME/.local_shell_env ] && source $HOME/.local_shell_env

# end of non-interactive conf
[ -z "$PS1" ] && return

# set prompt
autoload colors && colors
setopt prompt_subst
PROMPT='%(?..%{$fg_no_bold[red]%}%?) %{$fg_bold[black]%}%m %{$fg_bold[blue]%}%c%{$fg_no_bold[green]%}%#%{$reset_color%} '

[ -x "$(which dircolors)" ] && eval "`dircolors -b`"
[ -x "$(which lesspipe.sh)" ] && eval "`lesspipe.sh`"

export EDITOR='vim'

# disable auto-correct
unsetopt correct_all

## Command history configuration
HISTFILE=$HOME/.zsh_history
HISTSIZE=10000
SAVEHIST=10000
setopt append_history
setopt extended_history
setopt hist_expire_dups_first
setopt hist_ignore_dups # ignore dups in command history list
setopt hist_ignore_all_dups # no seriously, ignore dups
setopt hist_reduce_blanks
setopt hist_ignore_space
setopt hist_no_store
setopt hist_verify
setopt inc_append_history
unsetopt share_history
setopt interactive_comments

# advanced tab completion
autoload -U compinit && compinit
zstyle ':completion:*' menu select
zmodload zsh/complist
zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}
zstyle ':completion:*' matcher-list 'm:{a-zA-Z}={A-Za-z}' 'r:|[._-]=* r:|=*' 'l:|=* r:|=*'
zstyle ':completion:*' tag-order '!urls'

# zsh time format
TIMEFMT=$'\nreal\t%E\nuser\t%U\nsys\t%S\ncpu\t%P'

# no beeps please
setopt no_beep

# disable flow control
stty ixoff -ixon 
stty stop undef
stty start undef
setopt no_flow_control

# aliases
[ -r $HOME/.shell/aliases.sh ] && source $HOME/.shell/aliases.sh

# prevent exiting the shell with ^D
setopt ignoreeof

# key bindings
bindkey -e
bindkey -r "${terminfo[kich1]}" # disable insert key
bindkey '\e[A' up-line-or-history
bindkey '\e[B' down-line-or-history
bindkey '\eOA' up-line-or-history
bindkey '\eOB' down-line-or-history
bindkey '\e[H' beginning-of-line
bindkey '\e[1~' beginning-of-line
bindkey '\eOH' beginning-of-line
bindkey '\e[F'  end-of-line
bindkey '\e[4~' end-of-line
bindkey '\eOF' end-of-line
bindkey '^?' backward-delete-char
bindkey '\e[3~' delete-char
bindkey '\e3;5~' delete-char
bindkey ' ' magic-space

source ~/.zsh/zsh-syntax-highlighting/zsh-syntax-highlighting.zsh
ZSH_HIGHLIGHT_HIGHLIGHTERS=(main brackets)

return 0
