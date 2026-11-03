# Fonts shipped with inua

`MapleMono-NF-CN-Regular.ttf` and `MapleMono-NF-CN-Bold.ttf` are Maple Mono
NF CN from the Maple Mono project
(https://github.com/subframe7536/maple-font), version 7.9. They cover Latin,
Greek, Cyrillic, Simplified and Traditional Chinese, Japanese, and the Nerd
Fonts icon ranges, so one family serves the shell, its apps and a terminal
with prompts that draw icons. Korean comes from the Noto fallback in the
same font stack.

Licensed under the SIL Open Font License 1.1; the licence is in
`OFL-MapleMono.txt`. `make install` copies them to
`$XDG_DATA_HOME/fonts/inua`, where fontconfig finds them.

The Noto Sans CJK and Noto Serif CJK choices in Settings use the system's
fonts (`fonts-noto-cjk`, installed by `make deps`); they are not bundled.
