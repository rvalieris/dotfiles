with import <nixpkgs> {};
{
  allowUnfree = true;

  packageOverrides = pkgs: {
    # https://github.com/NixOS/nixpkgs/issues/124965
    rofi = pkgs.rofi.overrideAttrs (oldAttrs: rec {
      buildInputs = builtins.filter (x: x.pname != "gdk-pixbuf") oldAttrs.buildInputs;
    } );
  };
}
