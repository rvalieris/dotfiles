
# my dotfiles


### install

```bash
git clone --recursive this.repo ~/dotfiles
# or
rsync -crPl ~/dotfiles remote:~
# and sometimes --delete
```

### update submodules
```bash
cd dotfiles
git submodule foreach git pull origin master
```

### init the dotfiles
```bash
./stow.sh
```

