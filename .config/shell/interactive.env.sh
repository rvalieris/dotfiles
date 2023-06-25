
# lesspipe
[ -x "$(command -v lesspipe)" ] && eval "$(lesspipe)"
[ -x "$(command -v lesspipe.sh)" ] && eval "$(lesspipe.sh)"
export LESSHISTFILE=~/.cache/lesshst
export SYSTEMD_LESS="FSRM"

# ls colors
if [ ~/.cache/LS_COLORS -nt ~/.config/shell/LS_COLORS.gen.sh ]; then
	source ~/.cache/LS_COLORS
elif [ -x "$(command -v dircolors)" ]; then
	source ~/.config/shell/LS_COLORS.gen.sh | dircolors -b - > ~/.cache/LS_COLORS
	source ~/.cache/LS_COLORS
fi

# aliases
source ~/.config/shell/aliases.sh

# less colors
source ~/.config/shell/less_colors.sh

