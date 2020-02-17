
" organized by vim :options order

" important, bootstrap pathogen & submodules
set nocompatible
set encoding=utf-8
scriptencoding utf-8
set runtimepath^=~/.config/vim
runtime bundle/pathogen/autoload/pathogen.vim
execute pathogen#infect()
filetype plugin on

" moving around, searching and patterns
set incsearch
set ignorecase
set smartcase

" displaying text
set scrolloff=2
set number
set fillchars=vert:\ 
set list " make tabs visible
set listchars=tab:»\ 

" syntax, highlighting and spelling
syntax on
colorscheme molokai
set background=dark
set hlsearch
set cursorline
set termguicolors

" multiple windows
set laststatus=2
set hidden

" terminal
set notitle
set ttyfast

" GUI
set guicursor+=a:blinkon0-block-Cursor
set guioptions-=T
set guifont=DejaVu\ Sans\ Mono\ 10

" messages and info
set ruler
set showcmd
set noshowmode
set report=0
set belloff=all

" editing text
set backspace=indent,eol,start

" tabs and indenting
set tabstop=8
set noexpandtab
set softtabstop=0
set nosmarttab

" mapping
set ttimeoutlen=50
let mapleader = " "
noremap <leader><space> :noh<cr>
noremap <leader>n :Vexplore .<cr>
noremap <leader>m :Sexplore .<cr>
noremap <leader>b :Unite -no-split -quick-match buffer<cr>
noremap <leader>y :Unite -no-split history/yank<cr>
noremap <leader>h 0
noremap <leader>j <pagedown>
noremap <leader>k <pageup>
noremap <leader>l $
noremap Q <nop>
noremap ; :
inoremap ç <esc>
nnoremap ç <esc>
vnoremap ç <esc>
inoremap <f1> <esc>
nnoremap <f1> <esc>
vnoremap <f1> <esc>

noremap <leader><left> <C-w><
noremap <leader><down> <C-W>-
noremap <leader><up> <C-W>+
noremap <leader><right> <C-w>>

" the swap file
set directory=~/.cache/vim/swap//

" command line editing
set wildmenu
set wildmode=longest:full

" 25 various
set viminfo+=n~/.cache/vim/viminfo

" override some ftplugins set's
autocmd FileType * setlocal formatoptions-=c formatoptions-=r formatoptions-=o noexpandtab softtabstop=0 tabstop=8 nosmartindent

" etc
let g:netrw_liststyle=3
let g:unite_source_history_yank_enable=1
let g:unite_source_history_yank_limit=50
let g:airline_left_sep=''
let g:airline_right_sep=''
let g:airline#extensions#whitespace#enabled = 0
let g:airline_theme='murmur'
let g:python_recommended_style = 0
