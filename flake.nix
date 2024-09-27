{
  description = "jupyter server";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = import nixpkgs { inherit system; };
        pythonEnv = pkgs.python311.withPackages (ps: with ps; [
          pip
          h5py
          imutils
          matplotlib
          numpy
          opencv4
          pillow
          scikit-image
          scikit-learn
          scipy
          torch
          torchvision
          torchsummary
          flask
          waitress
          sqlalchemy
        ]);
        systemPackages = with pkgs; [
          pyright
          python-launcher
        ];
        musicCRS = pkgs.stdenv.mkDerivation {
          pname = "musicCRS-server";
          name = "musicCRS-server";
          buildInputs = [ pythonEnv ] ++ systemPackages;
          src=self;
          # Create a script to start Jupyter Notebook
          installPhase = ''
            mkdir -p $out/bin
            cat > $out/bin/musicCRS-server << EOF
            #!/usr/bin/env bash
            ${pythonEnv}/bin/python ./website/main.py
            EOF
            chmod +x $out/bin/musicCRS-server
          '';
        };
      in rec {
        devShell = pkgs.mkShell {
          buildInputs = [ pythonEnv ] ++ systemPackages;
        };
        packages.default = musicCRS;

        apps.default = {
          type = "app";
          drv = musicCRS;
          program = "${musicCRS}/bin/musicCRS-server";
        };
      });
}
