with import <nixpkgs> {};
{
  allowUnfree = true;

  packageOverrides = pkgs: {
    dunst = pkgs.dunst.override { dunstify = true; };
  };
}
