#!/bin/bash
set -e
ST="stow -R -t $HOME $@"

$ST zsh
$ST vim
$ST bash
$ST tmux
$ST shell
$ST R
$ST --no-folding tools
$ST --no-folding vimswaps

