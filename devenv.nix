{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  packages = [
    pkgs.git
    pkgs.bash
  ];

  languages.python.enable = true;
  languages.python.uv.enable = true;
  languages.python.uv.package = pkgs.uv;
  languages.python.uv.sync.enable = true;
  languages.python.uv.sync.allExtras = true;
  languages.python.venv.enable = true;
  languages.python.version = "3.12";

  scripts.generate-model.exec = ''
    ./source/model/generate_model.sh
  '';

  git-hooks.hooks = {
    shellcheck.enable = true;
    black.enable = true;
    typos.enable = true;
    yamllint.enable = true;
    yamlfmt.enable = true;
    check-toml.enable = true;
    commitizen.enable = true;
    nixfmt-rfc-style.enable = true;
    markdownlint.enable = true;
  };

  scripts.format.exec = ''
    yamlfmt .
    markdownlint --fix .
    pre-commit run --all-files
  '';

  scripts.test-all.exec = ''
    pytest -s -vv "$@"
  '';

  enterTest = ''
    test-all
  '';

  scripts.build.exec = ''
    uv build
  '';

  scripts.sample-pipeline-run.exec = ''
    python morphais_pipeline.py
  '';

  scripts.sample-pipeline-show.exec = ''
    dlt pipeline morphais_pipeline show
  '';
}
