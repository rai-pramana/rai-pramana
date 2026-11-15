<!--
  ⛩️  RAI PRAMANA — ライ・プラマナ
  間 · ma — the space between. Restraint over ornament.

  DUAL THEME — every widget is wrapped in <picture>, so light-theme visitors get a
  white card instead of a dark navy slab on a white page. GitHub wraps these in
  <themed-picture> itself and swaps sources on theme toggle.

  PALETTE — one accent only: muted gold. No saturated red anywhere in the widgets.

  dark : ink #1a1b27 · soft gold #D8BD8A (titles) · muted gold #B08D57 (icons)
         text #c9d1d9 · border #353A47 · deep ink #141520 (hero vignette)
  light: white #ffffff · soft gold #8A6A2F · muted copper #8A6428
         text #24292f · border #DCDCDC

  Why muted: #F7C948 and #E60012 read as toy-bright at 546px and fought the
  neo-Tokyo ink. Dropping them to #D8BD8A / #B08D57 keeps contrast (4.6:1 on
  ink) while letting the seigaiha texture and crest carry the theme instead of
  the colour shouting over it.

  Auto : 3D contributions + snake, regenerated daily by GitHub Actions.

  Editing notes (learned the hard way):
  · every block sits in its own <p>: inside a <div>, blank lines do NOT create
    paragraphs and GitHub strips style=, so widgets collapse to ~5px gaps
  · no <text> in any local SVG: the name is HTML, so a font/cache/proxy
    failure can never blank it out
  · paired cards need align="top" (154px vs 195px natural height) or they
    bottom-align and look broken
  · repo descriptions must stay ASCII: an em-dash shows up as a literal backslash-u2014
  · never bulk-replace <img> tags — rewrite the file and assert src+alt on each
  · snake light file is output/snake.svg (NOT snake-light.svg)
-->

<div align="center">

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/hero-dark.svg?v=4" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/hero-light.svg?v=4" />
  <img src="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/hero-dark.svg?v=4" width="100%" alt="" />
</picture>

<h1 align="center">Rai Pramana</h1>

<p><a href="https://github.com/rai-pramana"><img src="https://readme-typing-svg.demolab.com?font=Zen+Maru+Gothic&weight=600&size=24&duration=2600&pause=2800&color=D8BD8A&center=true&vCenter=true&width=700&height=48&lines=%E3%81%93%E3%82%93%E3%81%AB%E3%81%A1%E3%81%AF%E3%80%81%E3%83%A9%E3%82%A4%E3%81%A8%E3%82%82%E3%81%86%E3%81%97%E3%81%BE%E3%81%99;Software%20Engineer%20%C2%B7%20Data%20Engineer" alt="Typing SVG" /></a></p>

<p>
<img src="https://komarev.com/ghpvc/?username=rai-pramana&label=%E9%96%B2%E8%A6%A7%E8%80%85&color=B08D57&style=flat-square&labelColor=1a1b27" height="20" alt="Profile views" />
&nbsp;
<img src="https://img.shields.io/github/followers/rai-pramana?style=flat-square&logo=github&logoColor=D8BD8A&label=%E3%83%95%E3%82%A9%E3%83%AD%E3%83%AF%E3%83%BC&labelColor=1a1b27&color=B08D57" height="20" alt="Followers" />
&nbsp;
<a href="https://github.com/rai-pramana"><img src="https://img.shields.io/badge/GitHub-rai--pramana-181717?style=flat-square&logo=github&logoColor=D8BD8A&labelColor=1a1b27" height="20" alt="GitHub" /></a>
&nbsp;
<a href="https://medium.com/@rai-pramana"><img src="https://img.shields.io/badge/Medium-rai--pramana-1a1b27?style=flat-square&logo=medium&logoColor=D8BD8A&labelColor=353A47" height="20" alt="Medium" /></a>
</p>

<hr />

</div>

## 技術 · Stack

<div align="center">

<p><img src="https://cdn.simpleicons.org/python/B08D57" height="30" alt="Python" />&nbsp;<img src="https://cdn.simpleicons.org/openjdk/B08D57" height="30" alt="Java" />&nbsp;<img src="https://cdn.simpleicons.org/typescript/B08D57" height="30" alt="TypeScript" />&nbsp;<img src="https://cdn.simpleicons.org/javascript/B08D57" height="30" alt="JavaScript" />&nbsp;<img src="https://cdn.simpleicons.org/c/B08D57" height="30" alt="C" />&nbsp;<img src="https://cdn.simpleicons.org/php/B08D57" height="30" alt="PHP" />&nbsp;<img src="https://cdn.simpleicons.org/html5/B08D57" height="30" alt="HTML" />&nbsp;<img src="https://cdn.simpleicons.org/css/B08D57" height="30" alt="CSS" /></p>
<p><img src="https://cdn.simpleicons.org/nextdotjs/8A6428" height="30" alt="Next.js" />&nbsp;<img src="https://cdn.simpleicons.org/react/B08D57" height="30" alt="React" />&nbsp;<img src="https://cdn.simpleicons.org/nodedotjs/B08D57" height="30" alt="Node.js" />&nbsp;<img src="https://cdn.simpleicons.org/nestjs/B08D57" height="30" alt="NestJS" />&nbsp;<img src="https://cdn.simpleicons.org/express/B08D57" height="30" alt="Express" />&nbsp;<img src="https://cdn.simpleicons.org/laravel/8A6428" height="30" alt="Laravel" />&nbsp;<img src="https://cdn.simpleicons.org/tailwindcss/B08D57" height="30" alt="Tailwind CSS" /></p>
<p><img src="https://cdn.simpleicons.org/pytorch/B08D57" height="30" alt="PyTorch" />&nbsp;<img src="https://cdn.simpleicons.org/tensorflow/B08D57" height="30" alt="TensorFlow" />&nbsp;<img src="https://cdn.simpleicons.org/scikitlearn/B08D57" height="30" alt="scikit-learn" />&nbsp;<img src="https://cdn.simpleicons.org/opencv/B08D57" height="30" alt="OpenCV" />&nbsp;<img src="https://cdn.simpleicons.org/mysql/B08D57" height="30" alt="MySQL" />&nbsp;<img src="https://cdn.simpleicons.org/postgresql/B08D57" height="30" alt="PostgreSQL" />&nbsp;<img src="https://cdn.simpleicons.org/git/B08D57" height="30" alt="Git" />&nbsp;<img src="https://cdn.simpleicons.org/docker/B08D57" height="30" alt="Docker" />&nbsp;<img src="https://cdn.simpleicons.org/linux/B08D57" height="30" alt="Linux" /></p>

</div>

## 作品 · Selected Work

<div align="center">

<p><a href="https://github.com/rai-pramana/Biblio"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Biblio&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Biblio&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Biblio&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="Biblio" />
</picture></a>&nbsp;<a href="https://github.com/rai-pramana/Holic-Barbershop"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Holic-Barbershop&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Holic-Barbershop&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Holic-Barbershop&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="Holic-Barbershop" />
</picture></a></p>

<p><a href="https://github.com/rai-pramana/NyankoGarage"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=NyankoGarage&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=NyankoGarage&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=NyankoGarage&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="NyankoGarage" />
</picture></a>&nbsp;<a href="https://github.com/rai-pramana/Vehicle-AccidentYoloApp"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Vehicle-AccidentYoloApp&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Vehicle-AccidentYoloApp&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=rai-pramana&repo=Vehicle-AccidentYoloApp&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="Vehicle-AccidentYoloApp" />
</picture></a></p>

<p><a href="https://github.com/Kampus-Merdeka-Software-Engineering/BE-2-Medan-14"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=BE-2-Medan-14&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=BE-2-Medan-14&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=BE-2-Medan-14&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="BE-2-Medan-14" />
</picture></a>&nbsp;<a href="https://github.com/Kampus-Merdeka-Software-Engineering/FE-2-Medan-14"><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=FE-2-Medan-14&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=FE-2-Medan-14&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true&border_color=DCDCDC&description_lines_count=2&show_owner=false" />
  <img src="https://gh-readme-stats.vercel.app/api/pin/?username=Kampus-Merdeka-Software-Engineering&repo=FE-2-Medan-14&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true&border_color=353A47&description_lines_count=2&show_owner=false" width="345" align="top" alt="FE-2-Medan-14" />
</picture></a></p>

</div>

| Project | Summary | Stack |
| :-- | :-- | :-: |
| [**Biblio**](https://github.com/rai-pramana/Biblio) | Aplikasi Android review dan manajemen koleksi buku | <img src="https://cdn.simpleicons.org/android/B08D57" height="20" alt="android" /> <img src="https://cdn.simpleicons.org/openjdk/B08D57" height="20" alt="java" /> |
| [**Holic-Barbershop**](https://github.com/rai-pramana/Holic-Barbershop) | Sistem antrean barbershop online: QR check-in, status real-time, push notification | <img src="https://cdn.simpleicons.org/laravel/8A6428" height="20" alt="laravel" /> <img src="https://cdn.simpleicons.org/mysql/B08D57" height="20" alt="mysql" /> <img src="https://cdn.simpleicons.org/tailwindcss/B08D57" height="20" alt="tailwindcss" /> |
| [**NyankoGarage**](https://github.com/rai-pramana/NyankoGarage) | Garage management system: produk, stok, transaksi, real-time | <img src="https://cdn.simpleicons.org/nextdotjs/8A6428" height="20" alt="nextdotjs" /> <img src="https://cdn.simpleicons.org/nestjs/B08D57" height="20" alt="nestjs" /> <img src="https://cdn.simpleicons.org/postgresql/B08D57" height="20" alt="postgresql" /> |
| [**Vehicle-AccidentYoloApp**](https://github.com/rai-pramana/Vehicle-AccidentYoloApp) | Deteksi kecelakaan dari feed kamera dengan YOLO + notebook eksperimen | <img src="https://cdn.simpleicons.org/ultralytics/8A6428" height="20" alt="ultralytics" /> <img src="https://cdn.simpleicons.org/python/B08D57" height="20" alt="python" /> <img src="https://cdn.simpleicons.org/jupyter/8A6428" height="20" alt="jupyter" /> |
| [**BE-2-Medan-14**](https://github.com/Kampus-Merdeka-Software-Engineering/BE-2-Medan-14) | REST API booking hotel, capstone Kampus Merdeka | <img src="https://cdn.simpleicons.org/nodedotjs/B08D57" height="20" alt="nodedotjs" /> <img src="https://cdn.simpleicons.org/express/B08D57" height="20" alt="express" /> |
| [**FE-2-Medan-14**](https://github.com/Kampus-Merdeka-Software-Engineering/FE-2-Medan-14) | Frontend booking hotel, capstone Kampus Merdeka | <img src="https://cdn.simpleicons.org/html5/B08D57" height="20" alt="html5" /> <img src="https://cdn.simpleicons.org/css/B08D57" height="20" alt="css" /> <img src="https://cdn.simpleicons.org/javascript/B08D57" height="20" alt="javascript" /> |

## 記録 · Stats

<div align="center">

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api?username=rai-pramana&show_icons=true&include_all_commits=true&count_private=true&rank_icon=github&card_width=345&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api?username=rai-pramana&show_icons=true&include_all_commits=true&count_private=true&rank_icon=github&card_width=345&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&icon_color=8A6428&hide_border=true" />
  <img src="https://gh-readme-stats.vercel.app/api?username=rai-pramana&show_icons=true&include_all_commits=true&count_private=true&rank_icon=github&card_width=345&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true" width="345" align="top" alt="GitHub stats" />
</picture>&nbsp;<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://streak-stats.demolab.com?user=rai-pramana&background=1a1b27&border=353A47&stroke=B08D57&ring=D8BD8A&fire=B08D57&currStreakNum=D8BD8A&currStreakLabel=D8BD8A&sideNums=c9d1d9&sideLabels=c9d1d9&dates=8b949e&hide_border=true&card_width=345" />
  <source media="(prefers-color-scheme: light)" srcset="https://streak-stats.demolab.com?user=rai-pramana&background=ffffff&border=DCDCDC&stroke=8A6428&ring=8A6A2F&fire=8A6428&currStreakNum=8A6A2F&currStreakLabel=8A6A2F&sideNums=24292f&sideLabels=24292f&dates=6e7781&hide_border=true&card_width=345" />
  <img src="https://streak-stats.demolab.com?user=rai-pramana&background=1a1b27&border=353A47&stroke=B08D57&ring=D8BD8A&fire=B08D57&currStreakNum=D8BD8A&currStreakLabel=D8BD8A&sideNums=c9d1d9&sideLabels=c9d1d9&dates=8b949e&hide_border=true&card_width=345" width="345" align="top" alt="Streak stats" />
</picture></p>

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://gh-readme-stats.vercel.app/api/top-langs/?username=rai-pramana&layout=compact&langs_count=9&hide=jupyter%20notebook&card_width=437&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true" />
  <source media="(prefers-color-scheme: light)" srcset="https://gh-readme-stats.vercel.app/api/top-langs/?username=rai-pramana&layout=compact&langs_count=9&hide=jupyter%20notebook&card_width=437&bg_color=ffffff&title_color=8A6A2F&text_color=24292f&hide_border=true" />
  <img src="https://gh-readme-stats.vercel.app/api/top-langs/?username=rai-pramana&layout=compact&langs_count=9&hide=jupyter%20notebook&card_width=437&bg_color=1a1b27&title_color=D8BD8A&text_color=c9d1d9&icon_color=B08D57&hide_border=true" width="437" alt="Top languages" />
</picture></p>

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://activitygraph.vercel.app/graph?username=rai-pramana&bg_color=1a1b27&color=D8BD8A&line=B08D57&point=D8BD8A&area=true&area_color=D8BD8A&hide_border=true" />
  <source media="(prefers-color-scheme: light)" srcset="https://activitygraph.vercel.app/graph?username=rai-pramana&bg_color=ffffff&color=8A6A2F&line=8A6428&point=8A6428&area=true&area_color=8A6A2F&hide_border=true" />
  <img src="https://activitygraph.vercel.app/graph?username=rai-pramana&bg_color=1a1b27&color=D8BD8A&line=B08D57&point=D8BD8A&area=true&area_color=D8BD8A&hide_border=true" width="780" alt="Activity graph" />
</picture></p>

</div>

## 3D 貢献 · Contributions

<div align="center">

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/profile-3d-contrib/profile-custom.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/profile-3d-contrib/profile-custom-light.svg" />
  <img src="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/profile-3d-contrib/profile-custom.svg" width="780" alt="3D contribution graph" />
</picture></p>

</div>

## 蛇 · Snake

<div align="center">

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/output/snake-dark.svg" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/output/snake.svg" />
  <img width="780" alt="Snake eating my contribution graph" src="https://raw.githubusercontent.com/rai-pramana/rai-pramana/output/snake-dark.svg" />
</picture></p>

</div>

<div align="center">

<p><sub>一期一会 · よろしくお願いします</sub></p>

</div>

<p><picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/seigaiha-dark.svg?v=2" />
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/seigaiha-light.svg?v=2" />
  <img src="https://raw.githubusercontent.com/rai-pramana/rai-pramana/main/assets/seigaiha-dark.svg?v=2" width="100%" alt="" />
</picture></p>
