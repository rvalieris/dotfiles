
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

# haskell stuff
alias ghm='ghc --make -O3 -outputdir=/tmp/ -fforce-recomp'
alias ghi='ghci +RTS -M1G -RTS'
alias ghp='ghc -prof -fprof-auto -rtsopts -outputdir=/tmp/'

# etc
alias mupdf='mupdf -A2'
alias cl="xsv table -d'\t'"
alias R='R --quiet --no-save'
alias nix-up="nix-channel --update && nix-env -u"
alias apt-up='sudo apt update && sudo apt upgrade'
alias up-up='apt-up && nix-up && rustup update && conda update --all'

# singularity
alias sgl=singularity
