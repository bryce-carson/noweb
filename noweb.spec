##  noweb.spec -- OpenPKG RPM Package Specification
##  Copyright (c) 2000-2005 OpenPKG Foundation e.V. <http://openpkg.net/>
##  Copyright (c) 2000-2005 Ralf S. Engelschall <http://engelschall.com/>
##  Copyright (c) 2016-2025 Dilawar Singh <dilawars@ncbs.res.in>
##  Copyright (c) 2025      Bryce Carson <bryce.a.carson@gmail.com>
##
##  Permission to use, copy, modify, and distribute this software for
##  any purpose with or without fee is hereby granted, provided that
##  the above copyright notice and this permission notice appear in all
##  copies.
##
##  THIS SOFTWARE IS PROVIDED ``AS IS'' AND ANY EXPRESSED OR IMPLIED
##  WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF
##  MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
##  IN NO EVENT SHALL THE AUTHORS AND COPYRIGHT HOLDERS AND THEIR
##  CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
##  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
##  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF
##  USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
##  ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
##  OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT
##  OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF
##  SUCH DAMAGE.

%global forgeurl https://github.com/bryce-carson/noweb/
%global commit 50840b12b87af91fe9aea6b4979ea7f71286b5be
%forgemeta

%global debug_package %{nil}

%global noweb_make_variables CFLAGS="%{optflags} -Werror" LIBSRC=icon IPATH=/usr/lib64/icon BIN=%{_bindir} MAN=%{_mandir} LIB=%{_libexecdir}/noweb TEXINPUTS=%{_datadir}/texmf/tex/latex/noweb ELISP=%{_emacs_sitelispdir}/noweb GITVERSION=%{commit}

Name:          noweb
Version:       %commit
Summary:       A Simple, Extensible Tool for Literate Programming
License:       BSD-2-Clause OR Noweb
URL:           https://www.cs.tufts.edu/~nr/noweb/

Release:       %autorelease
Source:        %{forgesource}

BuildRequires: gcc icon gawk sed texlive texlive-kpathsea coreutils
Requires:      icon gawk emacs-filesystem texlive texlive-kpathsea

%description
"Literate programming is the art of preparing programs for human readers. Noweb
is designed to meet the needs of literate programmers while remaining as simple
as possible. Its primary advantages are simplicity, extensibility, and
language-independence. noweb uses 5 control sequences to WEB's 27. The noweb
manual is only 3 pages; an additional page explains how to customize its LaTeX
output. Noweb works \"out of the box\" with any programming language, and supports
TeX, LaTeX, HTML, and troff back ends." ---- Norman Ramsey

%prep
%forgesetup
cd src
./awkname gawk

%build
unset RUSTFLAGS # reduce the rust so I can breathe.
%make_build -C src %noweb_make_variables boot all

%install
%make_build -C src %noweb_make_variables DESTDIR=%{buildroot} install

%check
# Noweb is distributed with pre-tangled C and Icon sources to allow compilation
# without a pre-existing installation of Noweb; that's how the bootstrapping
# problem is solved. The clobber goal will remove all of the distributed C and
# Icon sources, requiring Noweb to tangle these for the programs to be built
# again. This makes an effective test.
%make_build -C src %noweb_make_variables check-tex clobber all

%files
%{_bindir}/noweb
%{_bindir}/notangle
%{_bindir}/noweave
%{_bindir}/nountangle
%{_bindir}/nodefs
%{_bindir}/noroots
%{_bindir}/nuweb2noweb
%{_bindir}/cpif
%{_bindir}/htmltoc
%{_bindir}/noroff
%{_bindir}/noindex
%{_bindir}/sl2h

%dir %{_libexecdir}/noweb
%{_libexecdir}/noweb/*

%dir %{_datadir}/texmf/tex/latex/noweb
%{_datadir}/texmf/tex/latex/noweb/noweb.sty
%{_datadir}/texmf/tex/latex/noweb/nwmac.tex

%dir %{_emacs_sitelispdir}/noweb
%{_emacs_sitelispdir}/noweb/noweb-mode.el

%doc %{_mandir}/man1
%doc %{_mandir}/man7

%changelog
%autochangelog
