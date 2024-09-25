{
  description = "A Nix-flake-based Python development environment";

  inputs.nixpkgs.url = "github:nixos/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      supportedSystems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forEachSupportedSystem = f: nixpkgs.lib.genAttrs supportedSystems (system: f {
        pkgs = import nixpkgs { inherit system; config.allowUnfree = true;};
      });
    in
    {
      devShells = forEachSupportedSystem ({ pkgs }: {
        default = pkgs.mkShell {
          packages = with pkgs; [ python311 zlib lz4 python-launcher elasticsearch ] ++
            (with pkgs.python311Packages; [
              pip
              pyright
              pylint
              pyflakes
              pytest
              numpy
              scikit-learn
              nltk
              requests
              waitress
              flask
            ]);
        };
      });
    };
}

