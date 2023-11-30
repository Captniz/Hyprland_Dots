:set number
:set autoindent
:set tabstop=4
:set shiftwidth=4
:set smarttab
:set softtabstop=4
:set mouse=a
:set background=light

call plug#begin('~/.config/nvim/plugged')

Plug 'nvim-lualine/lualine.nvim' "x
Plug 'kyazdani42/nvim-web-devicons'
Plug 'https://github.com/neovim/nvim-lspconfig' "x
Plug 'williamboman/mason-lspconfig.nvim'
Plug 'williamboman/mason.nvim'
Plug 'http://github.com/tpope/vim-surround' "x
Plug 'https://github.com/preservim/nerdtree' "x
Plug 'https://github.com/tpope/vim-commentary' "x
Plug 'https://github.com/lifepillar/pgsql.vim' "x
Plug 'https://github.com/ap/vim-css-color' "x
Plug 'https://github.com/rafi/awesome-vim-colorschemes' "x
Plug 'https://github.com/neoclide/coc.nvim' "x
Plug 'https://github.com/ryanoasis/vim-devicons' "x
Plug 'https://github.com/tc50cal/vim-terminal' "x
Plug 'https://github.com/preservim/tagbar' "x
Plug 'https://github.com/terryma/vim-multiple-cursors' "x
Plug 'sainnhe/everforest' "x
Plug 'nvim-treesitter/nvim-treesitter', {'do': ':TSUpdate'} "x
Plug 'https://github.com/sheerun/vim-polyglot' "x

set encoding=UTF-8

call plug#end()

let &t_8f = "\<Esc>[38;2;%lu;%lu;%lum"
let &t_8b = "\<Esc>[48;2;%lu;%lu;%lum"

" Enable syntax highlighting 
syntax enable
" Enable 256 colors palette 
set t_Co=256
" Important!! 
if has('termguicolors') 
    set termguicolors 
endif

nnoremap <C-f> :NERDTreeFocus<CR>
nnoremap <C-n> :NERDTree<CR>
nnoremap <C-t> :NERDTreeToggle<CR>
nnoremap <C-l> :call CocActionAsync('jumpDefinition')<CR>

nmap <F8> :TagbarToggle<CR>

:set completeopt-=preview " For No Previews

let g:NERDTreeDirArrowExpandable="+"
let g:NERDTreeDirArrowCollapsible="~"

" --- Just Some Notes ---
" :PlugClean :PlugInstall :UpdateRemotePlugins
"
" :CocInstall coc-python
" :CocInstall coc-clangd
" :CocInstall coc-snippets
" :CocCommand snippets.edit... FOR EACH FILE TYPE

" air-line
let g:airline_powerline_fonts = 1

if !exists('g:airline_symbols')
    let g:airline_symbols = {}
endif

" airline symbols
let g:airline_left_sep = ''
let g:airline_left_alt_sep = ''
let g:airline_right_sep = ''
let g:airline_right_alt_sep = ''
let g:airline_symbols.branch = ''
let g:airline_symbols.readonly = ''
let g:airline_symbols.linenr = ''

inoremap <expr> <Tab> pumvisible() ? coc#_select_confirm() : "<Tab>"


lua << END
require("mason-lspconfig").setup()
require("mason-lspconfig").setup()
require("mason").setup()
require('lualine').setup {
  options = {
    icons_enabled = true,
    theme = 'gruvbox-material',
    component_separators = { left = '', right = ''},
    section_separators = { left = '', right = ''},
    disabled_filetypes = {
      statusline = {},
      winbar = {},
    },
    ignore_focus = {},
    always_divide_middle = true,
    globalstatus = false,
    refresh = {
      statusline = 1000,
      tabline = 1000,
      winbar = 1000,
    }
  },
  sections = {
    lualine_a = {'mode'},
    lualine_b = {'branch', 'diff', 'diagnostics'},
    lualine_c = {'filename'},
    lualine_x = {'encoding', 'fileformat', 'filetype'},
    lualine_y = {'progress'},
    lualine_z = {'location'}
  },
  inactive_sections = {
    lualine_a = {},
    lualine_b = {},
    lualine_c = {'filename'},
    lualine_x = {'location'},
    lualine_y = {},
    lualine_z = {}
  },
  tabline = {},
  winbar = {},
  inactive_winbar = {},
  extensions = {}
}
END
