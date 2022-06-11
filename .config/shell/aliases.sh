
# common aliases
alias ls='ls --color=auto'
alias l='less -S'
alias ll='ls -lh'
alias ld='ll -d */'
alias la='ll -A'
alias df='df -hTP'
alias rm='rm -i'
alias cp='cp -i'
alias mv='mv -i'
alias grep='grep --color=auto'
alias ip='ip -color=auto'

# pgrep but better
pg() {
	T=$(mktemp)
	ps -eo pid,user,stat,ucomm,args > $T
	head -n1 $T
	tail -n+2 $T | grep "$@"
	rm -f $T
}

# haskell stuff
alias ghm='ghc --make -O3 -outputdir=/tmp/ -fforce-recomp'
alias ghi='ghci +RTS -M1G -RTS'
alias ghp='ghc -prof -fprof-auto -rtsopts -outputdir=/tmp/'

# etc
alias mupdf='mupdf -A2'
alias cl="xsv table -d'\t'"
alias R='R --quiet --no-save'
alias r='radian'

# singularity
alias sgl=singularity
