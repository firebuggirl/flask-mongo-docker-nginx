## Github yamllint => https://github.com/adrienverge/yamllint

  - Written in Python (compatible with Python 2 & 3).

      ` pip install --user yamllint `

     - NOTE: pip not auto installed on Mac OSX => run:

      ` brew install yamllint ` => see Docs => https://yamllint.readthedocs.io/en/stable/quickstart.html


  - yamllint is also packaged for all major operating systems, see installation examples (dnf, apt-get...) in the documentation.

  - `Usage`:

    - Lint one or more files

      ` yamllint my_file.yml my_other_file.yaml ... `

    - Lint all YAML files in a directory

      ` yamllint . `

    - Use a pre-defined lint configuration

      ` yamllint -d relaxed file.yaml `

    - Use a custom lint configuration

      ` yamllint -c /path/to/myconfig file-to-lint.yaml `

    - Output a parsable format (for syntax checking in editors like Vim, emacs...)

      ` yamllint -f parsable file.yaml `

    - Read more in the complete documentation:

      https://yamllint.readthedocs.io/en/stable/
