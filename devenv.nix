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
    ./dlt_source_morphais/model/generate_model.sh
  '';

  scripts.update-spec.exec = ''
    GIT_MERGE_AUTOEDIT=no \
      git subtree pull \
      --prefix dlt_source_morphais/model/spec \
      https://github.com/planet-a-ventures/morphais-openapi-spec.git \
      main \
      --squash
  '';

  scripts.refresh-model.exec = ''
    set -euo pipefail
    update-spec
    generate-model
    git add dlt_source_morphais/model/spec.py
    git commit -m'chore: update model'
  '';

  git-hooks.hooks = {
    shellcheck.enable = true;
    black.enable = true;
    typos.enable = true;
    yamllint.enable = true;
    yamlfmt.enable = true;
    yamlfmt.settings.lint-only = false;
    check-toml.enable = true;
    commitizen.enable = true;
    nixfmt-rfc-style.enable = true;
    mdformat.enable = true;
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
