{
  pkgs,
  lib,
  config,
  inputs,
  ...
}:

{
  # https://devenv.sh/packages/
  packages = [
    pkgs.git
  ];

  scripts.format.exec = ''
    markdownlint --fix .
    pre-commit run --all-files
  '';

  # https://devenv.sh/pre-commit-hooks/
  git-hooks.hooks = {
    typos.enable = true;
    yamllint.enable = true;
    yamlfmt.enable = true;
    yamlfmt.settings.lint-only = false;
    commitizen.enable = true;
    nixfmt-rfc-style.enable = true;
    markdownlint.enable = true;
    mdformat.enable = true;
    openapi-spec-validator.enable = true;
  };
}
