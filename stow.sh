#!/bin/bash
set -e

# check .stowrc file with extra args

stow zsh
stow vim
stow bash
stow tmux
stow shell
stow R
stow --no-folding tools
stow --no-folding vimswaps

