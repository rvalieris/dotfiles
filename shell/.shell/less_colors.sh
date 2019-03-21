# less termcap colors
# https://unix.stackexchange.com/a/108840
# man 5 terminfo
export LESS_TERMCAP_md=$(tput bold; tput setaf 6) # bold
export LESS_TERMCAP_so=$(tput setaf 0; tput setab 7) # standout
export LESS_TERMCAP_se=$(tput rmso; tput sgr0)
export LESS_TERMCAP_us=$(tput smul; tput bold; tput setaf 7) # underline
export LESS_TERMCAP_ue=$(tput rmul; tput sgr0)
export LESS_TERMCAP_me=$(tput sgr0)
#export LESS_TERMCAP_mb=$(tput bold; tput setaf 2) # blink
#export LESS_TERMCAP_mr=$(tput rev) # reverse
#export LESS_TERMCAP_mh=$(tput dim) # half-bright
#export LESS_TERMCAP_ZN=$(tput ssubm) # subscript
#export LESS_TERMCAP_ZV=$(tput rsubm)
#export LESS_TERMCAP_ZO=$(tput ssupm) # superscript
#export LESS_TERMCAP_ZW=$(tput rsupm)
